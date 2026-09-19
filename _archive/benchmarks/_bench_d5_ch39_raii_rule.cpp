// _bench_d5_ch39_raii_rule.cpp
// 基准：移动语义与 Rule of 5 的真实性能影响
// 编译：g++ -O2 -std=c++23 _bench_d5_ch39_raii_rule.cpp -o _bench_d5_ch39_raii_rule
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <cstring>
#include <utility>
#include <memory>
#include <cassert>
#include <cstdint>
#include <type_traits>
#include <random>

// ============================================================
// volatile sink 防 DCE
// ============================================================
static volatile void* g_sink_ptr = nullptr;
static volatile long long g_sink_val = 0;

// ============================================================
// 计时工具
// ============================================================
using Clock = std::chrono::steady_clock;

static long long median5(long long t[5]) {
    for (int i = 0; i < 5; ++i)
        for (int j = i + 1; j < 5; ++j)
            if (t[j] < t[i]) { long long tmp = t[i]; t[i] = t[j]; t[j] = tmp; }
    return t[2];
}

// ============================================================
// 类型定义
// ============================================================

// Rule of 5 手写：深拷贝 + 移动窃取
class BigData5 {
public:
    char* data_;
    std::size_t size_;
    static char* clone(const char* p, std::size_t n) {
        char* q = new char[n];
        std::memcpy(q, p, n);
        return q;
    }
    explicit BigData5(std::size_t n) : size_(n), data_(new char[n]) {
        for (std::size_t i = 0; i < n; ++i) data_[i] = static_cast<char>(i & 0x7F);
    }
    ~BigData5() noexcept { delete[] data_; }
    BigData5(const BigData5& o) : size_(o.size_), data_(clone(o.data_, o.size_)) {}
    BigData5& operator=(const BigData5& o) {
        if (this != &o) {
            char* tmp = clone(o.data_, o.size_);
            delete[] data_;
            data_ = tmp; size_ = o.size_;
        }
        return *this;
    }
    BigData5(BigData5&& o) noexcept : data_(o.data_), size_(o.size_) {
        o.data_ = nullptr; o.size_ = 0;
    }
    BigData5& operator=(BigData5&& o) noexcept {
        if (this != &o) {
            delete[] data_;
            data_ = o.data_; size_ = o.size_;
            o.data_ = nullptr; o.size_ = 0;
        }
        return *this;
    }
};

// Rule of 0：用 std::vector<char> 管理资源
class BigData0 {
public:
    std::vector<char> data_;
    explicit BigData0(std::size_t n) : data_(n) {
        for (std::size_t i = 0; i < n; ++i) data_[i] = static_cast<char>(i & 0x7F);
    }
};

// trivially copyable 类型
struct TrivialBlock {
    long long v[4];
};
static_assert(std::is_trivially_copyable_v<TrivialBlock>, "must be trivially copyable");

// ============================================================
// 场景 1：move 构造 vs copy 构造（深拷贝类型 BigData5）
// 使用对象池：预分配 N 个源对象，copy 时从池中拷贝，move 时从池中移动
// 然后反向：move 测完后把池重新填充
// 关键：copy 和 move 的计时只包含构造本身，不包含源对象的重建
// ============================================================
static void bench_move_ctor_vs_copy_ctor() {
    constexpr int N = 500000;
    constexpr std::size_t BLK = 1024;  // 1KB per object
    long long times_copy[5], times_move[5];

    for (int round = 0; round < 5; ++round) {
        // 预分配源对象池
        std::vector<BigData5> pool;
        pool.reserve(N);
        for (int i = 0; i < N; ++i) pool.emplace_back(BLK);

        // --- copy 测试：从 pool 逐个拷贝到 dst ---
        std::vector<BigData5> dst_copy;
        dst_copy.reserve(N);
        auto t0 = Clock::now();
        for (int i = 0; i < N; ++i) {
            dst_copy.push_back(pool[i]);  // copy ctor
        }
        auto t1 = Clock::now();
        g_sink_ptr = dst_copy.data();
        g_sink_val = dst_copy[0].data_[0];
        times_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // --- move 测试：从 pool 逐个移动到 dst ---
        // pool 此时仍完好（copy 没动 pool）
        std::vector<BigData5> dst_move;
        dst_move.reserve(N);
        auto t2 = Clock::now();
        for (int i = 0; i < N; ++i) {
            dst_move.push_back(std::move(pool[i]));  // move ctor
        }
        auto t3 = Clock::now();
        g_sink_ptr = dst_move.data();
        g_sink_val = dst_move[0].data_[0];
        times_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();
    }
    long long mc = median5(times_copy);
    long long mm = median5(times_move);
    std::cout << "[S1] move-ctor vs copy-ctor (BigData5, 1KB, N=" << N << "):" << std::endl;
    std::cout << "     copy-ctor median: " << mc << " ms" << std::endl;
    std::cout << "     move-ctor median: " << mm << " ms" << std::endl;
    if (mm > 0) std::cout << "     speedup: " << (double)mc / mm << "x" << std::endl;
}

