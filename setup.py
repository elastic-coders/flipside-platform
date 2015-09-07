import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'rb') as f:
    requires = f.read().decode().splitlines()

setup(
    name='flipside-platform',
    version='0.2-dev',
    description='Flipside platform automation',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flipside-{name} = flipside_platform.cmd.{name}:main'.format(name=name)
            for name in ('init', 'template', 'build', 'bootstrap', 'ssh',
                         'provision', 'configure', 'publish', 'deploy')
        ]
    }
)
