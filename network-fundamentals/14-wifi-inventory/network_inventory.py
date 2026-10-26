#!/usr/bin/env python3
"""
Project 14 - Who's on My Wi-Fi? Build a Home Network Inventory
=============================================================

Read the local ARP/neighbor table and build a device inventory. This is a
defensive exercise: know what is on your own network before you worry about
who should not be there.

Run:
    py -3 network_inventory.py
    py -3 network_inventory.py --output inventory.csv
    py -3 network_inventory.py --input samples/arp_sample.txt
    py -3 network_inventory.py --demo

Safety:
    This reads the local neighbor table. It does not scan, ping, or probe any
    device. Only inventory a network you own or have explicit permission to
    manage.
"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import platform
import re
import subprocess
import sys
from pathlib import Path


IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MAC_RE = re.compile(r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b")


def read_neighbor_table(input_path: Path | None) -> str:
    if input_path:
        return input_path.read_text(encoding="utf-8", errors="replace")

    system = platform.system().lower()
    if system.startswith("win"):
        command = ["arp", "-a"]
    elif system == "darwin":
        command = ["arp", "-an"]
    else:
        command = ["ip", "neigh"]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=15,
            check=False,
        )
    except FileNotFoundError:
        if command[0] == "ip":
            completed = subprocess.run(
                ["arp", "-an"], capture_output=True, text=True, errors="replace", timeout=15, check=False
            )
        else:
            raise
    return (completed.stdout or "") + (completed.stderr or "")


def is_interesting_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return not (
        address.is_multicast
        or address.is_unspecified
        or address.is_loopback
        or address.is_link_local
        or address == ipaddress.ip_address("255.255.255.255")
    )


def normalise_mac(value: str) -> str:
    return value.replace("-", ":").lower()


def is_locally_administered(mac: str) -> bool:
    """A locally administered MAC often means a phone used a privacy address."""
    try:
        first_octet = int(mac.split(":")[0], 16)
    except (ValueError, IndexError):
        return False
    return bool(first_octet & 0x02)


def parse_neighbors(text: str) -> list[dict[str, str]]:
    devices: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        ip_match = IPV4_RE.search(line)
        mac_match = MAC_RE.search(line)
        if not ip_match or not mac_match:
            continue
        ip = ip_match.group(0)
        mac = normalise_mac(mac_match.group(0))
        if not is_interesting_ip(ip) or mac in {"ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"}:
            continue
        devices[mac] = {
            "ip": ip,
            "mac": mac,
            "locally_administered": "yes" if is_locally_administered(mac) else "no",
        }
    return sorted(devices.values(), key=lambda item: tuple(int(part) for part in item["ip"].split(".")))


def load_known(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    known: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            mac = normalise_mac((row.get("mac") or "").strip())
            if mac:
                known[mac] = {
                    "owner": (row.get("owner") or "").strip(),
                    "trust": (row.get("trust") or "unknown").strip(),
                    "notes": (row.get("notes") or "").strip(),
                }
    return known


def build_inventory(devices: list[dict[str, str]], known: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    inventory = []
    for device in devices:
        match = known.get(device["mac"], {})
        inventory.append(
            {
                "ip": device["ip"],
                "mac": device["mac"],
                "locally_administered": device["locally_administered"],
                "owner": match.get("owner", ""),
                "trust": match.get("trust", "unknown"),
                "notes": match.get("notes", ""),
            }
        )
    return inventory


def print_inventory(inventory: list[dict[str, str]], output: Path | None) -> None:
    print("=" * 82)
    print("  HOME NETWORK INVENTORY")
    print("=" * 82)
    print(f"Devices found: {len(inventory)}")
    print(f"\n{'IP address':<16} {'MAC address':<18} {'Owner':<16} {'Trust':<10} Random MAC?")
    print("-" * 82)
    for device in inventory:
        owner = device["owner"] or "(unknown)"
        print(
            f"{device['ip']:<16} {device['mac']:<18} {owner:<16} "
            f"{device['trust']:<10} {device['locally_administered']}"
        )
        if device["notes"]:
            print(f"  note: {device['notes']}")

    unknown = [item for item in inventory if item["trust"] == "unknown"]
    print("\nSummary:")
    print(f"  Known/trusted : {len(inventory) - len(unknown)}")
    print(f"  Needs review  : {len(unknown)}")
    print("  Look for devices you do not recognize, duplicate names, or a device")
    print("  that disappears and reappears with a different MAC address.")

    if output:
        print(f"\n[+] CSV written to: {output}")


def write_csv(inventory: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ip", "mac", "owner", "trust", "notes", "locally_administered"],
        )
        writer.writeheader()
        writer.writerows(inventory)


def run_demo() -> None:
    base = Path(__file__).resolve().parent
    sample = base / "samples" / "arp_sample.txt"
    known_file = base / "samples" / "known_devices.csv"
    output = base / "samples" / "demo_inventory.csv"

    text = read_neighbor_table(sample)
    devices = parse_neighbors(text)
    known = load_known(known_file)
    inventory = build_inventory(devices, known)

    print("Using the bundled sample ARP table, not your real network.\n")
    print_inventory(inventory, output)
    write_csv(inventory, output)
    print("\nWhat to do next on your own network:")
    print("  1. Open your router's admin page (with permission from the owner).")
    print("  2. Compare its device list with this inventory.")
    print("  3. Name every device you recognize.")
    print("  4. Investigate anything you cannot explain.")
    print("  5. Change the router admin password if it is still the default.")
    print("\nThis tool reads the neighbor table only. It does not scan or probe.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a local device inventory from the ARP/neighbor table.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 network_inventory.py\n"
            "  py -3 network_inventory.py --output inventory.csv\n"
            "  py -3 network_inventory.py --input samples/arp_sample.txt\n"
            "  py -3 network_inventory.py --demo\n"
        ),
    )
    parser.add_argument("--input", type=Path, help="Read a saved ARP/neigh output instead of running a command.")
    parser.add_argument("--known", type=Path, help="CSV with mac,owner,trust,notes columns.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "inventory.csv",
        help="Where to write the CSV inventory.",
    )
    parser.add_argument("--demo", action="store_true", help="Use the bundled sample data.")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return 0

    try:
        text = read_neighbor_table(args.input)
    except (OSError, subprocess.SubprocessError) as error:
        print(f"ERROR: could not read the neighbor table: {error}")
        print("Try running the command manually (arp -a or ip neigh), save the output")
        print("to a file, then use --input FILE.")
        return 1

    devices = parse_neighbors(text)
    if not devices:
        print("No devices found. Try running the neighbor command manually and saving")
        print("the output, then use --input FILE.")
        return 1

    known = load_known(args.known)
    inventory = build_inventory(devices, known)
    print_inventory(inventory, args.output)
    write_csv(inventory, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
