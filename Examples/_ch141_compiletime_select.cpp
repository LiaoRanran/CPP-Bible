// Examples/_ch141_compiletime_select.cpp
// 编译期 DI：用 if constexpr 在编译期选择实现，避免虚调用与分支开销。
#include <iostream>

struct DevBackend  { static constexpr const char* name() { return "dev";  } };
struct ProdBackend { static constexpr const char* name() { return "prod"; } };

template <bool Production>
struct BackendSelector {
    auto make() const {
        if constexpr (Production) return ProdBackend{};   // ✅ 编译期确定
        else                      return DevBackend{};
    }
};

int main() {
    BackendSelector<false> dev;  std::cout << dev.make().name() << "\n";
    BackendSelector<true>  prod; std::cout << prod.make().name() << "\n";
}
