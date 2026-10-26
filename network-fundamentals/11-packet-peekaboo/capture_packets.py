#!/usr/bin/env python3
"""
Project 11 - Packet Peekaboo: Capture Your Own Traffic
=====================================================

Capture a small number of packets from your own computer and save them to a
PCAP file for analysis. This is the hands-on part of the project.

Install:
    py -3 -m pip install -r requirements.txt

Windows note:
    Scapy needs Npcap. Installing Wireshark includes Npcap. Run the terminal as
    Administrator if Windows refuses to open the capture interface.

Run:
    py -3 capture_packets.py --list-interfaces
    py -3 capture_packets.py --count 20 --output my_capture.pcap
    py -3 capture_packets.py --filter "udp port 53" --count 10

Safety:
    Capture only your own traffic, on your own machine and network. Do not
    capture on a shared, school, or workplace network without permission.
    Promiscuous mode is disabled on purpose.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from scapy.all import conf, get_if_list, sniff, wrpcap
except ImportError:
    print("This project needs Scapy.")
    print("Install it with: py -3 -m pip install -r requirements.txt")
    raise SystemExit(1)


def list_interfaces() -> None:
    print("Available capture interfaces:")
    for name in get_if_list():
        print(f"  - {name}")
    print("\nUse one of these names with --iface if the default is wrong.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture a few packets from your own machine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 capture_packets.py --list-interfaces\n"
            "  py -3 capture_packets.py --count 20 --output my_capture.pcap\n"
            '  py -3 capture_packets.py --filter "udp port 53" --count 10\n'
        ),
    )
    parser.add_argument("--iface", help="Interface name (see --list-interfaces).")
    parser.add_argument("--count", type=int, default=20, help="Stop after this many packets.")
    parser.add_argument("--timeout", type=int, default=30, help="Stop after this many seconds.")
    parser.add_argument(
        "--filter",
        default="udp port 53 or tcp port 443 or tcp port 80",
        help="BPF filter. The default focuses on DNS, HTTPS, and HTTP.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "samples" / "my_capture.pcap",
        help="Where to save the capture.",
    )
    parser.add_argument("--list-interfaces", action="store_true", help="Show interfaces and exit.")
    args = parser.parse_args()

    if args.list_interfaces:
        list_interfaces()
        return 0

    if args.count <= 0 or args.count > 500:
        print("ERROR: --count must be between 1 and 500 for this classroom exercise.")
        return 1

    print("=" * 72)
    print("  PACKET PEEKABOO - CAPTURE")
    print("=" * 72)
    print("This captures only traffic involving this computer.")
    print("Promiscuous mode is OFF.")
    print(f"Filter : {args.filter}")
    print(f"Count  : {args.count} packets")
    print(f"Timeout: {args.timeout} seconds")
    print("\nWhile the capture runs, open a simple website in your browser.")
    print("Press Ctrl+C to stop early.\n")

    conf.sniff_promisc = False

    kwargs = {
        "count": args.count,
        "timeout": args.timeout,
        "filter": args.filter,
        "store": True,
    }
    if args.iface:
        kwargs["iface"] = args.iface

    try:
        packets = sniff(**kwargs)
    except PermissionError:
        print("ERROR: permission denied. Run the terminal as Administrator (Windows)")
        print("or with sudo (Linux), and make sure Npcap is installed.")
        return 1
    except OSError as error:
        print(f"ERROR: could not capture: {error}")
        print("Try --list-interfaces, install Npcap, or run with more privileges.")
        return 1
    except Exception as error:
        # Scapy raises its own exception type when no packet provider is
        # available; keep the classroom message friendly.
        print(f"ERROR: could not start the capture: {error}")
        print("Install Npcap (Windows) or libpcap (Linux/macOS), then try again.")
        print("You can still use: py -3 analyze_pcap.py --demo")
        return 1
    except KeyboardInterrupt:
        print("\nCapture stopped early.")
        packets = []

    if not packets:
        print("No packets captured. Try a different interface or filter.")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    wrpcap(str(args.output), packets)

    print(f"\n[+] Captured {len(packets)} packets")
    print(f"[+] Saved to: {args.output}")
    print("\nNext step:")
    print(f"  py -3 analyze_pcap.py \"{args.output}\"")
    print("\nOpen it in Wireshark for the full experience. Remember: PCAP files can")
    print("contain private data. Keep yours local and delete it when finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
