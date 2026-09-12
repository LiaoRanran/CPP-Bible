// ATOM-LANG-INLINE-001 夹具 · main（只做观测与打印，不含任何期望值字面量）
//
// 可选 argv[1] 作为输出前缀：使**同一次实验的多次运行**（不同链接顺序 / 不同优化档）
// 能在同一份 `.out` 留痕里各自成 key，从而把"顺序依赖"变成机器可断言的读数。
//   例：`./exe ab_` → `ab_tu_a=1`；`./exe ba_` → `ba_tu_a=2`
#include <cstdio>

int tu_a_value();
int tu_b_value();
int tu_a_stable();
int tu_b_stable();

int main(int argc, char** argv) {
    const char* p = (argc > 1) ? argv[1] : "";
    std::printf("%stu_a=%d\n", p, tu_a_value());
    std::printf("%stu_b=%d\n", p, tu_b_value());
    std::printf("%sstable_a=%d\n", p, tu_a_stable());
    std::printf("%sstable_b=%d\n", p, tu_b_stable());
    return 0;
}
