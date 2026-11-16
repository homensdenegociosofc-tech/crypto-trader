from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Crypto Trader Pro API"
    database_url: str | None = None
    redis_url: str | None = None
    ai_provider: str = "deepseek"
    ai_model: str = "deepseek-chat"
    deepseek_api_key: str | None = None
    openai_api_key: str | None = None
    real_trading_enabled: bool = False
    initial_paper_balance: float = 1000.0
    max_risk_per_trade_percent: float = 1.0
    max_daily_loss_percent: float = 3.0
    max_position_percent: float = 15.0
    max_open_positions: int = 3
    max_trades_per_day: int = 10
    min_risk_reward: float = 1.5
    analysis_interval: str = "15m"
    analysis_candle_limit: int = 250
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
@lru_cache
def get_settings(): return Settings()
