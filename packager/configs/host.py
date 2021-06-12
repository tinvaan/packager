
import sys

from os.path import join
from subprocess import Popen, PIPE
from click.exceptions import ClickException


class Host:
    def __init__(self):
        self.platform = sys.platform


class Linux(Host):
    def __init__(self):
        super().__init__()

    @property
    def distro(self):
        assert self.platform == 'linux', "%s platform not supported" % self.platform
        with open(join('/etc/os-release'), 'r') as f:
            for info in f.readlines():
                name = info.split('NAME=')
                if len(name) == 2 and name[0] == '':
                    return str(name[1])
        raise ClickException('Distro information not found')

    def manager(self):
        assert self.platform == 'linux', "%s platform not supported" % self.platform
        if 'arch' in self.distro.lower():
            return Pacman()
        if set(['ubuntu', 'debian']).intersection(set(self.distro.lower())):
            return Debian()

    def get_owner(self, filename):
        raise NotImplementedError('Subclass responsibility')


class Pacman(Host):
    def __init__(self):
        super().__init__()
        self.cmd = 'pacman'

    def get_owner(self, filename):
        args = [self.cmd, '-Qo', filename.strip()]
        command = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.stdout.read(), command.stderr.read()
        if not stderr and command.poll() == 0:
            owner = stdout.decode('utf-8').split(' ')[-2].strip()
            version = stdout.decode('utf-8').split(' ')[-1].strip()
            return "%s (>=%s)" % (
                owner.replace('\n', ''), version.replace('\n', ''))
        raise ClickException(
            'Owner package for file "%s" not found' % filename.strip())


class Debian(Host):
    def __init__(self):
        super().__init__()
        self.cmd = 'dpkg'

    def get_owner(self, filename):
        args = [self.cmd, '-S', filename]
        command = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.stdout.read(), command.stderr.read()
        if command.poll() == 0:
            package = stdout.split(': ')[0]
            args = [self.cmd, '-s', package]
            command = Popen(args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = command.stdout.read(), command.stderr.read()
            if command.poll() == 0:
                for info in stdout.splitlines():
                    version = info.split('Version: ')[1] if len(info.split('Version: ')) == 2 else None
                    if version:
                        return "%s=%s" % (package, version)
        raise ClickException('Owner package for file "%s" not found' % filename)
