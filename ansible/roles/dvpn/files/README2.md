**install sentinelcli**
```sh
curl https://raw.githubusercontent.com/hoon-node/Node-Setup/main/Speedrun.sh | bash
```

**prepare variables for your sentinel dvpn node**
```sh
# Create a new Wallet for your sentinel node
sentinelcli keys mnemonic 
"ozone comic casual endless punch happy burst photo industry dismiss clean corn castle border bachelor various mosquito damage own aspect sheriff focus answer machine"

# Copy your Private Key to Access Sentinel Node via ssh
cat ~/.ssh/jw_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKTNqCzRZVoWV5hbr4yj+mnV0ckEBfr68LC3BqZd3JsD jw

# Convert your Wallet mnemonic to base64
echo -n "ozone comic casual endless punch happy burst photo industry dismiss clean corn castle border bachelor various mosquito damage own aspect sheriff focus answer machine" | base64
b3pvbmUgY29taWMgY2FzdWFsIGVuZGxlc3MgcHVuY2ggaGFwcHkgYnVyc3QgcGhvdG8gaW5kdXN0cnkgZGlzbWlzcyBjbGVhbiBjb3JuIGNhc3RsZSBib3JkZXIgYmFjaGVsb3IgdmFyaW91cyBtb3NxdWl0byBkYW1hZ2Ugb3duIGFzcGVjdCBzaGVyaWZmIGZvY3VzIGFuc3dlciBtYWNoaW5l
```

Go to Akash Console https://console.akash.network/ click on SDL Builder and import the following YML Code and click on deploy select a provider and click on accept bid.
NOTE: This Step costs 6,5 $ / month the goal is to earn more with the income stream from renting out network bandwidth.

Next step ist to update the deployment with the IPv4 from the leases tab.

```sh
brew untap ovrclk/tap
brew tap akash-network/tap
brew install akash-provider-services
```


**deploy sentinel node on Akash with SSH enabled**
```sh
cat > /opt/flare/conf/config.json <<EOF 
---
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
```

**after deployment update deployment with your IPv4**



```sh
sudo docker run -d \
    --name sentinel-dvpn-node \
    --restart unless-stopped \
    --volume /root/.sentinelnode:/root/.sentinelnode \
    --volume /lib/modules:/lib/modules \
    --cap-drop ALL \
    --cap-add NET_ADMIN \
    --cap-add NET_BIND_SERVICE \
    --cap-add NET_RAW \
    --cap-add SYS_MODULE \
    --sysctl net.ipv4.ip_forward=1 \
    --sysctl net.ipv6.conf.all.disable_ipv6=0 \
    --sysctl net.ipv6.conf.all.forwarding=1 \
    --sysctl net.ipv6.conf.default.forwarding=1 \
    --publish :/tcp \
    --publish :/udp \
    sentinel-dvpn-node process start
```

```sh
sudo docker run -d \
    --name sentinel-dvpn-node \
    --restart unless-stopped \
    --volume /root/.sentinelnode:/root/.sentinelnode \
    --publish :/tcp \
    --publish :/tcp \
    sentinel-dvpn-node process start
```