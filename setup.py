import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'rb') as f:
    requires = f.read().decode().splitlines()

setup(
    name='flipside-platform',
    version='0.0.1',
    description='Flipside platform automation',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flipside-init = flipside_platform.cmd.init:main',
            'flipside-template = flipside_platform.cmd.template:main',
            'flipside-buile = flipside_platform.cmd.build:main'
        ]
    }
)
