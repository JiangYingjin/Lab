#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <fnmatch.h>
#include <ctime>
#include <cstdlib>

void myfind(const std::string &path, const std::string &name_pattern, int mtime);

int main(int argc, char *argv[])
{
    std::string path = ".";
    std::string name_pattern;
    int mtime = -1;

    // 参数解析
    int i = 1;
    if (argc > 1 && argv[1][0] != '-')
    {
        path = argv[1];
        i++;
    }

    for (; i < argc; ++i)
    {
        std::string option = argv[i];
        if (option == "-name" && i + 1 < argc)
        {
            name_pattern = argv[++i];
        }
        else if (option == "-mtime" && i + 1 < argc)
        {
            mtime = std::stoi(argv[++i]);
        }
    }

    // 调用 myfind 函数
    myfind(path, name_pattern, mtime);

    return 0;
}

void myfind(const std::string &path, const std::string &name_pattern, int mtime)
{
    DIR *dir = opendir(path.c_str());
    if (!dir)
    {
        perror(("Cannot open directory: " + path).c_str());
        return;
    }

    struct dirent *entry;
    struct stat filestat;

    time_t now = std::time(nullptr);

    while ((entry = readdir(dir)) != nullptr)
    {
        std::string entry_name = entry->d_name;

        // 忽略 . 和 ..
        if (entry_name == "." || entry_name == "..")
            continue;

        std::string fullpath = path + "/" + entry_name;

        if (stat(fullpath.c_str(), &filestat) == -1)
        {
            perror(("Cannot access file: " + fullpath).c_str());
            continue;
        }

        // 检查文件名是否匹配
        bool name_match = true;
        if (!name_pattern.empty())
        {
            name_match = fnmatch(name_pattern.c_str(), entry_name.c_str(), 0) == 0;
        }

        // 检查修改时间是否匹配
        bool time_match = true;
        if (mtime != -1)
        {
            int days_diff = (now - filestat.st_mtime) / (60 * 60 * 24);
            time_match = (days_diff == mtime);
        }

        // 如果没有指定过滤条件，默认输出所有文件
        if (name_pattern.empty() && mtime == -1)
        {
            name_match = true;
            time_match = true;
        }

        // 如果匹配，输出文件路径
        if (name_match && time_match)
        {
            std::cout << fullpath << std::endl;
        }

        // 如果是目录，递归调用
        if (S_ISDIR(filestat.st_mode))
        {
            myfind(fullpath, name_pattern, mtime);
        }
    }

    closedir(dir);
}
