// RW-053 | CVE-2021-30551 | Chromium/V8 | defect_type: type_punning
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-30551
// project_url: https://v8.dev/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: V8 TurboFan 对 Map 迁移类型假设错误，优化后代码把一种 JS 对象
//   当作另一种布局访问（类型混淆 → 越界/任意读写原语）。
// notes: 最小重构：用 C++ 联合体 + 错误类型标签模拟"优化器假设与现实布局不一致"。
//   UBSan/ASan 视访问路径命中。
#include <cstdint>
#include <cstdio>
#include <cstring>

enum Shape { SHAPE_PACKED_DOUBLE = 1, SHAPE_PACKED_OBJECT = 2 };

struct JsObject {
    Shape shape;
    union {
        double as_double[2];      // SHAPE_PACKED_DOUBLE layout
        void* as_ptr[2];          // SHAPE_PACKED_OBJECT layout
    } data;
};

// BUG (mirrors the deopt bug): the optimized path caches the shape as DOUBLE
// but the object was migrated to OBJECT layout; reinterpretation ensues.
double read_number_fast(JsObject* obj, bool optimized_assumes_double) {
    if (optimized_assumes_double && obj->shape == SHAPE_PACKED_OBJECT) {
        // type confusion: pointer bits read as a double
        return obj->data.as_double[0];
    }
    return 0.0;
}

int main() {
    JsObject o{};
    o.shape = SHAPE_PACKED_OBJECT;
    o.data.as_ptr[0] = (void*)0x4141414141414141ULL;   // "object" field
    double v = read_number_fast(&o, true);             // confused read
    std::printf("confused value = %f\n", v);
    return 0;
}
