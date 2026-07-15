// ASM-81-string_view : std::string_view 零成本视图实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 string_view = {ptr, len} 16 字节；substr 为 O(1) 指针/长度调整（无拷贝），
//       与 std::string::substr 的 O(n) 堆分配+拷贝形成对比；operator[] 不查边界；size() 即取 len 字段。
#include <string_view>
#include <string>
#include <iostream>

// (1) string_view::substr：O(1) —— 仅调整 ptr 与 len，零拷贝
std::string_view sv_substr(std::string_view sv, std::size_t pos, std::size_t cnt) {
    return sv.substr(pos, cnt);
}

// (2) std::string::substr：O(n) —— 真实堆分配 + 拷贝
std::string str_substr(const std::string& s, std::size_t pos, std::size_t cnt) {
    return s.substr(pos, cnt);
}

// (3) operator[]：无边界检查，单条 mov
char sv_at(std::string_view sv, std::size_t i) {
    return sv[i];
}

// (4) size()：直接取 len 字段
std::size_t sv_size(std::string_view sv) {
    return sv.size();
}

// (5) 布局：string_view 固定 16 字节 = 指针 + size_t
constexpr std::size_t sv_sz = sizeof(std::string_view);
static_assert(sv_sz == 16, "string_view = const char* + size_t");

int main() {
    const char* lit = "hello world";
    std::string_view sv(lit, 11);
    volatile int sink = 0;
    auto sub = sv_substr(sv, 0, 5);   // 期望：仅改 ptr/len，无 call
    sink = (int)sub.size();
    sink += (int)sv_at(sv, 2);        // 期望：mov，无边界检查
    sink += (int)sv_size(sv);         // 期望：取 len 字段
    std::string s(lit);
    auto s2 = str_substr(s, 0, 5);    // 期望：operator new + memcpy
    sink += (int)s2.size();
    return (int)sink + (int)sv_sz;
}
