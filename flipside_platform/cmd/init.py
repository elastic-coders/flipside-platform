'''
flipside init
'''
import os

import yaml

from .. import config


def _render_to_file(template, path, context=None, force=False):
    if not force and os.path.exists(path):
        raise ValueError(
            u'File {} exists. Flipside is already inited'.format(path)
        )
    env = config.get_jinja_environment()
    content = env.get_template(template).render(context or {}).encode('utf8')
    with open(path, 'wb+') as f:
        f.write(content)


def _write_flipfile(app_name, template, force=False):
    path = config.get_flipfile_path()
    cfg = config.get_flipside_config(app_name, template)
    _render_to_file('flipfile.yaml', path, context=cfg, force=force)


def _write_saltstack_pillar(app_name, template, force=False):
    salt_path = config.get_salt_path()
    if not os.path.isdir(salt_path):
        os.makedirs(salt_path)
    cfg = config.get_salt_pillar_config(app_name, template)
    path = config.get_salt_pillar_path()
    template =
    _render_to_file('salt/{}/pillar.sls'.format(template), path, context=cfg,
                    force=force)
    path = config.get_salt_config_path()
    _render_to_file('salt/{}/config.yaml'.format(template), path, context=cfg,
                    force=force)


def do_init(app_name, template, force=False):
    _write_flipfile(app_name, template, force=force)
    _write_saltstack_pillar(app_name, template, force=force)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name')
    parser.add_argument('template')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    do_init(args.app_name, args.template, force=args.force)


if __name__ == '__main__':
    main()
