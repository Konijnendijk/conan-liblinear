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
    settings = "os", "arch", "compiler", "build_type"

    options = {"fPIC": [True, False]}
    default_options = "fPIC=True",

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

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

    def linux_build(self):

        if self.settings.compiler == "gcc":
            cc = "gcc"
            cxx = "g++"
        elif self.settings.compiler == "clang":
            cc = "clang"
            cxx = "clang++"
        else:
            raise Exception("Compiler not supported")

        cflags = ["-Wall", "-Wconversion"]
            
        if self.settings.build_type == "Debug":
            cflags.append("-g")
        else:
            cflags.append("-O3")
        
        if self.options.fPIC:
            cflags.append("-fPIC")

        self.system("cd {0} && make CFLAGS='{1}' CC={2} CXX={3} lib".format(self.source_subfolder, " ".join(cflags), cc, cxx))

    def windows_build(self):
        cflags = ["/nologo", "/EHsc", "/I.", "/D _CRT_SECURE_NO_DEPRECATE"]
        cflags.append("/{0}".format(self.settings.compiler.runtime))
        if self.settings.build_type == "Debug":
            cflags.append("/DEBUG")
        else:
            cflags.append("/O2")
        self.system('cd {0} && nmake /F Makefile.win CFLAGS="{1}" lib'.format(self.source_subfolder, " ".join(cflags)))

    def build(self):
        if self.settings.os == "Linux":
            self.linux_build()
        elif self.settings.compiler == "Visual Studio":
            self.windows_build()
        else:
            raise Exception("OS or compiler not supported")
            
    def package(self):
        self.copy(pattern="COPYRIGHT", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="*.h", dst="include", src=self.source_subfolder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
