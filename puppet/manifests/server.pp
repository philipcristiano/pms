
class lucid64 {

  file { "/etc/nginx/nginx.conf":
    source => "file:///etc/puppet/files/etc/nginx/sites-enabled/pms"
  }

  package { "nginx":
    ensure => present,
    require => Exec["Update APT"],
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
