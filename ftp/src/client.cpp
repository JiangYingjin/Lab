#include "client.h"
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <fstream>
#include <filesystem>
#include <chrono>
#include <iomanip>

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
        if (response.command == Command::CD)
        {
            // 如果是 pwd 命令，打印当前路径
            if (path == ".")
            {
                std::cout << response.argument << std::endl;
            }
            return true;
        }
        return false;
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
        // 接收服务器响应
        Message response = receiveResponse();

        // 检查是否是错误响应
        if (response.argument.substr(0, 7) == "Error: ")
        {
            printError(response.argument.substr(7)); // 去掉 "Error: " 前缀
            return false;
        }

        // 检查是否是正确的下载响应
        if (response.command != Command::DOWNLOAD)
        {
            printError("Unexpected server response");
            return false;
        }

        // 创建本地文件
        std::ofstream file(filename, std::ios::binary);
        if (!file)
        {
            printError("Cannot create local file: " + filename);
            return false;
        }

        // 接收文件内容
        size_t totalBytes = response.dataSize;
        size_t receivedBytes = 0;
        std::vector<char> buffer(8192); // 8KB 缓冲区

        while (receivedBytes < totalBytes)
        {
            size_t bytesToRead = std::min(totalBytes - receivedBytes, buffer.size());
            ssize_t bytesRead = recv(clientSocket, buffer.data(), bytesToRead, 0);

            if (bytesRead <= 0)
            {
                file.close();
                std::filesystem::remove(filename); // 删除不完整的文件
                printError("Connection lost while downloading");
                return false;
            }

            file.write(buffer.data(), bytesRead);
            receivedBytes += bytesRead;

            // 显示进度
            printProgress("Downloading " + filename, receivedBytes, totalBytes);
        }

        std::cout << std::endl; // 进度条完成后换行
        return true;
    }
    catch (const std::exception &e)
    {
        printError(e.what());
        if (std::filesystem::exists(filename))
        {
            std::filesystem::remove(filename);
        }
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
    size_t totalBytes = file.tellg();
    file.seekg(0, std::ios::beg);

    // 只发送文件名（不包含路径）
    std::string baseFilename = std::filesystem::path(filename).filename().string();

    // 发送上传请求
    Message msg{Command::UPLOAD, baseFilename, totalBytes};
    sendMessage(msg);

    try
    {
        // 发送文件内容
        size_t sentBytes = 0;
        std::vector<char> buffer(8192); // 8KB 缓冲区
        while (!file.eof() && sentBytes < totalBytes)
        {
            file.read(buffer.data(), buffer.size());
            std::streamsize bytesRead = file.gcount();
            if (bytesRead > 0)
            {
                ssize_t bytesSent = send(clientSocket, buffer.data(), bytesRead, 0);
                if (bytesSent > 0)
                {
                    sentBytes += bytesSent;
                    // 显示进度
                    printProgress("Uploading " + baseFilename, sentBytes, totalBytes);
                }
            }
        }

        std::cout << std::endl; // 进度条完成后换行

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

        // 检查是否是错误响应
        if (response.argument.substr(0, 7) == "Error: ")
        {
            printError(response.argument.substr(7)); // 去掉 "Error: " 前缀
            return false;
        }

        if (response.command != Command::DELETE)
        {
            printError("Unexpected server response");
            return false;
        }

        return true;
    }
    catch (const std::exception &e)
    {
        printError(e.what());
        return false;
    }
}

void Client::printProgress(const std::string &operation, size_t current, size_t total)
{
    const int width = 40;
    float percentage = (float)current / total;
    int pos = width * percentage;

    // 计算传输速度（需要添加时间跟踪）
    static auto lastTime = std::chrono::steady_clock::now();
    static size_t lastBytes = 0;
    auto now = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(now - lastTime);

    double speed = 0;
    if (duration.count() > 0)
    {
        speed = (current - lastBytes) * 1000.0 / duration.count(); // bytes per second
    }

    if (duration.count() >= 100) // 每100ms更新一次速度
    {
        lastTime = now;
        lastBytes = current;
    }

    // 计算预估剩余时间
    int eta = 0;
    if (speed > 0)
    {
        eta = (total - current) / speed;
    }

    // 清除当前行
    std::cout << "\r\033[K";

    // 显示操作和进度条
    std::cout << operation << ": [";
    for (int i = 0; i < width; ++i)
    {
        if (i < pos)
            std::cout << "=";
        else if (i == pos)
            std::cout << ">";
        else
            std::cout << " ";
    }
    std::cout << "] ";

    // 显示百分比和大小信息
    std::cout << int(percentage * 100.0) << "% ";
    std::cout << formatSize(current) << "/" << formatSize(total);

    // 显示传输速度
    if (speed > 0)
    {
        std::cout << " @ " << formatSize((size_t)speed) << "/s";
    }

    // 显示预估剩余时间
    if (eta > 0)
    {
        std::cout << " ETA: ";
        if (eta >= 3600)
        {
            std::cout << eta / 3600 << "h ";
            eta %= 3600;
        }
        if (eta >= 60)
        {
            std::cout << eta / 60 << "m ";
            eta %= 60;
        }
        std::cout << eta << "s";
    }

    std::cout << std::flush;
}

// 同���也需要添加 formatSize 函数
std::string Client::formatSize(size_t bytes)
{
    const char *units[] = {"B", "KB", "MB", "GB"};
    int unit = 0;
    double size = bytes;

    while (size >= 1024 && unit < 3)
    {
        size /= 1024;
        unit++;
    }

    char buffer[32];
    snprintf(buffer, sizeof(buffer), "%.1f %s", size, units[unit]);
    return buffer;
}

void Client::printError(const std::string &msg)
{
    std::cerr << "Error: " << msg << std::endl;
}