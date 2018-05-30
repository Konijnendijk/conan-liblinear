#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class LibLinearConan(ConanFile):
    name = "liblinear"
    version = "2.20"
    github_version = "220"
    description = "A Library for Large Linear Classification"
    url = "https://github.com/konijnendijk/conan-libname"
    homepage = "https://www.csie.ntu.edu.tw/~cjlin/liblinear/"

    # Indicates License type of the packaged library
    license = "BSD-3-Clause"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = {"os": ["Linux", "Windows"], 
                "arch": ["x86", "x86_64"], 
                "compiler": ["gcc", "Visual Studio"], 
                "build_type": ["Debug", "Release"]}
    options = {"shared": [True, False]}
    default_options = "shared=False"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "source_subfolder"

    def configure(self):
        if self.settings.os == 'Windows' and not self.options.shared:
            raise Exception("Building a static library is not supported on Windows")

    def source(self):
        source_url = "https://github.com/cjlin1/liblinear"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.github_version))
        extracted_dir = self.name + "-" + self.github_version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def system(self, command):
        retcode = os.system(command)
        if retcode != 0:
            raise Exception("Error while executing:\n\t %s" % command)

    def build(self):
        if self.settings.os != 'Windows':
            self.system("cd {0} && make {1}".format(self.source_subfolder, "lib" if self.options.shared else ""))
        else:
            self.system("cd {0} && nmake @Makefile.win lib".format(self.source_subfolder))
            
    def package(self):
        self.copy(pattern="COPYRIGHT", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="*.h", dst="include", src=self.source_subfolder)
        if self.options.shared:
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
