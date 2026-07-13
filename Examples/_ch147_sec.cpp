// _ch147_sec.cpp —— 安全审查：格式化/边界
#include <cstdio>
#include <string>

// 坏味道：受控写入但长度不可控 -> 审计点
void log_user(const std::string& name) {
    // 此处 name 来自外部输入；审查：是否需长度/字符白名单校验？
    std::printf("user=%s\n", name.c_str());
}

// 好味道：使用 std::format 类型安全
#include <format>
std::string safe_log(const std::string& name) {
    return std::format("user={}", name);
}
