# ☁️ [IPFS](ipns://ipfs.tech/) deployment Tutorial 🐇


| Key | Value |
| --- | --- |
| `Source` | 🕳️ [Documentation](http://docs-ipfs-tech.ipns.localhost:48084/how-to/command-line-quick-start/) |
| `Tutorial Author` | ☕ `Julian Wendland` |
| `$FIL Address` | `0xfA66faf3Faa192277bAb21Ef547ebdB47617B1da` |


![IPFS](../ipfs/images/IPFS.jpg)

**Hash based addressing instead of location based addressing with the worlds first Inter Planetary File System IPFS**

# Install IPFS
```sh 
curl -O https://dist.ipfs.tech/kubo/v0.20.0/kubo_v0.20.0_darwin-amd64.tar.gz
tar -xvzf kubo_v0.20.0_darwin-amd64.tar.gz
cd kubo
sudo bash install.sh
```

# Initialize IPFS
```sh 
ipfs daemon

Initializing daemon...
Kubo version: 0.20.0
Repo version: 13
System version: amd64/darwin
Golang version: go1.19.8

Error: no IPFS repo found in /Users/jw/.ipfs.
please run: 'ipfs init'
```

```sh 
ipfs init

generating ED25519 keypair...done
peer identity: 12D3KooWBcpXDYJbBx1bR4f3AfD4EahzVpcMLuM9fKnPmX3het4X
initializing IPFS node at /Users/jw/.ipfs
```

# Add IPFS Files
```sh 
➜  ipfs add -r julianwe.github.io/ 


added QmPwPK4gEqFn53HYweZ5L1Eue8PCbnz1kK5QQjFqSQZQ1q julianwe.github.io/Dockerfile
added QmRTxBHneq8qSzTSR9FDrqsxHHZT2ehLpKEbe8XoxEkSmp julianwe.github.io/about.html
added QmQaz4FZZE5gwFNHE2wrcw66dH8ygSHwfA14UsQQx4maky julianwe.github.io/contact.html
added QmVh9m47euAkLFXDhvV9HxjtpaKvdfNrfffu52Chdr1wE5 julianwe.github.io/css/jekyll.css
added QmWthuh1ZdL83Dhn82ynKVY7jaqjxnAc3BphVxa8qFcJmV julianwe.github.io/css/md.css
added QmYwQ59KhQQ7CLAYN7Uu5RizqSnwTceU8uZGahRQmvtHiT julianwe.github.io/css/splendor.css
added QmWYhJ7uYVy7sBTxH7bqXkhCZVkcmjhqPSGSfbPuESEvAB julianwe.github.io/css/splendor.min.css
added QmNXzFfCE16mtyKYufWFE7hsjRDUxk7C3DgZiBTnr1ZLXK julianwe.github.io/css/style.css
added QmbEsgYhNpLBazUJQ2mXnG43EshngVc15TLuPFNYW9ESox julianwe.github.io/css/tables.css
added QmfDRgA9o7B3obfNw4zaYp411Xuzv81w7FvRArqohe5Ck7 julianwe.github.io/css/w3.css
added QmQonhUj3ZbrtSmYgNcBXmY8p8cdVE6dNoobS1eWdrT541 julianwe.github.io/images/background.jpg
added QmSR44XHr6JTy7Buf36TiU2jFsJBAWCDaB3CdTKpKCXxaG julianwe.github.io/images/defilego.jpg
added QmeMtQw97czTWb42ThscKQwkyg17cvrKz4SKCdDEiYRCP8 julianwe.github.io/images/git.jpg
added QmSABQNfBZGsou269RQT5Bx249SKWrQw3QrexmGcvPiDEt julianwe.github.io/images/me.jpg
added QmVxuBcKfHzGjqfejSFKvDekJbYDiZNhnFRFNSxJagwvz6 julianwe.github.io/index.html
added QmNgpZQdDDQALnv5c6szWdJzCrXxUbsriA7qzNq3DGFQzu julianwe.github.io/js/main.js
added QmZDA9aRK4wxegcs93sFm5zafP2C4Pt2HbWfoPQk14QZ53 julianwe.github.io/js/search.js
added QmWHrtPBhZu5aus9Ni8VvgJr5jErAKvpwigLsUVce6s4UN julianwe.github.io/lib/jquery/jquery.min.js
added QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH julianwe.github.io/lib/justified-gallery/css/justifiedGallery.min.css
added QmbDsvemWctRqRZC2gFL5ZimkCAzk66LQ84HvoccNe2R6m julianwe.github.io/lib/justified-gallery/js/jquery.justifiedGallery.min.js
added QmSKadFNaAbZMb7WLt4tuSffHj9xHtMcZKACBQyaKBUKAq julianwe.github.io/mail.php
added Qmd6vdmBAgiXSaD4SiVRAVaCVwJogt1ScCWEBXRDDGm8xZ julianwe.github.io/projects/ERC-20/ERC-20.html
added QmXMEWxaiFwDm9xqFsxCD9Qv4cjri75pTGjudbrjCvWutx julianwe.github.io/projects/ERC-20/MyCustomToken.sol
added QmUXavWSqcHxyx6HbTPk5dp8SpTyJfcsVECSpXHAE8khTu julianwe.github.io/projects/ERC-20/README.md
added QmP6GeyKevoQAm7vaUWRaYixedoywgAii3Ai3urVykegHa julianwe.github.io/projects/ERC-20/images/ERC-20-Token.jpg
added QmTLM2AzeL4FKPWkSJzJbgUeR1uxwzHGksuH4Ziz19JEjy julianwe.github.io/projects/MultiSigEthereumWallet/MultiSigEthereumWallet.html
added QmbR4ugaZsWwSXz8iBLxBfy84J6RGeGmCFCyFUXG1uhDtE julianwe.github.io/projects/MultiSigEthereumWallet/MultiSigWallet.sol
added QmefRj3K6oCdLMFdkZ3dCLUZsAMzXSjcS6y9xC4JtMHxMp julianwe.github.io/projects/MultiSigEthereumWallet/README.md
added QmWWLhy2K4qPJbW4fzrmyuK19r2icZ6Bvoczxw7zbeZDQw julianwe.github.io/projects/MultiSigEthereumWallet/images/ApproveSpendingWalletFunds.jpg
added QmSu1G9u2W7bFxvAcaup7NhWC3qCADiYKgMbTegePqqoQu julianwe.github.io/projects/MultiSigEthereumWallet/images/DeployMultiSigWallet.png
added QmRedAo81zKZMmgXgshtpWZJoJm54pdsbFJ1DFZo3WoPeR julianwe.github.io/projects/MultiSigEthereumWallet/images/multisigwallet.jpg
added QmctDUPwBKT7t5rDqfLzTLQ6LehVb36exyZhszrqQ8UY6a julianwe.github.io/projects/SmartContractTutorial/README.md
added QmW6kmHsq5G5iti6eRs3CWZo9ojSDKY1t6LBWVb7sjoWCh julianwe.github.io/projects/SmartContractTutorial/SmartContractTutorial.html
added QmSPtspbh8JiyW4TrwaPeVAkoC39oeKcxihaQWo1xr4U5s julianwe.github.io/projects/SmartContractTutorial/VotingContract.sol
added QmbW7Eg8CWaqWq2vQjv6mhunA8FWefegZnLpihstLLFWRq julianwe.github.io/projects/SmartContractTutorial/images/DeployVotingContract.jpg
added QmbVy3mSQJQE2YNxJBpMENKBXQiCXmu6DtLc992gB9siwz julianwe.github.io/projects/SmartContractTutorial/images/InteractWithSmartContract.jpg
added Qmb473LKqKErdJ49x7Evf3huXmBYetFN5eTuhiYkDjVggf julianwe.github.io/projects/SmartContractTutorial/images/SolidityContract.jpg
added QmQjsowf2XF2uBuEoZr66U7vC15czHtGEf6LuNN1RXeHkF julianwe.github.io/projects/akash/README.md
added QmRHf4g3euE72Mfr9N57iRrsMAtZciR8YMe9xuwjwoQsVW julianwe.github.io/projects/akash/akash.html
added QmNamuDmH3dFbDMcphoMPb1WR7tvofH3FKa9aw3vDSyZnX julianwe.github.io/projects/akash/deploy.yml
added QmXaVEGboArhWypcruHhDwAetitcpuESifhWBh4PZzDppx julianwe.github.io/projects/akash/deploy_web.yml
added QmTnxW6kHavhS4srHEnEUegVeaNhq5Zzu6NguhTPeVuiZY julianwe.github.io/projects/akash/deploy_webapp.yml
added Qmc33G9ucbKxQvKyuvxC8zgv7usquwjsqiQBcGFSwUy72n julianwe.github.io/projects/akash/deployment.yml
added QmZjxmPSrHw2zFN8HmDTY99SBT1C9meMchuj1bb43Tsway julianwe.github.io/projects/akash/genesis.json
added QmXGggCXxDXoZNGmDdxu8ygpZTETuWjgdJdtTmXtQzowSg julianwe.github.io/projects/akash/images/akash.jpg
added Qmd4jsec9pHDDiDWnjQvLp8b7diBuPan6bvV3DFrLuUhYW julianwe.github.io/projects/ansible/README.md
added QmTu6JjhGRXGu7aynAxpJ1UD3zZuWYBRAd1sJDZ4Mx8AMs julianwe.github.io/projects/ansible/ansible.html
added QmeSnLu4X2FJ3ufFbZqSXgca47soJXyTbt8RS1SfjjE5eK julianwe.github.io/projects/ansible/images/ansible.jpg
added QmYVEugvYubAkpxLHzixa9VFB61dUwhsfdigmk7e5byje9 julianwe.github.io/projects/ansible/playbook.yml
added QmdsXNwLmrcNZ21zVFk3hVgyQqdABChRfoBJhnFmqT16UV julianwe.github.io/projects/ansible/projects.j2
added QmNZu6BxBdywuhAyGngpvN1aDSHYafZgzdESaNwssJHbSx julianwe.github.io/projects/ansible/projects_template.j2
added QmXAso78vzpRfPrkpjyC3PymApERFe487ksTYQQXjGjrzM julianwe.github.io/projects/brave/README.md
added QmVhbqPNvGuX8A5LPBg9qm8K3TrK2ecizVa7qAvif8pSSQ julianwe.github.io/projects/brave/brave-rewards-verification.txt
added QmeSvKFeV9TUAC9RsLCVUNL61ifVXgdq2sPssi7uozi6Vw julianwe.github.io/projects/brave/brave.html
added QmZRuNNxxAD5JeDz9RF69DsrcLDhcUrV2wgcixDt3wWNz4 julianwe.github.io/projects/brave/images/brave1.jpg
added QmbGDXyU5DqFFkubJzXhgPV8F36aJeVajDi19D2iLAZgi6 julianwe.github.io/projects/brave/images/brave2.jpg
added QmWRQGzzE3BGtbHsfkVd2zSoz6HxfiCnVUiTb7B2o4ZXWM julianwe.github.io/projects/handshake/README.md
added QmQaUCn4Fnscva4XDhSUmb48jjFy4Cz47URVUsY8NsxAtv julianwe.github.io/projects/handshake/handshake.html
added QmRjLMBhrT7tu47wB85zjpjBHDgKS7xmPcx97m66czsCxQ julianwe.github.io/projects/handshake/images/handshake.jpg
added QmWG2hfd9VTLHqWQo5KZisxThs58bCQZxez9Exjz3TGhpK julianwe.github.io/projects/ipfs/README.md
added QmRV4uXwchpr1FfGAUXVvovk263DxTPv4Rqc6S8wcCFyun julianwe.github.io/projects/ipfs/images/IPFS.jpg
added QmULN8ECS7NbomG5S8t1UHcsXkeJm6H4MbzqMHiZKTjeFC julianwe.github.io/projects/ipfs/images/ens1.jpg
added QmbMVtAcrmeE4Bm4ipZ68QCv4E4stLPiadQitbbPQfpKwH julianwe.github.io/projects/ipfs/images/ens2.jpg
added QmX2ZdEk424eynA2P3WJvuXHwMPub3Abr9hHka4cRaCRRv julianwe.github.io/projects/ipfs/ipfs.html
added QmTNpZqmtr3t7AfNZuhAZWgXCfYhzWMSX1WCWRfypef5sH julianwe.github.io/projects/ipfs/kubo/install.sh
added QmYgwxvxyDMKz7HkM8K5TyMQCWfGq2GNGdMwnKkKt8Cwfo julianwe.github.io/projects/ipfs/kubo_v0.20.0_darwin-amd64.tar.gz
added QmZ73R2RdjHwjgzqtQ66HxKHCxmp5bAxYgD88ZjdvgdGFZ julianwe.github.io/projects/projects/README.md
added QmSR1ngGkDaYTmBN4x7SHibSbiZtaBYMzBPMDYSim15a68 julianwe.github.io/projects/projects/projects.html
added QmVp4CAT9WwZGmAJXkvmxYvGK8S3FPtt3MWxcF13D4LAFL julianwe.github.io/projects/sentinel/README.md
added QmXL5DvW9PsgZQCq8BYzvSUM8REjRGUg3BEPJmFKDXQpUp julianwe.github.io/projects/sentinel/images/create-sentinel-node1.jpg
added QmaG1hLLGEwoufFVjx5mEw18FZoR1Hh2ytNLbyq86TDcNP julianwe.github.io/projects/sentinel/images/create-sentinel-node2.jpg
added QmbQppYJzdh8gAS2gacCQnVr3M9jkj5m1SojtoMGGtkPHx julianwe.github.io/projects/sentinel/images/create-sentinel-node3.jpg
added QmPJtNNnnPY6sBywaxEeQ6mxdbDdtgRxemQGS9NXYZTAhu julianwe.github.io/projects/sentinel/images/create-sentinel-node4.jpg
added QmanCiTyTCajxwjSFrbxrpsq3j2Sie7i33TNSnkTWYM8Fo julianwe.github.io/projects/sentinel/images/sentinel.jpg
added QmQKhGqCWghgkgegY24tJw4urRsNiQGyYHqNZF26cvfaTE julianwe.github.io/projects/sentinel/script
added QmW6TgMHEUqLBGavobiqSSxweTA8rfC3adkz2QST7HFtRb julianwe.github.io/projects/sentinel/sentinel-script.sh
added QmSgv51v27QxiGHJCPokGwh6P44TREb6gfVYu5Eyyr1nVj julianwe.github.io/projects/sentinel/sentinel.html
added QmdXnt3ZvTSC8u6hcxqPnVyrHedRXB86fzsP5YJw7SG4Hz julianwe.github.io/projects/vsc/Dockerfile
added QmNi7YVbyoxPjv8ygPCue8noBqPrCyDBA2CmvwoQogPcFC julianwe.github.io/projects/vsc/README.md
added QmP11jdi9cahj47W9H9MKFGeU8KiFjgHA18fPh4VBRAnjp julianwe.github.io/projects/vsc/images/vsc.jpg
added QmVS3hN7RtREHwGoQhTdCYzNDXdWJVGnYogMeaWEbyGXPt julianwe.github.io/projects/vsc/vsc.html
added QmZcyrN2XMzJcSAvdyfoVRSkwNsWkgng6avyrd9WSZApKx julianwe.github.io/projects/website/README.md
added QmTC6PPRDf7LHtSZrJAF2uLfXP4y7fAia78pPGmeuyo9h9 julianwe.github.io/projects/website/images/ansible-docker.jpg
added QmPu7Lr3qZkURtAaNsLoVFgRjP39pUAD7L1enanafvy2qh julianwe.github.io/projects/website/images/github_actions.jpg
added Qmdo2Xw8ccwxUD1NVvwwfeB91DgVXT6BEqj3rruJNspppa julianwe.github.io/projects/website/images/pages.jpg
added QmYxMjT9VkrJtAVJjuivuVGkN4jLLnrwYEHP2B6Y3Lt9xS julianwe.github.io/projects/website/website.html
added QmejfFQCgYNdDqyVwWiuf7Zao2iqFyLhcYMkTg1QCMvqnj julianwe.github.io/projects.html
added QmSogJbLGsmVpEnyBfGooaV6PbErYTK6kqgxVLnV3wRr3P julianwe.github.io/recommondations.html
added QmXcMVSxwi55dud2XyDfBsYkpwzrVRGSNW6pkVqkAjjXMW julianwe.github.io/search.html
added QmNifJHpFsNuZe9FK2ZoRH6wx6sWdqNjA5MMeSjvve55pj julianwe.github.io/css
added QmZE1Yb85CzWhVtSMX8N6zXfboNdXYJV8CMdzcpdYDpv5M julianwe.github.io/images
added QmVmVnyAfbd6Pt1HoEVA3HUovxEfApVgrMhZx6E2AYBqXb julianwe.github.io/js
added QmXJA6FHQXt4MfqB2xuer1cNBnjeKX8kWJcxArdywc4d7e julianwe.github.io/lib/jquery
added QmYyn5Gd82AWzPFFowS42UXVZcLFHtLorvhsNwJUkS3yRF julianwe.github.io/lib/justified-gallery/css
added QmexP16d3a4m5VgKVW5QMB1FX2XbYYCKoSmXzPVAxTPVFv julianwe.github.io/lib/justified-gallery/js
added QmbmYDjrCN1GmQ11U4tWcmMADm3YarpTQs1fKct6r4TEW4 julianwe.github.io/lib/justified-gallery
added QmPQXkj57Runa5SWAd8u6G64AWEnZKmx1vxghR6DpssKXf julianwe.github.io/lib
added QmdWjVXeJTiyvghsUYWG5ZD7yobeAjS3RcS3boRrvfXhpJ julianwe.github.io/projects/ERC-20/images
added Qmemvq1cgdfF2xkxi3iE1zdsPKE8FictZTTcdv7D4F5jba julianwe.github.io/projects/ERC-20
added QmWdg2UcUK3fFhUhdwYLnWaBMueNFrCz65YZq3bxphYwxg julianwe.github.io/projects/MultiSigEthereumWallet/images
added QmZpt3cE16GKHKxTiWXaV42pxcfuAEm1PVzTBYczNZjSyg julianwe.github.io/projects/MultiSigEthereumWallet
added QmexBWX2PXw5cZr64eczSJTacJs5RxUc7ZWxn5MbtVpric julianwe.github.io/projects/SmartContractTutorial/images
added QmdArytDRCsMFWrobNAPbcVM1ztgKw3HVMArqQf2Y2pBNZ julianwe.github.io/projects/SmartContractTutorial
added Qme8LC1ERVbYZHSkxPs2qSMbPqcCnQN1SSKvNQLvU7vFG5 julianwe.github.io/projects/akash/images
added QmTxFi9YJgZio9hVxMAmF7pTBEAJFuW9xoAtUr5Ng5TfZ2 julianwe.github.io/projects/akash
added QmXcp7hNi8EVTSzGSJp1p5sUEusLsKfw7dcZ8vV4yr437o julianwe.github.io/projects/ansible/images
added QmR18iraXDeZ8hP6esw4PFVaeNvQbv92W6kGTP9gV6ZNDE julianwe.github.io/projects/ansible
added QmbhsmcXanQw63q1dJf4vKgZpRa91wz2i8etv8QqA2sp7H julianwe.github.io/projects/brave/images
added Qmcxx1HdGPuahHn8Vbh7U928uQ17XAzcWrDEgzfPRJA11q julianwe.github.io/projects/brave
added QmYk1BzmrQBWNMZmdjVaNmYDQgTg7rLwiy8qbNmYaRjoR6 julianwe.github.io/projects/handshake/images
added QmXf9npuvjkrmw5dvFaNHy1mesAqQ5ZUwbn2viE4cknatx julianwe.github.io/projects/handshake
added QmPzn4JCa7yoQ7wxM7EtgRTC4DkEXztrJu9L6W31JjveRN julianwe.github.io/projects/ipfs/images
added QmZQ7JAy71KtXGKwZNA85eVDTnqhoUTCjHJuQ5ng53PMwR julianwe.github.io/projects/ipfs/kubo
added QmWTuAqMZjV1BdYxoKAgUgU3Z88D9ZJHftQwoeL4j5nxwk julianwe.github.io/projects/ipfs
added QmTPuSfAmT6F1V1QFojLfLuxXmNqgG4wYojjjEk64pHEQJ julianwe.github.io/projects/projects
added QmPESWganmxY2D9C2jEbCSrigs2JVhepZBDTE4DvPxwQBC julianwe.github.io/projects/sentinel/images
added QmU9UKpYFoFRMJFbcadZUCgbQNH6isHMAhyyQ9L6Abgdo5 julianwe.github.io/projects/sentinel
added QmSm9jKM2S2E3xoQmJKMcdzNnDMHJr8LNXbRgPZHVo52EP julianwe.github.io/projects/vsc/images
added QmVg5ru8dtPiVGcgZbPMCQThEnUz7mGx3BsoiyupyyK94c julianwe.github.io/projects/vsc
added QmQuyQ7tSde7UA1tiQTpTVZAGxCYooMidGtJ5HyYVz3cvL julianwe.github.io/projects/website/images
added QmTpU3Hc8VBN2FpQc2NpU1EPuLFL76ktkF966zTD5Cq3Ek julianwe.github.io/projects/website
added QmYR9Nt64JrTxAMgQppiyQ91XGa4nS8ybUTzCZiz8ALGVp julianwe.github.io/projects
added QmT8WZM21D1cAJBFtuVUD7MWX8vSYarHStHavvCt847RK4 julianwe.github.io
 57.59 MiB / 57.59 MiB [============================================================================================================] 100.00%
```

**IPFS Links to your Website**
**[ipfs://QmTtVgHuVWQEETLcPr1SVQNSvcTtosBKr1R8ehQgvps8Yd](ipfs://QmTtVgHuVWQEETLcPr1SVQNSvcTtosBKr1R8ehQgvps8Yd)**
**[ipfs://ipfs://bafybeicsolhq5q2hfaz6kdyhwvws5vnrrmlfyxasawd7eokrvwktzclkiy/projects/ipfs/ipfs.html](ipfs://bafybeigs3i74yqmnrsshyjffmmrnxp5d6p3brobimprbsvzps6ghs3ecsm/projects/ipfs/ipfs.html)**
**[https://gateway.ipfs.io/ipfs/QmTtVgHuVWQEETLcPr1SVQNSvcTtosBKr1R8ehQgvps8Yd](https://gateway.ipfs.io/ipfs/QmTtVgHuVWQEETLcPr1SVQNSvcTtosBKr1R8ehQgvps8Yd)**


**Go to https://app.ens.domains/ and Link your content Hash to ENS Domain**

| Set Content Hash | Update Records |
|---------|---------|
![](../ipfs/images/ens1.jpg) | ![](../ipfs/images/ens2.jpg) |
**[https://julianwendland.eth](https://julianwendland.eth)**


**Link DNS to your website**
[Docs](http://docs-ipfs-tech.ipns.localhost:48084/how-to/websites-on-ipfs/link-a-domain/)
[dnslink.io](https://dnslink.io/#step-1-choose-a-domain-name-to-link-from)

**Links**
[Source](https://makoto-inoue.medium.com/how-to-host-your-dapp-with-ipfs-ens-and-access-it-via-ethdns-c96046059d87)
[IPFS Desktop](https://github.com/ipfs/ipfs-desktop)
[IPFS Addon](https://chrome.google.com/webstore/detail/ipfs-companion/nibjojkomfdiaoajekhjakgkdhaomnch?hl=en)
[IPFS Docs](http://docs-ipfs-tech.ipns.localhost:48084/how-to/command-line-quick-start/)
