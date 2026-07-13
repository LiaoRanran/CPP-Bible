// ⑬ 文件：Examples/_ch12_unity.cpp，行号：1
// Unity build：把多个 TU 合并为单个翻译单元，减少头重复解析
#include "_ch12_part.h"
namespace ch12 {
    int compute_a(int x) { return x + 1; }
    int compute_b(int x) { return x * 2; }
}
