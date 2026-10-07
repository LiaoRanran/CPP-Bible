// RW-069 | CVE-2012-2677 | Boost | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2012-2677
// project_url: https://www.boost.org/
// year: 2012 | severity: MEDIUM | source_type: cve
// mechanism: Boost.pool ordered_malloc 的块数×块大小乘积整数溢出，
//   分配远小于请求的内存（堆越界写）。
// notes: 最小重构。UBSan + ASan 命中。
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: n * partition_size computed in size_t with crafted huge n from user input.
void* ordered_malloc_overflow(size_t n, size_t partition_size) {
    size_t bytes = n * partition_size;                 // wraps for huge n
    void* p = std::malloc(bytes);
    if (!p) return nullptr;
    std::memset(p, 0xAB, n > 64 ? 64 : n);             // writes "logical" amount
    return p;
}

int main() {
    // crafted: n = SIZE_MAX/8 + 1 with partition_size 16 -> wraps to small
    size_t n = (SIZE_MAX / 16) + 1;
    void* p = ordered_malloc_overflow(n, 16);
    std::printf("pool block = %p (requested %zu x 16)\n", p, n);
    std::free(p);
    return 0;
}
