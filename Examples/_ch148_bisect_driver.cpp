// _ch148_bisect_driver.cpp
// bisect 实证用的「被测程序」：answer() 应恒为 42。
// 坏提交将其改为 0，`git bisect run ./check.sh` 据此二分定位首坏提交。
// 编译：g++ -std=c++23 -O2 _ch148_bisect_driver.cpp -o _ch148_bisect_driver
#include <cstdio>

const int ANSWER = 42;          // 坏提交会把这行改为 0（见 ch148 实证仓库）
int answer() { return ANSWER; }

int main() {
    std::printf("%d\n", answer());
    return 0;
}
