from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.config import Settings, load_settings
from bot.message_formatter import format_price_message
from bot.price_service import PriceService, PriceServiceError
from bot.scheduler import (
    publish_prices,
    schedule_daily_price_job,
)


logger = logging.getLogger(__name__)

SETTINGS_KEY = "settings"


def _get_settings(application: Application) -> Settings:
    """Return validated application settings from bot data."""

    settings = application.bot_data.get(SETTINGS_KEY)

    if not isinstance(settings, Settings):
        raise RuntimeError(
            "Application settings are unavailable."
        )

    return settings


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Show the bot introduction and available commands."""

    del context

    if update.effective_message is None:
        return

    await update.effective_message.reply_text(
        "سلام 👋\n\n"
        "این ربات قیمت بیت‌کوین، اتریوم، تتر، "
        "طلا و نقره را دریافت و منتشر می‌کند.\n\n"
        "برای دریافت قیمت‌های فعلی از دستور "
        "/prices استفاده کنید."
    )


async def prices_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Fetch current prices and send them to the user."""

    if update.effective_message is None:
        return

    settings = _get_settings(context.application)
    service = PriceService(settings)

    try:
        prices = await service.fetch_all_prices()
    except PriceServiceError:
        logger.warning(
            "Could not fetch prices for /prices command.",
            exc_info=True,
        )

        await update.effective_message.reply_text(
            "❌ دریافت قیمت‌ها با خطا مواجه شد.\n"
            "لطفاً چند دقیقه دیگر دوباره تلاش کنید."
        )
        return

    message = format_price_message(
        prices,
        timezone_name=settings.timezone,
    )

    await update.effective_message.reply_text(
        text=message,
        parse_mode=ParseMode.HTML,
    )


async def channel_prices_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Publish current prices when /prices is posted in the channel."""

    del update

    settings = _get_settings(context.application)

    try:
        await publish_prices(
            application=context.application,
            settings=settings,
        )
    except Exception:
        logger.exception(
            "Could not publish prices from channel command."
        )


async def post_init(application: Application) -> None:
    """Register scheduled jobs after Telegram initialization."""

    settings = _get_settings(application)

    schedule_daily_price_job(
        application=application,
        settings=settings,
    )

    logger.info(
        "Daily price job scheduled for %s in %s.",
        settings.daily_post_time.strftime("%H:%M"),
        settings.timezone,
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Log unexpected Telegram application errors."""

    del update

    error = context.error
    exception_info = None

    if isinstance(error, BaseException):
        exception_info = (
            type(error),
            error,
            error.__traceback__,
        )

    logger.error(
        "Unhandled exception while processing an update.",
        exc_info=exception_info,
    )


def build_application(settings: Settings) -> Application:
    """Create and configure the Telegram application."""

    application = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .post_init(post_init)
        .build()
    )

    application.bot_data[SETTINGS_KEY] = settings

    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("prices", prices_command)
    )

    application.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POSTS
            & filters.Regex(
                r"^/prices(?:@MiladAssetPriceBot)?(?:\s|$)"
            ),
            channel_prices_command,
        )
    )

    application.add_error_handler(error_handler)

    return application


def main() -> None:
    """Load settings and start Telegram polling."""

    logging.basicConfig(
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        level=logging.INFO,
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    settings = load_settings()
    application = build_application(settings)

    logger.info("Telegram Asset Price Bot is starting.")
    application.run_polling()


if __name__ == "__main__":
    main()