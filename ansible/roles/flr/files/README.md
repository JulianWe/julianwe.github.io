# [Run Flare Node using Docker](https://dev.flare.network/run-node/using-docker)

![](../images/flare.jpg)

**install disk util**
```sh
sudo apt install fdisk
sudo apt install xxd
```

**install docker compose**
```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**add your user to docker group**
```sh
mkdir flare
cd flare
sudo usermod -a -G docker $USER
```

**backup device**
```sh
sudo -s
cp /etc/fstab /etc/fstab.backup
fstab_entry="UUID=$(sudo blkid -o value -s UUID /dev/sdb) /mnt/db ext4 discard,defaults 0 2"
echo "$fstab_entry" | sudo tee -a /etc/fstab
```

**list disk partition and create db mount**
```sh
# add disk on gcp vm and name it sbd
lsblk
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0  100G  0 disk 
├─sda1    8:1    0 99.9G  0 part /
├─sda14   8:14   0    3M  0 part 
└─sda15   8:15   0  124M  0 part /boot/efi
sdb       8:16   0  100G  0 disk 


sudo mkdir /mnt/db
sudo chown -R jw:root /mnt/db
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
sudo mount /dev/sdb /mnt/db
```

**create config.json folder & file for your flare node**
```sh
sudo mkdir -p /opt/flare/conf
sudo mkdir /opt/flare/logs
sudo chown -R jw:root /opt/flare

cat > /opt/flare/conf/config.json <<EOF 
{
  "snowman-api-enabled": false,
  "coreth-admin-api-enabled": false,
  "eth-apis": [
    "eth",
    "eth-filter",
    "net",
    "web3",
    "internal-eth",
    "internal-blockchain",
    "internal-transaction"
  ],
  "rpc-gas-cap": 50000000,
  "rpc-tx-fee-cap": 100,
  "pruning-enabled": true,
  "local-txs-enabled": false,
  "api-max-duration": 0,
  "api-max-blocks-per-request": 0,
  "allow-unfinalized-queries": false,
  "allow-unprotected-txs": false,
  "remote-tx-gossip-only-enabled": false,
  "log-level": "info"
}
EOF
```

**run flare observer docker container**
```sh
docker run -d --name flare \
  -e NETWORK_ID="flare" \
  -e AUTOCONFIGURE_BOOTSTRAP="1" \
  -e AUTOCONFIGURE_PUBLIC_IP="1" \
  -e AUTOCONFIGURE_BOOTSTRAP_ENDPOINT="https://flare-bootstrap.flare.network/ext/info" \
  -v /mnt/db:/app/db -v /opt/flare/conf:/app/conf/C \
  -v /opt/flare/logs:/app/logs \
  -p 0.0.0.0:9650:9650 \
  -p 0.0.0.0:9651:9651 \
  flarefoundation/go-flare:v1.10.0
```

**create docker_compose.yaml file**
```sh
sudo cat > /opt/observer/docker-compose.yaml <<EOF 
services:
  observer:
    container_name: flare-observer
    image: flarefoundation/go-flare:v1.10.0
    restart: on-failure
    environment:
      - NETWORK_ID=flare
      - AUTOCONFIGURE_BOOTSTRAP=1
      - AUTOCONFIGURE_PUBLIC_IP=1
      - AUTOCONFIGURE_BOOTSTRAP_ENDPOINT=https://flare-bootstrap.flare.network/ext/info
    volumes:
      - /mnt/db:/app/db
      - /opt/flare/conf:/app/conf/C
      - /opt/flare/logs:/app/logs
    ports:
      - 0.0.0.0:9650:9650
      - 0.0.0.0:9651:9651
EOF
```

**create directory & confirm flare observer health**
```sh
sudo mkdir /opt/observer
sudo chown -R jw:root /opt/observer

curl http://localhost:9650/ext/health | jq
curl -s http://127.0.0.1:9650/ext/health | jq -r ".checks.network.message.connectedPeers"
```


# Register as Validator

**confirm your node is running**
```sh
curl -X POST --data '{
    "jsonrpc":"2.0",
    "id"     :1,
    "method" :"info.getNodeID"
}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/info
```

**inspect validator status**
```sh
# Replace nodeIDs with your node ID from the output above
curl --data '{
    "jsonrpc": "2.0",
    "method": "platform.getCurrentValidators",
    "params": {
      "nodeIDs": ["NodeID-NcHj9PHyvtVJaiJfD2xvC4cuqkttTBZof"]
    },
    "id": 1
}' -H 'content-type:application/json;' https://flare-api.flare.network/ext/P | jq
```

**create public & private key**
```sh
docker run --rm ghcr.io/flare-foundation/fast-updates/go-client:latest keygen

