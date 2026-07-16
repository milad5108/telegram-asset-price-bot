from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, time

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings loaded from environment variables."""

    telegram_bot_token: str
    telegram_channel_id: str
    coingecko_api_key: str
    metalprice_api_key: str
    timezone: str
    daily_post_time: time
    request_timeout: float


def _get_required_env(name: str) -> str:
    """Return a required environment variable or raise a clear error."""

    value = os.getenv(name, "").strip()

    if not value:
        raise ValueError(
            f"Environment variable {name} is required. "
            "Add it to the .env file."
        )

    return value


def _parse_daily_post_time(value: str) -> time:
    """Convert an HH:MM value to a time object."""

    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise ValueError(
            "DAILY_POST_TIME must use the HH:MM format, for example 09:00."
        ) from exc


def _parse_request_timeout(value: str) -> float:
    """Convert the request timeout value to a positive number."""

    try:
        timeout = float(value)
    except ValueError as exc:
        raise ValueError("REQUEST_TIMEOUT must be a number.") from exc

    if timeout <= 0:
        raise ValueError("REQUEST_TIMEOUT must be greater than zero.")

    return timeout


def load_settings() -> Settings:
    """Load and validate application settings."""

    load_dotenv()

    return Settings(
        telegram_bot_token=_get_required_env("TELEGRAM_BOT_TOKEN"),
        telegram_channel_id=_get_required_env("TELEGRAM_CHANNEL_ID"),
        coingecko_api_key=_get_required_env("COINGECKO_API_KEY"),
        metalprice_api_key=_get_required_env("METALPRICE_API_KEY"),
        timezone=os.getenv("TIMEZONE", "Asia/Tehran").strip() or "Asia/Tehran",
        daily_post_time=_parse_daily_post_time(
            os.getenv("DAILY_POST_TIME", "09:00").strip()
        ),
        request_timeout=_parse_request_timeout(
            os.getenv("REQUEST_TIMEOUT", "15").strip()
        ),
    )
