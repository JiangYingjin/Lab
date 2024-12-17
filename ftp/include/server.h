#pragma once
#include <filesystem>
#include <sys/socket.h>
#include <netinet/in.h>
#include "protocol.h"

namespace ftp
{
    namespace server
    {

        class Server
        {
        public:
            explicit Server(uint16_t port);
            ~Server();

            void start();

        private:
            int serverSocket;
            int clientSocket;
            struct sockaddr_in serverAddr;
            std::filesystem::path currentDir;

            void handleClient();
            void handleCommand(const protocol::Message &msg);

            // 命令处理函数
            void handleList();
            void handleChangeDir(const std::string &path);
            void handleDownload(const std::string &filename);
            void handleUpload(const std::string &filename, size_t size);
            void handleMakeDir(const std::string &dirname);
            void handleRemoveDir(const std::string &dirname);
            void handleDelete(const std::string &filename);

            // 辅助函数
            void sendResponse(const protocol::Message &response);
            void sendFile(const std::filesystem::path &filePath);
        };

    } // namespace server
} // namespace ftp