'''
flipside-build command
'''
import importlib
import re

from .. import config


def do_build():
    app_config = config.get_app_config()
    build_dir = config.get_app_build_dir()
    build = app_config.get('build')
    if not build or not 'function' in build:
        raise ValueError('Build config not found')
    module, fun = re.match(r'^(.*)\.(.*)', build['function']).groups()
    module = importlib.import_module(module)
    fun = getattr(module, fun)
    fun(build_dir, **build.get('function_kwargs', {}))


def main():
    do_build()

if __name__ == '__main__':
    main()
