# Setup Kubernetes cluster on ubuntu

```sh
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install kubeadm kubectl kubelet -y 
sudo apt-mark hold kubeadm kubelet kubectl 

sudo systemctl enable docker
sudo systemctl start docker

sudo kubeadm init
kubeadm join

kubectl get nodes
kubectl get pods --all-namespaces
```