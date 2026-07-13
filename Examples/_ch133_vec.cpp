// 文件：Examples/_ch133_vec.cpp
// 行号：1
// 自包含示例：模拟 ClickHouse 的「向量化列批处理」。
// 对一列 uint64_t 做范围谓词 + 累加（filter + aggregate），
// 编译器在 -O2 下将其自动向量化为 SIMD 指令。

#include <cstdint>
#include <cstddef>

// 列批处理：src 长度为 n 的列，dst 输出过滤后的值，
// 返回通过谓词的元素个数，并把通过的值求和写入 *sum。
extern "C" std::size_t column_filter_sum(
    const uint64_t* src, std::size_t n,
    uint64_t lo, uint64_t hi,
    uint64_t* dst, uint64_t* sum)
{
    std::size_t k = 0;
    uint64_t acc = 0;
    for (std::size_t i = 0; i < n; ++i) {
        uint64_t v = src[i];          // ① 连续内存批量读取（列存友好）
        if (v >= lo && v < hi) {      // ② 谓词（向量化比较）
            dst[k++] = v;
            acc += v;                 // ③ 聚合
        }
    }
    *sum = acc;
    return k;
}

// 向量化 transform：dst[i] = src[i] * 3 + 1（典型列表达式求值）
extern "C" void column_transform(
    const uint64_t* src, uint64_t* dst, std::size_t n)
{
    for (std::size_t i = 0; i < n; ++i)
        dst[i] = src[i] * 3u + 1u;
}

#include <cstdio>
int main() {
    uint64_t src[8] = {10, 20, 30, 40, 50, 60, 70, 80};
    uint64_t dst[8], sum = 0;
    std::size_t k = column_filter_sum(src, 8, 25, 75, dst, &sum);
    printf("k=%zu sum=%llu\n", (unsigned long long)k, (unsigned long long)sum);
    uint64_t out[8];
    column_transform(src, out, 8);
    for (int i = 0; i < 8; ++i) printf("%llu ", (unsigned long long)out[i]);
    printf("\n");
    return (int)k;
}
