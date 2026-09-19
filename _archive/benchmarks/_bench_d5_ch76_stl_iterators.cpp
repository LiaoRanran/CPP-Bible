// _bench_d5_ch76_stl_iterators.cpp
// STL 迭代器类别对遍历性能的影响 — 基准程序
// 编译: g++ -O2 -std=c++23 _bench_d5_ch76_stl_iterators.cpp -o bench_d5_ch76.exe
// 运行: ./bench_d5_ch76.exe
//
// 环境: AMD Ryzen 9 7940HX, GCC 15.3.0 (MinGW-w64), -O2 -std=c++23
// 方法: 5轮取中位, volatile sink 防 DCE

#include <iostream>
#include <vector>
#include <deque>
#include <list>
#include <forward_list>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <chrono>
#include <random>
#include <functional>
#include <cstdint>
#include <cstring>

// ----------------------------------------------------------------
// 计时辅助
// ----------------------------------------------------------------
using Clock = std::chrono::steady_clock;
using Ms = std::chrono::duration<double, std::milli>;

// 取 5 轮中位数
double median5(std::function<double()> fn) {
    double vals[5];
    for (int i = 0; i < 5; ++i) vals[i] = fn();
    // 简单选择排序 5 元素
    for (int i = 0; i < 5; ++i)
        for (int j = i + 1; j < 5; ++j)
            if (vals[j] < vals[i]) {
                double t = vals[i]; vals[i] = vals[j]; vals[j] = t;
            }
    return vals[2];
}

// ----------------------------------------------------------------
// 场景1: 迭代器类别对遍历性能的影响
//   random_access_iterator: vector / deque
//   bidirectional_iterator: list / set
//   forward_iterator:       forward_list / unordered_set
// ----------------------------------------------------------------

