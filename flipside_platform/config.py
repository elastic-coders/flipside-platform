import os
import re
import subprocess

import jinja2
import yaml


def get_platform_config():
    fname = get_app_platform_config_path()
    if not os.path.isfile(fname):
        raise ValueError('platform config file {} not found'.format(fname))
    with open(fname, 'r') as f:
        return yaml.load(f)


def set_platform_config(config, merge=True):
    if merge:
        default = get_platform_config()
        default.update(config)
    else:
        default = config
    with open(get_app_platform_config_path(), 'wb') as f:
        f.write(yaml.dump(default).encode())


def get_master_ssh_params(target):
    if target == 'vagrant':
        # TODO: cache this
        ssh_cfg_out = subprocess.check_output(['vagrant', 'ssh-config']).decode()
        params = {'UserKnownHostsFile': '/dev/null',
                  'StrictHostKeyChecking': 'no'}
        for param in ('IdentityFile', 'Port', 'HostName', 'User'):
            mo = re.search(r'^[ ]+{} (.*)$'.format(param), ssh_cfg_out,
                           re.MULTILINE)
            if not mo:
                raise ValueError('bad vagrant ssh config')
            params[param] = mo.group(1)
    elif target == 'aws':
        platform = get_platform_config()
        return platform['master']['ssh']
    return params


def get_app_platform_config_path():
    return os.path.join(get_app_path(), '.flipside-platform.yaml')



def get_flipside_base_dir():
    '''Base dir of the installed flipside package'''
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


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


def get_app_salt_config_path():
    return os.path.join(get_app_salt_path(), 'config.yaml')


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


def is_platform_standalone():
    try:
        return get_platform_config()['master'].get('standalone', False)
    except KeyError:
        return False
