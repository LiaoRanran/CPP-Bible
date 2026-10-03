// sample_G063
// defect_type: stack_overflow_write
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2017-9047 (https://nvd.nist.gov/vuln/detail/CVE-2017-9047) [libxml2]
// (authoritative annotation in sample_G063.json)
#include <cstdio>
#include <cstring>
// CVE-2017-9047: xmlSnprintfElementContent 第二次追加未收缩可用空间
struct ElementContent {
    const char*     name;
    ElementContent* child;
};

static void xmlSnprintfElementContent(char* buf, size_t size, const ElementContent* content, int depth) {
    if (!content) return;
    size_t len = std::strlen(buf);
    if (depth > 0) {
        std::snprintf(buf + len, size, ", ");
        len = std::strlen(buf);
    }
    std::snprintf(buf + len, size - len, "%s", content->name);
    if (content->child) {
        len = std::strlen(buf);
        /* DEFECT */ // 原始缺陷: 递归子内容时 size 未按 len 收缩, 直接用原 size
        std::snprintf(buf + len, size, " includes %s", content->child->name);
    }
}

int main() {
    char buf[64];                       // 原始代码的 buf/size
    buf[0] = '\0';
    ElementContent child{ "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 0 };   // 60 字节
    ElementContent parent{ "elem", &child };
    xmlSnprintfElementContent(buf, sizeof(buf), &parent, 0);
    std::printf("content=%s\n", buf);
    return 0;
}
