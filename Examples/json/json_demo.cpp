// 手写 JSON 库真实用法演示 —— 模拟「配置读取 → 查询 → 修改 → 回写」完整链路
// 编译：g++ -std=c++23 -O2 -Wall -Wextra -o json_demo.exe json_demo.cpp
// 运行：./json_demo.exe
#include "json.hpp"

#include <iostream>
#include <string>

int main() {
    const std::string raw =
        R"({"app":"todo","version":2,)"
        R"("features":{"dark_mode":true,"sync":false},)"
        R"("servers":["eu","us"],)"
        R"("owner":{"name":"Alice"}})";

    json::Value cfg = json::parse(raw);

    // 1. 点路径查询（返回 nullptr 表示不存在 / 层级类型不符）
    if (const json::Value* dark = cfg.find("features.dark_mode"))
        std::cout << "dark_mode = " << (dark->as_bool() ? "on" : "off") << '\n';
    if (cfg.find("missing.key") == nullptr)
        std::cout << "missing.key -> not found\n";

    // 2. 就地修改：开同步 + 追加服务器 + 改名
    cfg["features"]["sync"].set(true);
    cfg["servers"].as_array().push_back(json::Value("asia"));
    if (json::Value* name = cfg.find("owner.name")) name->set("Bob");

    // 3. 紧凑回写（单行，适合网络 / 存储）
    std::cout << "\ncompact:\n" << json::serialize(cfg) << '\n';

    // 4. 美化回写（2 空格缩进，适合人读 / 日志）
    std::cout << "\npretty (indent=2):\n" << json::serialize(cfg, 2) << '\n';
    return 0;
}