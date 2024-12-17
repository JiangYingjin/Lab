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
              << "  help                 - Show this help\n"
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
        // ... 其余代码保持不变 ...
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }
}