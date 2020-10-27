from setuptools import setup

setup(
    name='SOBERS',
    version='0.0.1',
    author='M. Oner Yalcin',
    author_email='oneryalcin@gmail.com',
    packages=['sobers'],
    entry_points={
        'console_scripts': ['sobers-console=sobers.console:main'],
    },
    description='Type aware, with built in validation, Plugin based CSV cleaner',
)
