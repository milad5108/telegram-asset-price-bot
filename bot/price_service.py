from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from bot.config import Settings


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
METALPRICE_URL = "https://api.metalpriceapi.com/v1/latest"


@dataclass(frozen=True, slots=True)
class AssetPrice:
    """Normalized price information for one asset."""

    asset_id: str
    name: str
    symbol: str
    price_usd: float
    change_24h: float | None
    updated_at: datetime
    source: str


class PriceServiceError(RuntimeError):
    """Raised when a price provider returns invalid data or fails."""


class PriceService:
    """Fetch and normalize cryptocurrency and precious-metal prices."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def fetch_all_prices(self) -> list[AssetPrice]:
        """Fetch all supported asset prices concurrently."""

        async with httpx.AsyncClient(
            timeout=self._settings.request_timeout,
            headers={"User-Agent": "telegram-asset-price-bot/1.0"},
        ) as client:
            crypto_prices, metal_prices = await asyncio.gather(
                self._fetch_crypto_prices(client),
                self._fetch_metal_prices(client),
            )

        return [*crypto_prices, *metal_prices]

    async def _fetch_crypto_prices(
        self,
        client: httpx.AsyncClient,
    ) -> list[AssetPrice]:
        """Fetch Bitcoin, Ethereum, and Tether prices from CoinGecko."""

        payload = await self._request_json(
            client=client,
            url=COINGECKO_URL,
            source="CoinGecko",
            params={
                "ids": "bitcoin,ethereum,tether",
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            },
            headers={
                "accept": "application/json",
                "x-cg-demo-api-key": self._settings.coingecko_api_key,
            },
        )

        assets = (
            ("bitcoin", "Bitcoin", "BTC"),
            ("ethereum", "Ethereum", "ETH"),
            ("tether", "Tether", "USDT"),
        )

        prices: list[AssetPrice] = []

        for asset_id, name, symbol in assets:
            asset_data = payload.get(asset_id)

            if not isinstance(asset_data, dict):
                raise PriceServiceError(
                    f"CoinGecko response does not contain {asset_id}."
                )

            prices.append(
                AssetPrice(
                    asset_id=asset_id,
                    name=name,
                    symbol=symbol,
                    price_usd=self._require_number(
                        asset_data.get("usd"),
                        f"{asset_id}.usd",
                    ),
                    change_24h=self._optional_number(
                        asset_data.get("usd_24h_change"),
                        f"{asset_id}.usd_24h_change",
                    ),
                    updated_at=self._parse_timestamp(
                        asset_data.get("last_updated_at"),
                        f"{asset_id}.last_updated_at",
                    ),
                    source="CoinGecko",
                )
            )

        return prices

    async def _fetch_metal_prices(
        self,
        client: httpx.AsyncClient,
    ) -> list[AssetPrice]:
        """Fetch gold and silver prices from MetalpriceAPI."""

        payload = await self._request_json(
            client=client,
            url=METALPRICE_URL,
            source="MetalpriceAPI",
            params={
                "base": "USD",
                "currencies": "XAU,XAG",
            },
            headers={
                "accept": "application/json",
                "X-API-KEY": self._settings.metalprice_api_key,
            },
        )

        if payload.get("success") is False:
            error = payload.get("error")
            error_message = (
                error.get("info", "Unknown API error")
                if isinstance(error, dict)
                else "Unknown API error"
            )
            raise PriceServiceError(
                f"MetalpriceAPI request failed: {error_message}"
            )

        rates = payload.get("rates")

        if not isinstance(rates, dict):
            raise PriceServiceError(
                "MetalpriceAPI response does not contain rates."
            )

        updated_at = self._parse_timestamp(
            payload.get("timestamp"),
            "timestamp",
        )

        metals = (
            ("gold", "Gold", "XAU"),
            ("silver", "Silver", "XAG"),
        )

        prices: list[AssetPrice] = []

        for asset_id, name, symbol in metals:
            prices.append(
                AssetPrice(
                    asset_id=asset_id,
                    name=name,
                    symbol=symbol,
                    price_usd=self._extract_metal_usd_price(
                        rates,
                        symbol,
                    ),
                    change_24h=None,
                    updated_at=updated_at,
                    source="MetalpriceAPI",
                )
            )

        return prices

    async def _request_json(
        self,
        client: httpx.AsyncClient,
        url: str,
        source: str,
        params: dict[str, str],
        headers: dict[str, str],
    ) -> dict[str, Any]:
        """Send an HTTP request and return a validated JSON object."""

        try:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise PriceServiceError(
                f"{source} request timed out."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise PriceServiceError(
                f"{source} returned HTTP "
                f"{exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise PriceServiceError(
                f"Could not connect to {source}."
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise PriceServiceError(
                f"{source} returned invalid JSON."
            ) from exc

        if not isinstance(payload, dict):
            raise PriceServiceError(
                f"{source} returned an unexpected response."
            )

        return payload

    @staticmethod
    def _extract_metal_usd_price(
        rates: dict[str, Any],
        symbol: str,
    ) -> float:
        """Extract the USD price of one troy ounce of a metal."""

        direct_value = rates.get(f"USD{symbol}")

        if (
            isinstance(direct_value, (int, float))
            and not isinstance(direct_value, bool)
            and direct_value > 0
        ):
            return float(direct_value)

        inverse_rate = PriceService._require_number(
            rates.get(symbol),
            symbol,
        )

        if inverse_rate <= 0:
            raise PriceServiceError(
                f"Metal rate for {symbol} must be greater than zero."
            )

        return 1 / inverse_rate

    @staticmethod
    def _require_number(value: Any, field_name: str) -> float:
        """Validate and convert a required numeric field."""

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise PriceServiceError(
                f"Invalid numeric field: {field_name}."
            )

        return float(value)

    @staticmethod
    def _optional_number(
        value: Any,
        field_name: str,
    ) -> float | None:
        """Validate and convert an optional numeric field."""

        if value is None:
            return None

        return PriceService._require_number(value, field_name)

    @staticmethod
    def _parse_timestamp(
        value: Any,
        field_name: str,
    ) -> datetime:
        """Convert a UNIX timestamp to a timezone-aware datetime."""

        timestamp = PriceService._require_number(
            value,
            field_name,
        )

        try:
            return datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc,
            )
        except (OverflowError, OSError, ValueError) as exc:
            raise PriceServiceError(
                f"Invalid timestamp field: {field_name}."
            ) from exc
