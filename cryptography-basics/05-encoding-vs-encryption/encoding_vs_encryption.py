#!/usr/bin/env python3
"""
Project 05 - The Great Disguise: Encoding vs. Encryption
========================================================

A hands-on comparison of three things beginners often confuse:

    Base64  - encoding: changes the format, hides nothing
    ROT13   - a weak cipher: looks scrambled, trivially reversible
    AES-GCM - encryption: needs the right key, detects tampering

Install:
    py -3 -m pip install cryptography

Run:
    py -3 encoding_vs_encryption.py
    py -3 encoding_vs_encryption.py --text "my secret message"

Safety:
    Use fake messages while learning. Base64 is NOT encryption, and neither is
    ROT13. Never protect real secrets with either one.
"""

from __future__ import annotations

import argparse
import base64
import codecs
import getpass
import os
import sys

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("This project needs the 'cryptography' package.")
    print("Install it with: py -3 -m pip install cryptography")
    raise SystemExit(1)


SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def aes_encrypt(message: str, password: str) -> bytes:
    """Return salt + nonce + AES-GCM ciphertext as one byte string."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, message.encode("utf-8"), None)
    return salt + nonce + ciphertext


def aes_decrypt(blob: bytes, password: str) -> str:
    salt = blob[:SALT_SIZE]
    nonce = blob[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = blob[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(password, salt)
    return AESGCM(key).decrypt(nonce, ciphertext, None).decode("utf-8")


def show_comparison() -> None:
    print("\n" + "=" * 72)
    print("  QUICK COMPARISON")
    print("=" * 72)
    print(f"{'Method':<12} {'Hides content?':<18} {'Needs a key?':<14} {'Anyone can reverse?'}")
    print("-" * 72)
    print(f"{'Base64':<12} {'No':<18} {'No':<14} {'Yes - instantly'}")
    print(f"{'ROT13':<12} {'Sort of':<18} {'No':<14} {'Yes - instantly'}")
    print(f"{'AES-GCM':<12} {'Yes':<18} {'Yes':<14} {'No - not without the key'}")
    print("-" * 72)
    print("Rule of thumb: encoding is for compatibility, encryption is for secrecy.")


def run_demo(message: str, password: str) -> None:
    print("=" * 72)
    print("  THE GREAT DISGUISE")
    print("=" * 72)
    print(f"\nOriginal message:\n  {message}")

    print("\n" + "-" * 72)
    print("1. BASE64 (encoding)")
    print("-" * 72)
    encoded = base64.b64encode(message.encode("utf-8")).decode("ascii")
    decoded = base64.b64decode(encoded).decode("utf-8")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    print("Notice: no key was needed. Base64 is just a different alphabet.")
    print("It is useful for sending bytes through text-only systems, not for secrets.")

    print("\n" + "-" * 72)
    print("2. ROT13 (a weak substitution cipher)")
    print("-" * 72)
    rotated = codecs.encode(message, "rot_13")
    restored = codecs.encode(rotated, "rot_13")
    print(f"Rotated: {rotated}")
    print(f"Restored: {restored}")
    print("Notice: anyone can reverse it by applying ROT13 again. It is a puzzle,")
    print("not protection. Real ciphers need a secret key and a strong algorithm.")

    print("\n" + "-" * 72)
    print("3. AES-256-GCM (real encryption)")
    print("-" * 72)
    blob = aes_encrypt(message, password)
    packed = base64.b64encode(blob).decode("ascii")
    print(f"Encrypted (salt + nonce + ciphertext):\n  {packed}")
    print("\nThe random salt means the same message and password produce a different")
    print("result every time. Try running this demo twice and compare.")

    print("\nTrying the WRONG password:")
    try:
        aes_decrypt(blob, password + "-wrong")
        print("  [!] Unexpected: the wrong password worked.")
    except InvalidTag:
        print("  [+] Rejected. AES-GCM also detected that the key was wrong.")

    print("\nTrying the CORRECT password:")
    print(f"  {aes_decrypt(blob, password)}")

    print("\nTrying a TAMPERED ciphertext:")
    tampered = bytearray(blob)
    tampered[-1] ^= 0x01
    try:
        aes_decrypt(bytes(tampered), password)
        print("  [!] Unexpected: tampering was not detected.")
    except InvalidTag:
        print("  [+] Rejected. Authentication caught the modification.")

    show_comparison()
    print("\nKey takeaway: 'it looks like gibberish' is not a security property.")
    print("Ask instead: what is the key, who manages it, and can tampering be detected?")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare Base64, ROT13, and real AES encryption.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 encoding_vs_encryption.py\n"
            '  py -3 encoding_vs_encryption.py --text "meet me at noon"\n'
        ),
    )
    parser.add_argument("--text", help="Message to experiment with (default: a demo message).")
    args = parser.parse_args()

    if args.text:
        print("Enter a throwaway passphrase for the AES demonstration.")
        password = getpass.getpass("Passphrase: ")
        if not password:
            print("A passphrase is required for the AES section.")
            return 1
    else:
        password = "demo-passphrase-123"

    message = args.text or "Meet me at the treehouse at noon. Bring snacks."
    run_demo(message, password)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
