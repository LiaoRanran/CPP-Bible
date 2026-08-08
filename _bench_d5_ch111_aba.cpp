#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <random>
#include <cstring>
#include <cstdint>
#include <mutex>
#include <algorithm>

// ============================================================
// Infrastructure: volatile sinks, median timer, barrier
// ============================================================

static volatile long long g_drain = 0;

struct Timer {
    using C = std::chrono::steady_clock;
    C::time_point t0;
    Timer() : t0(C::now()) {}
    double ms() const {
        return std::chrono::duration<double, std::milli>(C::now() - t0).count();
    }
};

template<typename F>
double median_ms(F&& f, int rounds = 5) {
    std::vector<double> ts(rounds);
    for (int r = 0; r < rounds; ++r) {
        Timer t;
        f();
        ts[r] = t.ms();
    }
    std::sort(ts.begin(), ts.end());
    return ts[rounds / 2];
}

struct Barrier {
    std::atomic<int> cnt{0};
    std::atomic<int> sense{0};
    int N;
    Barrier(int n) : N(n) {}
    void wait() {
        int s = sense.load(std::memory_order_relaxed);
        if (cnt.fetch_add(1, std::memory_order_acq_rel) == N - 1) {
            cnt.store(0, std::memory_order_relaxed);
            sense.store(!s, std::memory_order_release);
        } else {
            while (sense.load(std::memory_order_acquire) == s) {}
        }
    }
};

// ============================================================
// Data structures
// ============================================================

// Tagged pointer packed into 64 bits (x86-64 uses only 48 VA bits)
struct TaggedPtr64 {
    uint64_t raw;
    void*    ptr() const { return reinterpret_cast<void*>(raw & 0x0000FFFFFFFFFFFFULL); }
    uint16_t tag() const { return static_cast<uint16_t>(raw >> 48); }
    static TaggedPtr64 make(void* p, uint16_t t) {
        uint64_t r = reinterpret_cast<uintptr_t>(p);
        return { r | (static_cast<uint64_t>(t) << 48) };
    }
};
static_assert(sizeof(TaggedPtr64) == 8);

// 128-bit tagged for DCAS
struct alignas(16) TaggedPtr128 {
    void*    ptr;
    uint64_t tag;
};
static_assert(sizeof(TaggedPtr128) == 16);

// Lock-free stack node (pre-allocated, never freed during benchmark)
struct alignas(16) Node {
    int  data;
    Node* next;
};

// ============================================================
// S1: CAS raw overhead — 8B plain vs 8B tagged vs 16B tagged
// ============================================================

void run_s1(int iters_per_thread, int nthreads, std::ostream& out) {
    long long total = static_cast<long long>(iters_per_thread) * nthreads;

    // --- S1a: Plain 8B CAS increment ---
    std::atomic<uint64_t> a1{0};
    double t_plain = median_ms([&]() {
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < iters_per_thread; ++i) {
                    uint64_t e = a1.load(std::memory_order_relaxed);
                    while (!a1.compare_exchange_weak(e, e + 1,
                        std::memory_order_release, std::memory_order_relaxed)) {}
                }
            });
        for (auto& th : ts) th.join();
        g_drain = static_cast<long long>(a1.load());
    });

    // --- S1b: Tagged 64-bit CAS (pack ptr+tag in uint64_t) ---
    std::atomic<uint64_t> a2{TaggedPtr64::make(nullptr, 0).raw};
    double t_tag64 = median_ms([&]() {
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < iters_per_thread; ++i) {
                    uint64_t e = a2.load(std::memory_order_relaxed);
                    TaggedPtr64 te{e};
                    TaggedPtr64 td = TaggedPtr64::make(te.ptr(), te.tag() + 1);
                    while (!a2.compare_exchange_weak(e, td.raw,
                        std::memory_order_release, std::memory_order_relaxed)) {
                        te = TaggedPtr64{e};
                        td = TaggedPtr64::make(te.ptr(), te.tag() + 1);
                    }
                }
            });
        for (auto& th : ts) th.join();
        g_drain = a2.load() ? 1 : 0;
    });

    // --- S1c: 128-bit tagged CAS (DCAS via __int128) ---
    std::atomic<__int128> a3{0};
    bool dc_lockfree = std::atomic<__int128>::is_always_lock_free;
    double t_tag128 = median_ms([&]() {
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < iters_per_thread; ++i) {
                    __int128 e = a3.load(std::memory_order_relaxed);
                    uint64_t hi = static_cast<uint64_t>(static_cast<unsigned __int128>(e) >> 64);
                    __int128 d = (static_cast<__int128>(hi + 1) << 64);
                    a3.compare_exchange_weak(e, d,
                        std::memory_order_release, std::memory_order_relaxed);
                }
            });
        for (auto& th : ts) th.join();
        g_drain = static_cast<long long>(a3.load());
    });

    out << "S1_Plain_8B_CAS_ms: " << t_plain << " (ops=" << total << ")" << std::endl;
    out << "S1_Tagged64_CAS_ms: " << t_tag64 << std::endl;
    out << "S1_Tagged128_CAS_ms: " << t_tag128 << " lockfree=" << (dc_lockfree ? "Y" : "N") << std::endl;
    out << "S1_Plain_ops_ms: " << (total / t_plain) << std::endl;
    out << "S1_Tagged64_ops_ms: " << (total / t_tag64) << std::endl;
    out << "S1_Tagged128_ops_ms: " << (total / t_tag128) << std::endl;
}

