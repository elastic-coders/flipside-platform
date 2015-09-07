'''
Utlities for creating wheel-based artifacts
'''
import sys
import os
import subprocess
import pkg_resources
import shutil
import glob

from .. import config


def get_package_name():
    return subprocess.check_output(
        [sys.executable, 'setup.py', '--name']
    )


def build(dist_dir, deps=True, use_requirements=False, py_version=2, ucs=4, **opts):
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
        if use_requirements:
            subprocess.check_call([sys.executable, '-m', 'pip', 'wheel', '--wheel-dir', wheelhouse, '--use-wheel', '-r', 'requirements.txt'])
            for fname in glob.glob('requirements*.txt'):
                shutil.copy(fname, dist_dir)
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'wheel', '--wheel-dir', wheelhouse, '--find-links', wheelhouse, '--use-wheel', package_name])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--find-links', wheelhouse, '--use-wheel', package_name])


def build_django_frontend(dist_dir, frontend_dir='frontend', **kwargs):
    import importlib
    environ = kwargs.get('environment')
    if os.path.exists(os.path.join(frontend_dir, 'bower.json')):
        subprocess.check_call(
            [
                'bower', 'install'
            ],
            cwd=frontend_dir
        )
    if os.path.exists(os.path.join(frontend_dir, 'Gruntfile.js')):
        subprocess.check_call(
            [
                'grunt',
                'build{}'.format(':{}'.format(environ) if environ else '')
            ],
            cwd=frontend_dir
        )
    settings_module = kwargs.get('settings_module') or 'settings'
    frontend_dist_dir = os.path.join(dist_dir, frontend_dir)
    sys.path.insert(0, '.')
    try:
        settings = importlib.import_module(settings_module)
    finally:
        del sys.path[0]
    if os.path.exists(frontend_dist_dir):
        shutil.rmtree(frontend_dist_dir)
    for _, src_path in settings.STATICFILES_DIRS:
        shutil.copytree(src_path, os.path.join(frontend_dist_dir,
                                               os.path.basename(src_path)))
