#include <atomic>
#include <thread>
std::atomic<int> x{0};
int main(){std::thread t1([]{x.fetch_add(1,std::memory_order_relaxed);});std::thread t2([]{x.fetch_add(1,std::memory_order_relaxed);});t1.join();t2.join();return x.load();}