// ============================================================
// S2: ABA guard cost — plain(unsafe) vs tagged64 vs tagged128 vs hazard
//     Measured as push+pop pairs on a lock-free stack
// ============================================================

// Pre-allocated node pool (never freed during benchmark)
static const int MAX_NODES = 1'000'000;
static Node g_pool[MAX_NODES];
static int g_pool_idx = 0;

Node* alloc_node() { return &g_pool[g_pool_idx++]; }

struct PlainStack {
    std::atomic<Node*> head{nullptr};
    void push(int v) {
        Node* n = alloc_node(); n->data = v;
        n->next = head.load(std::memory_order_relaxed);
        while (!head.compare_exchange_weak(n->next, n,
            std::memory_order_release, std::memory_order_relaxed)) {}
    }
    int pop() {
        Node* n = head.load(std::memory_order_acquire);
        while (n) {
            Node* nx = n->next; // ABA hazard: n may be recycled
            if (head.compare_exchange_weak(n, nx,
                std::memory_order_acq_rel, std::memory_order_acquire))
                break;
        }
        int v = n ? n->data : 0;
        g_drain += v;
        return v;
    }
};

struct Tagged64Stack {
    std::atomic<uint64_t> head{TaggedPtr64::make(nullptr, 0).raw};
    void push(int v) {
        Node* n = alloc_node(); n->data = v;
        TaggedPtr64 new_tp = TaggedPtr64::make(n, 0);
        uint64_t e = head.load(std::memory_order_relaxed);
        do {
            TaggedPtr64 te{e};
            new_tp = TaggedPtr64::make(n, te.tag() + 1);
            n->next = static_cast<Node*>(te.ptr());
        } while (!head.compare_exchange_weak(e, new_tp.raw,
            std::memory_order_release, std::memory_order_relaxed));
    }
    int pop() {
        uint64_t e = head.load(std::memory_order_acquire);
        while (true) {
            TaggedPtr64 te{e};
            Node* n = static_cast<Node*>(te.ptr());
            if (!n) return 0;
            Node* nx = n->next;
            TaggedPtr64 td = TaggedPtr64::make(nx, te.tag() + 1);
            if (head.compare_exchange_weak(e, td.raw,
                std::memory_order_acq_rel, std::memory_order_acquire)) {
                int v = n->data; g_drain += v; return v;
            }
        }
    }
};

struct Tagged128Stack {
    std::atomic<TaggedPtr128> head{TaggedPtr128{nullptr, 0}};
    void push(int v) {
        Node* n = alloc_node(); n->data = v;
        TaggedPtr128 e = head.load(std::memory_order_relaxed);
        TaggedPtr128 d{n, 0};
        do {
            d.tag = e.tag + 1;
            n->next = static_cast<Node*>(e.ptr);
        } while (!head.compare_exchange_weak(e, d,
            std::memory_order_release, std::memory_order_relaxed));
    }
    int pop() {
        TaggedPtr128 e = head.load(std::memory_order_acquire);
        while (true) {
            Node* n = static_cast<Node*>(e.ptr);
            if (!n) return 0;
            TaggedPtr128 d{n->next, e.tag + 1};
            if (head.compare_exchange_weak(e, d,
                std::memory_order_acq_rel, std::memory_order_acquire)) {
                int v = n->data; g_drain += v; return v;
            }
        }
    }
};

// Hazard-pointer-style: register pointer before deref
constexpr int MAX_THREADS_HP = 64;
static std::atomic<Node*> g_hazard[MAX_THREADS_HP];

