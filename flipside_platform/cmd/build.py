'''
flipside-build command
'''
import importlib
import re
import os

from .. import config


def do_build(**opts):
    app_config = config.get_app_config()
    build_dir = config.get_app_build_dir()
    build = app_config.get('build')
    if not build:
        raise ValueError('Build config not found')
    if not isinstance(build, (list, tuple)):
        build = (build,)
    for build_item in build:
        if not 'function' in build_item:
            raise ValueError('bad build config')
        module, fun = re.match(r'^(.*)\.(.*)', build_item['function']).groups()
        module = importlib.import_module(module)
        fun = getattr(module, fun)
        opts.update(build_item.get('function_kwargs') or {})
        fun(build_dir, **opts)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--environment', help='deploy environment (staging, production, ...)')
    args = parser.parse_args()
    do_build(**vars(args))

if __name__ == '__main__':
    main()
