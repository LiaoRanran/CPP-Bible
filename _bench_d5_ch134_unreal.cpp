// _bench_d5_ch134_unreal.cpp
// D5 benchmark: Unreal-style property access strategies
//   direct struct field  (baseline, what generated UObject getters reduce to)
//   pointer-to-member     (what UObject::FProperty offset access approximates)
//   virtual getter        (naive virtual dispatch)
//   string-key registry   (Blueprint FName property lookup simulation)
#include <cstdio>
#include <chrono>
#include <unordered_map>
#include <string>
#include <string_view>

volatile int g_sink = 0;

struct Transform {
    float x, y, z;
    float rx, ry, rz;
    float sx, sy, sz;
};

// --- Direct struct field access (baseline) ---
[[gnu::noinline]] int bench_direct(const Transform& t, int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) acc += (int)t.x;
    return acc;
}

// --- Virtual getter dispatch (naive reflection) ---
struct Reflectable {
    virtual float get_x() const = 0;
    virtual ~Reflectable() = default;
};
struct TransformVirt : public Reflectable {
    float x, y, z, rx, ry, rz, sx, sy, sz;
    TransformVirt(float x, float y, float z, float rx, float ry, float rz,
                  float sx, float sy, float sz)
        : x(x), y(y), z(z), rx(rx), ry(ry), rz(rz), sx(sx), sy(sy), sz(sz) {}
    float get_x() const override { return x; }
};

[[gnu::noinline]] Reflectable* get_reflectable() {
    static TransformVirt inst(1.0f, 2.0f, 3.0f, 0,0,0, 1,1,1);
    return &inst;
}

[[gnu::noinline]] int bench_virtual(const Transform& t, int N) {
    Reflectable* r = get_reflectable();
    int acc = 0;
    for (int i = 0; i < N; i++) acc += (int)r->get_x();
    return acc;
}

// --- String-key registry (Blueprint FName property lookup simulation) ---
struct StringReflectable {
    float x_, y_, z_;
    static std::unordered_map<std::string_view, int> prop_map;
public:
    StringReflectable(float x, float y, float z) : x_(x), y_(y), z_(z) {
        if (prop_map.empty()) {
            prop_map["x"] = 0; prop_map["y"] = 1; prop_map["z"] = 2;
        }
    }
    float get_by_name(std::string_view name) const {
        auto it = prop_map.find(name);
        if (it == prop_map.end()) return 0;
        switch (it->second) {
            case 0: return x_;
            case 1: return y_;
            case 2: return z_;
            default: return 0;
        }
    }
};
std::unordered_map<std::string_view, int> StringReflectable::prop_map;

[[gnu::noinline]] int bench_string_lookup(const Transform& t, int N) {
    StringReflectable sr(t.x, t.y, t.z);
    int acc = 0;
    for (int i = 0; i < N; i++) acc += (int)sr.get_by_name("x");
    return acc;
}

// --- Pointer-to-member (what UObject::FProperty offset access approximates) ---
struct OffsetReflectable {
public:
    float x_, y_, z_;
    OffsetReflectable(float x, float y, float z) : x_(x), y_(y), z_(z) {}
    float get_x() const { return x_; }
};

[[gnu::noinline]] int bench_offset_access(const Transform& t, int N) {
    OffsetReflectable or_(t.x, t.y, t.z);
    float OffsetReflectable::* off = &OffsetReflectable::x_;
    int acc = 0;
    for (int i = 0; i < N; i++) acc += (int)(or_.*off);
    return acc;
}

int main() {
    const int N = 10000000;
    Transform tr = {7.0f, 13.0f, 5.0f, 0,0,0, 1,1,1};

    volatile int w = bench_direct(tr, 1000); (void)w;

    struct { const char* name; int (*fn)(const Transform&, int); double median; } tests[] = {
        {"direct field",        bench_direct,        0},
        {"pointer-to-member",   bench_offset_access,  0},
        {"virtual getter",      bench_virtual,        0},
        {"string-key lookup",   bench_string_lookup,  0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(tr, N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch134 unreal D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-22s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
