# Setup Kubernetes cluster on ubuntu

![](../images/kubernetes.jpg)


```sh
# run kubernetes.yml playbook to install kubernetes on selected inventory hosts with the following steps 
ansible-playbook playbooks/kubernetes.yml -i inventory.yml --become
```

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

# from the output obove copy join command
kubeadm join 10.128.0.45:6443 --token 7jm2ro.hb118l2dgjl12nm1 --discovery-token-ca-cert-hash sha256:a57d8bd13c643717f7ae86560143c62be8fd96acd7ea4 --ignore-preflight-errors=all
```

```sh
# Configure access to k8s
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=/etc/kubernetes/admin.conf
```

```sh
# ssh into kubernetes master node verify kubernetes installation
kubectl get nodes
kubectl get pods -A -o wide 
kubectl get pods --all-namespaces
```
