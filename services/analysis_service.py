import math
from datetime import datetime,timezone
from services.market_data import BinanceMarketData
from services.indicator_engine import IndicatorEngine
from services.strategy_engine import StrategyEngine
class AnalysisService:
    def __init__(self): self.market=BinanceMarketData(); self.indicators=IndicatorEngine(); self.strategies=StrategyEngine()
    async def analyze(self,symbol,interval="15m",limit=250):
        df=await self.market.klines(symbol,interval,limit); out=self.indicators.calculate(df); row=out.iloc[-1].to_dict()
        required=["close","ema_9","ema_21","ema_50","rsi_14","atr_14","atr_pct","adx_14","plus_di","minus_di","bb_mid","bb_upper","bb_lower","bb_width_pct","volume_ratio","high_20_prev","low_20_prev","return_1","return_4"]
        if any(v is None or (isinstance(v,float) and math.isnan(v)) for v in [row.get(k) for k in required]): raise ValueError("INDICADORES_INCOMPLETOS")
        strategy=self.strategies.evaluate(row)
        return {"symbol":symbol,"interval":interval,"candle_close_time":out.iloc[-1].close_time.isoformat(),"generated_at":datetime.now(timezone.utc).isoformat(),"price":round(row["close"],8),"indicators":{k:round(float(row[k]),6) for k in required if k!="close"},"market":strategy,"data_quality":{"candles":len(out),"source":"Binance public market data","closed_candle_only":True},"execution_enabled":False}
