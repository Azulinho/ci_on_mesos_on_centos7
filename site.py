from suitable import Api

hosts = Api(['centos7.zerotier'], 
            remote_user='root', 
            sudo=True,
            verbosity='debug')


def install_vagrant():
  hosts.yum(name='https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.rpm')


def install_virtualbox():
  hosts.get_url(url='http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo', 
                dest='/etc/yum.repos.d/virtualbox.repo')
  
  hosts.yum(name='kernel-devel')
  hosts.yum(name='VirtualBox-5.0')


def install_mesos():
  hosts.yum(name='http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm')

  hosts.yum(name='mesosphere-zookeeper')
  hosts.yum(name='mesos')
  hosts.yum(name='marathon')

  hosts.command('echo 1 > /var/lib/zookeeper/myid')
  hosts.lineinfile(dest='/etc/zookeeper/conf/zoo.cfg', 
                   line='server.1=10.147.17.156:2888:3888')

  hosts.service(name='zookeeper', state='started', enabled='yes')

  hosts.lineinfile(dest='/etc/mesos/zk', 
                   line='zk://10.147.17.156:2181/mesos',
                   create='yes')
  
  hosts.lineinfile(dest='/etc/mesos-master/quorum', 
                   line='1',
                   create='yes')

  hosts.lineinfile(dest='/etc/mesos-master/hostname', 
                   line='centos7.zerotier',
                   create='yes')

  hosts.lineinfile(dest='/etc/marathon/conf/hostname', 
                   line='centos7.zerotier',
                   create='yes')

  hosts.service(name='mesos-master', state='started', enabled='yes')
  hosts.service(name='mesos-slave', state='started', enabled='yes')
  hosts.service(name='marathon', state='started', enabled='yes')

def update_os():
    hosts.yum(name='*',
              state='latest',
              update_cache='yes')
	

update_os()
install_mesos()
install_virtualbox()
install_vagrant()

