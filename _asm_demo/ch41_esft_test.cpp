// P1-GAP-3: enable_shared_from_this —— 内嵌 weak_this 与控制块初始化时机
// 揭示的底层事实：
//   - 继承 enable_shared_from_this<T> 的类，对象里多嵌一个 weak_ptr<T>（weak_this，16B）；
//   - shared_from_this() = weak_this.lock()，lock 失败（构造 shared_ptr 前调用）抛 bad_weak_ptr；
//   - weak_this 在首次构造 shared_ptr 时才被 _M_assign 初始化。
#include <memory>
#include <cstddef>

struct Plain { int x; };                      // 对照组：无 enable_shared_from_this

struct WithEsft : std::enable_shared_from_this<WithEsft> {
    int x;
};

long long sizeof_plain() { return sizeof(Plain); }
long long sizeof_with_esft() { return sizeof(WithEsft); }

// shared_from_this() 展开：weak_this.lock()，含空守卫（失败抛 bad_weak_ptr）
std::shared_ptr<WithEsft> grab(WithEsft* p) {
    return p->shared_from_this();
}