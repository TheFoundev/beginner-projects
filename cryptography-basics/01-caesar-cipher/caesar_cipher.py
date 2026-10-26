#!/usr/bin/env python3
"""
Project 01 - Secret Agent Starter Kit: Build Your First Cipher
=============================================================

A beginner-friendly Caesar cipher. It can encode, decode, and brute-force
a message by trying every possible shift.

This is a *learning* cipher. Never use it to protect real secrets.

Examples
--------
    py -3 caesar_cipher.py --message "HELLO WORLD" --shift 3
    py -3 caesar_cipher.py --message "KHOOR ZRUOG" --shift 3 --decode
    py -3 caesar_cipher.py --message "KHOOR ZRUOG" --brute-force
    py -3 caesar_cipher.py --demo
    py -3 caesar_cipher.py
"""

from __future__ import annotations

import argparse
import sys


def shift_character(character: str, shift: int) -> str:
    """Move one letter through the alphabet, wrapping Z back to A."""
    if character.isupper():
        base = ord("A")
    elif character.islower():
        base = ord("a")
    else:
        # Spaces, punctuation, and numbers do not change.
        return character

    return chr((ord(character) - base + shift) % 26 + base)


def caesar(text: str, shift: int) -> str:
    """Encode text with a Caesar shift (decode by using a negative shift)."""
    shift %= 26
    return "".join(shift_character(char, shift) for char in text)


def brute_force(ciphertext: str) -> None:
    """Print all 26 possible decodings, because a Caesar cipher is weak."""
    print("\nTrying every possible shift:\n")
    for shift in range(26):
        candidate = caesar(ciphertext, -shift)
        marker = "  <-- readable?" if shift == 3 else ""
        print(f"  shift {shift:2d}: {candidate}{marker}")


def interactive_mode() -> None:
    """A friendly prompt for learners who just want to try it."""
    print("=" * 58)
    print("  SECRET AGENT STARTER KIT")
    print("=" * 58)
    print("The Caesar cipher moves every letter by the same number of steps.")
    print("Example: HELLO with shift 3 becomes KHOOR.\n")

    message = input("Enter a message: ")
    if not message:
        print("No message entered. Try again with some text.")
        return

    while True:
        raw_shift = input("Enter a shift number (0-25): ").strip()
        try:
            shift = int(raw_shift)
            if 0 <= shift <= 25:
                break
        except ValueError:
            pass
        print("Please enter a whole number from 0 to 25.")

    mode = input("Do you want to (E)ncode or (D)ecode? [E/d]: ").strip().lower()
    if mode.startswith("d"):
        result = caesar(message, -shift)
        action = "Decoded"
    else:
        result = caesar(message, shift)
        action = "Encoded"

    print(f"\n{action} message: {result}")
    print("\nChallenge: send that result to a friend and see if they can")
    print("work out the shift without looking at the number.")


def run_demo() -> None:
    """A zero-setup demonstration that always works."""
    print("=" * 58)
    print("  DEMO: HELLO WORLD -> ?")
    print("=" * 58)

    plaintext = "HELLO WORLD"
    shift = 3
    encoded = caesar(plaintext, shift)
    decoded = caesar(encoded, -shift)

    print(f"Plaintext : {plaintext}")
    print(f"Shift     : {shift}")
    print(f"Encoded   : {encoded}")
    print(f"Decoded   : {decoded}")
    print(f"Round trip: {'PASS' if decoded == plaintext else 'FAIL'}")
    brute_force(encoded)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encode, decode, or brute-force a Caesar cipher.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  py -3 caesar_cipher.py --message "HELLO" --shift 3\n'
            '  py -3 caesar_cipher.py --message "KHOOR" --shift 3 --decode\n'
            '  py -3 caesar_cipher.py --message "KHOOR" --brute-force\n'
            "  py -3 caesar_cipher.py --demo\n"
        ),
    )
    parser.add_argument("--message", "-m", help="Text to encode or decode.")
    parser.add_argument("--shift", "-s", type=int, default=3, help="Number of alphabet steps (default: 3).")
    parser.add_argument("--decode", "-d", action="store_true", help="Decode instead of encode.")
    parser.add_argument("--brute-force", "-b", action="store_true", help="Try all 26 possible shifts.")
    parser.add_argument("--demo", action="store_true", help="Run a built-in demonstration.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return 0

    if args.message is None:
        interactive_mode()
        return 0

    shift = args.shift % 26
    if args.decode:
        result = caesar(args.message, -shift)
        print(f"Decoded (shift {shift}): {result}")
    else:
        result = caesar(args.message, shift)
        print(f"Encoded (shift {shift}): {result}")

    if args.brute_force:
        brute_force(result if args.decode else caesar(args.message, shift))

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nGoodbye, agent.")
        sys.exit(130)
