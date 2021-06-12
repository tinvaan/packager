# https://en.wikipedia.org/wiki/Package_format


import yaml

from os.path import dirname


class PackagerConfig:
    def __init__(self, configfile, data=None, configtype='BASE'):
        self.configtype = "BASE"
        self.configfile = configfile
        self.data = data if data else self.load(configfile).get('package')

    def __repr__(self):
        return "%s package config - %s : %s (%s)" % (
            self.configtype, self.name, self.version, self.configfile)

    @staticmethod
    def load(configfile):
        with open(configfile, 'r') as f:
            return yaml.safe_load(f)

    def update(self, configfile=None):
        self.data = self.load(configfile)

    def config_dir(self):
        return dirname(self.configfile)

    def validate(self, configfile):
        raise NotImplementedError()

    @property
    def package(self):
        return self.data

    @property
    def package_type(self):
        return self.configtype

    @property
    def name(self):
        return self.data.get('name', "")

    @property
    def authors(self):
        return self.data.get('authors', [])

    @property
    def maintainers(self):
        if not self.data.get('maintainers'):
            return self.data.get('authors', [])
        return self.data.get('maintainers', [])

    @property
    def version(self):
        return self.data.get('version', 0.0)

    @property
    def description(self):
        return self.data.get('description', "")

    @property
    def install(self):
        return self.data.get('install', [])

    @property
    def install_prefix(self):
        return self.data.get('install_prefix', '/usr/local')

    @property
    def build_arch(self):
        return self.data.get('architecture', "")

    @property
    def build_dir(self):
        return self.data.get('build', {}).get('dir')

    @property
    def build_type(self):
        return self.data.get('build', {}).get('type')

    @property
    def target_formats(self):
        return self.data.get('targets', [])

    @property
    def keep_bundles(self):
        return self.data.get('keep_bundles', True)

    @property
    def upstream_repo(self):
        upstream = self.data.get('upstream')
        if upstream:
            return upstream.get('repo', "")

    @property
    def issue_tracker(self):
        upstream = self.data.get('upstream')
        if upstream:
            return upstream.get('issues')

    @property
    def contact_irc(self):
        contact = self.data.get('contact')
        if contact:
            return contact.get('irc')

    @property
    def contact_email(self):
        contact = self.data.get('contact')
        if contact:
            return contact.get('email')
