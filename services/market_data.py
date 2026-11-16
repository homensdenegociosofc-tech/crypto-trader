import httpx
import pandas as pd
class MarketDataError(Exception): pass
class BinanceMarketData:
    BASE_URL="https://data-api.binance.vision/api/v3"
    async def klines(self,symbol:str,interval:str="15m",limit:int=250)->pd.DataFrame:
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                r=await client.get(f"{self.BASE_URL}/klines",params={"symbol":symbol,"interval":interval,"limit":limit})
                r.raise_for_status(); rows=r.json()
        except Exception as exc: raise MarketDataError(f"BINANCE_UNAVAILABLE:{type(exc).__name__}") from exc
        if not isinstance(rows,list) or len(rows)<60: raise MarketDataError("CANDLES_INSUFICIENTES")
        cols=["open_time","open","high","low","close","volume","close_time","quote_volume","trades","taker_base","taker_quote","ignore"]
        df=pd.DataFrame(rows,columns=cols)
        for c in ["open","high","low","close","volume","quote_volume","taker_base","taker_quote"]: df[c]=pd.to_numeric(df[c],errors="coerce")
        df["open_time"]=pd.to_datetime(df["open_time"],unit="ms",utc=True); df["close_time"]=pd.to_datetime(df["close_time"],unit="ms",utc=True)
        return df.dropna().reset_index(drop=True)
