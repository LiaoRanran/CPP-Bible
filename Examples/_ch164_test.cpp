// ⑫ 测试钩子：框架内置最小测试运行器（关联 第150章 测试）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <vector>
#include <functional>

struct TestCase { std::string name; std::function<bool()> body; };
struct TestRunner {
    std::vector<TestCase> cases;
    void add(const std::string& n, std::function<bool()> b) { cases.push_back({n, std::move(b)}); }
    int run() {
        int fail = 0;
        for (auto& c : cases) {
            bool ok = c.body();
            std::cout << (ok ? "[test] PASS " : "[test] FAIL ") << c.name << "\n";
            if (!ok) ++fail;
        }
        std::cout << "[test] summary: " << cases.size() - fail << "/" << cases.size() << " passed\n";
        return fail;
    }
};

int main() {
    TestRunner tr;
    tr.add("config_load",   [] { return true; });
    tr.add("di_resolve",    [] { return true; });
    tr.add("pipeline_drop", [] { return false; });  // 故意失败，演示失败路径
    return tr.run() == 0 ? 0 : 1;
}
