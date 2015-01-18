'''
flipside-build command
'''
import importlib
import re
import shutil
import os

from .. import config


def do_build(**opts):
    app_config = config.get_app_config()
    build_dir = config.get_app_build_dir()
    build = app_config.get('build')
    if not build or not 'function' in build:
        raise ValueError('Build config not found')
    module, fun = re.match(r'^(.*)\.(.*)', build['function']).groups()
    module = importlib.import_module(module)
    fun = getattr(module, fun)

    # XXX salt config (unused for now)
    if os.path.exists(config.get_app_salt_path()):
        salt_dst_dir = os.path.join(build_dir,
                                    os.path.basename(config.get_app_salt_path()))
        shutil.rmtree(salt_dst_dir, ignore_errors=True)
        shutil.copytree(config.get_app_salt_path(), salt_dst_dir)
    opts.update(build.get('function_kwargs', {}))
    fun(build_dir, **opts)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--environment', help='deploy environment (staging, production, ...)')
    args = parser.parse_args()
    do_build(**vars(args))

if __name__ == '__main__':
    main()
