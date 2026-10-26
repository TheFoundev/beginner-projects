#!/usr/bin/env python3
"""
Serve the training websites from Project 10 on localhost.

Run:
    py -3 serve_site.py
    py -3 serve_site.py --site fixed_site --port 8080

Then open http://127.0.0.1:8000 and use View Source / DevTools.

Safety:
    The server binds to 127.0.0.1 only. The vulnerable site is fictional and
    contains fake "secrets" for teaching information disclosure.
"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve a local training site.")
    parser.add_argument(
        "--site",
        choices=["vulnerable_site", "fixed_site"],
        default="vulnerable_site",
        help="Which training site to serve.",
    )
    parser.add_argument("--port", type=int, default=8000, help="Local port (default: 8000).")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    site = root / args.site
    if not site.is_dir():
        print(f"ERROR: missing site folder: {site}")
        return 1

    handler = partial(SimpleHTTPRequestHandler, directory=str(site))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)

    print("=" * 70)
    print(f"  SERVING: {args.site}")
    print("=" * 70)
    print(f"Open: http://127.0.0.1:{args.port}")
    print("Use View Source (Ctrl+U) and DevTools to hunt for clues.")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
