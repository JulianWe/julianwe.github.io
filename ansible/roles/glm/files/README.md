# Share Compute Resources with golem

![](../images/golem.jpg)

**make sure to enable nested virtulization on gcp vm**
```sh
gcloud compute instances create ansible \
    --project=akash-456617 \
    --zone=us-central1-c \
    --machine-type=n1-standard-2 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=enable-osconfig=TRUE,ssh-keys=jw:ssh-ed25519\ \
AAAAC3NzaC1lZDI1NTE5AAAAIKTNqCzRZVoWV5hbr4yj\+mnV0ckEBfr68LC3BqZd3JsD\ jw \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=513538345283-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=instance-20250503-150608,disk-resource-policy=projects/akash-456617/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/debian-cloud/global/images/debian-12-bookworm-v20250415,mode=rw,size=100,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ops-agent-policy=v2-x86-template-1-4-0,goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
    --enable-nested-virtualization 

NAME     ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP     STATUS
ansible  us-central1-c  n1-standard-2               10.128.0.24  34.173.226.140  RUNNING
```

**in order to delete vm type the following command**
```sh
gcloud compute instances delete ansible --zone=us-central1-c
```

**to access vm us ssh**
```sh
ssh-keyscan -t ed25519 34.173.226.140 >> ~/.ssh/known_hosts
ssh -i ~/.ssh/jw_ed25519 jw@34.173.226.140
```

**update virtual machine packages**
```sh
sudo apt update && sudo apt upgrade -y 
```

**rent out your idle cpu memory and storage using golem**
```sh
curl -sSf https://join.golem.network/as-provider | bash -

By installing & running this software you declare that you have read, understood and hereby accept the disclaimer and
privacy warning found at https://handbook.golem.network/see-also/terms

Do you accept the terms and conditions? [yes/no]: yes
golem-installer: installing to /home/jw/.local/bin
 Component                             Version
-----------               --------------------
golem core                              0.17.3 [done]
wasi runtime                             0.2.2 [done]
vm runtime                               0.5.2 [done]

                                             ```
                                             ```
                                             ```
                  ```                        ```
       `````````````        `````````        ```        `````````         ``````````````````
     ````      ```        ```       ```      ```      ```       ```       ```     ``     ```
     ``          ``      ```         ```     ```      ``         ```      ``      ``     ```
    ```          ``      ``           ``     ```     ```````````````      ``      ``     ```
     ``          ``      ```         ```     ```      ``                  ``      ``     ```
     ```       ```        ```       ```      ```      ```        `        ``      ``     ```
       `````````            `````````        ```        ``````````        ``      ``     ```
          ```
          ```               version: 0.17.3
       `````````
     ```       ```          commit: f8354c785
     ``          ``
    ```          ``         date: 2025-04-04
     ``          ``
     ````      ```          build: 883
       `````````

Initial node setup
Do you agree to augment stats.golem.network with data collected from your node (you can check the full range of information transferred in Terms)[allow/deny]? [allow/deny] (default=allow): allow
Node name  (default=lonely-fight): golem
Ethereum mainnet wallet address (default=Internal Golem wallet): 0xbF0a899891ed4084429847219689A81CbC033B79
Price GLM per hour (default=0.025): 
vm                   vm runtime                                        
wasmtime             wasmtime wasi runtime                             
Downloading certificates and whitelists                           [done]

[ATTENTION REQUIRED]
To ensure your system can find the Golem binaries, please include '/home/jw/.local/bin' within your path, by following the instructions below.
1. Add the path to your configuration file:
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
2. Apply the changes in your current terminal:
   export PATH="$HOME/.local/bin:$PATH"


echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```


**verify installation status**
```sh
golemsp status
┌───────────────────────────────┐
│  Status                       │
│                               │
│  Service    is not running    │
│  Version    0.17.3            │
│  Commit     f8354c785         │
│  Date       2025-04-04        │
│  Build      883               │
│                               │
│  Node Name  golem             │
│  Subnet     public            │
│  VM         no access         │
└───────────────────────────────┘

VM problem: kvm kernel module is not installed

```

**configure user access to kvm to resolv the issue**
```sh
sudo usermod -aG kvm $(whoami) && sudo reboot
```

**verify vm hat access to kvm**
```sh
golemsp status
┌───────────────────────────────┐
│  Status                       │
│                               │
│  Service    is not running    │
│  Version    0.17.3            │
│  Commit     f8354c785         │
│  Date       2025-04-04        │
│  Build      883               │
│                               │
│  Node Name  golem             │
│  Subnet     public            │
│  VM        **valid**          │
└───────────────────────────────┘
```

**use screen to detach cli output on remote machine**
```sh
# To detach and leave golemsp run running in the background: Press Ctrl-A followed by D.
screen -S provider
golemsp run
```

**recover provider screen**
```sh
screen -r provider
```

**verify settings and check documatation for further information**
```sh
golemsp settings show

node name: "golem"
Shared resources:
        cores:  1
        memory: 2.612634375691414 GiB
        disk:   1.50250244140625 GiB


Pricing for preset "wasmtime":

        0.025000000000000001 GLM per cpu hour
        0.005000000000000000 GLM per hour
        0.000000000000000000 GLM for start
```
