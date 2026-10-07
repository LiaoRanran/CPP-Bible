// RW-029 | CVE-2022-23308 | libxml2 | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-23308
// project_url: https://gitlab.gnome.org/GNOME/libxml2
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: xmlXPtrRangeToFunction / XML 指针范围求值中对已释放节点再次访问，
//   验证含 XPointer 的文档时触发。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstring>
#include <string>

struct XmlNode {
    std::string name;
    XmlNode* parent;
    XmlNode* sibling;
};

// BUG: range function walks parent chain after the node was unlinked and freed
// (dangling `parent` pointer kept by the range context).
XmlNode* xptr_range_start(XmlNode* cur) {
    XmlNode* p = cur->parent;         // captured before the tree edit ...
    delete cur;                       // ... cur (and edit) frees/mutates the chain
    return p->sibling;                // walks freed neighbourhood
}

int main() {
    XmlNode* root = new XmlNode{"root", nullptr, nullptr};
    XmlNode* child = new XmlNode{"target", root, nullptr};
    root->sibling = child;
    XmlNode* found = xptr_range_start(child);   // use-after-free walk
    std::printf("range start = %p\n", (void*)found);
    delete root;
    return 0;
}
