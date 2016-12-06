import os

from conans import ConanFile, CMake

username = os.getenv('CONAN_USERNAME', 'jason2506')
channel = os.getenv('CONAN_CHANNEL', 'testing')


class TestMsgPackConan(ConanFile):

    name = 'test-msgpack'
    version = '0.1.0'

    requires = (
        'msgpack/any@{username}/{channel}'.format(
            username=username,
            channel=channel,
        ),
    )

    settings = ('os', 'compiler', 'build_type', 'arch')
    generators = ('cmake', 'txt', 'env')

    def build(self):
        extra_opts = []
        extra_opts.append('-DMSGPACK_VERSION="{}"'.format(
            self.options['msgpack'].version,
        ))

        cmake = CMake(self.settings)
        self.run('cmake "{src_dir}" {opts} {extra_opts}'.format(
            src_dir=self.conanfile_directory,
            opts=cmake.command_line,
            extra_opts=' '.join(extra_opts),
        ))
        self.run('cmake --build . {}'.format(cmake.build_config))

    def imports(self):
        self.copy('*.dll', dst='bin', src='bin')
        self.copy('*.dylib', dst='bin', src='lib')

    def test(self):
        self.run('cd bin && .{}example'.format(os.sep))
