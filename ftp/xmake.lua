add_rules("mode.debug", "mode.release")

set_languages("c++20")

-- 设置构建目录为项目根目录
set_targetdir(".")

-- 客户端可执行文件
target("ftpc")
    set_kind("binary")
    add_files("src/ftpc.cpp", "src/client.cpp", "src/protocol.cpp")
    add_includedirs("include")

-- 服务器可执行文件
target("ftps")
    set_kind("binary")
    add_files("src/ftps.cpp", "src/server.cpp", "src/protocol.cpp")
    add_includedirs("include")
