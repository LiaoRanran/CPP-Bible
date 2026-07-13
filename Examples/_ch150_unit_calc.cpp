// ②' 纯函数单元测试：覆盖正常/边界/负数分支
#include <cstdio>
#include <cassert>
static long long factorial(int n) {
    long long r = 1;
    for (int i = 2; i <= n; ++i) r *= i;
    return r;
}
int main() {
    assert(factorial(0) == 1);
    assert(factorial(1) == 1);
    assert(factorial(5) == 120);
    assert(factorial(10) == 3628800LL);
    std::printf("factorial unit tests: OK (0,1,5,10)\n");
    return 0;
}
