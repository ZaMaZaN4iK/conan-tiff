import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class LibtiffConan(ConanFile):
    name = "libtiff"
    version = "4.0.6"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "zlib/1.2.8@lasote/stable"
    exports = ["CMakeLists.txt", "FindTIFF.cmake"]
    url="http://github.com/bilke/conan-tiff"
    license="http://www.remotesensing.org/libtiff/"

    ZIP_FOLDER_NAME = "tiff-%s" % version
    INSTALL_DIR = "_install"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://opengeosys.s3.amazonaws.com/ogs6-lib-sources/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        CMAKE_OPTIONALS = "-Dlzma=OFF -Djpeg=OFF "
        if self.settings.os == "Linux":
            CMAKE_OPTIONALS += "-DCMAKE_POSITION_INDEPENDENT_CODE=ON "
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=OFF "
        else:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=ON "
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s" % (cd_build, self.INSTALL_DIR, cmake.command_line, CMAKE_OPTIONALS))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindTIFF.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["tiffd", "tiffxxd"]
        else:
            self.cpp_info.libs = ["tiff", "tiffxx"]
