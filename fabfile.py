from fabric.api import cd, env, put, sudo
import time

env.hosts = ['33.33.33.10']
env.password = 'vagrant'
env.user = 'vagrant'

def bootstrap():
    put('puppet.tgz', '/tmp/puppet.tgz')
    sudo('rm -rf /etc/puppet')
    with cd('/etc'):
        sudo('tar xfz /tmp/puppet.tgz')
    sudo('puppet apply /etc/puppet/manifests/server.pp --modulepath=/etc/puppet/modules')
    sudo('easy_install -U distribute')
    sudo('pip install gunicorn')
    sudo('pip install gevent')

def deploy():
    sudo('rm -rf /tmp/pms*')
    put('dist/pms-*.tar.gz', '/tmp')
    sudo('mkdir -p /etc/pms')
    put('vagrant.conf', '/tmp/pms.conf')
    sudo('mv /tmp/pms.conf /etc/pms')
    sudo('chown -R pms /etc/pms')
    sudo('pip install /tmp/pms-*.tar.gz')
    sudo('/etc/init.d/nginx restart')
    sudo('sv restart pms')
