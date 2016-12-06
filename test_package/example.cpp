#include <iostream>
#include <sstream>
#include <string>

#include <msgpack.hpp>

int main(void) {
    msgpack::type::tuple<int, bool, std::string> src(1, true, "example");

    // serialize the object into the buffer.
    // any classes that implements write(const char*,size_t) can be a buffer.
    std::stringstream buffer;
    msgpack::pack(buffer, src);

    // send the buffer ...
    buffer.seekg(0);

    // deserialize the buffer into msgpack::object instance.
    std::string str(buffer.str());

#if !defined(VERSION_LT_1_2_0)
    msgpack::object_handle oh =
        msgpack::unpack(str.data(), str.size());

    // deserialized object is valid during the msgpack::object_handle instance is alive.
    msgpack::object deserialized = oh.get();
#elif !defined(VERSION_LT_1_0_0)
    msgpack::unpacked result;
    msgpack::unpack(result, str.data(), str.size());

    // deserialized object is valid during the msgpack::unpacked instance alive.
    msgpack::object deserialized = result.get();
#else
    // deserialized object is valid during the msgpack::zone instance alive.
    msgpack::zone mempool;

    msgpack::object deserialized;
    msgpack::unpack(str.data(), str.size(), NULL, &mempool, &deserialized);
#endif

    // msgpack::object supports ostream.
    std::cout << deserialized << std::endl;

    // convert msgpack::object instance into the original type.
    // if the type is mismatched, it throws msgpack::type_error exception.
    msgpack::type::tuple<int, bool, std::string> dst;
#if !defined(VERSION_LT_1_2_0)
    deserialized.convert(dst);
#else
    deserialized.convert(&dst);
#endif

    return 0;
}
