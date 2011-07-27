include nginx
class lucid64 {
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

  package { "python-pip":
    ensure => present,
  }

  package { "python-distribute":
    ensure => present,
  }

  package { "git-core":
    ensure => present,
  }

  user { "pms":
    comment => 'This user was created by Puppet',
    ensure => 'present',
  }

  file { "/etc/sv/pms" :
    ensure => directory,
    mode => 644,
    owner => "root",
  }

  file { "/etc/sv/pms/run":
    require => File["/etc/sv/pms"],
    mode => 755,
    content => "#!/bin/sh

GUNICORN=/usr/local/bin/gunicorn
ROOT=/etc/sv/pms
PID=/var/run/pms.pid

APP=pms.app:app

cd \$ROOT
exec \$GUNICORN \$APP
"
  }

  file { "/etc/service/pms":
    ensure => link,
    target => "/etc/sv/pms",
    require => File["/etc/sv/pms"],
  }

  nginx::site { "pms":
    domain => "pms",
    aliases => [],
    default_vhost => true,
    root => "/var/www/pms",
    upstreams => ["127.0.0.1:8000"],
  }
}

include lucid64
include mongodb
