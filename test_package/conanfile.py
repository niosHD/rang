from conans import ConanFile, Meson
import os

class RangConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = "pkg_config"
    exports_sources = "*"

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()

    def imports(self):
        self.copy("*.hpp")

    def test(self):
        self.run(".%svisualTest" % os.sep)
