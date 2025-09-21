import requests

# URLs für Uniswap und 1inch Token Listen
UNISWAP_TOKEN_LIST_URL = 'https://tokens.uniswap.org'
ONEINCH_TOKEN_LIST_URL = 'https://tokenlists.1inch.io'

# Layer-2 Netzwerk ChainIDs
LAYER_2_CHAIN_IDS = {10: 'Optimism', 42161: 'Arbitrum', 137: 'Polygon', 324: 'zkSync', 1101: 'StarkNet'}

# Coingecko API für Preisabfrage
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/token_price"

# Unterstützte Netzwerke in Coingecko für Preisabfragen
COINGECKO_CHAIN_IDS = {
    1: 'ethereum',
    10: 'optimistic-ethereum',
    42161: 'arbitrum-one',
    137: 'polygon-pos'
    # zkSync und StarkNet werden noch nicht vollständig von Coingecko unterstützt
}

def get_token_list(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen der Token-Liste von {url}")
        return None

def get_token_price(chain, contract_address):
    """Ruft den Preis eines Tokens basierend auf seinem Netzwerk und seiner Contract-Adresse ab."""
    if chain in COINGECKO_CHAIN_IDS:
        network = COINGECKO_CHAIN_IDS[chain]
        url = f"{COINGECKO_API_URL}/{network}?contract_addresses={contract_address}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            price_data = response.json()
            return price_data.get(contract_address.lower(), {}).get('usd', 'Preis nicht verfügbar')
    return 'Preis nicht verfügbar'

def print_layer_2_tokens_and_prices(token_list, source):
    if token_list and 'tokens' in token_list:
        print(f"\nLayer-2 Token-Adressen und Preise aus {source}:")
        for token in token_list['tokens']:
            network_id = token.get('chainId')
            if network_id in LAYER_2_CHAIN_IDS:
                name = token.get('name', 'Unbekannt')
                symbol = token.get('symbol', 'Unbekannt')
                address = token.get('address', 'Unbekannt')
                network_name = LAYER_2_CHAIN_IDS[network_id]

                # Preis des Tokens abrufen
                price = get_token_price(network_id, address)

                print(f"Token: {name} ({symbol}), Netzwerk: {network_name}, Adresse: {address}, Preis: {price} USD")
    else:
        print(f"Keine Token in der Liste von {source} gefunden.")

if __name__ == "__main__":
    # Abrufen der Uniswap-Token-Liste
    uniswap_tokens = get_token_list(UNISWAP_TOKEN_LIST_URL)
    print_layer_2_tokens_and_prices(uniswap_tokens, "Uniswap")

    # Abrufen der 1inch-Token-Liste
    oneinch_tokens = get_token_list(ONEINCH_TOKEN_LIST_URL)
    print_layer_2_tokens_and_prices(oneinch_tokens, "1inch")
