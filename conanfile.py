from conans import ConanFile, CMake
import os
import re

# parse the version from the rang.hpp file
def get_version():
    header_path = os.path.join(os.path.dirname(__file__), "include", "rang.hpp")
    if not os.path.isfile(header_path):
        return None
    with open(header_path, 'r') as myfile:
        data = myfile.read()
    version = []
    for x in ['MAJOR', 'MINOR', 'PATCH']:
        component = re.search("#define RANG_VERSION_%s\\s+([^\\s]+)" % x, data)
        if component:
            version.append(component.group(1))
    if len(version) > 0:
        return ".".join(version)
    return None

class RangConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    name = "rang"
    version = get_version()
    license = "The Unlicense"
    url = "https://github.com/agauniyal/rang"
    description = "A Minimal, Header only Modern c++ library for colors in your terminal"
    no_copy_source = True
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
    }

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        # the header is already installed via CMake along with the config files
        self.copy(pattern="LICENSE", dst="licenses", keep_path=False)

    def package_id(self):
        self.info.header_only()
