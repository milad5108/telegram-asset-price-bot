from datetime import time

import httpx
import pytest

from bot.config import Settings
from bot.price_service import PriceService, PriceServiceError


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


@pytest.mark.asyncio
async def test_fetch_crypto_prices() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-cg-demo-api-key"] == "test-coingecko-key"

        return httpx.Response(
            status_code=200,
            json={
                "bitcoin": {
                    "usd": 65000,
                    "usd_24h_change": 2.5,
                    "last_updated_at": 1_700_000_000,
                },
                "ethereum": {
                    "usd": 3500,
                    "usd_24h_change": -1.2,
                    "last_updated_at": 1_700_000_000,
                },
                "tether": {
                    "usd": 1,
                    "usd_24h_change": 0.01,
                    "last_updated_at": 1_700_000_000,
                },
            },
        )

    service = PriceService(make_settings())
    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        prices = await service._fetch_crypto_prices(client)

    assert len(prices) == 3
    assert prices[0].symbol == "BTC"
    assert prices[0].price_usd == 65000
    assert prices[1].symbol == "ETH"
    assert prices[1].change_24h == -1.2
    assert prices[2].symbol == "USDT"
    assert prices[2].price_usd == 1


@pytest.mark.asyncio
async def test_fetch_metal_prices() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-API-KEY"] == "test-metal-key"

        return httpx.Response(
            status_code=200,
            json={
                "success": True,
                "timestamp": 1_700_000_000,
                "base": "USD",
                "rates": {
                    "XAU": 0.0005,
                    "XAG": 0.04,
                },
            },
        )

    service = PriceService(make_settings())
    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        prices = await service._fetch_metal_prices(client)

    assert len(prices) == 2
    assert prices[0].symbol == "XAU"
    assert prices[0].price_usd == pytest.approx(2000)
    assert prices[1].symbol == "XAG"
    assert prices[1].price_usd == pytest.approx(25)


@pytest.mark.asyncio
async def test_missing_crypto_data_raises_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={},
        )

    service = PriceService(make_settings())
    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(
            PriceServiceError,
            match="does not contain bitcoin",
        ):
            await service._fetch_crypto_prices(client)
