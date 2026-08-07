# Repository Secrets and Environment Variables

This project uses environment variables to store configuration values and sensitive credentials.

**Never commit real API keys, Telegram bot tokens, passwords, or any other sensitive information to the repository.**

---

## Environment Variables

The application uses the following environment variables:

| Variable | Required | Sensitive | Description |
|----------|:--------:|:---------:|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Yes | Telegram Bot API token obtained from BotFather |
| `TELEGRAM_CHANNEL_ID` | Yes | No | Telegram channel username or ID used for scheduled posts |
| `COINGECKO_API_KEY` | Yes | Yes | CoinGecko API key for cryptocurrency price requests |
| `METALPRICE_API_KEY` | Yes | Yes | MetalpriceAPI key for gold and silver prices |
| `TIMEZONE` | Yes | No | Time zone used by the scheduler |
| `DAILY_POST_TIME` | Yes | No | Daily scheduled posting time |
| `REQUEST_TIMEOUT` | Yes | No | Timeout for external API requests (seconds) |

---

## Local Development

Copy the example environment file.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

After creating the `.env` file, replace the placeholder values with your own credentials.

Example:

```dotenv
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHANNEL_ID=<YOUR_TELEGRAM_CHANNEL_ID>

COINGECKO_API_KEY=<YOUR_COINGECKO_API_KEY>
METALPRICE_API_KEY=<YOUR_METALPRICE_API_KEY>

TIMEZONE=Asia/Tehran
DAILY_POST_TIME=09:00
REQUEST_TIMEOUT=15
```

---

## GitHub Repository Secrets

If GitHub Actions requires access to sensitive credentials in the future, store them in:

**Repository → Settings → Secrets and variables → Actions**

Recommended GitHub Secrets:

- `TELEGRAM_BOT_TOKEN`
- `COINGECKO_API_KEY`
- `METALPRICE_API_KEY`

Do not hard-code secrets inside the repository or GitHub Actions workflow files.

---

## Security Rules

- Never commit the real `.env` file.
- Never expose API keys or bot tokens in screenshots.
- Never print sensitive credentials in application logs.
- Never commit secrets to Git history.
- Keep `.env.example` free of real credentials.
- Rotate any credential immediately if it is accidentally exposed.

Before every commit:

```powershell
git status
git diff
git diff --cached
```

Verify that `.env` is ignored by Git:

```powershell
git check-ignore -v .env
```

---

## Important

The `.env.example` file may be committed to the repository.

The real `.env` file must remain local and must never be committed to the repository.