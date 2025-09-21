# Deploy Sentinel node on Akash Deployment

**install akash network cli tools**
```sh
mkdir akash
cd akash
brew untap ovrclk/tap
brew tap akash-network/tap
brew install akash-provider-services
```

**install akash provider services cli**
```sh
# This download may take several minutes to complete
curl -sfL https://raw.githubusercontent.com/akash-network/provider/main/install.sh | bash
sudo mv ./bin/provider-services /usr/local/bin
provider-services version
```

**setup wallet**
```sh
export AKASH_KEY_NAME=DeploymentWallet
export AKASH_KEYRING_BACKEND=os
provider-services keys add $AKASH_KEY_NAME
export AKASH_ACCOUNT_ADDRESS="$(provider-services keys show $AKASH_KEY_NAME -a)"
export AKASH_NET="https://raw.githubusercontent.com/akash-network/net/main/mainnet"
export AKASH_VERSION="$(curl -s https://api.github.com/repos/akash-network/provider/releases/latest | jq -r '.tag_name')"
export AKASH_CHAIN_ID="$(curl -s "$AKASH_NET/chain-id.txt")"
export AKASH_NODE="$(curl -s "$AKASH_NET/rpc-nodes.txt" | shuf -n 1)"
export AKASH_GAS=auto
export AKASH_GAS_ADJUSTMENT=1.25
export AKASH_GAS_PRICES=0.0025uakt
export AKASH_SIGN_MODE=amino-json

echo $AKASH_KEY_NAME $AKASH_ACCOUNT_ADDRESS

# How to recover Keys instead of creating a new wallet
provider-services keys add $AKASH_KEY_NAME --keyring-backend $AKASH_KEYRING_BACKEND --recover 
```

**check balance on your akash account address & fund your wallet using this link [crypto.com](https://crypto.com/app/x7oujro0iw)**
```sh
provider-services query bank balances --node $AKASH_NODE $AKASH_ACCOUNT_ADDRESS
```

**create deploy.yml file**

```sh
cat > deploy.yml <<EOF 
---
version: "2.0"
endpoints:
 uniq_name_endpoint: dvpn_on_akash # unique name, for example "dvpn_on_akash:", and enter this name in line 27 and 32.
    kind: ip
services:
  app:
    image: declab/sentinel_dvpn:0.7.1.1
    env:
      - "MNEMONIC_BASE64=b3pvbmUgY29taWMgY2FzdWFsIGVuZGxlc3MgcHVuY2ggaGFwcHkgYnVyc3QgcGhvdG8gaW5kdXN0cnkgZGlzbWlzcyBjbGVhbiBjb3JuIGNhc3RsZSBib3JkZXIgYmFjaGVsb3IgdmFyaW91cyBtb3NxdWl0byBkYW1hZ2Ugb3duIGFzcGVjdCBzaGVyaWZmIGZvY3VzIGFuc3dlciBtYWNoaW5l" # Mnemonic phrase encrypted with BASE64.
      - "MONIKER=dVPN on Akash Network v2RAY" # Your dVPN node name.
      - "REMOTE_PORT=8585" # Remote port for are connection sentinel client service.
      - "LISTEN_PORT=3333" # v2RAY listen port
      - "IPV4_ADDRESS=" # Node static IP address ( of leases section )
      - "RPC_ADDRESS=https://rpc.sentinel.co:443"
      
      - "GIGABYTE_PRICES=52573ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8,9204ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477,1180852ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783,122740ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518,15342624udvpn"
         # ^^Set the cost per 1 Gb of active traffic passed through your node.^^
         
      - "HOURLY_PRICES=18480ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8,770ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477,1871892ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783,18897ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518,10000000udvpn" # Set the cost per 1 hour of traffic passed through your node.
         
    expose:
      - port: 8585 # REMOTE_URL_PORT
        as: 8585
        to:
          - global: true
            ip: uniq_name_endpoint  # Name from string 3, for example "ip: dvpn_dimokus"
      - port: 3333 # LISTEN_PORT 
        as: 3333
        to:
          - global: true
            ip: uniq_name_endpoint  # Name from string 3, for example "ip: dvpn_dimokus"    
profiles:
  compute:
    app:
      resources:
        cpu:
          units: 1
        memory:
          size: 1Gi
        storage:
          size: 3Gi         
  placement:
    akash: 
      pricing:
        app:
          denom: uakt
          amount: 100000
deployment:
  app:
    akash:
      profile: app
      count: 1 
EOF

version: "2.0"
endpoints:
  unique_name_endpoint: dvpn_on_akash # unique name, for example "dvpn_on_akash:", and enter this name in line 27 and 32.
    kind: ip
services:
  app:
    image: declab/sentinel_dvpn_ssh:0.7.1.2
    
    env:
      - "SSH_KEY=ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKTNqCzRZVoWV5hbr4yj+mnV0ckEBfr68LC3BqZd3JsD jw" # Your SSH pubkey
      - "MNEMONIC_BASE64=b3pvbmUgY29taWMgY2FzdWFsIGVuZGxlc3MgcHVuY2ggaGFwcHkgYnVyc3QgcGhvdG8gaW5kdXN0cnkgZGlzbWlzcyBjbGVhbiBjb3JuIGNhc3RsZSBib3JkZXIgYmFjaGVsb3IgdmFyaW91cyBtb3NxdWl0byBkYW1hZ2Ugb3duIGFzcGVjdCBzaGVyaWZmIGZvY3VzIGFuc3dlciBtYWNoaW5l" # Mnemonic encrypted with BASE64.
      - "MONIKER=DVPN Node" # Your dVPN node name.
      - "REMOTE_PORT=8585" # TCP listen port.
      - "LISTEN_PORT=3333" # V2RAY listen port
      - "IPV4_ADDRESS=" # Node leased IP address (you will add it later)
      - "RPC_ADDRESS=https://rpc.sentinel.co:443"
      - "GIGABYTE_PRICES=52573ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8,9204ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477,1180852ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783,122740ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518,15342624udvpn"
      - "HOURLY_PRICES=18480ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8,770ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477,1871892ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783,18897ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518,10000000udvpn"

    expose:
      - port: 8585 # TCP listen port
        as: 8585
        to:
          - global: true
            ip: unique_name_endpoint  # Name used in line 3, for example "ip: dvpn_akash_node"
      - port: 3333 # V2RAY port
        as: 3333
        to:
          - global: true
            ip: unique_name_endpoint  # Name used in line 3, for example "ip: dvpn_akash_node"
      - port: 22 # SSH Port
        as: 22
        to:
          - global: true
profiles:
  compute:
    app:
      resources:
        cpu:
          units: 1
        memory:
          size: 1Gi
        storage:
          size: 3Gi         
  placement:
    akash: 
      pricing:
        app:
          denom: uakt
          amount: 100000
deployment:
  app:
    akash:
      profile: app
      count: 1
EOF
```




**generate certificate**
```sh
provider-services tx cert generate client --from $AKASH_KEY_NAME
provider-services tx cert publish client --from $AKASH_KEY_NAME
```


**create deployment**
```sh
provider-services tx deployment create deploy.yml --from $AKASH_KEY_NAME
```