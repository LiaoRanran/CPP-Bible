// _ch148_conventional_commit.cpp
// 用 <regex> 解析 Conventional Commits 提交信息，供 commit-msg 钩子复用。
// 编译：g++ -std=c++23 -O2 _ch148_conventional_commit.cpp -o _ch148_conventional_commit
#include <cstdio>
#include <regex>
#include <string>
#include <string_view>

struct Parsed {
    std::string type, scope, description;
    bool breaking = false;
};

// 形如：  feat(parser): add coroutine support
//        fix!: prevent null deref in scheduler
static bool parse_commit(const std::string& msg, Parsed& out) {
    static const std::regex re(
        R"(^(\w+)(?:\(([^)]*)\))?(!)?:\s*(.+)$)");
    std::smatch m;
    if (!std::regex_search(msg, m, re)) return false;
    out.type = m[1];
    out.scope = m[2];
    out.breaking = !m[3].str().empty();
    out.description = m[4];
    return true;
}

int main() {
    const char* samples[] = {
        "feat(parser): add coroutine support",
        "fix!: prevent null deref in scheduler",
        "chore: bump toolchain to GCC 14",
    };
    for (auto s : samples) {
        Parsed p;
        if (parse_commit(s, p)) {
            std::printf("[OK] type=%-6s scope=%-8s breaking=%-5s desc=%s\n",
                        p.type.c_str(), p.scope.c_str(),
                        p.breaking ? "true" : "false", p.description.c_str());
        } else {
            std::printf("[BAD] 不符合 Conventional Commits: %s\n", s);
        }
    }
    return 0;
}
