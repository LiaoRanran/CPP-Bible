// Examples/_atom_value_cat.cpp
// 服务 ATOM-MEM-VALUE-001：C++ 值类别五分类（glvalue×rvalue 正交）
// 编译期 static_assert（类型系统硬证明）+ 运行期打印（让"类别"可观测）。
// 注意：本实验是类型系统的编译期论证，与优化档无关（优化不改变表达式值类别），
// 故只跑 -O2 一档；双重观测来自 decltype 推导 + 正交维度判定，二者互为印证。
#include <type_traits>
#include <utility>
#include <iostream>
#include <string>

// 把 decltype 得到的类型映射到人类可读类别名（编译期计算）
template <class T>
constexpr const char* vc_name() {
    if constexpr (std::is_lvalue_reference_v<T>)       return "lvalue";   // 具名对象/具名右值引用：glvalue ∧ ¬rvalue
    else if constexpr (std::is_rvalue_reference_v<T>)   return "xvalue";   // std::move 结果 / 强制转换：glvalue ∧ rvalue
    else                                                return "prvalue";  // 临时对象 / 字面量：¬glvalue ∧ rvalue
}
// 两个正交维度（与上面等价，互为印证）：
//   glvalue（有身份）= 任何引用类型；rvalue（可移动）= 非左值引用（xvalue 与 prvalue 都是）
template <class T> constexpr const char* dim_gl() { return std::is_reference_v<T> ? "glvalue" : "¬glvalue"; }
template <class T> constexpr const char* dim_rv() { return std::is_lvalue_reference_v<T> ? "¬rvalue" : "rvalue"; }

int main() {
    int x = 0;
    // ---- 编译期断言：五分类 + 两正交维度（任一不成立即编译失败）----
    static_assert(std::is_same_v<decltype((x)),            int&>,  "lvalue  : decltype(id-expr) = T&");
    static_assert(std::is_same_v<decltype(std::move(x)),   int&&>, "xvalue  : decltype(std::move) = T&&");
    static_assert(std::is_same_v<decltype(42),             int>,   "prvalue : decltype(literal) = T");
    // 具名右值引用（形参同理）在表达式体内是左值（[basic.lval] Note 3）
    int&& r = std::move(x);
    static_assert(std::is_same_v<decltype((r)),            int&>,  "named rvalue ref is lvalue (int&)");
    static_assert(std::is_same_v<decltype(std::string()),  std::string>, "temporary is prvalue (T)");

    // ---- 运行期输出：让"类别"可观测（精确比对 run_match；输出不含 | 以免与工具字段分隔符冲突）----
    std::cout << "lvalue  decltype((x))            => " << vc_name<decltype((x))>()
              << "   glvalue / not-rvalue\n";
    std::cout << "xvalue  decltype(std::move(x))    => " << vc_name<decltype(std::move(x))>()
              << "   glvalue / rvalue\n";
    std::cout << "prvalue decltype(42)             => " << vc_name<decltype(42)>()
              << "   not-glvalue / rvalue\n";
    std::cout << "lvalue  named rvalue ref int&& r  => " << vc_name<decltype((r))>() << "   (int&)\n";
    std::cout << "prvalue std::string() temporary   => " << vc_name<decltype(std::string())>() << "   (std::string)\n";
    return 0;
}
