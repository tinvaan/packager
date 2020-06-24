
import re
import yaml
import shutil
import unittest
import warnings

from os import listdir
from os.path import exists, isfile
from click.testing import CliRunner

from packager.cli import init, validate, build


class TestCli(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore')

    def test_init(self):
        command = CliRunner().invoke(init)
        self.assertEqual(0, command.exit_code)
        self.assertTrue(exists('./.packager'))
        self.assertTrue(isfile('./.packager/config.yml'))

    def test_force_init(self):
        CliRunner().invoke(init)
        with open('./.packager/config.yml', 'w') as f:
            yaml.dump({'packager': {'foo': 'bar'}}, f) 
        command = CliRunner().invoke(init, ['--force'])
        self.assertEqual(0, command.exit_code)
        self.assertTrue(exists('./.packager'))
        self.assertTrue(isfile('./.packager/config.yml'))
        with open('./.packager/config.yml', 'r') as f:
            self.assertNotEqual(yaml.safe_load(f), {'packager': {'foo': 'bar'}})

    def test_validate(self):
        command = CliRunner().invoke(validate, ['./fixtures/example.yml'])
        self.assertNotEqual(0, command.exit_code)
        command = CliRunner().invoke(validate, ['./tests/fixtures/invalid.yml'])
        self.assertNotEqual(0, command.exit_code)
        command = CliRunner().invoke(validate, ['./tests/fixtures/example.yml'])
        self.assertEqual(0, command.exit_code)
        self.assertEqual(
            '\nConfig file at ./tests/fixtures/example.yml is valid\n', command.output)

    @unittest.skip('TODO')
    def test_build(self):
        command = CliRunner().invoke(build, ['./fixtures/example.yml'])
        self.assertNotEqual(0, command.exit_code)
        command = CliRunner().invoke(build, ['./tests/fixtures/invalid.yml'])
        self.assertNotEqual(0, command.exit_code)
        command = CliRunner().invoke(build, ['./tests/fixtures/example.yml'])
        self.assertEqual(0, command.exit_code)

    def tearDown(self):
        shutil.rmtree('./.packager', ignore_errors=True)
        for dir in listdir('/tmp'):
            if re.search('deb-pkg-tools', dir):
                shutil.rmtree('/tmp/' + dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
