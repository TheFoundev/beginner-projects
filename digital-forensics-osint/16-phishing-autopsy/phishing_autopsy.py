#!/usr/bin/env python3
"""
Project 16 - Phishing Autopsy: Dissect a Suspicious Email Safely
================================================================

Parse .eml files and explain the red flags: failed authentication, mismatched
sender domains, urgent language, dangerous attachments, and links that do not
go where they claim.

Run:
    py -3 phishing_autopsy.py samples/01-password-reset.eml
    py -3 phishing_autopsy.py samples/*.eml
    py -3 phishing_autopsy.py --demo
    py -3 phishing_autopsy.py samples/01-password-reset.eml --json

Safety:
    This is an offline parser. It never opens attachments, never loads remote
    images, and never visits links. Treat all suspicious email as evidence.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from email import policy
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
DOMAIN_IN_TEXT_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\b", re.IGNORECASE)

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
    "rebrand.ly", "cutt.ly", "shorturl.at", "tiny.cc",
}
SUSPICIOUS_TLDS = {
    "zip", "mov", "top", "xyz", "click", "loan", "work", "support", "rest",
    "fit", "cam", "quest", "monster", "sbs", "cfd",
}
DANGEROUS_EXTENSIONS = {
    ".exe", ".scr", ".js", ".vbs", ".bat", ".cmd", ".com", ".pif", ".lnk",
    ".iso", ".img", ".docm", ".xlsm", ".pptm", ".hta", ".jar", ".ps1",
}
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz"}

URGENCY_PHRASES = (
    "urgent", "immediately", "within 24 hours", "final notice", "last warning",
    "account will be suspended", "account will be closed", "act now",
    "expires today", "failure to comply",
)
CREDENTIAL_PHRASES = (
    "verify your account", "confirm your password", "reset your password",
    "update your payment", "sign in", "log in", "login", "validate your account",
)
MONEY_PHRASES = (
    "invoice", "payment", "wire transfer", "gift card", "cryptocurrency",
    "refund", "overdue", "bank details", "purchase order",
)


class EmailHTMLParser(HTMLParser):
    """Collect visible text, links, and whether the email contains a form."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.has_form = False
        self._current_href: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "form":
            self.has_form = True
        if tag.lower() == "a":
            attributes = {key.lower(): value or "" for key, value in attrs}
            self._current_href = attributes.get("href")
            self._anchor_text = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_parts.append(data)
            if self._current_href is not None:
                self._anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href is not None:
            text = " ".join(" ".join(self._anchor_text).split())
            self.links.append((self._current_href, text))
            self._current_href = None
            self._anchor_text = []

    def visible_text(self) -> str:
        return " ".join(" ".join(self.text_parts).split())


def decode_header_value(value: Any) -> str:
    if value is None:
        return ""
    try:
        chunks = []
        for part, encoding in decode_header(str(value)):
            if isinstance(part, bytes):
                chunks.append(part.decode(encoding or "utf-8", errors="replace"))
            else:
                chunks.append(part)
        return "".join(chunks)
    except Exception:
        return str(value)


def domain_of(address: str) -> str:
    _, email_address = parseaddr(address)
    return email_address.rpartition("@")[2].lower().strip(".")


def domains_match(first: str, second: str) -> bool:
    if not first or not second:
        return False
    return first == second or first.endswith("." + second) or second.endswith("." + first)


def clean_url(value: str) -> str:
    return value.strip().rstrip(".,;:)]}\"'")


def extract_urls(text: str) -> list[str]:
    found: list[str] = []
    for match in URL_RE.finditer(text):
        value = clean_url(match.group(0))
        if value not in found:
            found.append(value)
    return found


def parse_links_and_html(html_body: str) -> tuple[list[tuple[str, str]], bool, str]:
    parser = EmailHTMLParser()
    try:
        parser.feed(html_body)
        parser.close()
    except Exception:
        pass
    links = [(clean_url(href), text) for href, text in parser.links if href.lower().startswith(("http://", "https://"))]
    return links, parser.has_form, parser.visible_text()


