
from os.path import join, exists, isfile
from click.exceptions import ClickException

from ..host import Linux
from . import BuildConfig


class CMake(BuildConfig):
    def __init__(self, configfile, data=None):
        super().__init__(configfile, data)
        self.configtype = 'CMAKE'
        self.artifacts = [
            'CMakeFiles',
            'CMakeLists.txt',
            'CMakeCache.txt',
            'CTestConfig.cmake'
        ]

    def depends(self):
        results = set()
        host = Linux().manager()
        cmake_depend_file = join(self.build_dir, 'CMakeFiles/Makefile.cmake')
        if exists(cmake_depend_file) and isfile(cmake_depend_file):
            with open(cmake_depend_file, 'r') as f:
                for index, line in enumerate(f.readlines()):
                    if line == 'set(CMAKE_MAKEFILE_DEPENDS':
                        while ')' not in line:
                            names = set(line.split('/'))
                            if len(set(names).intersection(self.artifacts)) == 0:
                                results.add(host.get_owner(line))
        return list(results)

    def installables(self):
        targets = []
        manifest = join(self.build_dir, 'install_manifest.txt')
        if exists(manifest) and isfile(manifest):
            with open(manifest, 'r') as f:
                for target in f.readlines():
                    try:
                        targets.append({
                            'source': target,
                            'path': target.split(self.install_prefix)[1]
                        })
                    except IndexError:
                        raise ClickException('Inconsistent CMAKE_INSTALL_PREFIX found')
        return targets
