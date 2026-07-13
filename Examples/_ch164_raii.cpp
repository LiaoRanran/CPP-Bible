// ⑩ 生命周期管理（RAII）：构造即持有、析构即释放，杜绝资源泄漏
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <utility>

// 通用作用域守卫：离开作用域必执行清理（异常安全）
template <class F>
struct ScopeGuard { F f; explicit ScopeGuard(F g) : f(std::move(g)) {} ~ScopeGuard() { f(); } };
template <class F> ScopeGuard<F> finally(F f) { return ScopeGuard<F>(std::move(f)); }

struct Handle {
    std::string tag;
    explicit Handle(std::string t) : tag(std::move(t)) { std::cout << "[raii] acquire " << tag << "\n"; }
    ~Handle() { std::cout << "[raii] release " << tag << "\n"; }
};

int main() {
    {
        Handle h{"db-conn"};
        auto g = finally([] { std::cout << "[raii] flush + unlock\n"; });
        std::cout << "[raii] working...\n";
        // 即使此处 throw，h 与 g 仍会被析构
    }
    std::cout << "[raii] scope exited cleanly\n";
    return 0;
}
