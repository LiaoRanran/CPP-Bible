// RW-028 | CVE-2018-15473 | OpenSSH | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-15473
// project_url: https://www.openssh.com/
// year: 2018 | severity: MEDIUM | source_type: cve
// mechanism: 认证流程对无效用户名提前返回（不进入延迟/伪造认证），响应时延与
//   内容差异使攻击者可枚举有效用户名。
// notes: 最小重构。逻辑缺陷类（侧信道/信息泄露）。
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

struct UserDb {
    std::vector<std::string> names{"root", "deploy", "app"};
};

// BUG: invalid user short-circuits, valid user goes through the (slow) KEX auth
int auth_attempt(const UserDb& db, const char* user) {
    bool found = false;
    for (const auto& n : db.names) {
        if (n == user) { found = true; break; }
    }
    if (!found) {
        return 1;              // fast path: "invalid user" (observable difference)
    }
    // "perform" the expensive fake-auth dance for valid users
    volatile unsigned long spin = 0;
    for (unsigned long i = 0; i < 5000000UL; ++i) spin += i;
    return 2;
}

int main() {
    UserDb db;
    int r1 = auth_attempt(db, "definitely-not-a-user");
    int r2 = auth_attempt(db, "root");
    std::printf("invalid-user rc=%d (fast), valid-user rc=%d (slow) -> oracle\n", r1, r2);
    return 0;
}