{
"PublicKeyX":"0x134b190aebdc183dc6f7870219d697503c8f64a9528cca6bb996e2ea9916cead",
"PublicKeyY":"0x105a58d95d38c3c0b745d1040a583c68af91585aea4bb56eb31dba68dff33537",
"PrivateKey":"0x00750a76dd8f6e944232078625231a25447f6f0cbf4c864260de5bee08afd835"
}

# Replace key and address with your values from the output above to generate signature the address is in this case the public key
docker run --rm ghcr.io/flare-foundation/fast-updates/go-client:latest keygen --key "0x00750a76dd8f6e944232078625231a25447f6f0cbf4c864260de5bee08afd835" --address "0x134b190aebdc183dc6f7870219d697503c8f64a9528cca6bb996e2ea9916cead"
```

**register public key**
```sh
registerPublicKey(
  bytes32 0x134b190aebdc183dc6f7870219d697503c8f64a9528cca6bb996e2ea9916cead, // <-- REPLACE WITH YOUR GENERATED PublicKeyX
  bytes32 0x105a58d95d38c3c0b745d1040a583c68af91585aea4bb56eb31dba68dff33537, // <-- REPLACE WITH YOUR GENERATED PublicKeyY
  bytes 0x094f245f8a2d6c366d4646042478d6c32b04fdd044ebc1add082fa8d1910e0cc0b223cb7df3e6470bd1aa95d4968eecf96f0c794ec945e4b31dbb0f34605e75b28f9f6e15bb106c02d0eeaadc9cbdc8beb610b153d46a1347742b8ae948f255b  // <-- REPLACE WITH YOUR GENERATED Signature
)
```

**find staker.crt and staker.key under ~/.avalanchego/staking/**
```sh
PATH_TO_CRT=~/.avalanchego/staking/staker.crt
ZERO_PREFIX=0000000000000000000000000000000000000000000000000000000000000000
PATH_TO_KEY=~/.avalanchego/staking/staker.key
IDENTITY_ADDRESS=0x134b190aebdc183dc6f7870219d697503c8f64a9528cca6bb996e2ea9916cead 
```


**use the following commands to generate the required contract arguments _nodeId _certificateRaw & _signature**
```sh
cat $PATH_TO_CRT | tail -n +2 | head -n -1 | base64 -d | openssl dgst -sha256 -binary | openssl rmd160 -provider legacy -binary | xxd -p | sed -e 's/^/0x/;'

cat $PATH_TO_CRT | tail -n +2 | head -n -1 | base64 -d | xxd -p | tr -d '\n' | sed -e 's/^/0x/;' && echo

echo -n $ZERO_PREFIX$IDENTITY_ADDRESS | xxd -r -p | openssl dgst -sha256 -sign $PATH_TO_KEY | xxd -p | tr -d '\n' | sed -e 's/^/0x/;' && echo
```


**create config.json file to configure the node**
```sh
cat > config.json <<EOF 
{
  "snowman-api-enabled": false,
  "coreth-admin-api-enabled": false,
  "coreth-admin-api-dir": "",
  "eth-apis": ["web3"],
  "continuous-profiler-dir": "",
  "continuous-profiler-frequency": 900000000000,
  "continuous-profiler-max-files": 5,
  "rpc-gas-cap": 50000000,
  "rpc-tx-fee-cap": 100,
  "preimages-enabled": false,
  "pruning-enabled": true,
  "snapshot-async": true,
  "snapshot-verification-enabled": false,
  "metrics-enabled": true,
  "metrics-expensive-enabled": false,
  "local-txs-enabled": false,
  "api-max-duration": 30000000000,
  "ws-cpu-refill-rate": 0,
  "ws-cpu-max-stored": 0,
  "api-max-blocks-per-request": 30,
  "allow-unfinalized-queries": false,
  "allow-unprotected-txs": false,
  "keystore-directory": "",
  "keystore-external-signer": "",
  "keystore-insecure-unlock-allowed": false,
  "remote-tx-gossip-only-enabled": false,
  "tx-regossip-frequency": 60000000000,
  "tx-regossip-max-size": 15,
  "log-level": "info",
  "offline-pruning-enabled": false,
  "offline-pruning-bloom-filter-size": 512,
  "offline-pruning-data-directory": ""
}
EOF
```



# Using Flare Stake Tool

```sh
npm install @flarenetwork/flare-stake-tool -g
```

```sh
flare-stake-tool
```

```sh
PRIVATE_KEY_CB58=""
PRIVATE_KEY_HEX=""
```


**Launch the Staking Tool**
```sh
flare-stake-tool interactive
```

**retrieve your validators node ID by running**
```sh
curl --location 'http://localhost:9650/ext/info' --header 'Content-Type: application/json' --data '{ "jsonrpc":"2.0", "id":1, "method":"info.getNodeID" }'
```

```sh
flare-stake-tool info validators
```

flare-stake-tool interactive


