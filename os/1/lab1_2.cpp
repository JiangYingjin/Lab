#include <unistd.h>
#include <iostream>
#include <pthread.h>
#include <chrono>
#include <thread>

using namespace std;

// Shared variable
int shared_var = 0;

void *thread_func(void *arg)
{
    this_thread::sleep_for(std::chrono::milliseconds(10));
    while (true)
    {
        shared_var--;
        cout << "Thread: shared_var = " << shared_var << endl;
        this_thread::sleep_for(std::chrono::seconds(1));
    }
    return nullptr;
}

int main()
{
    cout << "Initial shared_var = " << shared_var << endl;

    pthread_t thread;

    // Create a thread
    if (pthread_create(&thread, nullptr, thread_func, nullptr))
    {
        cerr << "Error creating thread" << endl;
        return 1;
    }

    // Main thread
    while (true)
    {
        shared_var++;
        cout << "Main: shared_var = " << shared_var << endl;
        this_thread::sleep_for(std::chrono::seconds(1));
    }

    // Wait for the thread to finish
    pthread_join(thread, nullptr);

    return 0;
}
