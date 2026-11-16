from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class TradingMode(str, Enum):
    simulation = "Simulação"
    observation = "Observação"

class SessionStart(BaseModel):
    mode: TradingMode = TradingMode.simulation
    assets: list[str] = Field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"], min_length=1, max_length=20)
    daily_target_usdt: float = Field(default=50, ge=0)
    max_daily_loss_usdt: float = Field(default=20, gt=0)

    @field_validator("assets")
    @classmethod
    def validate_assets(cls, values: list[str]) -> list[str]:
        cleaned = list(dict.fromkeys(v.upper().strip() for v in values))
        if any(not v.endswith("USDT") or not v.isalnum() for v in cleaned):
            raise ValueError("Todos os ativos devem ser pares USDT válidos")
        return cleaned

class SessionState(BaseModel):
    active: bool = False
    emergency_stop: bool = False
    mode: TradingMode = TradingMode.simulation
    assets: list[str] = Field(default_factory=list)
    daily_target_usdt: float = 50
    max_daily_loss_usdt: float = 20
    started_at: datetime | None = None
    stopped_at: datetime | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIDecision(BaseModel):
    schema_version: str = "1.0"
    decision_id: str
    decision: str
    symbol: str | None = None
    side: str | None = None
    strategy: str | None = None
    confidence: float = Field(default=0, ge=0, le=1)
    entry_type: str | None = None
    entry_price: float | None = Field(default=None, gt=0)
    stop_loss: float | None = Field(default=None, gt=0)
    take_profit: float | None = Field(default=None, gt=0)
    position_size_usdt: float | None = Field(default=None, gt=0)
    risk_percentage: float | None = Field(default=None, gt=0)
    expected_risk_reward: float | None = Field(default=None, gt=0)
    timeframe: str | None = None
    max_holding_minutes: int | None = Field(default=None, gt=0)
    reason: str

class AccountSummary(BaseModel):
    balance: float
    open_pnl: float = 0
    daily_pnl: float = 0
    equity: float
    open_positions: int = 0
    trades_today: int = 0
