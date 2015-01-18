import os
import json
import jinja2
import yaml


CONFIG_FILE = '.flipside-config.json'


def get_platform_config():
    if not os.path.isfile(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r+') as f:
        return json.load(f)

def set_platform_config(config, merge=True):
    if merge:
        default = get_platform_config()
        default.update(config)
    else:
        default = config
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(default))


def get_flipside_templates_base_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))


def get_flipside_app_templates_base_dir():
    return os.path.join(get_flipside_templates_base_dir(), 'app_templates')


def get_app_path():
    '''The base app path.'''
    # TODO: walk up the dir tree to retreive the base git poject dir
    return os.path.abspath('.')


def get_app_flipside_path():
    '''Path to the .flipside dir within the app.'''
    return os.path.join(get_app_path(), '.flipside')


def get_flipfile_path():
    return os.path.join(get_app_flipside_path(), 'flipfile.yaml')


def get_app_salt_path():
    return os.path.join(get_app_flipside_path(), 'salt')


def get_app_template_path(template_name):
    return os.path.join(get_flipside_app_templates_base_dir(), template_name)


def get_app_template_meta_path(template_name):
    return os.path.join(get_app_template_path(template_name), 'meta.yaml')


def get_app_template_meta(template_name):
    with open(get_app_template_meta_path(template_name), 'rb') as f:
        return yaml.load(f.read().decode())


def get_jinja_environment():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(get_flipside_templates_base_dir()),
        extensions=['jinja2.ext.do'],
        keep_trailing_newline=True,
    )
    return env


def get_app_config():
    '''Config for app as of flipfile.'''
    with open(get_flipfile_path(), 'rb') as f:
        return yaml.load(f.read().decode())


def get_app_build_dir():
    '''Directory where to build the app to'''
    return os.path.join(get_app_path(), '.flipside-build')


def get_app_download_dir():
    '''Cache downloaded files here'''
    return os.path.join(get_app_path(), '.flipside-download')
