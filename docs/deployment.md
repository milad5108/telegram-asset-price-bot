# Deployment Guide

This document explains how to deploy the Telegram Asset Price Bot.

## Overview

The application is designed to run continuously and publish scheduled price updates to a Telegram channel.

Supported deployment options include:

- Local machine
- Virtual Private Server (VPS)
- Docker
- Cloud Virtual Machine

## Requirements

Before deployment, ensure that:

- Python 3.12 or newer is installed.
- All project dependencies are installed.
- The `.env` file contains valid configuration values.
- The Telegram bot has permission to post messages to the target channel.

## Production Configuration

The production `.env` file should contain valid credentials.

Do not commit the production `.env` file to the repository.

Example variables:

```dotenv
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHANNEL_ID=<YOUR_TELEGRAM_CHANNEL_ID>

COINGECKO_API_KEY=<YOUR_COINGECKO_API_KEY>
METALPRICE_API_KEY=<YOUR_METALPRICE_API_KEY>

TIMEZONE=Asia/Tehran
DAILY_POST_TIME=09:00
REQUEST_TIMEOUT=15
```

## Running the Application

Start the application:

```bash
python -m bot.main
```

Or using Docker:

```bash
docker compose up -d
```

## Monitoring

After deployment, verify that:

- The application starts successfully.
- No configuration errors are reported.
- Scheduled jobs run at the expected time.
- Messages are delivered to the Telegram channel.

## Updating the Application

Pull the latest changes:

```bash
git pull
```

Install updated dependencies if required:

```bash
pip install -r requirements.txt
```

Restart the application after updating.

## Security Recommendations

- Never expose API keys or bot tokens.
- Keep dependencies up to date.
- Review logs regularly.
- Rotate credentials if they are accidentally exposed.
- Back up important configuration files.

## Troubleshooting

If the application fails to start:

1. Verify that the `.env` file exists.
2. Check that all required environment variables are configured.
3. Confirm that API keys are valid.
4. Verify the Telegram bot token.
5. Review the application logs for errors.