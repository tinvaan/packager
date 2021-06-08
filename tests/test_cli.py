
import os
import re
import yaml
import shutil
import unittest

from click.testing import CliRunner
from os.path import join, exists, isfile, dirname

from packager import cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.ctx = self.runner.make_env()
        self.ctx.update({'dev': True})
        self.config = join(os.getcwd(), '.packager/config.yml')
        os.makedirs(join(os.getcwd(), '.packager'), exist_ok=True)
        with open(self.config, 'w') as f:
            example = join(dirname(__file__), './fixtures/example.yml')
            data = yaml.safe_load(open(example, 'r', encoding='utf-8'))
            yaml.safe_dump(data, f)

    def test_init(self):
        cmd = self.runner.invoke(
            cli.init, obj=self.ctx, catch_exceptions=False)
        self.assertEqual(0, cmd.exit_code)
        self.assertTrue(exists('./.packager'))
        self.assertTrue(isfile('./.packager/config.yml'))

    def test_force_init(self):
        self.runner.invoke(cli.init, obj=self.ctx, catch_exceptions=False)
        with open('./.packager/config.yml', 'w') as f:
            yaml.dump({'packager': {'foo': 'bar'}}, f)

        args = ['--force']
        cmd = self.runner.invoke(
            cli.init, args, obj=self.ctx, catch_exceptions=False)
        self.assertEqual(0, cmd.exit_code)
        self.assertTrue(exists('./.packager'))
        self.assertTrue(isfile('./.packager/config.yml'))
        with open('./.packager/config.yml', 'r') as f:
            self.assertNotEqual(
                yaml.safe_load(f), {'packager': {'foo': 'bar'}})

    def test_validate(self):
        args = ['./fixtures/example.yml']
        cmd = self.runner.invoke(cli.validate, args, catch_exceptions=False)
        self.assertNotEqual(0, cmd.exit_code)

        args = ['./tests/fixtures/invalid.yml']
        cmd = self.runner.invoke(cli.validate, args, catch_exceptions=False)
        self.assertNotEqual(0, cmd.exit_code)

        args = []
        cmd = self.runner.invoke(
            cli.validate, args, obj=self.ctx, catch_exceptions=False)
        self.assertEqual(0, cmd.exit_code)

        args = ['./tests/fixtures/example.yml']
        cmd = self.runner.invoke(
            cli.validate, args, obj=self.ctx, catch_exceptions=False)
        self.assertEqual(0, cmd.exit_code)
        self.assertEqual(
            cmd.output,
            '\nConfig file at ./tests/fixtures/example.yml is valid\n')

    def test_build(self):
        args = ['./fixtures/example.yml']
        cmd = self.runner.invoke(
            cli.build, args, obj=self.ctx, catch_exceptions=False)
        self.assertNotEqual(0, cmd.exit_code)

        args = ['./tests/fixtures/invalid.yml']
        cmd = self.runner.invoke(
            cli.build, args, obj=self.ctx, catch_exceptions=False)
        self.assertNotEqual(0, cmd.exit_code)

        args = ['./tests/fixtures/example.yml']
        cmd = self.runner.invoke(
            cli.build, args, obj=self.ctx, catch_exceptions=False)
        self.assertEqual(0, cmd.exit_code)

    def tearDown(self):
        shutil.rmtree('./.packager', ignore_errors=True)
        for dir in os.listdir('/tmp'):
            if re.search('deb-pkg-tools', dir):
                shutil.rmtree('/tmp/' + dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
