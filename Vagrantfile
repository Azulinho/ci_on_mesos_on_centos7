# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  machines = [
    { 'name' => 'centos7',
      'url' => 'https://github.com/holms/vagrant-centos7-box/releases/download/7.1.1503.001/CentOS-7.1.1503-x86_64-netboot.box',
      'ip' =>  '192.168.33.96' },
    { 'name' => 'suse12',
      'url' => 'http://sourceforge.net/projects/opensusevagrant/files/12.3/opensuse-12.3-32.box/download',
      'ip' =>  '192.168.33.97' }]

  machines.each do |item|
      config.vm.define item['name'] do |machine|
        machine.vm.box = item['name']
        machine.vm.box_url = item['url']
        machine.vm.hostname = item['name']
        machine.vm.network "private_network", ip: item['ip']
        machine.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: "venv"

        machine.vm.provider "virtualbox" do |vb|
          vb.memory = "1024"
          vb.linked_clone = true if Vagrant::VERSION =~ /^1.8/
        end

        machine.ssh.insert_key = false
        machine.ssh.private_key_path = ["~/.ssh/id_rsa", "~/.vagrant.d/insecure_private_key"]
        machine.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/authorized_keys"

        # provision all the VMs in parallel, we wait until we have booted
        # up all the VMs before executing ansible
      end
  end

  config.vm.provision :shell,
    inline: 'rpm -e patterns-openSUSE-minimal_base-conflicts || echo'

  config.vm.provision :shell,
    inline: 'test -e /usr/bin/zypper && zypper --non-interactive install python-pip'

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "site.yml"
    ansible.limit = "all"
    ansible.verbose = 'vvvv'
    ansible.sudo = true
    ansible.raw_arguments = ["-f", "5"]
    ansible.raw_ssh_args= ["-o ControlMaster=no", "-o ControlPersist=no", "-o ControlPath=/dev/null"]
    ansible.inventory_path = "./inventory/vagrant"
    ansible.groups = {
      "centos7" => ["192.168.33.96"],
      "suse12" => ["192.168.33.97"]
    }
  end
end
