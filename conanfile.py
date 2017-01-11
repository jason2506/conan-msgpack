import os
import sys
from distutils.version import LooseVersion

from conans import ConanFile, CMake, tools


class MsgPackConan(ConanFile):

    name = 'msgpack'
    version = '0.1.0'
    url = 'https://github.com/jason2506/conan-msgpack'
    license = 'BSL-1.0'

    dev_requires = (
        'gtest/1.8.0@lasote/stable',
    )

    settings = ('os', 'compiler', 'build_type', 'arch')
    generators = ('cmake', 'txt', 'env')
    build_policy = 'always'
    options = {
        'version': [
            '2.1.0',
            '2.0.0',
            '1.4.2', '1.4.1', '1.4.0',
            '1.3.0',
            '1.2.0',
            '1.1.0',
            '1.0.1', '1.0.0',
            '0.5.9',
        ],
        'use_cxx11': [True, False],
        'use_32bit': [True, False],
        'use_boost': [True, False],
        'enable_cxx': [True, False],
        'enable_shared': [True, False],
    }
    default_options = (
        'version={last_version}'.format(last_version=options['version'][0]),
        'use_cxx11=False',
        'use_32bit=False',
        'use_boost=False',
        'enable_cxx=True',
        'enable_shared=True',
    )

    exports = (
        'CMakeLists.txt',
        'FindMsgPack.cmake',
    )

    def source(self):
        ext = 'zip' if sys.platform == 'win32' else 'tar.gz'
        filename = 'cpp-{ver}.{ext}'.format(ver=self.options.version, ext=ext)
        url = 'https://github.com/msgpack/msgpack-c/archive/{}'.format(
            filename,
        )

        self.output.info('Downloading {}...'.format(url))
        tools.download(url, filename)
        tools.unzip(filename, '.')
        os.unlink(filename)

    def build(self):
        extra_opts = []
        extra_opts.append('-DPACKAGE_VERSION="{}"'.format(
            self.options.version,
        ))
        extra_opts.append('-DCMAKE_INSTALL_PREFIX="{}"'.format(
            self.package_folder,
        ))

        extra_opts.append('-DMSGPACK_CXX11={}'.format(self.options.use_cxx11))
        extra_opts.append('-DMSGPACK_32BIT={}'.format(self.options.use_32bit))
        extra_opts.append('-DMSGPACK_BOOST={}'.format(self.options.use_boost))

        extra_opts.append('-DMSGPACK_BUILD_TESTS={}'.format(
            bool(self.scope.dev and self.scope.build_tests),
        ))
        extra_opts.append('-DMSGPACK_BUILD_EXAMPLES={}'.format(
            bool(self.scope.dev and self.scope.build_examples),
        ))

        extra_opts.append('-DMSGPACK_ENABLE_CXX={}'.format(
            self.options.enable_cxx,
        ))
        extra_opts.append('-DMSGPACK_ENABLE_SHARED={}'.format(
            self.options.enable_shared,
        ))

        cmake = CMake(self.settings)
        self.run('cmake "{src_dir}" {opts} {extra_opts}'.format(
            src_dir=self.conanfile_directory,
            opts=cmake.command_line,
            extra_opts=' '.join(extra_opts),
        ))
        self.run('cmake --build . {}'.format(cmake.build_config))

    def package(self):
        self.run('cmake --build . --target install')
        self.copy('FindMsgPack.cmake', '.', '.')

    def package_info(self):
        if LooseVersion(str(self.options.version)) < LooseVersion('1.4.0'):
            self.cpp_info.libs = ['msgpack']
        else:
            self.cpp_info.libs = ['msgpackc']
