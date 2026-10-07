// RW-022 | CVE-2020-8231 | curl | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-8231
// project_url: https://curl.se/
// year: 2020 | severity: MEDIUM | source_type: cve
// mechanism: libcurl 连接复用（connection cache）——某 easy handle 已释放的
//   连接仍被另一 handle 复用，释放后使用。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstring>

struct Connection {
    int sock;
    char server[32];
};

struct EasyHandle {
    Connection* conn;
};

// BUG: caches the connection on the handle, but frees it during cleanup while
// another handle still references the same cache slot.
Connection* conn_cache[4] = {nullptr, nullptr, nullptr, nullptr};

void easy_cleanup(EasyHandle* h) {
    if (h->conn) {
        delete h->conn;                 // connection freed here
        conn_cache[0] = h->conn;        // cache still points at freed node
        h->conn = nullptr;
    }
}

int main() {
    EasyHandle a{}, b{};
    a.conn = new Connection{3, "example.com"};
    std::strcpy(a.conn->server, "example.com");
    conn_cache[0] = a.conn;
    easy_cleanup(&a);

    b.conn = conn_cache[0];             // reuse of freed connection
    std::printf("reused connection to %s (sock=%d)\n", b.conn->server, b.conn->sock);
    return 0;
}