static double bench_vector_traverse(int N, volatile long long& sink) {
    std::vector<int> v;
    v.reserve(N);
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) v.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (auto it = v.begin(); it != v.end(); ++it) s += *it;
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_deque_traverse(int N, volatile long long& sink) {
    std::deque<int> d;
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) d.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (auto it = d.begin(); it != d.end(); ++it) s += *it;
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_list_traverse(int N, volatile long long& sink) {
    std::list<int> l;
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) l.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (auto it = l.begin(); it != l.end(); ++it) s += *it;
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_set_traverse(int N, volatile long long& sink) {
    std::set<int> s;
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) s.insert(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long sum = 0;
        auto t0 = Clock::now();
        for (auto it = s.begin(); it != s.end(); ++it) sum += *it;
        auto t1 = Clock::now();
        sink = sum;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_forward_list_traverse(int N, volatile long long& sink) {
    std::forward_list<int> fl;
    std::mt19937 rng(42);
    // forward_list 前插为逆序，先存数组再逐个 push_front
    std::vector<int> tmp;
    tmp.reserve(N);
    for (int i = 0; i < N; ++i) tmp.push_back(static_cast<int>(rng()));
    for (int i = N - 1; i >= 0; --i) fl.push_front(tmp[i]);

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (auto it = fl.begin(); it != fl.end(); ++it) s += *it;
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_unordered_set_traverse(int N, volatile long long& sink) {
    std::unordered_set<int> us;
    us.reserve(N);
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) us.insert(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long sum = 0;
        auto t0 = Clock::now();
        for (auto it = us.begin(); it != us.end(); ++it) sum += *it;
        auto t1 = Clock::now();
        sink = sum;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

// ----------------------------------------------------------------
// 场景2: 连续存储(vector) vs 链式存储(list) 缓存局部性差异
//   同样的元素数，同样 random_access(bare pointer) vs bidirectional(node pointer)
//   对比逐元素累加
// ----------------------------------------------------------------
// 已被场景1覆盖 (vector vs list)，这里额外做 pointer-based 遍历对照

static double bench_raw_pointer_traverse(int N, volatile long long& sink) {
    int* arr = new int[N];
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) arr[i] = static_cast<int>(rng());

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (int* p = arr; p != arr + N; ++p) s += *p;
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    double r = median5(fn);
    delete[] arr;
    return r;
}

// ----------------------------------------------------------------
// 场景3: 迭代器解引用开销 — 连续 vs 非连续内存
//   vector::iterator (连续)  vs  list::iterator (非连续, 指针跳转)
//   通过 stride 访问模式隔离解引用开销
// ----------------------------------------------------------------

static double bench_vector_strided(int N, int stride, volatile long long& sink) {
    std::vector<int> v;
    v.resize(N);
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) v[i] = static_cast<int>(rng());

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        for (int i = 0; i < N; i += stride) s += v[i];
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_list_strided(int N, int stride, volatile long long& sink) {
    std::list<int> l;
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) l.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        volatile long long s = 0;
        auto t0 = Clock::now();
        int i = 0;
        for (auto it = l.begin(); it != l.end() && i < N; ++it, ++i) {
            if (i % stride == 0) s += *it;
        }
        auto t1 = Clock::now();
        sink = s;
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

// ----------------------------------------------------------------
// 场景4: std::sort (需 random_access) vs std::list::sort (需 bidirectional)
//   算法复杂度: std::sort ~ O(N log N) introsort
//               list::sort ~ O(N log N) merge sort
//   但实际性能差异巨大，因缓存友好性不同
// ----------------------------------------------------------------

static double bench_vector_sort(int N, volatile long long& sink) {
    std::vector<int> v;
    v.reserve(N);
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) v.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        // 每轮重新打乱
        std::vector<int> copy = v;
        auto t0 = Clock::now();
        std::sort(copy.begin(), copy.end());
        auto t1 = Clock::now();
        sink = copy[0];
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

static double bench_list_sort(int N, volatile long long& sink) {
    std::list<int> l;
    std::mt19937 rng(42);
    for (int i = 0; i < N; ++i) l.push_back(static_cast<int>(rng()));

    auto fn = [&]() -> double {
        // 每轮重新打乱 (用原始顺序重新拷贝)
        std::list<int> copy = l;
        auto t0 = Clock::now();
        copy.sort();
        auto t1 = Clock::now();
        sink = *copy.begin();
        return std::chrono::duration<double, std::milli>(t1 - t0).count();
    };
    return median5(fn);
}

// ----------------------------------------------------------------
// 主函数
// ----------------------------------------------------------------
int main() {
    constexpr int N_TRAVERSE = 2'000'000;  // 遍历场景: 2M 元素
    constexpr int N_SORT     = 500'000;     // 排序场景: 500K 元素
    constexpr int STRIDE     = 8;           // 步长访问 stride

    volatile long long sink = 0;

    std::cout << "=== D5 Benchmark: ch76 STL Iterators ===" << std::endl;
    std::cout << "CPU: AMD Ryzen 9 7940HX, GCC 15.3.0, -O2 -std=c++23" << std::endl;
    std::cout << "Method: 5-round median, volatile sink" << std::endl;
    std::cout << std::endl;

    // 场景1: 迭代器类别对遍历性能的影响
    std::cout << "--- Scenario 1: Iterator category traversal (N=" << N_TRAVERSE << ") ---" << std::endl;
    double t_vec   = bench_vector_traverse(N_TRAVERSE, sink);
    double t_deque = bench_deque_traverse(N_TRAVERSE, sink);
    double t_list  = bench_list_traverse(N_TRAVERSE, sink);
    double t_set   = bench_set_traverse(N_TRAVERSE, sink);
    double t_flist = bench_forward_list_traverse(N_TRAVERSE, sink);
    double t_uset  = bench_unordered_set_traverse(N_TRAVERSE, sink);

    std::cout << "vector (random_access)  : " << t_vec   << " ms" << std::endl;
    std::cout << "deque  (random_access)  : " << t_deque << " ms" << std::endl;
    std::cout << "list   (bidirectional)   : " << t_list  << " ms" << std::endl;
    std::cout << "set    (bidirectional)   : " << t_set   << " ms" << std::endl;
    std::cout << "fwd_lst(forward)        : " << t_flist << " ms" << std::endl;
    std::cout << "u_set  (forward)        : " << t_uset  << " ms" << std::endl;
    std::cout << "speedup vec/list        : " << (t_list / t_vec)   << "x" << std::endl;
    std::cout << "speedup vec/set         : " << (t_set / t_vec)    << "x" << std::endl;
    std::cout << "speedup vec/fwd_lst     : " << (t_flist / t_vec) << "x" << std::endl;
    std::cout << "speedup vec/u_set       : " << (t_uset / t_vec)  << "x" << std::endl;
    std::cout << std::endl;

    // 场景2: 连续存储 vs 链式存储 — 缓存局部性差异 (裸指针 vs vector vs list)
    std::cout << "--- Scenario 2: Contiguous vs linked storage (N=" << N_TRAVERSE << ") ---" << std::endl;
    double t_raw = bench_raw_pointer_traverse(N_TRAVERSE, sink);
    std::cout << "raw pointer (contiguous) : " << t_raw  << " ms" << std::endl;
    std::cout << "vector (contiguous)      : " << t_vec  << " ms" << std::endl;
    std::cout << "list (linked)             : " << t_list << " ms" << std::endl;
    std::cout << "speedup raw/list          : " << (t_list / t_raw) << "x" << std::endl;
    std::cout << "speedup raw/vector        : " << (t_vec / t_raw)  << "x" << std::endl;
    std::cout << std::endl;

    // 场景3: 迭代器解引用开销 — 步长访问
    std::cout << "--- Scenario 3: Dereference overhead, stride=" << STRIDE << " (N=" << N_TRAVERSE << ") ---" << std::endl;
    double t_v_stride = bench_vector_strided(N_TRAVERSE, STRIDE, sink);
    double t_l_stride = bench_list_strided(N_TRAVERSE, STRIDE, sink);
    std::cout << "vector strided(" << STRIDE << ")    : " << t_v_stride << " ms" << std::endl;
    std::cout << "list   strided(" << STRIDE << ")    : " << t_l_stride << " ms" << std::endl;
    std::cout << "speedup vec_stride/list_stride : " << (t_l_stride / t_v_stride) << "x" << std::endl;
    std::cout << std::endl;

    // 场景4: std::sort vs list::sort
    std::cout << "--- Scenario 4: std::sort (RA) vs list::sort (BD) (N=" << N_SORT << ") ---" << std::endl;
    double t_v_sort = bench_vector_sort(N_SORT, sink);
    double t_l_sort = bench_list_sort(N_SORT, sink);
    std::cout << "std::sort(vector)  : " << t_v_sort << " ms" << std::endl;
    std::cout << "list::sort(list)    : " << t_l_sort << " ms" << std::endl;
    std::cout << "speedup vec_sort/list_sort : " << (t_l_sort / t_v_sort) << "x" << std::endl;
    std::cout << std::endl;

    std::cout << "=== Done ===" << std::endl;
    return 0;
}
