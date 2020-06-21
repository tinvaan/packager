
from os import makedirs
from deb_pkg_tools.package import build_package

from .package import PackageBundle


class Debian(PackageBundle):
    def build(self):
        """
        Ref: https://linuxconfig.org/easy-way-to-create-a-debian-package-and-local-package-repository
        """
        configdir = self.config.config_dir()
        makedirs(configdir + '/DEBIAN', exist_ok=True)
        with open(configdir + '/DEBIAN/control', 'w') as f:
            content = [
                'Package: %s\n' % self.config.name,
                'Version: %s\n' % self.config.version,
                'Section: Custom\n',
                'Priority: optional\n',
                'Architecture: all\n',
                'Essential: no\n',
                'Maintainer: %s\n' % self.config.maintainers,
                'Description: %s\n' % self.config.description
            ]
            f.writelines(content)
        return build_package(configdir)
