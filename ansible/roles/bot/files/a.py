import requests
from web3 import Web3
import json

# Infura API Key (deinen eigenen einfügen!)
INFURA_PROJECT_ID = "76f915851be44eaabe672854358955a0"

networks = {
    "ethereum": {
        "rpc_url": f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
        "chain_id": 1,
        "quoter_address": '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
    },
    "optimism": {
        "rpc_url": f"https://optimism-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
        "chain_id": 10,
        "quoter_address": '0x61fFE014bA17989E743c5F6cB21bF9697530B21e'
    },
    "arbitrum": {
        "rpc_url": f"https://arbitrum-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
        "chain_id": 42161,
        "quoter_address": '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
    },
    "polygon": {
        "rpc_url": f"https://polygon-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
        "chain_id": 137,
        "quoter_address": '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
    }
}

# USDC-Adressen pro Netzwerk (Standard 6 Dezimalstellen)
USDC_ADDRESSES = {
    "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "optimism": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
    "arbitrum": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
}

UNISWAP_V3_QUOTER_ABI = json.loads("""[
  {
    "inputs": [
      { "internalType": "address", "name": "tokenIn", "type": "address" },
      { "internalType": "address", "name": "tokenOut", "type": "address" },
      { "internalType": "uint24", "name": "fee", "type": "uint24" },
      { "internalType": "uint256", "name": "amountIn", "type": "uint256" },
      { "internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160" }
    ],
    "name": "quoteExactInputSingle",
    "outputs": [{ "internalType": "uint256", "name": "amountOut", "type": "uint256" }],
    "stateMutability": "view",
    "type": "function"
  }
]""")

def get_token_list():
    # Offizielle Uniswap Tokenliste (nur ein Beispiel)
    url = "https://tokens.uniswap.org"
    response = requests.get(url)
    data = response.json()
    # Nur erste 50 Tokens aus Performance-Gründen
    return data["tokens"][:50]

def get_price(token_address, network, amount_in_wei=10**18, fee=3000):
    web3 = Web3(Web3.HTTPProvider(networks[network]['rpc_url']))
    quoter_contract = web3.eth.contract(address=networks[network]['quoter_address'], abi=UNISWAP_V3_QUOTER_ABI)
    
    token_in = token_address
    token_out = USDC_ADDRESSES[network]
    
    try:
        amount_out = quoter_contract.functions.quoteExactInputSingle(
            token_in, token_out, fee, amount_in_wei, 0
        ).call()
        # USDC hat 6 Dezimalstellen
        return amount_out / 1e6
    except Exception as e:
        # Token nicht gelistet oder Pool existiert nicht
        return None

def main():
    tokens = get_token_list()
    amount_in = 1  # 1 Token als Beispiel
    print(f"Preisvergleich von Tokens gegen USDC (für {amount_in} Token) auf Layer-2 Netzwerken:\n")
    for token in tokens:
        token_name = token["name"]
        token_symbol = token["symbol"]
        token_address = token["address"]

        print(f"{token_symbol} ({token_name}):")
        for network in networks.keys():
            price = get_price(token_address, network)
            if price:
                print(f"  {network.capitalize()}: {price:.6f} USDC")
            else:
                print(f"  {network.capitalize()}: Kein Preis verfügbar")
        print("")

if name == "__main__":
    main()