
from pathlib import Path
from os import makedirs
from shutil import copyfile
from os.path import join, dirname
from deb_pkg_tools.package import build_package

from . import PackageBundle
from ..utils import build_config


class Debian(PackageBundle):
    def __init__(self, config):
        super().__init__(config)
        self.pkgtype = 'deb'

    def build(self):
        """
        Ref: https://linuxconfig.org/easy-way-to-create-a-debian-package-and-local-package-repository
        """
        configdir = join(self.config.config_dir(), self.pkgtype)
        makedirs(configdir + '/DEBIAN', exist_ok=True)
        self.control(configdir)
        self.layout(configdir)
        return build_package(configdir)

    def control(self, debdir):
        with open(debdir + '/DEBIAN/control', 'w') as f:
            content = [
                'Package: %s\n' % self.config.name,
                'Version: %s\n' % self.config.version,
                'Section: Custom\n',
                'Priority: optional\n',
                'Architecture: all\n',
                'Essential: no\n',
                'Maintainer: %s\n' % self.config.maintainers,
                'Description: %s\n' % self.config.description,
                'Depends: %s\n' % build_config(self.config.configfile).depends()
            ]
            f.writelines(content)

    def layout(self, debdir):
        for item in self.config.install:
            source = item.get('source', '.')
            dest = Path(
                debdir + '/' + self.config.prefix +
                '/' + item.get('path', '.')).resolve()
            if dirname(dest) != dest:
                makedirs(dirname(dest), exist_ok=True)
            copyfile(source, dest)
