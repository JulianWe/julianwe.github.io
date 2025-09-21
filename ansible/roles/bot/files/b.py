import requests
from web3 import Web3
import json
import os

# Infura Projekt-ID
INFURA_PROJECT_ID = "76f915851be44eaabe672854358955a0"

# Layer2 RPC URLs via Infura
RPCS = {
    "ethereum": f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
    "optimism": f"https://optimism-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
    "arbitrum": f"https://arbitrum-mainnet.infura.io/v3/{INFURA_PROJECT_ID}",
    "polygon": f"https://polygon-mainnet.infura.io/v3/{INFURA_PROJECT_ID}"
}

# Chain IDs
CHAIN_IDS = {
    "ethereum": 1,
    "optimism": 10,
    "arbitrum": 42161,
    "polygon": 137
}

# UniswapV3 Pool ABI (Minimal: nur die Funktion 'slot0' zum Preisabruf)
UNISWAP_V3_POOL_ABI = json.loads("""[
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160","name": "sqrtPriceX96","type": "uint160"},
            {"internalType": "int24","name": "tick","type": "int24"},
            {"internalType": "uint16","name": "observationIndex","type": "uint16"},
            {"internalType": "uint16","name": "observationCardinality","type": "uint16"},
            {"internalType": "uint16","name": "observationCardinalityNext","type": "uint16"},
            {"internalType": "uint8","name": "feeProtocol","type": "uint8"},
            {"internalType": "bool","name": "unlocked","type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]""")

# Beispiel: Factory-Adressen UniswapV3 je Netzwerk (werden gebraucht für Pool-Adresse)
UNISWAP_V3_FACTORY = {
    "ethereum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "optimism": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "arbitrum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "polygon": "0x1F98431c8aD98523631AE4a59f267346ea31F984"
}

# UniswapV3 Factory ABI - minimal, nur Funktion getPool(tokenA, tokenB, fee)
UNISWAP_V3_FACTORY_ABI = json.loads("""[
    {
        "inputs": [
            {"internalType": "address","name": "tokenA","type": "address"},
            {"internalType": "address","name": "tokenB","type": "address"},
            {"internalType": "uint24","name": "fee","type": "uint24"}
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address","name": "pool","type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]""")

# Fee Tier - wir nutzen hier den gängigen 0.3% = 3000
FEE_TIER = 3000

def get_token_list():
    # Offizielle Uniswap Tokenliste (nur ein Beispiel)
    url = "https://tokens.uniswap.org"
    response = requests.get(url)
    data = response.json()
    # Nur erste 50 Tokens aus Performance-Gründen
    return data["tokens"][:50]

def build_token_address_map(token_list, chain_id):
    token_map = {}
    for token in token_list:
        if token["chainId"] == chain_id:
            token_map[token["symbol"]] = token["address"]
    return token_map

def init_web3_providers():
    providers = {}
    for net, rpc in RPCS.items():
        providers[net] = Web3(Web3.HTTPProvider(rpc))
    return providers

def get_uniswap_v3_pool_address(web3, factory_address, tokenA, tokenB, fee):
    factory = web3.eth.contract(address=Web3.toChecksumAddress(factory_address), abi=UNISWAP_V3_FACTORY_ABI)
    pool = factory.functions.getPool(tokenA, tokenB, fee).call()
    if pool == '0x0000000000000000000000000000000000000000':
        return None
    return pool

def get_price_from_pool(web3, pool_address, token0_address, token1_address):
    pool = web3.eth.contract(address=Web3.toChecksumAddress(pool_address), abi=UNISWAP_V3_POOL_ABI)
    try:
        slot0 = pool.functions.slot0().call()
        sqrtPriceX96 = slot0[0]
        # Preis berechnen: (sqrtPriceX96 / 2**96)^2 = price of token1 in token0
        price = (sqrtPriceX96 / 2**96) ** 2
        return price
    except Exception as e:
        print(f"Fehler beim Preisabruf vom Pool {pool_address}: {e}")
        return None

def compare_prices_across_layer2(tokens_maps, web3_providers):
    # Für jeden Token, der auf mindestens zwei Layer2s vorkommt, vergleichen wir Preise gegen ETH (native token)
    # Hier nutzen wir WETH als Referenz-Token, da Pools meist mit WETH gepaart sind.

    results = []

    # Wir nehmen WETH Adressen als Basis
    weth_addresses = {}
    for net, token_map in tokens_maps.items():
        weth = token_map.get("WETH")
        if weth:
            weth_addresses[net] = weth

    for symbol in tokens_maps["ethereum"].keys():
        # Prüfen, ob token auf mind. 2 Layer2s vorhanden ist
        nets_with_token = [net for net, tm in tokens_maps.items() if symbol in tm]
        if len(nets_with_token) < 2:
            continue

        # Preis pro Layer2 speichern
        prices = {}

        for net in nets_with_token:
            web3 = web3_providers[net]
            token_address = tokens_maps[net][symbol]
            weth_address = weth_addresses.get(net)
            if not weth_address:
                continue

            # Pooladresse holen (Token/WETH)
            pool_address = get_uniswap_v3_pool_address(web3, UNISWAP_V3_FACTORY[net], token_address, weth_address, FEE_TIER)
            if pool_address is None:
                # versuchen andere Reihenfolge Token0/Token1 vertauschen
                pool_address = get_uniswap_v3_pool_address(web3, UNISWAP_V3_FACTORY[net], weth_address, token_address, FEE_TIER)
                if pool_address is None:
                    continue

            price = get_price_from_pool(web3, pool_address, token_address, weth_address)
            if price is not None:
                prices[net] = price

        if len(prices) >= 2:
            results.append((symbol, prices))

    return results

def main():
    print("Tokenliste laden...")
    tokens = get_token_list()

    print("Token-Adressen pro Layer 2 Netzwerk aufbauen...")
    tokens_maps = {}
    for net, chain_id in CHAIN_IDS.items():
        tokens_maps[net] = build_token_address_map(tokens, chain_id)

    print(tokens_maps[net])

    print("Web3 Provider initialisieren...")
    web3_providers = init_web3_providers()

    print("Preisvergleich starten...")
    price_diffs = compare_prices_across_layer2(tokens_maps, web3_providers)
    print(price_diffs)

    print("\nArbitrage mögliche Token und Preise pro Netzwerk:")
    for symbol, prices in price_diffs:
        print(f"\nToken: {symbol}")
        for net, price in prices.items():
            print(f"  {net}: {price:.6f} ETH")

        # Einfacher Preisvergleich: Min und Max Preis
        min_net = min(prices, key=prices.get)
        max_net = max(prices, key=prices.get)
        diff = prices[max_net] - prices[min_net]
        perc = (diff / prices[min_net]) * 100 if prices[min_net] > 0 else 0
        print(f"  -> Differenz: {diff:.6f} ETH ({perc:.2f}%) zwischen {min_net} und {max_net}")

if __name__ == "__main__":
    if INFURA_PROJECT_ID == "DEIN_INFURA_PROJECT_ID":
        print("Bitte deinen Infura Projekt-ID in INFURA_PROJECT_ID eintragen!")
    else:
        main()
