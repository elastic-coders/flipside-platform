import subprocess
import os

from . import config


def platform_ssh(target, args=None, execlp=False):
    if target == 'aws':
        master_params = config.get_master_ssh_params(target)
        hostname = master_params.pop('HostName')
        opts = make_ssh_opts(master_params)
        cmd = ['ssh'] + opts + [hostname]
    elif target == 'vagrant':
        # We could just use ssh and its options...
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


def make_ssh_opts(params):

    def yo():
        for key, val in params.items():
            yield '-o'
            yield u'{}={}'.format(key, val)

    return list(yo())


def platform_scp(target, local, remote, direction):
    if direction not in ('up', 'down'):
        raise ValueError('bad direction')
    master_params = config.get_master_ssh_params(target)
    opts = make_ssh_opts(master_params)
    items = [local, u'{}://{}'.format(master_params['HostName'], remote)]
    if direction == 'down':
        items.reverse()
    subprocess.check_call(['scp', '-q'] + opts + items)


def platform_rsync(target, local, remote, direction):
    if direction not in ('up', 'down'):
        raise ValueError('bad direction')
    master_params = config.get_master_ssh_params(target)
    ssh_opts = make_ssh_opts(master_params)
    items = [local, u'{}://{}'.format(master_params['HostName'], remote)]
    if direction == 'down':
        items.reverse()
    subprocess.check_call(
        ['rsync', '-avz', '-e', 'ssh {}'.format(' '.join(ssh_opts))]
        + items
    )
