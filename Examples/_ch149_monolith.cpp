// 见 Examples/_ch149_monolith.cpp
// ⑱ 反模式：单翻译单元巨型构建，无法并行、缓存命中低
#include <cstdio>
void module_a() {}
void module_b() {}
void module_c() {}
int main() { module_a(); module_b(); module_c(); std::printf("monolith built\n"); return 0; }
