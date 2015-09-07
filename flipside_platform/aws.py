'''Setup aws master-minion infrastrucuture and platform'''
import boto.ec2
import getpass
import logging
import os
import time

from . import config

logger = logging.getLogger(__name__)


def create_security_group(conn, name):
    groups = [g for g in conn.get_all_security_groups() if g.name == name]
    group = groups[0] if groups else None
    if not group:
        group = conn.create_security_group(name, 'This is {}'.format(name))
        group.authorize(ip_protocol='tcp',
                        from_port=str(22),
                        to_port=str(22),
                        cidr_ip='0.0.0.0/0')
        group.authorize(ip_protocol='tcp',
                        from_port=str(80),
                        to_port=str(80),
                        cidr_ip='0.0.0.0/0')
        group.authorize(ip_protocol='tcp',
                        from_port=str(443),
                        to_port=str(443),
                        cidr_ip='0.0.0.0/0')
    return group


def create_ec2(conn, group_name, keypair_name):
    reservation = conn.run_instances(image_id='ami-00b11177',
                                     key_name=keypair_name,
                                     security_groups=[group_name],
                                     instance_type='t1.micro')
    running_instance = reservation.instances[0]
    status = running_instance.update()
    while status == 'pending':
        logger.info('waiting 10 secs for the instance to come up...')
        time.sleep(10)
        status = running_instance.update()
    addr = conn.allocate_address()
    addr.associate(running_instance.id)
    return addr.public_ip


def bootstrap(key_name=None, group_name=None, askpass=False):
    opts = {}
    if askpass:
        opts['aws_access_key_id'] = raw_input('AWS access key: ')
        opts['aws_secret_access_key'] = getpass.getpass('AWS secret key: ')
    conn = boto.ec2.connect_to_region('eu-west-1', **opts)

    group_name = group_name or 'grp_{}'.format(config.get_app_name())
    key_name = key_name or 'key_{}'.format(config.get_app_name())
    group = create_security_group(conn, group_name)
    secrets_dir = config.get_secrets_dir()
    if not os.path.exists(secrets_dir):
        os.mkdir(secrets_dir, 0700)
    key_path = os.path.join(secrets_dir, '{}.pem'.format(key_name))
    try:
        key = conn.create_key_pair(key_name)
    except boto.exception.EC2ResponseError:
        # Key exists
        logger.warning('using existing access key {} that shoud be in {}'.format(
            key_name, key_path))
    else:
        os.umask(0x077)
        with open(key_path, 'w') as f:
            f.write(key.material)

    public_ip = create_ec2(conn, group_name, key_name)
    cfg = {
        'master': {
            'ssh': {
                'HostName': public_ip,
                'IdentityFile': key_path,
                'User': 'ubuntu'
            }
        }
    }
    config.set_platform_config(cfg, merge=False)
    conn.close()
