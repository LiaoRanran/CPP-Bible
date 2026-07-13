// _ch148_precommit_lint.cpp
// 一个最小可运行的 pre-commit C++ 检查器：拒绝含制表符/Trailing 空格/CRLF 的源码。
// 用法：在 .git/hooks/pre-commit 中调用本程序，对 `git diff --cached --name-only` 的文件检查。
// 编译：g++ -std=c++23 -O2 _ch148_precommit_lint.cpp -o _ch148_precommit_lint
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>

static int check_file(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) return 0;  // 删除的文件跳过
    std::string line;
    int bad = 0;
    while (std::getline(in, line)) {
        if (!line.empty() && (line.back() == '\r')) {            // CRLF
            std::fprintf(stderr, "[FAIL] %s : CRLF 行尾\n", path.c_str());
            ++bad;
        }
        // 去掉可能的 \r 后检查 trailing 空格 / 制表符
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!line.empty() && (line.back() == ' ' || line.back() == '\t')) {
            std::fprintf(stderr, "[FAIL] %s : 行尾空白\n", path.c_str());
            ++bad;
        }
        for (char c : line) {
            if (c == '\t') {
                std::fprintf(stderr, "[FAIL] %s : 含制表符\n", path.c_str());
                ++bad;
                break;
            }
        }
    }
    return bad;
}

int main(int argc, char** argv) {
    int total = 0;
    for (int i = 1; i < argc; ++i) total += check_file(argv[i]);
    if (total) {
        std::fprintf(stderr, "pre-commit: 发现 %d 处问题，已拒绝提交。\n", total);
        return 1;  // 非零退出 -> 阻止提交
    }
    return 0;
}
