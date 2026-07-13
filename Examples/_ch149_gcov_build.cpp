// 见 Examples/_ch149_gcov_build.cpp
// ⑧ 覆盖率插桩构建产物：配合 --coverage 旗标生成 .gcno/.gcda
#include <cstdio>
int square(int x) { return x * x; }
int cube(int x)   { return x * x * x; }
int main() {
    std::printf("square(5)=%d cube(3)=%d\n", square(5), cube(3));
    return 0;
}
