
import re
import shutil
import unittest
import warnings

from os import listdir
from executor import ExternalCommandFailed
from os.path import join, basename, dirname

from packager.bundles.deb import Debian
from packager.configs.base import DebConfig


class TestDebian(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore')

    def test_build(self):
        with self.assertRaises(ExternalCommandFailed):
            config = DebConfig(join(dirname(__file__), './fixtures/example.yml'), {})
            package = Debian(config).build()

            config = DebConfig(join(dirname(__file__), './fixtures/example.yml'), {
                'version': '1.0.0',
                'description': 'This package has no name',
                'build': 'cmake',
                'authors': ['Harish Navnit <harishnavnit@gmail.com>']
            })
            Debian(config).build()

        config = DebConfig(join(dirname(__file__), './fixtures/exampleyml'), {
            'name': 'complete',
            'version': '1.0.0',
            'description': 'An example packager config for a debian package',
            'build': 'cmake',
            'authors': ['Harish Navnit <harishnavnit@gmail.com>']
        })
        package = Debian(config).build()
        self.assertEqual(basename(package), 'complete_1.0.0_all.deb')

        config = DebConfig(join(dirname(__file__), './fixtures/example.yml'), {
            'name': 'incomplete',
            'version': '1.0.0',
            'description': 'An example packager config for a debian package',
            'build': 'cmake'
        })
        package = Debian(config).build()
        self.assertEqual(basename(package), 'incomplete_1.0.0_all.deb')

    def tearDown(self):
        for dir in listdir('/tmp'):
            if re.search('deb-pkg-tools', dir):
                shutil.rmtree('/tmp/' + dir)
