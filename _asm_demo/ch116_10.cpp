#include <utility>
int g_global = 0;
[[gnu::noinline]] void by_move(int&& x) { g_global = x; }
[[gnu::noinline]] void by_forward(int&& x) { by_move(std::move(x)); }
[[gnu::noinline]] void by_forward2(int&& x) { by_move(std::forward<int>(x)); }
int main() {
    int a = 1;
    by_forward(std::move(a));
    by_forward2(std::move(a));
    return 0;
}
