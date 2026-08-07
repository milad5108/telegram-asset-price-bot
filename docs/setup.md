# Setup Guide

This guide explains how to set up the project for local development.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.12 or newer
- Git
- Docker (optional)
- Docker Compose (optional)

## Clone the Repository

```bash
git clone https://github.com/milad5108/telegram-asset-price-bot.git
cd telegram-asset-price-bot
```

## Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Copy the example configuration file.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Then edit the `.env` file and provide your own credentials.

## Run the Bot

```bash
python -m bot.main
```

## Run Tests

```bash
pytest
```

## Run Linting

```bash
ruff check .
```

## Project Structure

```text
bot/
tests/
assets/
docs/
.github/
```

The project is now ready for local development.