// ============================================================
// 场景 2：trivially copyable — move 等价于 copy（memcpy）
// 加大数据量到 20M，使用依赖链防折叠
// ============================================================
static void bench_trivially_copyable_move_vs_copy() {
    constexpr int N = 20000000;
    long long times_copy[5], times_move[5];

    for (int round = 0; round < 5; ++round) {
        TrivialBlock src{};
        src.v[0] = 0x42424242;
        src.v[1] = 0xDEADBEEF;
        src.v[2] = 0xCAFEBABE;
        src.v[3] = 0xFEEDFACE;

        // copy
        auto t0 = Clock::now();
        long long accum = 0;
        for (int i = 0; i < N; ++i) {
            TrivialBlock dst = src;   // copy
            accum ^= dst.v[i & 3];    // 依赖链
        }
        g_sink_val = accum;
        auto t1 = Clock::now();
        times_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // move
        accum = 0;
        for (int i = 0; i < N; ++i) {
            TrivialBlock dst = std::move(src);  // "move" == copy for trivially copyable
            accum ^= dst.v[i & 3];
        }
        g_sink_val = accum;
        auto t2 = Clock::now();
        times_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    }
    long long mc = median5(times_copy);
    long long mm = median5(times_move);
    std::cout << "[S2] trivially-copyable: move vs copy (32B, N=" << N << "):" << std::endl;
    std::cout << "     copy median: " << mc << " ms" << std::endl;
    std::cout << "     move median: " << mm << " ms" << std::endl;
    if (mm > 0 && mc > 0) std::cout << "     ratio move/copy: " << (double)mm / mc << "x" << std::endl;
}

