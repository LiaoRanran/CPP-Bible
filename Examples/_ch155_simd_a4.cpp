// 文件：Examples/_ch155_dep.cpp
// 行号：4
void add_dependent(float* a, int n) {
    for (int i = 1; i < n; ++i)
        a[i] = a[i - 1] + a[i];
}