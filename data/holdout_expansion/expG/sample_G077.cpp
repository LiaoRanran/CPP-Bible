// sample_G077
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2016-5385 (https://nvd.nist.gov/vuln/detail/CVE-2016-5385) [php]
// (authoritative annotation in sample_G077.json)
#include <cstdio>
#include <string>
// CVE-2016-5385 (HTTPoxy): HTTP_PROXY 环境变量被客户端注入并直接信任
static std::string http_get_with_proxy(const std::string& target_host, const std::string& env_http_proxy) {
    /* DEFECT */ // 原始缺陷: 未区分服务器配置的代理与客户端注入的 HTTP_PROXY
    if (!env_http_proxy.empty())
        return "proxy://" + env_http_proxy + " -> " + target_host;
    return "direct://" + target_host;
}

int main() {
    // 攻击者请求头: "Proxy: attacker.example:8080"
    // CGI 按 RFC 3875 把 HTTP 头映射为 HTTP_PROXY 环境变量
    std::string env_http_proxy = "attacker.example:8080";
    std::string result = http_get_with_proxy("api.internal.example", env_http_proxy);
    std::printf("出站请求: %s\n", result.c_str());
    std::printf("(正确行为: 忽略客户端注入的 HTTP_PROXY, 使用直连或服务器配置代理)\n");
    return 0;
}
