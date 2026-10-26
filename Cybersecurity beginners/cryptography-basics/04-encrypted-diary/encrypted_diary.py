#!/usr/bin/env python3
"""
Project 04 - The Unbreakable Diary: Encrypt a Folder
====================================================

Encrypt a folder into a single password-protected .diary file, then decrypt it
back into a folder. This uses AES-256-GCM (authenticated encryption) and
PBKDF2 key stretching from the `cryptography` package.

Install the one dependency first:
    py -3 -m pip install cryptography

Run:
    py -3 encrypted_diary.py encrypt my_folder -o my_secrets.diary
    py -3 encrypted_diary.py decrypt my_secrets.diary -o restored_folder
    py -3 encrypted_diary.py demo

Safety:
    Use fake notes while learning. There is NO password recovery. If you forget
    the passphrase, the data is gone. That is a feature, not a bug.
"""

from __future__ import annotations

import argparse
import getpass
import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("This project needs the 'cryptography' package.")
    print("Install it with: py -3 -m pip install cryptography")
    raise SystemExit(1)


MAGIC = b"DIARY1"          # Identifies our file format.
SALT_SIZE = 16             # Random salt makes the same password produce a different key.
NONCE_SIZE = 12            # Unique nonce for AES-GCM; never reuse with the same key.
KEY_SIZE = 32              # 32 bytes = 256-bit AES key.
KDF_ITERATIONS = 600_000   # Slows down password guessing.


def derive_key(password: str, salt: bytes) -> bytes:
    """Turn a human passphrase into a 256-bit encryption key."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def zip_folder(folder: Path) -> bytes:
    """Compress a folder into an in-memory ZIP archive."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(folder))
    return buffer.getvalue()


def safe_extract(archive_bytes: bytes, destination: Path) -> None:
    """
    Extract a ZIP without allowing entries to escape the destination folder.

    A malicious ZIP can contain names such as ../../important-file. This check
    stops that "zip slip" trick before any file is written.
    """
    destination = destination.resolve()
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if target != destination and destination not in target.parents:
                raise ValueError(f"Unsafe path inside archive: {member.filename}")
        archive.extractall(destination)


def encrypt_folder(folder: Path, output: Path, password: str, force: bool = False) -> None:
    if not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")
    if output.exists() and not force:
        raise FileExistsError(f"Output already exists: {output} (use --force to overwrite)")

    plaintext = zip_folder(folder)
    if not plaintext:
        raise ValueError("The folder is empty; nothing to encrypt.")

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    ciphertext = AESGCM(key).encrypt(nonce, plaintext, MAGIC)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(MAGIC + salt + nonce + ciphertext)

    print(f"[+] Encrypted folder : {folder}")
    print(f"[+] Output file      : {output}")
    print(f"[+] Files included   : {sum(1 for p in folder.rglob('*') if p.is_file())}")
    print(f"[+] Plaintext size   : {len(plaintext):,} bytes")
    print(f"[+] Encrypted size   : {output.stat().st_size:,} bytes")
    print("[!] Remember the passphrase. There is no recovery.")


def decrypt_archive(archive_path: Path, destination: Path, password: str, force: bool = False) -> None:
    if not archive_path.is_file():
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    if destination.exists() and any(destination.iterdir()) and not force:
        raise FileExistsError(
            f"Destination is not empty: {destination} (use --force to extract anyway)"
        )

    raw = archive_path.read_bytes()
    minimum_size = len(MAGIC) + SALT_SIZE + NONCE_SIZE + 16  # 16-byte GCM tag
    if len(raw) < minimum_size or not raw.startswith(MAGIC):
        raise ValueError("This does not look like a .diary file created by this tool.")

    offset = len(MAGIC)
    salt = raw[offset:offset + SALT_SIZE]
    offset += SALT_SIZE
    nonce = raw[offset:offset + NONCE_SIZE]
    offset += NONCE_SIZE
    ciphertext = raw[offset:]

    key = derive_key(password, salt)
    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, MAGIC)
    except InvalidTag as exc:
        raise ValueError("Wrong passphrase, or the file was modified.") from exc

    destination.mkdir(parents=True, exist_ok=True)
    safe_extract(plaintext, destination)

    print(f"[+] Decrypted archive : {archive_path}")
    print(f"[+] Restored to       : {destination}")
    print(f"[+] Files restored    : {sum(1 for p in destination.rglob('*') if p.is_file())}")


