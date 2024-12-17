#include <unistd.h>
#include <iostream>
#include <chrono>
#include <iomanip>

using namespace std;

int main()
{
    pid_t pid = fork();

    if (pid == 0)
    {
        // Child process
        execl("./an_ch2_1b", "an_ch2_1b", nullptr);
    }
    else if (pid > 0)
    {
        // Parent process
        while (true)
        {
            auto now = chrono::system_clock::now();
            time_t now_c = chrono::system_clock::to_time_t(now);
            tm *ltm = localtime(&now_c);

            cout << "The parent is talking at "
                 << put_time(ltm, "%H:%M:%S") << endl;

            sleep(1);
        }
    }
    else
    {
        cerr << "Fork failed!" << endl;
        return 1;
    }
    return 0;
}
