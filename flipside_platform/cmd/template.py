'''
flipside-template command
'''
import os
import glob
import yaml

from .. import config


def do_list():
    path = config.get_flipside_deploy_templates_path()
    for meta in glob.glob(os.path.join(path, '*/meta.yaml')):
        with open(meta, 'rb') as f:
            print(u'{}: {}'.format(os.path.dirname(meta), yaml.load(f)))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')
    list_parser = subparsers.add_parser('list')
    args = parser.parse_args()
    if args.subparser_name == 'list':
        do_list()
    else:
        assert False

if __name__ == '__main__':
    main()
