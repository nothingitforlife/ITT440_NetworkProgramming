import socket
import struct
import time

# Server configuration
server_ip = "127.0.0.1"
server_port = 123

ntp_epoch = 2208988800


# Get current NTP timestamp
def get_ntp_time():

    current_time = time.time_ns()

    seconds, nanoseconds = divmod(
        current_time, 1000000000
    )

    ntp_seconds = seconds + ntp_epoch

    ntp_fraction = (
        nanoseconds * (2**32)
    ) // 1000000000

    return struct.pack(
        "!II",
        ntp_seconds & 0xFFFFFFFF,
        ntp_fraction
    )


# Create NTP response
def create_response(request, receive_time):

    response = bytearray(48)

    # LI = 3, Version = 4, Mode = 4
    response[0] = (3 << 6) | (4 << 3) | 4

    # Server information
    response[1] = 16
    response[2] = 4

    struct.pack_into("!b", response, 3, -20)

    # Copy client transmit timestamp
    response[24:32] = request[40:48]

    # Insert server timestamps
    response[32:40] = receive_time
    response[40:48] = get_ntp_time()

    return bytes(response)


# Main server program
def main():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    server.bind((server_ip, server_port))

    print("NTP Server started")
    print("IP Address:", server_ip)
    print("Port:", server_port)
    print("Waiting for client request...")

    try:

        while True:

            # Receive client request
            data, address = server.recvfrom(1024)

            receive_time = get_ntp_time()

            print("\nRequest received from:", address)

            if len(data) < 48:
                print("Invalid packet")
                continue

            version = (data[0] >> 3) & 7
            mode = data[0] & 7

            print("NTP Version:", version)
            print("Client Mode:", mode)

            if version not in (3, 4) or mode != 3:
                print("Invalid NTP request")
                continue

            # Create response packet
            response = create_response(data, receive_time)

            # Send response to client
            server.sendto(response, address)

            print("Response sent successfully")
            print("Response size:", len(response), "bytes")

    except KeyboardInterrupt:
        print("\nServer stopped")

    finally:
        server.close()


if __name__ == "__main__":
    main()