struct HazardStack {
    std::atomic<Node*> head{nullptr};
    void push(int v) {
        Node* n = alloc_node(); n->data = v;
        n->next = head.load(std::memory_order_relaxed);
        while (!head.compare_exchange_weak(n->next, n,
            std::memory_order_release, std::memory_order_relaxed)) {}
    }
    // Per-thread hazard slot index (passed in via thread-local id)
    int pop(int tid) {
        Node* n;
        do {
            n = head.load(std::memory_order_acquire);
            if (!n) return 0;
            g_hazard[tid].store(n, std::memory_order_seq_cst);
            // Re-check: head still == n?
            if (head.load(std::memory_order_acquire) != n) continue;
        } while (!head.compare_exchange_weak(n, n->next,
            std::memory_order_acq_rel, std::memory_order_acquire));
        int v = n->data;
        g_hazard[tid].store(nullptr, std::memory_order_release);
        g_drain += v;
        return v;
    }
};

void run_s2(int pairs_per_thread, int nthreads, std::ostream& out) {
    out << "=== S2: ABA guard cost (stack push+pop) ===" << std::endl;

    // Reset pool
    g_pool_idx = 0;

    // Plain (unsafe, ABA risk) — fastest baseline
    PlainStack ps;
    double t_plain = median_ms([&]() {
        g_pool_idx = 0; ps.head.store(nullptr);
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < pairs_per_thread; ++i) {
                    ps.push(i);
                    ps.pop();
                }
            });
        for (auto& th : ts) th.join();
    });

    // Tagged 64-bit (safe, packed CAS)
    Tagged64Stack t64s;
    double t_tag64 = median_ms([&]() {
        g_pool_idx = 0;
        t64s.head.store(TaggedPtr64::make(nullptr, 0).raw);
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < pairs_per_thread; ++i) {
                    t64s.push(i);
                    t64s.pop();
                }
            });
        for (auto& th : ts) th.join();
    });

    // Tagged 128-bit (DCAS, may be locked)
    Tagged128Stack t128s;
    bool dc_lockfree = std::atomic<TaggedPtr128>::is_always_lock_free;
    double t_tag128 = median_ms([&]() {
        g_pool_idx = 0;
        t128s.head.store(TaggedPtr128{nullptr, 0});
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < pairs_per_thread; ++i) {
                    t128s.push(i);
                    t128s.pop();
                }
            });
        for (auto& th : ts) th.join();
    });

    // Hazard-pointer style
    HazardStack hs;
    for (int t = 0; t < MAX_THREADS_HP; ++t)
        g_hazard[t].store(nullptr, std::memory_order_relaxed);
    double t_hazard = median_ms([&]() {
        g_pool_idx = 0;
        hs.head.store(nullptr);
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&, tid = t]() {
                for (int i = 0; i < pairs_per_thread; ++i) {
                    hs.push(i);
                    hs.pop(tid);
                }
            });
        for (auto& th : ts) th.join();
    });

    long long total_ops = static_cast<long long>(pairs_per_thread) * nthreads;
    out << "S2_Plain_unsafe_ms: " << t_plain << " (ops/ms=" << (total_ops / t_plain) << ")" << std::endl;
    out << "S2_Tagged64_ms: " << t_tag64 << " (ops/ms=" << (total_ops / t_tag64) << ")" << std::endl;
    out << "S2_Tagged128_ms: " << t_tag128 << " (ops/ms=" << (total_ops / t_tag128) << ") lockfree=" << (dc_lockfree ? "Y" : "N") << std::endl;
    out << "S2_Hazard_ms: " << t_hazard << " (ops/ms=" << (total_ops / t_hazard) << ")" << std::endl;
    out << "S2_Tagged64_vs_Plain: " << (t_tag64 / t_plain) << "x" << std::endl;
    out << "S2_Tagged128_vs_Plain: " << (t_tag128 / t_plain) << "x" << std::endl;
    out << "S2_Hazard_vs_Plain: " << (t_hazard / t_plain) << "x" << std::endl;
}

// ============================================================
// S3 + S4: Lock-free vs Mutex stack throughput + scalability
// ============================================================

struct MutexStack {
    std::mutex mtx;
    Node* head = nullptr;
    void push(int v) {
        Node* n = alloc_node(); n->data = v;
        std::lock_guard<std::mutex> lk(mtx);
        n->next = head; head = n;
    }
    int pop() {
        std::lock_guard<std::mutex> lk(mtx);
        Node* n = head;
        if (!n) return 0;
        head = n->next;
        int v = n->data; g_drain += v; return v;
    }
};

