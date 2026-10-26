"""
To-Do API Server

A simple Flask API for managing to-do items, backed by Redis for counting.
Designed to run alongside an Nginx frontend in a Docker Compose stack.
"""
import os
import time
import redis
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
APP_PORT = int(os.environ.get("APP_PORT", 5000))

# In-memory storage (Redis persists across restarts when using volumes)
todos = []


def get_redis():
    """Get a Redis connection, or return None if unavailable."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2)
        r.ping()
        return r
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return None


@app.route("/health")
def health():
    """Health check endpoint."""
    r = get_redis()
    redis_status = "connected" if r else "disconnected"
    return jsonify({
        "status": "healthy",
        "redis": redis_status,
        "todos_count": len(todos)
    })


@app.route("/")
def index():
    """Root endpoint with API info."""
    return jsonify({
        "app": "To-Do API",
        "version": "2.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "GET /api/todos": "Get all todos",
            "GET /api/stats": "Get visit statistics",
            "POST /api/todos": "Add a todo (JSON: {task: '...'})"
        }
    })


@app.route("/api/todos", methods=["GET", "POST"])
def manage_todos():
    if request.method == "POST":
        data = request.get_json() or {}
        task = data.get("task", "").strip()
        if not task:
            return jsonify({"error": "Task is required"}), 400

        todo = {
            "id": len(todos) + 1,
            "task": task,
            "completed": False,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        todos.append(todo)
        return jsonify(todo), 201

    return jsonify(todos)


@app.route("/api/stats", methods=["GET"])
def stats():
    """Return visit statistics from Redis."""
    r = get_redis()
    if not r:
        return jsonify({"visits": 0, "online": False, "todos": len(todos)})

    visits = int(r.get("visitor_count") or 0)
    r.incr("visitor_count")

    return jsonify({
        "visits": int(r.get("visitor_count") or 0),
        "online": True,
        "todos": len(todos),
        "redis_key": "visitor_count"
    })


if __name__ == "__main__":
    print(f"Starting To-Do API on port {APP_PORT}")
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
