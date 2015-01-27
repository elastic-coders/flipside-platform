'''
Utlities for creating grunt-based artifacts
'''
import subprocess

from . import frontend


def build(dist_dir, environment, **kwargs):
    subprocess.check_call(['grunt', 'build:{}'.format(environment)])
    frontend.build(dist_dir, environment, **kwargs)
