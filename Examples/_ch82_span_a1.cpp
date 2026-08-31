// ⑩-1 被测代码（仅作汇编对照，下方 asm 为其 -O2 产物）
#include <span>
#include <cstddef>

int sum_span(std::span<const int> s) {
    int r = 0;
    for (std::size_t i = 0; i < s.size(); ++i) r += s[i];
    return r;
}

int sum_ptr(const int* p, std::size_t n) {
    int r = 0;
    for (std::size_t i = 0; i < n; ++i) r += p[i];
    return r;
}