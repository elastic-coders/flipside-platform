'''
flipside-bootstrap command

'''
from invoke import run

import flipside_platform.aws


def do_bootstrap(target, key_name=None):
    '''Bootstrap the platform on different infrastructure types.'''
    if target == 'aws':
        # XXX ???
        flipside_platform.aws.bootstrap(key_name=key_name)
        # provision will be done later....
        # flipside_platform.aws.provision()
    elif target == 'vagrant':
        run('vagrant up --provision')
        print "done"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('keyname')
    args = parser.parse_args()
    target = args.target.split("=")
    key_name = args.keyname.split("=")
    do_bootstrap(target[1], key_name[1])

if __name__ == '__main__':
    main()
