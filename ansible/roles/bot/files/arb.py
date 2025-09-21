import os
from web3 import Web3
from dotenv import load_dotenv
from telegram import Bot
import requests

load_dotenv()


import requests



BOT_TOKEN = '8055777814:AAE8pQ3QnJK3vkssvpz_cOV_8Cg9Ck3cGhE'  # Dein Bot-Token


def get_chat_id(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Fehler beim Abrufen: {response.status_code}")
        return None

    data = response.json()
    if not data.get("ok"):
        print(f"❌ Telegram-Fehler: {data.get('description')}")
        return None

    try:
        # Nehme die zuletzt gesendete Nachricht
        message = data["result"][-1]["message"]
        chat_id = message["chat"]["id"]
        username = message["chat"].get("username", "Kein Benutzername")
        print(f"✅ Chat-ID gefunden: {chat_id} (Benutzer: {username})")
        return chat_id
    except (IndexError, KeyError):
        print("⚠️ Keine gültige Nachricht gefunden. Hast du dem Bot schon geschrieben?")
        return None

CHAT_ID = get_chat_id(BOT_TOKEN)


def send_telegram_message(token, chat_id, msg):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': msg
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print('✅ Nachricht gesendet!')
    else:
        print('❌ Fehler:', response.text)


# Knuff Public RPC URLs
RPC_URLS = {
    "ethereum": os.getenv("ETH_RPC_URL", "https://eth-pokt.knuff.io"),
    "arbitrum": os.getenv("ARB_RPC_URL", "https://arbitrum-one.public.blastapi.io"),
    "optimism": os.getenv("OPT_RPC_URL", "https://optimism-mainnet.public.blastapi.io"),
    "base": os.getenv("BASE_RPC_URL", "https://base-mainnet.knuff.io"),
    "polygon_zkevm": os.getenv("POLYGON_ZKEVM_RPC_URL", "https://zkevm-rpc.com")
}

# Telegram-Konfiguration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ARBITRAGE_THRESHOLD = float(os.getenv("ARBITRAGE_THRESHOLD", 1.0))

bot = Bot(token=TELEGRAM_TOKEN)

# Uniswap Quoter
QUOTER_ADDRESS = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
QUOTER_ABI = [{
    "inputs": [
        {"internalType": "address", "name": "tokenIn", "type": "address"},
        {"internalType": "address", "name": "tokenOut", "type": "address"},
        {"internalType": "uint24", "name": "fee", "type": "uint24"},
        {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
        {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
    ],
    "name": "quoteExactInputSingle",
    "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
}]

# Token-Adressen und Infos 
TOKENS = {
    "WETH": {
        "symbol": "WETH",
        "decimals": 18,
        "addresses": {
            "ethereum": "0xC02aaA39b223FE8D0A0E5C4F27eAD9083C756Cc2",
            "arbitrum": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
            "optimism": "0x4200000000000000000000000000000000000006",
            "base": "0x4200000000000000000000000000000000000006",
            "polygon_zkevm": "0x4200000000000000000000000000000000000006"
        }
    },
    "USDC": {
        "symbol": "USDC",
        "decimals": 6,
        "addresses": {
            "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eb48",
            "arbitrum": "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8",
            "optimism": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
            "base": "0xd9AA294cEc8A978480Ce8e36b8EDEB7E6a36E0cE",
            "polygon_zkevm": "0xA8ce8aee21bc2a48a5ef670afcc9274c7bbbc035"
        }
    },
    "DAI": {
        "symbol": "DAI",
        "decimals": 18,
        "addresses": {
            "ethereum": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "arbitrum": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
            "optimism": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
            "base": "0x6A7661795C374c0bFC635934efAddFf3A7Ee23b6",
            "polygon_zkevm": "0xA26783fC5dAaD07224a23700365441a1e6E09F69"
        }
    },
    "WBTC": {
        "symbol": "WBTC",
        "decimals": 8,
        "addresses": {
            "ethereum": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
            "arbitrum": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
            "optimism": "0x68f180fcce6836688e9084f035309e29bf0a2095",
            "base": None,  # ggf. nicht verfügbar
            "polygon_zkevm": None
        }
    }
}
PAIRS = [
    ("WETH", "USDC"),
    ("WETH", "DAI"),
    ("WBTC", "USDC"),
]

FEE_TIER = 3000
AMOUNT_IN_ETH = 1

def get_quote(chain, token_in, token_out):
    web3 = Web3(Web3.HTTPProvider(RPC_URLS[chain]))
    quoter = web3.eth.contract(address=QUOTER_ADDRESS, abi=QUOTER_ABI)

    t_in = TOKENS[token_in]
    t_out = TOKENS[token_out]
    addr_in = t_in["addresses"].get(chain)
    addr_out = t_out["addresses"].get(chain)

    if not addr_in or not addr_out:
        return None

    amount_in = int(AMOUNT_IN_ETH * 10**t_in["decimals"])
    try:
        amount_out = quoter.functions.quoteExactInputSingle(
            addr_in, addr_out, FEE_TIER, amount_in, 0
        ).call()
        return amount_out / 10**t_out["decimals"]
    except:
        return None

def detect_arbitrage(prices: dict, token_in: str, token_out: str):
    max_chain = max(prices, key=prices.get)
    min_chain = min(prices, key=prices.get)
    max_price = prices[max_chain]
    min_price = prices[min_chain]

    if not max_price or not min_price:
        return None

    spread_percent = ((max_price - min_price) / min_price) * 100
    if spread_percent >= ARBITRAGE_THRESHOLD:
        return {
            "token_pair": f"{token_in} → {token_out}",
            "buy_on": min_chain,
            "sell_on": max_chain,
            "buy_price": min_price,
            "sell_price": max_price,
            "spread": spread_percent
        }
    return None

def main():
    print("📡 Starte Arbitrage-Scanner (Knuff RPCs)...")
    for token_in, token_out in PAIRS:
        prices = {}
        for chain in RPC_URLS:
            price = get_quote(chain, token_in, token_out)
            msg=(price)
            send_telegram_message(BOT_TOKEN, CHAT_ID, msg)
            if price:
                prices[chain] = price

        if len(prices) < 2:
            continue

        arb = detect_arbitrage(prices, token_in, token_out)
        if arb:
            msg = (
                f"🚨 Arbitrage für {arb['token_pair']}:\n"
                f"💰 Kaufen auf {arb['buy_on']} für {arb['buy_price']:.4f}\n"
                f"📈 Verkaufen auf {arb['sell_on']} für {arb['sell_price']:.4f}\n"
                f"📊 Spread: {arb['spread']:.2f}%"
            )
            send_telegram_message(BOT_TOKEN, CHAT_ID, msg)

if __name__ == "__main__":
    main()