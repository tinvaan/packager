
import os
import sys
import subprocess

from click.exceptions import UsageError, ClickException

from .configs import PackagerConfig
from .configs.builds import BuildConfig
from .configs.builds.cmake import CMake


def show(configfile):
    if sys.platform == 'win32':
        return os.startfile(configfile)
    return subprocess.call([os.environ.get('EDITOR', 'xdg-open'), configfile])


def build_config(configfile):
    data = BuildConfig.load(configfile)
    if data.get('build', {}).geT('type').lower() == 'cmake':
        return CMake(configfile)
    raise UsageError('Build type not supported')


def target_bundle(config, target):
    if target.lower() in set(['deb', 'debian']):
        from .bundles.deb import Debian
        return Debian(PackagerConfig(configfile=config, configtype='DEB'))

    raise ClickException('Target type not supported')
