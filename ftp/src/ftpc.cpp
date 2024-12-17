#include "client.h"
#include <iostream>
#include <string>
#include <sstream>

using namespace ftp::client;
using namespace ftp::protocol;

void printHelp()
{
    std::cout << "Available commands:\n"
              << "  ls                   - List files\n"
              << "  cd <path>            - Change directory\n"
              << "  get <file>           - Download file\n"
              << "  put <file>           - Upload file\n"
              << "  mkdir <dir>          - Create directory\n"
              << "  rmdir <dir>          - Remove directory\n"
              << "  rm <file>            - Delete file\n"
              << "  help, ?              - Show this help\n"
              << "  exit                 - Exit program\n";
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        std::cerr << "Usage: " << argv[0] << " <server_ip> <port>\n";
        return 1;
    }

    try
    {
        Client client(argv[1], std::stoi(argv[2]));

        // 连接到服务器
        if (!client.connect())
        {
            std::cerr << "Failed to connect to server\n";
            return 1;
        }

        std::cout << "Connected to server. Type 'help' for available commands.\n";

        std::string line;
        while (true)
        {
            std::cout << "ftp> ";
            std::getline(std::cin, line);

            std::istringstream iss(line);
            std::string command;
            iss >> command;

            if (command == "help" || command == "?")
            {
                printHelp();
            }
            else if (command == "ls")
            {
                auto files = client.listFiles();
                for (const auto &file : files)
                {
                    std::cout << file << std::endl;
                }
            }
            else if (command == "cd")
            {
                std::string path;
                iss >> path;
                if (client.changeDirectory(path))
                {
                    std::cout << "Directory changed successfully\n";
                }
                else
                {
                    std::cout << "Failed to change directory\n";
                }
            }
            else if (command == "get")
            {
                std::string filename;
                iss >> filename;
                if (client.downloadFile(filename))
                {
                    std::cout << "File downloaded successfully\n";
                }
                else
                {
                    std::cout << "Failed to download file\n";
                }
            }
            else if (command == "put")
            {
                std::string filename;
                iss >> filename;
                if (client.uploadFile(filename))
                {
                    std::cout << "File uploaded successfully\n";
                }
                else
                {
                    std::cout << "Failed to upload file\n";
                }
            }
            else if (command == "mkdir")
            {
                std::string dirname;
                iss >> dirname;
                if (client.createDirectory(dirname))
                {
                    std::cout << "Directory created successfully\n";
                }
                else
                {
                    std::cout << "Failed to create directory\n";
                }
            }
            else if (command == "rmdir")
            {
                std::string dirname;
                iss >> dirname;
                if (client.removeDirectory(dirname))
                {
                    std::cout << "Directory removed successfully\n";
                }
                else
                {
                    std::cout << "Failed to remove directory\n";
                }
            }
            else if (command == "rm")
            {
                std::string filename;
                iss >> filename;
                if (client.deleteFile(filename))
                {
                    std::cout << "File deleted successfully\n";
                }
                else
                {
                    std::cout << "Failed to delete file\n";
                }
            }
            else if (command == "exit")
            {
                break;
            }
            else if (!command.empty())
            {
                std::cout << "Unknown command. Type 'help' for available commands.\n";
            }
        }

        return 0;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }
}