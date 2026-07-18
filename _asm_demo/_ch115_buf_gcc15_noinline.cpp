#include <utility>
#include <cstddef>
#include <iostream>
struct Buf {
    int* p; std::size_t n;
    Buf() : p(nullptr), n(0) {}
    Buf(Buf&& o) noexcept : p(o.p), n(o.n) { o.p = nullptr; o.n = 0; }
    Buf(const Buf& o) : p(o.p ? new int[o.n] : nullptr), n(o.n) { if(p) for(std::size_t i=0;i<n;++i) p[i]=o.p[i]; }
    [[gnu::noinline]] Buf& operator=(Buf&& o) noexcept { if(this!=&o){ delete[] p; p=o.p; n=o.n; o.p=nullptr; o.n=0;} return *this; }
    [[gnu::noinline]] Buf& operator=(const Buf& o) { if(this!=&o){ delete[] p; p=o.p?new int[o.n]:nullptr; n=o.n; if(p) for(std::size_t i=0;i<n;++i) p[i]=o.p[i]; } return *this; }
    ~Buf() { delete[] p; }
};
int main() {
    Buf a, b, c;
    b = std::move(a);   // 移动赋值
    c = b;              // 拷贝赋值
    std::cout << c.n << '\n';
    return 0;
}
