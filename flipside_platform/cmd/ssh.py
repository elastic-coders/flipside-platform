from .. import utils


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='target machine (aws, vagrant)',
                        choices=['vagrant', 'aws'], required=True)
    args = parser.parse_args()
    utils.platform_ssh(args.target, execlp=True)

if __name__ == '__main__':
    main()
