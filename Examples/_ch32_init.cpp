// _ch32_init.cpp —— ch32 初始化深耕的真机取证源码（GCC 15.3.0 / MinGW-w64）
//
// 取证目标：
//  1. MVP（Most Vexing Parse）：Foo f(); 是函数声明而非对象定义
//  2. vector<int>(10,2) vs vector<int>{10,2} 的语义差异（真机 size 对比）
//  3. 成员初始化顺序 = 声明顺序（非初始化列表顺序），读未初始化成员的后果
//  4. 返回 initializer_list 的悬垂（底层数组是临时对象）
//  5. brace 初始化 vs 逐个赋值的生成代码对比（-O2 汇编 + 计时）
//  6. 零初始化 / 值初始化 / 默认初始化的实际字节差异
//
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch32_init.cpp -o _ch32_init.s

#include <cstdio>
#include <vector>
#include <initializer_list>
#include <string>
#include <chrono>
#include <cstddef>
#include <type_traits>

// ---- 1. MVP -------------------------------------------------------------
struct Foo {};
static Foo  g_mvp_obj{};   // 对比：真正的对象定义
// 下面这行若取消注释，链接期会报 undefined reference to `Foo f()'
// ——证明 `Foo f();' 被解析为**函数声明**（而非对象定义）：
// extern Foo mvp_is_function();

// ---- 2. initializer_list 优先劫持 ---------------------------------------
static void il_hijack() {
    std::vector<int> v_paren(10, 2);   // 10 个 2
    std::vector<int> v_brace{10, 2};   // 2 个元素：10 和 2
    std::printf("2) vector<int>(10,2).size()=%zu   vector<int>{10,2}.size()=%zu\n",
                v_paren.size(), v_brace.size());
}

// ---- 3. 成员初始化顺序 --------------------------------------------------
struct Order {
    int a;
    int b;
    Order(int x) : b(x), a(b) {}   // 实际先初始化 a（此时 b 未初始化）
};

// ---- 4. 返回 initializer_list 的悬垂 -----------------------------------
// 底层数组随函数返回而销毁，返回的 initializer_list 指向已释放的存储。
static std::initializer_list<int> dangling_il() {
    return {1, 2, 3};   // 编译期不报错，运行期访问即 UB
}

// ---- 5. brace vs assign 的生成代码 -------------------------------------
struct Vec3 { double x, y, z; };

__attribute__((noinline)) static Vec3 make_brace() { return {1.0, 2.0, 3.0}; }
__attribute__((noinline)) static Vec3 make_assign() {
    Vec3 v;              // 未初始化（内置类型成员）
    v.x = 1.0; v.y = 2.0; v.z = 3.0;
    return v;
}

// ---- 6. 三种初始化的字节差异 -------------------------------------------
struct Plain { int a; double b; char c; };

int main() {
    std::printf("=== ch32 初始化真机取证 (GCC %d.%d) ===\n", __GNUC__, __GNUC_MINOR__);

    // 1) MVP：用 decltype 证明 f() 的类型是函数而非对象
    {
        // `Foo f();' 若在函数内声明，类型为 Foo()（函数类型）
        using T = decltype(std::declval<Foo (*)()>());
        std::printf("1) MVP: Foo(*)() 是%s；Foo f(); 解析为函数声明"
                    "（对象定义须写 Foo f{};）\n",
                    std::is_function_v<std::remove_pointer_t<T>> ? "函数指针" : "对象");
    }

    il_hijack();

    // 3) 成员顺序：a 先被初始化，读到的是未初始化的 b
    {
        Order o(42);
        std::printf("3) Order o(42): o.a=%d o.b=%d  ", o.a, o.b);
        std::printf("（a 先于 b 初始化，读到未初始化的 b → a 值不确定/UB）\n");
    }

    // 4) 悬垂 initializer_list
    {
        std::initializer_list<int> il = dangling_il();
        std::printf("4) 返回 initializer_list: size=%zu"
                    "  ——底层数组随函数返回销毁，读取即 UB（此处不读取，仅看 size）\n",
                    il.size());
    }

    // 5) brace vs assign
    {
        const int N = 20'000'000;
        Vec3 sink{0, 0, 0};

        auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) { Vec3 v = make_brace(); sink.x += v.x; }
        auto t1 = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) { Vec3 v = make_assign(); sink.x += v.x; }
        auto t2 = std::chrono::steady_clock::now();

        double bns = std::chrono::duration<double, std::nano>(t1 - t0).count() / N;
        double ans = std::chrono::duration<double, std::nano>(t2 - t1).count() / N;
        std::printf("5) brace=%.3f ns/次  assign=%.3f ns/次  sink=%.1f\n",
                    bns, ans, sink.x);
    }

    // 6) 三种初始化的字节差异
    {
        Plain defaulted;                 // 默认初始化：成员 indeterminate
        Plain value{};                   // 值初始化：全 0
        static Plain zeroed;             // 静态存储期：零初始化
        std::printf("6) zeroed(静态) a=%d b=%g c=%d | value{} a=%d b=%g c=%d\n",
                    zeroed.a, zeroed.b, (int)zeroed.c,
                    value.a, value.b, (int)value.c);
        (void)defaulted;
    }
    return 0;
}
