#include "server.h"
#include <filesystem>
#include <iostream>
#include <unistd.h>
#include <cstring>
#include <fstream>

using namespace ftp::server;
using namespace ftp::protocol;

Server::Server(uint16_t port)
{
    // 创建并确保根目录存在
    rootDir = "/tmp/ftp";
    if (!std::filesystem::exists(rootDir))
    {
        if (!std::filesystem::create_directories(rootDir))
        {
            throw std::runtime_error("Failed to create root directory");
        }
    }

    // 设置当前工作目录为根目录
    currentDir = rootDir;

    // 创建 socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0)
    {
        throw std::runtime_error("Socket creation failed");
    }

    // 设置服务器地址
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(port);

    // 绑定地址
    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
    {
        throw std::runtime_error("Bind failed");
    }
}

void Server::start()
{
    // 开始监听
    listen(serverSocket, 5);
    std::cout << "Server started, listening on port " << ntohs(serverAddr.sin_port) << std::endl;

    while (true)
    {
        socklen_t clientLen = sizeof(struct sockaddr_in);
        clientSocket = accept(serverSocket, (struct sockaddr *)&serverAddr, &clientLen);

        if (clientSocket < 0)
        {
            std::cerr << "Accept failed" << std::endl;
            continue;
        }

        handleClient();
    }
}

void Server::handleList()
{
    std::vector<std::string> files;
    for (const auto &entry : std::filesystem::directory_iterator(currentDir))
    {
        // 获取相对于当前目录的路径
        std::string name = entry.path().filename().string();
        if (std::filesystem::is_directory(entry.path()))
        {
            name += "/";
        }
        files.push_back(name);
    }

    // 如果不在根目录，添加 ".." 目录
    if (currentDir != rootDir)
    {
        files.insert(files.begin(), "../");
    }

    // 发送文件列表
    std::string fileList;
    for (const auto &file : files)
    {
        fileList += file + "\n";
    }

    Message response{Command::LIST, fileList, fileList.size()};
    sendResponse(response);
}

Server::~Server()
{
    if (serverSocket >= 0)
    {
        close(serverSocket);
    }
}

