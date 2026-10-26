"""
Simple To-Do List API

A minimal Flask app that stores todo items in memory.
Used in Project 13 to demonstrate Docker + CI/CD integration.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage (resets when the container restarts)
todos = []


@app.route("/")
def home():
    return jsonify({
        "message": "To-Do List API",
        "endpoints": {
            "GET /api/todos": "Get all todos",
            "POST /api/todos": "Add a new todo (JSON: {task: '...'})",
        }
    })


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if data and "task" in data:
        todo = {"id": len(todos) + 1, "task": data["task"], "done": False}
        todos.append(todo)
        return jsonify(todo), 201
    return jsonify({"error": "No task provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
