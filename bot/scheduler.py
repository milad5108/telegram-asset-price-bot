from __future__ import annotations

import logging
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, Job

from bot.config import Settings
from bot.message_formatter import format_price_message
from bot.price_service import PriceService


logger = logging.getLogger(__name__)

DAILY_PRICE_JOB_NAME = "daily-price-post"


async def publish_prices(
    application: Application,
    settings: Settings,
) -> None:
    """Fetch prices and publish the formatted message to the channel."""

    service = PriceService(settings)
    prices = await service.fetch_all_prices()

    message = format_price_message(
        prices,
        timezone_name=settings.timezone,
    )

    await application.bot.send_message(
        chat_id=settings.telegram_channel_id,
        text=message,
        parse_mode=ParseMode.HTML,
    )


async def daily_price_job(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Run the scheduled daily price publication."""

    if context.job is None:
        raise RuntimeError("Scheduled job context is missing.")

    settings = context.job.data

    if not isinstance(settings, Settings):
        raise RuntimeError(
            "Scheduled job does not contain valid settings."
        )

    try:
        await publish_prices(
            application=context.application,
            settings=settings,
        )
    except Exception:
        logger.exception("Scheduled price publication failed.")


def schedule_daily_price_job(
    application: Application,
    settings: Settings,
) -> Job:
    """Register the daily Telegram channel publication job."""

    job_queue = application.job_queue

    if job_queue is None:
        raise RuntimeError(
            "JobQueue is unavailable. Install "
            "python-telegram-bot[job-queue]."
        )

    try:
        timezone = ZoneInfo(settings.timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(
            f"Unknown timezone: {settings.timezone}."
        ) from exc

    scheduled_time = settings.daily_post_time.replace(
        tzinfo=timezone,
    )

    return job_queue.run_daily(
        callback=daily_price_job,
        time=scheduled_time,
        data=settings,
        name=DAILY_PRICE_JOB_NAME,
    )
