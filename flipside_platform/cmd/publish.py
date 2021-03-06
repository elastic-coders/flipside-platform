'''
flipside-publish command
'''
from .. import config
from .. import utils


def do_publish(target, tag='master'):
    build_dir = config.get_app_build_dir()
    archive_name_in_host = '{name}/{tag}'.format(tag=tag,
                                                 name=config.get_app_name())
    local = build_dir.rstrip('/') + '/'
    remote = '/srv/salt/dist/{}/'.format(archive_name_in_host)
    utils.platform_ssh(target, args=['mkdir', '-p', remote])
    utils.platform_rsync(target, local, remote, direction='up')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    args = parser.parse_args()
    do_publish(args.target)

if __name__ == '__main__':
    main()
