# [Sia Storage Node](https://docs.sia.tech/hosting/setting-up-hostd/linux/debian)

![](../images/siacoin.jpg)

**download sia foundation hostd**
```sh
sudo curl -fsSL https://linux.sia.tech/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/siafoundation.gpg
sudo chmod 644 /usr/share/keyrings/siafoundation.gpg
echo "deb [signed-by=/usr/share/keyrings/siafoundation.gpg] https://linux.sia.tech/debian $(. /etc/os-release && echo "$VERSION_CODENAME") main" | sudo tee /etc/apt/sources.list.d/siafoundation.list
sudo apt update
```

**install hostd cli**
```sh
sudo apt install hostd
hostd version
sudo systemctl enable --now hostd
```

**configure hostd and enter your wallet private key**
```sh
sudo hostd config
sudo hostd version
sudo systemctl enable --now hostd
sudo systemctl status hostd
```

**update hostd service**
```sh
sudo apt update
sudo apt upgrade hostd
```

**access hostd [webui](http://127.0.0.1:9980) using portforwarding**
```sh
ssh -L 9980:localhost:9980 jw@34.16.28.187 -i ~/.ssh/jw_ed25519
```

**creating volume & configure pricing**
![](../images/sia_volume.jpg)


