// _ch145_return.cpp —— 返回值策略（值 / 引用 / optional）（g++ -O2 -S 取证）
#include <optional>

struct Big { long a[8]; };

Big by_value() { return Big{1,2,3,4,5,6,7,8}; }       // 大对象：sret 隐藏指针返回
const Big& by_ref(const Big& b) { return b; }          // 返回入参地址
std::optional<Big> by_opt() { return Big{1,2,3,4,5,6,7,8}; }

long use_value() { return by_value().a[0]; }
long use_ref(const Big& b) { return by_ref(b).a[0]; }

int main() {
    Big b{};
    return static_cast<int>(use_value() + use_ref(b));
}
