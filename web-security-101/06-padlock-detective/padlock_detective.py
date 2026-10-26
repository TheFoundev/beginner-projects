#!/usr/bin/env python3
"""
Project 06 - Padlock Detective: Is That Site Really Secure?
===========================================================

Connect to a public website, retrieve its TLS certificate, and explain what the
padlock in your browser actually proves.

Run:
    py -3 padlock_detective.py example.com
    py -3 padlock_detective.py python.org --json
    py -3 padlock_detective.py --demo

Safety:
    This is a passive TLS handshake with a public website. Do not use it to
    probe hosts you do not own or have permission to visit. It does not scan,
    attack, or bypass anything.
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone
from typing import Any


def parse_certificate_time(value: str) -> datetime:
    """Convert a certificate date such as 'Jun  1 12:00:00 2026 GMT' to UTC."""
    return datetime.fromtimestamp(ssl.cert_time_to_seconds(value), tz=timezone.utc)


def flatten_name(name: Any) -> dict[str, str]:
    """Turn the certificate's nested name tuples into a simple dictionary."""
    result: dict[str, str] = {}
    if not name:
        return result
    for group in name:
        for key, value in group:
            result.setdefault(key, value)
    return result


def fetch_certificate(host: str, port: int = 443, timeout: float = 8.0) -> dict[str, Any]:
    """Perform a normal, verified TLS handshake and collect certificate details."""
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=host) as tls_socket:
            certificate = tls_socket.getpeercert()
            protocol = tls_socket.version()
            cipher = tls_socket.cipher()

    if not certificate:
        raise ValueError("The server did not provide a certificate.")

    not_before = parse_certificate_time(certificate["notBefore"])
    not_after = parse_certificate_time(certificate["notAfter"])
    now = datetime.now(timezone.utc)
    days_left = (not_after - now).days

    return {
        "host": host,
        "port": port,
        "protocol": protocol,
        "cipher": cipher[0] if cipher else "unknown",
        "subject": flatten_name(certificate.get("subject")),
        "issuer": flatten_name(certificate.get("issuer")),
        "serial": certificate.get("serialNumber", "unknown"),
        "not_before": not_before.isoformat(),
        "not_after": not_after.isoformat(),
        "days_left": days_left,
        "san": [value for key, value in certificate.get("subjectAltName", ()) if key == "DNS"],
    }


def print_report(info: dict[str, Any]) -> None:
    print("=" * 72)
    print(f"  PADLOCK REPORT: {info['host']}:{info['port']}")
    print("=" * 72)
    print(f"TLS version       : {info['protocol']}")
    print(f"Cipher suite      : {info['cipher']}")
    print(f"Certificate issued : {info['issuer'].get('organizationName', 'unknown')}")
    print(f"Issuer common name : {info['issuer'].get('commonName', 'unknown')}")
    print(f"Subject            : {info['subject'].get('commonName', 'unknown')}")
    print(f"Valid from        : {info['not_before']}")
    print(f"Valid until       : {info['not_after']}")
    print(f"Days remaining    : {info['days_left']}")
    print(f"Serial number     : {info['serial'][:40]}{'...' if len(info['serial']) > 40 else ''}")

    print("\nNames this certificate covers:")
    for name in info["san"][:12]:
        print(f"  - {name}")
    if len(info["san"]) > 12:
        print(f"  ... and {len(info['san']) - 12} more")

    if info["days_left"] < 0:
        print("\n[!] This certificate is EXPIRED.")
    elif info["days_left"] < 30:
        print("\n[!] This certificate expires soon.")
    else:
        print("\n[+] The certificate is currently within its validity period.")

    print("\nWhat the padlock proves:")
    print("  - You are talking to a server that holds a certificate for this name.")
    print("  - The connection is encrypted, so others on the network cannot read it.")
    print("  - The certificate is trusted by your browser's root store.")
    print("  - The certificate is currently valid (not expired).")

    print("\nWhat the padlock does NOT prove:")
    print("  - That the website owners are honest.")
    print("  - That the site is free of scams, malware, or fake products.")
    print("  - That the content is accurate or legal.")
    print("  - That you typed the right domain (lookalike domains can have padlocks too).")

    print("\nThe padlock is a locked tunnel, not a trust badge.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a public website's TLS certificate.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 padlock_detective.py example.com\n"
            "  py -3 padlock_detective.py wikipedia.org --json\n"
            "  py -3 padlock_detective.py --demo\n"
        ),
    )
    parser.add_argument("host", nargs="?", help="Domain name, for example example.com.")
    parser.add_argument("--port", type=int, default=443, help="TLS port (default: 443).")
    parser.add_argument("--timeout", type=float, default=8.0, help="Connection timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--demo", action="store_true", help="Inspect a few public example sites.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.demo:
        hosts = ["example.com", "python.org", "wikipedia.org"]
        results = []
        for host in hosts:
            try:
                info = fetch_certificate(host, args.port, args.timeout)
                print_report(info)
                results.append(info)
                print()
            except (socket.error, ssl.SSLError, ValueError) as error:
                print(f"[!] Could not inspect {host}: {error}\n")
        if args.json and results:
            print(json.dumps(results, indent=2))
        return 0 if results else 1

    if not args.host:
        parser.print_help()
        print("\nProvide a host, or use --demo.")
        return 1

    try:
        info = fetch_certificate(args.host, args.port, args.timeout)
    except ssl.SSLCertVerificationError as error:
        print(f"[!] Certificate verification failed: {error}")
        print("    Your browser would probably warn you too. Do not continue blindly.")
        return 2
    except (socket.error, ssl.SSLError, ValueError) as error:
        print(f"[!] Could not inspect {args.host}: {error}")
        return 1

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print_report(info)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
