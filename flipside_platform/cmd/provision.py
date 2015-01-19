'''
flipside-provision command

'''
from invoke import run

from .. import provision
from .. import config


def do_provision(target, salt_version, standalone):
    ''' Installs salt and ancillary packages in the master machine
    '''
    provision.upload_and_excecute_myself(target, salt_version, standalone)
    config.set_platform_config({'master': {'standalone': standalone}},
                               merge=True)


def main():
    # XXX this argument parsing is the same in flipside_platorm/provision.py
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    parser.add_argument('--salt-version',
                        help='salt version for provisioning',
                        default='stable')
    parser.add_argument('--standalone', action='store_true',
                        help='use salt in standalone mode (no daemons)')
    args = parser.parse_args()
    do_provision(**vars(args))

if __name__ == '__main__':
    main()
