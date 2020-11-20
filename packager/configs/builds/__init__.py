
from .. import PackagerConfig


class BuildConfig(PackagerConfig):
    def __init__(self, configfile, data=None):
        super().__init__(configfile, data)

    def __repr__(self):
        return "<%s> build config" % self.build_type

    def depends(self):
        raise NotImplementedError("Subclass responsibility")

    def installables(self):
        raise NotImplementedError("Subclass responsibility")
