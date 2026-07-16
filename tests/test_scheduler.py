from datetime import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram.constants import ParseMode

from bot.config import Settings
from bot.scheduler import (
    DAILY_PRICE_JOB_NAME,
    daily_price_job,
    publish_prices,
    schedule_daily_price_job,
)


def make_settings() -> Settings:
    return Settings(
        telegram_bot_token="test-token",
        telegram_channel_id="@test-channel",
        coingecko_api_key="test-coingecko-key",
        metalprice_api_key="test-metal-key",
        timezone="Asia/Tehran",
        daily_post_time=time(hour=9),
        request_timeout=15,
    )


def test_schedule_daily_price_job() -> None:
    settings = make_settings()

    application = MagicMock()
    application.job_queue = MagicMock()

    expected_job = MagicMock()
    application.job_queue.run_daily.return_value = expected_job

    result = schedule_daily_price_job(
        application=application,
        settings=settings,
    )

    assert result is expected_job

    call_arguments = (
        application.job_queue.run_daily.call_args.kwargs
    )

    assert call_arguments["callback"] is daily_price_job
    assert call_arguments["data"] == settings
    assert call_arguments["name"] == DAILY_PRICE_JOB_NAME
    assert call_arguments["time"].hour == 9
    assert call_arguments["time"].minute == 0
    assert call_arguments["time"].tzinfo.key == "Asia/Tehran"


@pytest.mark.asyncio
async def test_daily_price_job_calls_publish_prices() -> None:
    settings = make_settings()
    application = MagicMock()

    context = SimpleNamespace(
        application=application,
        job=SimpleNamespace(data=settings),
    )

    with patch(
        "bot.scheduler.publish_prices",
        new_callable=AsyncMock,
    ) as mocked_publish:
        await daily_price_job(context)

    mocked_publish.assert_awaited_once_with(
        application=application,
        settings=settings,
    )


@pytest.mark.asyncio
async def test_publish_prices_sends_html_message() -> None:
    settings = make_settings()

    application = MagicMock()
    application.bot.send_message = AsyncMock()

    fake_prices = [MagicMock()]

    with (
        patch("bot.scheduler.PriceService") as service_class,
        patch(
            "bot.scheduler.format_price_message",
            return_value="<b>Test prices</b>",
        ) as formatter,
    ):
        service = service_class.return_value
        service.fetch_all_prices = AsyncMock(
            return_value=fake_prices
        )

        await publish_prices(
            application=application,
            settings=settings,
        )

    service_class.assert_called_once_with(settings)
    service.fetch_all_prices.assert_awaited_once_with()

    formatter.assert_called_once_with(
        fake_prices,
        timezone_name="Asia/Tehran",
    )

    application.bot.send_message.assert_awaited_once_with(
        chat_id="@test-channel",
        text="<b>Test prices</b>",
        parse_mode=ParseMode.HTML,
    )


def test_missing_job_queue_raises_error() -> None:
    application = MagicMock()
    application.job_queue = None

    with pytest.raises(
        RuntimeError,
        match="JobQueue is unavailable",
    ):
        schedule_daily_price_job(
            application=application,
            settings=make_settings(),
        )
