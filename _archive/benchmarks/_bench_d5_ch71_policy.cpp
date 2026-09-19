// _bench_d5_ch71_policy.cpp — ch71 Policy-Based Design：编译期策略选择 vs 运行时多态
// g++ -O2 -std=c++23 _bench_d5_ch71_policy.cpp -o bench71
//
// 方法学：每个子基准跑 5 轮取中位；volatile sink 防 DCE；
// 循环体用依赖链，使 sum 无闭式解，编译器无法把整个循环折叠成常数。
//
// 四个场景：
//   S1: Policy 排序（模板参数 Comparator）vs std::function comparator
//   S2: Policy 容器（模板参数 Transform 策略）vs 虚函数策略
//   S3: 模板策略内联 vs 函数指针间接跳转
//   S4: 多策略组合（3 个策略参数）的运行时零开销 vs 虚函数分派
//
// 关键：S2/S3/S4 的运行时间接版本均通过 volatile 全局指针或混合类型数组
// 阻止 GCC 去虚拟化（devirtualization），确保间接调用真实发生。

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <random>
#include <vector>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) {
        double t0 = now_ms();
        f();
        t.push_back(now_ms() - t0);
    }
    std::vector<double> raw = t;
    std::sort(t.begin(), t.end());
    std::printf("%-48s median %9.3f ms   raw:", name, t[2]);
    for (double v : raw) std::printf(" %.3f", v);
    std::printf("\n");
    return t[2];
}

volatile std::uint64_t g_sink;
volatile void* g_escape;

// 依赖链：读出值混入下一次写入 —— 无闭式解，不可折叠
#define DEP(s, val) s = s * 1315423911ull + static_cast<std::uint64_t>(val)

// ================================================================
// S1: Policy 排序（模板参数 Comparator）vs std::function comparator
// ================================================================

// 策略：比较器（无状态空结构体，可被 EBO 优化）
struct LessCmp    { static bool less(int a, int b) { return a < b; } };
struct GreaterCmp { static bool less(int a, int b) { return a > b; } };

// Policy-based 插入排序：Comparator 是模板参数，比较操作完全内联
template <typename Cmp>
void insertion_sort_policy(int* a, int n) {
    for (int i = 1; i < n; ++i) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && Cmp::less(key, a[j])) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = key;
    }
}

// std::function 版本：每次比较都是间接调用（类型擦除 + 内部间接跳转）
void insertion_sort_func(int* a, int n, std::function<bool(int, int)> cmp) {
    for (int i = 1; i < n; ++i) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && cmp(key, a[j])) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = key;
    }
}

// ================================================================
// S2: Policy 容器（模板参数 Transform 策略）vs 虚函数策略
// ================================================================

// 策略：每次插入时的变换
struct TransformIdentity { static int transform(int v) { return v; } };
struct TransformOffset   { static int transform(int v) { return v + 1; } };

// Policy-based 容器：Transform 策略是模板参数，push 时变换被内联
template <typename Transform>
struct PolicyContainer {
    int* data;
    int size;
    int cap;
    PolicyContainer(int c) : data(new int[c]), size(0), cap(c) {}
    ~PolicyContainer() { delete[] data; }
    void push(int v) {
        if (size < cap) {
            data[size++] = Transform::transform(v);
        }
    }
};

// 虚函数策略容器：每次 push 走 vtable 间接调用
struct VTransform {
    virtual int transform(int) = 0;
    virtual ~VTransform() = default;
};
struct VTransformIdentity : VTransform { int transform(int v) override { return v; } };
struct VTransformOffset   : VTransform { int transform(int v) override { return v + 1; } };

struct VirtualContainer {
    int* data;
    int size;
    int cap;
    VTransform* strategy;
    VirtualContainer(int c, VTransform* s) : data(new int[c]), size(0), cap(c), strategy(s) {}
    ~VirtualContainer() { delete[] data; }
    void push(int v) {
        if (size < cap) {
            data[size++] = strategy->transform(v);
        }
    }
};

// volatile 全局指针：阻止 GCC 去虚拟化
// 编译器无法在编译期确定 strategy 指向哪个派生类，必须走 vtable
static volatile VTransform* g_vtransform = nullptr;

// ================================================================
// S3: 模板策略内联 vs 函数指针间接跳转
// ================================================================

