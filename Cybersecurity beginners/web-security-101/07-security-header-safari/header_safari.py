#!/usr/bin/env python3
"""
Project 07 - Security Header Safari
===================================

Fetch a public web page's response headers and grade a few browser security
settings. Headers are instructions the server sends to your browser, such as
"do not let other sites frame me" or "only run scripts from these sources."

Run:
    py -3 header_safari.py https://example.com
    py -3 header_safari.py https://example.com https://python.org
    py -3 header_safari.py --demo

Safety:
    This performs a single normal GET request to a public page. It does not
    scan, fuzz, or attack. Use passive observation only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


CHECKS: list[dict[str, Any]] = [
    {
        "header": "Content-Security-Policy",
        "weight": 30,
        "why": "Limits where scripts, styles, and other resources may come from.",
    },
    {
        "header": "Strict-Transport-Security",
        "weight": 20,
        "why": "Tells browsers to keep using HTTPS for this site.",
    },
    {
        "header": "X-Content-Type-Options",
        "weight": 15,
        "why": "Stops browsers from guessing a file type and running the wrong thing.",
    },
    {
        "header": "X-Frame-Options",
        "weight": 15,
        "why": "Helps stop clickjacking by controlling whether the page can be framed.",
    },
    {
        "header": "Referrer-Policy",
        "weight": 10,
        "why": "Controls how much of your previous URL is shared with other sites.",
    },
    {
        "header": "Permissions-Policy",
        "weight": 10,
        "why": "Restricts access to camera, microphone, location, and similar features.",
    },
]


def grade_for(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 55:
        return "C"
    if score >= 35:
        return "D"
    return "F"


def normalise_url(value: str) -> str:
    if "://" not in value:
        value = "https://" + value
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Not a usable http(s) URL: {value}")
    return value


def fetch_headers(url: str, timeout: float = 10.0) -> dict[str, Any]:
    """Request a page and return its status, final URL, and headers."""
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "CyberStarterLab/1.0 (educational header check)"},
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        headers = {key.lower(): value for key, value in response.headers.items()}
        status = getattr(response, "status", None)
        final_url = response.geturl()

    return {
        "requested_url": url,
        "final_url": final_url,
        "status": status,
        "headers": headers,
    }


def analyse(result: dict[str, Any]) -> dict[str, Any]:
    headers = result["headers"]
    scheme = urllib.parse.urlparse(result["final_url"]).scheme
    findings: list[dict[str, Any]] = []
    score = 0

    for check in CHECKS:
        name = check["header"]
        value = headers.get(name.lower())
        present = bool(value)
        earned = check["weight"] if present else 0

        # A strict CSP with frame-ancestors is a modern alternative to X-Frame-Options.
        if name == "X-Frame-Options" and not present:
            csp = headers.get("content-security-policy", "").lower()
            if "frame-ancestors" in csp:
                present = True
                value = "covered by CSP frame-ancestors"
                earned = check["weight"]

        # HSTS is only meaningful over HTTPS.
        if name == "Strict-Transport-Security" and scheme != "https":
            earned = 0
            present = False
            value = "ignored because the page is HTTP"

        score += earned
        findings.append(
            {
                "header": name,
                "present": present,
                "value": value,
                "weight": check["weight"],
                "earned": earned,
                "why": check["why"],
            }
        )

    if scheme != "https":
        score = max(0, score - 20)

    grade = grade_for(score)

    return {
        "url": result["final_url"],
        "status": result["status"],
        "scheme": scheme,
        "score": score,
        "grade": grade,
        "findings": findings,
    }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 78)
    print(f"  {report['url']}")
    print("=" * 78)
    print(f"HTTP status : {report['status']}")
    print(f"Scheme      : {report['scheme'].upper()}")
    print(f"Score       : {report['score']}/100")
    print(f"Grade       : {report['grade']}")
    if report["scheme"] != "https":
        print("[!] This page is not using HTTPS. Any headers cannot fix that.")
    print()

    for finding in report["findings"]:
        marker = "[+]" if finding["present"] else "[ ]"
        state = "present" if finding["present"] else "MISSING"
        print(f"{marker} {finding['header']:<32} {state}")
        print(f"    {finding['why']}")
        if finding["value"]:
            value = str(finding["value"]).replace("\n", " ")
            print(f"    Value: {value[:120]}{'...' if len(value) > 120 else ''}")
        print()

    print("Remember: a missing header is not automatically a vulnerability.")
    print("It is one clue. A real review needs context about what the page does.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check browser security headers on public web pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 header_safari.py example.com\n"
            "  py -3 header_safari.py https://example.com https://python.org\n"
            "  py -3 header_safari.py --demo\n"
        ),
    )
    parser.add_argument("urls", nargs="*", help="One or more public URLs.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a report.")
    parser.add_argument("--demo", action="store_true", help="Check a few public example sites.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    urls = args.urls
    if args.demo:
        urls = ["https://example.com", "https://python.org", "https://wikipedia.org"]

    if not urls:
        parser.print_help()
        print("\nProvide at least one URL, or use --demo.")
        return 1

    results: list[dict[str, Any]] = []
    for url in urls:
        try:
            page = fetch_headers(normalise_url(url), args.timeout)
            report = analyse(page)
            results.append(report)
            if not args.json:
                print_report(report)
                print()
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as error:
            print(f"[!] Could not check {url}: {error}")
            if not args.json:
                print()

    if args.json:
        print(json.dumps(results, indent=2))

    return 0 if results else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
