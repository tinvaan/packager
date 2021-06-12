
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

    def inputs(self, lines):
        indices = (-1, -1)
        for index, line in enumerate(lines):
            if line.startswith("set(CMAKE_MAKEFILE_DEPENDS"):
                indices = (index, )
            if indices[0] != -1 and line.startswith(")"):
                indices = (indices[0], index)
                break

        begin, end = indices
        return [dep.replace('"', '')
                for dep in [line.strip() for line in lines[begin + 1:end - 1]]]

    def depends(self):
        results = set()
        host = Linux().manager()
        cmake_depend_file = join(self.build_dir, 'CMakeFiles/Makefile.cmake')
        if exists(cmake_depend_file) and isfile(cmake_depend_file):
            with open(cmake_depend_file, 'r') as f:
                lines = self.inputs([line.strip() for line in f.readlines()])
                for line in lines:
                    parts = [part.strip() for part in line.split('/')]
                    parts = [part.replace('"', '') for part in parts]
                    if not set(parts).intersection(self.artifacts):
                        results.add(host.get_owner(line))
        return ", ".join(list(results))

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
                        raise ClickException(
                            'Inconsistent CMAKE_INSTALL_PREFIX')
        return targets
