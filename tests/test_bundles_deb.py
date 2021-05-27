
import os
import re
import shutil
import tempfile
import unittest

from pathlib import Path
from executor import ExternalCommandFailed
from os.path import join, exists, dirname, basename

from packager.bundles.deb import Debian
from packager.configs.base import DebConfig


class TestDebian(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = join(dirname(__file__), './fixtures/example.yml')
        cls.bundle = Debian(DebConfig(cls.spec))

    def setUp(self):
        self.debdir = tempfile.mkdtemp()
        os.makedirs(self.debdir + '/DEBIAN', exist_ok=True)
        for item in self.bundle.config.install:
            source = item.get('source')
            if source != dirname(source):
                os.makedirs(dirname(source), exist_ok=True)
            Path(source).touch()

    def test_control(self):
        self.bundle.control(self.debdir)
        self.assertTrue(exists(self.debdir + '/DEBIAN/control'))

    def test_layout(self):
        self.bundle.layout(self.debdir)

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

        config = DebConfig(join(dirname(__file__), './fixtures/example.yml'), {
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
        for dir in os.listdir('/tmp'):
            if re.search('deb-pkg-tools', dir):
                shutil.rmtree('/tmp/' + dir)
