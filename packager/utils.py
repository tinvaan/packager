
import os
import sys
import subprocess

from .configs.base import *
from .bundles.deb import Debian


def show(configfile):
    if sys.platform == 'win32':
        return os.startfile(configfile)
    return subprocess.call([os.environ.get('EDITOR', 'xdg-open'), configfile])


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
