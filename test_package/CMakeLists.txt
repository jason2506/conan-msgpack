cmake_minimum_required(VERSION 3.1)

project(MsgPack VERSION 0.1.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
set(CMAKE_SKIP_RPATH OFF)

option(MSGPACK_VERSION "msgpack version" "2.0.0")
find_package(msgpack ${MSGPACK_VERSION} REQUIRED)

if(${MSGPACK_VERSION} VERSION_LESS "1.0.0")
    add_definitions(-DVERSION_LT_1_0_0)
endif()

if(${MSGPACK_VERSION} VERSION_LESS "1.2.0")
    add_definitions(-DVERSION_LT_1_2_0)
endif()

add_executable(example example.cpp)
target_link_libraries(example MsgPack::MsgPack)
