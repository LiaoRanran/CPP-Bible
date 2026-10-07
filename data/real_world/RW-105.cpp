// RW-105 | CVE-2023-27536 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-27536
// project_url: https://curl.se/
// year: 2023 | severity: LOW | source_type: cve
// mechanism: GSSAPI 委托（delegation）标志在连接复用间保留，前一次请求的
//   凭据被复用到后续请求（凭据泄露）。
// notes: 最小重构（连接复用状态泄漏）。
#include <cstdio>
#include <string>

struct GssConn {
    bool delegate;              // GSSAPI delegation enabled for this attempt
    std::string principal;      // credential principal in use
};

struct ConnCache {
    GssConn* cached;            // reused connection keeps its old auth state
};

// BUG: the delegate flag is not reset when the connection is pulled from the
// cache for a *different* request.
void reuse_connection(ConnCache& cache, bool request_wants_delegate,
                      const std::string& new_principal) {
    if (cache.cached) {
        // BUG: cache.cached->delegate keeps its previous value
        std::printf("reused conn: delegate=%s (requested %s), principal=%s\n",
                    cache.cached->delegate ? "true" : "false",
                    request_wants_delegate ? "true" : "false",
                    cache.cached->principal.c_str());
        return;
    }
    cache.cached = new GssConn{request_wants_delegate, new_principal};
}

int main() {
    ConnCache cache{nullptr};
    reuse_connection(cache, true, "svc-delegated@REALM");    // first: delegation on
    reuse_connection(cache, false, "user@OTHER");            // second: still on (bug)
    delete cache.cached;
    return 0;
}
