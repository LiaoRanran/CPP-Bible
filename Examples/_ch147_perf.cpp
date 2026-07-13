// _ch147_perf.cpp —— 性能回归审查：意外拷贝 vs 引用
#include <string>
#include <vector>

struct Record { std::string key; int val; };

// 坏味道：按值传递大对象
int bad_lookup(std::vector<Record> db, const std::string& k) {
    for (auto& r : db)
        if (r.key == k) return r.val;
    return -1;
}

// 好味道：const 引用 + 范围 for 引用
int good_lookup(const std::vector<Record>& db, const std::string& k) {
    for (const auto& r : db)
        if (r.key == k) return r.val;
    return -1;
}
