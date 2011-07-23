
class lucid64 {
  package { "nginx":
    ensure => present,
    require => Exec["Update APT"],
  }

  file { "/etc/nginx/nginx.conf":
    source => "file:///etc/puppet/files/etc/nginx/sites-enabled/pms"
  }

  exec { "Update APT":
    command => "/usr/bin/apt-get -q -q update",
  }

  package { "libevent-dev":
    ensure => present,
  }

  package { "python-dev":
    ensure => present,
  }

  package { "beanstalkd":
    ensure => present,
  }

  package { "runit":
    ensure => present,
  }

  user { "pms":
    comment => 'This user was created by Puppet',
    ensure => 'present',
  }


  package { "python-pip":
    ensure => present,
  }

  package { "python-distribute":
    ensure => present,
  }

  package { "git-core":
    ensure => present,
  }
}



include lucid64
include mongodb
