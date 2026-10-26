# Instructions for Project 6: Package a Multilingual "Hello World" in Docker

## Overview

An enhanced Python greeting application that supports 8 languages, environment variable configuration, argument parsing, and unit tests — all containerized in Docker.

## Files

| File | Description |
|------|-------------|
| `app.py` | Multilingual greeting app with CLI args and env vars |
| `Dockerfile` | Multi-stage config with labels, health checks, non-root user |
| `tests/test_app.py` | 11 unit tests for the GreetingGenerator class |
| `.dockerignore` | Prevents unnecessary files from bloating the image |

## Step-by-Step

### 1. Build the Image
```bash
docker build -t hello-docker .
```

### 2. Run with Default Settings
```bash
docker run --rm hello-docker
```

### 3. Run with Arguments
```bash
docker run --rm hello-docker --name Alice --lang spanish
```

### 4. Run with Environment Variables
```bash
docker run --rm -e GREETING_NAME="From Env" -e GREETING_LANG=japanese hello-docker
```

### 5. List Available Languages
```bash
docker run --rm hello-docker --list
```

### 6. Run Tests Inside the Container
```bash
# Build a test image (or use the running container)
docker run --rm hello-docker python -m pytest tests/ -v
```

### 7. Push to Docker Hub
```bash
docker tag hello-docker yourusername/hello-docker:latest
docker push yourusername/hello-docker:latest
```

---
*You've just containerized a fully-featured application with tests, environment variables, and health checks — all the essentials Docker offers.*