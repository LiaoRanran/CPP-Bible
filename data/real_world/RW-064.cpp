// RW-064 | CVE-2023-5868 | PostgreSQL | defect_type: memory_leak
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-5868
// project_url: https://www.postgresql.org/
// year: 2023 | severity: MEDIUM | source_type: cve
// mechanism: aggregate 函数（如某些 JSON/数组聚合）内存上下文计算错误，
//   重复调用持续泄露（DoS 面）。
// notes: 最小重构。LeakSanitizer 应报 "detected memory leaks"。
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: per-call scratch buffer allocated in a context that never resets, so
// every aggregate transition leaks (real shape: wrong memory context selected).
std::vector<char*> g_ctx_leaks;

void agg_transition(const char* value) {
    char* scratch = new char[256];            // allocated in the "per-tuple" ctx
    std::strncpy(scratch, value, 255);
    scratch[255] = '\0';
    // BUG: never freed / wrong context: pointer only kept in a debug list
    g_ctx_leaks.push_back(scratch);
}

int main() {
    for (int i = 0; i < 64; ++i) {
        agg_transition("aggregate-input");    // 64 x 256 bytes leaked
    }
    std::printf("aggregate processed %zu groups (leaked)\n", g_ctx_leaks.size());
    return 0;
}
