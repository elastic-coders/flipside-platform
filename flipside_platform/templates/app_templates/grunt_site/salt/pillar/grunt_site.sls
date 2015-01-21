# Configurable section
{%- for param, value in extra.items() %}
{{ '{% set ' ~  param ~ ' = "' ~ value ~ '" -%}' }}
{%- endfor %}
# END configurable section

{% raw -%}
{% set home = "/home/" ~ app_name %}
{% set root_dir = home ~ "/static"  %}

nginx:
  ng:
    server:
      config: 
        worker_processes: 4
        pid: /run/nginx.pid
        events:
          worker_connections: 768
        http:
          sendfile: 'on'
          include:
            - /etc/nginx/mime.types
            - /etc/nginx/conf.d/*.conf
            - /etc/nginx/sites-enabled/*.conf
    vhosts:
      managed:
        {{ app_name }}.conf:
          enabled: True
          config:
            - server:
              - server_name: {{ server_name }}
              - listen:
                - 80
              - location /:
                - root: {{ root_dir }}
                - index: index.html
                - expires: -1

users:
  {{ app_name }}:
    fullname: {{ app_name }}
    homedir: {{ home }}
    createhome: True

# XXX this only works for a single app!!!
grunt_site:
  app_name: {{ app_name }}
  root_dir: {{ root_dir }}
  home_dir: {{ home }}

{%- endraw %}
