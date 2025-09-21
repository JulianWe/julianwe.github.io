# Nervos Network Node

![](../images/nervos.jpg)

**install requirements**
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
sudo apt install cargo -y
sudo apt install make -y
sudo apt install build-essential -y
sudo apt install libssl-dev -y
sudo apt install pkg-config -y

export RUSTFLAGS=--cfg=rustix_use_libc
export OPENSSL_DIR=/usr/bin/openssl
```

**download nervos network light client**
```sh
git clone https://github.com/nervosnetwork/ckb-light-client.git
cd ckb-light-client
cargo build --release
```

**copy cbk light client**
```sh
mkdir cbk
cp light-client-bin cbk/ckb-light-client -r
cp config/mainnet.toml cbk/
cd cbk
```

**run cbk light client**
```sh
RUST_LOG=info,ckb_light_client=info ./ckb-light-client run --config-file ./mainnet.toml
```


# Nervos Mining

**install rustup**
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**download cbk miner**
```sh
git clone https://github.com/nervosnetwork/ckb-miner.git
cd ckb-miner
cargo build --release
cargo install --path .
```

**create f2pool mining pool account & start cbk miner with your details**
```sh
/home/jw/.cargo/bin/ckb-miner  \
  -t 4 \
  -c stratum+tcp://ckb.f2pool.com:4300 \
  -u victorynox.victorynox.001
```
