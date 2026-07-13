// 见 Examples/_ch149_unity.cpp
// ⑮ 增量/Unity 构建：合并翻译单元减少头解析开销（需确保各 TU 无重名）
#include <cstdio>
void unit_a() { std::printf("unit_a compiled\n"); }
void unit_b() { std::printf("unit_b compiled\n"); }
int main() { unit_a(); unit_b(); std::printf("unity build ok\n"); return 0; }
