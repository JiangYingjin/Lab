#pragma once
#include <string>
#include <stdexcept>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "protocol.h"

namespace ftp
{

    class Socket
    {
        friend class ServerSocket;

    public:
        Socket() : sockfd(-1) {}
        virtual ~Socket()
        {
            if (sockfd != -1)
            {
                close(sockfd);
            }
        }

        // 接收数据
        ssize_t receive(void *buffer, size_t length)
        {
            return recv(sockfd, buffer, length, 0);
        }

        // 发送数据
        ssize_t send(const void *buffer, size_t length)
        {
            return ::send(sockfd, buffer, length, 0);
        }

        // 接收消息
        protocol::Message receiveMessage()
        {
            protocol::Message msg;
            ssize_t bytesRead = receive(&msg, sizeof(msg));
            if (bytesRead != sizeof(msg))
            {
                throw std::runtime_error("Failed to receive message");
            }
            return msg;
        }

        // 发送消息
        void sendMessage(const protocol::Message &msg)
        {
            ssize_t bytesSent = send(&msg, sizeof(msg));
            if (bytesSent != sizeof(msg))
            {
                throw std::runtime_error("Failed to send message");
            }
        }

    protected:
        int sockfd;
        void setSockfd(int fd) { sockfd = fd; }
    };

    // 服务器 socket 类
    class ServerSocket : public Socket
    {
    public:
        explicit ServerSocket(uint16_t port)
        {
            sockfd = socket(AF_INET, SOCK_STREAM, 0);
            if (sockfd == -1)
            {
                throw std::runtime_error("Failed to create socket");
            }

            // 设置地址重用
            int opt = 1;
            setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

            struct sockaddr_in addr;
            addr.sin_family = AF_INET;
            addr.sin_addr.s_addr = INADDR_ANY;
            addr.sin_port = htons(port);

            if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
            {
                throw std::runtime_error("Failed to bind socket");
            }

            if (listen(sockfd, 5) < 0)
            {
                throw std::runtime_error("Failed to listen on socket");
            }
        }

        // 接受客户端连接
        Socket *acceptClient()
        {
            struct sockaddr_in clientAddr;
            socklen_t clientLen = sizeof(clientAddr);

            Socket *clientSocket = new Socket();
            int clientFd = accept(sockfd, (struct sockaddr *)&clientAddr, &clientLen);

            if (clientFd < 0)
            {
                delete clientSocket;
                throw std::runtime_error("Failed to accept client connection");
            }

            clientSocket->setSockfd(clientFd);
            return clientSocket;
        }
    };

    // 客户端 socket 类
    class ClientSocket : public Socket
    {
    public:
        void connect(const std::string &host, uint16_t port)
        {
            sockfd = socket(AF_INET, SOCK_STREAM, 0);
            if (sockfd == -1)
            {
                throw std::runtime_error("Failed to create socket");
            }

            struct sockaddr_in addr;
            addr.sin_family = AF_INET;
            addr.sin_port = htons(port);

            if (inet_pton(AF_INET, host.c_str(), &addr.sin_addr) <= 0)
            {
                throw std::runtime_error("Invalid address");
            }

            if (::connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
            {
                throw std::runtime_error("Connection failed");
            }
        }
    };

} // namespace ftp