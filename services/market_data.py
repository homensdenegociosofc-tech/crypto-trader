from datetime import datetime, timezone
import httpx
import pandas as pd


class MarketDataError(Exception):
    pass


class BinanceMarketData:
    BASE_URL = "https://data-api.binance.vision/api/v3"

    async def klines(self, symbol: str, interval: str = "15m", limit: int = 250) -> pd.DataFrame:
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.get(
                    f"{self.BASE_URL}/klines",
                    params={"symbol": symbol, "interval": interval, "limit": limit},
                )
                response.raise_for_status()
                rows = response.json()
        except Exception as exc:
            raise MarketDataError(f"BINANCE_UNAVAILABLE:{type(exc).__name__}") from exc

        if not isinstance(rows, list) or len(rows) < 60:
            raise MarketDataError("CANDLES_INSUFICIENTES")

        columns = [
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_base",
            "taker_quote", "ignore",
        ]
        df = pd.DataFrame(rows, columns=columns)

        numeric_columns = [
            "open", "high", "low", "close", "volume", "quote_volume",
            "taker_base", "taker_quote",
        ]
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        df = df.dropna().reset_index(drop=True)

        now = pd.Timestamp(datetime.now(timezone.utc))
        df["is_closed"] = df["close_time"] <= now

        # Elimina explicitamente qualquer candle ainda em formação.
        closed = df[df["is_closed"]].copy().reset_index(drop=True)
        if len(closed) < 60:
            raise MarketDataError("CANDLES_FECHADOS_INSUFICIENTES")

        return closed
