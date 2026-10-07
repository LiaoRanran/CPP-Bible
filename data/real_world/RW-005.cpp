// RW-005 | CVE-2023-0286 | OpenSSL | defect_type: type_punning
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-0286
// project_url: https://www.openssl.org/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: X.400 地址（ADDRESS 类型）在比较/渲染时被按 GENERAL_NAME 联合体
//   的另一分支解释，类型混淆导致按错误布局读取数据。
// notes: 最小重构。UB 检测（-fsanitize=undefined 或 ASan 栈）应命中。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

enum NameType { GEN_EMAIL = 1, GEN_OTHERNAME = 5, GEN_ADDRESS = 7 };

struct GeneralName {
    int type;
    union {
        struct { char* email; } email_name;
        struct { char* data; int len; } other_name;
        struct { char* address; int addr_len; } address; // X.400
    } u;
};

// BUG: assumes any non-EMAIL name is `other_name` and reads the len field,
// which for ADDRESS misinterprets the layout (type confusion / union misuse).
void render_name(const GeneralName* n) {
    if (n->type == GEN_EMAIL) {
        std::printf("email: %s\n", n->u.email_name.email);
    } else {
        // reads OTHERNAME layout even when type == GEN_ADDRESS
        char* p = n->u.other_name.data;
        int len = n->u.other_name.len;   // for ADDRESS this reads the wrong union member
        std::printf("other: %.*s (len=%d)\n", len > 0 && len < 64 ? len : 0, p, len);
    }
}

int main() {
    GeneralName n{};
    n.type = GEN_ADDRESS;
    n.u.address.address = (char*)"x400-crafted-payload";
    n.u.address.addr_len = 0x40000000; // crafted huge length lands in the union
    render_name(&n);
    return 0;
}
