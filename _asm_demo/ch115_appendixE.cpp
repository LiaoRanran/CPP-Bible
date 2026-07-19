#include <cstring>
#include <cstddef>
#include <utility>

struct Big {
    char* data; size_t sz;
    Big(size_t n): data(new char[n]), sz(n) { std::memset(data, 0, n); }
    [[gnu::noinline]] Big(const Big& o): data(new char[o.sz]), sz(o.sz) { std::memcpy(data, o.data, sz); }
    [[gnu::noinline]] Big(Big&& o) noexcept : data(o.data), sz(o.sz) { o.data=nullptr; o.sz=0; }
    ~Big() { delete[] data; }
};

Big make_big_rvo() { return Big(1024); }                              // ① RVO

[[gnu::noinline]] char use_copy(const Big& src){ Big dst = src; return dst.data[0]; }        // ③ 拷贝构造
[[gnu::noinline]] char use_move(Big& src){ Big dst = std::move(src); return dst.data[0]; }   // ② 移动构造

int main(){ Big a(8); (void)use_copy(a); (void)use_move(a); return 0; }
