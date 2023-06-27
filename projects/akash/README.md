# ☁️ [Akash](https://akash.network/) deployment Tutorial 🐇

![Akash](app/images/Akash.jpg)

## About

**Censorship-resistant, permissionless, and self-sovereign, Akash Network is the world’s first open source cloud. $AKT**

## About

| Key | Value |
| --- | --- |
| `Source` | 🕳️ [Documentation](https://docs.akash.network/guides/deploy) |
| `Tutorial Author` | ☕ `Julian Wendland` |
| `$AKT Address` | `akash1srujzhj2v9fkzhnn635udlczyhdpetuh34mhad` |

## Variables

:information_source: **Note:** you can always check if all the required variables are set using "echo $variable" before your command.
|Name|Description|Example values |
|---|---|---|
|`AKASH_NET`| The URL of Akash Network. In This Tutorial we are using Mainnet | `https://raw.githubusercontent.com/ovrclk/net/master/mainnet` |
|`AKASH_VERSION`| Akash Version. | `0.10.1` |
|`AKASH_NODE`| Akash network configuration base URL. | `http://rpc.akash.forbole.com:80` |
|`AKASH_CHAIN_ID`| Chain ID of the Akash network connecting to. | `akashnet-2` |
|`ACCOUNT_ADDRESS`| The address of your account. | `akash1srujzhj2v9fkzhnn635udlczyhdpetuh34mhad` |
|`KEYRING_BACKEND`| Keyring backend to use for local keys. (os,file or test) | `file` |
|`KEY_NAME` | The name of the key you will be deploying from. | `julian` |

# Prepare `akash` environment ☁️

## 🏳️ Start Installation

```sh
cd ~

brew untap ovrclk/tap
brew tap akash-network/tap
brew install akash-provider-services

brew install jq -y
brew install unzip -y
brew install coreutils -y 

curl -sfL https://raw.githubusercontent.com/akash-network/node/master/install.sh | bash
curl -s "$AKASH_NET/genesis.json" > genesis.json 
curl -s "$AKASH_NET/seed-nodes.txt" | paste -d, -s
curl -s "$AKASH_NET/peer-nodes.txt" | paste -d, -s

sudo mv ./bin/akash /usr/local/bin
sudo mv ./bin/provider-services /usr/local/bin
```

**Setup required variables for Installation & later use. `AKASH_NET`,`AKASH_VERSION`, `AKASH_NODE` & `AKASH_CHAIN_ID`**

```sh
export AKASH_NET="https://raw.githubusercontent.com/akash-network/net/master/mainnet"
export AKASH_VERSION="$(curl -s https://api.github.com/repos/akash-network/provider/releases/latest | jq -r '.tag_name')"
export AKASH_NODE="$(curl -s "$AKASH_NET/rpc-nodes.txt" | shuf -n 1)"
export AKASH_CHAIN_ID="$(curl -s "$AKASH_NET/chain-id.txt")"
export AKASH_KEYRING_BACKEND=os

export AKASH_GAS=auto
export AKASH_GAS_ADJUSTMENT=1.25
export AKASH_GAS_PRICES=0.025uakt
export AKASH_SIGN_MODE=amino-json

# Check variables
echo AKASH_NET: $AKASH_NET, AKASH_VERSION: $AKASH_VERSION, AKASH_VERSION, AKASH_NODE: $AKASH_NODE, AKASH_CHAIN_ID:  $AKASH_CHAIN_ID, AKASH_KEYRING_BACKEND:  $AKASH_KEYRING_BACKEND, AKASH_GAS: $AKASH_GAS, AKASH_ADJUSTMENTS:  $AKASH_GAS_ADJUSTMENT, AKASH_GAS_PRICES:  $AKASH_GAS_PRICES, AKASH_SIGN_MODE: $AKASH_SIGN_MODE

```

## 💳 Wallet Setup

**Setup required variables `KEY_NAME` and `KEYRING_BACKEND` for wallet creation**

```sh
export AKASH_KEY_NAME=julian
```

**🔑 How to create key if you haven't yet setup a key**

```sh
akash keys add $AKASH_KEY_NAME  --keyring-backend $AKASH_KEYRING_BACKEND
provider-services keys add $AKASH_KEY_NAME

- name: julian
  type: local
  address: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A3vv0umfPwqVh24RYmVIa0CkfSQd/09gOR70o7tsRiPW"}'
  mnemonic: ""


**Important** write this mnemonic phrase in a safe place.
It is the only way to recover your account if you ever forget your password.

******** ******** ******** ******** ******** ******** ******** ******** ******** ******** ********
```
:warning: **Important** write this mnemonic phrase in a safe place. It is the only way to recover your account if you ever forget your password.


**How to export keys** 🔒

```sh
akash keys export $AKASH_KEY_NAME --keyring-backend $AKASH_KEYRING_BACKEND 
                     
Enter passphrase to encrypt the exported key: ********
-----BEGIN TENDERMINT PRIVATE KEY-----
kdf: bcrypt
salt: **************************
type: secp256k1
********************************
-----END TENDERMINT PRIVATE KEY-----
```


**How to recover keys** 🔓

```sh
akash keys add $AKASH_KEY_NAME --keyring-backend $AKASH_KEYRING_BACKEND --recover
provider-services keys add $AKASH_KEY_NAME --keyring-backend $AKASH_KEYRING_BACKEND --recover
```

**📬 How to retrieve and export `ACCOUNT_ADDRESS` as variable**

```sh
export ACCOUNT_ADDRESS=$(akash --keyring-backend $AKASH_KEYRING_BACKEND keys show $AKASH_KEY_NAME -a)
or
export ACCOUNT_ADDRESS="$(provider-services keys show $AKASH_KEY_NAME -a)"

echo $ACCOUNT_ADDRESS
akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z
```

**💰 How to check if there is enought `$AKT` to send transactions**

The balance indicated is denominated in uAKT (AKT x 10^-6) We're now setup to deploy.

```sh
akash query bank balances $ACCOUNT_ADDRESS --node $AKASH_NODE 
balances:
- amount: "20000000"
  denom: uakt
pagination:
  next_key: null
  total: "0"
```

ℹ️ **Note: You can buy `$AKT` on [BitMax](https://bitmax.io/register?inviteCode=LQDS1MMP) using this link or [Osmosis](https://app.osmosis.zone/)** and withdraw them to your deployment `ACCOUNT_ADDRESS`

## 📜 Prepare for deployment SDL File

[Choose deployment image](https://github.com/ovrclk/awesome-akash)
Create a deployment configuration file: `deploy.yml` to deploy the `ovrclk/lunie-light` for [Lunie Light](https://github.com/ovrclk/lunie-light) Node app container using [SDL](https://github.com/ovrclk/docs/blob/5d695ab63f391ebf255d48859ed3f626040fbf47/sdl/README.md):

```sh
cat > deploy.yml <<EOF
---
version: '2.0'
services:
  webapp:
    image: 'victorynox0815/docker-repo:webapp'
    expose:
      - port: 80
        as: 8080
        to:
          - global: true
profiles:
  compute:
    webapp:
      resources:
        cpu:
          units: 2
        memory:
          size: 512Mi
        storage:
          - size: 10Gi
  placement:
    dcloud:
      pricing:
        webapp:
          denom: uakt
          amount: 1000
deployment:
  webapp:
    dcloud:
      profile: webapp
      count: 1
EOF
```

**How to generate certificate & Publish Cert to the Blockchain** `requires $AKT fees`

```sh
provider-services tx cert generate client --from $AKASH_KEY_NAME
provider-services tx cert publish client --from $AKASH_KEY_NAME

confirm transaction before signing and broadcasting [y/N]: y

```

⚠️ **Important** certificate needs to be created only once per account and can be used across all deployments.

**How to revoke certificate** `requires $AKT fees`

```sh
provider-services tx cert revoke --from=$AKASH_KEY_NAME --node=$AKASH_NODE
```

## 💣 How to deploy

`requires $AKT fees`

```sh
provider-services tx deployment create deploy_webapp.yml --from $AKASH_KEY_NAME

```

You should see a response similar to:

```json
{
    "body": {
        "messages": [
            {
                "@type": "/akash.deployment.v1beta2.MsgCreateDeployment",
                "id": {
                    "owner": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z",
                    "dseq": "11679305"
                },
                "groups": [
                    {
                        "name": "dcloud",
                        "requirements": {
                            "signed_by": {
                                "all_of": [],
                                "any_of": []
                            },
                            "attributes": []
                        },
                        "resources": [
                            {
                                "resources": {
                                    "cpu": {
                                        "units": {
                                            "val": "2000"
                                        },
                                        "attributes": []
                                    },
                                    "memory": {
                                        "quantity": {
                                            "val": "536870912"
                                        },
                                        "attributes": []
                                    },
                                    "storage": [
                                        {
                                            "name": "default",
                                            "quantity": {
                                                "val": "10737418240"
                                            },
                                            "attributes": []
                                        }
                                    ],
                                    "endpoints": [
                                        {
                                            "kind": "RANDOM_PORT",
                                            "sequence_number": 0
                                        }
                                    ]
                                },
                                "count": 1,
                                "price": {
                                    "denom": "uakt",
                                    "amount": "1000.000000000000000000"
                                }
                            }
                        ]
                    }
                ],
                "version": "ryDgGMFLpGX7MGi5A4rADG5Jpr6hfOipQcNGLUa7gFc=",
                "deposit": {
                    "denom": "uakt",
                    "amount": "5000000"
                },
                "depositor": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
            }
        ],
        "memo": "",
        "timeout_height": "0",
        "extension_options": [],
        "non_critical_extension_options": []
    },
    "auth_info": {
        "signer_infos": [],
        "fee": {
            "amount": [
                {
                    "denom": "uakt",
                    "amount": "2981"
                }
            ],
            "gas_limit": "119215",
            "payer": "",
            "granter": ""
        }
    },
    "signatures": []
}

confirm transaction before signing and broadcasting [y/N]: y
{
    "height": "11679307",
    "txhash": "05815E511FF30B1C46C76794880F5A7E74FBA5A86BDD40699CB820944025B014",
    "codespace": "",
    "code": 0,
    "data": "0A2F0A2D2F616B6173682E6465706C6F796D656E742E763162657461322E4D73674372656174654465706C6F796D656E74",
    "raw_log": "[{\"events\":[{\"type\":\"akash.v1\",\"attributes\":[{\"key\":\"module\",\"value\":\"deployment\"},{\"key\":\"action\",\"value\":\"deployment-created\"},{\"key\":\"version\",\"value\":\"af20e018c14ba465fb3068b9038ac00c6e49a6bea17ce8a941c3462d46bb8057\"},{\"key\":\"owner\",\"value\":\"akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z\"},{\"key\":\"dseq\",\"value\":\"11679305\"},{\"key\":\"module\",\"value\":\"market\"},{\"key\":\"action\",\"value\":\"order-created\"},{\"key\":\"owner\",\"value\":\"akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z\"},{\"key\":\"dseq\",\"value\":\"11679305\"},{\"key\":\"gseq\",\"value\":\"1\"},{\"key\":\"oseq\",\"value\":\"1\"}]},{\"type\":\"coin_received\",\"attributes\":[{\"key\":\"receiver\",\"value\":\"akash14pphss726thpwws3yc458hggufynm9x77l4l2u\"},{\"key\":\"amount\",\"value\":\"5000000uakt\"}]},{\"type\":\"coin_spent\",\"attributes\":[{\"key\":\"spender\",\"value\":\"akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z\"},{\"key\":\"amount\",\"value\":\"5000000uakt\"}]},{\"type\":\"message\",\"attributes\":[{\"key\":\"action\",\"value\":\"/akash.deployment.v1beta2.MsgCreateDeployment\"},{\"key\":\"sender\",\"value\":\"akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z\"}]},{\"type\":\"transfer\",\"attributes\":[{\"key\":\"recipient\",\"value\":\"akash14pphss726thpwws3yc458hggufynm9x77l4l2u\"},{\"key\":\"sender\",\"value\":\"akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z\"},{\"key\":\"amount\",\"value\":\"5000000uakt\"}]}]}]",
    "logs": [
        {
            "msg_index": 0,
            "log": "",
            "events": [
                {
                    "type": "akash.v1",
                    "attributes": [
                        {
                            "key": "module",
                            "value": "deployment"
                        },
                        {
                            "key": "action",
                            "value": "deployment-created"
                        },
                        {
                            "key": "version",
                            "value": "af20e018c14ba465fb3068b9038ac00c6e49a6bea17ce8a941c3462d46bb8057"
                        },
                        {
                            "key": "owner",
                            "value": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
                        },
                        {
                            "key": "dseq",
                            "value": "11679305"
                        },
                        {
                            "key": "module",
                            "value": "market"
                        },
                        {
                            "key": "action",
                            "value": "order-created"
                        },
                        {
                            "key": "owner",
                            "value": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
                        },
                        {
                            "key": "dseq",
                            "value": "11679305"
                        },
                        {
                            "key": "gseq",
                            "value": "1"
                        },
                        {
                            "key": "oseq",
                            "value": "1"
                        }
                    ]
                },
                {
                    "type": "coin_received",
                    "attributes": [
                        {
                            "key": "receiver",
                            "value": "akash14pphss726thpwws3yc458hggufynm9x77l4l2u"
                        },
                        {
                            "key": "amount",
                            "value": "5000000uakt"
                        }
                    ]
                },
                {
                    "type": "coin_spent",
                    "attributes": [
                        {
                            "key": "spender",
                            "value": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
                        },
                        {
                            "key": "amount",
                            "value": "5000000uakt"
                        }
                    ]
                },
                {
                    "type": "message",
                    "attributes": [
                        {
                            "key": "action",
                            "value": "/akash.deployment.v1beta2.MsgCreateDeployment"
                        },
                        {
                            "key": "sender",
                            "value": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
                        }
                    ]
                },
                {
                    "type": "transfer",
                    "attributes": [
                        {
                            "key": "recipient",
                            "value": "akash14pphss726thpwws3yc458hggufynm9x77l4l2u"
                        },
                        {
                            "key": "sender",
                            "value": "akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z"
                        },
                        {
                            "key": "amount",
                            "value": "5000000uakt"
                        }
                    ]
                }
            ]
        }
    ],
    "info": "",
    "gas_wanted": "119215",
    "gas_used": "105941",
    "tx": null,
    "timestamp": "",
    "events": [
        {
            "type": "coin_spent",
            "attributes": [
                {
                    "key": "c3BlbmRlcg==",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "Mjk4MXVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "coin_received",
            "attributes": [
                {
                    "key": "cmVjZWl2ZXI=",
                    "value": "YWthc2gxN3hwZnZha20yYW1nOTYyeWxzNmY4NHoza2VsbDhjNWxhenc4ajg=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "Mjk4MXVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "transfer",
            "attributes": [
                {
                    "key": "cmVjaXBpZW50",
                    "value": "YWthc2gxN3hwZnZha20yYW1nOTYyeWxzNmY4NHoza2VsbDhjNWxhenc4ajg=",
                    "index": true
                },
                {
                    "key": "c2VuZGVy",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "Mjk4MXVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "message",
            "attributes": [
                {
                    "key": "c2VuZGVy",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                }
            ]
        },
        {
            "type": "tx",
            "attributes": [
                {
                    "key": "ZmVl",
                    "value": "Mjk4MXVha3Q=",
                    "index": true
                },
                {
                    "key": "ZmVlX3BheWVy",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                }
            ]
        },
        {
            "type": "tx",
            "attributes": [
                {
                    "key": "YWNjX3NlcQ==",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHovMQ==",
                    "index": true
                }
            ]
        },
        {
            "type": "tx",
            "attributes": [
                {
                    "key": "c2lnbmF0dXJl",
                    "value": "UGVJbEIrdStybHZZaVdhbk1EWmtNTlRMVzJOT09uSFFFcnVKRnF3WVR4cGlDSzNybHJGM0pSZWR0eFR0eWdXQmNaajg4Qk14WVlVdXRWT1hFWjZnUGc9PQ==",
                    "index": true
                }
            ]
        },
        {
            "type": "message",
            "attributes": [
                {
                    "key": "YWN0aW9u",
                    "value": "L2FrYXNoLmRlcGxveW1lbnQudjFiZXRhMi5Nc2dDcmVhdGVEZXBsb3ltZW50",
                    "index": true
                }
            ]
        },
        {
            "type": "akash.v1",
            "attributes": [
                {
                    "key": "bW9kdWxl",
                    "value": "ZGVwbG95bWVudA==",
                    "index": true
                },
                {
                    "key": "YWN0aW9u",
                    "value": "ZGVwbG95bWVudC1jcmVhdGVk",
                    "index": true
                },
                {
                    "key": "dmVyc2lvbg==",
                    "value": "YWYyMGUwMThjMTRiYTQ2NWZiMzA2OGI5MDM4YWMwMGM2ZTQ5YTZiZWExN2NlOGE5NDFjMzQ2MmQ0NmJiODA1Nw==",
                    "index": true
                },
                {
                    "key": "b3duZXI=",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "ZHNlcQ==",
                    "value": "MTE2NzkzMDU=",
                    "index": true
                }
            ]
        },
        {
            "type": "akash.v1",
            "attributes": [
                {
                    "key": "bW9kdWxl",
                    "value": "bWFya2V0",
                    "index": true
                },
                {
                    "key": "YWN0aW9u",
                    "value": "b3JkZXItY3JlYXRlZA==",
                    "index": true
                },
                {
                    "key": "b3duZXI=",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "ZHNlcQ==",
                    "value": "MTE2NzkzMDU=",
                    "index": true
                },
                {
                    "key": "Z3NlcQ==",
                    "value": "MQ==",
                    "index": true
                },
                {
                    "key": "b3NlcQ==",
                    "value": "MQ==",
                    "index": true
                }
            ]
        },
        {
            "type": "coin_spent",
            "attributes": [
                {
                    "key": "c3BlbmRlcg==",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "NTAwMDAwMHVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "coin_received",
            "attributes": [
                {
                    "key": "cmVjZWl2ZXI=",
                    "value": "YWthc2gxNHBwaHNzNzI2dGhwd3dzM3ljNDU4aGdndWZ5bm05eDc3bDRsMnU=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "NTAwMDAwMHVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "transfer",
            "attributes": [
                {
                    "key": "cmVjaXBpZW50",
                    "value": "YWthc2gxNHBwaHNzNzI2dGhwd3dzM3ljNDU4aGdndWZ5bm05eDc3bDRsMnU=",
                    "index": true
                },
                {
                    "key": "c2VuZGVy",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                },
                {
                    "key": "YW1vdW50",
                    "value": "NTAwMDAwMHVha3Q=",
                    "index": true
                }
            ]
        },
        {
            "type": "message",
            "attributes": [
                {
                    "key": "c2VuZGVy",
                    "value": "YWthc2gxdWZ0M3dxd3puc2g1ZmZwdHIwZ2c0MHIyc3I4dmhkbGdhbjB5NHo=",
                    "index": true
                }
            ]
        }
    ]
}
```


and export the following variables `DSEQ` Deployment Sequence, `GSEQ` Group Sequence, `OSEQ` Order Sequence from **your** deployment.

```sh
export DSEQ=11679305
export OSEQ=1
export GSEQ=1


echo $DSEQ $GSEQ $OSEQ
```


```sh 
provider-services query market bid list --owner=$ACCOUNT_ADDRESS --node $AKASH_NODE --dseq $DSEQ 
bids:
- bid:
    bid_id:
      dseq: "11679305"
      gseq: 1
      oseq: 1
      owner: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z
      provider: akash1qhjtxmacslmefm3v4sn5ggq6ed9jn83cy2rjd0
    created_at: "11679309"
    price:
      amount: "36.069600000000000000"
      denom: uakt
    state: closed
  escrow_account:
    balance:
      amount: "0.000000000000000000"
      denom: uakt
    depositor: akash1qhjtxmacslmefm3v4sn5ggq6ed9jn83cy2rjd0
    funds:
      amount: "0.000000000000000000"
      denom: uakt
    id:
      scope: bid
      xid: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z/11679305/1/1/akash1qhjtxmacslmefm3v4sn5ggq6ed9jn83cy2rjd0
    owner: akash1qhjtxmacslmefm3v4sn5ggq6ed9jn83cy2rjd0
    settled_at: "11679458"
    state: closed
    transferred:
      amount: "0.000000000000000000"
      denom: uakt
- bid:
    bid_id:
      dseq: "11679305"
      gseq: 1
      oseq: 1
      owner: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z
      provider: akash1pev2y734effvxxn8rzkp5vqq0jmqq0y0s8hvjc
    created_at: "11679309"
    price:
      amount: "35.680000000000000000"
      denom: uakt
    state: closed
  escrow_account:
    balance:
      amount: "0.000000000000000000"
      denom: uakt
    depositor: akash1pev2y734effvxxn8rzkp5vqq0jmqq0y0s8hvjc
    funds:
      amount: "0.000000000000000000"
      denom: uakt
    id:
      scope: bid
      xid: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z/11679305/1/1/akash1pev2y734effvxxn8rzkp5vqq0jmqq0y0s8hvjc
    owner: akash1pev2y734effvxxn8rzkp5vqq0jmqq0y0s8hvjc
    settled_at: "11679361"
    state: closed
    transferred:
      amount: "0.000000000000000000"
      denom: uakt
- bid:
    bid_id:
      dseq: "11679305"
      gseq: 1
      oseq: 1
      owner: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z
      provider: akash1pl9sm32kt0xmcyfwjsf9guu9f93yf8p6k7grtn
    created_at: "11679309"
    price:
      amount: "21.000000000000000000"
      denom: uakt
    state: closed
  escrow_account:
    balance:
      amount: "0.000000000000000000"
      denom: uakt
    depositor: akash1pl9sm32kt0xmcyfwjsf9guu9f93yf8p6k7grtn
    funds:
      amount: "0.000000000000000000"
      denom: uakt
    id:
      scope: bid
      xid: akash1uft3wqwznsh5ffptr0gg40r2sr8vhdlgan0y4z/11679305/1/1/akash1pl9sm32kt0xmcyfwjsf9guu9f93yf8p6k7grtn
    owner: akash1pl9sm32kt0xmcyfwjsf9guu9f93yf8p6k7grtn
    settled_at: "11679361"
    state: closed
    transferred:
      amount: "0.000000000000000000"
      denom: uakt
```


**How to list market bid**

```sh
provider-services query market bid list --owner=$ACCOUNT_ADDRESS --node $AKASH_NODE --dseq  $DSEQ 
```


**create & confirm market lease**

```sh
export PROVIDER="akash1qhjtxmacslmefm3v4sn5ggq6ed9jn83cy2rjd0"

provider-services tx market lease create --dseq $DSEQ --provider $PROVIDER --from $AKASH_KEY_NAME
provider-services query market lease list --owner $AKASH_ACCOUNT_ADDRESS --node $AKASH_NODE --dseq $DSEQ

```


**How to get market lease**

```sh
akash query market lease list --owner $ACCOUNT_ADDRESS --chain-id $AKASH_CHAIN_ID --node $AKASH_NODE
akash query market lease get --owner $ACCOUNT_ADDRESS --dseq $DSEQ --oseq $OSEQ --gseq $GSEQ --provider $PROVIDER --chain-id $AKASH_CHAIN_ID --node $AKASH_NODE
```



```text
jw@ChainLink:~$ akash deploy create deploy.yml --from $KEY_NAME --chain-id $AKASH_CHAIN_ID --keyring-backend $KEYRING_BACKEND --node $AKASH_NODE --fees 5000uakt
Enter keyring passphrase:
I[2021-03-14|16:43:00.592] tx sent successfully                         hash=58F0A15FCCB40B79BB98031DC43FB99DB2DB0824D966EE45B94C977EB39703B8 code=0 codespace= action=create-deployment dseq=83887
I[2021-03-14|16:43:03.834] deployment created                           addr=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket dseq=83887
I[2021-03-14|16:43:03.834] order for deployment created                 addr=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket dseq=83887 oseq=1
I[2021-03-14|16:43:09.767] bid for order created                        addr=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket dseq=83887 oseq=1 price=100uakt
D[2021-03-14|16:43:09.767] Processing bid
D[2021-03-14|16:43:09.767] All groups have at least one bid
I[2021-03-14|16:43:24.767] Done waiting on bids                         qty=1
I[2021-03-14|16:43:24.767] Winning bid                                  gseq=1 price=100uakt provider=akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz
I[2021-03-14|16:43:28.417] All expected leases created                  addr=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket dseq=83887
I[2021-03-14|16:43:28.417] lease for order created                      addr=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket dseq=83887 oseq=1 price=100uakt
I[2021-03-14|16:43:28.417] Waiting on leases to be ready                leaseQuantity=1
D[2021-03-14|16:43:28.417] Checking status of lease                     lease=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket/83887/1/1/akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz
D[2021-03-14|16:43:28.528] Could not get lease status                   lease=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket/83887/1/1/akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz err="remote server returned 404"
I[2021-03-14|16:43:28.918] sending manifest to provider                 action=send-manifest provider=akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz dseq=83887
D[2021-03-14|16:43:29.055] Could not get lease status                   lease=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket/83887/1/1/akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz err="remote server returned 503"
I[2021-03-14|16:43:36.133] service ready                                lease=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket/83887/1/1/akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz service=web
I[2021-03-14|16:43:36.133] lease ready                                  leaseID=akash1ny2lt9mcfet63k8ur2ue9xqaunxe80we64hket/83887/1/1/akash1ccktptfkvdc67msasmesuy5m7gpc76z75kukpz
{
 "name": "web",
 "available": 1,
 "total": 1,
 "uris": [
  "5pvofe14fp8uhcmi1lhij63g0s.ingress.ams1p0.mainnet.akashian.io"
 ],
 "observed_generation": 1,
 "replicas": 1,
 "updated_replicas": 1,
 "ready_replicas": 1,
 "available_replicas": 1
}
```

ℹ️ **Note:** 🎉 `SERVICE_NAME` is "web"

```sh
export SERVICE_NAME=webapp
```


**How to verify deployment creation**

```sh
# List all deloyments
akash query deployment list --owner $ACCOUNT_ADDRESS --chain-id $AKASH_CHAIN_ID --node $AKASH_NODE

# List specific dployment
akash query deployment get --owner $ACCOUNT_ADDRESS --node $AKASH_NODE --dseq $DSEQ
```


**🔍 How to view deployment**

```sh
akash provider lease-status --log_level=info --dseq $DSEQ --from $KEY_NAME --home ~/.akash --provider $PROVIDER --keyring-backend $AKASH_KEYRING_BACKEND --node $AKASH_NODE
```


**📝 How to view logs**

```sh
akash --node $AKASH_NODE provider service-logs --service $SERVICE_NAME --owner $ACCOUNT_ADDRESS --dseq $DSEQ --gseq $GSEQ --oseq $OSEQ --provider $PROVIDER

akash --node $AKASH_NODE provider lease-logs --from $ACCOUNT_ADDRESS --provider $PROVIDER --dseq $DSEQ --keyring-backend $AKASH_KEYRING_BACKEND --service SERVICE_NAME --home ~/.akash 
```


**♻️ How to Update Deployment** `requires $AKT fees`

```sh
echo akash tx deployment update deploy.yml --from $KEY_NAME --node $AKASH_NODE --chain-id $AKASH_CHAIN_ID --fees 5000uakt --keyring-backend $AKASH_KEYRING_BACKEND --dseq $DSEQ 
```


**❌ How to close deployment** `requires $AKT fees`

```sh
provider-services tx deployment close --dseq $AKASH_DSEQ  --owner $AKASH_ACCOUNT_ADDRESS --from $AKASH_KEY_NAME 

echo akash tx deployment close --node $AKASH_NODE --chain-id $AKASH_CHAIN_ID --dseq $DSEQ  --owner $ACCOUNT_ADDRESS --from $KEY_NAME --keyring-backend $AKASH_KEYRING_BACKEND -y --fees 5000uakt  --gas=auto
```

### 💡 End 💲 `AKT` 🚀 🌕
