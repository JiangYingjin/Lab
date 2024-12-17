#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <vector>
#include <chrono>
#include <iomanip>

using namespace std;

const int READER_FIRST = 1;
const int WRITER_FIRST = 2;

enum class RequestType
{
    Reader,
    Writer
};

struct Process
{
    int id;
    RequestType type;
    int start_time;
    int duration;
};

time_t now = time(0);
void print_now_sec()
{
    // 打印程序已运行的秒数，保留小数点
    cout << fixed << setprecision(1) << difftime(time(0), now) << "s: ";
}

class ReaderWriter
{
public:
    ReaderWriter(int priority) : priority_(priority) {}

    void read(int id, int duration)
    {
        // print_now_sec();
        cout << "reader " << id << " waiting to read" << endl;
        readerQueue.push(id);

        unique_lock<mutex> lock(mutex_);
        // 当调用 wait 方法时，当前的 lock 会被释放
        // 调用 wait 后，当前线程会被阻塞，直到条件变量 cv_ 被通知（通常是通过 notify_one() 或 notify_all()）或者 can_read() 返回 true
        // 一旦 can_read() 的条件满足，wait 方法会重新获取 lock，然后继续执行后面的代码
        cv_.wait(lock, [this]()
                 { return can_read(); });
        readerQueue.pop();
        readingCount++;
        lock.unlock();

        // print_now_sec();
        cout << "reader " << id << " starts to read" << endl;
        this_thread::sleep_for(chrono::seconds(duration));
        // print_now_sec();
        cout << "reader " << id << " ends reading" << endl;

        lock.lock();
        readingCount--;
        cv_.notify_all();
    }

    void write(int id, int duration)
    {
        // print_now_sec();
        cout << "writer " << id << " waiting to write" << endl;
        writerQueue.push(id);

        unique_lock<mutex> lock(mutex_);
        cv_.wait(lock, [this]()
                 { return can_write(); });

        writerQueue.pop();
        writerMutex_ = 0;
        lock.unlock();

        // print_now_sec();
        cout << "writer " << id << " starts to write" << endl;
        this_thread::sleep_for(chrono::seconds(duration));
        // print_now_sec();
        cout << "writer " << id << " ends writing" << endl;

        lock.lock();
        writerMutex_ = 1;
        cv_.notify_all();
    }

private:
    mutex mutex_;
    int writerMutex_ = 1;
    condition_variable cv_;
    queue<int> readerQueue;
    queue<int> writerQueue;
    int readingCount = 0;
    int priority_;

    /*
    线程等待：条件变量允许线程在某个条件不满足时挂起（阻塞），而不是持续占用 CPU 资源。这对于避免忙等待（busy waiting）非常有用
    通知机制：当某个条件发生变化时，其他线程可以使用条件变量来通知等待的线程，表明条件已满足。
    释放锁：当一个线程调用 wait() 方法时，条件变量会自动释放与之关联的互斥锁，允许其他线程访问共享资源。
    阻塞线程：调用 wait() 的线程会被阻塞，直到条件变量被通知（通过 notify_one() 或 notify_all()）或者条件满足。
    恢复执行：当条件变量被通知后，等待的线程会重新获取互斥锁，然后继续执行。
    */

    bool can_read()
    {
        if (priority_ == READER_FIRST)
        {
            // 没有在写的线程
            return writerMutex_ == 1;
        }
        else if (priority_ == WRITER_FIRST)
        {
            // 没有在写的线程，也没有等待要写
            return writerMutex_ == 1 && writerQueue.empty();
        }
        else
        {
            return false;
        }
    }

    bool can_write()
    {
        if (priority_ == READER_FIRST)
        {
            return readerQueue.empty() && writerMutex_ == 1 && readingCount == 0;
        }
        else if (priority_ == WRITER_FIRST)
        {
            // 没有在写的线程，也没有在读的线程
            return writerMutex_ == 1 && readingCount == 0;
        }
        else
        {
            return false;
        }
    }
};

void process_request(ReaderWriter &rw, const Process &p)
{
    if (p.type == RequestType::Reader)
    {
        this_thread::sleep_for(chrono::seconds(p.start_time));
        rw.read(p.id, p.duration);
    }
    else
    {
        this_thread::sleep_for(chrono::seconds(p.start_time));
        rw.write(p.id, p.duration);
    }
}

int main()
{
    int priority, num_processes;
    cin >> priority >> num_processes;

    ReaderWriter rw(priority);
    vector<thread> threads;
    vector<Process> processes;

    for (int i = 0; i < num_processes; ++i)
    {
        int id, start_time, duration;
        char type;
        cin >> id >> type >> start_time >> duration;

        Process p{id, (type == 'R' ? RequestType::Reader : RequestType::Writer), start_time, duration};
        processes.push_back(p);
        // cout << p.id << " " << (p.type == RequestType::Reader ? "Reader" : "Writer") << " " << p.start_time << " " << p.duration << endl;
    }

    for (auto &p : processes)
    {
        threads.push_back(thread(process_request, ref(rw), p));
    }

    for (auto &t : threads)
    {
        t.join();
    }

    return 0;
}
