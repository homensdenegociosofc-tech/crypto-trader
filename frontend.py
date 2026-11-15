import streamlit as st
import requests

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
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Motor Online! Banco de Dados e Cache conectados.")
            st.json(data)
        else:
            st.warning(f"⚠️ O motor respondeu com código {response.status_code}. Se o erro persistir, pode ser que o Render esteja reiniciando.")
    except requests.exceptions.Timeout:
        st.warning("⚠️ O motor está demorando para responder (pode estar acordando). Clique em 'Atualizar Dados' abaixo.")
    except Exception as e:
        st.error(f"❌ Erro ao conectar no motor: {e}")

st.divider()

# Cotações (Usando CryptoCompare - mais estável e sem bloqueio)
st.subheader("Cotações em Tempo Real (Mercado)")
st.write("Preços puxados diretamente da API pública CryptoCompare.")

symbols = ["BTC", "ETH", "SOL", "BNB", "XRP"]
labels = {
    "BTC": "BTCUSDT (Bitcoin)",
    "ETH": "ETHUSDT (Ethereum)",
    "SOL": "SOLUSDT (Solana)",
    "BNB": "BNBUSDT (Binance Coin)",
    "XRP": "XRPUSDT (Ripple)"
}

cols = st.columns(len(symbols))

try:
    # Puxa todos os preços de uma vez
    url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={','.join(symbols)}&tsyms=USD"
    res = requests.get(url, timeout=10)
    prices = res.json()
    
    for i, symbol in enumerate(symbols):
        price = prices.get(symbol, {}).get("USD", 0)
        with cols[i]:
            st.metric(label=labels[symbol], value=f"$ {price:,.2f}")
except Exception as e:
    st.error(f"Erro ao puxar preços: {e}")

st.divider()
if st.button("🔄 Atualizar Dados"):
    st.rerun()
