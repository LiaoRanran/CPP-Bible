// RW-055 | CVE-2021-21224 | Chromium/V8 | defect_type: type_punning
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-21224
// project_url: https://v8.dev/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: Pwn2Own 2021 Vancouver 致胜链的一环 —— TurboFan 对
//   Number.parseInt 结果的整数类型假设被"无穷大/NaN 折叠"绕过，类型混淆。
// notes: 最小重构（数值域混淆 → 位模式重解释）。UB/ASan 按路径命中。
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: parseIntFast folds to Int32 even when the input produced a float
// (Infinity), then the value is stored into a raw int32 slot.
struct Slot {
    uint64_t bits;    // raw tag+payload slot (double or int32, tag missing)
};

int32_t confused_parse_store(const char* text) {
    double parsed = std::strtod(text, nullptr);   // "1e999" -> +inf
    float f = static_cast<float>(parsed);
    int32_t i = (int32_t)f;                        // UB: inf -> int32 conversion
    Slot s{};
    std::memcpy(&s.bits, &i, sizeof(i));           // raw store; later read as double
    double reread = 0;
    std::memcpy(&reread, &s.bits, sizeof(reread)); // bit reinterpretation
    std::printf("reread as double: %f\n", reread);
    return i;
}

int main() {
    volatile int32_t v = confused_parse_store("1e999"); // crafted large numeric literal
    std::printf("stored int32: %d\n", (int)v);
    return 0;
}
