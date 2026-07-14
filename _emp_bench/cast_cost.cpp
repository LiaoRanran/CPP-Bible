// cast_cost.cpp —— 实测 dynamic_cast vs static_cast vs 虚调用开销（ch27 §10 声称）
// 编译: g++ -std=c++23 -O2 -pthread cast_cost.cpp -o cast_cost && ./cast_cost
#include <cstdio>
#include <chrono>

struct Base { virtual ~Base() = default; virtual int work() { return 1; } };
struct Derived : Base { int work() override { return 2; } };

static inline double ns(std::chrono::nanoseconds t, long long n){ return t.count()/(double)n; }

int main(){
    const long long N = 100'000'000LL;
    Derived d; Base* p = &d; volatile int sink = 0;

    // 虚函数调用
    {
        auto t0 = std::chrono::high_resolution_clock::now();
        for(long long i=0;i<N;++i) sink += p->work();
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("virtual call           : %.3f ns/op   (sink=%d)\n", ns(t1-t0,N), (int)sink);
    }
    // static_cast 下行 + 调用
    {
        auto t0 = std::chrono::high_resolution_clock::now();
        for(long long i=0;i<N;++i){ Derived* q=static_cast<Derived*>(p); sink += q->work(); }
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("static_cast down+call  : %.3f ns/op   (sink=%d)\n", ns(t1-t0,N), (int)sink);
    }
    // dynamic_cast 下行 + 调用（成功路径）
    {
        auto t0 = std::chrono::high_resolution_clock::now();
        for(long long i=0;i<N;++i){ Derived* q=dynamic_cast<Derived*>(p); sink += q->work(); }
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("dynamic_cast down+call : %.3f ns/op   (sink=%d)\n", ns(t1-t0,N), (int)sink);
    }
    // dynamic_cast 失败路径（返回 nullptr）
    {
        Base b; Base* pb=&b;
        long long hit=0;
        auto t0 = std::chrono::high_resolution_clock::now();
        for(long long i=0;i<N;++i){ Derived* q=dynamic_cast<Derived*>(pb); if(!q) ++hit; }
        auto t1 = std::chrono::high_resolution_clock::now();
        std::printf("dynamic_cast fail      : %.3f ns/op   (null=%lld)\n", ns(t1-t0,N), hit);
    }
    return 0;
}
