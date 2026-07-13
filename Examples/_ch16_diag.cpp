// 演示：g++ -Wall -Wconversion 真实诊断（未用变量 + 收窄转换）
#include <vector>
int compute(int n) {
    std::vector<int> v(n, 1);
    int total = 0;
    for (int x : v) total += x;
    int unused = 42;          // 触发 -Wunused-variable
    int d = total / 3.0;       // 触发 -Wconversion（double -> int 收窄）
    return d;
}
int main() { return compute(4); }
