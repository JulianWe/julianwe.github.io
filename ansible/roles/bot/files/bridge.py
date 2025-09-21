from web3 import Web3
import requests

# Ethereum Mainnet URL (Layer 1)
L1_RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"

# Layer 2 RPC URLs (Arbitrum, Optimism, zkSync)
L2_RPC_URLS = {
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
    "zksync": "https://zksync2-mainnet.zksync.io",
}

# Bridge APIs URLs (This is pseudo - you'd need real bridge API endpoints)
BRIDGE_APIS = {
    "hop": "https://api.hop.exchange/v1",
    "celer": "https://api.cbridge.celer.network/v1",
    "connext": "https://router.api.connext.network",
}

# Initialize Web3 instance for Layer 1 (Ethereum Mainnet)
web3_l1 = Web3(Web3.HTTPProvider(L1_RPC_URL))

# Token contract ABI (ERC-20 Standard)
ERC20_ABI = '[...]'  # The ERC-20 contract ABI goes here

def get_token_balance(address, token_contract_address):
    """Get token balance of an address on Layer 1."""
    token_contract = web3_l1.eth.contract(address=token_contract_address, abi=ERC20_ABI)
    balance = token_contract.functions.balanceOf(address).call()
    return web3_l1.fromWei(balance, 'ether')

def approve_token_transfer(spender, amount, token_contract_address, private_key):
    """Approve tokens for bridging."""
    account = web3_l1.eth.account.privateKeyToAccount(private_key)
    token_contract = web3_l1.eth.contract(address=token_contract_address, abi=ERC20_ABI)
    
    # Create the transaction to approve
    transaction = token_contract.functions.approve(spender, amount).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3_l1.toWei('20', 'gwei'),
        'nonce': web3_l1.eth.getTransactionCount(account.address),
    })
    
    # Sign and send transaction
    signed_txn = web3_l1.eth.account.signTransaction(transaction, private_key=private_key)
    tx_hash = web3_l1.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3_l1.toHex(tx_hash)

def bridge_token_to_layer2(layer2, token_contract_address, amount, private_key):
    """Bridge tokens from Layer 1 to Layer 2."""
    if layer2 not in L2_RPC_URLS:
        raise ValueError(f"Unsupported Layer 2: {layer2}")
    
    # Example using Hop Protocol API for bridging
    if layer2 == "arbitrum":
        bridge_api_url = BRIDGE_APIS["hop"] + "/bridge"
        payload = {
            "fromChainId": 1,
            "toChainId": 42161,  # Arbitrum chain ID
            "token": token_contract_address,
            "amount": amount,
        }
    elif layer2 == "optimism":
        bridge_api_url = BRIDGE_APIS["celer"] + "/transfer"
        payload = {
            "src_chain_id": 1,
            "dest_chain_id": 10,  # Optimism chain ID
            "token_address": token_contract_address,
            "amount": amount,
        }
    elif layer2 == "zksync":
        bridge_api_url = BRIDGE_APIS["connext"] + "/xtransfer"
        payload = {
            "originDomain": "1",  # Ethereum Mainnet
            "destinationDomain": "zkSync",
            "asset": token_contract_address,
            "amount": amount,
        }

    # Send the bridge request (simplified example, you'd handle more complexity in a real use case)
    response = requests.post(bridge_api_url, json=payload)
    return response.json()

def bridge_token_from_l2(layer2, token_contract_address, amount, private_key):
    """Bridge tokens back from Layer 2 to Layer 1."""
    # Similar logic for bridging from L2 to L1
    if layer2 == "arbitrum":
        # Use the Arbitrum bridge API
        bridge_api_url = BRIDGE_APIS["hop"] + "/withdraw"
    elif layer2 == "optimism":
        bridge_api_url = BRIDGE_APIS["celer"] + "/withdraw"
    elif layer2 == "zksync":
        bridge_api_url = BRIDGE_APIS["connext"] + "/withdraw"
    
    # Payload for withdrawal
    payload = {
        "token_address": token_contract_address,
        "amount": amount,
    }
    
    response = requests.post(bridge_api_url, json=payload)
    return response.json()

# Example Usage:
private_key = "YOUR_PRIVATE_KEY"
user_address = "YOUR_WALLET_ADDRESS"
token_contract_address = "ERC20_CONTRACT_ADDRESS"

# 1. Get user balance on Layer 1
balance = get_token_balance(user_address, token_contract_address)
print(f"Balance on Layer 1: {balance} Tokens")

# 2. Approve tokens for bridging
amount_to_bridge = web3_l1.toWei(10, 'ether')  # Bridging 10 tokens
spender_address = "BRIDGE_CONTRACT_ADDRESS"
approve_tx = approve_token_transfer(spender_address, amount_to_bridge, token_contract_address, private_key)
print(f"Approve transaction hash: {approve_tx}")

# 3. Bridge tokens to Layer 2 (e.g., Arbitrum)
bridge_tx = bridge_token_to_layer2("arbitrum", token_contract_address, amount_to_bridge, private_key)
print(f"Bridging transaction response: {bridge_tx}")
