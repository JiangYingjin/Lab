#include "server.h"
#include <iostream>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

// 检查端口是否可用
bool isPortAvailable(uint16_t port)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
        return false;

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    bool available = (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) == 0);
    close(sock);
    return available;
}

// 获取可用端口
uint16_t getAvailablePort(uint16_t startPort)
{
    std::vector<uint16_t> defaultPorts = {21, 2101}; // 默认尝试这些端口

    // 首先尝试指定的起始端口
    if (startPort > 0)
    {
        if (isPortAvailable(startPort))
        {
            return startPort;
        }
        return 0; // 如果指定端口不可用，返回0表示失败
    }

    // 然后尝试默认端口
    for (uint16_t port : defaultPorts)
    {
        if (isPortAvailable(port))
        {
            return port;
        }
    }

    // 如果默认端口都不可用，从2102开始尝试
    uint16_t port = 2102;
    while (port < 65535)
    {
        if (isPortAvailable(port))
        {
            return port;
        }
        port++;
    }

    return 0; // 如果没有可用端口，返回0
}

int main(int argc, char *argv[])
{
    uint16_t port = 0;

    if (argc > 2)
    {
        std::cerr << "Usage: " << argv[0] << " [port]\n";
        return 1;
    }
    else if (argc == 2)
    {
        try
        {
            port = std::stoi(argv[1]);
            port = getAvailablePort(port);
            if (port == 0)
            {
                std::cerr << "Specified port " << argv[1] << " is not available\n";
                return 1;
            }
        }
        catch (const std::exception &)
        {
            std::cerr << "Invalid port number\n";
            return 1;
        }
    }
    else
    {
        port = getAvailablePort(0);
        if (port == 0)
        {
            std::cerr << "No available ports found\n";
            return 1;
        }
    }

    try
    {
        ftp::server::Server server(port);

        std::cout << "FTP Server starting on port " << port << "...\n";
        server.start();

        return 0;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }
}