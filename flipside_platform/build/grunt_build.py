'''
Utlities for creating grunt-based artifacts
'''
import subprocess
import shutil
import os

from .. import config


def build(dist_dir, environment, **kwargs):
    subprocess.check_call(['grunt', 'build:{}'.format(environment)])
    frontend_dir = os.path.join(dist_dir, 'frontend')
    shutil.rmtree(frontend_dir)
    shutil.copytree('dist', frontend_dir)
