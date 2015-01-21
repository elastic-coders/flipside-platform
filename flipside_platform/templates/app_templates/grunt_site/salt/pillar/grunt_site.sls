# Configurable section
{%- for param, value in extra.items() %}
{{ '{% set ' ~  param ~ ' = "' ~ value ~ '" -%}' }}
{%- endfor %}
# END configurable section

{% raw -%}
{% set home = "/home/" ~ app_name %}

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
                - location ~ ^/favicon\.(ico|png)$:
                  - rewrite: (.*) /static/images$1
                - location ~ ^/robots\.txt$:
                  - rewrite: (.*) /static$1
                - location /static:
                  - alias: {{ home }}/static

users:
  {{ app_name }}:
    fullname: {{ app_name }}
    homedir: {{ home }}
    createhome: True
{%- endraw %}
