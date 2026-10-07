// RW-106 | CVE-2021-22947 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-22947
// project_url: https://curl.se/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: STARTTLS 之前的服务器应答被注入到 TLS 阶段（响应注入），
//   前期明文响应伪装成后 TLS 数据。
// notes: 最小重构（协议阶段状态混合）。
#include <cstdio>
#include <string>
#include <vector>

struct MailSession {
    std::vector<std::string> pre_tls_replies;    // collected before STARTTLS
    bool in_tls;
    std::vector<std::string> app_visible;        // what the client app consumes
};

// BUG: replies received before the STARTTLS handshake are appended to the same
// buffer consumed after TLS — injection window.
void feed_reply(MailSession& s, const std::string& line) {
    if (!s.in_tls) {
        s.pre_tls_replies.push_back(line);
        // BUG: also visible to the app layer
        s.app_visible.push_back(line);
        return;
    }
    s.app_visible.push_back(line);
}

void starttls(MailSession& s) {
    s.in_tls = true;
    // BUG: pre-TLS buffer not cleared -> attacker bytes live on into TLS phase
}

int main() {
    MailSession s;
    feed_reply(s, "+OK attacker-injected line");
    starttls(s);
    std::printf("app sees %zu lines; first: %s\n",
                s.app_visible.size(), s.app_visible[0].c_str());
    return 0;
}
