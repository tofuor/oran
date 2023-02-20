echo "docker install ..."
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl status docker
sudo systemctl start docker

echo "install kubernetes ..."
sudo curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/kubernetes.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/kubernetes.gpg] http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list
apt-cache madison kubeadm
K_VER="1.26.1-00"
sudo apt install -y kubelet=${K_VER} kubectl=${K_VER} kubeadm=${K_VER}
sudo apt-mark hold kubeadm kubelet kubectl
sudo kubeadm version

echo "deploy kubernetes ..."
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
# sudo nano /etc/modules-load.d/containerd.conf
# overlay
# br_netfilter
sudo modprobe overlay
sudo modprobe br_netfilter

# sudo nano /etc/sysctl.d/kubernetes.conf
# net.bridge.bridge-nf-call-ip6tables = 1
# net.bridge.bridge-nf-call-iptables = 1
# net.ipv4.ip_forward = 1
sudo sysctl --system

echo "install containerd"
apt-get install -y git vim curl net-tools openssh-server python3-pip nfs-common apt-transport-https ca-certificates
# install containerd
wget https://github.com/containerd/containerd/releases/download/v1.6.2/containerd-1.6.2-linux-amd64.tar.gz
sudo tar Czxvf /usr/local containerd-1.6.2-linux-amd64.tar.gz
# Then, download the systemd service file and set it up so that you can manage the service via systemd.
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mv containerd.service /usr/lib/systemd/system
#restart container service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd

#cleak
sudo systemctl status containerd

echo "install runC"
wget https://github.com/opencontainers/runc/releases/download/v1.1.1/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

sudo mkdir -p /etc/containerd/
containerd config default | tee /etc/containerd/config.toml
sudo nano  /etc/containerd/config.toml
######################################
SystemdCgroup = false -> true
######################################
sudo systemctl restart containerd