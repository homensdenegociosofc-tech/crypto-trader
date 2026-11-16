from datetime import datetime, timezone
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from schemas import SessionStart, SessionState
from state_manager import StateManager
from services.paper_executor import PaperTradingEngine

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"] if settings.allowed_origins == "*" else settings.allowed_origins.split(","), allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
state = StateManager()
engine = PaperTradingEngine()

@app.get("/")
def root():
    return {"status": "online", "message": "Crypto Trader Pro funcionando", "version": "0.2.0", "mode": "paper_trading"}

@app.get("/health")
def health():
    db_status = "não configurado"
    if settings.database_url:
        try:
            conn = psycopg2.connect(settings.database_url, connect_timeout=5)
            conn.close()
            db_status = "conectado"
        except Exception:
            db_status = "indisponível"
    return {"api": "ok", "database": db_status, "redis": state.health(), "ai_provider": settings.ai_provider, "real_trading_enabled": False, "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/api/session/start", response_model=SessionState)
def start_session(payload: SessionStart):
    current = state.get()
    if current.active:
        raise HTTPException(409, "Já existe uma sessão ativa")
    new_state = SessionState(active=True, mode=payload.mode, assets=payload.assets, daily_target_usdt=payload.daily_target_usdt, max_daily_loss_usdt=payload.max_daily_loss_usdt, started_at=datetime.now(timezone.utc))
    return state.save(new_state)

@app.post("/api/session/stop", response_model=SessionState)
def stop_session():
    current = state.get()
    current.active = False
    current.stopped_at = datetime.now(timezone.utc)
    return state.save(current)

@app.post("/api/emergency-stop", response_model=SessionState)
def emergency_stop():
    current = state.get()
    current.active = False
    current.emergency_stop = True
    current.stopped_at = datetime.now(timezone.utc)
    return state.save(current)

@app.get("/api/session/status", response_model=SessionState)
def session_status():
    return state.get()

@app.get("/api/account/summary")
def account_summary():
    return engine.summary()

@app.get("/api/positions")
def positions():
    return {"items": engine.positions, "total": len(engine.positions)}

@app.get("/api/orders")
def orders():
    return {"items": engine.orders, "total": len(engine.orders)}

@app.get("/api/history")
def history():
    return {"items": engine.history, "total": len(engine.history)}
