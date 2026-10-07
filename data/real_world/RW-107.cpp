// RW-107 | CVE-2023-44487 | HTTP/2 协议栈（nginx/httpd/Go 等） | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-44487
// project_url: https://httpwg.org/specs/rfc9113.html
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: HTTP/2 Rapid Reset —— 客户端立即 RST_STREAM 每个请求流，
//   服务端在“重置-重建”循环中消耗 CPU/内存（协议状态机 DoS）。
// notes: 最小重构（流状态机计数）。C++ 服务器侧防护判定缺失。
#include <cstdio>
#include <cstdint>

struct H2Conn {
    uint32_t active_streams;
    uint32_t reset_count_window;      // resets in the current window
    uint32_t max_concurrent;          // advertised SETTINGS_MAX_CONCURRENT_STREAMS
    bool rapid_reset_guard;           // mitigation flag
};

// BUG: RST_STREAM frees server-side work but the guard threshold (ratio of
// resets to completed streams) is missing -> attacker loops forever cheaply.
bool on_headers(H2Conn& c) {
    if (c.active_streams >= c.max_concurrent + 100) {  // cap itself bypassed by resets
        return false;
    }
    c.active_streams += 1;
    return true;
}

void on_rst_stream(H2Conn& c) {
    if (c.active_streams > 0) c.active_streams -= 1;
    c.reset_count_window += 1;
    if (c.rapid_reset_guard) {
        if (c.reset_count_window > 100) {
            std::printf("guard would terminate connection here\n");
        }
    }
    // BUG: with guard disabled (the vulnerable default) nothing throttles
}

int main() {
    H2Conn c{0, 0, 100, /*rapid_reset_guard=*/false};
    long long server_work = 0;
    for (int i = 0; i < 100000; ++i) {
        if (on_headers(c)) {
            server_work += 100;    // "build response" cost
        }
        on_rst_stream(c);          // client resets immediately; work still burned
    }
    std::printf("server work units burned=%lld with %u resets\n",
                server_work, c.reset_count_window);
    return 0;
}
