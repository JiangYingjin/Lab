#include "protocol.h"
#include <cstdint>
#include <cstring>  // for memcpy

namespace ftp::protocol {

std::vector<char> Message::serialize() const {
    std::vector<char> data;
    // 序列化 command
    data.push_back(static_cast<char>(command));
    
    // 序列化 argument
    uint32_t argSize = argument.size();
    data.insert(data.end(), 
        reinterpret_cast<char*>(&argSize), 
        reinterpret_cast<char*>(&argSize) + sizeof(argSize));
    data.insert(data.end(), argument.begin(), argument.end());
    
    // 序列化 dataSize
    data.insert(data.end(), 
        reinterpret_cast<const char*>(&dataSize), 
        reinterpret_cast<const char*>(&dataSize) + sizeof(dataSize));
    
    return data;
}

Message Message::deserialize(const std::vector<char>& data) {
    Message msg;
    size_t pos = 0;
    
    // 反序列化 command
    msg.command = static_cast<Command>(data[pos++]);
    
    // 反序列化 argument
    uint32_t argSize;
    memcpy(&argSize, &data[pos], sizeof(argSize));
    pos += sizeof(argSize);
    
    msg.argument = std::string(data.begin() + pos, data.begin() + pos + argSize);
    pos += argSize;
    
    // 反序列化 dataSize
    memcpy(&msg.dataSize, &data[pos], sizeof(msg.dataSize));
    
    return msg;
}

} 