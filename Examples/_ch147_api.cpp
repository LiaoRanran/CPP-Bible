// _ch147_api.cpp —— ABI / API 兼容性审查示例
// 在头文件中稳定导出符号；不要随意改动已发布函数签名。
#pragma once
#include <cstdint>

// 稳定接口（自 v1 起不变）
[[nodiscard]] int32_t compute_v1(int32_t a, int32_t b);

// 新增功能用重载/新函数，而非修改旧签名（避免 ABI 破坏）
[[nodiscard]] int64_t compute_v2(int64_t a, int64_t b);
