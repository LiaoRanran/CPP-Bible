// 文件：Examples/_ch155_simd.cpp
// 行号：4
// 可向量化的逐元素加法：连续访问、无循环依赖、无分支
void add_arrays(float* __restrict a, float* __restrict b,
                float* __restrict c, int n) {
    for (int i = 0; i < n; ++i)
        c[i] = a[i] + b[i];
}
