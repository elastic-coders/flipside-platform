{% raw -%}
{% from "nginx/ng/map.jinja" import nginx with context -%}
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

{% if pillar.django_site.get('ssl_cert') -%}
app-{{ pillar.django_site.app_name }}-nginx-cert:
  file.managed:
    - name: {{ pillar.django_site.ssl_cert_path }}
    - makedirs: True
    - mode: 660
    - user: {{ nginx.lookup.webuser }}
    - group: root
    - contents_pillar: django_site:ssl_cert

app-{{ pillar.django_site.app_name }}-nginx-key:
  file.managed:
    - name: {{ pillar.django_site.ssl_key_path }}
    - makedirs: True
    - mode: 660
    - user: {{ nginx.lookup.webuser }}
    - group: root
    - contents_pillar: django_site:ssl_key
{% endif -%}
{% endraw -%}