// 策略：逐元素变换（含位运算，不易被向量化）
struct OpScramble { static int apply(int x) { return (x ^ 0x5A5A) * 2654435761u; } };

// Policy-based transform：Op 被完全内联进循环
template <typename Op>
void transform_policy(int* a, int n) {
    for (int i = 0; i < n; ++i)
        a[i] = Op::apply(a[i]);
}

// 函数指针版本：每次调用都是间接跳转
void transform_fptr(int* a, int n, int (*op)(int)) {
    for (int i = 0; i < n; ++i)
        a[i] = op(a[i]);
}

int op_scramble_fn(int x) { return (x ^ 0x5A5A) * 2654435761u; }

// volatile 函数指针：阻止 GCC 通过指针分析内联目标
static int (*volatile g_fptr)(int) = nullptr;

// ================================================================
// S4: 多策略组合（3 个策略参数）的运行时零开销 vs 虚函数分派
// ================================================================

// 策略 1: 线程安全（无状态空结构体）
struct NoLock  { static void lock() {} static void unlock() {} };

// 策略 2: 变换
struct PassThrough { static int apply(int v) { return v; } };

// 策略 3: 日志（无状态空结构体）
struct NoLog { static void log(const char*) {} };

// Policy-based 多策略宿主：3 个策略参数，无状态策略全部编译消除
template <typename TP, typename CP, typename LP>
struct Worker {
    static int process(int v) {
        TP::lock();
        int r = CP::apply(v);
        LP::log("process");
        TP::unlock();
        return r;
    }
};

// 虚函数多策略宿主：每次 process 产生 4 次间接调用 (lock + apply + log + unlock)
struct VThread {
    virtual void lock() = 0;
    virtual void unlock() = 0;
    virtual ~VThread() = default;
};
struct VNoLock : VThread { void lock() override {} void unlock() override {} };
struct VSpinLock : VThread {
    void lock() override {}
    void unlock() override {}
};

struct VCompute {
    virtual int apply(int) = 0;
    virtual ~VCompute() = default;
};
struct VPassThrough : VCompute { int apply(int v) override { return v; } };
struct VDouble : VCompute { int apply(int v) override { return v * 2; } };

struct VLog {
    virtual void log(const char*) = 0;
    virtual ~VLog() = default;
};
struct VNoLog : VLog { void log(const char*) override {} };
struct VCountLog : VLog { void log(const char*) override {} };

struct VWorker {
    VThread* tp;
    VCompute* cp;
    VLog* lp;
    VWorker(VThread* t, VCompute* c, VLog* l) : tp(t), cp(c), lp(l) {}
    int process(int v) {
        tp->lock();
        int r = cp->apply(v);
        lp->log("process");
        tp->unlock();
        return r;
    }
};

// 混合类型数组：两种不同的 VWorker 配置交替使用
// 阻止 GCC 去虚拟化 —— 编译器无法确定每次迭代调用哪个派生类
static VWorker* g_workers[2] = {nullptr, nullptr};

// ================================================================
// main
// ================================================================

