#!/usr/bin/env python3
"""
Project 10 - Source Code Treasure Hunt
======================================

Audit a local website folder for information that was accidentally left in
HTML comments, JavaScript, hidden fields, or robots.txt. The point is to learn
how small leftovers can reveal internal paths and clues.

Run:
    py -3 audit_site.py vulnerable_site
    py -3 audit_site.py fixed_site
    py -3 audit_site.py --demo

This tool only reads local files. It does not contact any website.

Safety:
    The vulnerable_site folder is a fictional training target. Its "secrets" are
    fake. Never publish real credentials or internal notes in a public site.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".html", ".htm", ".js", ".mjs", ".css", ".txt", ".json", ".xml",
    ".md", ".yml", ".yaml", ".env", ".ini", ".conf",
}

SUSPICIOUS_WORDS = {
    "admin": "mentions an admin area",
    "password": "mentions a password",
    "secret": "mentions a secret",
    "token": "mentions a token",
    "api_key": "mentions an API key",
    "apikey": "mentions an API key",
    "internal": "mentions internal material",
    "staging": "mentions a staging environment",
    "backup": "mentions a backup",
    "debug": "mentions debug mode",
    "todo": "contains a developer TODO",
    "fixme": "contains a developer FIXME",
}

SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"), "possible hard-coded secret", "high"),
    (re.compile(r"(?i)bearer\s+[a-z0-9._\-]{12,}"), "possible bearer token", "high"),
    (re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]+['\"]"), "possible hard-coded password", "high"),
    (re.compile(r"(?i)(/admin|/backup|/internal|/staging|/private)"), "internal-looking path", "medium"),
    (re.compile(r"(?i)hidden[^>]*name=['\"]?(debug|role|admin)"), "hidden debug or role field", "medium"),
]

HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
JS_LINE_COMMENT_RE = re.compile(r"//[^\n]*")
JS_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


@dataclass
class Finding:
    severity: str
    file: Path
    line: int
    message: str
    evidence: str


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def clean_evidence(value: str, limit: int = 120) -> str:
    value = " ".join(value.split())
    return value[:limit] + ("..." if len(value) > limit else "")


def check_text_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings

    relative = path.relative_to(root)

    for match in HTML_COMMENT_RE.finditer(text):
        comment = match.group(1)
        findings.append(
            Finding(
                "medium",
                relative,
                line_number(text, match.start()),
                "HTML comment left in the page",
                clean_evidence(comment),
            )
        )

    comment_spans: list[tuple[int, int, str]] = []
    for match in JS_BLOCK_COMMENT_RE.finditer(text):
        comment_spans.append((match.start(), match.end(), match.group(0)))
    if path.suffix.lower() in {".js", ".mjs"}:
        for match in JS_LINE_COMMENT_RE.finditer(text):
            comment_spans.append((match.start(), match.end(), match.group(0)))

    for _, _, comment in comment_spans:
        findings.append(
            Finding(
                "low",
                relative,
                line_number(text, text.find(comment)),
                "JavaScript comment worth reviewing",
                clean_evidence(comment),
            )
        )

    lowered = text.lower()
    for word, explanation in SUSPICIOUS_WORDS.items():
        start = 0
        while True:
            index = lowered.find(word, start)
            if index == -1:
                break
            # Do not double-report every word inside a comment we already flagged.
            inside_comment = any(begin <= index < end for begin, end, _ in comment_spans)
            if not inside_comment:
                findings.append(
                    Finding(
                        "low",
                        relative,
                        line_number(text, index),
                        f"Suspicious wording: {explanation}",
                        clean_evidence(text[max(0, index - 45): index + 75]),
                    )
                )
            start = index + len(word)

    for pattern, message, severity in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    severity,
                    relative,
                    line_number(text, match.start()),
                    message,
                    clean_evidence(match.group(0)),
                )
            )

    return findings


def check_robots(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings

    for number, line in enumerate(lines, start=1):
        if line.strip().lower().startswith("disallow:"):
            target = line.split(":", 1)[1].strip()
            if target and target != "/":
                findings.append(
                    Finding(
                        "medium",
                        path.relative_to(root),
                        number,
                        "robots.txt reveals a path (it does not protect it)",
                        clean_evidence(line),
                    )
                )
    return findings


def audit_folder(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        if path.name == "robots.txt":
            findings.extend(check_robots(path, root))
        if path.suffix.lower() in TEXT_EXTENSIONS:
            findings.extend(check_text_file(path, root))
    return findings


def print_findings(root: Path, findings: list[Finding]) -> None:
    print("=" * 78)
    print(f"  AUDIT: {root}")
    print("=" * 78)

    if not findings:
        print("\n[+] No leftover comments, fake secrets, or risky robots entries found.")
        print("    This does not prove the site is secure; it only means this simple")
        print("    checklist came back clean.")
        return

    order = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(findings, key=lambda item: (order[item.severity], str(item.file), item.line))

    counts = {"high": 0, "medium": 0, "low": 0}
    for finding in findings:
        counts[finding.severity] += 1
        print(f"\n[{finding.severity.upper():<6}] {finding.file}:{finding.line}")
        print(f"  {finding.message}")
        print(f"  Evidence: {finding.evidence}")

    print("\n" + "-" * 78)
    print(f"Summary: {counts['high']} high, {counts['medium']} medium, {counts['low']} low")
    print("High findings deserve immediate removal. Medium findings reveal clues.")
    print("Low findings are context, not necessarily vulnerabilities.")


def run_demo() -> None:
    base = Path(__file__).resolve().parent
    vulnerable = base / "vulnerable_site"
    fixed = base / "fixed_site"

    print("=" * 78)
    print("  SOURCE CODE TREASURE HUNT - BEFORE AND AFTER")
    print("=" * 78)
    print("Auditing the intentionally leaky training site...\n")
    vulnerable_findings = audit_folder(vulnerable)
    print_findings(vulnerable, vulnerable_findings)

    print("\n\nAuditing the cleaned-up version...\n")
    fixed_findings = audit_folder(fixed)
    print_findings(fixed, fixed_findings)

    print("\n" + "=" * 78)
    print("  WHAT CHANGED?")
    print("=" * 78)
    print(f"Vulnerable site findings: {len(vulnerable_findings)}")
    print(f"Fixed site findings     : {len(fixed_findings)}")
    print("\nThe fixed version removed comments, fake keys, hidden debug fields,")
    print("and the sensitive robots.txt entries. Information disclosure is often")
    print("just a leftover, not a sophisticated attack.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a local website folder for accidental information leaks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 audit_site.py vulnerable_site\n"
            "  py -3 audit_site.py fixed_site\n"
            "  py -3 audit_site.py --demo\n"
        ),
    )
    parser.add_argument("folder", nargs="?", type=Path, help="Website folder to audit.")
    parser.add_argument("--demo", action="store_true", help="Compare the vulnerable and fixed sites.")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return 0

    if not args.folder:
        parser.print_help()
        print("\nProvide a folder, or use --demo.")
        return 1

    if not args.folder.is_dir():
        print(f"ERROR: folder not found: {args.folder}")
        return 1

    findings = audit_folder(args.folder.resolve())
    print_findings(args.folder.resolve(), findings)
    return 1 if any(item.severity == "high" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
