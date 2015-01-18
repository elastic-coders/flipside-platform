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
    raise NotImplemented('not tested yet')
    app_config = config.get_app_config()
    src_path = config.get_app_salt_path()
    transfers = [
        (os.path.join(src_path, 'state'), '/srv/salt/'),
        (os.path.join(src_path, 'pillar'), '/srv/pillar/'),
    ]
    for src, dst in transfers:
        if target == 'aws':
            config_ = config.get_platform_config()
            cmd = ['rsync', '-avz', '-e',
                   'ssh -l ubuntu -i {}'.format(_config['master']['keypair']),
                   build_dir.rstrip('/') + '/',
                   '{}://{}'.format(_config['master']['ip'], dst)]
            subprocess.check_call(cmd)
        elif target == 'vagrant':
            # TODO use rsync
            dst_dir = os.path.join('.dist', os.path.relpath(dst, '/'))
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.rmtree(dst_dir)
            shutil.copytree(src, dst_dir)
            cmd = 'cp -r {} {}'.format(os.path.join('/vagrant', dst_dir),
                                       dst)
            utils.platform_ssh(target, [cmd])
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
