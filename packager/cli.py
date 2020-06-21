
import click

from configs.base import *
from bundles.deb import Debian


@click.group
def packager():
    pass


@packager.command()
@packager.option('--config')
def build(config):
    package = Debian(DebConfig(config))
    package.build()


if __name__ == '__main__':
    packager()