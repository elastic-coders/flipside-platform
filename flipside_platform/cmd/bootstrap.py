'''
flipside-bootstrap command

'''
from invoke import run

import flipside_platform.aws


def do_bootstrap(**opts):
    '''Bootstrap the platform on different infrastructure types.'''
    target = opts.get('target')
    key_name = opts.get('keyname')
    if target == 'aws':
        # XXX ???
        flipside_platform.aws.bootstrap(key_name=key_name)
        # provision will be done later....
        # flipside_platform.aws.provision()
    elif target == 'vagrant':
        run('vagrant up --provision')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='target machine (aws, vagrant)')
    parser.add_argument('--keyname', help='pem file name, must be in ./secret')
    args = parser.parse_args()
    do_bootstrap(**vars(args))

if __name__ == '__main__':
    main()
