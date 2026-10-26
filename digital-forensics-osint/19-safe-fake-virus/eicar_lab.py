#!/usr/bin/env python3
"""
Project 19 - The Safe Fake Virus: Meet the EICAR Test File
==========================================================

EICAR is a harmless text string that antivirus products agree to detect as a
test. It is not malware and it cannot do anything. It exists so you can safely
see whether your antivirus is awake.

Run:
    py -3 eicar_lab.py create
    py -3 eicar_lab.py inspect lab/eicar.com.txt
    py -3 eicar_lab.py cleanup lab/eicar.com.txt
    py -3 eicar_lab.py demo

Safety:
    EICAR is harmless, but it will probably trigger an antivirus alert. That is
    the point. Do not email it to people, upload it to random sites, or rename it
    to pretend it is real malware. Only create it on your own test machine.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

EICAR_TEXT = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
# The standard file is 68 bytes with no trailing newline. Some editors add one;
# inspect_file() accepts that harmless variant too.
EICAR_BYTES = EICAR_TEXT.encode("ascii")
EICAR_SHA256 = hashlib.sha256(EICAR_BYTES).hexdigest()
DEFAULT_PATH = Path(__file__).resolve().parent / "lab" / "eicar.com.txt"


def create_test_file(path: Path, force: bool = False) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path} (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(EICAR_BYTES)
    print("=" * 76)
    print("  EICAR TEST FILE CREATED")
    print("=" * 76)
    print(f"Path   : {path}")
    print(f"Size   : {len(EICAR_BYTES)} bytes")
    print(f"SHA-256: {EICAR_SHA256}")
    print("\nThis file is HARMLESS. It is a standard antivirus test string.")
    print("Your antivirus may quarantine or delete it immediately. That is a")
    print("successful test, not a problem.")
    print("\nTry:")
    print(f"  py -3 eicar_lab.py inspect \"{path}\"")
    print(f"  py -3 eicar_lab.py cleanup \"{path}\"")


def inspect_file(path: Path) -> int:
    print("=" * 76)
    print("  EICAR TEST FILE INSPECTION")
    print("=" * 76)

    if not path.is_file():
        print(f"File not found: {path}")
        print("If you just created it, your antivirus may have quarantined it.")
        print("That is a successful detection test. Check your antivirus history.")
        return 1

    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    exact = data == EICAR_BYTES
    without_newline = data.strip() == EICAR_TEXT.encode("ascii")
    is_eicar = exact or without_newline

    print(f"Path          : {path}")
    print(f"Size          : {len(data)} bytes")
    print(f"SHA-256       : {digest}")
    print(f"Exact match   : {'yes' if exact else 'no'}")
    print(f"EICAR variant : {'yes' if without_newline else 'no'}")
    print(f"Verdict       : {'HARMLESS EICAR TEST FILE' if is_eicar else 'UNKNOWN - do not run'}")

    if is_eicar:
        print("\nWhat now?")
        print("  1. If your antivirus alerts, that is expected and good.")
        print("  2. Do not double-click the file or send it to anyone.")
        print("  3. Delete it with the cleanup command below.")
        print(f"\n  py -3 eicar_lab.py cleanup \"{path}\"")
        return 0

    print("\nThis file does not match the standard EICAR test string.")
    print("Do not open it. Delete it and investigate where it came from.")
    return 2


def cleanup_file(path: Path, assume_yes: bool = False) -> int:
    if not path.exists():
        print(f"Nothing to clean up: {path} does not exist.")
        print("It may already have been deleted or quarantined.")
        return 0

    if not assume_yes:
        answer = input(f"Delete this harmless test file? {path} [y/N]: ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled. The file was not deleted.")
            return 1

    path.unlink()
    print(f"[+] Deleted: {path}")
    return 0


def print_first_responder_checklist() -> None:
    print("\n" + "=" * 76)
    print("  FIRST RESPONDER CHECKLIST (for a REAL malware scare)")
    print("=" * 76)
    print("EICAR is harmless, but the habits are the same for a suspicious file:")
    print("  1. Stop using the device. Do not open the file.")
    print("  2. Disconnect from Wi-Fi/Ethernet if you suspect real malware.")
    print("  3. Write down what happened: time, file name, where it came from.")
    print("  4. Record the SHA-256 hash before deleting, if it is safe to do so.")
    print("  5. Run a full antivirus scan and follow its instructions.")
    print("  6. Tell your school/workplace IT or security team.")
    print("  7. Change important passwords from a different, clean device.")
    print("  8. Do not pay a ransom or install random 'cleanup' tools.")
    print("\nFor EICAR specifically: an antivirus alert is the expected result.")


def run_demo() -> None:
    print("=" * 76)
    print("  THE SAFE FAKE VIRUS - DEMO")
    print("=" * 76)
    print("Creating EICAR in a temporary folder so nothing is left behind.\n")

    with tempfile.TemporaryDirectory(prefix="eicar-demo-") as temporary:
        path = Path(temporary) / "eicar.com.txt"
        create_test_file(path)
        print()
        code = inspect_file(path)
        if code == 0:
            print("\nCreating a second copy to show the overwrite guard...")
            try:
                create_test_file(path)
            except FileExistsError as error:
                print(f"[+] Guard worked: {error}")
            cleanup_file(path, assume_yes=True)

    print_first_responder_checklist()
    print("\nKey lesson: a file can be tiny, harmless, and still trigger security")
    print("tools. Always verify what a file is before you trust it.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safely create, inspect, and delete the harmless EICAR test file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 eicar_lab.py create\n"
            "  py -3 eicar_lab.py inspect lab/eicar.com.txt\n"
            "  py -3 eicar_lab.py cleanup lab/eicar.com.txt\n"
            "  py -3 eicar_lab.py demo\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create the harmless test file.")
    create_parser.add_argument("--path", type=Path, default=DEFAULT_PATH, help="Where to write the file.")
    create_parser.add_argument("--force", action="store_true", help="Overwrite an existing file.")

    inspect_parser = subparsers.add_parser("inspect", help="Check whether a file is the EICAR test file.")
    inspect_parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)

    cleanup_parser = subparsers.add_parser("cleanup", help="Delete the test file.")
    cleanup_parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    cleanup_parser.add_argument("--yes", action="store_true", help="Delete without asking.")

    subparsers.add_parser("demo", help="Create, inspect, and remove a temporary test file.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create":
        try:
            create_test_file(args.path, force=args.force)
        except (FileExistsError, OSError) as error:
            print(f"ERROR: {error}")
            return 1
        print_first_responder_checklist()
        return 0

    if args.command == "inspect":
        return inspect_file(args.path)

    if args.command == "cleanup":
        return cleanup_file(args.path, assume_yes=args.yes)

    if args.command == "demo":
        run_demo()
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
