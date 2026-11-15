import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Crypto Trader Pro", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- CSS PREMIUM (DASHBOARD PROFISSIONAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #050505; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    h1, h2, h3, h4, p, span, div { color: #E0E0E0 !important; }
    h1 { color: #FF8C00 !important; font-weight: 800; letter-spacing: -1px; font-size: 2rem !important; margin-bottom: 0px !important;}
    
    [data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #222; min-width: 280px !important; max-width: 280px !important; }
    [data-testid="stSidebar"] .block-container { padding: 1rem !important; }
    [data-testid="stSidebar"] .stRadio label { font-size: 14px; }
    [data-testid="stSidebar"] .stNumberInput input { font-size: 14px; padding: 4px; }
    
    /* Cards de Métricas do Topo */
    .metric-card {
        background: linear-gradient(145deg, #121212, #0a0a0a);
        border: 1px solid #222;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        text-align: center;
    }
    .metric-title { font-size: 12px; color: #888 !important; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;}
    .metric-value { font-size: 24px; color: #FF8C00 !important; font-weight: 800; margin: 5px 0; }
    .metric-delta { font-size: 12px; font-weight: 600; }

    /* Botões */
    .stButton>button {
        background-color: #121212; color: #FF8C00;
        border: 1px solid #FF8C00; font-weight: 600;
        border-radius: 6px; height: 40px; font-size: 14px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #FF8C00; color: #000; box-shadow: 0 0 10px rgba(255,140,0,0.4); }
    
    div[data-testid="stButton"] button[kind="primary"] { background: linear-gradient(90deg, #1DB954, #169c46); color: white; border: none; }
    div[data-testid="stButton"] button[kind="primary"]:hover { box-shadow: 0 0 15px rgba(29,185,84,0.6); }
    
    div[data-testid="stButton"] button[kind="secondary"] { background: linear-gradient(90deg, #E50914, #b80710); color: white; border: none; }
    div[data-testid="stButton"] button[kind="secondary"]:hover { box-shadow: 0 0 15px rgba(229,9,20,0.6); }

    /* Estilo dos Cards de Moedas */
    .coin-card {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .coin-name { font-weight: 700; font-size: 16px; color: #FFF !important; margin-bottom: 5px;}
    .coin-price { font-size: 22px; font-weight: 800; color: #FFF !important; }
    .coin-up { color: #1DB954 !important; font-weight: 600; font-size: 14px;}
    .coin-down { color: #E50914 !important; font-weight: 600; font-size: 14px;}
    
    [data-testid="stDataFrame"] { border: 1px solid #222; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- BUSCA DE PREÇOS E VARIAÇÃO (MARKETS) ---
@st.cache_data(ttl=30)
def get_market_data(coin_ids):
    if not coin_ids: return {}
    try:
        ids = ",".join(coin_ids)
        # Usando a rota /coins/markets que traz a variação de 24h
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            # Transforma a lista num dicionário pra facilitar a busca
            return {item['id']: item for item in data}
        return {}
    except:
        return {}

# --- INICIALIZAÇÃO DO ESTADO ---
if 'robo_rodando' not in st.session_state: st.session_state.robo_rodando = False
if 'saldo_virtual' not in st.session_state: st.session_state.saldo_virtual = 1000.00

# --- MAPEAMENTO ---
opcoes_ativos = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT", "LTCUSDT",
    "DOTUSDT", "MATICUSDT", "SHIBUSDT", "TRXUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT", "XLMUSDT", "BCHUSDT", "NEARUSDT",
    "APTUSDT", "OPUSDT", "ARBUSDT", "FILUSDT", "LDOUSDT", "VETUSDT", "ICPUSDT", "HBARUSDT", "IMXUSDT", "RNDRUSDT"
]
mapa_moedas = {
    "BTCUSDT": "bitcoin", "ETHUSDT": "ethereum", "SOLUSDT": "solana", "BNBUSDT": "binancecoin", 
    "XRPUSDT": "ripple", "ADAUSDT": "cardano", "DOGEUSDT": "dogecoin", "LINKUSDT": "chainlink", 
    "AVAXUSDT": "avalanche-2", "LTCUSDT": "litecoin", "DOTUSDT": "polkadot", "MATICUSDT": "matic-network",
    "SHIBUSDT": "shiba-inu", "TRXUSDT": "tron", "UNIUSDT": "uniswap", "ATOMUSDT": "cosmos", 
    "ETCUSDT": "ethereum-classic", "XLMUSDT": "stellar", "BCHUSDT": "bitcoin-cash", "NEARUSDT": "near",
    "APTUSDT": "aptos", "OPUSDT": "optimism", "ARBUSDT": "arbitrum", "FILUSDT": "filecoin",
    "LDOUSDT": "lido-dao", "VETUSDT": "vechain", "ICPUSDT": "internet-computer", "HBARUSDT": "hedera-hashgraph"
}

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>⚙️ CONFIGURAÇÕES</h3>", unsafe_allow_html=True)
    
    st.markdown("**MODO DE OPERAÇÃO**")
    modo = st.radio("", ["Simulação", "Observação", "Real (Bloqueado)"], index=0, label_visibility="collapsed")
    if modo == "Real (Bloqueado)":
        st.error("🔒 Requer API Keys.")
        modo = "Simulação"
        
    st.markdown("<hr style='margin: 10px 0; border-color: #333;'>", unsafe_allow_html=True)
    
    st.markdown("**BUSCAR E MONITORAR ATIVOS**")
    ativos_selecionados = st.multiselect(
        "Buscar par (ex: BTC, ETH):", 
        options=opcoes_ativos,
        default=["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='margin: 10px 0; border-color: #333;'>", unsafe_allow_html=True)
    
    st.markdown("**GESTÃO DE RISCO (DIÁRIO)**")
    meta_diaria = st.number_input("Meta (USDT)", value=50.0, step=10.0)
    perda_maxima = st.number_input("Perda (USDT)", value=20.0, step=5.0)

# --- CABEÇALHO E STATUS (SEMPRE VISÍVEL) ---
col_titulo, col_status_api = st.columns([3, 1])

with col_titulo:
    st.markdown("<h1>⚡ Crypto Trader Terminal Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #888; font-size: 14px;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Modo: {modo}</span>", unsafe_allow_html=True)

with col_status_api:
    # Status do UptimeRobot/Render (Simulado no visual)
    try:
        api_url = "https://crypto-trader-ztx7.onrender.com/health"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            st.markdown("<div style='background: rgba(29,185,84,0.15); border: 1px solid #1DB954; border-radius: 6px; padding: 8px; text-align: center; color: #1DB954; font-weight: 600;'>● MOTOR ONLINE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background: rgba(255,140,0,0.15); border: 1px solid #FF8C00; border-radius: 6px; padding: 8px; text-align: center; color: #FF8C00; font-weight: 600;'>● MOTOR INSTÁVEL</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div style='background: rgba(229,9,20,0.15); border: 1px solid #E50914; border-radius: 6px; padding: 8px; text-align: center; color: #E50914; font-weight: 600;'>● MOTOR OFFLINE</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PAINEL DE CONTROLE ---
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
        time.sleep(1)
        st.rerun()

with col_info:
    if st.session_state.robo_rodando:
        st.markdown("<div style='background-color: rgba(29,185,84,0.1); border-left: 4px solid #1DB954; padding: 10px; border-radius: 4px;'><span style='color: #1DB954; font-weight: 600;'>🤖 ROBÔ OPERANDO:</span> Analisando o mercado em busca de oportunidades nos ativos selecionados.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color: rgba(255,140,0,0.1); border-left: 4px solid #FF8C00; padding: 10px; border-radius: 4px;'><span style='color: #FF8C00; font-weight: 600;'>⚠️ SISTEMA PARADO:</span> Configure o risco ao lado e clique em Iniciar.</div>", unsafe_allow_html=True)

st.divider()

# --- MÉTRICAS PRINCIPAIS ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Saldo Virtual</div><div class="metric-value">$ {st.session_state.saldo_virtual:,.2f}</div><div class="metric-delta" style="color: #1DB954;">↑ +0.00% hoje</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><div class="metric-title">Resultado Aberto</div><div class="metric-value">$ 0.00</div><div class="metric-delta" style="color: #1DB954;">↑ 0.00%</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><div class="metric-title">Resultado do Dia</div><div class="metric-value" style="color: #1DB954 !important;">+ $ 12.50</div><div class="metric-delta" style="color: #1DB954;">↑ +1.25%</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Meta Diária</div><div class="metric-value">$ {meta_diaria:.2f}</div><div class="metric-delta" style="color: #FF8C00;">Restam $ {meta_diaria - 12.50:.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br><h4>Mercado em Tempo Real</h4>", unsafe_allow_html=True)

# --- ÁREA DE COTAÇÕES (ESTILO UPTIMEROBOT) ---
ids_para_buscar = [mapa_moedas[a] for a in ativos_selecionados if a in mapa_moedas]
market_data = get_market_data(ids_para_buscar)

if not ativos_selecionados:
    st.info("Nenhum ativo selecionado. Use a barra lateral para buscar e adicionar moedas.")
else:
    # Cria no máximo 4 colunas por linha para ficar bonito
    cols = st.columns(4)
    for i, ativo in enumerate(ativos_selecionados):
        col_idx = i % 4
        coin_id = mapa_moedas.get(ativo)
        data = market_data.get(coin_id, {})
        
        price = data.get("current_price", 0.0)
        change = data.get("price_change_percentage_24h", 0.0)
        
        # Define cor e seta baseado na variação de 24h
        if change is not None and change > 0:
            cor = "#1DB954"
            seta = "▲"
            classe_delta = "coin-up"
        else:
            cor = "#E50914"
            seta = "▼"
            classe_delta = "coin-down"
            if change is None: change = 0.0

        with cols[col_idx]:
            st.markdown(f"""
            <div class="coin-card">
                <div class="coin-name">{ativo}</div>
                <div class="coin-price">$ {price:,.2f}</div>
                <div class="{classe_delta}">{seta} {abs(change):.2f}% (24h)</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ABAS DO SISTEMA ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Posições Abertas", "📋 Ordens em Aberto", "📜 Histórico"])

with tab1:
    st.info("Utilize a aba de cotações acima para acompanhar o mercado. Os gráficos de análise técnica aparecerão aqui em breve.")

with tab2:
    if st.session_state.robo_rodando:
        df_posicoes = pd.DataFrame({
            "Ativo": ["BTCUSDT", "ETHUSDT"],
            "Direção": ["LONG", "LONG"],
            "Qtd": [0.005, 0.1],
            "Preço Entrada": ["$ 64,500.00", "$ 1,800.00"],
            "Preço Atual": ["$ 64,976.00", "$ 1,817.37"],
            "Stop Loss": ["$ 63,000.00", "$ 1,750.00"],
            "PnL": ["+$ 2.38", "+$ 1.73"]
        })
        st.dataframe(df_posicoes, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma posição aberta no momento.")

with tab3:
    if st.session_state.robo_rodando:
        df_ordens = pd.DataFrame({
            "Hora": ["10:15:32", "10:20:10"],
            "Ativo": ["SOLUSDT", "BTCUSDT"],
            "Tipo": ["Limit Buy", "Take Profit"],
            "Preço": ["$ 70.00", "$ 66,000.00"],
            "Qtd": [10.0, 0.005],
            "Status": ["⏳ Aguardando", "⏳ Aguardando"]
        })
        st.dataframe(df_ordens, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma ordem pendente.")

with tab4:
    st.info("As operações finalizadas aparecerão aqui.")
