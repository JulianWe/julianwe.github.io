# How to create a Chainlink Operator Node

![](../chainlink/images/chainlink.jpg)

[Docs](https://docs.chain.link/)


**Run Ethereum Client**
```sh
docker pull ethereum/client-go:latest

mkdir ~/.geth-goerli && cd ~/.geth-goerli

docker run --name eth -p 8546:8546 -v ~/.geth-goerli:/geth -it \
    ethereum/client-go --goerli --ws --ipcdisable \
    --ws.addr 0.0.0.0 --ws.origins="*" --datadir /geth

```


**create alchemy or infura account**
ETH_URL=wss://eth-goerli.alchemyapi.io/v2/YOUR_PROJECT_ID
ETH_URL=wss://goerli.infura.io/ws/v3/YOUR_PROJECT_ID

ETH_URL=wss://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3
https://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3


**create postgres database**
```sh
docker run --name cl-postgres -e POSTGRES_PASSWORD=test0815test0815 -p 5432:5432 -d postgres
```


**create toml config**


```sh
mkdir ~/.chainlink-goerli && cd ~/.chainlink-goerli


echo "[Log]
Level = 'warn'

[WebServer]
AllowOrigins = '*'
SecureCookies = false

[WebServer.TLS]
HTTPSPort = 0

[[EVM]]
ChainID = '5'

[[EVM.Nodes]]
Name = 'Goerli'
WSURL = 'wss://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3'
HTTPURL = 'https://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3'
" > ~/.chainlink-goerli/config.toml
```


**create database password config**
```sh
echo "[Password]
Keystore = 'test0815test0815'
[Database]
URL = 'postgresql://postgres:test0815test0815@host.docker.internal:5432/postgres?sslmode=disable'
" > ~/.chainlink-goerli/secrets.toml
```


**run chainlink operator container**
```sh
cd ~/.chainlink-goerli && docker run --platform linux/x86_64/v8 --name chainlink -v ~/.chainlink-goerli:/chainlink -it -p 6688:6688 --add-host=host.docker.internal:host-gateway smartcontract/chainlink:2.0.0 node -config /chainlink/config.toml -secrets /chainlink/secrets.toml start

Enter API EMail:
Enter API Password:
```

**Connect chainlink UI**
http://localhost:6688

![](../chainlink/images/Operator.jpg)








# How to setup your own Operator Smart Contract

[Chainlink Testnet Token](https://faucets.chain.link/goerli)
[Chainlink Docs Fulfilling Request](https://docs.chain.link/chainlink-nodes/v1/fulfilling-requests)


[Remix Ethereum IDE](https://remix.ethereum.org/#url=https://docs.chain.link/samples/ChainlinkNodes/Operator.sol&lang=en&optimize=false&runs=200&evmVersion=null&version=soljson-v0.7.6+commit.7338295f.js)

**In Remix IDE Select compiler version '0.7.6'**
```java
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;
import "@chainlink/contracts/src/v0.7/Operator.sol";
```



**[ChainLink Contract Addresses:](https://docs.chain.link/resources/link-token-contracts)** 

**Goerli Testnet: 0x326C977E6efc84E512bB9C30f76E30c160eD06FB**
**Ethereum Mainnet: 0x514910771AF9Ca656af840dff83E8264EcF986CA**
Set 'LINK' Contract and 'OWNER' values and click transact.
![](../chainlink/images/deploy_contract.jpg)

**Note: the output shows your newly deployed operator smart contract: 0xfc5F20476E6289c7120A89D45e383EB28603152f**
```sh
[view on etherscan](https://goerli.etherscan.io/tx/0xebeea65d9e90c804b049a8d34e115f88ea14ea49b267d2843a2e2ef8f0ee7382)
[block:9412412 txIndex:11]from: 0x0f0...f05E5to: Operator.(constructor)value: 0 weidata: 0x60a...f05e5logs: 0hash: 0xfd1...938e7
status	true Transaction mined and execution succeed
transaction hash	0xebeea65d9e90c804b049a8d34e115f88ea14ea49b267d2843a2e2ef8f0ee7382
block hash	0xfd1c521f5cbd50873b056f5a34176ae2f33137abf326ca15b878c15fdc3938e7
block number	9412412
contract address	0xfc5F20476E6289c7120A89D45e383EB28603152f
from	0x0f0d2BF29AAe4E6D8d646F967Df8c49B28Df05E5
to	Operator.(constructor)
gas	3754948 gas
transaction cost	3754948 gas 
input	0x60a...f05e5
decoded input	{
	"address link": "0x326C977E6efc84E512bB9C30f76E30c160eD06FB",
	"address owner": "0x0f0d2BF29AAe4E6D8d646F967Df8c49B28Df05E5"
}
```


**Copy your Chainlink node address from Operator ui under 'settings' & 'key management': 0x321f40D5D7f678A35DCfC15Df852135F2c53e1AA**
![](../chainlink/images/ChainLink_Operator.jpg)


[Chainlink Smart Contract (v0.7) that we deployed on GitHub](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.7/Operator.sol)
With the Following fuctions:
![](../chainlink/images/deployed_contract.jpg)

and call the functions 'setAuthorizedSenders' & 'isAuthorizedSender' with the address of your node (in my case the array: '["0x321f40D5D7f678A35DCfC15Df852135F2c53e1AA"]') to verify that your chainlink node address can call the operator contract. The function must return true. You can use Remix IDE or instead Etherscan: https://goerli.etherscan.io/address/0xfc5f20476e6289c7120a89d45e383eb28603152f#writeContract

![](../chainlink/images/Etherscan_CSC.jpg)



# Add a Job to your Node

