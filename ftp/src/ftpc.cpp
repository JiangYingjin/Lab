#include "client.h"
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <chrono>

using namespace ftp::client;
using namespace ftp::protocol;

// ANSI 颜色代码
namespace Color {
    const std::string Reset   = "\033[0m";
    const std::string Bold    = "\033[1m";
    const std::string Red     = "\033[31m";
    const std::string Green   = "\033[32m";
    const std::string Yellow  = "\033[33m";
    const std::string Blue    = "\033[34m";
    const std::string Magenta = "\033[35m";
    const std::string Cyan    = "\033[36m";
    const std::string White   = "\033[37m";
}

// 添加更多颜色和样式组合
namespace Style {
    // 状态颜色
    const std::string Success = Color::Green;
    const std::string Error = Color::Red;
    const std::string Info = Color::Blue;
    const std::string Warning = Color::Yellow;
    const std::string Highlight = Color::Cyan;

    // 组合样式
    const std::string Header = Color::Bold + Color::Magenta;
    const std::string Prompt = Color::Bold + Color::Blue;
    const std::string Command = Color::Bold + Color::Cyan;
    const std::string Path = Color::Bold + Color::Yellow;
    const std::string Dir = Color::Blue;
    const std::string File = Color::White;
    const std::string Size = Color::Green;
}

