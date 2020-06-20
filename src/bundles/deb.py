
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
                'Package: %s' % self.config.name,
                'Verson: %s' % self.config.version,
                'Section: Custom',
                'Priority: optional',
                'Architecture: all',
                'Essential: no',
                'Maintainer: %s' % self.config.maintainers,
                'Description: %s' % self.config.description
            ]
            f.writelines(content)
        return build_package(configdir)
