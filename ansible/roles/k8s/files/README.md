# Setup Kubernetes cluster on ubuntu

![](../images/kubernetes.jpg)

```sh
# installing Kubernetes
sudo apt-get update && sudo apt-get upgrade -y
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
sudo kubeadm init
kubeadm join
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
