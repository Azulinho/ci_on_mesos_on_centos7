Deployment scripts for: Mesos Cluster + Marathon + Vagrant
===========================================================



USAGE:
=======

  virtualenv venv
  . venv/bin/activate
  pip install ansible

Edit inventory/<my new inventory>

  ansible-playbook -i inventory/<my new inventory> site.yaml

And you should have installed:

* Mesos
* Virtualbox
* Vagrant

And running:

* Mesos Master
* Mesos Slave
* zookeeper
* Marathon

You can access the Mesos Master on: http://IP_ADDRESS:5050

The marathon frameworks is also installed and available on http://IP_ADDRESS:8080


This setup would allow you to consume this mesos cluster through the Jenkins Mesos Plugin, and the (forked) Jenkins Vagrant plugin (https://github.com/Azulinho/vagrant-plugin.git)

So that a jenkins job would allocate a mesos slave on demand and spin up an ephemeral vagrant instance (linux/windows/OSX) to run a particular build/test/deployment test job.

this is a logfile of a jenkins job consuming a vagrant instance, inside a mesos slave:

	Started by user jenkins
	Mesos slave(hostname): 172.17.0.1
	[EnvInject] - Loading node environment variables.
	Building remotely on mesos-jenkins-89f5f525-e22a-41dd-a8d1-93ca0d39adf0 (mesos-512MB) in workspace /tmp/mesos/slaves/5d3fad8a-ab07-4eaa-9a82-04dc1dd5faa8-S0/frameworks/5d3fad8a-ab07-4eaa-9a82-04dc1dd5faa8-0002/executors/mesos-jenkins-89f5f525-e22a-41dd-a8d1-93ca0d39adf0/runs/c3b0bf6f-93ed-4a52-965e-adcd7c0fcf0f/jenkins/workspace/mesos
	[EnvInject] - Executing scripts and injecting environment variables after the SCM step.
	[EnvInject] - Injecting as environment variables the properties content
	HOME=/root

	[EnvInject] - Variables injected successfully.
	[mesos] $ vagrant -v
	Vagrant 1.8.1
	[ vagrant ]: Executing command :[vagrant, provision, --provision-with, virtualbox] in folder /tmp
	[/tmp] $ vagrant provision --provision-with virtualbox
	==> default: VM is not currently running. Please, first bring it up with `vagrant up` then run this command.
	[mesos] $ vagrant -v
	Vagrant 1.8.1
	[ vagrant ]: Executing command :[vagrant, up, --destroy-on-error, --provider=virtualbox] in folder /tmp
	[/tmp] $ vagrant up --destroy-on-error --provider=virtualbox
	Bringing machine 'default' up with 'virtualbox' provider...
	==> default: Checking if box 'boxcutter/ubuntu1404' is up to date...

	==> default: Clearing any previously set forwarded ports...

	==> default: Clearing any previously set network interfaces...

	==> default: Preparing network interfaces based on configuration...
	    default: Adapter 1: nat
	==> default: Forwarding ports...
	    default: 22 (guest) => 2222 (host) (adapter 1)
	==> default: Booting VM...

	==> default: Waiting for machine to boot. This may take a few minutes...
	    default: SSH address: 127.0.0.1:2222
	    default: SSH username: vagrant
	    default: SSH auth method: private key

	==> default: Machine booted and ready!
	==> default: Checking for guest additions in VM...

	==> default: Mounting shared folders...
	    default: /vagrant => /tmp

	==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
	==> default: flag to force provisioning. Provisioners marked to run always will still run.

	[mesos] $ vagrant -v
	Vagrant 1.8.1
	[ vagrant ]: Executing command :[vagrant, ssh, --command, df] in folder /tmp
	[/tmp] $ vagrant ssh --command df

	Filesystem                   1K-blocks   Used Available Use% Mounted on
	udev                            239252      4    239248   1% /dev
	tmpfs                            50084    416     49668   1% /run
	/dev/mapper/vagrant--vg-root  65156900 927208  60896780   2% /
	none                                 4      0         4   0% /sys/fs/cgroup
	none                              5120      0      5120   0% /run/lock
	none                            250404      0    250404   0% /run/shm
	none                            102400      0    102400   0% /run/user
	/dev/sda1                       240972  38666    189865  17% /boot
	vagrant                        2951456  12564   2938892   1% /vagrant

	[mesos] $ vagrant -v
	Vagrant 1.8.1
	[ vagrant ]: Executing command :[vagrant, destroy, --force] in folder /tmp
	[/tmp] $ vagrant destroy --force

	==> default: Forcing shutdown of VM...

	==> default: Destroying VM and associated drives...

	Finished: SUCCESS



GOTCHAS:
========

Depending on the networking setup, you have to make sure the Mesos Master is using the correct ip address, when the master box has multiple IP addresses.


	cat /etc/default/mesos-master
	PORT=5050
	ZK=`cat /etc/mesos/zk`
	ADVERTISE_IP=10.147.17.156
	IP=10.147.17.156


There is an issue with Centos 7 FirewallD and Docker. While it seems to be marked as fixed upstream, I had multiple issues and it wasn't clear if the cause was firewalld or not.
The playbooks in this example, disable firewalld and enable iptables



