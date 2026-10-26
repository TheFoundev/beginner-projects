# Instructions for Project 8: Interactive Quote Generator in Docker

## Overview

A Python quote generator with JSON-based quotes, category filtering, and interactive mode — all running in Docker.

## Files

| File | Description |
|------|-------------|
| `app.py` | Main app with QuoteGenerator class, CLI, and interactive mode |
| `quotes.json` | 15 quotes across 6 categories |
| `Dockerfile` | Multi-label container definition |
| `tests/test_app.py` | 10 unit tests |
| `INSTRUCTIONS.md` | Deployment guide |

## Commands

```bash
# Build
docker build -t quote-generator .

# Random quote
docker run --rm quote-generator

# Quote from a specific category
docker run --rm quote-generator --category wisdom

# List all categories
docker run --rm quote-generator --list-categories

# Interactive mode (press Enter for new quote)
docker run --it --rm quote-generator --interactive

# Use your own quotes file
docker run --rm -v ./my-quotes.json:/app/quotes.json quote-generator
```

## Adding Your Own Quotes

Edit `quotes.json` or create your own file:
```json
[
  {"text": "Your quote here.", "author": "Author Name", "category": "motivation"}
]
```

Mount it at runtime: `docker run --rm -v ./my-quotes.json:/app/quotes.json quote-generator`
