#include "client.h"
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <fstream>
#include <filesystem>

using namespace ftp::client;
using namespace ftp::protocol;

Client::Client(const std::string &serverIP, uint16_t port)
{
    // 创建 socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket < 0)
    {
        throw std::runtime_error("Socket creation failed");
    }

    // 设置服务器地址
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    if (inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr) <= 0)
    {
        throw std::runtime_error("Invalid address");
    }
}

Client::~Client()
{
    if (clientSocket >= 0)
    {
        close(clientSocket);
    }
}

bool Client::connect()
{
    if (::connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
    {
        return false;
    }
    return true;
}

void Client::sendMessage(const Message &msg)
{
    std::vector<char> data = msg.serialize();
    uint32_t size = data.size();

    // 发送消息大小
    send(clientSocket, &size, sizeof(size), 0);
    // 发送消息内容
    send(clientSocket, data.data(), data.size(), 0);
}

Message Client::receiveResponse()
{
    // 接收消息大小
    uint32_t msgSize;
    if (recv(clientSocket, &msgSize, sizeof(msgSize), 0) <= 0)
    {
        throw std::runtime_error("Failed to receive message size");
    }

    // 接收消息内容
    std::vector<char> buffer(msgSize);
    if (recv(clientSocket, buffer.data(), msgSize, 0) <= 0)
    {
        throw std::runtime_error("Failed to receive message content");
    }

    return Message::deserialize(buffer);
}

std::vector<std::string> Client::listFiles()
{
    Message msg{Command::LIST, "", 0};
    sendMessage(msg);

    Message response = receiveResponse();
    std::vector<std::string> files;

    // 解析文件列表
    std::string fileList = response.argument;
    size_t pos = 0;
    while ((pos = fileList.find('\n')) != std::string::npos)
    {
        std::string file = fileList.substr(0, pos);
        if (!file.empty())
        {
            files.push_back(file);
        }
        fileList.erase(0, pos + 1);
    }
    if (!fileList.empty())
    {
        files.push_back(fileList);
    }

    return files;
}

bool Client::changeDirectory(const std::string &path)
{
    Message msg{Command::CD, path, 0};
    sendMessage(msg);

    try
    {
        Message response = receiveResponse();
        return response.command == Command::CD;
    }
    catch (const std::exception &)
    {
        return false;
    }
}

bool Client::downloadFile(const std::string &filename)
{
    Message msg{Command::DOWNLOAD, filename, 0};
    sendMessage(msg);

    try
    {
        // 接收文件大小信息
        Message response = receiveResponse();
        if (response.command != Command::DOWNLOAD)
        {
            return false;
        }

        // 创建本地文件
        std::ofstream file(filename, std::ios::binary);
        if (!file)
        {
            return false;
        }

        // 接收文件内容
        size_t remainingBytes = response.dataSize;
        std::vector<char> buffer(8192); // 8KB 缓冲区

        while (remainingBytes > 0)
        {
            size_t bytesToRead = std::min(remainingBytes, buffer.size());
            ssize_t bytesRead = recv(clientSocket, buffer.data(), bytesToRead, 0);

            if (bytesRead <= 0)
            {
                return false;
            }

            file.write(buffer.data(), bytesRead);
            remainingBytes -= bytesRead;
        }

        return true;
    }
    catch (const std::exception &)
    {
        return false;
    }
}

bool Client::uploadFile(const std::string &filename)
{
    // 尝试多种可能的路径
    std::filesystem::path filePath;
    std::ifstream file;

    // 1. 首先尝试直接打开（处理绝对路径和当前目录的相对路径）
    file.open(filename, std::ios::binary);
    if (file)
    {
        filePath = filename;
    }
    else
    {
        // 2. 尝试从当前工作目录打开
        filePath = std::filesystem::current_path() / filename;
        file.open(filePath, std::ios::binary);
    }

    if (!file)
    {
        std::cerr << "Error: Cannot open file '" << filename << "'\n"
                  << "Tried paths:\n"
                  << "  " << filename << "\n"
                  << "  " << (std::filesystem::current_path() / filename).string() << "\n";
        return false;
    }

    // 获取文件大小
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    // 只发送文件名（不包含路径）
    std::string baseFilename = std::filesystem::path(filename).filename().string();

    // 发送上传请求
    Message msg{Command::UPLOAD, baseFilename, fileSize};
    sendMessage(msg);

    try
    {
        // 发送文件内容
        std::vector<char> buffer(8192); // 8KB 缓冲区
        while (!file.eof())
        {
            file.read(buffer.data(), buffer.size());
            std::streamsize bytesRead = file.gcount();
            if (bytesRead > 0)
            {
                send(clientSocket, buffer.data(), bytesRead, 0);
            }
        }

        // 接收上传确认
        Message response = receiveResponse();
        if (response.command != Command::UPLOAD)
        {
            std::cerr << "Error: " << response.argument << '\n';
            return false;
        }
        return true;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error during upload: " << e.what() << '\n';
        return false;
    }
}

bool Client::createDirectory(const std::string &dirname)
{
    Message msg{Command::MKDIR, dirname, 0};
    sendMessage(msg);

    try
    {
        Message response = receiveResponse();
        return response.command == Command::MKDIR;
    }
    catch (const std::exception &)
    {
        return false;
    }
}

bool Client::removeDirectory(const std::string &dirname)
{
    Message msg{Command::RMDIR, dirname, 0};
    sendMessage(msg);

    try
    {
        Message response = receiveResponse();
        return response.command == Command::RMDIR;
    }
    catch (const std::exception &)
    {
        return false;
    }
}

bool Client::deleteFile(const std::string &filename)
{
    Message msg{Command::DELETE, filename, 0};
    sendMessage(msg);

    try
    {
        Message response = receiveResponse();
        return response.command == Command::DELETE;
    }
    catch (const std::exception &)
    {
        return false;
    }
}