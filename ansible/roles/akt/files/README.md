# **Setup Akash Cloud Provider on GCP 🐇**

![](../images/akash1.jpg)


[**Source: Documentation**](https://akash.network/docs/providers/build-a-cloud-provider/akash-cli/kubernetes-cluster-for-akash-providers/kubernetes-cluster-for-akash-providers/)


```sh
# install gcloud cli
brew update
brew upgrade
brew cleanup

brew install google-cloud-sdk
export PATH="$PATH:/google-cloud-sdk/bin"

# login to Google Cloud
gcloud auth login
```

```sh
# generate ssh key to access gcp ubuntu vm with ed25519 or rsa**
ssh-keygen -t ed25519  -f ~/.ssh/jw_ed25519 -C jw ; cat ~/.ssh/jw_ed25519.pub
ssh-keygen -t rsa -f ~/.ssh/jw_rsa -C jw ; cat ~/.ssh/id_rsa.pub
```

```text
# deployment sizing ubuntu 22.04 x86/64, amd64 noble image built on 2025-04-09 from Google Cloud
Ansible Node Requirements (t2d-standard-1 (1 vCPU, 4 GB Arbeitsspeicher))
Kubernetes Control Plane Node Requirements (t2d-standard-2 (2 vCPU, 8 GB Arbeitsspeicher))

Minimum Specs

2 CPU
4 GB RAM
30 GB disk

Recommended Specs

4 CPU
8 GB RAM
40 GB disk
```


```sh
# create gcloud vm command using ui and add ssh public key to access vm
 cat ~/.ssh/jw_ed25519.pub
```
![](../images/gcp_vm.jpg)


```sh
# create gcp ubuntu vm ansible host
gcloud compute instances create ansible \
    --project=akash-456617 \
    --zone=us-central1-a \
    --machine-type=t2d-standard-1 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=ssh-keys=jw:ssh-ed25519\ \
AAAAC3NzaC1lZDI1NTE5AAAAIKTNqCzRZVoWV5hbr4yj\+mnV0ckEBfr68LC3BqZd3JsD\ jw \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=513538345283-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=ansible-1,disk-resource-policy=projects/akash-456617/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/ubuntu-os-cloud/global/images/ubuntu-2404-noble-amd64-v20250409,mode=rw,size=10,type=pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
    --enable-nested-virtualization

NAME     ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP     STATUS
ansible  us-central1-c  t2d-standard-1              10.128.0.15  35.192.168.243  RUNNING
```


```sh
# copy public ed25519 or rsa SSH key from gcp vm in known hosts file and connect to vm. 
# Note ed25519 is more secure than rsa!

ssh-keyscan -t ed25519 34.173.226.140 >> ~/.ssh/known_hosts
ssh-keyscan -t rsa 34.173.226.140 >> ~/.ssh/known_hosts

ssh -i ~/.ssh/jw_ed25519 jw@34.173.226.140
ssh -i ~/.ssh/jw_rsa jw@34.173.226.140
```

```sh
# installing Kubernetes
apt-get update && apt-get upgrade -y
apt-get install docker.io gpg -y
apt-get install kubelet kubeadm kubectl -y  
apt-get install python3-pip virtualenv -y  
apt-get install apt-transport-https ca-certificates curl -y
kubeadm init 
```

```sh
# Configure access to k8s
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=/etc/kubernetes/admin.conf
```

```sh
# SSH into Kubernetes Master Node verify kubernetes installation
kubectl get nodes
kubectl get pods -A -o wide 
```

```sh
# Run provider script to build playbooks
git clone https://github.com/akash-network/provider-playbooks.git
cd provider-playbooks
./scripts/setup_provider.sh
```

```sh
# Clone Kubespray for Kubernetes Setup https://github.com/kubespray Download Updates and and install Kubespray 
cd ~ && sudo -s
apt-get update && apt-get upgrade
apt-get install docker.io -y
apt-get install python3-pip virtualenv -y
git clone -b v2.24.1 --depth=1 https://github.com/kubernetes-sigs/kubespray.git
```

```sh
# Setup Python 3 environment and install requirements
cd ~/kubespray
virtualenv --python=python3 venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

```sh
# Build Ansible Inventory for Kubernetes Hosts
cd ~/kubespray

cp -rfp inventory/sample inventory/akash

#REPLACE IP ADDRESSES BELOW WITH YOUR KUBERNETES CLUSTER IP ADDRESSES
declare -a IPS=(10.0.10.11 10.0.10.12 10.0.10.13 10.0.10.14)

CONFIG_FILE=inventory/akash/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

```sh
# Update DNS Server Config group_vars
vi inventory/akash/group_vars/all/all.yml
```
```yml
## Uncomment upstream dns servers
upstream_dns_servers:
  - 8.8.8.8
  - 1.1.1.1
```

```sh
# Generate ed25519 ssh key to access container on ubuntu passwordless vm with ed25519
ssh-keygen -t rsa -C $(hostname) -f "$HOME/.ssh/id_rsa" -P "" ; cat ~/.ssh/id_rsa.pub
```

```sh
# Run kubespray docker container
docker run --rm -it --mount type=bind,source="$(pwd)"/inventory/akash,dst=/kubespray/inventory \
  --mount type=bind,source="${HOME}"/.ssh/id_rsa.pub,dst=/root/.ssh/id_rsa \
  quay.io/kubespray/kubespray:v2.27.0 bash
```


```sh
# Inside the container you may now run the kubespray playbooks to create kubernetes cluster
ansible-playbook -i inventory/akash/inventory.ini --private-key /root/.ssh/id_rsa -become cluster.yml
```


```sh
# Create and apply custom kernel parameters
# **_NOTE:_** Apply these settings to ALL Kubernetes worker nodes to guard against too many open files errors.
cat > /etc/sysctl.d/90-akash.conf << EOF
# Common: tackle "failed to create fsnotify watcher: too many open files"
fs.inotify.max_user_instances = 512
fs.inotify.max_user_watches = 1048576

# Custom: increase memory mapped files limit to allow Solana node
# https://docs.solana.com/running-validator/validator-start
vm.max_map_count = 1000000
EOF 

# Apply Configs
sysctl -p /etc/sysctl.d/90-akash.conf
```

**Copy Public Key to the Kubernetes Hosts**
```sh
ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.0.10.11
ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.0.10.12
ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.0.10.13
ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.0.10.14
```
