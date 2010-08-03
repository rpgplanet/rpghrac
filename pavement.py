from paver.easy import *
from paver.setuputils import setup

from setuptools import find_packages

VERSION = (0, 1, 2)

__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'rpghrac',
    version = __versionstr__,
    description = 'RPG hrac',
    long_description = '\n'.join((
        'RPG hrac',
        '',
    )),
    author = 'Almad',
    author_email='bugs@almad.net',
    license = 'BSD',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
 
    install_requires = [
        'setuptools>=0.6b1',
    ],
)

@task
def freeze_requirements():
    sh('pip freeze -r requirements.txt > freezed-requirements.txt')
    

@task
@needs('freeze_requirements', 'setuptools.command.sdist')
def sdist():
    """ Custom sdist """

@task
def deploy_production():
    """ Deploy to production server """
    sh('fab deploy')