def analyse_email(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > 10_000_000:
        raise ValueError("Email is larger than 10 MB; this teaching parser refuses it.")

    message = BytesParser(policy=policy.default).parsebytes(raw)

    from_header = decode_header_value(message.get("From", ""))
    reply_header = decode_header_value(message.get("Reply-To", ""))
    return_header = decode_header_value(message.get("Return-Path", ""))
    subject = decode_header_value(message.get("Subject", ""))
    date = decode_header_value(message.get("Date", ""))
    message_id = decode_header_value(message.get("Message-ID", ""))
    auth_results = " ".join(str(item) for item in message.get_all("Authentication-Results", []))
    received_spf = " ".join(str(item) for item in message.get_all("Received-SPF", []))

    from_display, from_address = parseaddr(from_header)
    reply_address = parseaddr(reply_header)[1]
    return_address = parseaddr(return_header)[1]
    from_domain = from_address.rpartition("@")[2].lower()
    reply_domain = reply_address.rpartition("@")[2].lower()
    return_domain = return_address.rpartition("@")[2].lower()

    plain_parts: list[str] = []
    html_parts: list[str] = []
    attachments: list[dict[str, Any]] = []
    links: list[tuple[str, str]] = []
    has_form = False

    for part in message.walk():
        content_type = part.get_content_type()
        disposition = part.get_content_disposition()
        filename = part.get_filename()
        if filename:
            filename = decode_header_value(filename)

        if filename or disposition == "attachment":
            payload = part.get_payload(decode=True) or b""
            attachments.append(
                {
                    "filename": filename or "(unnamed)",
                    "content_type": content_type,
                    "size_bytes": len(payload),
                }
            )
            continue

        if content_type == "text/plain":
            try:
                plain_parts.append(part.get_content())
            except Exception:
                payload = part.get_payload(decode=True) or b""
                plain_parts.append(payload.decode("utf-8", errors="replace"))
        elif content_type == "text/html":
            try:
                html_body = part.get_content()
            except Exception:
                payload = part.get_payload(decode=True) or b""
                html_body = payload.decode("utf-8", errors="replace")
            html_parts.append(html_body)
            parsed_links, form_found, visible = parse_links_and_html(html_body)
            links.extend(parsed_links)
            has_form = has_form or form_found
            if visible:
                plain_parts.append(visible)

    body_text = "\n".join(plain_parts)
    all_text = f"{subject}\n{body_text}".lower()

    findings: list[dict[str, Any]] = []

    def add(points: int, reason: str, evidence: str = "") -> None:
        findings.append({"points": points, "reason": reason, "evidence": evidence})

    # Authentication results
    auth_blob = f"{auth_results} {received_spf}".lower()
    if not auth_blob.strip():
        add(5, "No visible SPF/DKIM/DMARC results", "The message has no Authentication-Results or Received-SPF header.")
    for mechanism, label, points in (
        ("spf", "SPF", 20),
        ("dkim", "DKIM", 15),
        ("dmarc", "DMARC", 25),
    ):
        if re.search(rf"\b{mechanism}=fail\b", auth_blob):
            add(points, f"{label} authentication failed", f"{label} reported a failure.")
        elif re.search(rf"\b{mechanism}=softfail\b", auth_blob):
            add(max(5, points // 2), f"{label} returned softfail", f"{label} reported a soft failure.")

    # Sender identity mismatch
    if reply_domain and from_domain and not domains_match(reply_domain, from_domain):
        add(15, "Reply-To points to a different domain", f"From: {from_domain} | Reply-To: {reply_domain}")
    if return_domain and from_domain and not domains_match(return_domain, from_domain):
        add(10, "Return-Path domain differs from From", f"From: {from_domain} | Return-Path: {return_domain}")
    if from_display and re.search(r"\b(it|helpdesk|security|billing|account|support)\b", from_display.lower()):
        if from_domain in {"gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "proton.me"}:
            add(10, "Role-style display name using a free email domain", f"{from_display} <{from_address}>")

    # Language pressure
    urgency_hits = [phrase for phrase in URGENCY_PHRASES if phrase in all_text]
    credential_hits = [phrase for phrase in CREDENTIAL_PHRASES if phrase in all_text]
    money_hits = [phrase for phrase in MONEY_PHRASES if phrase in all_text]
    if urgency_hits:
        add(min(18, 6 * len(urgency_hits)), "Urgent or threatening language", ", ".join(urgency_hits[:4]))
    if credential_hits:
        add(min(16, 8 * len(credential_hits)), "Requests account or credential action", ", ".join(credential_hits[:4]))
    if money_hits:
        add(min(12, 6 * len(money_hits)), "Payment or invoice pressure", ", ".join(money_hits[:4]))

    # Links
    plain_urls = extract_urls(body_text)
    link_urls = [href for href, _ in links]
    urls = []
    for value in plain_urls + link_urls:
        if value not in urls:
            urls.append(value)

    link_hosts: set[str] = set()
    for value in urls:
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        if host:
            link_hosts.add(host)

    if link_hosts and from_domain and not any(domains_match(host, from_domain) for host in link_hosts):
        add(15, "Links do not use the sender's domain", f"Sender: {from_domain} | Links: {', '.join(sorted(link_hosts))}")

    for value in urls:
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        if not host:
            continue
        try:
            ipaddress.ip_address(host)
            add(20, "Link uses a raw IP address", value)
        except ValueError:
            pass
        if host in SHORTENERS:
            add(10, "Link uses a URL shortener", value)
        if host.startswith("xn--") or ".xn--" in host:
            add(20, "Link uses punycode, which can disguise lookalike characters", value)
        tld = host.rsplit(".", 1)[-1]
        if tld in SUSPICIOUS_TLDS:
            add(8, f"Link uses a high-risk top-level domain .{tld}", value)
        if parsed.scheme == "http":
            add(8, "Link uses plain HTTP instead of HTTPS", value)

    # Link text that claims one domain but points to another
    for href, text in links:
        parsed = urlparse(href)
        actual_host = (parsed.hostname or "").lower()
        if not actual_host or not text:
            continue
        candidate = URL_RE.search(text)
        claimed = urlparse(candidate.group(0)).hostname if candidate else None
        if not claimed:
            domain_match = DOMAIN_IN_TEXT_RE.search(text)
            claimed = domain_match.group(0) if domain_match else None
        if claimed and not domains_match(claimed.lower(), actual_host):
            add(20, "Displayed link text does not match the real destination", f"Shows: {claimed} | Goes to: {actual_host}")

    if has_form:
        add(25, "HTML email contains a form", "Legitimate services usually send you to their own site instead of collecting credentials inside email.")

    # Attachments
    for attachment in attachments:
        filename = attachment["filename"].lower()
        extension = Path(filename).suffix.lower()
        if extension in DANGEROUS_EXTENSIONS:
            add(30, "Dangerous attachment type", attachment["filename"])
        elif extension in ARCHIVE_EXTENSIONS:
            add(10, "Archive attachment can hide another file type", attachment["filename"])

    score = min(100, sum(item["points"] for item in findings))
    if score >= 60:
        verdict = "HIGH RISK - likely phishing"
    elif score >= 30:
        verdict = "SUSPICIOUS - verify through a separate channel"
    else:
        verdict = "LOW SIGNALS - still verify before acting"

    return {
        "file": str(path),
        "subject": subject,
        "from": from_header,
        "from_address": from_address,
        "from_domain": from_domain,
        "reply_to": reply_header,
        "return_path": return_header,
        "to": decode_header_value(message.get("To", "")),
        "date": date,
        "message_id": message_id,
        "auth_results": auth_results,
        "received_spf": received_spf,
        "urls": urls,
        "links": [{"href": href, "text": text} for href, text in links],
        "attachments": attachments,
        "has_form": has_form,
        "findings": findings,
        "score": score,
        "verdict": verdict,
        "body_preview": body_text.strip()[:700],
    }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 80)
    print("  PHISHING AUTOPSY")
    print("=" * 80)
    print(f"File    : {report['file']}")
    print(f"Subject : {report['subject']}")
    print(f"From    : {report['from']}")
    print(f"Reply-To: {report['reply_to'] or '(none)'}")
    print(f"Return-Path: {report['return_path'] or '(none)'}")
    print(f"Date    : {report['date']}")
    print(f"Score   : {report['score']}/100")
    print(f"Verdict : {report['verdict']}")

    print("\nAuthentication:")
    if report["auth_results"]:
        print(f"  {report['auth_results'][:300]}")
    elif report["received_spf"]:
        print(f"  {report['received_spf'][:300]}")
    else:
        print("  (no authentication headers found)")

    print("\nLinks found (not visited):")
    if report["links"]:
        for link in report["links"]:
            text = f" | text: {link['text'][:80]}" if link["text"] else ""
            print(f"  - {link['href']}{text}")
    elif report["urls"]:
        for url in report["urls"]:
            print(f"  - {url}")
    else:
        print("  (none)")

    print("\nAttachments (not opened):")
    if report["attachments"]:
        for attachment in report["attachments"]:
            print(
                f"  - {attachment['filename']} ({attachment['content_type']}, "
                f"{attachment['size_bytes']} bytes)"
            )
    else:
        print("  (none)")

    print("\nRed flags:")
    if report["findings"]:
        for finding in sorted(report["findings"], key=lambda item: -item["points"]):
            print(f"  +{finding['points']:>2}  {finding['reason']}")
            if finding["evidence"]:
                print(f"        {finding['evidence'][:180]}")
    else:
        print("  No obvious red flags in this simple checklist. That is not a guarantee.")

    print("\nBody preview:")
    preview = report["body_preview"].replace("\n", " ")
    print(f"  {preview if preview else '(no readable text body)'}")

    print("\nWhat to do next:")
    print("  1. Do not click links or open attachments.")
    print("  2. Verify through a separate channel: type the official domain yourself")
    print("     or call the organization using a number you already trust.")
    print("  3. Report it using your school or workplace phishing button.")
    print("  4. If you already clicked, change affected passwords from a clean device")
    print("     and tell your IT/security team.")
    print("\nThis tool is a checklist, not a verdict from a security team.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze .eml files for common phishing red flags without opening them.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 phishing_autopsy.py samples/01-password-reset.eml\n"
            "  py -3 phishing_autopsy.py samples/*.eml\n"
            "  py -3 phishing_autopsy.py --demo\n"
            "  py -3 phishing_autopsy.py samples/01-password-reset.eml --json\n"
        ),
    )
    parser.add_argument("files", nargs="*", type=Path, help="One or more .eml files.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of reports.")
    parser.add_argument("--demo", action="store_true", help="Analyze all bundled sample emails.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    files = list(args.files)
    if args.demo:
        files = sorted((Path(__file__).resolve().parent / "samples").glob("*.eml"))

    if not files:
        parser.print_help()
        print("\nProvide an .eml file, or use --demo.")
        return 1

    reports: list[dict[str, Any]] = []
    for path in files:
        if not path.is_file():
            print(f"[!] File not found: {path}")
            continue
        try:
            report = analyse_email(path)
        except Exception as error:
            print(f"[!] Could not analyze {path}: {error}")
            continue
        reports.append(report)
        if not args.json:
            print_report(report)
            print()

    if args.json:
        print(json.dumps(reports, indent=2))

    if reports and not args.json:
        print("=" * 80)
        print("  SUMMARY")
        print("=" * 80)
        for report in reports:
            print(f"{report['score']:>3}/100  {report['verdict']:<52} {Path(report['file']).name}")
        print("\nRemember: a low score does not prove an email is safe. Verify important")
        print("requests through a channel you already trust.")

    return 0 if reports else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
