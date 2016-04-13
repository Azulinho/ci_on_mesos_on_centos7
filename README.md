

First set the following variables:

  export IP_ADDRESS=<ip address of the host to bootstrap>
  export REMOTE_USER=< remote user with sudo and ssh access>
  export HOSTNAME=<hostname of the remote box>

Then:

make bootstrap
make install

And you should have:

Mesos, Virtualbox, Vagrant installed.

A Mesos Master, a Mesos Slave and one zookeeper running.
You can access the Mesos Master on: http://IP_ADDRESS:5050

The marathon frameworks is also installed and available on http://IP_ADDRESS:8080

 
This setup would allow you to consume this mesos cluster through the Jenkins Mesos Plugin, and the (forked) Jenkins Vagrant plugin.
So that a jenkins job would allocate a mesos slave on demand and spin up an ephemeral vagrant instance (linux/windows/OSX) to run a particular build/test/deployment test job.


GOTCHAS:
 

Depending on the networking setup, you have to make sure the Mesos Master is using the correct ip address, when the master box has multiple IP addresses.


	cat /etc/default/mesos-master 
	PORT=5050
	ZK=`cat /etc/mesos/zk`
	ADVERTISE_IP=10.147.17.156
	IP=10.147.17.156


There is an issue with Centos 7 FirewallD and Docker. While it seems to be marked as fixed upstream, I had multiple issues and it wasn't clear if the cause was firewalld or not.
Disable the Firewall and check again.