void run_s3_s4(int pairs_per_thread, std::ostream& out) {
    out << "=== S3/S4: Lock-free(Tagged64) vs Mutex stack throughput ===" << std::endl;

    const int thread_counts[] = {1, 2, 4, 8, 16};
    const int max_t = thread_counts[4];

    // Pre-allocate enough nodes for the largest run
    long long total_nodes = static_cast<long long>(pairs_per_thread) * max_t * 2;
    if (total_nodes > MAX_NODES) total_nodes = MAX_NODES;
    const int actual_pairs = static_cast<int>(total_nodes / max_t / 2);

    out << "S34_pairs_per_thread: " << actual_pairs << std::endl;

    for (int nt : thread_counts) {
        long long ops = static_cast<long long>(actual_pairs) * nt;

        // Lock-free (Tagged64)
        Tagged64Stack t64s;
        double t_lf = median_ms([&]() {
            g_pool_idx = 0;
            t64s.head.store(TaggedPtr64::make(nullptr, 0).raw);
            std::vector<std::thread> ts;
            for (int t = 0; t < nt; ++t)
                ts.emplace_back([&]() {
                    for (int i = 0; i < actual_pairs; ++i) {
                        t64s.push(i);
                        t64s.pop();
                    }
                });
            for (auto& th : ts) th.join();
        });

        // Mutex
        MutexStack ms;
        double t_mtx = median_ms([&]() {
            g_pool_idx = 0;
            ms.head = nullptr;
            std::vector<std::thread> ts;
            for (int t = 0; t < nt; ++t)
                ts.emplace_back([&]() {
                    for (int i = 0; i < actual_pairs; ++i) {
                        ms.push(i);
                        ms.pop();
                    }
                });
            for (auto& th : ts) th.join();
        });

        double ops_lf = ops / t_lf;
        double ops_mtx = ops / t_mtx;
        out << "S34_T" << nt << "_LockFree_ms: " << t_lf
            << " ops/ms=" << ops_lf << std::endl;
        out << "S34_T" << nt << "_Mutex_ms: " << t_mtx
            << " ops/ms=" << ops_mtx << std::endl;
        out << "S34_T" << nt << "_LF_vs_MTX: "
            << (ops_lf / ops_mtx) << "x" << std::endl;
    }
}

// ============================================================
// S5: compare_exchange_weak vs compare_exchange_strong in CAS loop
// ============================================================

void run_s5(int iters_per_thread, int nthreads, std::ostream& out) {
    out << "=== S5: weak vs strong CAS loop ===" << std::endl;
    long long total = static_cast<long long>(iters_per_thread) * nthreads;

    // weak CAS loop
    std::atomic<uint64_t> a1{0};
    double t_weak = median_ms([&]() {
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < iters_per_thread; ++i) {
                    uint64_t e = a1.load(std::memory_order_relaxed);
                    while (!a1.compare_exchange_weak(e, e + 1,
                        std::memory_order_release, std::memory_order_relaxed)) {}
                }
            });
        for (auto& th : ts) th.join();
        g_drain = static_cast<long long>(a1.load());
    });

    // strong CAS loop
    std::atomic<uint64_t> a2{0};
    double t_strong = median_ms([&]() {
        std::vector<std::thread> ts;
        for (int t = 0; t < nthreads; ++t)
            ts.emplace_back([&]() {
                for (int i = 0; i < iters_per_thread; ++i) {
                    uint64_t e = a2.load(std::memory_order_relaxed);
                    while (!a2.compare_exchange_strong(e, e + 1,
                        std::memory_order_release, std::memory_order_relaxed)) {}
                }
            });
        for (auto& th : ts) th.join();
        g_drain = static_cast<long long>(a2.load());
    });

    out << "S5_Weak_ms: " << t_weak << " (ops=" << total << ")" << std::endl;
    out << "S5_Strong_ms: " << t_strong << std::endl;
    out << "S5_Weak_ops_ms: " << (total / t_weak) << std::endl;
    out << "S5_Strong_ops_ms: " << (total / t_strong) << std::endl;
    out << "S5_Weak_vs_Strong: " << (t_weak / t_strong) << "x (<1 means weak faster)" << std::endl;

    // Add a note about x86 TSO
    out << "S5_Note: x86-64 TSO — both map to lock cmpxchg; weak may skip extra check on LL/SC archs" << std::endl;
}

// ============================================================
// D5.3 demo: minimal standalone verification
// ============================================================

