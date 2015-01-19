'''Configures the salt master


1. upload new salt stuff from .flipside/salt
 - state/ into /srv/salt
 - pillar/ into /srv/pillar
 - TODO: salt master config
 - TODO: salt minion config
2. `sudo salt \* saltutil.refresh_pillar`
3. TODO: `sudo salt \* saltutil.sync_modules`
'''
import importlib
import re
import os
import shutil

from .. import config
from .. import utils


def do_configure(target):
    raise NotImplemented('not yet tested')  # test me
    src_path = config.get_app_salt_path()
    # Old command:
    # for src, dst in [("salt/roots/", "/srv/salt"),
    #                  ("salt/pillar/", "/srv/pillar")]:
    #     cmd = ['rsync', '-avz',
    #            '--exclude', 'dist',
    #            '-e', 'ssh -l ubuntu -i {}'.format(key_path),
    #            src.rstrip('/') + '/',
    #            '{}:///{}/'.format(host, dst)
    #        ]
    transfers = [
        (os.path.join(src_path, 'state'), '/srv/salt/'),
        (os.path.join(src_path, 'pillar'), '/srv/pillar/'),
    ]
    for src, dst in transfers:
        utils.platform_rsync(
            target,
            local=src,
            remote=dst,
            direction='up'
        )
    # TODO: refresh pillar


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    args = parser.parse_args()
    do_configure(args.target)

if __name__ == '__main__':
    main()
