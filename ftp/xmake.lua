add_rules("mode.debug", "mode.release")

set_languages("c++20")

target("protocol")
set_kind("static")
add_files("src/protocol.cpp")
add_includedirs("include")

target("client")
set_kind("static")
add_files("src/client.cpp")
add_includedirs("include")
add_deps("protocol")

target("server")
set_kind("static")
add_files("src/server.cpp")
add_includedirs("include")
add_deps("protocol")

target("ftpc")
set_kind("binary")
add_files("src/ftpc.cpp")
add_includedirs("include")
add_deps("client", "protocol")

target("ftps")
set_kind("binary")
add_files("src/ftps.cpp")
add_includedirs("include")
add_deps("server", "protocol")
