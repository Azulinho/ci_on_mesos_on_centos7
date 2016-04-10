#!/bin/sh

sudo yum -y install python-virtualenv python-devel openssh-server
sudo yum -y groupinstall "Development Tools"
which pip || (curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python2.7)
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
test -e ~/.ssh/id_rsa || ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ''
sudo test -e /root/.ssh || sudo mkdir -p /root/.ssh
sudo grep "$(cat ~/.ssh/id_rsa.pub)" /root/.ssh/authorized_keys || (cat ~/.ssh/id_rsa.pub | sudo tee -a /root/.ssh/authorized_keys )
sudo systemctl enable sshd.service
sudo systemctl start sshd.service