void Server::handleClient()
{
    try
    {
        while (true)
        {
            // 接收客户端消息
            uint32_t msgSize;
            if (recv(clientSocket, &msgSize, sizeof(msgSize), 0) <= 0)
            {
                break;
            }

            // 读取消息内容
            std::vector<char> buffer(msgSize);
            if (recv(clientSocket, buffer.data(), msgSize, 0) <= 0)
            {
                break;
            }

            // 解析消息
            Message msg = Message::deserialize(buffer);

            handleCommand(msg);
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error handling client: " << e.what() << std::endl;
    }

    close(clientSocket);
}

void Server::handleCommand(const Message &msg)
{
    try
    {
        switch (msg.command)
        {
        case Command::LIST:
            handleList();
            break;
        case Command::CD:
            handleChangeDir(msg.argument);
            break;
        case Command::DOWNLOAD:
            handleDownload(msg.argument);
            break;
        case Command::UPLOAD:
            handleUpload(msg.argument, msg.dataSize);
            break;
        case Command::MKDIR:
            handleMakeDir(msg.argument);
            break;
        case Command::RMDIR:
            handleRemoveDir(msg.argument);
            break;
        case Command::DELETE:
            handleDelete(msg.argument);
            break;
        case Command::QUIT:
            throw std::runtime_error("Client disconnected");
        default:
            throw std::runtime_error("Unknown command");
        }
    }
    catch (const std::exception &e)
    {
        // 发送错误响应给客户端
        Message response{msg.command, std::string("Error: ") + e.what(), 0};
        sendResponse(response);
    }
}

void Server::handleChangeDir(const std::string &path)
{
    std::filesystem::path newPath;
    if (path.empty() || path == "/")
    {
        // 如果路径为空或"/"，则切换到根目录
        newPath = rootDir;
    }
    else if (path[0] == '/')
    {
        // 如果是绝对路径，则从根目录开始解析
        newPath = std::filesystem::canonical(rootDir / path.substr(1));
    }
    else
    {
        // 如果是相对路径，则从当前目录开始解析
        newPath = std::filesystem::canonical(currentDir / path);
    }

    // 检查新路径是否在根目录下
    std::string rootStr = std::filesystem::canonical(rootDir).string();
    std::string newPathStr = newPath.string();

    if (newPathStr.substr(0, rootStr.length()) != rootStr)
    {
        throw std::runtime_error("Access denied: Cannot access directory outside root");
    }

    if (!std::filesystem::exists(newPath))
    {
        throw std::runtime_error("Path does not exist");
    }
    if (!std::filesystem::is_directory(newPath))
    {
        throw std::runtime_error("Path is not a directory");
    }

    currentDir = newPath;
    // 返回相对于根目录的路径
    std::string relPath = newPathStr.substr(rootStr.length());
    if (relPath.empty()) relPath = "/";
    Message response{Command::CD, "Changed to: " + relPath, 0};
    sendResponse(response);
}

void Server::handleDownload(const std::string &filename)
{
    std::filesystem::path filePath = currentDir / filename;
    if (!std::filesystem::exists(filePath))
    {
        throw std::runtime_error("File does not exist");
    }

    // 读取文件内容
    std::ifstream file(filePath, std::ios::binary);
    if (!file)
    {
        throw std::runtime_error("Cannot open file");
    }

    // 获取文件大小
    size_t fileSize = std::filesystem::file_size(filePath);

    // 发送文件大小信息
    Message response{Command::DOWNLOAD, filename, fileSize};
    sendResponse(response);

    sendFile(filePath);
}

void Server::handleUpload(const std::string &filename, size_t size)
{
    // 检查文件名是否包含路径分隔符
    if (filename.find('/') != std::string::npos || filename.find('\\') != std::string::npos)
    {
        throw std::runtime_error("Invalid filename: Cannot contain path separators");
    }

    std::filesystem::path filePath = currentDir / filename;
    std::string rootStr = std::filesystem::canonical(rootDir).string();
    std::string filePathStr = std::filesystem::canonical(currentDir).string() + "/" + filename;

    if (filePathStr.substr(0, rootStr.length()) != rootStr)
    {
        throw std::runtime_error("Access denied: Cannot write outside root directory");
    }

    // 创建文件
    std::ofstream file(filePath, std::ios::binary);
    if (!file)
    {
        throw std::runtime_error("Cannot create file");
    }

    // 接收文件内容
    size_t remainingBytes = size;
    std::vector<char> buffer(8192); // 8KB 缓冲区

    while (remainingBytes > 0)
    {
        size_t bytesToRead = std::min(remainingBytes, buffer.size());
        ssize_t bytesRead = recv(clientSocket, buffer.data(), bytesToRead, 0);
        
        if (bytesRead <= 0)
        {
            throw std::runtime_error("Failed to receive file content");
        }

        file.write(buffer.data(), bytesRead);
        remainingBytes -= bytesRead;
    }

    // 发送上传成功响应
    Message response{Command::UPLOAD, "File uploaded successfully", 0};
    sendResponse(response);
}

void Server::sendResponse(const Message &response)
{
    std::vector<char> data = response.serialize();
    uint32_t size = data.size();

    // 发送消息大小
    send(clientSocket, &size, sizeof(size), 0);
    // 发送消息内容
    send(clientSocket, data.data(), data.size(), 0);
}

void Server::sendFile(const std::filesystem::path &filePath)
{
    std::ifstream file(filePath, std::ios::binary);
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
}

void Server::handleMakeDir(const std::string &dirname)
{
    std::filesystem::path dirPath = currentDir / dirname;
    if (std::filesystem::exists(dirPath))
    {
        throw std::runtime_error("Directory already exists");
    }

    if (!std::filesystem::create_directory(dirPath))
    {
        throw std::runtime_error("Failed to create directory");
    }

    Message response{Command::MKDIR, "Directory created successfully", 0};
    sendResponse(response);
}

void Server::handleRemoveDir(const std::string &dirname)
{
    std::filesystem::path dirPath = currentDir / dirname;
    if (!std::filesystem::exists(dirPath))
    {
        throw std::runtime_error("Directory does not exist");
    }

    if (!std::filesystem::is_directory(dirPath))
    {
        throw std::runtime_error("Path is not a directory");
    }

    if (!std::filesystem::remove_all(dirPath))
    {
        throw std::runtime_error("Failed to remove directory");
    }

    Message response{Command::RMDIR, "Directory removed successfully", 0};
    sendResponse(response);
}

void Server::handleDelete(const std::string &filename)
{
    std::filesystem::path filePath = currentDir / filename;
    if (!std::filesystem::exists(filePath))
    {
        throw std::runtime_error("File does not exist");
    }

    if (!std::filesystem::is_regular_file(filePath))
    {
        throw std::runtime_error("Path is not a regular file");
    }

    if (!std::filesystem::remove(filePath))
    {
        throw std::runtime_error("Failed to delete file");
    }

    Message response{Command::DELETE, "File deleted successfully", 0};
    sendResponse(response);
}