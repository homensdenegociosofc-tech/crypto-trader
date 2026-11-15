import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Crypto Trader", page_icon="📈", layout="wide")

# INJEÇÃO DO TEMA PRETO E LARANJA (CSS)
st.markdown("""
    <style>
    /* Fundo preto */
    .stApp {
        background-color: #0a0a0a;
    }
    /* Textos em laranja */
    h1, h2, h3, p, span, div {
        color: #FF8C00 !important;
    }
    /* Botões laranja */
    .stButton>button {
        background-color: #FF8C00;
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #FFA500;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Crypto Trader - Painel de Controle")
st.write("Bem-vindo ao seu sistema automatizado de trading.")

st.divider()

# Verificando o Motor (API)
st.subheader("Status do Motor (API)")
api_url = "https://crypto-trader-zxt7.onrender.com/health" # Link do seu motor

try:
    response = requests.get(api_url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get("banco_de_dados") == "conectado com sucesso":
            st.success("✅ Motor Online! Banco de Dados e Cache conectados.")
        else:
            st.warning("⚠️ Motor online, mas com erro nas conexões.")
        st.json(data)
    else:
        st.error("❌ Motor respondeu com erro.")
except Exception as e:
    st.warning(f"⚠️ Motor dormindo. Ele vai acordar em alguns segundos, aguarde...")
    st.error(f"Detalhe técnico: {e}")

st.divider()

# Cotações da Binance
st.subheader("Cotações em Tempo Real (Binance)")
st.write("Preços puxados diretamente da API pública da Binance.")

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
cols = st.columns(len(symbols))

for i, symbol in enumerate(symbols):
    try:
        # Puxa o preço direto da Binance
        res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        price = float(res.json()["price"])
        with cols[i]:
            st.metric(label=symbol, value=f"$ {price:,.2f}")
    except:
        with cols[i]:
            st.metric(label=symbol, value="Erro")

if st.button("🔄 Atualizar Preços"):
    st.rerun()
