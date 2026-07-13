// ⑦ SIMD 友好：对已对齐、连续的 float 数组做逐元素运算
// g++ -O2 会自动向量化为 mulps / ymm 指令
void scale(float* __restrict a, const float* __restrict b, int n, float k) {
    for (int i = 0; i < n; ++i)
        a[i] = b[i] * k;
}
