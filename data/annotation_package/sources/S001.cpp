#include <atomic>
#include <thread>
#include <cstdio>
std::atomic<int> f{0};int d=0;
int main(){std::thread w([]{d=42;f.store(1,std::memory_order_relaxed);});while(f.load(std::memory_order_relaxed)==0){}std::printf("%d\n",d);w.join();}
