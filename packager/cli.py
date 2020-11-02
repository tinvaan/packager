
import os
import yaml
import click

from os.path import join, exists, isfile, basename

from .utils import show, get_target_bundle


@click.group()
@click.pass_context
def cli(ctx):
    """Packager: Package your source code into distributable bundles"""
    ctx.ensure_object(dict)


@cli.command()
@click.option('--force', is_flag=True)
@click.pass_context
def init(ctx, force=False):
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

    show(config)
    return ctx.invoke(validate, config=open(config, 'r', encoding='utf-8'))


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
    assert data.get('package').get('build') in builds, "Unsupported build type"
    assert data.get('package').keys() and \
        len(set(data.get('package').keys()).difference(keys)) == 0, \
        "Missing required packager config key/values"
    assert data.get('package').get('targets') and \
        len(set(data.get('package').get('targets')).difference(targets)) == 0,\
        "Unsupported target specification"
    click.echo('\nConfig file at %s is valid' % config.name)
    return True, data


@cli.command()
@click.argument('config', type=click.File('r'))
def build(config):
    ctx = click.get_current_context()
    valid, data = ctx.forward(validate)
    if valid:
        for target in data.get('package', {}).get('targets', []):
            bundle = get_target_bundle(config, target)
            bundle.build()
        return
    click.echo('Config file at %s is invalid' % config.name)
