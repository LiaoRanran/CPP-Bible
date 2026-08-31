#include <chrono>
#include <iostream>
#include <stdexcept>

static long long sink = 0;
int compute_ec(int x, int& out){ if(x==0) return -1; out=x*2; return 0; }
int compute_ex(int x){ if(x==0) throw std::runtime_error("zero"); return x*2; }

int main(){
    const int N = 10'000'000;
    auto t0 = std::chrono::steady_clock::now();
    long long s = 0;
    for (int i=0;i<N;++i){ int o; if(compute_ec(i+1,o)==0) s+=o;
        asm volatile("" : "+r"(s) :: "memory"); }   // 阻止编译器把等差数列求和闭式化(DCE)
    auto t1 = std::chrono::steady_clock::now();
    sink += s;
    std::cout << "error-code success: " << (t1-t0).count()/1e6 << " ms" << std::endl;
    return 0;
}