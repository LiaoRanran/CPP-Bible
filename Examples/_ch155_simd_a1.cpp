// 文件：Examples/_ch155_simd.cpp
// 行号：4
void add_arrays(float* __restrict a, float* __restrict b,
                float* __restrict c, int n) {
    for (int i = 0; i < n; ++i)
        c[i] = a[i] + b[i];
}