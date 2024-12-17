#include <unistd.h>
#include <iostream>
#include <chrono>
#include <iomanip>

using namespace std;

int main()
{
    while (true)
    {
        auto now = chrono::system_clock::now();
        time_t now_c = chrono::system_clock::to_time_t(now);
        tm *ltm = localtime(&now_c);

        cout << "The child is talking at "
             << put_time(ltm, "%H:%M:%S") << endl;

        sleep(1);
    }
    return 0;
}
