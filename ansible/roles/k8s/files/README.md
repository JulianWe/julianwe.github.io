# Setup Kubernetes cluster on ubuntu

![](../images/kubernetes.jpg)


```sh
# run kubernetes.yml playbook to install kubernetes on selected inventory hosts with the following steps 
ansible-playbook playbooks/kubernetes.yml -i inventory.yml --become
```

![](../videos/kubernetes.gif)

```sh
# create inventory.yml file with any virtual machine
[gcp]
34.16.28.102 ansible_ssh_private_key_file=~/.ssh/jw_ed25519

[kubernetes]
35.226.46.33 ansible_ssh_private_key_file=~/.ssh/jw_ed25519
```


**this playbook installes kubernetes on our [kubernetes] vm**
```sh
# Create Kubernetes Cluster using Ansible Playbooks & Roles
# Author: Julian Wendland
---
- hosts: kubernetes
  tasks:

    - name: Include variables from a file
      include_vars:
        file: "../roles/k8s/vars/main.yml"
      register: vars

    - name: Include the k8s role
      include_role:
        name: roles/k8s
```


**this playbook automates the folloowing steps until kubeadm join**
```sh
---
- name: install kubernetes packages
  shell: | 
    apt-get update && apt-get upgrade -y
    apt-get install apt-transport-https ca-certificates curl -y
    apt-get install docker.io gpg -y
    echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | tee /etc/apt/sources.list.d/kubernetes.list
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o kubernetes-apt-keyring.gpg 
    mv kubernetes-apt-keyring.gpg /etc/apt/keyrings
    apt-get update
    apt-get install kubelet kubeadm kubectl -y
  register: packages

- name: systemctl start & enable container services
  shell: | 
    systemctl enable docker
    systemctl start docker
    systemctl start containerd
    systemctl enable containerd
    systemctl start kubelet
    systemctl enable kubelet
  register: systemctl

- name: initialize k8s
  shell: | 
    kubeadm init --ignore-preflight-errors=all
  register: kubeadm_init

- name: display kubeadm init for kubeadm join command
  debug:
    msg: "{{ kubeadm_init.stdout_lines }}"

- name: kubectl get nodes for kubeadm join
  shell: | 
    kubectl get nodes
  register: nodes

- name: copy k8s config
  shell: | 
    mkdir -p $HOME/.kube
    cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    chown $(id -u):$(id -g) $HOME/.kube/config
    export KUBECONFIG=/etc/kubernetes/admin.conf
  register: config
...
```

**same procedure with manuel steps on ubuntu**
```sh
# installing Kubernetes
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo apt update
sudo apt-get install docker.io -y
sudo apt-get install kubelet kubeadm kubectl -y  
sudo apt-get install apt-transport-https ca-certificates curl -y
```

```sh
# use systemctl to start and enable container services
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl start containerd
sudo systemctl enable containerd
sudo systemctl start kubelet
sudo systemctl enable kubelet
```

```sh
# use kubeadm to initilize k8s and join node to cluster
sudo kubeadm init --ignore-preflight-errors=all
```

```sh
# configure access to k8s
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=/etc/kubernetes/admin.conf
```

```sh
# from the kubeadm init output copy join command and run on worker nodes
kubeadm join 10.128.0.52:6443 --token c625mw.unir2d5c5t8v838f --discovery-token-ca-cert-hash sha256:c7bd19bdc0d77acbe563df872c50d41a9ce51db0ea334f09392f1fb55f63f908 --ignore-preflight-errors=all
```

```sh
# ssh into kubernetes master node verify kubernetes installation
kubectl get nodes
kubectl get pods -A -o wide 
kubectl get pods --all-namespaces
```
