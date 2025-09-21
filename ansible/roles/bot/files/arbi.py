import time
from web3 import Web3
from uniswap import Uniswap
import requests

# === Konfiguration ===
TELEGRAM_ENABLED = False
TELEGRAM_TOKEN = "8055777814:AAE8pQ3QnJK3vkssvpz_cOV_8Cg9Ck3cGhE"
TELEGRAM_CHAT_ID = "35034588"
ARBITRAGE_THRESHOLD = 0.01  # 1 %

# Netzwerke & Token
NETWORKS = {
    "optimism": {
        "rpc": "https://optimism.llamarpc.com",
        "chain_id": 10,
        "tokens": {
            "USDC": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
            "WETH": "0x4200000000000000000000000000000000000006"
        }
    },
    "arbitrum": {
        "rpc": "https://arb1.arbitrum.io/rpc",
        "chain_id": 42161,
        "tokens": {
            "USDC": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
            "WETH": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
        }
    },
    "polygon": {
        "rpc": "https://polygon-rpc.com",
        "chain_id": 137,
        "tokens": {
            "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
        }
    }
}

# === Funktionen ===

def get_price(network_name, token_in, token_out, amount_in_wei):
    try:
        rpc = NETWORKS[network_name]["rpc"]
        web3 = Web3(Web3.HTTPProvider(rpc))
        uni = Uniswap(address=None, private_key=None, web3=web3, version=3)
        return uni.get_price_input(token_in, token_out, amount_in_wei)
    except Exception as e:
        print(f"Fehler bei {network_name}: {e}")
        return None

def send_telegram_message(text):
    if not TELEGRAM_ENABLED:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Fehler: {e}")

def find_arbitrage(token_pair=("WETH", "USDC"), amount_eth=1.0):
    print(f"\n🔎 Suche Arbitrage für {token_pair[0]} → {token_pair[1]} bei {amount_eth} ETH")
    prices = {}

    amount_in = int(amount_eth * 1e18)
    for net in NETWORKS:
        token_in = NETWORKS[net]["tokens"][token_pair[0]]
        token_out = NETWORKS[net]["tokens"][token_pair[1]]
        price = get_price(net, token_in, token_out, amount_in)
        if price:
            prices[net] = price / 1e6  # USDC hat 6 Dezimalstellen

    if len(prices) < 2:
        print("Nicht genügend Preisdaten.")
        return

    sorted_prices = sorted(prices.items(), key=lambda x: x[1])
    low = sorted_prices[0]
    high = sorted_prices[-1]

    diff_percent = (high[1] - low[1]) / low[1]
    if diff_percent >= ARBITRAGE_THRESHOLD:
        msg = f"💸 Arbitrage-Möglichkeit:\nKaufe auf {low[0]} für {low[1]:.4f} USDC\nVerkaufe auf {high[0]} für {high[1]:.4f} USDC\n🔁 Gewinnspanne: {diff_percent*100:.2f}%"
        print(msg)
        send_telegram_message(msg)
    else:
        print(f"Keine Arbitrage-Möglichkeit. Spanne: {diff_percent*100:.2f}%")

# === Hauptprogramm ===

if __name__ == "__main__":
    while True:
        find_arbitrage(("WETH", "USDC"), amount_eth=1.0)
        time.sleep(30)  # alle 30 Sekunden prüfen
