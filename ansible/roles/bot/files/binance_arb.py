
import requests


def get_prices(symbols):
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    prices = {item['symbol']: float(item['price']) for item in response.json()}
    print(prices)
    return {symbol: prices[symbol] for symbol in symbols}

def check_arbitrage(prices, symbol1, symbol2):
    price1 = prices[symbol1]
    price2 = prices[symbol2]
    
    if price1 < price2:
        profit = price2 - price1
        print(f'Arbitrage Opportunity: Buy {symbol1} at {price1} and sell {symbol2} at {price2}. Profit: {profit}')
    elif price2 < price1:
        profit = price1 - price2
        print(f'Arbitrage Opportunity: Buy {symbol2} at {price2} and sell {symbol1} at {price1}. Profit: {profit}')
    else:
        print('No arbitrage opportunity.')


if __name__ == "__main__":
    check_triangular_arbitrage()
