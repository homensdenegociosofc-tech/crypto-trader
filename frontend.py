import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Crypto Trader Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

API_URL = "https://crypto-trader-ztx7.onrender.com"
REQUEST_TIMEOUT = 60

st.markdown("""
<style>
:root{--bg:#070707;--sidebar:#0b0b0b;--surface:#111;--surface2:#181818;--border:#292929;--text:#f5f5f5;--muted:#8d8d95;--primary:#e63946;--primary2:#b91c2b;--success:#22c55e;--warning:#f59e0b;--danger:#ef4444}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important}
html,body,button,input,textarea,select,label,[class*="css"]{font-family:Inter,Arial,sans-serif!important}
[data-testid="stHeader"]{background:rgba(7,7,7,.93)!important;border-bottom:1px solid #171717}
[data-testid="stMainBlockContainer"]{max-width:1500px!important;padding-top:2rem!important;padding-bottom:3rem!important}
#MainMenu,footer,[data-testid="stSidebarNav"]{display:none!important} h1,h2,h3,h4,h5,h6{color:var(--text)!important}p,label{color:#d4d4d8!important}
[data-testid="stSidebar"]{background:var(--sidebar)!important;border-right:1px solid var(--border)!important;min-width:300px!important;max-width:300px!important}
[data-testid="stSidebar"]>div:first-child{padding:1.15rem .9rem}[data-testid="stSidebar"] hr{border-color:var(--border)!important}
.sidebar-title{text-align:center;color:var(--text)!important;font-weight:850;letter-spacing:.05em;margin:0 0 12px}.sidebar-title strong{color:var(--primary)!important}
[data-testid="stRadio"]>div{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:5px}
div[data-testid="stMultiSelect"]>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;min-height:46px!important;box-shadow:none!important}
div[data-testid="stMultiSelect"]>div:focus-within{border-color:var(--primary)!important;box-shadow:0 0 0 3px rgba(230,57,70,.15)!important}
div[data-testid="stMultiSelect"] input{color:var(--text)!important}div[data-testid="stMultiSelect"] span[data-baseweb="tag"]{background:var(--primary)!important;border-radius:6px!important;color:#fff!important}div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span{color:#fff!important;font-weight:700!important}
div[data-baseweb="popover"]{z-index:999999!important}div[data-baseweb="popover"]>div,div[data-baseweb="popover"] ul{background:#151515!important}div[data-baseweb="popover"]>div{border:1px solid #3a3a3a!important;border-radius:10px!important;box-shadow:0 18px 50px rgba(0,0,0,.75)!important;overflow:hidden!important}div[data-baseweb="popover"] ul{padding:6px!important;max-height:340px!important;overflow-y:auto!important}
div[data-baseweb="popover"] li,div[data-baseweb="popover"] [role="option"]{background:#151515!important;color:#f5f5f5!important;border-radius:7px!important;min-height:42px!important;padding:9px 12px!important}div[data-baseweb="popover"] li *,div[data-baseweb="popover"] [role="option"] *{color:#f5f5f5!important}div[data-baseweb="popover"] li:hover,div[data-baseweb="popover"] [role="option"]:hover,div[data-baseweb="popover"] [role="option"][aria-selected="true"]{background:var(--primary)!important}
[data-testid="stNumberInput"]>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;overflow:hidden}[data-testid="stNumberInput"] input{background:var(--surface)!important;color:var(--text)!important;border:none!important}
.stButton>button{min-height:44px;background:var(--surface)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:9px!important;font-weight:750!important}.stButton>button:hover{background:var(--surface2)!important;border-color:var(--primary)!important;box-shadow:0 0 0 3px rgba(230,57,70,.15)!important}div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,var(--primary),var(--primary2))!important;color:#fff!important;border-color:var(--primary)!important}
.crypto-title{color:var(--text)!important;font-size:2rem;font-weight:850;letter-spacing:-.04em}.crypto-title span{color:var(--primary)!important}.crypto-subtitle{color:var(--muted)!important;font-size:.82rem;margin-top:7px}
.status-box{border-radius:9px;padding:10px;text-align:center;font-weight:800;font-size:.75rem}.online{background:rgba(34,197,94,.10);border:1px solid var(--success);color:var(--success)!important}.warning{background:rgba(245,158,11,.10);border:1px solid var(--warning);color:var(--warning)!important}.offline{background:rgba(239,68,68,.10);border:1px solid var(--danger);color:var(--danger)!important}
.system-box{min-height:44px;display:flex;align-items:center;padding:0 14px;border-radius:9px;font-weight:750}.running{background:rgba(34,197,94,.10);border-left:4px solid var(--success);color:#dcfce7!important}.stopped{background:rgba(230,57,70,.10);border-left:4px solid var(--primary);color:#ffe4e6!important}
.metric-card{background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.012));border:1px solid var(--border);border-radius:12px;padding:18px 16px;min-height:112px;display:flex;flex-direction:column;justify-content:center;text-align:center}.metric-title{font-size:.68rem;color:var(--muted)!important;text-transform:uppercase;letter-spacing:.07em;font-weight:800}.metric-value{font-size:1.55rem;color:var(--text)!important;font-weight:850;margin-top:8px}.positive{color:var(--success)!important}.primary{color:var(--primary)!important}
.coin-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:17px;min-height:125px;margin-bottom:12px}.coin-name{color:#d4d4d8!important;font-weight:800;font-size:.76rem}.coin-price{color:var(--text)!important;font-size:1.35rem;font-weight:850;margin:7px 0}.coin-up{color:var(--success)!important;font-weight:750}.coin-down{color:var(--danger)!important;font-weight:750}.section-title{color:var(--text)!important;font-size:1.25rem;font-weight:800}.section-time{color:var(--muted)!important;font-size:.75rem;font-weight:400}.empty-box{background:var(--surface);border:1px solid var(--border);border-radius:9px;padding:15px;color:var(--muted)!important}
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:8px;border-bottom:1px solid var(--border)}[data-testid="stTabs"] button[role="tab"]{color:#a1a1aa!important}[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{color:#fff!important;border-bottom-color:var(--primary)!important}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("auto_update", True)
st.session_state.setdefault("flash", None)

OPCOES_ATIVOS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","LINKUSDT","AVAXUSDT","LTCUSDT","DOTUSDT","MATICUSDT","SHIBUSDT","TRXUSDT","UNIUSDT","ATOMUSDT","ETCUSDT","XLMUSDT","BCHUSDT","NEARUSDT"]
MAPA_MOEDAS = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","SOLUSDT":"solana","BNBUSDT":"binancecoin","XRPUSDT":"ripple","ADAUSDT":"cardano","DOGEUSDT":"dogecoin","LINKUSDT":"chainlink","AVAXUSDT":"avalanche-2","LTCUSDT":"litecoin","DOTUSDT":"polkadot","MATICUSDT":"matic-network","SHIBUSDT":"shiba-inu","TRXUSDT":"tron","UNIUSDT":"uniswap","ATOMUSDT":"cosmos","ETCUSDT":"ethereum-classic","XLMUSDT":"stellar","BCHUSDT":"bitcoin-cash","NEARUSDT":"near"}
MAPA_INVERSO = {v:k.replace("USDT","") for k,v in MAPA_MOEDAS.items()}

def api_request(method, path, json=None):
    try:
        response = requests.request(method, f"{API_URL}{path}", json=json, timeout=REQUEST_TIMEOUT)
        if response.status_code >= 400:
            try: detail = response.json().get("detail", response.text)
            except ValueError: detail = response.text
            return None, f"Backend respondeu {response.status_code}: {detail}"
        return response.json(), None
    except requests.Timeout:
        return None, "O Render demorou para responder. Aguarde alguns segundos e tente novamente."
    except requests.RequestException as exc:
        return None, f"Não foi possível conectar ao motor: {type(exc).__name__}"

@st.cache_data(ttl=10, show_spinner=False)
def get_backend_snapshot():
    status, e1 = api_request("GET", "/api/session/status")
    summary, e2 = api_request("GET", "/api/account/summary")
    positions, e3 = api_request("GET", "/api/positions")
    orders, e4 = api_request("GET", "/api/orders")
    history, e5 = api_request("GET", "/api/history")
    error = next((e for e in [e1,e2,e3,e4,e5] if e), None)
    return status or {}, summary or {}, positions or {"items":[]}, orders or {"items":[]}, history or {"items":[]}, error

@st.cache_data(ttl=15, show_spinner=False)
def get_market_data(coin_ids):
    if not coin_ids: return {}
    result = {}
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids":",".join(coin_ids),"vs_currencies":"usd","include_24hr_change":"true"}, timeout=8, headers={"User-Agent":"CryptoTraderPro/1.0"})
        res.raise_for_status()
        for cid,data in res.json().items(): result[cid]={"current_price":data.get("usd",0),"price_change_percentage_24h":data.get("usd_24h_change",0)}
        if result: return result
    except (requests.RequestException,ValueError,TypeError): pass
    try:
        symbols=[MAPA_INVERSO[c] for c in coin_ids if c in MAPA_INVERSO]
        res=requests.get("https://min-api.cryptocompare.com/data/pricemultifull",params={"fsyms":",".join(symbols),"tsyms":"USD"},timeout=8)
        res.raise_for_status(); raw=res.json().get("RAW",{})
        for cid in coin_ids:
            sym=MAPA_INVERSO.get(cid); usd=raw.get(sym,{}).get("USD",{}) if sym else {}
            if usd: result[cid]={"current_price":usd.get("PRICE",0),"price_change_percentage_24h":usd.get("CHANGEPCT24HOUR",0)}
    except (requests.RequestException,ValueError,TypeError): pass
    return result

status, summary, positions_data, orders_data, history_data, backend_error = get_backend_snapshot()
session_active = bool(status.get("active", False))

with st.sidebar:
    st.markdown('<div class="sidebar-title">CRYPTO <strong>CONTROL</strong></div>', unsafe_allow_html=True)
    modo_visual = st.radio("Modo", ["Simulação","Observação","Real"], index=0, horizontal=True)
    if modo_visual == "Real": st.warning("Modo Real bloqueado nesta fase."); modo="Simulação"
    else: modo=modo_visual
    st.markdown("<hr>", unsafe_allow_html=True)
    default_assets = status.get("assets") or ["BTCUSDT","ETHUSDT","SOLUSDT"]
    ativos_selecionados = st.multiselect("Ativos:", OPCOES_ATIVOS, default=[a for a in default_assets if a in OPCOES_ATIVOS])
    st.markdown("<hr>", unsafe_allow_html=True)
    meta_diaria = st.number_input("Meta (USDT)", min_value=0.0, value=float(status.get("daily_target_usdt",50)), step=10.0)
    perda_maxima = st.number_input("Perda máxima (USDT)", min_value=1.0, value=float(status.get("max_daily_loss_usdt",20)), step=5.0)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.session_state.auto_update = st.toggle("🔄 Auto-Update", value=st.session_state.auto_update)

col_titulo,col_status=st.columns([3,1])
with col_titulo:
    st.markdown('<div class="crypto-title">Crypto Trader <span>Pro</span></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="crypto-subtitle">{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} &nbsp;•&nbsp; Ambiente: {modo}</div>',unsafe_allow_html=True)
with col_status:
    if backend_error: st.markdown('<div class="status-box offline">● MOTOR OFFLINE</div>',unsafe_allow_html=True)
    else: st.markdown('<div class="status-box online">● MOTOR ONLINE</div>',unsafe_allow_html=True)

if st.session_state.flash:
    kind,message=st.session_state.flash; getattr(st,kind)(message); st.session_state.flash=None
if backend_error: st.error(backend_error)

st.markdown("<br>",unsafe_allow_html=True)
col_start,col_stop,col_info=st.columns([1,1,2])
with col_start:
    if not session_active:
        if st.button("▶ INICIAR SESSÃO",type="primary",use_container_width=True,disabled=bool(backend_error)):
            if not ativos_selecionados: st.warning("Selecione pelo menos um ativo.")
            else:
                payload={"mode":modo,"assets":ativos_selecionados,"daily_target_usdt":meta_diaria,"max_daily_loss_usdt":perda_maxima}
                with st.spinner("Iniciando sessão no backend..."):
                    data,error=api_request("POST","/api/session/start",json=payload)
                st.cache_data.clear(); st.session_state.flash=("error",error) if error else ("success","Sessão iniciada no backend."); st.rerun()
    else: st.button("● SESSÃO ATIVA",type="primary",disabled=True,use_container_width=True)
with col_stop:
    if st.button("🚨 EMERGÊNCIA",use_container_width=True,disabled=bool(backend_error)):
        with st.spinner("Acionando parada de emergência..."):
            data,error=api_request("POST","/api/emergency-stop")
        st.cache_data.clear(); st.session_state.flash=("error",error) if error else ("warning","Parada de emergência acionada."); st.rerun()
with col_info:
    css="running" if session_active else "stopped"
    texto="ROBÔ OPERANDO: sessão Paper Trading ativa" if session_active else "SISTEMA PARADO"
    st.markdown(f'<div class="system-box {css}">{texto}</div>',unsafe_allow_html=True)

balance=float(summary.get("balance",1000)); open_pnl=float(summary.get("open_pnl",0)); daily_pnl=float(summary.get("daily_pnl",0))
st.markdown("<br>",unsafe_allow_html=True)
m1,m2,m3,m4=st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><div class="metric-title">Saldo virtual</div><div class="metric-value">$ {balance:,.2f}</div></div>',unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card"><div class="metric-title">Resultado aberto</div><div class="metric-value">$ {open_pnl:,.2f}</div></div>',unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card"><div class="metric-title">Resultado do dia</div><div class="metric-value positive">$ {daily_pnl:,.2f}</div></div>',unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><div class="metric-title">Meta diária</div><div class="metric-value primary">$ {meta_diaria:,.2f}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
run_every="15s" if st.session_state.auto_update else None
@st.fragment(run_every=run_every)
def render_market_prices(ativos):
    titulo,botao=st.columns([4,1])
    with titulo: st.markdown(f'<div class="section-title">Mercado em tempo real <span class="section-time">Atualizado às {datetime.now().strftime("%H:%M:%S")}</span></div>',unsafe_allow_html=True)
    with botao:
        if st.button("🔄 Atualizar",use_container_width=True,key="market_refresh"): st.cache_data.clear(); st.rerun(scope="fragment")
    if not ativos: st.markdown('<div class="empty-box">Nenhum ativo selecionado.</div>',unsafe_allow_html=True); return
    dados=get_market_data([MAPA_MOEDAS[a] for a in ativos if a in MAPA_MOEDAS]); cols=st.columns(4)
    for i,ativo in enumerate(ativos):
        item=dados.get(MAPA_MOEDAS.get(ativo),{}); price=item.get("current_price",0) or 0; change=item.get("price_change_percentage_24h",0) or 0
        if price==0: price_display,change_display,delta_class="---","Aguardando cotação...","coin-name"
        else: price_display=f"$ {price:,.2f}"; change_display=f'{"▲" if change>=0 else "▼"} {abs(change):.2f}% (24h)'; delta_class="coin-up" if change>=0 else "coin-down"
        with cols[i%4]: st.markdown(f'<div class="coin-card"><div class="coin-name">{ativo}</div><div class="coin-price">{price_display}</div><div class="{delta_class}">{change_display}</div></div>',unsafe_allow_html=True)
render_market_prices(ativos_selecionados)

st.markdown("<br>",unsafe_allow_html=True)
tab1,tab2,tab3,tab4=st.tabs(["📊 Visão Geral","💼 Posições Abertas","📋 Ordens em Aberto","📜 Histórico"])
with tab1:
    st.info("Backend conectado. Indicadores e decisões da IA serão adicionados na próxima fase.")
with tab2:
    items=positions_data.get("items",[])
    if items: st.dataframe(pd.DataFrame(items),use_container_width=True,hide_index=True)
    else: st.info("Nenhuma posição aberta no backend.")
with tab3:
    items=orders_data.get("items",[])
    if items: st.dataframe(pd.DataFrame(items),use_container_width=True,hide_index=True)
    else: st.info("Nenhuma ordem registrada no backend.")
with tab4:
    items=history_data.get("items",[])
    if items: st.dataframe(pd.DataFrame(items),use_container_width=True,hide_index=True)
    else: st.info("Nenhum evento no histórico do backend.")
