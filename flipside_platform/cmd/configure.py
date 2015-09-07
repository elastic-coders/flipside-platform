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
import logging
import subprocess
import time

from .. import config
from .. import utils


def do_configure(target, do_config=False):
    src_path = config.get_app_salt_path()
    app_config = config.get_app_config()
    transfers = [
        (os.path.join(src_path, 'state'), '/srv/salt/'),
        (os.path.join(src_path, 'pillar'), '/srv/pillar/'),
    ]
    for src, dst in transfers:
        utils.platform_rsync(
            target,
            local=src.rstrip('/') + '/',
            remote=dst,
            direction='up'
        )
    standalone = config.is_platform_standalone()
    if do_config:
        salt_config_path = config.get_app_salt_config_path()
        dst_config_path = '/etc/salt/{}.d/01-flipside-app-{}.conf'.format(
            'minion' if standalone else 'master',
            config.get_app_name()
        )
        remote_tmp = '/tmp/xxxx'  # XXX
        utils.platform_scp(
            target,
            local=salt_config_path,
            remote=remote_tmp,
            direction='up'
        )
        utils.platform_ssh(
            target,
            args=['sudo', 'cp', remote_tmp, dst_config_path]
        )
        if not standalone:
            utils.platform_ssh(
                target,
                args=['sudo', 'service', 'salt-master', 'restart']
            )
            for i in range(5):
                try:
                    utils.platform_ssh(
                        target,
                        args=['sudo', 'salt', '-l', 'quiet', '\*', 'test.ping']
                    )
                except subprocess.CalledProcessError:
                    logging.warning('retrying to connect to minions. Sleeping')
                    time.sleep(1)
                    pass
                else:
                    break
            else:
                logging.error('Could not reach minions after restart')

    # TODO: refresh pillar


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    parser.add_argument('--config',
                        help='update master config too (restarts master)',
                        action='store_true',
                        default=True)
    args = parser.parse_args()
    do_configure(args.target, args.config)

if __name__ == '__main__':
    main()
