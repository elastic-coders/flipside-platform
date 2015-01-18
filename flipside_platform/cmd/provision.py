'''
flipside-provision command

'''
from invoke import run

import flipside_platform.aws


def do_provision(**opts):
    ''' Installs salt and ancillary packages in the master machine
    
    flipside-provision --target=[aws|vagrant] --salt-version --standalone
    '''
    target = opts.get('target')
    # not yet implemented salt version and standlone parameters handling!!
    salt_version = opts.get('salt-version')
    standalone = opts.get('standalone')
    if target == 'aws':
        flipside_platform.aws.provision(
            salt_version=salt_version, 
            standalone=standalone
        )
    elif target == 'vagrant':
        run('vagrant up --provision')

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', 
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    parser.add_argument('--salt-version', 
                        help='salt version for provisioning')
    parser.add_argument('--standalone', action='store_true', 
                        help='use standalone....')
    args = parser.parse_args()
    do_provision(**vars(args))

if __name__ == '__main__':
    main()
