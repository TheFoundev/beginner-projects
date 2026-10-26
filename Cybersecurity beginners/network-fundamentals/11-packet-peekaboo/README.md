# Project 11 — Packet Peekaboo: Watch Your Own Traffic

**Track:** Network Fundamentals  
**Type:** Coding (Python + Scapy) + Wireshark  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

The internet is a giant postal system, and your data travels in small envelopes
called packets. Wireshark is a slow-motion camera for those envelopes. This
project gives you a safe synthetic capture to explore first, then a script to
capture your own traffic in a limited, ethical way.

## What the code does

| File | Purpose |
|---|---|
| `make_sample_pcap.py` | Builds a safe PCAP with DNS, HTTPS, and plaintext HTTP |
| `analyze_pcap.py` | Summarizes packets, DNS names, protocols, and HTTP payloads |
| `capture_packets.py` | Captures a small number of packets from **your own** machine |
| `samples/demo.pcap` | Ready-made synthetic capture |

The demo packets use reserved example addresses and never touch the internet.

## Install

```powershell
cd "C:\Foundev\Cybersecurity beginners\network-fundamentals\11-packet-peekaboo"
py -3 -m pip install -r requirements.txt
```

On Windows, Scapy also needs **Npcap**. Installing Wireshark includes it. Run
the terminal as Administrator if capture permissions fail.

## Run it

```powershell
# Analyze the included sample
py -3 analyze_pcap.py --demo

# Rebuild the sample if you want
py -3 make_sample_pcap.py

# Open the sample in Wireshark
# (install Wireshark, then File -> Open -> samples/demo.pcap)

# Capture your own traffic (your machine only)
py -3 capture_packets.py --list-interfaces
py -3 capture_packets.py --count 20 --output samples/my_capture.pcap
py -3 analyze_pcap.py samples/my_capture.pcap
```

## Wireshark filters to try

| Filter | What it shows |
|---|---|
| `dns` | Name lookups |
| `tls` | Encrypted HTTPS traffic |
| `http` | Plaintext web traffic |
| `ip.addr == 93.184.216.34` | Traffic to one address |
| `tcp.port == 443` | HTTPS connections |

## Experiments to try

1. Which DNS name appears in the sample? What IP address does it resolve to?
2. Find the plaintext HTTP request. What would an observer learn from it?
3. Compare the port 443 packet with the port 80 packet. What is different?
4. Capture your own DNS traffic while opening a site. What names show up?
5. Explain why HTTPS still leaks some metadata (such as the destination IP and
   often the domain name) even though the content is encrypted.

## What you learn

- Packets, protocols, ports, and DNS.
- Why TLS matters on untrusted networks.
- How to capture and analyze traffic safely and ethically.

## Safety

- Capture **only your own** traffic, on your own machine and network.
- Do not capture on a school, workplace, or public network without written
  permission.
- Promiscuous mode is disabled on purpose.
- PCAP files can contain private data. Keep them local and delete them when done.
