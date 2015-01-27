'''
Just copy to build dir.
'''
import shutil
import os


def build(dist_dir, environment, **kwargs):
    frontend_dir = os.path.join(dist_dir, 'frontend')
    if os.path.exists(frontend_dir):
        shutil.rmtree(frontend_dir)
    shutil.copytree('dist', frontend_dir)
