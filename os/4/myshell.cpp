#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

const int MAX_HISTORY = 10;

// 保存历史命令的全局变量
std::vector<std::string> history;

// 添加命令到历史记录
void add_to_history(const std::string &command)
{
    if (command.empty())
        return;
    if (history.size() == MAX_HISTORY)
    {
        history.erase(history.begin());
    }
    history.push_back(command);
}

// 打印历史命令
void print_history()
{
    for (size_t i = 0; i < history.size(); ++i)
    {
        std::cout << i + 1 << ": " << history[i] << std::endl;
    }
}

// 内部命令处理
bool handle_internal_command(const std::vector<std::string> &tokens)
{
    if (tokens.empty())
        return false;

    if (tokens[0] == "exit")
    {
        // exit 命令
        exit(0);
    }
    else if (tokens[0] == "cd")
    {
        // cd 命令
        if (tokens.size() < 2)
        {
            std::cerr << "cd: Missing argument" << std::endl;
            return true;
        }
        if (chdir(tokens[1].c_str()) != 0)
        {
            perror("cd");
        }
        return true;
    }
    else if (tokens[0] == "history")
    {
        // 打印历史命令
        print_history();
        return true;
    }

    return false; // 不是内部命令
}

// 分割输入命令为令牌
std::vector<std::string> split_command(const std::string &command)
{
    std::vector<std::string> tokens;
    std::istringstream stream(command);
    std::string token;
    while (stream >> token)
    {
        tokens.push_back(token);
    }
    return tokens;
}

// 执行外部命令
void execute_external_command(const std::vector<std::string> &tokens)
{
    std::vector<char *> args;
    for (const auto &token : tokens)
    {
        args.push_back(const_cast<char *>(token.c_str()));
    }
    args.push_back(nullptr);

    pid_t pid = fork();
    if (pid == 0)
    {
        // 子进程
        execvp(args[0], args.data());
        perror("execvp"); // 如果 execvp 失败
        exit(1);
    }
    else if (pid > 0)
    {
        // 父进程等待子进程
        wait(nullptr);
    }
    else
    {
        perror("fork");
    }
}

// 获取当前工作目录的函数
std::string get_current_directory()
{
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != nullptr)
    {
        return std::string(cwd);
    }
    return "unknown";
}

int main()
{
    while (true)
    {
        // 打印提示符，包含当前工作目录
        std::cout << "(mysh) " << get_current_directory() << " > ";
        std::string command;
        std::getline(std::cin, command);

        if (command.empty())
            continue;

        // 保存命令到历史记录
        add_to_history(command);

        // 分割命令为令牌
        auto tokens = split_command(command);

        // 处理内部命令
        if (handle_internal_command(tokens))
        {
            continue;
        }

        // 执行外部命令
        execute_external_command(tokens);
    }

    return 0;
}
