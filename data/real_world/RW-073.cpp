// RW-073 | CVE-2022-3432 | Godot Engine | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-3432
// project_url: https://godotengine.org/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: 资源加载器对同一资源对象释放后仍被引用（编辑器加载特制资源时
//   释放后使用）。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstring>
#include <unordered_map>

struct Resource {
    int rid;
    char path[32];
    int refs;
};

std::unordered_map<int, Resource*> g_cache;

Resource* load_resource(int rid, const char* path) {
    auto it = g_cache.find(rid);
    if (it != g_cache.end()) return it->second;
    Resource* r = new Resource{rid, {0}, 1};
    std::strncpy(r->path, path, 31);
    g_cache[rid] = r;
    return r;
}

void unload_resource(int rid) {
    auto it = g_cache.find(rid);
    if (it != g_cache.end()) {
        delete it->second;
        it->second = nullptr;      // BUG: entry kept (null) while other holders
                                   // still point at the freed Resource
    }
}

int main() {
    Resource* r = load_resource(7, "res://crafted.tres");
    Resource* holder = r;          // another subsystem grabbed the pointer
    unload_resource(7);            // freed
    holder->refs += 1;             // use-after-free write
    std::printf("holder touched freed resource rid=%d\n", holder->rid);
    return 0;
}