// 格式化文件大小
std::string formatSize(size_t bytes)
{
    const char* units[] = {"B", "KB", "MB", "GB"};
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

void printHelp()
{
    std::cout << Style::Header << "\nFTP Client Commands:\n" << Color::Reset
              << "\n"
              << Style::Command << "  File Operations:\n" << Color::Reset
              << "    l, ls" << Color::Reset << "                  - List files and directories\n"
              << "    get <file>" << Color::Reset << "             - Download file\n"
              << "    put <file>" << Color::Reset << "             - Upload file\n"
              << "\n"
              << Style::Command << "  Directory Operations:\n" << Color::Reset
              << "    cd <path>" << Color::Reset << "              - Change directory\n"
              << "    pwd" << Color::Reset << "                    - Print working directory\n"
              << "    mkdir <dir>" << Color::Reset << "            - Create directory\n"
              << "    rm <file|dir> [-r]" << Color::Reset << "     - Remove file or directory (-r for recursive)\n"
              << "\n"
              << Style::Command << "  System Commands:\n" << Color::Reset
              << "    clear, cls" << Color::Reset << "             - Clear screen\n"
              << "    help, ?" << Color::Reset << "                - Show this help\n"
              << "    exit, quit, q" << Color::Reset << "          - Exit program\n"
              << "\n";
}

// 分割命令行参数
std::vector<std::string> splitCommand(const std::string &line)
{
    std::vector<std::string> args;
    std::istringstream iss(line);
    std::string arg;
    
    while (iss >> arg)
    {
        args.push_back(arg);
    }
    
    return args;
}

void clearScreen()
{
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

// 打印进度信息
void printProgress(const std::string &operation, size_t current, size_t total)
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
    std::cout << Style::Info << operation << ": " << Color::Reset;
    std::cout << "[";
    for (int i = 0; i < width; ++i)
    {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] ";

    // 显示百分比和大小信息
    std::cout << Style::Success << int(percentage * 100.0) << "%" << Color::Reset;
    std::cout << " " << formatSize(current) << "/" << formatSize(total);

    // 显示传输速度
    if (speed > 0)
    {
        std::cout << " " << Style::Info << "@ " << formatSize((size_t)speed) << "/s" << Color::Reset;
    }

    // 显示预估剩余时间
    if (eta > 0)
    {
        std::cout << " " << Style::Warning << "ETA: ";
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
        std::cout << eta << "s" << Color::Reset;
    }

    std::cout << std::flush;
}

// 打印文件列表
void printFileList(const std::vector<std::string> &files)
{
    std::cout << Style::Header << "\nDirectory contents:" << Color::Reset << std::endl;
    
    size_t maxWidth = 0;
    for (const auto &file : files)
    {
        maxWidth = std::max(maxWidth, file.length());
    }
    maxWidth = ((maxWidth + 4) / 4) * 4; // 对齐到4的倍数

    int columns = 80 / (maxWidth + 2);
    columns = std::max(1, columns);
    int col = 0;

    for (const auto &file : files)
    {
        if (file.back() == '/')
        {
            std::cout << Style::Dir << std::left << std::setw(maxWidth + 2) << file << Color::Reset;
        }
        else
        {
            std::cout << Style::File << std::left << std::setw(maxWidth + 2) << file << Color::Reset;
        }

        if (++col >= columns)
        {
            std::cout << "\n";
            col = 0;
        }
    }
    if (col != 0) std::cout << "\n";
    std::cout << Style::Info << "Total: " << files.size() << " items" << Color::Reset << std::endl;
}

// 打印成功消息
void printSuccess(const std::string &msg)
{
    std::cout << Style::Success << "✓ " << msg << Color::Reset << std::endl;
}

// 打印错误消息
void printError(const std::string &msg)
{
    std::cerr << Style::Error << "✗ " << msg << Color::Reset << std::endl;
}

// 打印警告消息
void printWarning(const std::string &msg)
{
    std::cout << Style::Warning << "! " << msg << Color::Reset << std::endl;
}

// 打印信息消息
void printInfo(const std::string &msg)
{
    std::cout << Style::Info << "ℹ " << msg << Color::Reset << std::endl;
}

// 打印用法提示
void printUsage(const std::string &cmd, const std::string &usage)
{
    std::cout << Style::Warning << "Usage: " << Style::Command << cmd 
              << Color::Reset << " " << usage << std::endl;
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printError("Invalid arguments");
        printUsage(argv[0], "<server_ip> <port>");
        return 1;
    }

    try
    {
        Client client(argv[1], std::stoi(argv[2]));

        if (!client.connect())
        {
            printError("Failed to connect to server");
            return 1;
        }

        std::cout << Style::Success << "✓ Connected to server " << Style::Highlight 
                  << argv[1] << ":" << argv[2] << Color::Reset << "\n"
                  << Style::Info << "Type " << Style::Command << "help" << Color::Reset 
                  << Style::Info << " or " << Style::Command << "?" << Color::Reset 
                  << Style::Info << " for available commands." << Color::Reset << std::endl;

        std::string line;
        while (true)
        {
            std::cout << Style::Prompt << "ftp> " << Color::Reset;
            std::getline(std::cin, line);

            auto args = splitCommand(line);
            if (args.empty()) continue;

            std::string &command = args[0];
            std::transform(command.begin(), command.end(), command.begin(), ::tolower);

            if (command == "help" || command == "?")
            {
                printHelp();
            }
            else if (command == "ls" || command == "l")
            {
                auto files = client.listFiles();
                printFileList(files);
            }
            else if (command == "cd")
            {
                if (args.size() < 2)
                {
                    printUsage("cd", "<path>");
                    continue;
                }
                if (client.changeDirectory(args[1]))
                {
                    printSuccess("Directory changed successfully");
                }
                else
                {
                    printError("Failed to change directory");
                }
            }
            else if (command == "get")
            {
                if (args.size() < 2)
                {
                    printUsage("get", "<file>");
                    continue;
                }
                bool success = client.downloadFile(args[1]);
                if (success)
                {
                    printSuccess("File downloaded successfully");
                }
            }
            else if (command == "put")
            {
                if (args.size() < 2)
                {
                    printUsage("put", "<file>");
                    continue;
                }
                if (client.uploadFile(args[1]))
                {
                    printSuccess("File uploaded successfully");
                }
                else
                {
                    printError("Failed to upload file");
                }
            }
            else if (command == "mkdir")
            {
                if (args.size() < 2)
                {
                    printUsage("mkdir", "<dir>");
                    continue;
                }
                if (client.createDirectory(args[1]))
                {
                    printSuccess("Directory created successfully");
                }
                else
                {
                    printError("Failed to create directory");
                }
            }
            else if (command == "rm")
            {
                if (args.size() < 2)
                {
                    printUsage("rm", "<file|dir> [-r]");
                    continue;
                }
                
                bool recursive = (args.size() > 2 && args[2] == "-r");
                
                if (recursive)
                {
                    if (client.removeDirectory(args[1]))
                    {
                        printSuccess("Directory removed successfully");
                    }
                    else
                    {
                        printError("Failed to remove directory");
                    }
                }
                else
                {
                    if (client.deleteFile(args[1]))
                    {
                        printSuccess("File deleted successfully");
                    }
                    else
                    {
                        printError("Failed to delete file");
                    }
                }
            }
            else if (command == "pwd")
            {
                if (!client.changeDirectory("."))
                {
                    printError("Failed to get current directory");
                }
            }
            else if (command == "clear" || command == "cls")
            {
                clearScreen();
            }
            else if (command == "exit" || command == "quit" || command == "q")
            {
                std::cout << Style::Success << "✓ Goodbye! Thanks for using FTP client." << Color::Reset << std::endl;
                break;
            }
            else if (!command.empty())
            {
                printError("Unknown command. Type 'help' for available commands.");
            }
        }

        return 0;
    }
    catch (const std::exception &e)
    {
        printError(std::string("Error: ") + e.what());
        return 1;
    }
}