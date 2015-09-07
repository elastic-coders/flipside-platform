'''Deploy using salt master'''

from .. import utils
from .. import config


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    args = parser.parse_args()
    # XXX make this standalone/master switch more reusable and generic
    if config.is_platform_standalone():
        cmd = ['sudo salt-call state.highstate']
    else:
        cmd = ['sudo salt * --show-timeout --timeout 20 \* state.highstate']
    utils.platform_ssh(
        args.target,
        cmd,
        execlp=True)

if __name__ == '__main__':
    main()
