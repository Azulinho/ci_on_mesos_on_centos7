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
      'url' => 'http://sourceforge.net/projects/opensusevagrant/files/12.3/opensuse-12.3-64.box/download',
      'ip' =>  '192.168.33.97' }]

  machines.each do |item|
    config.vm.define item['name'] do |machine|
      machine.vm.box = item['name']
      machine.vm.box_url = item['url']
      machine.vm.hostname = item['name']
      machine.vm.network "private_network", ip: item['ip']
      #machine.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: "venv"

      machine.vm.provider "virtualbox" do |vb|
        vb.memory = "1024"
        # https://github.com/hashicorp/otto/issues/423#issuecomment-186076403
        vb.linked_clone = true if Vagrant::VERSION =~ /^1.8/
        vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
        vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
        if item['name'] == 'centos7'
          vb.customize ["storagectl",  :id, "--name", "SATA Controller", "--hostiocache", "on"]
        else
          vb.customize ["storagectl",  :id, "--name", "SATA", "--hostiocache", "on"]
        end
      end
    end
  end

$script = <<SCRIPT
#!/bin/bash
if [ -e "/etc/SuSE-release" ]; then
  test -e /etc/bootstrap.python || ( rpm -e patterns-openSUSE-minimal_base-conflicts-12.3-7.10.1.x86_64  || echo )
  test -e /etc/bootstrap.python || ( zypper install -y python python-xml && touch /etc/bootstrap.python)
fi
rm -f /etc/udev/rules.d/70-persistent-net.rules
SCRIPT

  config.vm.provision :shell, inline: $script

  config.vm.provision :ansible do |ansible|
    ansible.playbook = 'site.yml'
    ansible.inventory_path = 'inventory/vagrant'
    if ENV.key?('LIMIT')
      ansible.limit=ENV['LIMIT']
    end
    if ENV.key?('TAGS')
      ansible.tags=ENV['TAGS']
    end
    if ENV.key?('START_AT_TASK')
      ansible.start-at-task=ENV['START_AT_TASK']
    end
  end
end
