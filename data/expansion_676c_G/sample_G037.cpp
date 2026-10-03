// sample_G037
// defect_type: heap_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-16839 (https://nvd.nist.gov/vuln/detail/CVE-2018-16839) [curl]
// (authoritative annotation in sample_G037.json)
#include <cstdio>
#include <cstring>
// CVE-2018-16839: SASL 响应长度 int 溢出 → 小分配 + 大写入
static char* sasl_build_login_response(int userlen, int authzlen) {
    /* DEFECT */ int total = userlen + authzlen + 32;   // 原始缺陷: int 溢出
    char* resp = new char[total > 0 ? total : 1];       // 溢出后分配 1 字节
    size_t real = (size_t)userlen + (size_t)authzlen + 32;
    std::memset(resp, 'A', real);                       // 按真实需求写入 → 堆越界写
    return resp;
}

int main() {
    // crafted 超长用户名/授权 ID(运行时变量绕过常量折叠)
    volatile int ul = 0x40000000, al = 0x40000000;
    char* r = sasl_build_login_response(ul, al);
    std::printf("resp[0]=%c\n", r[0]);
    delete[] r;
    return 0;
}
