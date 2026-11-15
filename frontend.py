import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Crypto Trader Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #050505; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}

    h1, h2, h3, h4, p, span, div { color: #E0E0E0 !important; }
    h1 { color: #FF8C00 !important; font-weight: 800; font-size: 2rem !important; margin-bottom: 0px !important;}
    
    /* Sidebar Super Compacta */
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #222; min-width: 260px !important; max-width: 260px !important; }
    [data-testid="stSidebar"] .block-container { padding: 10px !important; }
    
    /* Dropdown Correto */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: #FFF !important; border: 1px solid #333 !important; }
    div[data-baseweb="popover"] ul { background-color: #111 !important; }
    div[data-baseweb="popover"] li { color: #FFF !important; font-size: 14px; }
    div[data-baseweb="popover"] li:hover { background-color: #FF8C00 !important; color: #000 !important; }
    span[data-baseweb="tag"] { background-color: #FF8C00 !important; color: #000 !important; }

    /* Cards */
    .metric-card { background: linear-gradient(145deg, #121212, #0a0a0a); border: 1px solid #222; border-radius: 10px; padding: 15px; text-align: center; }
    .metric-title { font-size: 11px; color: #888 !important; text-transform: uppercase; font-weight: 700;}
    .metric-value { font-size: 22px; color: #FF8C00 !important; font-weight: 800; margin: 5px 0; }
    
    .coin-card { background-color: #111; border: 1px solid #222; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
    .coin-name { font-weight: 700; font-size: 15px; color: #FFF !important; }
    .coin-price { font-size: 20px; font-weight: 800; color: #FFF !important; }
    .coin-up { color: #1DB954 !important; font-weight: 600; font-size: 13px;}
    .coin-down { color: #E50914 !important; font-weight: 600; font-size: 13px;}

    /* Botões */
    .stButton>button { background-color: #121212; color: #FF8C00; border: 1px solid #FF8C00; font-weight: 600; border-radius: 6px; font-size: 14px; transition: all 0.3s; }
    .stButton>button:hover { background-color: #FF8C00; color: #000; box-shadow: 0 0 10px rgba(255,140,0,0.4); }
    div[data-testid="stButton"] button[kind="primary"] { background: linear-gradient(90deg, #1DB954, #169c46); color: white; border: none; }
    div[data-testid="stButton"] button[kind="secondary"] { background: linear-gradient(90deg, #E50914, #b80710); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO ---
if 'robo_rodando' not in st.session_state: st.session_state.robo_rodando = False
if 'saldo_virtual' not in st.session_state: st.session_state.saldo_virtual = 1000.00
if 'auto_update' not in st.session_state: st.session_state.auto_update = True

# --- MAPEAMENTO ---
opcoes_ativos = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "LTCUSDT", "DOTUSDT", "MATICUSDT", "SHIBUSDT", "TRXUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT", "XLMUSDT", "BCHUSDT", "NEARUSDT"]
mapa_moedas = {"BTCUSDT": "bitcoin", "ETHUSDT": "ethereum", "SOLUSDT": "solana", "BNBUSDT": "binancecoin", "XRPUSDT": "ripple", "ADAUSDT": "cardano", "DOGEUSDT": "dogecoin", "LINKUSDT": "chainlink", "AVAXUSDT": "avalanche-2", "LTCUSDT": "litecoin", "DOTUSDT": "polkadot", "MATICUSDT": "matic-network", "SHIBUSDT": "shiba-inu", "TRXUSDT": "tron", "UNIUSDT": "uniswap", "ATOMUSDT": "cosmos", "ETCUSDT": "ethereum-classic", "XLMUSDT": "stellar", "BCHUSDT": "bitcoin-cash", "NEARUSDT": "near"}

@st.cache_data(ttl=10)
def get_market_data(coin_ids):
    if not coin_ids: return {}
    try:
        ids = ",".join(coin_ids)
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h"
        res = requests.get(url, timeout=5)
        if res.status_code == 200: return {item['id']: item for item in res.json()}
        return {}
    except: return {}

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h4 style='text-align: center; margin-bottom: 10px; color:#FF8C00 !important;'>⚙️ PAINEL</h4>", unsafe_allow_html=True)
    modo = st.radio("Modo", ["Simulação", "Observação", "Real"], index=0, horizontal=True)
    if modo == "Real": modo = "Simulação"
    
    st.markdown("<hr style='margin: 5px 0; border-color: #333;'>", unsafe_allow_html=True)
    ativos_selecionados = st.multiselect("Ativos:", options=opcoes_ativos, default=["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    
    st.markdown("<hr style='margin: 5px 0; border-color: #333;'>", unsafe_allow_html=True)
    meta_diaria = st.number_input("Meta (USDT)", value=50.0, step=10.0)
    perda_maxima = st.number_input("Perda (USDT)", value=20.0, step=5.0)
    
    st.markdown("<hr style='margin: 5px 0; border-color: #333;'>", unsafe_allow_html=True)
    st.session_state.auto_update = st.toggle("🔄 Auto-Update (10s)", value=True, help="Atualiza apenas os preços sem travar a tela.")

# --- CABEÇALHO ---
col_titulo, col_status_api = st.columns([3, 1])
with col_titulo:
    st.markdown("<h1>⚡ Crypto Trader Terminal Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #888; font-size: 13px;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Modo: {modo}</span>", unsafe_allow_html=True)

with col_status_api:
    try:
        response = requests.get("https://crypto-trader-ztx7.onrender.com/health", timeout=3)
        if response.status_code == 200:
            st.markdown("<div style='background: rgba(29,185,84,0.1); border: 1px solid #1DB954; border-radius: 6px; padding: 6px; text-align: center; color: #1DB954; font-weight: 600; font-size: 12px;'>● MOTOR ONLINE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background: rgba(255,140,0,0.1); border: 1px solid #FF8C00; border-radius: 6px; padding: 6px; text-align: center; color: #FF8C00; font-weight: 600; font-size: 12px;'>● MOTOR INSTÁVEL</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div style='background: rgba(229,9,20,0.1); border: 1px solid #E50914; border-radius: 6px; padding: 6px; text-align: center; color: #E50914; font-weight: 600; font-size: 12px;'>● MOTOR OFFLINE</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- BOTÕES DE CONTROLE ---
col_btn_start, col_btn_stop, col_info = st.columns([1, 1, 2])
with col_btn_start:
    if not st.session_state.robo_rodando:
        if st.button("▶ INICIAR SESSÃO", type="primary", use_container_width=True):
            st.session_state.robo_rodando = True
            st.rerun()
    else:
        st.button("🟢 SESSÃO ATIVA", type="primary", disabled=True, use_container_width=True)
with col_btn_stop:
    if st.button("🚨 EMERGÊNCIA", type="secondary", use_container_width=True):
        st.session_state.robo_rodando = False
        st.error("KILL SWITCH ACIONADO!")
        st.rerun()
with col_info:
    if st.session_state.robo_rodando:
        st.markdown("<div style='background-color: rgba(29,185,84,0.1); border-left: 4px solid #1DB954; padding: 8px; border-radius: 4px;'><span style='color: #1DB954; font-weight: 600;'>🤖 ROBÔ OPERANDO:</span> Analisando o mercado...</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: rgba(255,140,0,0.1); border-left: 4px solid #FF8C00; padding: 8px; border-radius: 4px;'><span style='color: #FF8C00; font-weight: 600;'>⚠️ SISTEMA PARADO</span></div>", unsafe_allow_html=True)

# --- MÉTRICAS ---
st.markdown("<br>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card"><div class="metric-title">Saldo Virtual</div><div class="metric-value">$ {st.session_state.saldo_virtual:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown('<div class="metric-card"><div class="metric-title">Resultado Aberto</div><div class="metric-value">$ 0.00</div></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="metric-card"><div class="metric-title">Resultado do Dia</div><div class="metric-value" style="color: #1DB954 !important;">+ $ 12.50</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card"><div class="metric-title">Meta Diária</div><div class="metric-value">$ {meta_diaria:.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# FRAGMENTO PROFISSIONAL: Atualiza APENAS esta área a cada 10 segundos
# =====================================================================
# O run_every só é ativado se o usuário ligar o toggle na sidebar
tempo_atualizacao = "10s" if st.session_state.auto_update else None

@st.fragment(run_every=tempo_atualizacao)
def render_market_prices(ativos):
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h4 style='margin-bottom:0;'>Mercado em Tempo Real <span style='font-size: 12px; color: #888; font-weight: 400;'>Atualizado às {datetime.now().strftime('%H:%M:%S')}</span></h4>", unsafe_allow_html=True)
    with col_btn:
        if st.button("🔄 Forçar Atualização", use_container_width=True):
            st.cache_data.clear()
            st.rerun(scope="fragment") # Recarrega APENAS este bloco
            
    if not ativos:
        st.info("Nenhum ativo selecionado. Use a barra lateral para buscar e adicionar moedas.")
        return

    ids_para_buscar = [mapa_moedas[a] for a in ativos if a in mapa_moedas]
    market_data = get_market_data(ids_para_buscar)
    
    cols = st.columns(4)
    for i, ativo in enumerate(ativos):
        col_idx = i % 4
        coin_id = mapa_moedas.get(ativo)
        data = market_data.get(coin_id, {})
        
        price = data.get("current_price", 0.0)
        change = data.get("price_change_percentage_24h", 0.0) or 0.0
        
        seta = "▲" if change >= 0 else "▼"
        classe_delta = "coin-up" if change >= 0 else "coin-down"

        with cols[col_idx]:
            st.markdown(f"""
            <div class="coin-card">
                <div class="coin-name">{ativo}</div>
                <div class="coin-price">$ {price:,.2f}</div>
                <div class="{classe_delta}">{seta} {abs(change):.2f}% (24h)</div>
            </div>
            """, unsafe_allow_html=True)

# Chama a função do fragmento
render_market_prices(ativos_selecionados)

# --- ABAS ---
st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Posições Abertas", "📋 Ordens em Aberto", "📜 Histórico"])

with tab1:
    st.info("Os gráficos de análise técnica aparecerão aqui na próxima fase.")
with tab2:
    if st.session_state.robo_rodando:
        st.dataframe(pd.DataFrame({"Ativo": ["BTCUSDT", "ETHUSDT"],"Direção": ["LONG", "LONG"],"Qtd": [0.005, 0.1],"Preço Entrada": ["$ 64,500.00", "$ 1,800.00"],"Preço Atual": ["$ 64,976.00", "$ 1,817.37"],"PnL": ["+$ 2.38", "+$ 1.73"]}), use_container_width=True, hide_index=True)
    else: st.info("Nenhuma posição aberta.")
with tab3:
    if st.session_state.robo_rodando:
        st.dataframe(pd.DataFrame({"Hora": ["10:15:32"],"Ativo": ["SOLUSDT"],"Tipo": ["Limit Buy"],"Preço": ["$ 70.00"],"Qtd": [10.0],"Status": ["⏳ Aguardando"]}), use_container_width=True, hide_index=True)
    else: st.info("Nenhuma ordem pendente.")
with tab4:
    st.info("O histórico aparecerá aqui.")
