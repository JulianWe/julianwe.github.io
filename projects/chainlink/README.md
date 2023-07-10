# How to create a Chainlink Node

![](../chainlink/images/chainlink.jpg)

[Docs](https://docs.chain.link/)


**Run Ethereum Client**
```sh
docker pull ethereum/client-go:latest

mkdir ~/.geth-goerli

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
mkdir ~/.chainlink-goerli


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


**start chainlink container**
```sh
cd ~/.chainlink-goerli && docker run --platform linux/x86_64/v8 --name chainlink -v ~/.chainlink-goerli:/chainlink -it -p 6688:6688 --add-host=host.docker.internal:host-gateway smartcontract/chainlink:2.0.0 node -config /chainlink/config.toml -secrets /chainlink/secrets.toml start

Enter API EMail:
Enter API Password:
```

**Connect chainlink UI**
http://localhost:6688

![](../chainlink/images/Operator.jpg)

