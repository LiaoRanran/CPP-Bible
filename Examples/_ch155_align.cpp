// 文件：Examples/_ch155_align.cpp
// 行号：4
// 对齐加载 vs 未对齐加载：_mm_load_ps 要求 16 字节对齐
#include <immintrin.h>
void load_aligned(const float* __restrict a, const float* __restrict b,
                  float* __restrict c) {
    __m128 va = _mm_load_ps(a);   // 假定 a 16 字节对齐
    __m128 vb = _mm_load_ps(b);
    _mm_store_ps(c, _mm_add_ps(va, vb));
}
void load_unaligned(const float* a, const float* b, float* c) {
    __m128 va = _mm_loadu_ps(a);  // 任意对齐均可
    __m128 vb = _mm_loadu_ps(b);
    _mm_storeu_ps(c, _mm_add_ps(va, vb));
}
