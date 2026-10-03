// sample_G099
// defect_type: compiler_warning
// severity: low
// planted: true
// expected_verdict: catch
// expected_detectors: compiler-warn
// source: fmtlib/fmt#3415 (https://github.com/fmtlib/fmt/issues/3415) [fmtlib/fmt]
// (authoritative annotation in sample_G099.json)
#include <cstdio>
#include <string>
#include <utility>
// fmtlib/fmt#3415 (等价重构): map() 返回绑定到临时对象的引用 → -Wdangling-reference
struct ArgMapper {
    const std::string& map(const std::string& s) { return s; }
    const std::string& map(int) { static const std::string empty; return empty; }
};

template <typename T>
void format_value(T&& val) {
    /* DEFECT */ // 镜像 core.h:1674: const auto& arg = arg_mapper<Context>().map(FMT_FORWARD(val));
    const auto& arg = ArgMapper().map(std::forward<T>(val));   // mapper 为临时对象, 告警点
    std::printf("format: %s\n", arg.c_str());
}

int main() {
    std::string s = "hello";
    format_value(s);                      // 左值: mapper().map 返回形参引用(绑定临时, 危险)
    format_value(std::string("temp"));    // 右值: 引用绑定到已析构临时
    return 0;
}
