// _ch133_vectorize.cpp
// ClickHouse 风格「列存 + 向量化执行」最小等价：对一列浮点批量做 a+b 并累加
// 编译：g++ -std=c++20 -O3 -march=native -S -masm=intel _ch133_vectorize.cpp -o Examples/_ch133_vectorize.asm
#include <cstddef>

// 列批量相加（ClickHouse IColumn 上 executeOnColumn 的标量等价）
void column_add(const float* a, const float* b, float* out, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) {
        out[i] = a[i] + b[i];   // 编译器在此处生成 packed SSE/AVX 指令
    }
}

// 列向量点积式累加（Block 级别一次处理一整块，而非逐行）
float column_dot(const float* a, const float* b, std::size_t n) {
    float s = 0.0f;
    for (std::size_t i = 0; i < n; ++i) {
        s += a[i] * b[i];       // 同一循环体被向量化，FMA/packed mul+add
    }
    return s;
}

int main() {
    constexpr std::size_t N = 1024;
    static float A[N], B[N], C[N];
    for (std::size_t i = 0; i < N; ++i) { A[i] = (float)i; B[i] = (float)(N - i); }
    column_add(A, B, C, N);
    return (int)column_dot(A, B, N);
}
