#include <cstdio>
enum class Backend { CPU, GPU };
template <Backend B>
void compute() {
    if constexpr (B == Backend::CPU) { std::puts("cpu"); }
    else { std::puts("gpu"); }
}
int main(){ compute<Backend::CPU>(); compute<Backend::GPU>(); return 0; }
