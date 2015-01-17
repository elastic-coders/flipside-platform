'''
Representation of app template
'''
import yaml

from . import config


class AppTemplateNotFound(Exception):
    pass



def get_app_template_meta_path(app_template):
    return os.path.join(config.get_flipside_app_templates_base_dir(), app_template)


def get_app_template():
    app_config = config.get_app_config()
    meta_path = config.get_app_template_meta_path(app_config['template'])
    if not os.path.exists(meta_path):
        raise AppTemplateNotFound(meta_path)
    with open(meta_path, 'rb') as f:
        return yaml.load(f.read().decode())
