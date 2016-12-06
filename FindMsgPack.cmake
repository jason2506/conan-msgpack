find_path(MsgPack_INCLUDE_DIR NAMES msgpack.h PATHS ${CONAN_INCLUDE_DIRS_MSGPACK})
find_library(MsgPack_LIBRARY NAMES ${CONAN_LIBS_MSGPACK} PATHS ${CONAN_LIB_DIRS_MSGPACK})

set(MsgPack_FOUND TRUE)
set(MsgPack_INCLUDE_DIRS ${MsgPack_INCLUDE_DIR})
set(MsgPack_LIBRARIES ${MsgPack_LIBRARY})

if(NOT TARGET MsgPack::MsgPack)
    add_library(MsgPack::MsgPack UNKNOWN IMPORTED)
    set_target_properties(MsgPack::MsgPack
        PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${MagPack_INCLUDE_DIRS}"
            IMPORTED_LOCATION "${MsgPack_LIBRARY}")
endif()

mark_as_advanced(
    MsgPack_LIBRARY
    MsgPack_INCLUDE_DIR
)
