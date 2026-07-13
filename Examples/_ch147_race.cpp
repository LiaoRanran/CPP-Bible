#include <thread>
int g = 0;
void inc(){ for(int i=0;i<100000;++i) ++g; }   // 非原子、非加锁
int main(){ std::thread a(inc), b(inc); a.join(); b.join(); }
