# -*- coding: utf-8 -*-
# 676c-G spec part18: GitHub issue 组 II (tinyxml2/jsoncpp/fmt, G098-G102)
PART = [
("G098", dict(
  defect_type="logic_error", func="XMLQueryUnsignedAttribute", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="github_issue", id="leethomason/tinyxml2#728", url="https://github.com/leethomason/tinyxml2/issues/728",
           project="tinyxml2", commit="", simplification="剥离 XML 解析层，按 issue 报告的确切行为（输入 10000000000 → 返回 1410065408 而非错误/饱和）镜像无溢出检查的无符号解析"),
  trigger="QueryUnsignedAttribute 解析 10000000000（超过 uint32 范围）→ 静默截断为 1410065408",
  notes="tinyxml2#728（未修复）: QueryUnsignedAttribute 对超过 uint32 范围的输入静默截断（10000000000 → 1410065408），未报错也未饱和到 UINT32_MAX。逻辑缺陷，正确=报错/饱和、实际=截断 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstdlib>
// tinyxml2#728: QueryUnsignedAttribute 溢出静默截断
static bool query_unsigned_attribute(const char* value, unsigned* out) {
    char* end = 0;
    /* DEFECT */ // 原始缺陷: strtoul 之后直接截断为 unsigned, 无范围检查
    unsigned long v = std::strtoul(value, &end, 10);
    if (end == value) return false;      // 只检查"不是数字"
    *out = (unsigned)v;                  // 10000000000 → 1410065408 (静默截断)
    return true;
}

int main() {
    // issue 中的确切输入: 10 000 000 000 (hex 0x2_540B_E400)
    unsigned parsed = 0;
    bool ok = query_unsigned_attribute("10000000000", &parsed);
    std::printf("ok=%d parsed=%u (期望: 报错或 4294967295, 实际: 1410065408)\n",
                (int)ok, parsed);
    return 0;
}
'''),

("G099", dict(
  defect_type="heap_overread", func="getLocationLineAndColumn", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="open-source-parsers/jsoncpp#1682", url="https://github.com/open-source-parsers/jsoncpp/issues/1682",
           project="jsoncpp", commit="", simplification="剥离 jsoncpp Reader 全流程，按 issue『Root Cause』一节引用的 getLocationLineAndColumn 循环直接镜像（CR 为最后一个字节时无条件 peek *current）"),
  trigger="输入以单个 CR(0x0d) 结尾且产生解析错误：错误定位循环在 current==end_ 后仍读 *current",
  notes="jsoncpp#1682（已修复）: getLocationLineAndColumn 对 CR 结尾输入堆越界读 1 字节（issue 附 json_reader.cpp:1820-1840 根因代码：CR 分支 current++ 后未重测 current != end_ 即 peek）。",
), r'''
#include <cstdio>
#include <cstring>
// jsoncpp#1682: getLocationLineAndColumn CR 结尾 → 越界读 1 字节
static void getLocationLineAndColumn(const char* location, const char* begin_, const char* end_,
                                     int& line, int& column) {
    const char* p = begin_;
    line = 1;
    column = 1;
    while (p < location && p != end_) {
        if (*p == '\r') {
            ++p;
            /* DEFECT */ if (*p == '\n')   // 原始缺陷: 未重测 p != end_, CR 是最后一字节时读越界
                ++p;
            ++line;
            column = 1;
        } else if (*p == '\n') {
            ++p;
            ++line;
            column = 1;
        } else {
            ++p;
            ++column;
        }
    }
}

int main() {
    // crafted 输入(issue 的最小触发): 堆上 1 字节 CR, 解析错误 token 指向它
    char* doc = new char[1]{ '\r' };
    const char* begin_ = doc;
    const char* end_ = doc + 1;
    int line = 0, column = 0;
    getLocationLineAndColumn(end_, begin_, end_, line, column);   // location==end(CR 之后)
    std::printf("line=%d column=%d\n", line, column);
    delete[] doc;
    return 0;
}
'''),

("G100", dict(
  defect_type="use_after_free", func="Reader_getFormattedErrorMessages", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="github_issue", id="open-source-parsers/jsoncpp#1623", url="https://github.com/open-source-parsers/jsoncpp/issues/1623",
           project="jsoncpp", commit="", simplification="按 issue 中的 POC 代码直接镜像（Reader::parse 保存指向输入串的指针，输入串析构后 getFormattedErrorMessages 读回）"),
  trigger="parse 失败保存指向 doc 的 token 指针，doc 析构后 getFormattedErrorMessages 读已释放内存",
  notes="jsoncpp#1623（已修复）: Reader::parse 保存悬垂指针，getFormattedErrorMessages 触发 UAF（issue 附完整 POC testcase.cpp 与复现 commit ca98c98）。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
// jsoncpp#1623: parse 保存指向输入串的 token 指针 → 输入串析构后 UAF
struct JsonReader {
    const char* error_token_begin;   // parse 失败时保存(指向输入缓冲)
    int         error_token_len;
    bool        ok;

    bool parse(const char* begin, const char* end) {
        // 镜像 POC: 解析失败(非法 JSON), 记录错误 token 位置
        ok = false;
        error_token_begin = begin + 2;      /* DEFECT */ // 指向调用方缓冲
        error_token_len = (int)(end - begin);
        return false;
    }
    std::string getFormattedErrorMessages() const {
        /* DEFECT */ return "parse error near: " + std::string(error_token_begin,
                                              (size_t)error_token_len > 8 ? 8 : (size_t)error_token_len);
    }
};

int main() {
    JsonReader reader;
    {
        std::string doc = "{\n  \"a\": 1,\n  trailing\n}";   // 非法 JSON → 产生错误
        reader.parse(doc.data(), doc.data() + doc.size());
    }   // doc 析构 → reader 内的 token 指针悬垂
    std::printf("%s\n", reader.getFormattedErrorMessages().c_str());   // UAF 读
    return 0;
}
'''),

("G101", dict(
  defect_type="logic_error", func="value_as_uint64", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="github_issue", id="open-source-parsers/jsoncpp#1545", url="https://github.com/open-source-parsers/jsoncpp/issues/1545",
           project="jsoncpp", commit="", simplification="按 issue 报告的确切行为（[2^64, 2^64+2^11] 范围返回 0 而非抛异常）镜像经 double 转换的 uint64 解析路径"),
  trigger="解析 18446744073709551616 (2^64)：double 往返精度丢失 + 越界 float→uint64 转换（x86 硬件产生不定值）",
  notes="jsoncpp#1545（已修复）: [2^64, 2^64+2^11] 的数字经 double 往返静默返回错误值而非抛异常（issue 附完整复现代码与修复 PR #1519）。底层是 float→uint64 越界转换 UB，但 GCC/Clang 默认 -fsanitize=undefined **不包含** float-cast-overflow → 检测器无报告。这是真实的检测器盲区（浮点转换检查未启用），诚实标 miss。",
), r'''
#include <cstdio>
#include <cstdint>
#include <stdexcept>
// jsoncpp#1545: uint64 解析经 double 往返 → [2^64, 2^64+2^11] 静默归 0
static uint64_t value_as_uint64(const char* digits) {
    /* DEFECT */ // 原始缺陷: 值先转 double, 大整数精度丢失后再转回 uint64
    double d = 0.0;
    for (const char* p = digits; *p; ++p)
        d = d * 10.0 + (*p - '0');
    if (d > 1.8446744073709552e19 + 2048.0)     // 超过 2^64+2^11 才报错(issue 描述的边界)
        throw std::runtime_error("double out of UInt64 range");
    return (uint64_t)d;                          // 2^64+1 → double 舍入为 2^64 → 截断为 0
}

int main() {
    try {
        // issue 中的确切输入: 18446744073709551616 = 2^64 (max+1) → 期望报错, 实际返回 0
        uint64_t v = value_as_uint64("18446744073709551616");
        std::printf("parsed=%llu (期望: 抛异常, 实际: %llu)\n",
                    (unsigned long long)v, (unsigned long long)v);
    } catch (const std::exception& e) {
        std::printf("exception: %s\n", e.what());
    }
    return 0;
}
'''),

("G102", dict(
  defect_type="compiler_warning", func="format_value_map", severity="low", planted=True,
  verdict="catch", detectors=["compiler-warn"],
  src=dict(type="github_issue", id="fmtlib/fmt#3415", url="https://github.com/fmtlib/fmt/issues/3415",
           project="fmtlib/fmt", commit="", simplification="剥离 fmt 库依赖，按 issue 引用的 core.h:1674 模式（const auto& arg = mapper().map(FMT_FORWARD(val)) 对临时对象的悬垂引用告警）以等价调用结构重构，故标 planted=true"),
  trigger="map() 以右值引用返回绑定到临时对象的引用 → g++13 -Wall 触发 -Wdangling-reference",
  notes="fmtlib/fmt#3415（已修复）: fmt::v9 core.h:1674 的 arg_mapper().map() 模式在 gcc 13.1 -Wall 下触发 -Wdangling-reference（issue 附 godbolt 复现）。本样本以等价调用模式复现该告警。",
), r'''
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
'''),
]
