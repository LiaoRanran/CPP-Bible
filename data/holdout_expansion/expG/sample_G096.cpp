// sample_G096
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: open-source-parsers/jsoncpp#1682 (https://github.com/open-source-parsers/jsoncpp/issues/1682) [jsoncpp]
// (authoritative annotation in sample_G096.json)
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