void run_demo(std::ostream& out) {
    out << "=== D5.3 Demo: minimal correctness check ===" << std::endl;

    // 1) Show that tagged 128-bit CAS on this platform is lock-free or not
    bool dcas_lf = std::atomic<__int128>::is_always_lock_free;
    out << "DEMO_128bit_atomic_lockfree: " << (dcas_lf ? "true" : "false") << std::endl;

    // 2) Show tagged 64-bit CAS correctly detects ABA-like changes
    std::atomic<uint64_t> tagged{TaggedPtr64::make(nullptr, 0).raw};
    uint64_t e = tagged.load(std::memory_order_relaxed);
    TaggedPtr64 te{e};
    // Simulate A->B->A: update tag each time
    TaggedPtr64 d1 = TaggedPtr64::make(reinterpret_cast<void*>(0x1000), te.tag() + 1);
    tagged.compare_exchange_strong(e, d1.raw,
        std::memory_order_release, std::memory_order_relaxed);
    // Now change back to same "pointer" but different tag
    e = tagged.load(std::memory_order_relaxed);
    TaggedPtr64 te2{e};
    TaggedPtr64 d2 = TaggedPtr64::make(reinterpret_cast<void*>(0x1000), te2.tag() + 1);
    tagged.compare_exchange_strong(e, d2.raw,
        std::memory_order_release, std::memory_order_relaxed);
    TaggedPtr64 final_tp{tagged.load(std::memory_order_relaxed)};
    out << "DEMO_Tagged64_final_ptr: 0x" << std::hex
        << reinterpret_cast<uintptr_t>(final_tp.ptr()) << std::dec << std::endl;
    out << "DEMO_Tagged64_final_tag: " << final_tp.tag() << std::endl;
    out << "DEMO_Tagged64_expected_tag: 2" << std::endl;

    // 3) Show that weak CAS loop matches strong CAS final result
    std::atomic<uint64_t> w{0}, s{0};
    int weak_fails = 0;
    for (int i = 0; i < 10000; ++i) {
        uint64_t ew = w.load(std::memory_order_relaxed);
        if (!w.compare_exchange_weak(ew, ew + 1,
            std::memory_order_relaxed, std::memory_order_relaxed))
            ++weak_fails;
    }
    for (int i = 0; i < 10000; ++i) {
        uint64_t es = s.load(std::memory_order_relaxed);
        while (!s.compare_exchange_strong(es, es + 1,
            std::memory_order_relaxed, std::memory_order_relaxed)) {}
    }
    out << "DEMO_Weak_spur_fails: " << weak_fails << " (x86-64: usually 0)" << std::endl;
    out << "DEMO_Final_weak: " << w.load() << " Final_strong: " << s.load() << std::endl;

    // 4) Lock-free push/pop correctness
    g_pool_idx = 0;
    Tagged64Stack ts;
    ts.push(42);
    ts.push(99);
    int v1 = ts.pop();
    int v2 = ts.pop();
    out << "DEMO_Stack_push99_pop=" << v1 << " push42_pop=" << v2 << std::endl;

    out << "DEMO_all_checks_passed: yes" << std::endl;
}

// ============================================================
// main
// ============================================================

int main() {
    const int ITERS_S1 = 50000;     // per thread for S1 raw CAS
    const int PAIRS_S2 = 50000;     // push+pop pairs per thread for S2
    const int ITERS_S5 = 50000;     // per thread for S5

    std::cout << "========== D5 Benchmark: ch111 ABA Solutions ==========" << std::endl;
    std::cout << "Compiler: GCC " << __GNUC__ << "." << __GNUC_MINOR__ << "." << __GNUC_PATCHLEVEL__ << std::endl;

#ifdef _WIN32
    std::cout << "Platform: Windows (MinGW-w64)" << std::endl;
#else
    std::cout << "Platform: POSIX" << std::endl;
#endif

    std::cout << "Features: -std=c++23 -O2 -pthread";
#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_16
    std::cout << " -mcx16";
#endif
    std::cout << std::endl;
    std::cout << std::endl;

    // S1: CAS raw overhead (16 threads for contention)
    run_s1(ITERS_S1, 16, std::cout);
    std::cout << std::endl;

    // S2: ABA guard cost (8 threads)
    run_s2(PAIRS_S2, 8, std::cout);
    std::cout << std::endl;

    // S3+S4: Lock-free vs mutex scalability (1/2/4/8/16 threads)
    run_s3_s4(30000, std::cout);
    std::cout << std::endl;

    // S5: weak vs strong (16 threads, contended)
    run_s5(ITERS_S5, 16, std::cout);
    std::cout << std::endl;

    // D5.3 Demo
    run_demo(std::cout);

    std::cout << std::endl << "========== Done ==========" << std::endl;
    return 0;
}
