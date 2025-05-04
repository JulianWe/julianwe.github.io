
# ☁️ [AIOZ Network](https://docs.aioz.network/aioz-depin/aioz-nodes/cli-node) - Setup CLI Node 🐇


![](../images/aioz_node.jpg)


```sh
# download aioznode
curl -LO https://github.com/AIOZNetwork/aioz-dcdn-cli-node/files/13561211/aioznode-linux-amd64-1.1.0.tar.gz
tar xzf aioznode-linux-amd64-1.1.0.tar.gz
mv aioznode-linux-amd64-1.1.0 aioznode

export PATH="$PATH:/aioznode"
```

```sh
# Verify the node is runnable
./aioznode version
1.1.0
```

```sh
# Create new private key
./aioznode keytool new --save-priv-key privkey.json
```
`--save-priv-key` write the private key to file


**IMPORTANT NOTE: Make sure to backup and secure your mnemonic phrase as it will be used in case of migration or recovering your node.**

**Run the node**
```sh
# Run the node
./aioznode start --home nodedata --priv-key-file privkey.json
```

`--home data folder of the node`

`--priv-key-file` the private key file which the node starts with. If you do not specify the private key file, the node will ask for it from the standard input stream.


**View reward**
```sh
# View reward
./aioznode reward balance
```

**Withdraw reward**
```sh
# Withdraw reward
./aioznode reward withdraw --address 0xfA66faf3Faa192277bAb21Ef547ebdB47617B1da --amount 1aioz --priv-key-file privkey.json
```

**Recover private key from mnemonic phrase**
```sh
# Recover private key from mnemonic phrase
./aioznode keytool recover "rain wing olive skate effort present long myself combine giant vote stay sweet bundle agree lock connect glide absent spider effort attitude enemy mouse" --save-priv-key privkey.json
```

`--save-priv-key` write the private key to file.


**or create docker container to run aioz node**
```sh
FROM ubuntu:latest

WORKDIR /root
RUN apt update && apt upgrade -y
RUN apt install curl -y
COPY privkey.json /root
RUN curl -LO https://github.com/AIOZNetwork/aioz-dcdn-cli-node/files/13561211/aioznode-linux-amd64-1.1.0.tar.gz
RUN tar xzf aioznode-linux-amd64-1.1.0.tar.gz
RUN mv aioznode-linux-amd64-1.1.0 /root/aioznode
COPY privkey.json /root
RUN /root/aioznode start --home nodedata --priv-key-file /root/privkey.json
```

