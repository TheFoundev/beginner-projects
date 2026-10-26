#!/usr/bin/env python3
"""
Project 12 - The Internet's Address Book: A DNS Detective Story
==============================================================

Look up the main DNS record types for a domain and explain what each one does.
DNS is the internet's contact list: it turns names such as example.com into
numbers that computers can use.

Install:
    py -3 -m pip install -r requirements.txt

Run:
    py -3 dns_detective.py example.com
    py -3 dns_detective.py example.com --type MX
    py -3 dns_detective.py --demo
    py -3 dns_detective.py example.com --json

Safety:
    This performs ordinary DNS lookups. It does not scan ports, brute-force
    subdomains, or attack the domain.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

try:
    import dns.exception
    import dns.resolver
except ImportError:
    print("This project needs dnspython.")
    print("Install it with: py -3 -m pip install -r requirements.txt")
    raise SystemExit(1)


RECORD_HELP = {
    "A": "IPv4 address for the domain",
    "AAAA": "IPv6 address for the domain",
    "MX": "Mail servers that receive email for the domain",
    "TXT": "Free-form text records, often used for verification and email policy",
    "NS": "Name servers that are authoritative for the domain",
    "CNAME": "An alias pointing to another name",
}

DEFAULT_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]


def make_resolver(nameserver: str | None) -> dns.resolver.Resolver:
    resolver = dns.resolver.Resolver(configure=True)
    resolver.timeout = 5
    resolver.lifetime = 8
    if nameserver:
        resolver.nameservers = [nameserver]
    return resolver


def query_type(resolver: dns.resolver.Resolver, domain: str, record_type: str) -> dict[str, Any]:
    try:
        answers = resolver.resolve(domain, record_type, raise_on_no_answer=False)
    except dns.resolver.NXDOMAIN:
        return {
            "type": record_type,
            "status": "NXDOMAIN",
            "help": RECORD_HELP.get(record_type, ""),
            "records": [],
            "ttl": None,
        }
    except dns.resolver.NoNameservers:
        return {
            "type": record_type,
            "status": "NO_NAMESERVERS",
            "help": RECORD_HELP.get(record_type, ""),
            "records": [],
            "ttl": None,
        }
    except dns.exception.Timeout:
        return {
            "type": record_type,
            "status": "TIMEOUT",
            "help": RECORD_HELP.get(record_type, ""),
            "records": [],
            "ttl": None,
        }

    if answers.rrset is None:
        return {
            "type": record_type,
            "status": "NO_ANSWER",
            "help": RECORD_HELP.get(record_type, ""),
            "records": [],
            "ttl": None,
        }

    records = []
    for item in answers:
        if record_type == "MX":
            records.append(f"{item.preference} {item.exchange}")
        elif record_type == "TXT":
            chunks = [part.decode("utf-8", errors="replace") for part in item.strings]
            records.append("".join(chunks))
        else:
            records.append(str(item).rstrip("."))

    return {
        "type": record_type,
        "status": "OK",
        "help": RECORD_HELP.get(record_type, ""),
        "records": records,
        "ttl": answers.rrset.ttl,
    }


def run_lookup(domain: str, types: list[str], nameserver: str | None) -> dict[str, Any]:
    resolver = make_resolver(nameserver)
    results = [query_type(resolver, domain, record_type) for record_type in types]
    return {
        "domain": domain,
        "nameservers": [str(item) for item in resolver.nameservers],
        "results": results,
    }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 76)
    print(f"  DNS REPORT: {report['domain']}")
    print("=" * 76)
    print(f"Resolver(s): {', '.join(report['nameservers'])}")

    for result in report["results"]:
        print(f"\n[{result['type']}] {result['help']}")
        print(f"  Status: {result['status']}")
        if result["ttl"] is not None:
            print(f"  TTL   : {result['ttl']} seconds")
        if result["records"]:
            for value in result["records"]:
                print(f"  -> {value}")
        else:
            print("  -> (no records of this type)")

    print("\nHow to read this:")
    print("  - A/AAAA records point a name at an address.")
    print("  - MX records tell email where to go.")
    print("  - TXT records often carry SPF, DKIM, or domain-verification strings.")
    print("  - NS records identify the name servers in charge of the zone.")
    print("  - CNAME records create an alias, not a new address.")
    print("\nTTL means 'how long may a resolver cache this answer?'")
    print("A short TTL can make changes faster but increases lookup traffic.")


def parse_types(value: str) -> list[str]:
    requested = [item.strip().upper() for item in value.split(",") if item.strip()]
    invalid = [item for item in requested if item not in RECORD_HELP]
    if invalid:
        raise argparse.ArgumentTypeError(
            f"unknown record type(s): {', '.join(invalid)}. Choose from {', '.join(RECORD_HELP)}"
        )
    return requested


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Look up common DNS records for a domain.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 dns_detective.py example.com\n"
            "  py -3 dns_detective.py example.com --type MX,TXT\n"
            "  py -3 dns_detective.py example.com --nameserver 1.1.1.1\n"
            "  py -3 dns_detective.py --demo\n"
        ),
    )
    parser.add_argument("domain", nargs="?", help="Domain to look up, for example example.com.")
    parser.add_argument(
        "--type",
        dest="types",
        type=parse_types,
        default=DEFAULT_TYPES,
        help="Comma-separated record types (default: A,AAAA,MX,TXT,NS,CNAME).",
    )
    parser.add_argument("--nameserver", help="Use a specific resolver, for example 1.1.1.1.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a report.")
    parser.add_argument("--demo", action="store_true", help="Look up example.com.")
    args = parser.parse_args()

    domain = args.domain or ("example.com" if args.demo else None)
    if not domain:
        parser.print_help()
        print("\nProvide a domain, or use --demo.")
        return 1

    try:
        report = run_lookup(domain, args.types, args.nameserver)
    except dns.exception.DNSException as error:
        print(f"ERROR: DNS lookup failed: {error}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
