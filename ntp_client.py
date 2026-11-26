
import socket
import struct
import time
import datetime
from zoneinfo import ZoneInfo

# Server configuration
server_ip = "127.0.0.1"
server_port = 123

ntp_epoch = 2208988800


# Convert NTP timestamp to seconds
def convert_timestamp(timestamp):

    seconds, fraction = struct.unpack(
        "!II", timestamp
    )

    return seconds + fraction / (2**32)


# Create NTP request
packet = bytearray(48)

# LI = 0, Version = 4, Mode = 3
packet[0] = (0 << 6) | (4 << 3) | 3

# Get client timestamp
current_time = time.time_ns()

seconds, nanoseconds = divmod(
    current_time, 1000000000
)

ntp_seconds = seconds + ntp_epoch

ntp_fraction = (
    nanoseconds * (2**32)
) // 1000000000

# Insert client transmit timestamp
struct.pack_into(
    "!II",
    packet,
    40,
    ntp_seconds & 0xFFFFFFFF,
    ntp_fraction
)

# Record client send time (T1)
t1 = convert_timestamp(packet[40:48])


# Create UDP socket
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

client.settimeout(5)

try:

    # Send request
    client.sendto(packet, (server_ip, server_port))

    print("NTP request sent")

    # Receive server response
    response, address = client.recvfrom(1024)

    # Record client receive time (T4)
    receive_ns = time.time_ns()

    seconds, nanoseconds = divmod(
        receive_ns, 1000000000
    )

    t4 = (
        seconds + ntp_epoch
        + nanoseconds / 1000000000
    )

    print("NTP response received")
    print("Server address:", address)
    print("Packet size:", len(response), "bytes")

    if len(response) < 48:
        print("Invalid NTP response")

    else:

        # Read server information
        li = (response[0] >> 6) & 3
        version = (response[0] >> 3) & 7
        mode = response[0] & 7
        stratum = response[1]

        print("\nNTP Server Information")
        print("Version:", version)
        print("Mode:", mode)
        print("Stratum:", stratum)
        print("Leap Indicator:", li)

        # Check origin timestamp
        if response[24:32] == packet[40:48]:
            print("Origin timestamp: Matched")
        else:
            print("Origin timestamp: Not matched")

        # Read server timestamps
        t2 = convert_timestamp(response[32:40])
        t3 = convert_timestamp(response[40:48])

        # Calculate network delay
        delay = (t4 - t1) - (t3 - t2)

        # Calculate clock offset
        offset = ((t2 - t1) + (t3 - t4)) / 2

        print("\nNTP Calculation")
        print("Network Delay:", round(delay * 1000, 3), "ms")
        print("Clock Offset:", round(offset * 1000, 3), "ms")

        # Read server transmit timestamp
        seconds, fraction = struct.unpack(
            "!II", response[40:48]
        )

        unix_time = (
            seconds - ntp_epoch
            + fraction / (2**32)
        )

        server_time = datetime.datetime.fromtimestamp(
            unix_time,
            ZoneInfo("Asia/Kuala_Lumpur")
        )

        print("\nServer Time (Malaysia):", server_time)

        if li == 3 or stratum == 16:
            print("Clock Status: Unsynchronized")
        else:
            print("Clock Status: Synchronized")

except socket.timeout:
    print("Server response timeout")

finally:
    client.close()
