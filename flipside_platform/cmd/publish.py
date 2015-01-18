'''
flipside-publish command
'''
import importlib
import re

from .. import config
from .. import utils


def do_publish(target, tag='master'):
    raise NotImplemented('not tested yet')
    app_config = config.get_app_config()
    build_dir = config.get_app_build_dir()
    archive_name_in_host = '{name}/{tag}'.format(tag=tag,
                                                 name=app_config['appName'])
    if target == 'aws':
        config = config.get_platform_config()
        cmd = ['rsync', '-avz', '-e',
               'ssh -l ubuntu -i {}'.format(config['master']['keypair']),
               build_dir.rstrip('/') + '/',
               '{}:///srv/salt/dist/{}/'.format(config['master']['ip'],
                                                archive_name_in_host)]
        subprocess.check_call(cmd)
    elif target == 'vagrant':
        # TODO use rsync
        dst_dir = '.dist/{}'.format(archive_name_in_host)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.rmtree(dst_dir)
        shutil.copytree(archive, dst_dir)
        utils.platform_ssh(ctx, target, [
            'cp',
            '-r',
            '/vagrant/.dist/{}'.format(name),
            '/srv/salt/dist'])


def main():
    do_publish()

if __name__ == '__main__':
    main()
