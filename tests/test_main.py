from datetime import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram.constants import ParseMode

from bot.config import Settings
from bot.main import (
    SETTINGS_KEY,
    channel_prices_command,
    post_init,
    prices_command,
    start_command,
)
from bot.price_service import PriceServiceError


def make_settings() -> Settings:
    return Settings(
        telegram_bot_token="123456:test-token",
        telegram_channel_id="@test-channel",
        coingecko_api_key="test-coingecko-key",
        metalprice_api_key="test-metal-key",
        timezone="Asia/Tehran",
        daily_post_time=time(hour=9),
        request_timeout=15,
    )


@pytest.mark.asyncio
async def test_start_command_sends_help_message() -> None:
    message = MagicMock()
    message.reply_text = AsyncMock()

    update = SimpleNamespace(
        effective_message=message,
    )

    await start_command(
        update=update,
        context=MagicMock(),
    )

    sent_text = message.reply_text.await_args.args[0]

    assert "/prices" in sent_text
    assert "بیت‌کوین" in sent_text


@pytest.mark.asyncio
async def test_prices_command_sends_formatted_message() -> None:
    settings = make_settings()

    message = MagicMock()
    message.reply_text = AsyncMock()

    update = SimpleNamespace(
        effective_message=message,
    )

    application = SimpleNamespace(
        bot_data={SETTINGS_KEY: settings},
    )
    context = SimpleNamespace(
        application=application,
    )

    fake_prices = [MagicMock()]

    with (
        patch("bot.main.PriceService") as service_class,
        patch(
            "bot.main.format_price_message",
            return_value="<b>Prices</b>",
        ) as formatter,
    ):
        service = service_class.return_value
        service.fetch_all_prices = AsyncMock(
            return_value=fake_prices
        )

        await prices_command(update, context)

    service_class.assert_called_once_with(settings)
    service.fetch_all_prices.assert_awaited_once_with()

    formatter.assert_called_once_with(
        fake_prices,
        timezone_name="Asia/Tehran",
    )

    message.reply_text.assert_awaited_once_with(
        text="<b>Prices</b>",
        parse_mode=ParseMode.HTML,
    )


@pytest.mark.asyncio
async def test_prices_command_handles_service_error() -> None:
    settings = make_settings()

    message = MagicMock()
    message.reply_text = AsyncMock()

    update = SimpleNamespace(
        effective_message=message,
    )
    context = SimpleNamespace(
        application=SimpleNamespace(
            bot_data={SETTINGS_KEY: settings},
        )
    )

    with patch("bot.main.PriceService") as service_class:
        service = service_class.return_value
        service.fetch_all_prices = AsyncMock(
            side_effect=PriceServiceError(
                "Provider unavailable."
            )
        )

        await prices_command(update, context)

    sent_text = message.reply_text.await_args.args[0]

    assert "دریافت قیمت‌ها با خطا مواجه شد" in sent_text


@pytest.mark.asyncio
async def test_channel_prices_command_publishes_prices() -> None:
    settings = make_settings()

    application = SimpleNamespace(
        bot_data={SETTINGS_KEY: settings},
    )
    context = SimpleNamespace(
        application=application,
    )

    with patch(
        "bot.main.publish_prices",
        new_callable=AsyncMock,
    ) as mocked_publish:
        await channel_prices_command(
            update=MagicMock(),
            context=context,
        )

    mocked_publish.assert_awaited_once_with(
        application=application,
        settings=settings,
    )


@pytest.mark.asyncio
async def test_channel_prices_command_handles_publish_error() -> None:
    settings = make_settings()

    application = SimpleNamespace(
        bot_data={SETTINGS_KEY: settings},
    )
    context = SimpleNamespace(
        application=application,
    )

    with (
        patch(
            "bot.main.publish_prices",
            new_callable=AsyncMock,
        ) as mocked_publish,
        patch(
            "bot.main.logger.exception"
        ) as mocked_logger,
    ):
        mocked_publish.side_effect = RuntimeError(
            "Telegram unavailable."
        )

        await channel_prices_command(
            update=MagicMock(),
            context=context,
        )

    mocked_publish.assert_awaited_once_with(
        application=application,
        settings=settings,
    )
    mocked_logger.assert_called_once_with(
        "Could not publish prices from channel command."
    )


@pytest.mark.asyncio
async def test_post_init_registers_scheduler() -> None:
    settings = make_settings()

    application = MagicMock()
    application.bot_data = {
        SETTINGS_KEY: settings,
    }

    with patch(
        "bot.main.schedule_daily_price_job"
    ) as mocked_scheduler:
        await post_init(application)

    mocked_scheduler.assert_called_once_with(
        application=application,
        settings=settings,
    )