def ask_password(confirm: bool) -> str:
    password = getpass.getpass("Passphrase: ")
    if len(password) < 12:
        print("[!] Use at least 12 characters for a real passphrase.")
    if confirm:
        again = getpass.getpass("Confirm passphrase: ")
        if password != again:
            raise ValueError("Passphrases did not match.")
    if not password:
        raise ValueError("Passphrase cannot be empty.")
    return password


def run_demo() -> None:
    """Create a fake diary, encrypt it, decrypt it, and compare the contents."""
    print("=" * 68)
    print("  ENCRYPTED DIARY - DEMO")
    print("=" * 68)

    with tempfile.TemporaryDirectory(prefix="diary-demo-") as temp:
        base = Path(temp)
        source = base / "my_diary"
        source.mkdir()
        (source / "monday.txt").write_text(
            "Dear diary, today I learned that encryption is not the same as encoding.\n",
            encoding="utf-8",
        )
        (source / "plans.txt").write_text(
            "Build a password manager. Read one cybersecurity article.\n",
            encoding="utf-8",
        )
        (source / "nested").mkdir()
        (source / "nested" / "secret.txt").write_text(
            "This nested file should survive the round trip.\n",
            encoding="utf-8",
        )

        archive = base / "my_diary.diary"
        restored = base / "restored"
        passphrase = "correct-horse-battery-staple-42"

        encrypt_folder(source, archive, passphrase)

        print("\n[?] Trying a wrong passphrase first...")
        try:
            decrypt_archive(archive, base / "wrong", "this-is-not-the-passphrase", force=True)
            print("[!] Unexpected: the wrong passphrase worked.")
        except ValueError as error:
            print(f"[+] Safely rejected: {error}")

        print("\n[?] Now trying the correct passphrase...")
        decrypt_archive(archive, restored, passphrase, force=True)

        original_files = {
            p.relative_to(source): p.read_text(encoding="utf-8")
            for p in source.rglob("*") if p.is_file()
        }
        restored_files = {
            p.relative_to(restored): p.read_text(encoding="utf-8")
            for p in restored.rglob("*") if p.is_file()
        }

        print("\n[+] Round-trip comparison:")
        print(f"    Files match: {'YES' if original_files == restored_files else 'NO'}")
        for name in sorted(original_files):
            print(f"    - {name}")

        print("\nWhat did we learn?")
        print("  - The archive is unreadable without the passphrase.")
        print("  - A wrong passphrase fails cleanly.")
        print("  - Encryption protects confidentiality; authentication detects tampering.")
        print("  - Losing the passphrase means losing the data forever.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a folder with AES-256-GCM.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 encrypted_diary.py encrypt my_folder -o secrets.diary\n"
            "  py -3 encrypted_diary.py decrypt secrets.diary -o restored\n"
            "  py -3 encrypted_diary.py demo\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a folder.")
    encrypt_parser.add_argument("folder", type=Path)
    encrypt_parser.add_argument("-o", "--output", type=Path, required=True)
    encrypt_parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a .diary archive.")
    decrypt_parser.add_argument("archive", type=Path)
    decrypt_parser.add_argument("-o", "--output", type=Path, required=True)
    decrypt_parser.add_argument("--force", action="store_true", help="Extract into a non-empty folder.")

    subparsers.add_parser("demo", help="Run a complete round-trip demonstration.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        run_demo()
        return 0

    if args.command == "encrypt":
        try:
            password = ask_password(confirm=True)
            encrypt_folder(args.folder, args.output, password, force=args.force)
        except (FileNotFoundError, FileExistsError, ValueError) as error:
            print(f"ERROR: {error}")
            return 1
        return 0

    if args.command == "decrypt":
        try:
            password = ask_password(confirm=False)
            decrypt_archive(args.archive, args.output, password, force=args.force)
        except (FileNotFoundError, FileExistsError, ValueError) as error:
            print(f"ERROR: {error}")
            return 1
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
