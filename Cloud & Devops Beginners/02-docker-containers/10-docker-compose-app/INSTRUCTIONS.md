# Project 10: Docker Compose — To-Do App with Redis Counter

## Overview

A 3-container application: Flask API + Nginx frontend + Redis database, all orchestrated with Docker Compose.

## Architecture

```
┌─────────┐    API    ┌──────────┐
│  Nginx  │ ◄──────── │  Flask   │
│ (port)  │           │ API      │
│ :8080   │     :5000 │ :5000    │
└────┬────┘           └────┬─────┘
     │                     │
     │    Frontend + API  │  Redis
     └────────────────────┼─────────
                          │  :6379
                     ┌────┴────┐
                     │  Redis  │
                     │ (shared │
                     │  data)  │
                     └─────────┘
```

## Quick Start

```bash
# Build and start all services
docker compose up --build

# View the site
# - Frontend: http://localhost:8080
# - API directly: http://localhost:5000
# - Health check: http://localhost:5000/health

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Stop and remove all volumes (clears Redis data)
docker compose down -v
```

## Features

- **Nginx reverse proxy** — Routes `/api/*` to Flask, serves static files
- **Flask API** — To-Do CRUD operations + Redis-backed visitor counter
- **Redis with health checks** — Persistent storage, starts before Flask
- **Auto-restart policies** — All containers restart on failure
- **Health checks** — Each service monitors its own health

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `redis` | Redis hostname (container name) |
| `REDIS_PORT` | `6379` | Redis port |
| `APP_PORT` | `5000` | Flask listen port |