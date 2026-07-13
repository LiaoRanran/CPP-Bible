// 例：_ch131_format_check.cpp
// 目的：在【不依赖 fmt】的前提下，复现 fmt 的两大核心机制：
//   (a) 编译期解析格式串、统计 "{}" 占位符数量；
//   (b) 编译期校验 占位符数量 == 实参数（类型安全格式化）。
// fmt 的 basic_format_string<Args...> 正是用“编译期格式串 + static_assert”完成这点；
// 这里用 C++20 类类型 NTTP（fixed_string）等价还原，无需任何第三方库。

#include <cstdio>

// ① 编译期递归扫描格式串，统计 "{}" 占位符个数
constexpr int count_args(const char* s, int i = 0, int n = 0) {
    return s[i] == '\0' ? n
         : (s[i] == '{' && s[i + 1] == '}') ? count_args(s, i + 2, n + 1)
         : count_args(s, i + 1, n);
}

// ② 编译期字符串（类类型 NTTP，C++20）：数组长度由字面量精确推导，全部初始化
template <std::size_t N>
struct fixed_string {
    char data[N];
    consteval fixed_string(const char (&s)[N]) {
        for (std::size_t i = 0; i < N; ++i) data[i] = s[i];
    }
};

// ③ 按类型分派输出（等价 fmt 的 formatter 特化分派）
inline void emit(int v)         { std::printf("%d", v); }
inline void emit(double v)      { std::printf("%g", v); }
inline void emit(const char* v) { std::printf("%s", v); }

// ④ 类型安全格式化入口：Fmt 是编译期 NTTP（类模板参数推导为 fixed_string<N>），
//    占位符数量在编译期即可校验
template <fixed_string Fmt, typename... Ts>
void safe_fmt(Ts... ts) {
    constexpr int need = count_args(Fmt.data);     // Fmt 为 NTTP -> 编译期常量表达式
    static_assert(need == sizeof...(Ts),
                  "格式串占位符数量与参数数量不匹配（编译期）");
    std::printf("%s", Fmt.data);
    (emit(ts), ...);                               // 折叠表达式：按各实参类型分派 emit
}

// ⑤ 演示：合法调用（占位符 3 == 参数 3，类型与 emit 重载匹配）
int demo() {
    safe_fmt<"pi={} name={} n={}">(3.14, "fmt", 42);
    return 0;
}

// 注：若写成 safe_fmt<"{} {}">(1);
//     —— 占位符 2 != 参数 1，static_assert 在编译期直接失败，与 fmt 行为一致。

// ⑥ 入口：使示例可独立运行
int main() { return demo(); }
