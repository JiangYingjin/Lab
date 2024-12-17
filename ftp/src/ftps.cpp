#include "server.h"
#include <iostream>
#include <string>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <port>\n";
        return 1;
    }

    try
    {
        uint16_t port = std::stoi(argv[1]);
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