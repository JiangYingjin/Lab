#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <vector>
#include <chrono>
#include <algorithm>

using namespace std;

struct Customer
{
    int id;
    int arrivalTime;
};

class BarberShop
{
private:
    int numChairs;
    int haircutTime;
    int customersInChairs = 0;
    queue<Customer> waitingQueue;
    mutex mtx;
    condition_variable cvBarber;
    condition_variable cvCustomer;

public:
    BarberShop(int c, int ht) : numChairs(c), haircutTime(ht) {}

    void customerArrives(Customer customer)
    {
        // 模拟顾客到达时间
        this_thread::sleep_for(chrono::seconds(customer.arrivalTime));
        // cout << "customer " << customer.id << " arrives at " << customer.arrivalTime << " seconds" << endl;

        // 加锁：在构造 lock 对象时，它会尝试锁定 mtx 互斥量。如果 mtx 已经被其他线程锁定，当前线程将会阻塞，直到 mtx 可用。
        // 作用域管理：lock 对象的生命周期与其作用域相同。当 lock 超出作用域时，它的析构函数会被调用，自动解锁 mtx，确保不会造成死锁。
        unique_lock<mutex> lock(mtx);

        // 检查是否有空椅子
        if (customersInChairs < numChairs)
        {
            cout << "customer " << customer.id << ": there are " << customersInChairs << " customers in front waiting for a haircut" << endl;
            waitingQueue.push(customer);
            customersInChairs++;
            cvCustomer.notify_one(); // 通知理发师

            // 让当前线程等待，直到条件变量 cvBarber 被通知
            // 在调用 wait 时，线程会自动释放与 lock 关联的互斥量，并进入等待状态
            // 这样可以避免死锁，因为其他线程可以在此期间获得锁并修改共享资源。
            cvBarber.wait(lock); // 等待理发师完成理发
        }
        else
        {
            cout << "customer " << customer.id << ": no more empty chairs, customer leaves" << endl;
        }

        // 自动解锁 mtx
    }

    void barberCutsHair()
    {
        while (true)
        {
            unique_lock<mutex> lock(mtx);
            cvCustomer.wait(lock, [this]
                            { return !waitingQueue.empty(); });

            // 取出队首顾客
            Customer customer = waitingQueue.front();
            waitingQueue.pop();
            customersInChairs--;
            lock.unlock();

            // 开始理发并模拟理发时间
            this_thread::sleep_for(chrono::seconds(haircutTime));

            // 理发结束
            cout << "customer " << customer.id << " finished haircut" << endl;

            cvBarber.notify_one(); // 通知顾客理发结束
        }
    }
};

int main()
{
    int n, barberCount, chairCount, haircutTime;
    cin >> n >> barberCount >> chairCount >> haircutTime;

    BarberShop shop(chairCount, haircutTime);
    vector<thread> customersThreads;
    vector<Customer> customers(n);

    // 读取顾客到达时间
    for (int i = 0; i < n; ++i)
    {
        cin >> customers[i].id >> customers[i].arrivalTime;
    }

    // 创建顾客线程
    for (int i = 0; i < n; ++i)
    {
        // cout << "create customer thread " << i << endl;
        customersThreads.push_back(thread(&BarberShop::customerArrives, &shop, customers[i]));
    }

    // 创建理发师线程
    thread barberThread(&BarberShop::barberCutsHair, &shop);

    // 等待所有顾客线程结束
    for (auto &t : customersThreads)
    {
        t.join();
    }

    // 结束理发师线程
    barberThread.join();

    return 0;
}