int main() {
    std::mt19937 rng(std::random_device{}());

    // ===== S1: 排序比较器 =====
    // 插入排序 O(n^2)，比较次数 ~n^2/2，放大比较器开销
    constexpr int S1_N = 64;
    constexpr int S1_REP = 200000;
    std::vector<int> arr1(S1_N);
    for (int i = 0; i < S1_N; ++i) arr1[i] = rng();
    g_escape = arr1.data();

    {
        std::vector<int> work(S1_N);
        bench("S1a policy_sort  (template Cmp)", [&] {
            std::uint64_t s = 0;
            for (int r = 0; r < S1_REP; ++r) {
                std::copy(arr1.begin(), arr1.end(), work.begin());
                insertion_sort_policy<LessCmp>(work.data(), S1_N);
                DEP(s, work[0]);
            }
            g_sink = s;
        });
        bench("S1b func_sort    (std::function)", [&] {
            std::uint64_t s = 0;
            std::function<bool(int, int)> cmp = [](int a, int b) { return a < b; };
            for (int r = 0; r < S1_REP; ++r) {
                std::copy(arr1.begin(), arr1.end(), work.begin());
                insertion_sort_func(work.data(), S1_N, cmp);
                DEP(s, work[0]);
            }
            g_sink = s;
        });
    }

    // ===== S2: 容器变换策略 =====
    // 每次插入调用一次策略，策略开销是主要测量对象
    constexpr int S2_N = 1000000;
    constexpr int S2_REP = 5;
    std::vector<int> vals2(S2_N);
    for (int i = 0; i < S2_N; ++i) vals2[i] = rng();
    g_escape = vals2.data();

    {
        bench("S2a policy_container (template)", [&] {
            std::uint64_t s = 0;
            for (int r = 0; r < S2_REP; ++r) {
                PolicyContainer<TransformIdentity> c(S2_N);
                for (int i = 0; i < S2_N; ++i) {
                    c.push(vals2[i]);
                    DEP(s, c.data[c.size - 1]);
                }
            }
            g_sink = s;
        });
        // 虚函数版：通过 volatile 全局指针设置策略，阻止去虚拟化
        VTransformIdentity vts;
        VTransformOffset vto;
        // 运行期随机选择策略实例，编译器无法确定具体类型
        g_vtransform = (rng() & 1) ? static_cast<VTransform*>(&vts) : static_cast<VTransform*>(&vto);
        bench("S2b virtual_container (vtable)", [&] {
            std::uint64_t s = 0;
            for (int r = 0; r < S2_REP; ++r) {
                VirtualContainer c(S2_N, const_cast<VTransform*>(g_vtransform));
                for (int i = 0; i < S2_N; ++i) {
                    c.push(vals2[i]);
                    DEP(s, c.data[c.size - 1]);
                }
            }
            g_sink = s;
        });
    }

    // ===== S3: 内联 vs 间接跳转 =====
    constexpr int S3_N = 4000000;
    constexpr int S3_REP = 3;
    std::vector<int> arr3(S3_N);
    for (int i = 0; i < S3_N; ++i) arr3[i] = rng() & 0xFFFF;
    g_escape = arr3.data();

    {
        bench("S3a policy_transform (inline)", [&] {
            std::uint64_t s = 0;
            for (int r = 0; r < S3_REP; ++r) {
                std::vector<int> work = arr3;
                transform_policy<OpScramble>(work.data(), S3_N);
                DEP(s, work[0]);
            }
            g_sink = s;
        });
        // 函数指针通过 volatile 全局变量传入，阻止编译器内联
        g_fptr = op_scramble_fn;
        bench("S3b fptr_transform   (indirect)", [&] {
            std::uint64_t s = 0;
            for (int r = 0; r < S3_REP; ++r) {
                std::vector<int> work = arr3;
                transform_fptr(work.data(), S3_N, g_fptr);
                DEP(s, work[0]);
            }
            g_sink = s;
        });
    }

    // ===== S4: 多策略组合 =====
    // 3 个策略参数：NoLock + PassThrough + NoLog
    // 模板版：全部无状态策略编译消除，process 退化为 return v
    // 虚函数版：4 次 vtable 间接调用 (lock + apply + log + unlock)
    // 混合类型数组阻止去虚拟化
    constexpr int S4_N = 50000000;
    {
        bench("S4a policy_worker (3 policies, all noop)", [&] {
            std::uint64_t s = 0;
            for (int i = 0; i < S4_N; ++i) {
                int r = Worker<NoLock, PassThrough, NoLog>::process(i & 0xFFFF);
                DEP(s, r);
            }
            g_sink = s;
        });
        // 两种不同的 VWorker 配置，交替使用阻止去虚拟化
        VNoLock vt1; VPassThrough vcp1; VNoLog vl1;
        VSpinLock vt2; VDouble vcp2; VCountLog vl2;
        VWorker vw1(&vt1, &vcp1, &vl1);
        VWorker vw2(&vt2, &vcp2, &vl2);
        g_workers[0] = &vw1;
        g_workers[1] = &vw2;
        bench("S4b virtual_worker (4 vtable dispatches)", [&] {
            std::uint64_t s = 0;
            for (int i = 0; i < S4_N; ++i) {
                int r = g_workers[i & 1]->process(i & 0xFFFF);
                DEP(s, r);
            }
            g_sink = s;
        });
    }

    std::printf("g_sink = %llu\n", (unsigned long long)g_sink);
    return 0;
}
