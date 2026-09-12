// Examples/_atom_unique_deleter.cpp
// 服务 ATOM-MEM-UNIQUE-002：unique_ptr 的删除器是**类型的一部分**（进类型系统、无状态可零开销），
// shared_ptr 的删除器被**类型擦除**进控制块（对象大小不随删除器变化）。
// 观测纪律：删除器调用计数用 volatile（防 -O2 常量折叠，M2 §5）；数组路径用 operator new[]/delete[]
// 重载计数，证明 unique_ptr<T[]> 走的是 delete[] 而不是 delete。
#include <cstdio>
#include <cstddef>
#include <cstdlib>
#include <memory>
#include <type_traits>

// ---- 观测点（volatile：-O2 不可折叠；观测通路必须活着）----
static volatile int g_stateless_calls = 0;
static volatile int g_stateful_calls = 0;
static volatile int g_final_calls = 0;
static volatile long g_arr_new = 0;
static volatile long g_arr_del = 0;

void* operator new[](std::size_t n) { g_arr_new = g_arr_new + 1; return std::malloc(n); }
void  operator delete[](void* p) noexcept { g_arr_del = g_arr_del + 1; std::free(p); }
// sized 版本必须同时定义（否则 -Wsized-deallocation 告警）；转发到上面那条，保证**计数通路唯一**
// （教训：分配器内手动 +1 与 operator new 钩子叠加会造成双重计数）。
void  operator delete[](void* p, std::size_t) noexcept { operator delete[](p); }

// ---- 三种删除器：无状态（空类，可被 EBO 吸收）/ 有状态（带成员）/ 数组 ----
struct StatelessDel {
    void operator()(int* p) const noexcept { g_stateless_calls = g_stateless_calls + 1; delete p; }
};
struct StatefulDel {
    int tag = 7;                       // 有状态：删除器必须被存储
    void operator()(int* p) const noexcept { g_stateful_calls = g_stateful_calls + 1; delete p; }
};
// 空但 final：libstdc++ 的空基类优化门槛是"空**且非 final**"（内部 trait __empty_not_final）。
// 这是**真证伪对照**——若"无状态删除器 ⇒ 不增大对象"是普遍规则，本类型也该是 8；实测 16。
// 于是 claim 必须写成"libstdc++ 实现边界"而不是"语言保证"。
struct StatelessFinalDel final {
    void operator()(int* p) const noexcept { g_final_calls = g_final_calls + 1; delete p; }
};

// ---- 编译期探测：数组特化不提供 operator* / operator->（只提供 operator[]）----
template <class T, class = void> struct has_deref : std::false_type {};
template <class T> struct has_deref<T, std::void_t<decltype(*std::declval<T&>())>> : std::true_type {};

template <class T, class = void> struct has_arrow : std::false_type {};
template <class T> struct has_arrow<T, std::void_t<decltype(std::declval<T&>().operator->())>> : std::true_type {};

template <class T, class = void> struct has_subscript : std::false_type {};
template <class T> struct has_subscript<T, std::void_t<decltype(std::declval<T&>()[0])>> : std::true_type {};

