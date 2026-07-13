// 文件：Examples/_ch155_avx512.cpp
// 行号：4
// 同一逐元素加法，但用 -mavx512f 编译 -> zmm 512 位寄存器
void add_arrays512(float* __restrict a, float* __restrict b,
                   float* __restrict c, int n) {
    for (int i = 0; i < n; ++i)
        c[i] = a[i] + b[i];
}
