// Examples/_atom_fwd_fold.cpp
// 服务 ATOM-MEM-VALUE-002：引用折叠与万能引用（forwarding reference）。
// 论断一：引用折叠只有 4 条规则，唯一折叠成右值引用的是 "右值引用的右值引用"（T&& && → T&&）；
//         这 4 个别名能通过编译本身就依赖折叠规则（否则 T& & 这类写法非法）。
// 论断二：T&& 只有在"推导语境"下才是万能引用：传左值推 T=int&（折叠回左值引用），
//         传右值推 T=int（T&& 即右值引用）；auto&& 同理；const T&& 不是万能引用（不参与特判，只接右值）。
// 类型系统论证（decltype/static_assert 编译期硬证明）+ 运行期打印（推导结果可观测）。
#include <type_traits>
#include <utility>
#include <iostream>

// ---- 四条折叠规则的别名直证：引用只能"经模板形参/typedef 引入"才折叠（[dcl.ref]），
//      直接写 T& & 反而非法——所以用别名层叠把第二个引用经模板形参引入 ----
template <class T> using Lref = T&;
template <class T> using Rref = T&&;
template <class T> using LrefLref = Lref<Lref<T>>;    // T& &    （左值引用的左值引用）
template <class T> using LrefRref = Rref<Lref<T>>;    // T& &&   （左值引用的右值引用）
template <class T> using RrefLref = Lref<Rref<T>>;    // T&& &   （右值引用的左值引用）
template <class T> using RrefRref = Rref<Rref<T>>;    // T&& &&  （右值引用的右值引用）

static_assert(std::is_same_v<LrefLref<int>, int&>,  "T& &   folds to T&");
static_assert(std::is_same_v<LrefRref<int>, int&>,  "T& &&  folds to T&");
static_assert(std::is_same_v<RrefLref<int>, int&>,  "T&& &  folds to T&");
static_assert(std::is_same_v<RrefRref<int>, int&&>, "T&& && folds to T&&  (only this one stays rvalue-ref)");

// ---- 万能引用：推导语境下的 T&&（[temp.deduct.call] 特判）----
template <class T>
void sink_univ(T&&) {
    // T 的形状即推导结果：传左值 → T=int&（T&& 折叠成 int&）；传右值 → T=int（T&& 即 int&&）
    std::cout << "univ   T&& : T=" << (std::is_lvalue_reference_v<T> ? "int&  " : "int   ")
              << " param_is_lvalue_ref=" << (std::is_lvalue_reference_v<T&&> ? 1 : 0) << "\n";
}
// ---- 反例：const T&& 不是万能引用（无推导特判，只绑定右值）----
template <class T>
void sink_const_rref(const T&&) {
    std::cout << "const T&& : T=" << (std::is_lvalue_reference_v<T> ? "int&  (ERROR: deduced from lvalue!)" : "int   (rvalue only)")
              << "\n";
}
// 左值 sink（对照：接受左值的普通重载；打印运行时值，不用整句常量冒充观测）
void sink_lvalue(int& x) { std::cout << "sink_lvalue called x=" << x << "\n"; }

int main() {
    int lv = 0;
    // ---- 折叠规则的运行期可观测形式（与 static_assert 同构）----
    std::cout << "fold T& &   => " << (std::is_same_v<LrefLref<int>, int&> ? "int&" : "OTHER") << "\n";
    std::cout << "fold T& &&  => " << (std::is_same_v<LrefRref<int>, int&> ? "int&" : "OTHER") << "\n";
    std::cout << "fold T&& &  => " << (std::is_same_v<RrefLref<int>, int&> ? "int&" : "OTHER") << "\n";
    std::cout << "fold T&& && => " << (std::is_same_v<RrefRref<int>, int&&> ? "int&&" : "OTHER") << "\n";

    // ---- auto&& 也是万能引用： decltype(变量) 给出声明类型 ----
    auto&& a1 = lv;    // 传左值 → int&
    auto&& a2 = 42;    // 传右值 → int&&
    std::cout << "auto&& from lvalue => " << (std::is_same_v<decltype(a1), int&> ? "int&" : "OTHER") << "\n";
    std::cout << "auto&& from rvalue => " << (std::is_same_v<decltype(a2), int&&> ? "int&&" : "OTHER") << "\n";

    // ---- 万能引用推导：左值 → 左值引用；右值 → 右值引用 ----
    sink_univ(lv);     // T=int&
    sink_univ(42);     // T=int
    sink_const_rref(42);   // 只接右值：T=int（无左值特判）
    sink_lvalue(lv);   // 对照：普通左值引用重载
    return 0;
}
