// Phase 4.5 实证：std::expected 跨优化等级代码生成对比（嵌入式视角）
//
// 编译（GCC 15.3.0, MinGW-w64 x86_64-msvcrt）：
//   g++ -std=c++26 -O0 -c ch08_opt_expected.cpp -o o0.o
//   g++ -std=c++26 -O2 -c ch08_opt_expected.cpp -o o2.o
//   g++ -std=c++26 -Os -c ch08_opt_expected.cpp -o os.o
//   objdump -d -M intel -C o0.o | sed -n '/<parse_digit>/,/ret/p'
//
// 关键手法：[[gnu::noinline]] 强制 parse_digit 独立成符号，
// 使 -O0 / -O2 / -Os 对比的是"同一个函数"的代码生成，而非被内联后的差异。
//
// 嵌入式关切：MCU 固件普遍用 -Os 以压缩 flash 占用，
// 本实证回答"零开销抽象在 -Os 下是否仍零开销"。
#include <expected>

// 解析单个十六进制字符，返回 expected<int, const char*>
[[gnu::noinline]]
std::expected<int, const char*> parse_digit(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return std::unexpected<const char*>("not a hex digit");
}

[[gnu::noinline]]
int use(char c) {
    auto r = parse_digit(c);
    return r.value_or(-1);
}

int main() { return use('A'); }
