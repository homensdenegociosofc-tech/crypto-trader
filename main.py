from datetime import datetime,timezone
import asyncio, psycopg2
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from schemas import SessionStart,SessionState,AnalysisRequest
from state_manager import StateManager
from services.paper_executor import PaperTradingEngine
from services.analysis_service import AnalysisService
from services.market_data import MarketDataError
s=get_settings(); app=FastAPI(title=s.app_name,version="0.3.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
state=StateManager(); engine=PaperTradingEngine(); analysis=AnalysisService()
@app.get("/")
def root(): return {"status":"online","version":"0.3.0","mode":"paper_trading","automatic_execution":False}
@app.get("/health")
def health():
    db="não configurado"
    if s.database_url:
        try: c=psycopg2.connect(s.database_url,connect_timeout=5); c.close(); db="conectado"
        except Exception: db="indisponível"
    return {"api":"ok","database":db,"redis":state.health(),"ai_provider":s.ai_provider,"real_trading_enabled":False,"analysis_engine":"ready","timestamp":datetime.now(timezone.utc).isoformat()}
@app.post("/api/session/start",response_model=SessionState)
def start(p:SessionStart):
    cur=state.get()
    if cur.active: raise HTTPException(409,"Já existe uma sessão ativa")
    return state.save(SessionState(active=True,emergency_stop=False,mode=p.mode,assets=p.assets,daily_target_usdt=p.daily_target_usdt,max_daily_loss_usdt=p.max_daily_loss_usdt,started_at=datetime.now(timezone.utc)))
@app.post("/api/session/stop",response_model=SessionState)
def stop():
    cur=state.get(); cur.active=False; cur.stopped_at=datetime.now(timezone.utc); return state.save(cur)
@app.post("/api/emergency-stop",response_model=SessionState)
def emergency():
    cur=state.get(); cur.active=False; cur.emergency_stop=True; cur.stopped_at=datetime.now(timezone.utc); return state.save(cur)
@app.get("/api/session/status",response_model=SessionState)
def session_status(): return state.get()
@app.get("/api/account/summary")
def summary(): return engine.summary()
@app.get("/api/positions")
def positions(): return {"items":engine.positions,"total":len(engine.positions)}
@app.get("/api/orders")
def orders(): return {"items":engine.orders,"total":len(engine.orders)}
@app.get("/api/history")
def history(): return {"items":engine.history,"total":len(engine.history)}
@app.get("/api/analysis/{symbol}")
async def analyze_symbol(symbol:str,interval:str="15m"):
    try:return await analysis.analyze(symbol.upper(),interval,s.analysis_candle_limit)
    except (MarketDataError,ValueError) as exc: raise HTTPException(503,str(exc))
@app.post("/api/analysis")
async def analyze_batch(p:AnalysisRequest):
    results=await asyncio.gather(*(analysis.analyze(x,p.interval,s.analysis_candle_limit) for x in p.symbols),return_exceptions=True)
    items=[]
    for symbol,result in zip(p.symbols,results):
        items.append({"symbol":symbol,"error":str(result)}) if isinstance(result,Exception) else items.append(result)
    return {"items":items,"total":len(items),"execution_enabled":False}
