import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Crypto Trader Pro", page_icon="⚡", layout="wide")

# --- TEMA PREMIUM (PRETO E LARANJA) ---
st.markdown("""
    <style>
    /* Fonte e Fundo */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #050505; }

    /* Títulos e Textos */
    h1, h2, h3, h4, p, span, div { color: #E0E0E0 !important; }
    h1 { color: #FF8C00 !important; font-weight: 800; letter-spacing: -1px; }
    h2 { color: #FF8C00 !important; font-weight: 600; }
    
    /* Cartões de Métricas Customizados */
    .metric-card {
        background: linear-gradient(145deg, #121212, #0a0a0a);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); border-color: #FF8C00; }
    .metric-title { font-size: 14px; color: #888 !important; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;}
    .metric-value { font-size: 32px; color: #FF8C00 !important; font-weight: 800; margin-top: 5px; }
    .metric-delta { font-size: 14px; color: #28a745 !important; font-weight: 600; }

    /* Botões Premium */
    .stButton>button {
        background-color: #121212; color: #FF8C00;
        border: 1px solid #FF8C00; font-weight: 700;
        border-radius: 8px; padding: 12px 24px; font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #FF8C00; color: #000; box-shadow: 0 0 15px rgba(255,140,0,0.5); }
    
    /* Botão Iniciar */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, #1DB954, #169c46); color: white; border: none;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        box-shadow: 0 0 20px rgba(29,185,84,0.6); transform: scale(1.02);
    }
    
    /* Botão Emergência */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: linear-gradient(90deg, #E50914, #b80710); color: white; border: none;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        box-shadow: 0 0 20px rgba(229,9,20,0.6); transform: scale(1.02);
    }

    /* Ajustes na Sidebar */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }
    [data-testid="stSidebar"] .stRadio label { color: #E0E0E0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CACHE PARA NÃO ESTOURAR A API DE PREÇOS ---
@st.cache_data(ttl=15)
def get_prices():
    try:
        # Usando CoinGecko que é mais estável para Streamlit
        ids = "bitcoin,ethereum,solana,binancecoin,ripple"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
        headers = {"accept": "application/json", "User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {}

# --- INICIALIZAÇÃO DO ESTADO ---
if 'robo_rodando' not in st.session_state: st.session_state.robo_rodando = False
if 'saldo_virtual' not in st.session_state: st.session_state.saldo_virtual = 1000.00

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Configurações</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Modo de Operação")
    modo = st.radio("", ["Simulação (Paper)", "Observação", "Real (Bloqueado)"], index=0, label_visibility="collapsed")
    if modo == "Real (Bloqueado)":
        st.error("🔒 Modo Real requer API Keys da Binance e 2FA.")
        modo = "Simulação (Paper)"
        
    st.divider()
    st.markdown("### 💎 Ativos Monitorados")
    ativos = st.multiselect(
        "Pares USDT:", 
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"],
        default=["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### 🛡️ Gestão de Risco")
    meta_diaria = st.number_input("Meta Diária (USDT)", value=50.0, step=10.0)
    perda_maxima = st.number_input("Perda Máxima (USDT)", value=20.0, step=5.0)

# --- CABEÇALHO ---
st.markdown("<h1>⚡ Crypto Trader Terminal Pro</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #888;'>Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Status do Mercado: <span style='color:#1DB954;'>● ONLINE</span></p>", unsafe_allow_html=True)
st.divider()

# --- CONTROLE DE SESSÃO ---
col_status, col_btn1, col_btn2 = st.columns([2, 1, 1])

with col_status:
    if st.session_state.robo_rodando:
        st.markdown("""
        <div style='background-color: rgba(29,185,84,0.1); border: 1px solid #1DB954; border-radius: 8px; padding: 15px; display: flex; align-items: center;'>
            <span style='font-size: 24px; margin-right: 15px;'>🟢</span>
            <div>
                <h4 style='margin: 0; color: #1DB954 !important;'>SESSÃO ATIVA</h4>
                <p style='margin: 0; font-size: 14px; color: #888 !important;'>O robô está monitorando o mercado em busca de oportunidades.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background-color: rgba(255,255,255,0.05); border: 1px solid #333; border-radius: 8px; padding: 15px; display: flex; align-items: center;'>
            <span style='font-size: 24px; margin-right: 15px;'>⚪</span>
            <div>
                <h4 style='margin: 0; color: #E0E0E0 !important;'>SESSÃO PARADA</h4>
                <p style='margin: 0; font-size: 14px; color: #888 !important;'>Aguardando o comando para iniciar as operações.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_btn1:
    if not st.session_state.robo_rodando:
        if st.button("▶ INICIAR SESSÃO", type="primary", use_container_width=True):
            st.session_state.robo_rodando = True
            st.rerun()
    else:
        if st.button("⏸ PAUSAR ENTRADAS", use_container_width=True):
            st.warning("Entradas pausadas temporariamente.")

with col_btn2:
    if st.button("🚨 EMERGÊNCIA", type="secondary", use_container_width=True):
        st.session_state.robo_rodando = False
        st.error("KILL SWITCH ACIONADO! Operações encerradas.")
        time.sleep(1.5)
        st.rerun()

st.divider()

# --- MÉTRICAS PRINCIPAIS (DESIGN CUSTOMIZADO) ---
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Saldo Virtual</div>
        <div class="metric-value">$ {st.session_state.saldo_virtual:,.2f}</div>
        <div class="metric-delta">↑ +0.00% hoje</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Resultado Aberto</div>
        <div class="metric-value">$ 0.00</div>
        <div class="metric-delta">↑ 0.00%</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Resultado do Dia</div>
        <div class="metric-value" style="color: #1DB954 !important;">+ $ 12.50</div>
        <div class="metric-delta">↑ +1.25%</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Meta Diária</div>
        <div class="metric-value">$ {meta_diaria:.2f}</div>
        <div class="metric-delta" style="color: #FF8C00 !important;">Restam $ {meta_diaria - 12.50:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- ABAS DO SISTEMA ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Posições", "📋 Ordens", "📜 Histórico"])

with tab1:
    st.markdown("<h3>🌐 Cotações em Tempo Real</h3>", unsafe_allow_html=True)
    prices = get_prices()
    
    if prices:
        coins = {"BTCUSDT": "bitcoin", "ETHUSDT": "ethereum", "SOLUSDT": "solana", "BNBUSDT": "binancecoin", "XRPUSDT": "ripple"}
        cols = st.columns(len(coins))
        
        for i, (label, coin_id) in enumerate(coins.items()):
            price = prices.get(coin_id, {}).get("usd", 0)
            with cols[i]:
                st.metric(label=label, value=f"$ {price:,.2f}")
    else:
        st.warning("⚠️ Não foi possível carregar as cotações agora. Aguarde alguns segundos e recarregue a página.")

    st.markdown("<br><h3>🔗 Status do Motor (Backend)</h3>", unsafe_allow_html=True)
    try:
        api_url = "https://crypto-trader-ztx7.onrender.com/health"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            st.success("✅ Motor Online, Banco de Dados e Cache conectados.")
        else:
            st.warning("⚠️ Motor online, mas instável.")
    except:
        st.error("❌ Motor offline (acordando). Aguarde 30 segundos e recarregue.")

with tab2:
    st.markdown("<h3>💼 Posições Abertas</h3>", unsafe_allow_html=True)
    if st.session_state.robo_rodando:
        df_posicoes = pd.DataFrame({
            "Ativo": ["BTCUSDT", "ETHUSDT"],
            "Direção": ["🟢 LONG", "🟢 LONG"],
            "Qtd": [0.005, 0.1],
            "Preço Entrada": ["$ 64,500.00", "$ 1,800.00"],
            "Preço Atual": ["$ 64,976.00", "$ 1,817.37"],
            "Stop Loss": ["$ 63,000.00", "$ 1,750.00"],
            "PnL": ["+$ 2.38", "+$ 1.73"]
        })
        st.dataframe(df_posicoes, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma posição aberta. Inicie a sessão para simular operações.")

with tab3:
    st.markdown("<h3>📋 Ordens em Aberto</h3>", unsafe_allow_html=True)
    if st.session_state.robo_rodando:
        df_ordens = pd.DataFrame({
            "Hora": ["10:15:32", "10:20:10"],
            "Ativo": ["SOLUSDT", "BTCUSDT"],
            "Tipo": ["Limit Buy", "Take Profit"],
            "Preço": ["$ 70.00", "$ 66,000.00"],
            "Qtd": [10.0, 0.005],
            "Status": ["⏳ Pendente", "⏳ Pendente"]
        })
        st.dataframe(df_ordens, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma ordem pendente no momento.")

with tab4:
    st.markdown("<h3>📜 Histórico de Operações</h3>", unsafe_allow_html=True)
    st.info("O histórico aparecerá aqui após a primeira operação finalizada.")
