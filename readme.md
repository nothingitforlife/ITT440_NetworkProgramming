# Development of NTP Client-Server Using Python Raw UDP Socket Programming

A simple NTPv4 client and server written in Python using raw UDP sockets (no external NTP library). The client sends a 48-byte NTP request, the server replies with its timestamps, and the client calculates network delay and clock offset. Built for learning how the NTP packet format and time synchronisation work.

**Course Project** — ITT440 Network Programming, Bachelor of Computer Science (Hons.) Computer Networks, Fakulti Sains Komputer, Universiti Teknologi MARA (UiTM) Shah Alam
**Student:** Luqman Hakim bin Zulkifli (2024676746)
**Lecturer:** Dr. Shaiful Bakhtiar bin Rodzman

## Demo Video

▶️ https://drive.google.com/file/d/1i3Gvhv2wkMSPrgLEbVmEWRqQ7v2VBX98/view?usp=sharing


## Features

- NTPv4 packet handling over IPv4 UDP (48-byte packets, port 123)
- Server validates requests (minimum length, version 3 or 4, client mode 3)
- Server records receive time (T2) and transmit time (T3) as 64-bit NTP timestamps
- Client checks that the origin timestamp in the reply matches its own request
- Client calculates **network delay** and **clock offset** using T1, T2, T3, T4
- Displays server time converted to Malaysia time (Asia/Kuala_Lumpur)
- Reports clock status from the Leap Indicator and stratum (LI 3 / stratum 16 = unsynchronized)
- 5-second client timeout handling

## How It Works

```
Client                         Server
  |  --- request (T1) ------>   |
  |                             |  T2 = receive time
  |                             |  T3 = transmit time
  |  <--- response (T2, T3) --- |
  T4 = receive time

delay  = (T4 - T1) - (T3 - T2)
offset = ((T2 - T1) + (T3 - T4)) / 2
```

## Tech Stack

- Python 3.9 or newer (`zoneinfo` is used)
- Standard library only: `socket`, `struct`, `time`, `datetime`, `zoneinfo`
- Tested on Ubuntu (WSL2), client and server on the same computer via localhost

## Getting Started

### Prerequisites

- Python 3.9+
- Linux / WSL2 recommended
- Root permission (`sudo`) to run the server, because port 123 is a privileged port (below 1024)

### Installation

```bash
git clone https://github.com/nothingitforlife/ITT440_NetworkProgramming.git
cd ~/ITT440_NetworkProgramming
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

No `.env` file is needed. The server address and port are set at the top of both files:

```python
server_ip = "127.0.0.1"
server_port = 123
```

### Run

Open two terminals.

**Terminal 1 — start the server** (port 123 needs sudo; use the venv's Python):

```bash
sudo venv/bin/python ntp_server.py
```

**Terminal 2 — run the client:**

```bash
python3 ntp_client.py
```

### Sample Output (client)

```
NTP request sent
NTP response received
Packet size: 48 bytes

NTP Server Information
Version: 4
Mode: 4
Stratum: 16
Leap Indicator: 3
Origin timestamp: Matched

NTP Calculation
Network Delay: <x> ms
Clock Offset: <x> ms

Clock Status: Unsynchronized
```

> The server intentionally reports stratum 16 and LI 3, so the client shows "Unsynchronized".

## Project Structure

```
<repo>/
├── ntp_server.py      # UDP server: receives request, replies with T2 and T3
├── ntp_client.py      # UDP client: sends request, calculates delay and offset
├── requirements.txt
├── .gitignore
├── docs/
│   └── screenshots/
└── README.md
```

## Acknowledgements

- Dr. Shaiful Bakhtiar bin Rodzman, lecturer for ITT440 Network Programming
- RFC 5905 — Network Time Protocol Version 4
- Python documentation: `socket`, `struct`, `zoneinfo`

## License

This project was developed for academic purposes at Universiti Teknologi MARA (UiTM) Shah Alam.
