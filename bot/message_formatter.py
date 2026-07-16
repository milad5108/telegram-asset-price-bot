from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from bot.price_service import AssetPrice


ASSET_ORDER = {
    "bitcoin": 0,
    "ethereum": 1,
    "tether": 2,
    "gold": 3,
    "silver": 4,
}

ASSET_EMOJIS = {
    "bitcoin": "₿",
    "ethereum": "◆",
    "tether": "₮",
    "gold": "🥇",
    "silver": "🥈",
}


def format_price_message(
    prices: Iterable[AssetPrice],
    timezone_name: str,
) -> str:
    """Build a Telegram HTML message containing all asset prices."""

    price_list = list(prices)

    if not price_list:
        raise ValueError("At least one asset price is required.")

    timezone = _load_timezone(timezone_name)
    ordered_prices = sorted(
        price_list,
        key=lambda item: ASSET_ORDER.get(item.asset_id, 999),
    )

    lines = [
        "<b>📊 قیمت روز دارایی‌ها</b>",
        "",
    ]

    lines.extend(_format_asset_line(price) for price in ordered_prices)

    lines.extend(
        [
            "",
            "<b>🕒 آخرین به‌روزرسانی منابع</b>",
            *_format_source_updates(ordered_prices, timezone),
            "",
            "💵 مبنای قیمت‌ها: دلار آمریکا",
            "⚠️ قیمت فلزات ممکن است با تأخیر روزانه ارائه شود.",
        ]
    )

    return "\n".join(lines)


def _format_asset_line(price: AssetPrice) -> str:
    """Format one asset price as a Telegram HTML line."""

    emoji = ASSET_EMOJIS.get(price.asset_id, "•")
    name = escape(price.name)
    symbol = escape(price.symbol)
    formatted_price = _format_usd_price(price)

    line = (
        f"{emoji} <b>{name}</b> "
        f"(<code>{symbol}</code>): "
        f"<code>${formatted_price}</code>"
    )

    if price.symbol in {"XAU", "XAG"}:
        line += " / اونس تروا"

    if price.change_24h is not None:
        line += f"  {_format_change(price.change_24h)}"

    return line


def _format_usd_price(price: AssetPrice) -> str:
    """Format prices using an appropriate number of decimal places."""

    if price.symbol == "USDT":
        return f"{price.price_usd:,.4f}"

    return f"{price.price_usd:,.2f}"


def _format_change(change: float) -> str:
    """Format a 24-hour percentage change."""

    if change > 0:
        return f"🟢 <code>+{change:.2f}%</code>"

    if change < 0:
        return f"🔴 <code>{change:.2f}%</code>"

    return "⚪ <code>0.00%</code>"


def _format_source_updates(
    prices: list[AssetPrice],
    timezone: ZoneInfo,
) -> list[str]:
    """Create one update-time line for every price provider."""

    updates: dict[str, datetime] = {}

    for price in prices:
        current_timestamp = updates.get(price.source)

        if (
            current_timestamp is None
            or price.updated_at > current_timestamp
        ):
            updates[price.source] = price.updated_at

    return [
        (
            f"• {escape(source)}: "
            f"<code>{updated_at.astimezone(timezone):%Y-%m-%d %H:%M}</code>"
        )
        for source, updated_at in sorted(updates.items())
    ]


def _load_timezone(timezone_name: str) -> ZoneInfo:
    """Load a valid IANA timezone."""

    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(
            f"Unknown timezone: {timezone_name}."
        ) from exc
