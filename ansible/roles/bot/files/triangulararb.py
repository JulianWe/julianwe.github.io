import requests

# API-URLs für drei Währungspaare auf Binance
url = 'https://api.binance.com/api/v3/ticker/price'

def get_prices():
    response = requests.get(url)
    prices {item['symbol']: float(item['price']) for item in response.json()}
    return prices

def check_triangular_arbitrage():
    prices = get_prices()
    print(prices)
    # Beispiel: BTC/USDT, ETH/USDT, ETH/BTC
    btc_usdt = prices['ZKUSDT']
    eth_usdt = prices['ZKUSDC']
    eth_btc = prices['ZKBTC']

    # Berechnung der Arbitragemöglichkeiten
    if (btc_usdt * eth_btc) < eth_usdt:
        print("Arbitrage-Möglichkeit gefunden: BTC -> ETH -> USDT")
    elif (eth_usdt / eth_btc) < btc_usdt:
        print("Arbitrage-Möglichkeit gefunden: ETH -> BTC -> USDT")

if __name__ == "__main__":
    check_triangular_arbitrage()
