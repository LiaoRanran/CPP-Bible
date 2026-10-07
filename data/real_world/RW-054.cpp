// RW-054 | CVE-2020-16040 | Chromium/V8 | defect_type: type_punning
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-16040
// project_url: https://v8.dev/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: V8 优化编译器在整数回绕（speculative number）假设上被绕过，
//   类型混淆导致越界访问数组长度。
// notes: 最小重构（模拟"长度字段被以错误宽度读回"的混淆）。
#include <cstdint>
#include <cstdio>
#include <vector>

struct FastArray {
    uint32_t length;            // JSArray length (Smis in real V8)
    int32_t elements[8];
};

// BUG: the JIT read the length as int32 while the mutated object holds a
// double-backed length value; negative length treated as huge unsigned.
int read_element_confused(FastArray* a, int32_t idx) {
    int32_t len = (int32_t)a->length;
    if (len < 0) {
        // confused: negative length passes via wraparound comparison
        return a->elements[idx & 7];
    }
    if (idx < len) return a->elements[idx];
    return -1;
}

int main() {
    FastArray a{};
    a.length = 0xFFFFFFFFu;      // crafted length: -1 as int32
    a.elements[0] = 424242;
    int v = read_element_confused(&a, 0);
    std::printf("confused read = %d\n", v);
    return 0;
}
