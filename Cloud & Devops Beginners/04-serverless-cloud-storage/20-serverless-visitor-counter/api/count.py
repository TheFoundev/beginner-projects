"""
Serverless Visitor Counter API

This function increments and returns a visitor count
using Upstash Redis as a serverless database.

Deploy on Vercel: https://vercel.com
Upstash Redis: https://upstash.com

Learn more: https://vercel.com/docs/concepts/functions/serverless-functions
"""
import os
import redis
from http.server import BaseHTTPRequestHandler


# Read environment variables set in Vercel
REDIS_URL = os.environ.get("REDIS_URL", "")
REDIS_TOKEN = os.environ.get("REDIS_TOKEN", "")


def get_redis():
    """Initialize connection to Upstash Redis."""
    if not REDIS_URL or not REDIS_TOKEN:
        return None
    return redis.Redis(
        host=REDIS_URL.replace("redis://", "").replace("rediss://", ""),
        port=6379,
        password=REDIS_TOKEN,
        ssl=True,
        decode_responses=True
    )


class VisitorCounter(BaseHTTPRequestHandler):
    """HTTP handler for the visitor counter API."""

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data.encode())

    def do_GET(self):
        r = get_redis()
        if r is None:
            self.send_json({"count": -1, "error": "Redis not configured"}, 500)
            return

        try:
            r.incr("visitor_count")
            count = r.get("visitor_count")
            self.send_json({"count": int(count)})
        except Exception as e:
            self.send_json({"count": -1, "error": str(e)}, 500)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()


# For standalone testing (optional)
if __name__ == "__main__":
    print("Redis URL configured:", bool(REDIS_URL))
    print("Redis Token configured:", bool(REDIS_TOKEN))
    print("Set REDIS_URL and REDIS_TOKEN env vars from your Upstash dashboard.")
