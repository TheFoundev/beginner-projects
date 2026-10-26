# Instructions for Project 9: Share Your Mad Libs Container on Docker Hub

## Overview

A Python Mad Libs story generator with 3 story templates, interactive mode, and unit tests — containerized and ready for Docker Hub.

## Files

| File | Description |
|------|-------------|
| `app.py` | Main app with MadLibsGenerator class, CLI & interactive mode |
| `Dockerfile` | Container definition with healthcheck |
| `tests/test_app.py` | 10 unit tests |
| `.dockerignore` | Prevents bloating the image |
| `INSTRUCTIONS.md` | Deployment guide |

## Build & Run Locally

```bash
# Build
docker build -t madlibs-app .

# Random story
docker run --rm madlibs-app --story adventure

# List templates
docker run --rm madlibs-app --list

# Interactive mode
docker run -it --rm madlibs-app --interactive
```

## Share on Docker Hub

```bash
# 1. Sign up at https://hub.docker.com
# 2. Login
docker login

# 3. Tag your image
docker tag madlibs-app yourusername/madlibs-app:latest

# 4. Push to Docker Hub
docker push yourusername/madlibs-app:latest

# 5. Anyone can now run it:
docker run -it --rm yourusername/madlibs-app:latest --interactive
```
