# Configurable section
{%- for param, value in extra.items() %}
{{ '{% set ' ~  param ~ ' = "' ~ value ~ '" -%}' }}
{%- endfor %}
# set to True to enable ssl (needs secrets in django_site_secrets state)
{{ '{% set enable_ssl = False %}' }}

# END configurable section

{% raw -%}
{% set home = "/home/" ~ app_name %}
{% set uwsgi_socket = home ~ "/uwsgi.sock" %}
{% set ssl_cert_path = "/etc/nginx/ssl/" ~ app_name ~ "/server.crt" %}
{% set ssl_key_path = "/etc/nginx/ssl/" ~ app_name ~ "/server.key" %}

django_site:
  app_name: {{ app_name }}
  ssl_cert_path: {{ ssl_cert_path }}
  ssl_key_path: {{ ssl_key_path }}
  enable_ssl: {{ enable_ssl }}

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
              {%- if enable_ssl %}
              - listen 443 ssl
              - ssl_certificate: {{ ssl_cert_path }}
              - ssl_certificate_key: {{ ssl_key_path }}
              {%- endif %}
              - location /:
                - uwsgi_pass: unix://{{ uwsgi_socket }}
                - include: uwsgi_params
                {#- uncomment if behind load balancer - uwsgi_param:  UWSGI_SCHEME $http_x_forwarded_proto #}
                - uwsgi_param: SERVER_SOFTWARE nginx/$nginx_version
                - location ~ ^/favicon\.(ico|png)$:
                  - rewrite: (.*) /static/images$1
                - location ~ ^/robots\.txt$:
                  - rewrite: (.*) /static$1
                - location /static:
                  - alias: {{ home }}/static
                - location /media:
                  - alias: {{ home }}/media
                {%- if enable_ssl %}
                - if ($https = ""):
                    - rewrite: ^/[a-zA-Z\-]*/admin https://$host$request_uri? permanent
                {%- endif %}

users:
  {{ app_name }}:
    fullname: {{ app_name }}
    homedir: {{ home }}
    createhome: True
    groups:
      - uwsgi

uwsgi_ng:
  apps:
    managed:
      {{ app_name }}:
        home: {{ home }}
        package_name: {{ package_name }}
        uwsgi_socket: {{ uwsgi_socket }}
{%- endraw %}
