from datetime import datetime,timezone
from redis import Redis
from config import get_settings
from schemas import SessionState
class StateManager:
    KEY="crypto_trader:session"
    def __init__(self):
        self.s=get_settings(); self._memory=SessionState(); self._redis=None
        if self.s.redis_url:
            try:
                self._redis=Redis.from_url(self.s.redis_url,decode_responses=True,socket_timeout=5); self._redis.ping()
            except Exception:self._redis=None
    def get(self):
        if self._redis:
            raw=self._redis.get(self.KEY)
            if raw:return SessionState.model_validate_json(raw)
        return self._memory
    def save(self,x):
        x.updated_at=datetime.now(timezone.utc); self._memory=x
        if self._redis:self._redis.set(self.KEY,x.model_dump_json())
        return x
    def health(self): return "conectado" if self._redis else ("não configurado" if not self.s.redis_url else "indisponível")
