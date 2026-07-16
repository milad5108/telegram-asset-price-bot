from datetime import datetime, timezone

import pytest

from bot.message_formatter import format_price_message
from bot.price_service import AssetPrice


def make_prices() -> list[AssetPrice]:
    updated_at = datetime.fromtimestamp(
        1_700_000_000,
        tz=timezone.utc,
    )

    return [
        AssetPrice(
            asset_id="bitcoin",
            name="Bitcoin",
            symbol="BTC",
            price_usd=65000,
            change_24h=2.5,
            updated_at=updated_at,
            source="CoinGecko",
        ),
        AssetPrice(
            asset_id="ethereum",
            name="Ethereum",
            symbol="ETH",
            price_usd=3500,
            change_24h=-1.2,
            updated_at=updated_at,
            source="CoinGecko",
        ),
        AssetPrice(
            asset_id="tether",
            name="Tether",
            symbol="USDT",
            price_usd=1,
            change_24h=0,
            updated_at=updated_at,
            source="CoinGecko",
        ),
        AssetPrice(
            asset_id="gold",
            name="Gold",
            symbol="XAU",
            price_usd=2000,
            change_24h=None,
            updated_at=updated_at,
            source="MetalpriceAPI",
        ),
        AssetPrice(
            asset_id="silver",
            name="Silver",
            symbol="XAG",
            price_usd=25,
            change_24h=None,
            updated_at=updated_at,
            source="MetalpriceAPI",
        ),
    ]


def test_format_price_message() -> None:
    message = format_price_message(
        make_prices(),
        timezone_name="Asia/Tehran",
    )

    assert "<b>📊 قیمت روز دارایی‌ها</b>" in message
    assert "<code>$65,000.00</code>" in message
    assert "<code>$1.0000</code>" in message
    assert "<code>+2.50%</code>" in message
    assert "<code>-1.20%</code>" in message
    assert "$2,000.00</code> / اونس تروا" in message
    assert "CoinGecko" in message
    assert "MetalpriceAPI" in message


def test_empty_price_list_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="At least one asset price is required",
    ):
        format_price_message([], timezone_name="Asia/Tehran")


def test_invalid_timezone_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="Unknown timezone",
    ):
        format_price_message(
            make_prices(),
            timezone_name="Invalid/Timezone",
        )
