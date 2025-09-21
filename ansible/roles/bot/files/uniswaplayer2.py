from web3 import Web3
from uniswap import Uniswap
import web3.utils
import json
from web3.exceptions import ContractLogicError
from eth_abi import decode_single
from decimal import Decimal

# ABI für den Uniswap V3 QuoterV2 Contract
#UNISWAP_V3_QUOTER_ABI = '''[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"amountIn","type":"uint256"}],"name":"quoteExactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"name":"quoteExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint256","name":"amountOut","type":"uint256"}],"name":"quoteExactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"name":"quoteExactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"path","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"view","type":"function"}]'''

# ABI für den Uniswap V3 QuoterV2 Contract
UNISWAP_V3_QUOTER_ABI = '''[
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
]'''


# Layer 2 Netzwerke und ihre RPC-URLs
networks = {
    "ethereum": {
        "rpc_url": "https://mainnet.infura.io/v3/5309f62fbf1f41eb97e16033efed3ca4",
        "chain_id": 1,
        "quoter_address": '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
    },
    "optimism": {
        "rpc_url": "https://optimism-mainnet.infura.io/v3/5309f62fbf1f41eb97e16033efed3ca4",
        "chain_id": 10,
        "quoter_address": '0x61fFE014bA17989E743c5F6cB21bF9697530B21e'
    },
    "arbitrum": {
        "rpc_url": "https://arbitrum-mainnet.infura.io/v3/5309f62fbf1f41eb97e16033efed3ca4",
        "chain_id": 42161,
        "quoter_address": '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'

    },
    "polygon": {
        "rpc_url": "https://polygon-mainnet.infura.io/v3/5309f62fbf1f41eb97e16033efed3ca4",
        "chain_id": 137,
        "quoter_address":'0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'
    }
    #"base":{
    #    "rpc_url": "https://base-mainnet.infura.io/v3/5309f62fbf1f41eb97e16033efed3ca4",
    #    "chain_id": 8453
    #}
}

