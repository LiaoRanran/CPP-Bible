// _ch135_constexpr.cpp
// 取证目标（第⑯节）：constexpr / if constexpr 把分支在编译期消除。
#include <cstdio>

template <typename T>
constexpr auto describe() {
    if constexpr (sizeof(T) == 1)      return "byte";
    else if constexpr (sizeof(T) <= 4) return "word";
    else                                return "wide";
}

int main() {
    constexpr const char* d = describe<long long>();
    std::printf("%s\n", d); // "wide"，分支在编译期确定
}
