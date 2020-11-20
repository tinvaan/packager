
class PackageBundle:
    def __init__(self, config):
        self.config = config

    def show(self, revision="HEAD"):
        pass

    def fetch(self, revision="HEAD"):
        pass

    def push(self, registry=None):
        pass

    def publish(self):
        raise NotImplementedError()

    def update(self):
        pass

    def log(self):
        pass

    def build(self):
        raise NotImplementedError()

    def install(self):
        pass
