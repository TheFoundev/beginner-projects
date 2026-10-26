#!/usr/bin/env python3
"""
Project 13 - Ping, Route, Repeat: Map a Trip Across the Internet
================================================================

Measure the journey to a public destination: how long replies take, how many
routers are in the path, and where the route changes.

Run:
    py -3 ping_route.py example.com
    py -3 ping_route.py example.com --count 3 --max-hops 10
    py -3 ping_route.py example.com --no-trace
    py -3 ping_route.py --demo

Safety:
    Use public, allowed destinations only. This runs the normal ping and
    traceroute commands with a small packet count. Do not use it to flood or
    probe networks you do not own.
"""

from __future__ import annotations

import argparse
import platform
import re
import socket
import subprocess
import sys
from statistics import mean


TIME_RE = re.compile(r"time[=<]\s*([\d.]+)\s*ms", re.IGNORECASE)
WINDOWS_SUMMARY_RE = re.compile(
    r"Minimum\s*=\s*([\d.]+)ms,\s*Maximum\s*=\s*([\d.]+)ms,\s*Average\s*=\s*([\d.]+)ms",
    re.IGNORECASE,
)
UNIX_SUMMARY_RE = re.compile(
    r"rtt\s+min/avg/max(?:/mdev)?\s*=\s*([\d.]+)/([\d.]+)/([\d.]+)",
    re.IGNORECASE,
)


def run_command(command: list[str], timeout: int) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
        output = (completed.stdout or "") + (completed.stderr or "")
        return completed.returncode, output.strip()
    except FileNotFoundError:
        return 127, f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"Command timed out after {timeout} seconds: {' '.join(command)}"


def ping_command(host: str, count: int) -> list[str]:
    if platform.system().lower().startswith("win"):
        return ["ping", "-n", str(count), host]
    return ["ping", "-c", str(count), host]


def trace_command(host: str, max_hops: int) -> list[str]:
    if platform.system().lower().startswith("win"):
        return ["tracert", "-h", str(max_hops), "-w", "1000", host]
    return ["traceroute", "-m", str(max_hops), "-w", "2", host]


def parse_ping(output: str) -> dict[str, float | int | None]:
    times = [float(value) for value in TIME_RE.findall(output)]
    minimum = maximum = average = None

    windows_match = WINDOWS_SUMMARY_RE.search(output)
    unix_match = UNIX_SUMMARY_RE.search(output)
    if windows_match:
        minimum, maximum, average = (float(value) for value in windows_match.groups())
    elif unix_match:
        minimum, average, maximum = (float(value) for value in unix_match.groups())
    elif times:
        minimum, maximum, average = min(times), max(times), mean(times)

    return {
        "sent": len(times) or None,
        "minimum_ms": minimum,
        "average_ms": average,
        "maximum_ms": maximum,
    }


def parse_trace(output: str) -> list[dict[str, str]]:
    hops: list[dict[str, str]] = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"^(\d+)\s+(.*)$", stripped)
        if not match:
            continue
        hop_number, rest = match.groups()
        addresses = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", rest)
        name = ""
        if rest and not rest.startswith("*"):
            name = rest.split()[0] if rest.split() else ""
        hops.append(
            {
                "hop": hop_number,
                "name": name if not re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", name) else "",
                "address": addresses[-1] if addresses else "*",
            }
        )
    return hops


def print_ping(host: str, address: str, output: str, stats: dict[str, object]) -> None:
    print("\n" + "-" * 72)
    print(f"PING {host} ({address})")
    print("-" * 72)
    if stats["average_ms"] is None:
        print(output if output else "No ping replies were parsed.")
        return
    print(f"Replies parsed : {stats['sent']}")
    print(f"Minimum        : {stats['minimum_ms']:.1f} ms")
    print(f"Average        : {stats['average_ms']:.1f} ms")
    print(f"Maximum        : {stats['maximum_ms']:.1f} ms")
    print("\nRaw output:")
    for line in output.splitlines()[:20]:
        print(f"  {line}")


def print_trace(host: str, output: str, hops: list[dict[str, str]]) -> None:
    print("\n" + "-" * 72)
    print(f"ROUTE TO {host}")
    print("-" * 72)
    if not hops:
        print(output if output else "No route hops were parsed.")
        return
    print(f"Hops found: {len(hops)}")
    print(f"  {'Hop':>3}  {'Address':<18} Name")
    for hop in hops:
        print(f"  {hop['hop']:>3}  {hop['address']:<18} {hop['name']}")
    print("\nA hop is one router between you and the destination.")
    print("Stars (*) usually mean a router did not answer the trace request.")
    print("That is common and does not always mean something is broken.")


def run_demo(host: str, count: int, max_hops: int, do_trace: bool) -> int:
    print("=" * 72)
    print("  PING, ROUTE, REPEAT - DEMO")
    print("=" * 72)
    print(f"Destination: {host}")
    print("Using a small packet count and a short hop limit to stay gentle.")

    try:
        address = socket.gethostbyname(host)
        print(f"Resolved to: {address}")
    except socket.gaierror as error:
        print(f"ERROR: could not resolve {host}: {error}")
        return 1

    code, output = run_command(ping_command(host, count), timeout=60)
    stats = parse_ping(output)
    print_ping(host, address, output, stats)
    if code not in (0, 1):
        print(f"\n[!] ping exited with code {code}.")

    if do_trace:
        code, trace_output = run_command(trace_command(host, max_hops), timeout=120)
        hops = parse_trace(trace_output)
        print_trace(host, trace_output, hops)
        if code != 0 and not hops:
            print(f"\n[!] traceroute exited with code {code}. It may not be installed.")

    print("\n" + "=" * 72)
    print("  WHAT DID WE LEARN?")
    print("=" * 72)
    print("- Latency is the round-trip time in milliseconds.")
    print("- More hops means more routers, but not always more delay.")
    print("- A nearby server can still be slow if its network is congested.")
    print("- Traceroute shows the path, but routes can change from minute to minute.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure ping latency and trace a route to a public host.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 ping_route.py example.com\n"
            "  py -3 ping_route.py example.com --count 3 --max-hops 10\n"
            "  py -3 ping_route.py example.com --no-trace\n"
            "  py -3 ping_route.py --demo\n"
        ),
    )
    parser.add_argument("host", nargs="?", help="Public host name, for example example.com.")
    parser.add_argument("--count", type=int, default=4, help="Number of ping packets (1-10).")
    parser.add_argument("--max-hops", type=int, default=15, help="Maximum traceroute hops (1-30).")
    parser.add_argument("--no-trace", action="store_true", help="Skip traceroute.")
    parser.add_argument("--demo", action="store_true", help="Run against example.com.")
    args = parser.parse_args()

    host = args.host or ("example.com" if args.demo else None)
    if not host:
        parser.print_help()
        print("\nProvide a host, or use --demo.")
        return 1

    if not 1 <= args.count <= 10:
        print("ERROR: --count must be between 1 and 10.")
        return 1
    if not 1 <= args.max_hops <= 30:
        print("ERROR: --max-hops must be between 1 and 30.")
        return 1

    return run_demo(host, args.count, args.max_hops, not args.no_trace)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
