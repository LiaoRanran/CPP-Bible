// sample_G097
// defect_type: use_after_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: open-source-parsers/jsoncpp#1623 (https://github.com/open-source-parsers/jsoncpp/issues/1623) [jsoncpp]
// (authoritative annotation in sample_G097.json)
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
