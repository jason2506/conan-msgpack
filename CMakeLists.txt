cmake_minimum_required(VERSION 3.1)

project(conan-msgpack VERSION 0.1.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

option(PACKAGE_VERSION "original package version" "2.1.0")
add_subdirectory("./msgpack-c-cpp-${PACKAGE_VERSION}")
