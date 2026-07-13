// _ch145_strong.cpp —— 强类型与 =delete 防误用（g++ 编译取证，warnings clean）
#include <cstdint>

struct UserId { int64_t v; explicit UserId(int64_t x) : v(x) {} };
struct OrderId { int64_t v; explicit OrderId(int64_t x) : v(x) {} };

// 误用：UserId 不能隐式转 OrderId，编译期即拦截
void process(OrderId id) { (void)id; }

// 删除危险的隐式转换构造，杜绝窄化/误用
struct Meter {
    explicit Meter(double m) : m_(m) {}
    Meter(int) = delete;          // 禁止从 int 构造（易错的单位混淆）
    double m_ = 0;
};

int main() {
    UserId u{42};
    OrderId o{7};
    // process(u);                // ❌ 编译错误：UserId != OrderId
    process(o);                   // ✅
    Meter m{1.5};                 // ✅
    // Meter bad{3};              // ❌ 编译错误：Meter(int) 已删除
    (void)u; (void)m;
    return 0;
}
