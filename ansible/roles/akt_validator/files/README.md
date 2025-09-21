# Setup Akash Validator


**configure variables**
```sh
AKASH_NET="https://raw.githubusercontent.com/akash-network/net/main/mainnet"
export AKASH_CHAIN_ID="$(curl -s "$AKASH_NET/chain-id.txt")"
```

**create staking validator**
```sh
provider-services tx staking create-validator \
  --amount=1000000uakt \
  --pubkey="$(akash tendermint show-validator)" \
  --moniker="$AKASH_MONIKER" \
  --chain-id="$AKASH_CHAIN_ID" \
  --commission-rate="0.10" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1" \
  --gas="auto" \
  --gas-prices="0.0025uakt" \
  --gas-adjustment=1.5 \
  --from="$AKASH_KEY_NAME" 
```

**create keybase.io account https://keybase.io/ and creyte pgp key for your identity**
```sh
provider-services tx staking edit-validator
  --new-moniker="$AKASH_MONIKER" \
  --website="https://akash.network" \
  --identity=51A04EF97948D704 \
  --details="Validator" \
  --chain-id="$AKASH_CHAIN_ID" \
  --gas="auto" \
  --gas-prices="0.0025uakt" \
  --gas-adjustment=1.5 \
  --from="$AKASH_KEY_NAME" \
  --commission-rate="0.10" 
```

**view validator description**
```sh
provider-services query staking validator $AKASH_VALIDATOR_ADDRESS
```

**Track Validator Signing Information**
```sh
provider-services query slashing signing-info $AKASH_VALIDATOR_PUBKEY \
  --chain-id="$AKASH_CHAIN_ID"
```

**start provider services**
```sh
provider-services start
```

**provider services status**
```sh
provider-services status
```
