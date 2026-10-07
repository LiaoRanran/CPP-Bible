// RW-024 | CVE-2019-20372 | nginx | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2019-20372
// project_url: https://nginx.org/
// year: 2020 | severity: MEDIUM | source_type: cve
// mechanism: error_page 指向外部重定向时，未消费的请求体与请求行状态导致
//   请求走私（前后端解析不一致）。
// notes: 最小重构。逻辑缺陷类（HTTP 解析状态机）。
#include <cstdio>
#include <cstring>
#include <string>

struct HttpReq {
    std::string method;
    std::string target;
    bool had_body;
    long content_length;
};

// BUG: on the error_page redirect path, the request body is left unconsumed,
// so it is interpreted as the *next* request on the kept-alive connection.
std::string handle_error_page(HttpReq& req) {
    if (req.target == "/protected") {
        // e.g. 302 to /login: response sent, but body not drained
        return "HTTP/1.1 302 Found\r\nLocation: /login\r\n\r\n";
    }
    return "200 OK\r\n\r\n";
}

int main() {
    HttpReq req{"POST", "/protected", true, 18};
    std::string resp = handle_error_page(req);
    // kept-alive connection now starts at attacker bytes that frontend treats
    // as body but backend treats as the next request line ("smuggling").
    std::printf("%s", resp.c_str());
    std::printf("[leftover body interpreted as next request: %s]\n",
                req.had_body ? "GET /admin HTTP/1.1" : "(none)");
    return 0;
}
