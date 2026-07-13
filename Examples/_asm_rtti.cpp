#include <typeinfo>
#include <cstdio>

struct Base { virtual ~Base() = default; virtual int f() const { return 1; } };
struct Der : Base { int f() const override { return 2; } };
struct Other {};

// typeid 取动态类型 name
const char* get_name(const Base& b) {
    return typeid(b).name();
}

// dynamic_cast 下行转换，失败返 nullptr
const Der* down_cast(const Base* p) {
    return dynamic_cast<const Der*>(p);
}

// dynamic_cast 引用失败抛 std::bad_cast
const Der& down_cast_ref(const Base& b) {
    return dynamic_cast<const Der&>(b);
}

int main() {
    Der d;
    Base* p = &d;
    std::printf("%s\n", get_name(*p));
    const Der* q = down_cast(p);
    if (q) std::printf("ok %d\n", q->f());
    const Der& r = down_cast_ref(*p);
    std::printf("%d\n", r.f());
    return 0;
}
