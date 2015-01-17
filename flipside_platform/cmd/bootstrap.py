'''
flipside-bootstrap command

'''
from invoke import run

import flipside_platform.aws


def platform_bootstrap(target):
    '''Bootstrap the platform on different infrastructure types.'''
    if target == 'aws':
        # XXX ???
        flipside_platform.aws.bootstrap()
        # provision will be done later....
        # flipside_platform.aws.provision()
    elif target == 'vagrant':
        run('vagrant up --provision')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()
    do_boostrap(args.target)

if __name__ == '__main__':
    main()