// ============================================================
// 场景 3：Rule of 5 手写 vs Rule of 0 编译器生成（copy + move）
// ============================================================
static void bench_rule5_vs_rule0() {
    constexpr int N = 500000;
    constexpr std::size_t BLK = 1024;
    long long times_r5_copy[5], times_r0_copy[5];
    long long times_r5_move[5], times_r0_move[5];

    for (int round = 0; round < 5; ++round) {
        // R5 copy
        std::vector<BigData5> pool5;
        pool5.reserve(N);
        for (int i = 0; i < N; ++i) pool5.emplace_back(BLK);

        std::vector<BigData5> dst5c;
        dst5c.reserve(N);
        auto t0 = Clock::now();
        for (int i = 0; i < N; ++i) dst5c.push_back(pool5[i]);
        auto t1 = Clock::now();
        g_sink_ptr = dst5c.data();
        g_sink_val = dst5c[0].data_[0];
        times_r5_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // R0 copy
        std::vector<BigData0> pool0;
        pool0.reserve(N);
        for (int i = 0; i < N; ++i) pool0.emplace_back(BLK);

        std::vector<BigData0> dst0c;
        dst0c.reserve(N);
        auto t2 = Clock::now();
        for (int i = 0; i < N; ++i) dst0c.push_back(pool0[i]);
        auto t3 = Clock::now();
        g_sink_ptr = dst0c.data();
        g_sink_val = dst0c[0].data_[0];
        times_r0_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();

        // R5 move（pool5 仍完好）
        std::vector<BigData5> dst5m;
        dst5m.reserve(N);
        auto t4 = Clock::now();
        for (int i = 0; i < N; ++i) dst5m.push_back(std::move(pool5[i]));
        auto t5 = Clock::now();
        g_sink_ptr = dst5m.data();
        g_sink_val = dst5m[0].data_[0];
        times_r5_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t5 - t4).count();

        // R0 move（pool0 仍完好）
        std::vector<BigData0> dst0m;
        dst0m.reserve(N);
        auto t6 = Clock::now();
        for (int i = 0; i < N; ++i) dst0m.push_back(std::move(pool0[i]));
        auto t7 = Clock::now();
        g_sink_ptr = dst0m.data();
        g_sink_val = dst0m[0].data_[0];
        times_r0_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t7 - t6).count();
    }
    long long r5c = median5(times_r5_copy);
    long long r0c = median5(times_r0_copy);
    long long r5m = median5(times_r5_move);
    long long r0m = median5(times_r0_move);
    std::cout << "[S3] Rule of 5 vs Rule of 0 (1KB, N=" << N << "):" << std::endl;
    std::cout << "     R5 copy median: " << r5c << " ms" << std::endl;
    std::cout << "     R0 copy median: " << r0c << " ms" << std::endl;
    std::cout << "     R5 move median: " << r5m << " ms" << std::endl;
    std::cout << "     R0 move median: " << r0m << " ms" << std::endl;
    if (r0c > 0 && r5c > 0) std::cout << "     copy ratio R0/R5: " << (double)r0c / r5c << "x" << std::endl;
    if (r0m > 0 && r5m > 0) std::cout << "     move ratio R0/R5: " << (double)r0m / r5m << "x" << std::endl;
}

// ============================================================
// 场景 4：return 值的移动 — NRVO vs std::move（聚焦 move ctor 本身成本）
// ============================================================
// NRVO 路径：返回局部对象，编译器直接在调用方栈上构造
static BigData5 make_nrvo(std::size_t n) {
    BigData5 obj(n);
    return obj;  // NRVO: 无 move/copy
}
// std::move 路径：显式 move，强制走 move ctor
static BigData5 make_move(std::size_t n) {
    BigData5 obj(n);
    return std::move(obj);  // 强制 move ctor
}

