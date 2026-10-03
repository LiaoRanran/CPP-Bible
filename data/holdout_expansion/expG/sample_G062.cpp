// sample_G062
// defect_type: use_after_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-4658 (https://nvd.nist.gov/vuln/detail/CVE-2016-4658) [libxml2]
// (authoritative annotation in sample_G062.json)
#include <cstdio>
#include <cstring>
// CVE-2016-4658: XPointer range 含 namespace 节点 → 节点释放后复用
struct XmlNode {
    char* name;
    bool  is_namespace;
};

static void xml_free_node(XmlNode* n) {
    delete[] n->name;
    delete n;
}

static XmlNode* g_result_set[8];
static int g_result_n = 0;

static void xptr_add_to_range(XmlNode* node) {
    /* DEFECT */ // 原始缺陷: 未禁止 namespace 节点进入 range
    g_result_set[g_result_n++] = node;
}

int main() {
    XmlNode* ns = new XmlNode{ new char[8], true };
    std::memcpy(ns->name, "xmlns:a", 8);
    xptr_add_to_range(ns);        // namespace 节点进入 range 结果集
    // 解析器清理阶段释放 namespace 节点(但结果集仍持有指针)
    xml_free_node(ns);
    // range 遍历阶段复用已释放节点
    for (int i = 0; i < g_result_n; ++i)
        std::printf("range node: %s\n", g_result_set[i]->name);   // UAF 读
    return 0;
}
