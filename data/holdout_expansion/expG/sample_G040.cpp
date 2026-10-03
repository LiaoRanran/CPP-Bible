// sample_G040
// defect_type: logic_error
// severity: low
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2021-22876 (https://nvd.nist.gov/vuln/detail/CVE-2021-22876) [curl]
// (authoritative annotation in sample_G040.json)
#include <cstdio>
#include <string>
// CVE-2021-22876: 自动 Referer 不剥离 URL 凭据 → 信息泄露
static std::string build_referer(const std::string& url) {
    /* DEFECT */ // 原始缺陷: 直接取 scheme:// 之后整段, 未剥离 user:password@
    size_t scheme_end = url.find("://");
    return url.substr(0, scheme_end + 3) + url.substr(scheme_end + 3, url.find('/', scheme_end + 3) - scheme_end - 3) + "/";
}

int main() {
    // 受害者使用带凭据的 URL 访问, 跳转到第三方页面
    std::string url = "https://alice:hunter2@internal.example.com/secret/page";
    std::string referer = build_referer(url);
    std::printf("Referer: %s\n", referer.c_str());
    std::printf("(正确行为: Referer 不应包含 alice:hunter2)\n");
    return 0;
}
