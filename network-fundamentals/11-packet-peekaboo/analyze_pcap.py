#!/usr/bin/env python3
"""
Project 11 - Packet Peekaboo: Analyze a Packet Capture
======================================================

Read a .pcap file and summarize what is visible: who talked to whom, which
protocols were used, which DNS names were requested, and whether any HTTP
payload was sent in plaintext.

Install:
    py -3 -m pip install -r requirements.txt

Run:
    py -3 analyze_pcap.py samples/demo.pcap
    py -3 analyze_pcap.py --demo
    py -3 analyze_pcap.py my_capture.pcap --json

Safety:
    Analyze captures of your own traffic only. A PCAP can contain private data.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from scapy.all import DNS, DNSQR, DNSRR, IP, IPv6, Raw, TCP, UDP, rdpcap
except ImportError:
    print("This project needs Scapy.")
    print("Install it with: py -3 -m pip install -r requirements.txt")
    raise SystemExit(1)


def packet_addresses(packet: Any) -> tuple[str, str]:
    if IP in packet:
        return packet[IP].src, packet[IP].dst
    if IPv6 in packet:
        return packet[IPv6].src, packet[IPv6].dst
    return "unknown", "unknown"


def protocol_label(packet: Any) -> str:
    if DNS in packet:
        return "DNS"
    if TCP in packet:
        if packet[TCP].dport == 443 or packet[TCP].sport == 443:
            return "TLS"
        if packet[TCP].dport == 80 or packet[TCP].sport == 80:
            return "HTTP"
        return "TCP"
    if UDP in packet:
        return "UDP"
    return "OTHER"


def dns_name(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").rstrip(".")
    return str(value).rstrip(".")


def first_dns_record(value: Any, record_type: type) -> Any | None:
    """Return one DNS record from old or new Scapy fields.

    Older Scapy versions expose dns.qd and dns.an as one record. Scapy 2.8
    exposes list-like fields even when there is only one record. This helper
    keeps the teaching script working across both layouts.
    """
    if value is None:
        return None
    if isinstance(value, record_type):
        return value
    try:
        if len(value) > 0:
            candidate = value[0]
            return candidate if isinstance(candidate, record_type) else None
    except (TypeError, IndexError):
        pass
    return None


def describe_packet(packet: Any) -> str:
    label = protocol_label(packet)
    if label == "DNS" and DNS in packet:
        dns = packet[DNS]
        question = first_dns_record(dns.qd, DNSQR)
        if question is not None:
            name = dns_name(question.qname)
            if dns.qr == 0:
                return f"query {name}"
            answer_record = first_dns_record(dns.an, DNSRR)
            answer = f" -> {dns_name(answer_record.rdata)}" if answer_record else ""
            return f"response {name}{answer}"
        return "DNS message"

    if TCP in packet:
        tcp = packet[TCP]
        flags = str(tcp.flags)
        return f"{tcp.sport} -> {tcp.dport} flags={flags}"

    if UDP in packet:
        udp = packet[UDP]
        return f"{udp.sport} -> {udp.dport}"

    return "packet"


def http_payload(packet: Any) -> str | None:
    if Raw not in packet:
        return None
    payload = bytes(packet[Raw].load)
    if not payload:
        return None
    text = payload.decode("utf-8", errors="replace")
    if text.startswith(("GET ", "POST ", "HEAD ", "PUT ", "DELETE ")):
        return " ".join(text.splitlines()[0].split())
    return None


def analyze(path: Path) -> dict[str, Any]:
    packets = rdpcap(str(path))
    protocols: Counter[str] = Counter()
    sources: Counter[str] = Counter()
    destinations: Counter[str] = Counter()
    dns_queries: list[str] = []
    plaintext_http: list[dict[str, str]] = []
    rows: list[dict[str, Any]] = []

    for index, packet in enumerate(packets, start=1):
        label = protocol_label(packet)
        src, dst = packet_addresses(packet)
        protocols[label] += 1
        sources[src] += 1
        destinations[dst] += 1
        info = describe_packet(packet)

        if DNS in packet:
            question = first_dns_record(packet[DNS].qd, DNSQR)
            if question is not None and packet[DNS].qr == 0:
                name = dns_name(question.qname)
                if name not in dns_queries:
                    dns_queries.append(name)

        payload_line = http_payload(packet)
        if payload_line:
            plaintext_http.append(
                {
                    "packet": str(index),
                    "source": src,
                    "destination": dst,
                    "request": payload_line,
                }
            )

        rows.append(
            {
                "number": index,
                "source": src,
                "destination": dst,
                "protocol": label,
                "info": info,
            }
        )

    return {
        "file": str(path),
        "packet_count": len(packets),
        "protocols": dict(protocols),
        "top_sources": sources.most_common(5),
        "top_destinations": destinations.most_common(5),
        "dns_queries": dns_queries,
        "plaintext_http": plaintext_http,
        "packets": rows,
    }


def print_report(report: dict[str, Any], limit: int) -> None:
    print("=" * 78)
    print(f"  PACKET CAPTURE: {report['file']}")
    print("=" * 78)
    print(f"Packets read: {report['packet_count']}")

    print("\nProtocols:")
    for name, count in sorted(report["protocols"].items(), key=lambda item: -item[1]):
        print(f"  {name:<8} {count}")

    print("\nTop sources:")
    for address, count in report["top_sources"]:
        print(f"  {address:<20} {count} packets")

    print("\nTop destinations:")
    for address, count in report["top_destinations"]:
        print(f"  {address:<20} {count} packets")

    print("\nDNS names requested:")
    if report["dns_queries"]:
        for name in report["dns_queries"]:
            print(f"  - {name}")
    else:
        print("  (none)")

    print("\nPlaintext HTTP requests (visible to anyone on the network):")
    if report["plaintext_http"]:
        for item in report["plaintext_http"]:
            print(f"  packet {item['packet']}: {item['source']} -> {item['destination']}")
            print(f"    {item['request']}")
    else:
        print("  (none detected)")

    print(f"\nFirst {min(limit, len(report['packets']))} packets:")
    print(f"  {'#':>4}  {'Source':<16} {'Destination':<16} {'Proto':<6} Info")
    for row in report["packets"][:limit]:
        print(
            f"  {row['number']:>4}  {row['source']:<16} {row['destination']:<16} "
            f"{row['protocol']:<6} {row['info']}"
        )

    print("\nWhat this means:")
    print("  - DNS names are often visible even when the website uses HTTPS.")
    print("  - TLS (port 443) encrypts the content, so the payload is not readable.")
    print("  - Plain HTTP (port 80) exposes the request in clear text. Never log in")
    print("    or send private data over an HTTP page.")
    print("\nA packet capture can also contain personal data. Treat PCAP files as private.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize a PCAP file with Scapy.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 analyze_pcap.py samples/demo.pcap\n"
            "  py -3 analyze_pcap.py --demo\n"
            "  py -3 analyze_pcap.py my_capture.pcap --json\n"
        ),
    )
    parser.add_argument("pcap", nargs="?", type=Path, help="PCAP file to analyze.")
    parser.add_argument("--limit", type=int, default=15, help="How many packet rows to print.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a report.")
    parser.add_argument("--demo", action="store_true", help="Analyze the bundled sample capture.")
    args = parser.parse_args()

    path = args.pcap
    if args.demo:
        path = Path(__file__).resolve().parent / "samples" / "demo.pcap"
    if path is None:
        parser.print_help()
        print("\nProvide a PCAP file, or use --demo.")
        return 1

    if not path.exists():
        print(f"ERROR: file not found: {path}")
        if args.demo:
            print("Create it with: py -3 make_sample_pcap.py")
        return 1

    try:
        report = analyze(path)
    except Exception as error:  # Scapy raises several format-specific exceptions.
        print(f"ERROR: could not read {path}: {error}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
