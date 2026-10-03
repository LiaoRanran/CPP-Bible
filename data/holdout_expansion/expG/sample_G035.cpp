// sample_G035
// defect_type: use_after_free
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2026-3805 (https://nvd.nist.gov/vuln/detail/CVE-2026-3805) [curl]
// (authoritative annotation in sample_G035.json)
#include <cstdio>
#include <string>
// CVE-2026-3805: SMB 第二次请求使用已释放请求数据的指针 → UAF
struct SmbRequest {
    std::string path;    // 14 字节, SSO: 存储在对象内部
};

struct SmbSession {
    const char* tree;    // 指向 request 内部数据的指针(悬垂来源)
};

static void smb_first_request(SmbSession* s) {
    SmbRequest* r = new SmbRequest;
    r->path = "//server/share";              // SSO: c_str() 指向对象内部
    s->tree = r->path.c_str();
    /* DEFECT */ delete r;                    // 原始缺陷: 请求销毁未清空 s->tree
}

static void smb_second_request(SmbSession* s) {
    std::printf("tree=%s\n", s->tree);        // 第二次请求读已释放内存 → UAF
}

int main() {
    SmbSession s{ 0 };
    smb_first_request(&s);
    smb_second_request(&s);
    return 0;
}
