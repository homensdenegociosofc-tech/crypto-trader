import hashlib
import json
import math
from datetime import datetime, timezone

from services.market_data import BinanceMarketData
from services.indicator_engine import IndicatorEngine
from services.strategy_engine import StrategyEngine


class AnalysisService:
    def __init__(self):
        self.market = BinanceMarketData()
        self.indicators = IndicatorEngine()
        self.strategies = StrategyEngine()

    async def analyze(self, symbol: str, interval: str = "15m", limit: int = 250) -> dict:
        df = await self.market.klines(symbol, interval, limit)
        calculated = self.indicators.calculate(df)
        last = calculated.iloc[-1]
        row = last.to_dict()

        required = [
            "close", "ema_9", "ema_21", "ema_50", "rsi_14", "atr_14",
            "atr_pct", "adx_14", "plus_di", "minus_di", "bb_mid",
            "bb_upper", "bb_lower", "bb_width_pct", "volume_ratio",
            "high_20_prev", "low_20_prev", "return_1", "return_4",
        ]
        if any(
            value is None or (isinstance(value, float) and math.isnan(value))
            for value in (row.get(key) for key in required)
        ):
            raise ValueError("INDICADORES_INCOMPLETOS")

        generated_at = datetime.now(timezone.utc)
        open_time = last.open_time.to_pydatetime()
        close_time = last.close_time.to_pydatetime()
        candle_is_closed = close_time <= generated_at
        if not candle_is_closed:
            raise ValueError("CANDLE_AINDA_ABERTO")

        data_age_seconds = max(0, int((generated_at - close_time).total_seconds()))
        strategy = self.strategies.evaluate(row)

        snapshot_base = {
            "symbol": symbol,
            "interval": interval,
            "candle_open_time": open_time.isoformat(),
            "candle_close_time": close_time.isoformat(),
            "price": round(float(row["close"]), 8),
        }
        snapshot_id = hashlib.sha256(
            json.dumps(snapshot_base, sort_keys=True).encode("utf-8")
        ).hexdigest()[:24]

        # Nesta fase, candidato não equivale a sinal confirmado.
        candidate = strategy.get("candidate")
        confirmed_signal = None
        confirmation_reasons = []
        if candidate:
            confirmation_reasons.append(
                "Candidato técnico detectado, aguardando validação Multi-IA e Safety Gate."
            )

        market = {
            **strategy,
            "candidate": candidate,
            "confirmed_signal": confirmed_signal,
            "trade_allowed": False,
            "confirmation_reasons": confirmation_reasons,
        }

        return {
            "snapshot_id": snapshot_id,
            "symbol": symbol,
            "interval": interval,
            "candle_open_time": open_time.isoformat(),
            "candle_close_time": close_time.isoformat(),
            "generated_at": generated_at.isoformat(),
            "data_age_seconds": data_age_seconds,
            "price": round(float(row["close"]), 8),
            "indicators": {
                key: round(float(row[key]), 6)
                for key in required
                if key != "close"
            },
            "market": market,
            "data_quality": {
                "candles": len(calculated),
                "source": "Binance public market data",
                "closed_candle_only": True,
                "selected_candle_is_closed": candle_is_closed,
                "last_open_candle_discarded": True,
                "data_age_seconds": data_age_seconds,
            },
            "execution_enabled": False,
        }
