import os
import functools
from suitable import Api

#ip_address = '10.147.17.156'
#hostname = 'centos7.zerotier'

ip_address = os.environ['IP_ADDRESS']
hostname = os.environ['HOSTNAME']
remote_user = os.environ['REMOTE_USER']

hosts = Api([ip_address], 
            remote_user=remote_user,
            sudo=True,
            host_key_checking=False, 
            UserKnownHostsFile='/dev/null',
            record_host_keys=False,
            verbosity='debug')

def echo(fn):
  @functools.wraps(fn)
  def wrapped(*v, **k):
    print("calling %s ..." % fn.__name__)
    fn()
  return wrapped

@echo
def add_epel_repository():
    hosts.yum(name='epel-release')

@echo
def install_vagrant():
  missing = False
  for k,v in hosts.command('rpm -qa')['contacted'].iteritems():
    if 'vagrant' not in v['stdout']:
      missing = True

  if missing:
    hosts.yum(name='https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.rpm')


@echo
def install_virtualbox():
  hosts.get_url(url='http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo', 
                dest='/etc/yum.repos.d/virtualbox.repo')
  
  hosts.yum(name='kernel-devel')
  hosts.yum(name='VirtualBox-5.0', update_cache='yes' )
  hosts.user(name=os.environ['USER'], groups='vboxusers', append='yes')

  loaded = False
  for k,v in hosts.command('lsmod')['contacted'].iteritems():
    if 'vboxdrv' in v['stdout']:
      loaded = True

  if not loaded:
    hosts.shell("KERN_DIR=/usr/src/kernels/"
                "`rpm -q kernel-devel --queryformat "
                "'%{version}-%{release}.%{arch}'` "
                "/usr/lib/virtualbox/vboxdrv.sh setup")
  hosts.service(name='vboxdrv', state='started', enabled='yes')


@echo
def install_mesos():
  hosts.yum(name='http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm')

  hosts.yum(name='mesosphere-zookeeper')
  hosts.yum(name='mesos')
  hosts.yum(name='marathon')

  hosts.command('echo 1 | sudo tee /var/lib/zookeeper/myid')
  hosts.lineinfile(dest='/etc/zookeeper/conf/zoo.cfg', 
                   line='server.1=%s:2888:3888' % ip_address)
  hosts.template(
   src='templates/zookeeper.xml.j2', 
   dest='/etc/firewalld/services/zookeeper.xml', 
   owner='root', 
   group='root', 
   mode='u=rw,g=r,o=r' 
  )

  hosts.service(name='firewalld', state='started', enabled='yes')
  hosts.service(name='firewalld', state='reloaded', enabled='yes')
  hosts.service(name='zookeeper', state='started', enabled='yes')

  hosts.lineinfile(dest='/etc/mesos/zk', 
                   line='zk://%s:2181/mesos' % ip_address,
                   create='yes')
  
  hosts.lineinfile(dest='/etc/mesos-master/quorum', 
                   line='1',
                   create='yes')

  hosts.lineinfile(dest='/etc/mesos-master/hostname', 
                   line=hostname,
                   create='yes')

  hosts.lineinfile(dest='/etc/marathon/conf/hostname', 
                   line=hostname,
                   create='yes')

  hosts.template(
   src='templates/mesos-master.xml.j2', 
   dest='/etc/firewalld/services/mesos-master.xml', 
   owner='root', 
   group='root', 
   mode='u=rw,g=r,o=r' 
  )
  hosts.template(
   src='templates/mesos-slave.xml.j2', 
   dest='/etc/firewalld/services/slave-master.xml', 
   owner='root', 
   group='root', 
   mode='u=rw,g=r,o=r' 
  )
  hosts.template(
   src='templates/marathon.xml.j2', 
   dest='/etc/firewalld/services/marathon.xml', 
   owner='root', 
   group='root', 
   mode='u=rw,g=r,o=r' 
  )
  hosts.service(name='mesos-master', state='started', enabled='yes')
  hosts.service(name='mesos-slave', state='started', enabled='yes')
  hosts.service(name='marathon', state='started', enabled='yes')


@echo
def update_os():
  hosts.yum(name='*',
            state='latest',
            update_cache='yes')

  updated = False
  for k,v in hosts.command('rpm -qa')['contacted'].iteritems():
    if v['changed']:
      updated = True

  if updated:
    print('reboot this')

        
update_os()
add_epel_repository()
install_mesos()
install_virtualbox()
install_vagrant()