# Token-Adressen auf den jeweiligen Layer-2-Netzwerken
contract_addresses = {
    "ethereum": { #1
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "ENS": "0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72",
        "SNX": "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
        "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "CRV": "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        #"ENJ": "0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c"
    },
    "optimism": { # 10
        "USDC": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "WETH": "0x4200000000000000000000000000000000000006",
        "LINK": "0x350a791Bfc2C21F9Ed5d10980Dad2e2638ffa7f6",
        "ENS": "0xAd42D013ac31486B73b6b059e748172994736426",
        "SNX": "0x8700dAec35aF8Ff88c16BdF0418774CB3D7599B4",
        "UNI": "0x6fd9d7AD17242c41f7131d257212c54A0e816691",
        "CRV": "0x0994206dfE8De6Ec6920FF4D779B0d950605Fb53",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    "arbitrum": { # 42161
        "USDC": "0xcebA9300f2b948710d2653dD7B07f33A8B32118C",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "LINK": "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4",
        "ENS": "0x6314C31A7a1652cE482cffe247E9CB7c3f4BB9aF",
        "SNX": "0xcBA56Cd8216FCBBF3fA6DF6137F3147cBcA37D60",
        "UNI": "0xFa7F8980b0f1E64A2062791cc3b0871572f1F7f0",
        "CRV": "0x11cDb42B0EB46D95f990BeDD4695A6e3fA034978",
        "DAI": "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        #"ENJ": "0x7fa9549791EFc9030e1Ed3F25D18014163806758"
    },
    "polygon": { # 137
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "LINK": "0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39",
        "ENS": "0xbD7A5Cf51d22930B8B3Df6d834F9BCEf90EE7c4f",
        "SNX": "0x50B728D8D964fd00C2d0AAD81718b71311feF68a",
        "UNI": "0xb33EaAd8d922B1083446DC23f610c2567fB5180f",
        "CRV": "0x172370d5Cd63279eFa6d502DAB29171933a610AF",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
    }
}

# Uniswap V3 Router Contract Adressen für Layer-2-Netzwerke
router_addresses = {
    "optimism": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "arbitrum": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "polygon": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "base": "0xE592427A0AEce92De3Edee1F18E0157C05861564"
}


# Uniswap Web3 RPC Provider
def uniswap_interface(network_name):
    try:
        network = networks[network_name]
        rpc_url = network["rpc_url"]
        chain_id = network["chain_id"]

        # Web3 Instanz und Uniswap-Client erstellen
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        uniswap = Uniswap(address=None, private_key=None, web3=web3, version=3)

        return uniswap

    except Exception as e:
        print(f"Fehler beim Abrufen des Preises auf {network_name}: {e}")



def get_price_from_uniswap_v3(network_name, token_in, token_out, amount_in=1, fee=3000):
    """
    Holt den Preis für token_in → token_out auf Uniswap V3 auf dem angegebenen Netzwerk.
    Args:
        network_name (str): z. B. "optimism"
        token_in (str): Address von z. B. WETH
        token_out (str): Address von z. B. USDC
        amount_in (float): Menge in token_in
        fee (int): Pool-Fee, z. B. 500 (0.05%), 3000 (0.3%), 10000 (1%)

    Returns:
        Decimal: Preis in token_out für amount_in token_in
    """

    web3 = get_web3(network_name)
    router_address = UNISWAP_V3_ROUTER_ADDRESS
    router_contract = web3.eth.contract(address=router_address, abi=UNISWAP_V3_ROUTER_ABI)

    try:
        # Convert amount to raw (18 decimals for ETH/WETH)
        token_in_decimals = get_token_decimals(web3, token_in)
        token_out_decimals = get_token_decimals(web3, token_out)
        amount_in_wei = int(Decimal(amount_in) * Decimal(10 ** token_in_decimals))

        # Call quoteExactInputSingle
        quote = router_contract.functions.quoteExactInputSingle(
            Web3.toChecksumAddress(token_in),
            Web3.toChecksumAddress(token_out),
            fee,
            amount_in_wei,
            0  # sqrtPriceLimitX96
        ).call()

        # Convert result to float
        amount_out = Decimal(quote) / Decimal(10 ** token_out_decimals)
        return round(amount_out, 6)

    except ContractLogicError as e:
        print(f"⚠️ Contract-Fehler ({network_name}): {e}")
    except Exception as e:
        print(f"❌ Fehler beim Abrufen des Preises auf {network_name}: {e}")
    
    return None


# Funktion zum Abrufen des Preises eines Tokens auf einem Layer-2-Netzwerk
def get_price_from_contract_address(contract_address_one, contract_address_two, network_name):
    uniswap = uniswap_interface(network_name)
    # Preis von WETH gegen USDC abrufen
    try:
        print("try")
        price_in_usdc = uniswap.get_price_input(contract_address_one, contract_address_two, 10**18) / 10**6
        #print(contract_address_one, network_name, contract_address_two, price)
        #print(f"Preis von { contract_address_one } {contract_address_two }on Network: {network_name} : {price:.6f}")
    except Exception as e:
        print(f"Fehler no data: {e}")

    return price_in_usdc

def format_price(price, decimals=2):
    """Formatiert den Preis auf die angegebene Anzahl von Dezimalstellen."""
    return f"{price:.{decimals}f}"



def compare_prices_across_networks(select_token_one, select_token_two, amount_in):
    prices = {}
    for network in networks.keys():
        token_in = contract_addresses[network].get(select_token_one)
        token_out = contract_addresses[network].get(select_token_two)
        
        if token_in and token_out:
            price = get_price_from_uniswap_v3(network, token_in, token_out, amount_in)
            if price:
                prices[network] = float(price)

    # Arbitrage prüfen
    if prices:
        max_net = max(prices, key=prices.get)
        min_net = min(prices, key=prices.get)
        spread = prices[max_net] - prices[min_net]
        if spread / prices[min_net] > 0.01:  # >1% Spread
            message = (
                f"*Arbitrage-Möglichkeit gefunden!*\n"
                f"{select_token_one} → {select_token_two}\n"
                f"{min_net}: {format_price(prices[min_net])} | "
                f"{max_net}: {format_price(prices[max_net])}\n"
                f"Spread: {format_price(spread)}"
            )
            send_telegram_message(message)
    return prices



# Starten der Abfrage
if __name__ == "__main__":
    # Nur Layer-2 Netzwerke verwenden
    layer2_networks = ["optimism", "arbitrum", "polygon"]
    select_token_one = "WETH"
    select_token_two = "USDC"
    amount_in = 1  # z.B. 1 WETH

    prices = {}
    for network in layer2_networks:
        token_in = contract_addresses[network].get(select_token_one)
        token_out = contract_addresses[network].get(select_token_two)

        if not token_in or not token_out:
            print(f"Token-Adresse fehlt auf {network}.")
            continue

        price = get_price_from_uniswap_v3(network, token_in, token_out, amount_in)
        if price:
            prices[network] = float(price)
            print(f"{network.title()}: {format_price(price)} {select_token_two} für {amount_in} {select_token_one}")
        else:
            print(f"Preis konnte auf {network} nicht abgerufen werden.")

    # Arbitrage-Erkennung
    if len(prices) >= 2:
        max_net = max(prices, key=prices.get)
        min_net = min(prices, key=prices.get)
        spread = prices[max_net] - prices[min_net]
        spread_pct = (spread / prices[min_net]) * 100

        if spread_pct > 1:  # Arbitrage nur wenn >1% Unterschied
            message = (
                f"🚨 *Arbitrage-Möglichkeit erkannt!*\n"
                f"{select_token_one} → {select_token_two}\n"
                f"📉 Günstig: {min_net} – {format_price(prices[min_net])}\n"
                f"📈 Teuer: {max_net} – {format_price(prices[max_net])}\n"
                f"🔁 Spread: {format_price(spread)} ({spread_pct:.2f}%)"
            )
            print("\n" + message)
            send_telegram_message(message)
        else:
            print(f"\nKein signifikanter Arbitrage-Spread. Max. Spread: {spread_pct:.2f}%")
    else:
        print("Nicht genügend Preisdaten für Arbitragevergleich.")