int main(int argc, char**) {
    // ① 类型参数 vs 类型擦除：unique_ptr 的 sizeof 随删除器变化，shared_ptr 不随
    std::printf("sizeof unique_ptr default=%d\n", (int)sizeof(std::unique_ptr<int>));
    std::printf("sizeof unique_ptr stateless=%d\n", (int)sizeof(std::unique_ptr<int, StatelessDel>));
    std::printf("sizeof unique_ptr stateful=%d\n", (int)sizeof(std::unique_ptr<int, StatefulDel>));
    std::printf("sizeof unique_ptr array=%d\n", (int)sizeof(std::unique_ptr<int[]>));
    std::printf("sizeof unique_ptr ref deleter=%d\n", (int)sizeof(std::unique_ptr<int, StatefulDel&>));
    std::printf("sizeof unique_ptr final stateless=%d\n", (int)sizeof(std::unique_ptr<int, StatelessFinalDel>));
    // shared_ptr 的删除器**不是模板参数**：语言层面就没有 shared_ptr<T, D>。实测编译错误原文：
    //   error: wrong number of template arguments (2, should be 1)
    //   note: provided for 'template<class _Tp> class std::shared_ptr'   （GCC 15.3.0 与 14.2 一致）
    // 删除器只能经构造函数注入、被擦除进控制块 ⇒ 对象大小与删除器无关（对比上面 unique_ptr 的变化）。
    {
        std::shared_ptr<int> sp_default(new int(1));
        std::shared_ptr<int> sp_stateless(new int(2), StatelessDel{});
        std::shared_ptr<int> sp_stateful(new int(3), StatefulDel{});
        std::printf("sizeof shared_ptr default=%d\n", (int)sizeof(sp_default));
        std::printf("sizeof shared_ptr stateless=%d\n", (int)sizeof(sp_stateless));
        std::printf("sizeof shared_ptr stateful=%d\n", (int)sizeof(sp_stateful));
        int sizes_equal = (sizeof(sp_default) == sizeof(sp_stateless)
                           && sizeof(sp_stateless) == sizeof(sp_stateful)) ? 1 : 0;
        std::printf("shared_ptr sizes equal=%d\n", sizes_equal);
        // 擦除的直接后果：同一个静态类型 shared_ptr<int> 的变量可改持不同删除器的对象
        sp_stateless = std::shared_ptr<int>(new int(4), StatefulDel{});
        std::printf("shared_ptr retargeted=%d\n", (int)(sp_stateless != nullptr));
    }

    // ② 数组特化的接口特征（编译期）：只有 operator[]，没有 operator* / operator->
    std::printf("array has subscript=%d\n", (int)has_subscript<std::unique_ptr<int[]>>::value);
    std::printf("array has deref=%d\n", (int)has_deref<std::unique_ptr<int[]>>::value);
    std::printf("array has arrow=%d\n", (int)has_arrow<std::unique_ptr<int[]>>::value);
    std::printf("object has subscript=%d\n", (int)has_subscript<std::unique_ptr<int>>::value);
    std::printf("object has deref=%d\n", (int)has_deref<std::unique_ptr<int>>::value);
    std::printf("object has arrow=%d\n", (int)has_arrow<std::unique_ptr<int>>::value);

    // ③ 删除器真的被调用（观测通路活着）且每个对象恰一次——一律用**差分**读，
    //    不读全局累计值（红队 S4 拦截：原版累计值混入了 shared_ptr 块的调用，构成不可解释）
    int st0 = g_stateless_calls, sf0 = g_stateful_calls, fin0 = g_final_calls;
    {
        std::unique_ptr<int> a(new int(1));
        std::unique_ptr<int, StatelessDel> b(new int(2));
        std::unique_ptr<int, StatefulDel> c(new int(3), StatefulDel{});
        std::unique_ptr<int, StatelessFinalDel> f(new int(4));
    }
    std::printf("stateless calls delta=%d\n", (int)(g_stateless_calls - st0));
    std::printf("stateful calls delta=%d\n", (int)(g_stateful_calls - sf0));
    std::printf("final deleter calls delta=%d\n", (int)(g_final_calls - fin0));

    // ④ 数组特化走 delete[]（不是 delete）：operator delete[] 计数
    {
        // 长度与下标都从 argc 派生（**运行期**值）：避免被 -O2 折叠成立即数而退化成恒真观测
        //（红队 S4 拦截：原版 n=8 / arr[3]=42 被折叠成 mov edx,8 / mov r8d,42，零信息）
        const std::size_t n = static_cast<std::size_t>(argc) + 7;
        const int idx = argc + 2;
        std::unique_ptr<int[]> arr(new int[n]);
        arr[idx] = argc * 10 + 2;
        std::printf("array len=%d elem=%d\n", (int)n, arr[idx]);
    }
    std::printf("array new calls=%d\n", (int)g_arr_new);
    std::printf("array delete calls=%d\n", (int)g_arr_del);

    // 对照组：单对象 unique_ptr 走 delete，不碰 delete[]
    long before = g_arr_del;
    {
        std::unique_ptr<int> one(new int(9));
    }
    std::printf("single object delete[] delta=%d\n", (int)(g_arr_del - before));
    return 0;
}
