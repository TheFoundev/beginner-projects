#!/usr/bin/env python3
"""
Project 17 - Metadata Mystery: What Your Photos Reveal
======================================================

Inspect EXIF metadata in an image, then create a cleaned copy with the metadata
removed. Photos can carry camera details, timestamps, editing software, and
sometimes GPS coordinates.

Install:
    py -3 -m pip install -r requirements.txt

Run:
    py -3 photo_metadata.py demo
    py -3 photo_metadata.py inspect samples/demo_photo.jpg
    py -3 photo_metadata.py strip samples/demo_photo.jpg cleaned.jpg
    py -3 photo_metadata.py inspect cleaned.jpg

Safety:
    Use your own photos. Metadata can contain private information; do not post
    someone else's photo metadata without permission.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import ExifTags, Image, ImageDraw, ImageOps
except ImportError:
    print("This project needs Pillow.")
    print("Install it with: py -3 -m pip install -r requirements.txt")
    raise SystemExit(1)


SENSITIVE_TAGS = {
    "Make", "Model", "DateTime", "DateTimeOriginal", "DateTimeDigitized",
    "Software", "Artist", "Copyright", "GPSInfo", "SerialNumber",
    "LensModel", "OwnerName", "ImageDescription",
}


def safe_value(value: Any, limit: int = 160) -> str:
    try:
        text = str(value)
    except Exception:
        text = repr(value)
    text = " ".join(text.split())
    return text[:limit] + ("..." if len(text) > limit else "")


def gps_to_decimal(gps: dict[str, Any]) -> tuple[float, float] | None:
    """Convert EXIF GPS degrees/minutes/seconds into decimal degrees."""
    try:
        def to_degrees(values: Any) -> float:
            degrees, minutes, seconds = values
            return float(degrees) + float(minutes) / 60 + float(seconds) / 3600

        latitude = to_degrees(gps[2])
        if str(gps.get(1, "N")).upper().startswith("S"):
            latitude = -latitude
        longitude = to_degrees(gps[4])
        if str(gps.get(3, "E")).upper().startswith("W"):
            longitude = -longitude
        return latitude, longitude
    except Exception:
        return None


def inspect_image(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        exif = image.getexif()
        tags: list[dict[str, str]] = []
        gps_text = None

        for tag_id, value in exif.items():
            name = ExifTags.TAGS.get(tag_id, f"Tag{tag_id}")
            if name == "GPSInfo" and isinstance(value, dict):
                gps_named = {
                    ExifTags.GPSTAGS.get(key, f"Tag{key}"): safe_value(item)
                    for key, item in value.items()
                }
                decimal = gps_to_decimal(value)
                if decimal:
                    gps_text = f"{decimal[0]:.6f}, {decimal[1]:.6f}"
                tags.append(
                    {
                        "tag": name,
                        "value": json.dumps(gps_named),
                        "sensitive": "yes",
                    }
                )
            else:
                tags.append(
                    {
                        "tag": name,
                        "value": safe_value(value),
                        "sensitive": "yes" if name in SENSITIVE_TAGS else "no",
                    }
                )

        return {
            "file": str(path),
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height,
            "size_bytes": path.stat().st_size,
            "tag_count": len(tags),
            "tags": tags,
            "gps_decimal": gps_text,
        }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 76)
    print("  METADATA MYSTERY")
    print("=" * 76)
    print(f"File       : {report['file']}")
    print(f"Format     : {report['format']} ({report['mode']})")
    print(f"Dimensions : {report['width']} x {report['height']}")
    print(f"Size       : {report['size_bytes']:,} bytes")
    print(f"EXIF tags  : {report['tag_count']}")

    if report["gps_decimal"]:
        print(f"\n[!] GPS coordinates: {report['gps_decimal']}")
        print("    This can reveal where the photo was taken.")
    elif any(tag["tag"] == "GPSInfo" for tag in report["tags"]):
        print("\n[!] The image contains a GPS block but it could not be decoded.")
    else:
        print("\n[+] No GPS block found.")

    if not report["tags"]:
        print("\nNo EXIF tags found. The image may already be cleaned, or it may")
        print("never have had metadata.")
        return

    print("\nAll metadata tags:")
    for tag in report["tags"]:
        marker = "[!]" if tag["sensitive"] == "yes" else "   "
        print(f"  {marker} {tag['tag']:<22} {tag['value']}")

    print("\nMost revealing tags to check:")
    present = {tag["tag"] for tag in report["tags"]}
    for name in (
        "Make", "Model", "DateTimeOriginal", "DateTime", "Software",
        "Artist", "GPSInfo",
    ):
        if name in present:
            print(f"  - {name}")

    print("\nWhy this matters:")
    print("  - A photo can reveal a device model, a timestamp, and a location.")
    print("  - Social platforms often strip metadata, but email and file sharing")
    print("    may preserve it.")
    print("  - Strip metadata before sharing a sensitive photo publicly.")


def strip_metadata(source: Path, destination: Path, force: bool = False) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"Image not found: {source}")
    if destination.exists() and not force:
        raise FileExistsError(f"Output exists: {destination} (use --force to overwrite)")
    if source.resolve() == destination.resolve():
        raise ValueError("Choose a different output path so the original is preserved.")

    before = inspect_image(source)["tag_count"]

    with Image.open(source) as original:
        # Preserve the visual orientation, then build a fresh image so old
        # metadata and text chunks are not carried into the saved copy.
        oriented = ImageOps.exif_transpose(original)
        clean = Image.new(oriented.mode, oriented.size)
        clean.paste(oriented)

        suffix = destination.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            if clean.mode not in {"RGB", "L"}:
                clean = clean.convert("RGB")
            clean.save(destination, format="JPEG", quality=95, optimize=True)
        elif suffix == ".png":
            clean.save(destination, format="PNG", optimize=True)
        elif suffix == ".webp":
            clean.save(destination, format="WEBP", quality=95)
        else:
            raise ValueError("Use an output ending in .jpg, .jpeg, .png, or .webp.")

    after = inspect_image(destination)["tag_count"]
    print(f"[+] Original : {source}")
    print(f"[+] Clean copy: {destination}")
    print(f"[+] EXIF tags before: {before}")
    print(f"[+] EXIF tags after : {after}")
    print("[+] The cleaned image was re-encoded, so it may look slightly different")
    print("    at the pixel level. That is expected.")


def create_demo_image(path: Path) -> None:
    """Generate a colorful sample photo with fake EXIF data."""
    width, height = 900, 600
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    top = (15, 118, 110)
    bottom = (217, 249, 157)
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)

    draw.ellipse((80, 80, 300, 300), fill=(255, 245, 210), outline=(20, 40, 60), width=3)
    draw.rectangle((420, 140, 780, 430), fill=(20, 40, 60), outline=(255, 255, 255), width=4)
    draw.text((450, 180), "CYBER LAB", fill=(217, 249, 157))
    draw.text((450, 215), "sample photo", fill=(255, 255, 255))

    exif = Image.Exif()
    exif[271] = "Foundev"                     # Make
    exif[272] = "DemoPhone 1"                 # Model
    exif[305] = "DemoCam 1.0"                 # Software
    exif[306] = "2026:10:26 09:00:00"          # DateTime
    exif[315] = "Demo Student"                 # Artist
    exif[33432] = "Fictional sample image"     # Copyright

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=94, exif=exif)


def run_demo() -> None:
    base = Path(__file__).resolve().parent
    sample = base / "samples" / "demo_photo.jpg"
    cleaned = base / "samples" / "demo_photo_clean.jpg"

    print("=" * 76)
    print("  METADATA MYSTERY - DEMO")
    print("=" * 76)
    print("Creating a fictional sample photo with fake camera metadata...")
    create_demo_image(sample)

    print("\n1. Inspecting the original")
    print_report(inspect_image(sample))

    print("\n\n2. Creating a cleaned copy")
    strip_metadata(sample, cleaned, force=True)

    print("\n3. Inspecting the cleaned copy")
    print_report(inspect_image(cleaned))

    print("\n" + "=" * 76)
    print("  WHAT CHANGED?")
    print("=" * 76)
    print("The cleaned copy has no EXIF camera tags. The image itself is still")
    print("there, but the story about the device, time, and software is gone.")
    print("\nTry a real photo from your phone (one you own) to see GPS and more.")
    print("Never upload someone else's photo metadata without permission.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and remove EXIF metadata from images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 photo_metadata.py demo\n"
            "  py -3 photo_metadata.py inspect samples/demo_photo.jpg\n"
            "  py -3 photo_metadata.py strip samples/demo_photo.jpg cleaned.jpg\n"
            "  py -3 photo_metadata.py inspect cleaned.jpg --json\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    inspect_parser = subparsers.add_parser("inspect", help="Show image metadata.")
    inspect_parser.add_argument("image", type=Path)
    inspect_parser.add_argument("--json", action="store_true", help="Print JSON.")

    strip_parser = subparsers.add_parser("strip", help="Create a copy without metadata.")
    strip_parser.add_argument("source", type=Path)
    strip_parser.add_argument("destination", type=Path)
    strip_parser.add_argument("--force", action="store_true", help="Overwrite the output if it exists.")

    subparsers.add_parser("demo", help="Create a sample photo, inspect it, and clean it.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        run_demo()
        return 0

    if args.command == "inspect":
        if not args.image.is_file():
            print(f"ERROR: image not found: {args.image}")
            return 1
        report = inspect_image(args.image)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)
        return 0

    if args.command == "strip":
        try:
            strip_metadata(args.source, args.destination, force=args.force)
        except (FileNotFoundError, FileExistsError, ValueError, OSError) as error:
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
