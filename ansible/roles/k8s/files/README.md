# Setup Kubernetes cluster on ubuntu

```sh
sudo apt-get update && sudo apt-get install -y kubelet kubeadm kubectl
sudo systemctl enable docker
sudo systemctl start docker
sudo apt install kubeadm kubelet kubectl 
sudo apt-mark hold kubeadm kubelet kubectl 
sudo kubeadm init
kubeadm join

kubectl get nodes
kubectl get pods --all-namespaces
```