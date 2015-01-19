include:
  - memcached
  - nginx.ng
  - rsyslog
  - users
  - uwsgi_ng

python3:
  pkg.installed

python3-pip:
  pkg.installed

python-virtualenv:
  pkg.installed
