#!/usr/bin/env python3
"""
Project 11 - Packet Peekaboo: Watch Your Own Traffic
===================================================

Build a small, safe PCAP file containing a DNS lookup and two web requests.
Then open it in Wireshark or run analyze_pcap.py to see what a packet capture
can reveal.

Install:
    py -3 -m pip install -r requirements.txt

Run:
    py -3 make_sample_pcap.py
    py -3 analyze_pcap.py samples/demo.pcap

The sample uses reserved example addresses (192.0.2.0/24, 93.184.216.34) and
never touches a real network.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scapy.all import DNS, DNSQR, DNSRR, Ether, IP, Raw, TCP, UDP, wrpcap
except ImportError:
    print("This project needs Scapy.")
    print("Install it with: py -3 -m pip install -r requirements.txt")
    raise SystemExit(1)


CLIENT_IP = "192.0.2.10"
DNS_IP = "192.0.2.53"
WEB_IP = "93.184.216.34"
CLIENT_MAC = "02:00:00:00:00:10"
GATEWAY_MAC = "02:00:00:00:00:01"
DOMAIN = "example.com"


def create_demo_pcap(output: Path) -> list:
    """Create four synthetic packets and save them as a PCAP file."""
    packets = []

    # 1. The client asks DNS: "What is the address of example.com?"
    dns_query = (
        Ether(src=CLIENT_MAC, dst=GATEWAY_MAC)
        / IP(src=CLIENT_IP, dst=DNS_IP)
        / UDP(sport=53000, dport=53)
        / DNS(id=1234, rd=1, qd=DNSQR(qname=DOMAIN, qtype="A"))
    )
    packets.append(dns_query)

    # 2. The DNS server answers with an A record.
    dns_answer = (
        Ether(src=GATEWAY_MAC, dst=CLIENT_MAC)
        / IP(src=DNS_IP, dst=CLIENT_IP)
        / UDP(sport=53, dport=53000)
        / DNS(
            id=1234,
            qr=1,
            aa=0,
            rd=1,
            ra=1,
            qd=DNSQR(qname=DOMAIN, qtype="A"),
            an=DNSRR(rrname=DOMAIN, type="A", ttl=300, rdata=WEB_IP),
        )
    )
    packets.append(dns_answer)

    # 3. A normal HTTPS connection begins with a TCP SYN to port 443.
    tls_syn = (
        Ether(src=CLIENT_MAC, dst=GATEWAY_MAC)
        / IP(src=CLIENT_IP, dst=WEB_IP)
        / TCP(sport=51000, dport=443, flags="S", seq=1000)
    )
    packets.append(tls_syn)

    # 4. A deliberately plaintext HTTP request to port 80. This is the kind of
    #    payload a network observer could read if TLS were not used.
    http_get = (
        Ether(src=CLIENT_MAC, dst=GATEWAY_MAC)
        / IP(src=CLIENT_IP, dst=WEB_IP)
        / TCP(sport=51001, dport=80, flags="PA", seq=2000, ack=1)
        / Raw(
            load=(
                "GET /login HTTP/1.1\r\n"
                "Host: example.com\r\n"
                "User-Agent: PacketPeekaboo/1.0\r\n"
                "Accept: text/html\r\n"
                "\r\n"
            ).encode("ascii")
        )
    )
    packets.append(http_get)

    output.parent.mkdir(parents=True, exist_ok=True)
    wrpcap(str(output), packets)
    return packets


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a safe, synthetic packet capture.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "samples" / "demo.pcap",
        help="Where to write the PCAP file.",
    )
    args = parser.parse_args()

    packets = create_demo_pcap(args.output)
    print("=" * 70)
    print("  SAMPLE PCAP CREATED")
    print("=" * 70)
    print(f"File    : {args.output}")
    print(f"Packets : {len(packets)}")
    print("\nContains:")
    print("  1. DNS query for example.com")
    print("  2. DNS answer with an IP address")
    print("  3. TCP SYN to port 443 (start of an HTTPS connection)")
    print("  4. Plaintext HTTP GET to port 80")
    print("\nNext steps:")
    print(f"  py -3 analyze_pcap.py \"{args.output}\"")
    print(f"  Open the file in Wireshark: \"{args.output}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
