
import os
import yaml
import click

from collections import OrderedDict
from os.path import join, exists, isfile, basename

from .configs.base import *
from .bundles.deb import Debian


def get_target_bundle(config, target):
    target = target.lower()
    '''TODO
    if target == 'rpm':
        return RPMConfig(config.name)
    if target == 'tar'  or target == 'archive':
        return ArchiveConfig(config.name)
    if target == 'pacman':
        return PacmanConfig(config.name)
    '''
    if target == 'deb' or target == 'debian':
        return Debian(DebConfig(config.name))


@click.group()
def cli():
    """Packager: Package your source code into distributable bundles"""
    pass


@cli.command()
@click.option('--force', is_flag=True)
def init(force=False):
    workdir = join(os.getcwd(), '.packager')
    os.makedirs(workdir, exist_ok=True)
    config = join(workdir, 'config.yml')
    if not (exists(config) and isfile(config)) or force:
        with open(config, 'w') as f:
            yaml.dump({
                'package': {
                    'name': basename(os.getcwd()),
                    'version': "1.0.0",
                    'description': "Add package description here",
                    'build': '',
                    'authors': list(),
                    'maintainers': list(),
                    'targets': list()
                }
            }, f, sort_keys=False)


@cli.command()
@click.argument('config', type=click.File('r'))
def validate(config):
    builds = set(['cmake', 'qmake', 'make'])
    targets = set(['debian', 'rpm', 'pacman'])
    keys = set([
        'name',
        'version',
        'description',
        'build',
        'authors',
        'maintainers',
        'targets'
    ])
    data = yaml.safe_load(config)
    assert data.get('package').get('build') in builds
    assert data.get('package').keys() and \
        len(set(data.get('package').keys()).difference(keys)) == 0
    assert data.get('package').get('targets') and \
        len(set(data.get('package').get('targets')).difference(targets)) == 0
    click.echo('\nConfig file at %s is valid' % config.name)


@cli.command()
@click.argument('config', type=click.File('r'))
def build(config):
    data = yaml.safe_load(config)
    for target in data.get('package').get('targets'):
        bundle = get_target_bundle(config, target)
        bundle.build()
