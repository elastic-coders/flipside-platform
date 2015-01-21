'''
Utlities for creating wheel-based artifacts
'''
import sys
import os
import subprocess
import pkg_resources
import shutil

from .. import config


def get_package_name():
    return subprocess.check_output(
        [sys.executable, 'setup.py', '--name']
    )


def build(dist_dir, deps=True, py_version=2, ucs=4, **opts):
    try:
        import wheel
    except ImportError:
        raise ValueError('please install wheel')
    package_name = get_package_name()
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)
    # XXX we are creating a new dir out of the blue
    download_dir = config.get_app_download_dir()
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    wheelhouse = os.path.join(dist_dir, 'wheelhouse')
    subprocess.check_call([sys.executable, 'setup.py', 'bdist_wheel', '-d', wheelhouse])
    if deps:
        # XXX the followint python version and ucs checks are not 100% relevant
        if py_version is not None:
            assert sys.version_info[0] == py_version, 'Use python {} for this please'.format(py_version)
        if ucs is not None:
            assert ((sys.maxunicode >= 1114111) if ucs == 4 else (sys.maxunicode < 111411)), 'Use a UCS-{} python build please'.format(ucs)

        subprocess.check_call([sys.executable, '-m', 'pip', 'wheel', '--wheel-dir', wheelhouse, '--find-links', wheelhouse, '--download-cache', download_dir, '--use-wheel', package_name])
        for down in os.listdir(download_dir):
            if down.endswith('.whl'):
                shutil.copy(os.path.join(download_dir, down),
                            os.path.join(wheelhouse, down.split('%2F')[-1]))
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--find-links', wheelhouse, '--use-wheel', package_name])
