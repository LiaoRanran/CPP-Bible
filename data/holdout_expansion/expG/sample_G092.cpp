// sample_G092
// defect_type: heap_overread
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: nlohmann/json#575 (https://github.com/nlohmann/json/issues/575) [nlohmann/json]
// (authoritative annotation in sample_G092.json)
#include <cstdio>
#include <cstring>
// nlohmann/json#575 (等价重构): 字符串解析越过输入末尾 → 堆越界读
static void json_parse_string(const char* cur, const char* end) {
    if (*cur != '\"') return;
    ++cur;
    /* DEFECT */ while (*cur && *cur != '\"') ++cur;   // 原始缺陷: 未检查 cur < end
    ++cur;                                             // READ 2: 再读闭合引号之后 1 字节
    std::printf("string parsed len=%ld\n", (long)(cur - end));
}

int main() {
    // crafted JSON 输入(OSS-Fuzz 用例结构): 4 字节堆缓冲, 引号未闭合
    char* in = new char[4]{ '\"', 'a', 'b', 'c' };
    json_parse_string(in, in + 4);
    delete[] in;
    return 0;
}
