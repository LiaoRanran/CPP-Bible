// 文件：Examples/_ch155_dep.cpp
// 行号：4
// 带循环携带依赖：a[i] 依赖 a[i-1]，无法向量化 -> 标量
void add_dependent(float* a, int n) {
    for (int i = 1; i < n; ++i)
        a[i] = a[i - 1] + a[i];
}
