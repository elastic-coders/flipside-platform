'''
flipside-bootstrap command

'''
import subprocess

import flipside_platform.aws


def do_bootstrap(**opts):
    '''Bootstrap the platform on different infrastructure types.'''
    target = opts.get('target')
    key_name = opts.get('keyname')
    if target == 'aws':
        flipside_platform.aws.bootstrap(key_name=key_name)
    elif target == 'vagrant':
        subprocess.check_call(['vagrant', 'up', '--no-provision'])


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    parser.add_argument('--keyname',
                        help='aws keypair name. Will be stored in .secrets/',
                        default='keypair')
    parser.add_argument('--askpass', action='store_true',
                        help='ask aws security credentials')
    args = parser.parse_args()
    do_bootstrap(**vars(args))

if __name__ == '__main__':
    main()
