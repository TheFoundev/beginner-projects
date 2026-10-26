#!/usr/bin/env python3
"""
Project 03 - Hash Detective: The Digital Fingerprint
====================================================

A hash is a one-way fingerprint for data. This tool creates SHA-256
fingerprints for files or text, compares them with an expected value, and
demonstrates how a one-character change creates a completely new hash.

Run:
    py -3 hash_detective.py --file notes.txt
    py -3 hash_detective.py --file notes.txt --expected <sha256>
    py -3 hash_detective.py --text "hello"
    py -3 hash_detective.py --demo

Safety:
    Only hash files you own. Hashing is read-only and does not modify the file.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from pathlib import Path


def hash_bytes(data: bytes) -> str:
    """Return the SHA-256 fingerprint of some bytes as a hex string."""
    return hashlib.sha256(data).hexdigest()


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """
    Hash a file in chunks so even large files use very little memory.

    The file is opened in binary mode: hashes work on exact bytes, not text.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def compare(expected: str, actual: str) -> bool:
    """Compare fingerprints safely, ignoring case and accidental spaces."""
    return expected.strip().lower() == actual.strip().lower()


def print_hash(label: str, value: str) -> None:
    print(f"{label:<18} {value}")
    print(f"{'':<18} ({len(value)} hexadecimal characters)")


def run_demo() -> None:
    """Create a file, hash it, tamper with it, and compare the fingerprints."""
    print("=" * 70)
    print("  HASH DETECTIVE - DEMO")
    print("=" * 70)

    with tempfile.TemporaryDirectory(prefix="hash-demo-") as temp_dir:
        path = Path(temp_dir) / "secret_note.txt"
        original = b"The meeting is at 10:00 in room 4.\n"
        path.write_bytes(original)

        first = hash_file(path)
        print("\n1. Original file")
        print(f"   Content: {original.decode().strip()}")
        print_hash("SHA-256:", first)

        tampered = b"The meeting is at 10:00 in room 5.\n"
        path.write_bytes(tampered)
        second = hash_file(path)
        print("\n2. After changing one character (4 -> 5)")
        print(f"   Content: {tampered.decode().strip()}")
        print_hash("SHA-256:", second)

        print("\n3. Comparison")
        print(f"   Same fingerprint? {'YES' if first == second else 'NO'}")
        print(f"   Characters changed: {sum(a != b for a, b in zip(first, second))} of 64")
        print("\nThis is the avalanche effect: a tiny change creates a wildly")
        print("different fingerprint. That is why hashes are useful for spotting")
        print("tampered downloads, but useless for hiding the original data.")

        print("\n4. Verify an expected fingerprint")
        expected = first
        print(f"   Expected: {expected}")
        print(f"   Actual  : {second}")
        print(f"   Match?  {'YES' if compare(expected, second) else 'NO - tampering detected'}")

        print("\n5. The same input always gives the same hash")
        print(f"   Hash of original again: {hash_bytes(original)}")
        print(f"   Matches first hash?    {'YES' if hash_bytes(original) == first else 'NO'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and verify SHA-256 fingerprints.",
        epilog=(
            "Examples:\n"
            "  py -3 hash_detective.py --file notes.txt\n"
            "  py -3 hash_detective.py --file download.zip --expected abc123...\n"
            '  py -3 hash_detective.py --text "hello"\n'
            "  py -3 hash_detective.py --demo\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--file", "-f", type=Path, help="File to fingerprint.")
    source.add_argument("--text", "-t", help="Text to fingerprint instead of a file.")
    parser.add_argument("--expected", "-e", help="Expected SHA-256 value to compare against.")
    parser.add_argument("--demo", action="store_true", help="Run a tamper-detection demonstration.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return 0

    if args.file is None and args.text is None:
        parser.print_help()
        print("\nNo input provided. Use --file, --text, or --demo.")
        return 1

    if args.file is not None:
        if not args.file.exists() or not args.file.is_file():
            print(f"ERROR: file not found: {args.file}")
            return 1
        actual = hash_file(args.file)
        print(f"File: {args.file}")
    else:
        actual = hash_bytes(args.text.encode("utf-8"))
        print(f"Text: {args.text}")

    print_hash("SHA-256:", actual)

    if args.expected:
        if compare(args.expected, actual):
            print("\nRESULT: MATCH - the data matches the expected fingerprint.")
            return 0
        print("\nRESULT: NO MATCH - the file may be corrupted, altered, or from a different source.")
        return 2

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
