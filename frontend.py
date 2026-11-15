import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Crypto Trader - Terminal", page_icon="📈", layout="wide")

# --- TEMA PRETO E LARANJA ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3, h4, p, span, div { color: #FF8C00 !important; }
    .stButton>button {
        background-color: #1a1a1a; color: #FF8C00; border: 1px solid #FF8C00;
        font-weight: bold; border-radius: 5px; width: 100%;
    }
    .stButton>button:hover { background-color: #FF8C00; color: black; }
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #28a745; color: white; border: none;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #218838; color: white;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: #dc3545; color: white; border: none;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: #c82333; color: white;
    }
    .stAlert { background-color: #1a1a1a; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'robo_rodando' not in st.session_state:
    st.session_state.robo_rodando = False
if 'saldo_virtual' not in st.session_state:
    st.session_state.saldo_virtual = 1000.00

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.title("Configurações")
    st.subheader("Modo de Operação")
    modo = st.radio("Selecione o modo:", ["Simulação (Paper)", "Observação", "Real (Bloqueado)"], index=0)
    if modo == "Real (Bloqueado)":
        st.warning("⚠️ O modo real exige configuração de API Keys.")
        modo = "Simulação (Paper)"
        
    st.subheader("Ativos Monitorados")
    ativos_selecionados = st.multiselect(
        "Pares USDT:", 
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"],
        default=["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    )
    
    st.subheader("Gestão de Risco (Diário)")
    meta_diaria = st.number_input("Meta (USDT)", value=50.0)
    perda_maxima = st.number_input("Perda Máxima (USDT)", value=20.0)

# --- CABEÇALHO ---
st.title("📈 Crypto Trader Terminal")
st.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Modo: **{modo}**")
st.divider()

# --- PAINEL DE CONTROLE (BOTÕES) ---
col_status, col_btn1, col_btn2 = st.columns([2, 1, 1])

with col_status:
    if st.session_state.robo_rodando:
        st.success("🟢 SESSÃO ATIVA - O robô está monitorando o mercado.")
    else:
        st.info("⚪ SESSÃO PARADA - Aguardando início.")

with col_btn1:
    if not st.session_state.robo_rodando:
        if st.button("▶️ INICIAR SESSÃO", type="primary", use_container_width=True):
            st.session_state.robo_rodando = True
            st.rerun()
    else:
        if st.button("⏸️ PAUSAR NOVAS ENTRADAS", use_container_width=True):
            st.warning("Entradas pausadas (Saídas continuam ativas).")

with col_btn2:
    if st.button("🚨 PARADA DE EMERGÊNCIA", type="secondary", use_container_width=True):
        st.session_state.robo_rodando = False
        st.error("KILL SWITCH ACIONADO! Todas as operações foram encerradas.")
        time.sleep(2)
        st.rerun()

st.divider()

# --- MÉTRICAS PRINCIPAIS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Saldo Virtual", f"$ {st.session_state.saldo_virtual:,.2f}", "+0.00%")
m2.metric("Resultado Aberto", "$ 0.00", "0.00%")
m3.metric("Resultado do Dia", "$ 12.50", "+1.25%")
m4.metric("Meta Diária", f"$ {meta_diaria:.2f}", "Restam $ 37.50")

st.divider()

# --- ABAS DO SISTEMA ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "💼 Posições Abertas", "📋 Ordens", "📜 Histórico"])

with tab1:
    st.subheader("Cotações em Tempo Real")
    try:
        symbols = ["BTC", "ETH", "SOL", "BNB"]
        url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={','.join(symbols)}&tsyms=USD"
        prices = requests.get(url, timeout=5).json()
        cols = st.columns(len(symbols))
        for i, sym in enumerate(symbols):
            price = prices.get(sym, {}).get("USD", 0)
            with cols[i]:
                st.metric(label=f"{sym}USDT", value=f"$ {price:,.2f}")
    except:
        st.warning("Não foi possível carregar as cotações agora.")
        
    st.subheader("Status do Motor (Backend API)")
    try:
        # LINK CORRIGIDO AQUI!
        api_url = "https://crypto-trader-ztx7.onrender.com/health"
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            st.success("✅ Motor Online e Conectado ao Banco de Dados e Cache.")
        else:
            st.warning("⚠️ Motor online, mas instável.")
    except:
        st.error("❌ Motor offline (pode estar acordando).")

with tab2:
    st.subheader("Posições Abertas (Simulação)")
    if st.session_state.robo_rodando:
        df_posicoes = pd.DataFrame({
            "Ativo": ["BTCUSDT", "ETHUSDT"],
            "Direção": ["LONG", "LONG"],
            "Qtd": [0.005, 0.1],
            "Preço Entrada": ["$ 64,500.00", "$ 1,800.00"],
            "Preço Atual": ["$ 64,976.00", "$ 1,817.37"],
            "Stop Loss": ["$ 63,000.00", "$ 1,750.00"],
            "PnL (Lucro)": ["+$ 2.38", "+$ 1.73"]
        })
        st.dataframe(df_posicoes, use_container_width=True)
    else:
        st.info("Nenhuma posição aberta. Inicie a sessão para simular operações.")

with tab3:
    st.subheader("Ordens em Aberto")
    if st.session_state.robo_rodando:
        df_ordens = pd.DataFrame({
            "Hora": ["10:15:32", "10:20:10"],
            "Ativo": ["SOLUSDT", "BTCUSDT"],
            "Tipo": ["Limit Buy", "Take Profit"],
            "Preço": ["$ 70.00", "$ 66,000.00"],
            "Qtd": [10.0, 0.005],
            "Status": ["Pendente", "Pendente"]
        })
        st.dataframe(df_ordens, use_container_width=True)
    else:
        st.info("Nenhuma ordem pendente no momento.")

with tab4:
    st.subheader("Histórico de Operações")
    st.info("O histórico aparecerá aqui após a primeira operação finalizada.")
