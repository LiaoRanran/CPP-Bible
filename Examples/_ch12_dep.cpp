// ⑨ 文件：Examples/_ch12_dep.cpp，行号：1
// -MMD 演示：此 TU 包含 _ch12_dep.h，生成的 .d 会记录该依赖
#include "_ch12_dep.h"

namespace ch12 {
    int add(int a, int b) { return a + b; }
}
