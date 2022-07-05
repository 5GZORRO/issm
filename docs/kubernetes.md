# Bootstrap Kubernetes Cluster v1.19

Follow these instructions to install Kubernetes cluster.

Create Ubuntu 20.04 VMs with 2vCPUs 8GB RAM 100 GB disk

For all VMs (master and nodes) perform the below

## Docker CE 19.03.9
Update packages

```
sudo apt-get update
sudo apt-get upgrade
```
The below commands are taken from the [docker installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

```
sudo apt-get update
```

Install some utilities

```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

Add the key and ensure its fingerprint

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
```

Register docker repository

```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
```

Install docker 19.03.9

```
sudo apt-get install docker-ce=5:19.03.9~3-0~ubuntu-focal containerd.io
```

Verify docker

```
sudo docker run hello-world
```

## Turn swap off

```
sudo swapoff -a
```

Run `sudo vi /etc/fstab` and comment out swap partition

Invoke `top` and ensure swap not used


## Kubelet, Kubectl, Kubeadm
Become sudo `sudo -s` and run the below to install the exact versions of kubernetes plane on your node

```bash
apt-get update && apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -qy kubelet=1.19.4-00 kubectl=1.19.4-00 kubeadm=1.19.4-00 kubernetes-cni=0.8.7-00
apt-mark hold kubelet kubeadm kubectl
sysctl net.bridge.bridge-nf-call-iptables=1
```

## kubeadm init (master node)

**Log into master node**

run the below under sudo

```
kubeadm init --pod-network-cidr=10.244.0.0/16
```

Exit `sudo`

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Install flannel as default CNI. The below taken from [here](https://github.com/coreos/flannel/blob/master/README.md#deploying-flannel-manually)

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

Wait until all running

```
kubectl get pod --all-namespaces
```

## kubeadm join (worker nodes)

**Log into a worker node and become root (sudo -s)**

Invoke the `kubeadm join ...` command that kube init printed in master node

On kubernetes master, list the nodes and ensure your VM appears

```
kubectl get nodes -o wide
```

