from fabric.api import cd, env, put, sudo
import time

env.hosts = ['33.33.33.10']
env.password = 'vagrant'
env.user = 'vagrant'

def bootstrap():
    sudo('apt-get update')
    put('puppet.tgz', '/tmp/puppet.tgz')
    sudo('rm -rf /etc/puppet')
    with cd('/etc'):
        sudo('tar xfz /tmp/puppet.tgz')
    sudo('puppet apply /etc/puppet/manifests/server.pp')
    sudo('easy_install -U distribute')
    sudo('pip install plug==0.1.3')
    sudo('pip install virtualenv')

def deploy():
    put('pms-*.plug', '/tmp/')
    sudo('mkdir -p /etc/pms')
    put('vagrant.conf', '/tmp/pms.conf')
    sudo('mv /tmp/pms.conf /etc/pms')
    sudo('chown -R pms /etc/pms')
    sudo('plug install /tmp/pms-0.1.2.pms.plug')
    sudo('plug setup pms-0.1.2.pms.plug')
    sudo('/etc/init.d/nginx restart')
