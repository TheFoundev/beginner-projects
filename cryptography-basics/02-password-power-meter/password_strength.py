#!/usr/bin/env python3
"""
Project 02 - The Password Power Meter
=====================================

A friendly password-strength checker that runs entirely on your computer.
It never saves, sends, or displays the password you type.

Run:
    py -3 password_strength.py
    py -3 password_strength.py --demo

Safety:
    Use made-up passwords while learning. Never type a real password into
    random websites, online checkers, or code you found on the internet.
"""

from __future__ import annotations

import getpass
import math
import re
import string
import sys


COMMON_PASSWORDS = {
    "123456", "123456789", "12345678", "password", "qwerty", "12345",
    "123123", "111111", "abc123", "password1", "iloveyou", "admin",
    "welcome", "monkey", "letmein", "dragon", "football", "master",
    "sunshine", "princess", "login", "passw0rd", "starwars", "whatever",
    "trustno1", "qwerty123", "1q2w3e4r", "zaq12wsx", "superman",
}

KEYBOARD_SEQUENCES = (
    "qwerty", "asdf", "zxcv", "1234", "2345", "3456", "4567", "5678",
    "6789", "7890", "abcd", "bcde", "cdef", "defg", "efgh", "fghi",
)


def estimate_character_pool(password: str) -> int:
    """Estimate how many different characters an attacker might try."""
    pool = 0
    if any(char.islower() for char in password):
        pool += 26
    if any(char.isupper() for char in password):
        pool += 26
    if any(char.isdigit() for char in password):
        pool += 10
    if any(char in string.punctuation for char in password):
        pool += len(string.punctuation)
    if " " in password:
        pool += 1
    return pool


def estimate_entropy_bits(password: str) -> float:
    """
    Rough entropy: length x log2(pool size).

    This is a useful teaching estimate, not a promise about crack time.
    Real attackers also use dictionaries, leaked passwords, and patterns.
    """
    pool = estimate_character_pool(password)
    if pool <= 1 or not password:
        return 0.0
    return len(password) * math.log2(pool)


def has_common_word_shape(password: str) -> bool:
    """Catch things like 'password123' and 'welcome2026'."""
    lowered = password.lower()
    if lowered in COMMON_PASSWORDS:
        return True
    stripped = re.sub(r"[^a-z]", "", lowered)
    if stripped in COMMON_PASSWORDS:
        return True
    # Remove trailing digits/symbols and check again.
    base = re.sub(r"[\d\W_]+$", "", lowered)
    return base in COMMON_PASSWORDS and len(base) >= 4


def has_keyboard_sequence(password: str) -> bool:
    lowered = password.lower()
    return any(sequence in lowered for sequence in KEYBOARD_SEQUENCES)


def has_long_repeat(password: str) -> bool:
    return bool(re.search(r"(.)\1{2,}", password))


def analyse_password(password: str) -> dict:
    """Return a score, label, entropy estimate, and friendly advice."""
    length = len(password)
    classes = sum(
        [
            any(char.islower() for char in password),
            any(char.isupper() for char in password),
            any(char.isdigit() for char in password),
            any(char in string.punctuation for char in password),
        ]
    )

    score = 0
    if length >= 8:
        score += 15
    if length >= 12:
        score += 20
    if length >= 16:
        score += 15
    score += classes * 8
    if length and len(set(password)) / length >= 0.65:
        score += 8

    advice: list[str] = []
    is_common = has_common_word_shape(password)
    sequence = has_keyboard_sequence(password)
    repeat = has_long_repeat(password)

    if is_common:
        score -= 45
        advice.append("This looks like a famous or easy-to-guess password. Pick something unique.")
    if sequence:
        score -= 15
        advice.append("Avoid keyboard runs such as 1234, qwerty, or abcd.")
    if repeat:
        score -= 10
        advice.append("Avoid repeating the same character three or more times.")
    if length < 12:
        advice.append("Length is your best friend: aim for 12+ characters, or a 4-word passphrase.")
    if classes < 3 and length < 16:
        advice.append("Mix uppercase, lowercase, numbers, and symbols.")
    if re.search(r"(19|20)\d{2}", password):
        score -= 5
        advice.append("Years are easy to guess. Avoid birthdays and graduation years.")

    score = max(0, min(100, score))
    entropy = estimate_entropy_bits(password)

    if score < 25:
        label = "Very weak"
    elif score < 45:
        label = "Weak"
    elif score < 65:
        label = "Fair"
    elif score < 85:
        label = "Strong"
    else:
        label = "Very strong"

    if not advice:
        advice.append("Nice work. Keep it unique and store it in a password manager.")

    return {
        "length": length,
        "classes": classes,
        "score": score,
        "label": label,
        "entropy": entropy,
        "advice": advice,
        "common": is_common,
    }


def print_report(password: str, show_password: bool = False) -> None:
    report = analyse_password(password)
    bar_length = 24
    filled = round((report["score"] / 100) * bar_length)
    bar = "#" * filled + "." * (bar_length - filled)

    print("\n" + "-" * 62)
    if show_password:
        print(f"Sample password : {password}")
    print(f"Length          : {report['length']} characters")
    print(f"Character types : {report['classes']} of 4")
    print(f"Score           : {report['score']}/100  [{bar}]")
    print(f"Rating          : {report['label']}")
    print(f"Rough entropy   : {report['entropy']:.1f} bits")
    print("\nAdvice:")
    for tip in report["advice"]:
        print(f"  - {tip}")
    print("-" * 62)


def run_demo() -> None:
    samples = [
        ("password123", "A classic terrible password"),
        ("Summer2026!", "Predictable: a word, a year, and a symbol"),
        ("Blue-Coffee-Rocket-42!", "A long passphrase-style password"),
        ("correct horse battery staple", "A famous four-word passphrase"),
        ("Tr0ub4dor&3", "Short but complex-looking"),
    ]

    print("=" * 62)
    print("  PASSWORD POWER METER - DEMO")
    print("=" * 62)
    print("These are sample passwords, not real ones. Watch how length and")
    print("predictability matter more than a confusing pile of symbols.")

    for sample, note in samples:
        print(f"\n\nSample: {note}")
        print_report(sample, show_password=True)

    print("\nRemember: a password manager lets you use a different long random")
    print("password for every account, so one leak does not unlock everything.")


def interactive_mode() -> None:
    print("=" * 62)
    print("  PASSWORD POWER METER")
    print("=" * 62)
    print("Type a MADE-UP password. It stays on this computer and is never saved.")
    print("Press Ctrl+C to quit.\n")

    try:
        password = getpass.getpass("Fake password: ")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")
        return

    if not password:
        print("No password entered.")
        return

    print_report(password)
    print("\nNext step: turn your best idea into a passphrase of 4+ random words,")
    print("then store it in a password manager.")


def main() -> int:
    if "--demo" in sys.argv[1:]:
        run_demo()
        return 0

    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("Usage:")
        print("  py -3 password_strength.py          # type a made-up password")
        print("  py -3 password_strength.py --demo   # see sample passwords")
        print("\nThere is no password command-line argument on purpose, so a real")
        print("password does not end up in your shell history.")
        return 0

    if len(sys.argv) > 1:
        print("This program has no password argument on purpose, so passwords do")
        print("not end up in your command history. Use --demo or run it directly.")
        return 1

    interactive_mode()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nGoodbye.")
        sys.exit(130)
