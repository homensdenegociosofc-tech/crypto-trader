import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Crypto Trader Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root {
  --bg:#070707; --sidebar:#0b0b0b; --surface:#111; --surface2:#181818;
  --border:#292929; --text:#f5f5f5; --muted:#8d8d95; --primary:#e63946;
  --primary2:#b91c2b; --success:#22c55e; --warning:#f59e0b; --danger:#ef4444;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important}
html,body,button,input,textarea,select,label,[class*="css"]{font-family:Inter,Arial,sans-serif!important}
[data-testid="stHeader"]{background:rgba(7,7,7,.93)!important;border-bottom:1px solid #171717}
[data-testid="stMainBlockContainer"]{max-width:1500px!important;padding-top:2rem!important;padding-bottom:3rem!important}
#MainMenu,footer,[data-testid="stSidebarNav"]{display:none!important}
h1,h2,h3,h4,h5,h6{color:var(--text)!important} p,label{color:#d4d4d8!important}

/* Sidebar */
[data-testid="stSidebar"]{background:var(--sidebar)!important;border-right:1px solid var(--border)!important;min-width:300px!important;max-width:300px!important}
[data-testid="stSidebar"]>div:first-child{padding:1.15rem .9rem}
[data-testid="stSidebar"] hr{border-color:var(--border)!important}
.sidebar-title{text-align:center;color:var(--text)!important;font-weight:850;letter-spacing:.05em;margin:0 0 12px}
.sidebar-title strong{color:var(--primary)!important}
[data-testid="stRadio"]>div{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:5px}

/* Multiselect fechado */
div[data-testid="stMultiSelect"]>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;min-height:46px!important;box-shadow:none!important}
div[data-testid="stMultiSelect"]>div:focus-within{border-color:var(--primary)!important;box-shadow:0 0 0 3px rgba(230,57,70,.15)!important}
div[data-testid="stMultiSelect"] input{color:var(--text)!important;caret-color:var(--primary)!important}
div[data-testid="stMultiSelect"] input::placeholder{color:var(--muted)!important}
div[data-testid="stMultiSelect"] svg{fill:#d4d4d8!important}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"]{background:var(--primary)!important;border:1px solid var(--primary)!important;border-radius:6px!important;color:#fff!important;margin:3px!important}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span{color:#fff!important;font-weight:750!important}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg{fill:#fff!important}

/* Pop-up do multiselect: visível, escuro e acima da página */
div[data-baseweb="popover"]{z-index:999999!important}
div[data-baseweb="popover"]>div{background:#151515!important;border:1px solid #3a3a3a!important;border-radius:10px!important;box-shadow:0 18px 50px rgba(0,0,0,.75)!important;overflow:hidden!important}
div[data-baseweb="popover"] ul{background:#151515!important;padding:6px!important;max-height:340px!important;overflow-y:auto!important}
div[data-baseweb="popover"] li,div[data-baseweb="popover"] [role="option"]{background:#151515!important;color:#f5f5f5!important;border-radius:7px!important;min-height:42px!important;padding:9px 12px!important}
div[data-baseweb="popover"] li *,div[data-baseweb="popover"] [role="option"] *{color:#f5f5f5!important}
div[data-baseweb="popover"] li:hover,div[data-baseweb="popover"] [role="option"]:hover,div[data-baseweb="popover"] [role="option"][aria-selected="true"]{background:var(--primary)!important;color:#fff!important}
div[data-baseweb="popover"] li:hover *,div[data-baseweb="popover"] [role="option"]:hover *,div[data-baseweb="popover"] [role="option"][aria-selected="true"] *{color:#fff!important;font-weight:750!important}
div[data-baseweb="popover"] ul::-webkit-scrollbar{width:7px}
div[data-baseweb="popover"] ul::-webkit-scrollbar-track{background:#111}
div[data-baseweb="popover"] ul::-webkit-scrollbar-thumb{background:#4a4a4a;border-radius:10px}
div[data-baseweb="popover"] ul::-webkit-scrollbar-thumb:hover{background:var(--primary)}

/* Inputs e botões */
[data-testid="stNumberInput"]>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;overflow:hidden}
[data-testid="stNumberInput"] input{background:var(--surface)!important;color:var(--text)!important;border:none!important}
[data-testid="stNumberInput"] button{background:var(--surface2)!important;color:var(--text)!important;border-color:var(--border)!important}
.stButton>button{min-height:44px;background:var(--surface)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:9px!important;font-weight:750!important;transition:.18s ease!important}
.stButton>button:hover{background:var(--surface2)!important;border-color:var(--primary)!important;box-shadow:0 0 0 3px rgba(230,57,70,.15)!important;transform:translateY(-1px)}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,var(--primary),var(--primary2))!important;color:#fff!important;border-color:var(--primary)!important}

/* Cabeçalho, status e cards */
.crypto-title{color:var(--text)!important;font-size:2rem;font-weight:850;letter-spacing:-.04em}.crypto-title span{color:var(--primary)!important}
.crypto-subtitle{color:var(--muted)!important;font-size:.82rem;margin-top:7px}
.status-box{border-radius:9px;padding:10px;text-align:center;font-weight:800;font-size:.75rem}
.online{background:rgba(34,197,94,.10);border:1px solid var(--success);color:var(--success)!important}
.warning{background:rgba(245,158,11,.10);border:1px solid var(--warning);color:var(--warning)!important}
.offline{background:rgba(239,68,68,.10);border:1px solid var(--danger);color:var(--danger)!important}
.system-box{min-height:44px;display:flex;align-items:center;padding:0 14px;border-radius:9px;font-weight:750}
.running{background:rgba(34,197,94,.10);border-left:4px solid var(--success);color:#dcfce7!important}
.stopped{background:rgba(230,57,70,.10);border-left:4px solid var(--primary);color:#ffe4e6!important}
.metric-card{background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.012));border:1px solid var(--border);border-radius:12px;padding:18px 16px;min-height:112px;display:flex;flex-direction:column;justify-content:center;text-align:center;transition:.18s ease}
.metric-card:hover,.coin-card:hover{border-color:var(--primary);transform:translateY(-2px)}
.metric-title{font-size:.68rem;color:var(--muted)!important;text-transform:uppercase;letter-spacing:.07em;font-weight:800}
.metric-value{font-size:1.55rem;color:var(--text)!important;font-weight:850;margin-top:8px}.positive{color:var(--success)!important}.primary{color:var(--primary)!important}
.coin-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:17px;min-height:125px;margin-bottom:12px;transition:.18s ease}
.coin-name{color:#d4d4d8!important;font-weight:800;font-size:.76rem;letter-spacing:.05em}.coin-price{color:var(--text)!important;font-size:1.35rem;font-weight:850;margin:7px 0}.coin-up{color:var(--success)!important;font-weight:750;font-size:.79rem}.coin-down{color:var(--danger)!important;font-weight:750;font-size:.79rem}
.section-title{color:var(--text)!important;font-size:1.25rem;font-weight:800}.section-time{color:var(--muted)!important;font-size:.75rem;font-weight:400}.empty-box{background:var(--surface);border:1px solid var(--border);border-radius:9px;padding:15px;color:var(--muted)!important}
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:8px;border-bottom:1px solid var(--border)}
[data-testid="stTabs"] button[role="tab"]{color:#a1a1aa!important}[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{color:#fff!important;border-bottom-color:var(--primary)!important}
@media(max-width:900px){[data-testid="stSidebar"]{min-width:270px!important;max-width:270px!important}.crypto-title{font-size:1.55rem}}
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("robo_rodando", False)
st.session_state.setdefault("saldo_virtual", 1000.00)
st.session_state.setdefault("auto_update", True)

opcoes_ativos = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","LINKUSDT","AVAXUSDT","LTCUSDT","DOTUSDT","MATICUSDT","SHIBUSDT","TRXUSDT","UNIUSDT","ATOMUSDT","ETCUSDT","XLMUSDT","BCHUSDT","NEARUSDT"]
mapa_moedas = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","SOLUSDT":"solana","BNBUSDT":"binancecoin","XRPUSDT":"ripple","ADAUSDT":"cardano","DOGEUSDT":"dogecoin","LINKUSDT":"chainlink","AVAXUSDT":"avalanche-2","LTCUSDT":"litecoin","DOTUSDT":"polkadot","MATICUSDT":"matic-network","SHIBUSDT":"shiba-inu","TRXUSDT":"tron","UNIUSDT":"uniswap","ATOMUSDT":"cosmos","ETCUSDT":"ethereum-classic","XLMUSDT":"stellar","BCHUSDT":"bitcoin-cash","NEARUSDT":"near"}
mapa_inverso = {"bitcoin":"BTC","ethereum":"ETH","solana":"SOL","binancecoin":"BNB","ripple":"XRP","cardano":"ADA","dogecoin":"DOGE","chainlink":"LINK","avalanche-2":"AVAX","litecoin":"LTC","polkadot":"DOT","matic-network":"MATIC","shiba-inu":"SHIB","tron":"TRX","uniswap":"UNI","cosmos":"ATOM","ethereum-classic":"ETC","stellar":"XLM","bitcoin-cash":"BCH","near":"NEAR"}

@st.cache_data(ttl=15, show_spinner=False)
def get_market_data(coin_ids):
    if not coin_ids:
        return {}
    result = {}
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": ",".join(coin_ids), "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=8,
            headers={"accept":"application/json", "User-Agent":"CryptoTraderPro/1.0"},
        )
        res.raise_for_status()
        for cid, data in res.json().items():
            result[cid] = {"current_price": data.get("usd",0), "price_change_percentage_24h": data.get("usd_24h_change",0)}
        if result:
            return result
    except (requests.RequestException, ValueError, TypeError):
        pass
    try:
        symbols = [mapa_inverso[c] for c in coin_ids if c in mapa_inverso]
        if symbols:
            res = requests.get(
                "https://min-api.cryptocompare.com/data/pricemultifull",
                params={"fsyms": ",".join(symbols), "tsyms": "USD"},
                timeout=8,
                headers={"User-Agent":"CryptoTraderPro/1.0"},
            )
            res.raise_for_status()
            raw = res.json().get("RAW", {})
            for cid in coin_ids:
                sym = mapa_inverso.get(cid)
                usd = raw.get(sym, {}).get("USD", {}) if sym else {}
                if usd:
                    result[cid] = {"current_price": usd.get("PRICE",0), "price_change_percentage_24h": usd.get("CHANGEPCT24HOUR",0)}
    except (requests.RequestException, ValueError, TypeError):
        pass
    return result

with st.sidebar:
    st.markdown('<div class="sidebar-title">CRYPTO <strong>CONTROL</strong></div>', unsafe_allow_html=True)
    modo_visual = st.radio("Modo", ["Simulação","Observação","Real"], index=0, horizontal=True)
    if modo_visual == "Real":
        st.warning("Modo Real ainda não habilitado. O sistema continuará em Simulação.")
        modo = "Simulação"
    else:
        modo = modo_visual
    st.markdown("<hr>", unsafe_allow_html=True)
    ativos_selecionados = st.multiselect("Ativos:", opcoes_ativos, default=["BTCUSDT","ETHUSDT","SOLUSDT"], placeholder="Selecione os ativos")
    st.markdown("<hr>", unsafe_allow_html=True)
    meta_diaria = st.number_input("Meta (USDT)", min_value=0.0, value=50.0, step=10.0)
    perda_maxima = st.number_input("Perda máxima (USDT)", min_value=0.0, value=20.0, step=5.0)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.session_state.auto_update = st.toggle("🔄 Auto-Update", value=st.session_state.auto_update)

col_titulo, col_status = st.columns([3,1])
with col_titulo:
    st.markdown('<div class="crypto-title">Crypto Trader <span>Pro</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="crypto-subtitle">{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} &nbsp;•&nbsp; Ambiente: {modo}</div>', unsafe_allow_html=True)
with col_status:
    try:
        health = requests.get("https://crypto-trader-ztx7.onrender.com/health", timeout=4)
        if health.status_code == 200:
            st.markdown('<div class="status-box online">● MOTOR ONLINE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box warning">● MOTOR INSTÁVEL</div>', unsafe_allow_html=True)
    except requests.RequestException:
        st.markdown('<div class="status-box offline">● MOTOR OFFLINE</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col_start, col_stop, col_info = st.columns([1,1,2])
with col_start:
    if not st.session_state.robo_rodando:
        if st.button("▶ INICIAR SESSÃO", type="primary", use_container_width=True):
            st.session_state.robo_rodando = True
            st.rerun()
    else:
        st.button("● SESSÃO ATIVA", type="primary", disabled=True, use_container_width=True)
with col_stop:
    if st.button("🚨 EMERGÊNCIA", use_container_width=True):
        st.session_state.robo_rodando = False
        st.rerun()
with col_info:
    css = "running" if st.session_state.robo_rodando else "stopped"
    texto = "ROBÔ OPERANDO: analisando o mercado..." if st.session_state.robo_rodando else "SISTEMA PARADO"
    st.markdown(f'<div class="system-box {css}">{texto}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
m1,m2,m3,m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><div class="metric-title">Saldo virtual</div><div class="metric-value">$ {st.session_state.saldo_virtual:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown('<div class="metric-card"><div class="metric-title">Resultado aberto</div><div class="metric-value">$ 0.00</div></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="metric-card"><div class="metric-title">Resultado do dia</div><div class="metric-value positive">+ $ 12.50</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><div class="metric-title">Meta diária</div><div class="metric-value primary">$ {meta_diaria:.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
run_every = "15s" if st.session_state.auto_update else None

@st.fragment(run_every=run_every)
def render_market_prices(ativos):
    titulo, botao = st.columns([4,1])
    with titulo:
        st.markdown(f'<div class="section-title">Mercado em tempo real <span class="section-time">Atualizado às {datetime.now().strftime("%H:%M:%S")}</span></div>', unsafe_allow_html=True)
    with botao:
        if st.button("🔄 Atualizar", use_container_width=True, key="market_refresh"):
            st.cache_data.clear()
            st.rerun(scope="fragment")
    if not ativos:
        st.markdown('<div class="empty-box">Nenhum ativo selecionado.</div>', unsafe_allow_html=True)
        return
    dados = get_market_data([mapa_moedas[a] for a in ativos if a in mapa_moedas])
    cols = st.columns(4)
    for i, ativo in enumerate(ativos):
        item = dados.get(mapa_moedas.get(ativo), {})
        price = item.get("current_price",0) or 0
        change = item.get("price_change_percentage_24h",0) or 0
        if price == 0:
            price_display, change_display, delta_class = "---", "Aguardando cotação...", "coin-name"
        else:
            price_display = f"$ {price:,.2f}"
            change_display = f'{"▲" if change >= 0 else "▼"} {abs(change):.2f}% (24h)'
            delta_class = "coin-up" if change >= 0 else "coin-down"
        card = f'<div class="coin-card"><div class="coin-name">{ativo}</div><div class="coin-price">{price_display}</div><div class="{delta_class}">{change_display}</div></div>'
        with cols[i % 4]:
            st.markdown(card, unsafe_allow_html=True)

render_market_prices(ativos_selecionados)

st.markdown("<br>", unsafe_allow_html=True)
tab1,tab2,tab3,tab4 = st.tabs(["📊 Visão Geral","💼 Posições Abertas","📋 Ordens em Aberto","📜 Histórico"])
with tab1:
    st.info("Os gráficos de análise técnica aparecerão aqui na próxima fase.")
with tab2:
    if st.session_state.robo_rodando:
        st.dataframe(pd.DataFrame({"Ativo":["BTCUSDT","ETHUSDT"],"Direção":["LONG","LONG"],"Qtd":[0.005,0.1],"Preço Entrada":["$ 64,500.00","$ 1,800.00"],"Preço Atual":["$ 64,976.00","$ 1,817.37"],"PnL":["+$ 2.38","+$ 1.73"]}), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma posição aberta.")
with tab3:
    if st.session_state.robo_rodando:
        st.dataframe(pd.DataFrame({"Hora":["10:15:32"],"Ativo":["SOLUSDT"],"Tipo":["Limit Buy"],"Preço":["$ 70.00"],"Qtd":[10.0],"Status":["⏳ Aguardando"]}), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma ordem pendente.")
with tab4:
    st.info("O histórico aparecerá aqui.")
