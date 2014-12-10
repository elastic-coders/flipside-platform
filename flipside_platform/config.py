'''
Config generation.
'''
import os

import jinja2
import yaml


def _get_common_config(app_name, template):
    return {'app_name': app_name, 'template': template}


def get_flipside_config(app_name, template):
    '''Configuration for flipside.

    Returns:
      a dict representing the flipside config

    Args:
      app_name: the name of the app
      template: the flipside template name

    Raises:
      ValueError if template name is invalid
    '''
    return _get_common_config(app_name, template)


def get_salt_pillar_config(app_name, template):
    '''Configuration for salt.

    Returns:
      a dict representing the salt pillar

    Args:
      app_name: the name of the app
      template: the flipside template name

    Raises:
      ValueError if template name is invalid
    '''
    return _get_common_config(app_name, template)


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


def get_salt_path():
    return os.path.join(get_app_flipside_path(), 'salt')


def get_salt_pillar_path():
    return os.path.join(get_salt_path(), 'pillar.sls')


def get_salt_config_path():
    return os.path.join(get_salt_path(), 'config.yaml')


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
