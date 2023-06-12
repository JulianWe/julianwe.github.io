
# ☁️ [Sentinel DVPN](https://sentinel.co/) Tutorial 🐇

![Sentinel](images/sentinel.jpg)


| Key | Value |
| --- | --- |
| `Source ` | 🕳️ [Documentation](https://github.com/sentinel-official/cli-client) |
| `Tutorial Author ` | ☕ `Julian Wendland` |
| `$AKT Address` | `sent1nzsagwgzjmpcu0csx6xxmhhn5zuynwxfnghzmg` |


## Variables
|Name|Description|Example values |
|---|---|---|
|`ACCOUNT_ADDRESS`| The address of your account. | `akash1srujzhj2v9fkzhnn635udlczyhdpetuh34mhad` |
|`KEYRING_BACKEND`| Keyring backend to use for local keys. (os,file or test) | `file` |
|`KEY_NAME` | The name of the key you will be deploying from. | `julian` |


# Prepare `Sentinel` Installation ☁️
## 🏳️ Start Installation
```sh
brew install v2ray wireguard-tools
curl --silent https://raw.githubusercontent.com/sentinel-official/cli-client/master/scripts/install.sh | sh
```


## 💳 Wallet Setup 
**Setup required variables `KEY_NAME`  for wallet creation**
```sh
export KEY_NAME=sentinel
```

## Generate Mnemonic Passphrase 
```sh
sentinelcli keys mnemonic 
```

## Add Keys 
```sh
sentinelcli keys add sentinel --keyring-backend file
```

## OR Generate Multiple Keys for Multisig Wallet
```sh
You can create and store a multisig key by passing the list of key names stored in a keyring
and the minimum number of signatures required through --multisig-threshold. The keys are
sorted by address, unless the flag --nosort is set.
Example:

    keys add mymultisig --multisig "keyname1,keyname2,keyname3" --multisig-threshold 2
```

## Add Keys
```sh
sentinelcli keys add Sentinel --keyring-backend file  
Enter keyring passphrase:
Re-enter keyring passphrase:

- name: Sentinel
  type: local
  address: sent1nzsagwgzjmpcu0csx6xxmhhn5zuynwxfnghzmg
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"AqHdR4e6Pd+b3R86ijGBD0cNopUBW0jR7Al//zE8TTci"}'
  mnemonic: ""
```

## Query Nodes & select Node
```sh
sentinelcli query nodes \
    --home "${HOME}/.sentinelcli" \
    --node https://rpc.sentinel.co:443 \
    --status Active \
    --page 1
```

## Subscribe to Provider Node
```sh 
sentinelcli tx subscription subscribe-to-node \
    --home "${HOME}/.sentinelcli" \
    --keyring-backend file \
    --chain-id sentinelhub-2 \
    --node https://rpc.sentinel.co:443 \
    --gas-prices 0.1udvpn \
    --from Sentinel sentnode1qse6l5jc6nj95xrs86fzw53lsd8krl8ehv208x 1000
```


## Query Account subscription
```sh 
sentinelcli query subscriptions \
    --home "${HOME}/.sentinelcli" \
    --node https://rpc.sentinel.co:443 \
    --status Active \
    --page 1 \
    --address <ACCOUNT_ADDRESS>
```


## Connect 
```sh 
sudo sentinelcli connect \
    --home "${HOME}/.sentinelcli" \
    --keyring-backend file \
    --chain-id sentinelhub-2 \
    --node https://rpc.sentinel.co:443 \
    --gas-prices 0.1udvpn \
    --yes \
    --from <KEY_NAME> <SUBSCRIPTION_ID> <NODE_ADDRESS>
```






