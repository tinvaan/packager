
import os
import yaml
import click

from os.path import join, exists, isfile, basename

from .utils import show, target_bundle


default = join(os.getcwd(), '.packager/config.yml')


@click.group()
@click.pass_context
def cli(ctx):
    """Packager: Package your source code into distributable bundles"""
    ctx.ensure_object(dict)


@cli.command()
@click.option('--force', is_flag=True)
@click.pass_context
def init(ctx, force=False):
    """
    Initialize a project with packager config file
    """
    valid = False
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

    if not ctx.obj.get('dev', False):
        show(config)
        ctx.obj['init'] = True
        valid, data = ctx.invoke(validate)
    if valid or ctx.obj.get('dev', False):
        return click.echo("\nSuccessfully initialized project")
    raise click.UsageError("Failed to initialize project")


@cli.command()
@click.argument('config', nargs=-1, type=click.File('r'))
def edit(config):
    """
    Edit the packager configuration.
    """
    config = config[0] if config else open(default, 'r', encoding='utf-8')
    return show(config)


@cli.command()
@click.argument('config', nargs=-1, type=click.File('r'))
def validate(config):
    """
    Check if the packager configuration is valid.
    """
    builds = set(['cmake', 'qmake', 'make'])
    targets = set(['debian', 'rpm', 'pacman'])
    keys = set([
        'name',
        'version',
        'description',
        'build',
        'authors',
        'maintainers',
        'install',
        'prefix',
        'targets'
    ])
    config = config[0] if config else open(default, 'r', encoding='utf-8')
    data = yaml.safe_load(config)
    try:
        assert data.get('package').get('build').get('type') in builds,\
            "Unsupported build type <%s>"
        assert data.get('package').keys() and \
            len(set(data.get('package').keys()).difference(keys)) == 0, \
            "Missing required packager config key/values"
        assert data.get('package').get('targets') and \
            len(set(data.get('package').get('targets')).difference(targets)) == 0,\
            "Unsupported target specification"
    except AssertionError as err:
        raise click.BadParameter(err)
    ctx = click.get_current_context()
    if not (ctx.obj.get('init', False) or ctx.obj.get('build', False)):
        click.echo('\nConfig file at %s is valid' % config.name)
    return True, data


@cli.command()
@click.argument('config', nargs=-1, type=click.File('r'))
def build(config):
    """
    Build the package per config specifications.
    """
    click.echo()
    config = config[0] if config else open(default, 'r', encoding='utf-8')
    ctx = click.get_current_context()
    ctx.obj['build'] = True
    valid, data = ctx.forward(validate)
    if valid:
        for target in data.get('package', {}).get('targets', []):
            bundle = target_bundle(config.name, target)
            bundle.build()
        return
    raise click.UsageError('Config file at %s is invalid' % config.name)


@cli.command()
@click.argument('config', nargs=-1, type=click.File('r'))
def install(config):
    """
    TODO: Extend the installation instructions
    """
