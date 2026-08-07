# Configuration Guide

This document explains how to configure the application before running it.

## Environment Variables

The project uses a `.env` file for configuration.

Create a local `.env` file by copying the example file.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

## Required Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token from BotFather |
| `TELEGRAM_CHANNEL_ID` | Telegram channel username or channel ID |
| `COINGECKO_API_KEY` | CoinGecko API key |
| `METALPRICE_API_KEY` | MetalpriceAPI key |
| `TIMEZONE` | Scheduler time zone |
| `DAILY_POST_TIME` | Daily automatic posting time |
| `REQUEST_TIMEOUT` | Timeout for external API requests (seconds) |

## Example Configuration

```dotenv
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHANNEL_ID=<YOUR_TELEGRAM_CHANNEL_ID>

COINGECKO_API_KEY=<YOUR_COINGECKO_API_KEY>
METALPRICE_API_KEY=<YOUR_METALPRICE_API_KEY>

TIMEZONE=Asia/Tehran
DAILY_POST_TIME=09:00
REQUEST_TIMEOUT=15
```

## Security Notes

- Never commit the real `.env` file.
- Never publish API keys or bot tokens.
- Keep `.env.example` free of sensitive information.
- Rotate exposed credentials immediately.

## Verification

Before running the application, verify that:

- The `.env` file exists.
- All required variables are configured.
- API keys are valid.
- The Telegram bot has permission to access the target channel.