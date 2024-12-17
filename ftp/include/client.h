#pragma once
#include <sys/socket.h>
#include <netinet/in.h>
#include "protocol.h"

namespace ftp
{
    namespace client
    {

        class Client
        {
        public:
            Client(const std::string &serverIP, uint16_t port);
            ~Client();

            bool connect();

            // 客户端命令接口
            std::vector<std::string> listFiles();
            bool changeDirectory(const std::string &path);
            bool downloadFile(const std::string &filename);
            bool uploadFile(const std::string &filename);
            bool createDirectory(const std::string &dirname);
            bool removeDirectory(const std::string &dirname);
            bool deleteFile(const std::string &filename);

        private:
            int clientSocket;
            struct sockaddr_in serverAddr;

            // 辅助函数
            void sendMessage(const protocol::Message &msg);
            protocol::Message receiveResponse();
            void printProgress(const std::string &operation, size_t current, size_t total);
            std::string formatSize(size_t bytes);
            void printError(const std::string &msg);
        };

    } // namespace client
} // namespace ftp