cmake_minimum_required(VERSION 3.1)

option(PACKAGE_VERSION "original package version" "2.0.0")
project(msgpack VERSION ${PACKAGE_VERSION})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory("./msgpack-c-cpp-${PACKAGE_VERSION}")
