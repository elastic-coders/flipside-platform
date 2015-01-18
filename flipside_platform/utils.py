import subprocess
import os

from . import config


def platform_ssh(target, args=None, execlp=False):
    if target == 'aws':
        config_ = config.get_platform_config()
        cmd = ['ssh', '-i', config_['master']['keypair'],
               'ubuntu@{}'.format(config_['master']['ip'])]
    elif target == 'vagrant':
        cmd = ['vagrant', 'ssh', '--']
    else:
        print('crazy stuff')
        return
    if args:
        cmd.extend(args)
    if execlp:
        cmd.insert(0, cmd[0])
        os.execlp(*cmd)
    else:
        subprocess.check_call(cmd)
