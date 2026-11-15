import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="Crypto Trader", page_icon="📈", layout="wide")

# INJEÇÃO DO TEMA PRETO E LARANJA (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3, p, span, div { color: #FF8C00 !important; }
    .stButton>button {
        background-color: #FF8C00;
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stButton>button:hover { background-color: #FFA500; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Crypto Trader - Painel de Controle")
st.write("Bem-vindo ao seu sistema automatizado de trading.")

st.divider()

# Verificando o Motor (API)
st.subheader("Status do Motor (API)")
api_url = "https://crypto-trader-zxt7.onrender.com/health"

with st.spinner("Verificando motor..."):
    try:
        # Aumentamos o tempo de espera para 30 segundos, caso o Render esteja dormindo
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Motor Online! Banco de Dados e Cache conectados.")
            st.json(data)
        else:
            st.warning(f"⚠️ Motor respondeu, mas com código de erro: {response.status_code}. Pode estar acordando.")
    except requests.exceptions.Timeout:
        st.warning("⚠️ O motor está demorando muito para responder (pode estar acordando). Clique em 'Atualizar' abaixo.")
    except Exception as e:
        st.error(f"❌ Erro ao conectar no motor: {e}")

st.divider()

# Cotações (Usando CoinGecko para não ser bloqueado)
st.subheader("Cotações em Tempo Real (Mercado)")
st.write("Preços puxados diretamente da API pública CoinGecko.")

# Mapeamento das moedas
coins = {
    "BTCUSDT (Bitcoin)": "bitcoin",
    "ETHUSDT (Ethereum)": "ethereum",
    "SOLUSDT (Solana)": "solana",
    "BNBUSDT (Binance Coin)": "binancecoin",
    "XRPUSDT (Ripple)": "ripple"
}

cols = st.columns(len(coins))

try:
    # Puxa todos os preços de uma vez (mais rápido)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,ripple&vs_currencies=usd"
    res = requests.get(url, timeout=10)
    prices = res.json()
    
    for i, (label, coin_id) in enumerate(coins.items()):
        price = prices.get(coin_id, {}).get("usd", 0)
        with cols[i]:
            st.metric(label=label, value=f"$ {price:,.2f}")
except Exception as e:
    st.error(f"Erro ao puxar preços: {e}")

st.divider()
if st.button("🔄 Atualizar Dados"):
    st.rerun()
