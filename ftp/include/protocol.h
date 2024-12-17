#pragma once
#include <string>
#include <vector>
#include <cstring>

namespace ftp {
namespace protocol {

// FTP 命令枚举
enum class Command
{
    LIST,     // 列出文件/目录
    CD,       // 改变工作目录
    DOWNLOAD, // 下载文件
    UPLOAD,   // 上传文件
    MKDIR,    // 创建目录
    RMDIR,    // 删除目录
    DELETE,   // 删除文件
    PWD,      // 显示当前工作目录
    QUIT      // 退出
};

// 定义协议消息格式
class Message
{
public:
    Command command;
    std::string argument;
    size_t dataSize;

    std::vector<char> serialize() const;
    static Message deserialize(const std::vector<char>& data);
};

} // namespace protocol
} // namespace ftp 