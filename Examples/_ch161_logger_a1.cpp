// D5.3 可复现 demo — ch161 日志库
// 演示：std::format 与 ostringstream 生成相同文本（语义等价）；
//       批量写 N 行到临时文件，行数必须与 N 一致。正确性断言（非时间/倍数）。
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <format>
#include <fstream>
#include <sstream>
#include <string>

int main() {
    int id = 42;
    std::string a = std::format("id={} extra={}", id, id * 2);
    std::ostringstream os;
    os << "id=" << id << " extra=" << (id * 2);
    assert(a == os.str());                 // 两种格式化方式文本等价

    const int N = 1000;
    std::string buf;
    buf.reserve((size_t)N * 32);
    for (int i = 0; i < N; ++i) buf += std::format("line {}\n", i);

    const char* tmp = "_bench_tmp_demo161.log";
    { std::ofstream ofs(tmp, std::ios::trunc); ofs << buf; }
    long lines = 0;
    { std::ifstream f(tmp); char c; while (f.get(c)) if (c == '\n') ++lines; }  // 离开作用域即关闭，避免 Windows 下删除失败
    assert(lines == N);                    // 批量写行数正确
    std::remove(tmp);                      // 清理临时文件
    std::printf("demo ch161: format==ostringstream: %s, lines=%ld OK\n", a.c_str(), lines);
    return 0;
}