static void bench_nrvo_vs_move_return() {
    constexpr int N = 500000;
    constexpr std::size_t BLK = 1024;
    long long times_nrvo[5], times_move[5];

    for (int round = 0; round < 5; ++round) {
        // NRVO
        auto t0 = Clock::now();
        long long acc = 0;
        for (int i = 0; i < N; ++i) {
            BigData5 dst = make_nrvo(BLK);
            acc ^= dst.data_[0];
        }
        g_sink_val = acc;
        auto t1 = Clock::now();
        times_nrvo[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // std::move return
        acc = 0;
        auto t2 = Clock::now();
        for (int i = 0; i < N; ++i) {
            BigData5 dst = make_move(BLK);
            acc ^= dst.data_[0];
        }
        g_sink_val = acc;
        auto t3 = Clock::now();
        times_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();
    }
    long long mn = median5(times_nrvo);
    long long mm = median5(times_move);
    std::cout << "[S4] NRVO vs std::move return (1KB, N=" << N << "):" << std::endl;
    std::cout << "     NRVO median:      " << mn << " ms" << std::endl;
    std::cout << "     std::move median: " << mm << " ms" << std::endl;
    if (mm > 0 && mn > 0) std::cout << "     move overhead vs NRVO: " << (double)mm / mn << "x" << std::endl;
}

// ============================================================
// 场景 5：容器中 push_back(move(x)) vs push_back(x)
// 使用预分配对象池，copy 和 move 都从同一个池取
// ============================================================
static void bench_push_back_move_vs_copy() {
    constexpr int N = 200000;
    constexpr std::size_t BLK = 1024;
    long long times_copy[5], times_move[5];

    for (int round = 0; round < 5; ++round) {
        // 预分配源对象池
        std::vector<BigData5> pool;
        pool.reserve(N);
        for (int i = 0; i < N; ++i) pool.emplace_back(BLK);

        // copy 路径
        std::vector<BigData5> v_copy;
        v_copy.reserve(N);
        auto t0 = Clock::now();
        for (int i = 0; i < N; ++i) {
            v_copy.push_back(pool[i]);  // copy
        }
        auto t1 = Clock::now();
        g_sink_ptr = v_copy.data();
        g_sink_val = v_copy[0].data_[0];
        times_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // move 路径（pool 仍完好，因为 copy 不修改 pool）
        std::vector<BigData5> v_move;
        v_move.reserve(N);
        auto t2 = Clock::now();
        for (int i = 0; i < N; ++i) {
            v_move.push_back(std::move(pool[i]));  // move
        }
        auto t3 = Clock::now();
        g_sink_ptr = v_move.data();
        g_sink_val = v_move[0].data_[0];
        times_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();
    }
    long long mc = median5(times_copy);
    long long mm = median5(times_move);
    std::cout << "[S5] push_back(copy) vs push_back(move) (1KB, N=" << N << "):" << std::endl;
    std::cout << "     push_back(copy) median: " << mc << " ms" << std::endl;
    std::cout << "     push_back(move) median: " << mm << " ms" << std::endl;
    if (mm > 0 && mc > 0) std::cout << "     speedup: " << (double)mc / mm << "x" << std::endl;
}

// ============================================================
// 场景 6：vector<string> 的 move vs copy
// 使用预分配对象池
// ============================================================
static void bench_vector_string_move_vs_copy() {
    constexpr int N = 200000;
    constexpr int STR_LEN = 256;
    long long times_copy[5], times_move[5];

    for (int round = 0; round < 5; ++round) {
        // 预分配源对象池
        std::vector<std::string> pool;
        pool.reserve(N);
        for (int i = 0; i < N; ++i) {
            std::string s(STR_LEN, 'x');
            s[s.size() - 1] = static_cast<char>('A' + (i % 26));
            pool.push_back(std::move(s));
        }

        // copy
        std::vector<std::string> v_copy;
        v_copy.reserve(N);
        auto t0 = Clock::now();
        for (int i = 0; i < N; ++i) {
            v_copy.push_back(pool[i]);  // copy
        }
        auto t1 = Clock::now();
        g_sink_ptr = v_copy.data();
        g_sink_val = v_copy[0][0];
        times_copy[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();

        // move（pool 仍完好）
        std::vector<std::string> v_move;
        v_move.reserve(N);
        auto t2 = Clock::now();
        for (int i = 0; i < N; ++i) {
            v_move.push_back(std::move(pool[i]));  // move
        }
        auto t3 = Clock::now();
        g_sink_ptr = v_move.data();
        g_sink_val = v_move[0][0];
        times_move[round] = std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();
    }
    long long mc = median5(times_copy);
    long long mm = median5(times_move);
    std::cout << "[S6] vector<string> push_back copy vs move (256B strings, N=" << N << "):" << std::endl;
    std::cout << "     copy median: " << mc << " ms" << std::endl;
    std::cout << "     move median: " << mm << " ms" << std::endl;
    if (mm > 0 && mc > 0) std::cout << "     speedup: " << (double)mc / mm << "x" << std::endl;
}

// ============================================================
// main
// ============================================================
int main() {
    std::cout << "=== D5 Benchmark: Move Semantics & Rule of 5 ===" << std::endl;
    std::cout << "Compiler: GCC 15.3.0, -O2 -std=c++23" << std::endl;
    std::cout << "CPU: AMD Ryzen 9 7940HX" << std::endl;
    std::cout << "5 rounds, median reported" << std::endl;
    std::cout << std::endl;

    bench_move_ctor_vs_copy_ctor();
    std::cout << std::endl;

    bench_trivially_copyable_move_vs_copy();
    std::cout << std::endl;

    bench_rule5_vs_rule0();
    std::cout << std::endl;

    bench_nrvo_vs_move_return();
    std::cout << std::endl;

    bench_push_back_move_vs_copy();
    std::cout << std::endl;

    bench_vector_string_move_vs_copy();
    std::cout << std::endl;

    std::cout << "=== Done ===" << std::endl;
    return 0;
}
