// sample_G053
// defect_type: use_after_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2020-11656 (https://nvd.nist.gov/vuln/detail/CVE-2020-11656) [sqlite]
// (authoritative annotation in sample_G053.json)
#include <cstdio>
#include <cstring>
// CVE-2020-11656: ALTER TABLE token 释放后仍被引用 → UAF
struct Token {
    char* z;   // 词法单元内容
    int   n;
};

static void token_free(Token* t) {
    delete[] t->z;
    /* DEFECT */ // 原始缺陷: 释放后 t->z 未置空, 错误路径仍引用
}

static char* alter_rename_error_message(const Token* t) {
    char* msg = new char[64];
    /* DEFECT */ std::snprintf(msg, 64, "rename failed near: %.*s", t->n, t->z);   // 读已释放内存
    return msg;
}

int main() {
    Token t;
    t.n = 11;
    t.z = new char[12];
    std::memcpy(t.z, "ORDER BY x", 12);
    token_free(&t);                                  // compound SELECT 的 ORDER BY token 被释放
    char* msg = alter_rename_error_message(&t);      // 错误消息仍引用 → UAF
    std::printf("%s\n", msg);
    delete[] msg;
    return 0;
}
