# 文件：Examples/_ch13_conanfile.py
# 行号：1
from conan import ConanFile

class MyApp(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    requires = (
        "fmt/10.1.1",
        "ms-gsl/0.40.0",
    )

    def layout(self):
        self.folders.source = "."
        self.folders.build = "build"
        self.folders.generators = "build"
