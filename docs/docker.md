# Docker Guide

This document explains how to run the project using Docker.

## Requirements

Before using Docker, make sure the following tools are installed:

- Docker Desktop
- Docker Compose

Verify the installation:

```bash
docker --version
docker compose version
```

## Build the Docker Image

```bash
docker build -t telegram-asset-price-bot .
```

## Run the Container

```bash
docker run --env-file .env telegram-asset-price-bot
```

## Using Docker Compose

Start the application:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

Stop the application:

```bash
docker compose down
```

## Rebuild After Code Changes

```bash
docker compose up --build
```

## View Logs

```bash
docker compose logs
```

Follow logs in real time:

```bash
docker compose logs -f
```

## Common Commands

Restart the application:

```bash
docker compose restart
```

Stop all containers:

```bash
docker compose down
```

Remove unused Docker resources:

```bash
docker system prune
```

## Environment Variables

Docker reads configuration values from the local `.env` file.

Never include the real `.env` file inside the repository or Docker image.

## Notes

- Keep Docker Desktop running before starting the project.
- Make sure the `.env` file exists before launching the container.
- Rebuild the image whenever dependencies change.