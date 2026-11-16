from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_validator
class TradingMode(str, Enum):
    simulation="Simulação"
    observation="Observação"
class SessionStart(BaseModel):
    mode: TradingMode=TradingMode.simulation
    assets: list[str]=Field(default_factory=lambda:["BTCUSDT","ETHUSDT","SOLUSDT"],min_length=1,max_length=20)
    daily_target_usdt: float=Field(default=50,ge=0)
    max_daily_loss_usdt: float=Field(default=20,gt=0)
    @field_validator("assets")
    @classmethod
    def clean_assets(cls,v):
        out=list(dict.fromkeys(x.upper().strip() for x in v))
        if any(not x.endswith("USDT") or not x.isalnum() for x in out): raise ValueError("Pares USDT inválidos")
        return out
class SessionState(BaseModel):
    active: bool=False
    emergency_stop: bool=False
    mode: TradingMode=TradingMode.simulation
    assets:list[str]=Field(default_factory=list)
    daily_target_usdt:float=50
    max_daily_loss_usdt:float=20
    started_at:datetime|None=None
    stopped_at:datetime|None=None
    updated_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
class AnalysisRequest(BaseModel):
    symbols:list[str]=Field(min_length=1,max_length=20)
    interval:str="15m"
    @field_validator("symbols")
    @classmethod
    def symbols_valid(cls,v):
        out=list(dict.fromkeys(x.upper().strip() for x in v))
        if any(not x.endswith("USDT") or not x.isalnum() for x in out): raise ValueError("Símbolo inválido")
        return out
    @field_validator("interval")
    @classmethod
    def interval_valid(cls,v):
        allowed={"1m","3m","5m","15m","30m","1h","2h","4h","1d"}
        if v not in allowed: raise ValueError("Intervalo não permitido")
        return v
