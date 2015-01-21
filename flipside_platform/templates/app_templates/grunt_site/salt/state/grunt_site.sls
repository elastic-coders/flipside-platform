{% raw -%}
{% from "nginx/ng/map.jinja" import nginx with context %}
include:
  - nginx.ng
  - users

{% set app_name = pillar['grunt_site'].app_name %}
{% set root_dir = pillar['grunt_site'].root_dir %}
{% set home_dir = pillar['grunt_site'].home_dir %}

# XXX not sure this is sane
remove-nginx-default-{{ app_name }}:
  file.absent:
    - name: /etc/nginx/sites-enabled/default

# XXX not sure this is sane
nginx-reload-{{ app_name }}:
  service.running:
    - name: nginx
    - reload: True
    - watch:
        - file: remove-nginx-default-{{ app_name }}

app-{{ app_name }}-dist:
  file.recurse:
    - name: {{ root_dir }}
    - source: {{ 'salt://dist/' ~ app_name ~ '/master/frontend' }}
    - group: {{ nginx.lookup.webuser }}
    - dir_mode: 750
    - file_mode: 640

app-{{ app_name }}-home-perms:
  file.directory:
    - name: {{ home_dir }}
    - group: {{ nginx.lookup.webuser }}

{% endraw -%}


