#!/usr/bin/env python3
"""
Project 18 - Digital Footprint Audit: What Can Strangers Learn About You?
========================================================================

Check a list of your OWN public profile URLs and produce a privacy report:
is the page public, does it use HTTPS, is it marked noindex, does it expose an
email or phone number you choose to check, and which third-party hosts does it
load assets from?

Run:
    py -3 footprint_audit.py --demo
    py -3 footprint_audit.py --input profiles_sample.txt
    py -3 footprint_audit.py --input my_profiles.txt --email me@example.com

Safety:
    Use this only for your own profiles. It makes one normal GET request per
    URL (plus robots.txt) and does not search for other people, scrape search
    engines, bypass logins, or probe for vulnerabilities.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_robots: list[str] = []
        self.asset_sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        elif tag.lower() == "meta" and attributes.get("name", "").lower() == "robots":
            self.meta_robots.append(attributes.get("content", "").lower())
        elif tag.lower() in {"script", "img", "iframe", "source"}:
            source = attributes.get("src") or attributes.get("srcset")
            if source:
                self.asset_sources.append(source)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    def title(self) -> str:
        return " ".join(" ".join(self.title_parts).split())


def load_profiles(path: Path) -> list[dict[str, str]]:
    profiles: list[dict[str, str]] = []
    for number, raw_line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            label, url = (part.strip() for part in line.split("|", 1))
        else:
            label, url = f"Profile {number}", line
        profiles.append({"label": label or f"Profile {number}", "url": url})
    return profiles


def fetch_text(url: str, timeout: float, limit: int = 2_000_000) -> tuple[str, dict[str, str], str, int]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "FootprintAudit/1.0 (personal self-audit; one request)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(limit)
        charset = response.headers.get_content_charset() or "utf-8"
        text = raw.decode(charset, errors="replace")
        headers = {key.lower(): value for key, value in response.headers.items()}
        return text, headers, response.geturl(), response.status


def get_robots_disallows(url: str, timeout: float) -> list[str]:
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        text, _, _, _ = fetch_text(robots_url, timeout, limit=200_000)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return []

    disallows: list[str] = []
    active = False
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        if key.lower() == "user-agent":
            active = value == "*"
        elif active and key.lower() == "disallow" and value:
            disallows.append(value)
    return disallows


def path_is_disallowed(path: str, disallows: list[str]) -> bool:
    for rule in disallows:
        if rule == "/":
            continue
        if rule.endswith("$"):
            if path == rule[:-1]:
                return True
        elif path.startswith(rule):
            return True
    return False


def phone_digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def analyse_profile(
    label: str,
    requested_url: str,
    email_to_check: str | None,
    phone_to_check: str | None,
    timeout: float,
) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(requested_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must start with http:// or https:// and include a host")

    result: dict[str, Any] = {
        "label": label,
        "requested_url": requested_url,
        "final_url": "",
        "status": None,
        "https": False,
        "redirected": False,
        "title": "",
        "noindex": False,
        "robots_disallow": False,
        "email_found": False,
        "phone_found": False,
        "third_party_hosts": "",
        "exposure_score": 0,
        "verdict": "",
        "error": "",
    }

    try:
        text, headers, final_url, status = fetch_text(requested_url, timeout)
    except urllib.error.HTTPError as error:
        result.update({"status": error.code, "error": f"HTTP {error.code}: {error.reason}"})
        return result
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        result["error"] = str(error)
        return result

    parser = PageParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception:
        pass

    final_parsed = urllib.parse.urlparse(final_url)
    result["final_url"] = final_url
    result["status"] = status
    result["https"] = final_parsed.scheme == "https"
    result["redirected"] = final_url.rstrip("/") != requested_url.rstrip("/")
    result["title"] = parser.title()[:160]

    x_robots = headers.get("x-robots-tag", "").lower()
    result["noindex"] = "noindex" in x_robots or any("noindex" in value for value in parser.meta_robots)

    disallows = get_robots_disallows(final_url, timeout)
    result["robots_disallow"] = path_is_disallowed(final_parsed.path or "/", disallows)

    lowered = text.lower()
    if email_to_check:
        result["email_found"] = email_to_check.lower() in lowered
    if phone_to_check:
        digits = phone_digits(phone_to_check)
        result["phone_found"] = bool(digits and len(digits) >= 7 and digits in phone_digits(text))

    final_host = (final_parsed.hostname or "").lower()
    third_party: set[str] = set()
    for source in parser.asset_sources:
        absolute = urllib.parse.urljoin(final_url, source)
        host = (urllib.parse.urlparse(absolute).hostname or "").lower()
        if host and host != final_host:
            third_party.add(host)
    result["third_party_hosts"] = ", ".join(sorted(third_party)[:10])

    score = 0
    if not result["https"]:
        score += 20
    if result["email_found"]:
        score += 25
    if result["phone_found"]:
        score += 25
    if result["redirected"] and (urllib.parse.urlparse(final_url).hostname or "") != (parsed.hostname or ""):
        score += 10
    if not result["noindex"]:
        score += 10
    if third_party:
        score += 5
    result["exposure_score"] = min(100, score)

    if score >= 50:
        result["verdict"] = "High exposure - review now"
    elif score >= 25:
        result["verdict"] = "Moderate exposure - review"
    else:
        result["verdict"] = "Lower exposure - keep an eye on it"

    return result


def print_report(result: dict[str, Any], email: str | None, phone: str | None) -> None:
    print("=" * 82)
    print(f"  {result['label']}")
    print("=" * 82)
    print(f"Requested : {result['requested_url']}")
    if result["error"]:
        print(f"Status    : ERROR - {result['error']}")
        print("Next step : Check the URL, or remove it if the profile no longer exists.")
        return

    print(f"Final URL : {result['final_url']}")
    print(f"Status    : {result['status']}")
    print(f"HTTPS     : {'yes' if result['https'] else 'NO - plain HTTP'}")
    print(f"Title     : {result['title'] or '(no title)'}")
    print(f"Noindex   : {'yes' if result['noindex'] else 'no - search engines may index it'}")
    print(f"Robots    : {'path is disallowed for polite crawlers' if result['robots_disallow'] else 'not disallowed by robots.txt'}")
    print(f"Exposure  : {result['exposure_score']}/100 - {result['verdict']}")

    if email:
        print(f"Email     : {'FOUND on the page' if result['email_found'] else 'not found'}")
    if phone:
        print(f"Phone     : {'FOUND on the page' if result['phone_found'] else 'not found'}")
    if result["third_party_hosts"]:
        print(f"Third-party assets: {result['third_party_hosts']}")
    else:
        print("Third-party assets: none detected in script/img/iframe tags")

    print("\nWhat to consider:")
    if result["email_found"] or result["phone_found"]:
        print("  - Remove contact details that do not need to be public.")
    if not result["https"]:
        print("  - Use HTTPS. Plain HTTP can expose what you read or submit.")
    if not result["noindex"]:
        print("  - If the page should stay private, set a noindex rule or make it")
        print("    visible only to signed-in users. robots.txt is not access control.")
    if result["redirected"]:
        print("  - The URL redirects. Confirm the final destination is still yours.")
    if result["third_party_hosts"]:
        print("  - Review third-party widgets and remove ones you do not need.")
    print("  - Search your own name and usernames in a private browser window.")
    print("  - Check your email on Have I Been Pwned through the official site.")
    print("  - Delete old accounts you no longer use, starting with the riskiest.")


def write_csv(results: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "label", "requested_url", "final_url", "status", "https", "redirected",
        "title", "noindex", "robots_disallow", "email_found", "phone_found",
        "third_party_hosts", "exposure_score", "verdict", "error",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)


def run_demo(input_path: Path, output_path: Path) -> int:
    profiles = load_profiles(input_path)
    print("=" * 82)
    print("  DIGITAL FOOTPRINT AUDIT - DEMO")
    print("=" * 82)
    print("Using public example domains, not your real profiles.")
    print("Replace profiles_sample.txt with your own URLs to do a real audit.\n")

    results = []
    for index, profile in enumerate(profiles):
        if index:
            time.sleep(1)
        print(f"Checking: {profile['label']} ...")
        try:
            result = analyse_profile(profile["label"], profile["url"], None, None, 10.0)
        except ValueError as error:
            print(f"  invalid URL: {error}")
            continue
        results.append(result)
        print_report(result, None, None)
        print()

    if results:
        write_csv(results, output_path)
        print(f"[+] Report written to: {output_path}")
        print("\nYour turn:")
        print("  1. Create my_profiles.txt with your own public profile URLs.")
        print("  2. Run: py -3 footprint_audit.py --input my_profiles.txt --email you@example.com")
        print("  3. Fix the highest-exposure items first.")
    return 0 if results else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit your own public profiles for basic exposure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 footprint_audit.py --demo\n"
            "  py -3 footprint_audit.py --input profiles_sample.txt\n"
            "  py -3 footprint_audit.py --input my_profiles.txt --email me@example.com\n"
        ),
    )
    parser.add_argument("--input", type=Path, help="Text file with one URL per line, or 'label | url'.")
    parser.add_argument("--output", type=Path, default=Path("footprint_report.csv"), help="CSV output path.")
    parser.add_argument("--email", help="Optional email to check for on your own pages.")
    parser.add_argument("--phone", help="Optional phone number to check for on your own pages.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of detailed reports.")
    parser.add_argument("--demo", action="store_true", help="Use the bundled example profiles.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    input_path = args.input
    if args.demo:
        input_path = base / "profiles_sample.txt"
        if args.output == Path("footprint_report.csv"):
            args.output = base / "samples" / "demo_footprint_report.csv"

    if not input_path:
        parser.print_help()
        print("\nProvide --input FILE, or use --demo.")
        return 1
    if not input_path.is_file():
        print(f"ERROR: file not found: {input_path}")
        return 1

    if args.demo:
        return run_demo(input_path, args.output)

    profiles = load_profiles(input_path)
    if not profiles:
        print("No URLs found in the input file.")
        return 1

    results: list[dict[str, Any]] = []
    for index, profile in enumerate(profiles):
        if index:
            time.sleep(1)
        try:
            result = analyse_profile(
                profile["label"], profile["url"], args.email, args.phone, args.timeout
            )
        except ValueError as error:
            print(f"[!] Skipping {profile['url']}: {error}")
            continue
        results.append(result)
        if not args.json:
            print_report(result, args.email, args.phone)
            print()

    write_csv(results, args.output)

    if args.json:
        print(json.dumps(results, indent=2))
    elif results:
        print("=" * 82)
        print("  SUMMARY")
        print("=" * 82)
        for result in results:
            print(f"{result['exposure_score']:>3}/100  {result['verdict']:<34} {result['label']}")
        print(f"\nCSV report: {args.output}")
        print("\nThis is a simple checklist, not a complete privacy audit. Review the")
        print("manual steps in the project README as well.")

    return 0 if results else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
