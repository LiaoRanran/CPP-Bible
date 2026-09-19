// 真实基准 D5 — ch161 日志库（GCC 15.3.0, -pthread）
// 维度：① 格式化方式对照：ostringstream vs snprintf vs std::format
//       ② 落地策略对照：同步逐条 flush vs 缓冲批量写 vs 后台线程异步
// 诚实背景：ch161 §16 已证明「朴素 mutex 队列 + 平凡 sink」异步反而更慢；
//           本基准让 sink 为真实文件写（昂贵），于是异步把昂贵 IO 移出生产者路径而变快——
//           两种情况都成立，结论取决于 sink 成本（见 D5.2）。
// 防 DCE：格式化结果长度累加到 volatile g_sink；临时日志文件用完 std::remove。
#include <algorithm>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <format>
#include <fstream>
#include <mutex>
#include <queue>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

static volatile long g_sink = 0;
static const char* TMP = "_bench_tmp_logger.log";

double fmt_ostringstream(int N) {
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        int id = i; double v = i * 1.5;
        std::ostringstream os;
        os << "id=" << id << " val=" << v << " extra=" << (id * 2);
        g_sink += (long)os.str().size();
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
double fmt_snprintf(int N) {
    char buf[128];
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        int id = i; double v = i * 1.5;
        int n = std::snprintf(buf, sizeof buf, "id=%d val=%.3f extra=%d", id, v, id * 2);
        g_sink += n;
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
double fmt_stdformat(int N) {
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        int id = i; double v = i * 1.5;
        std::string s = std::format("id={} val={:.3f} extra={}", id, v, id * 2);
        g_sink += (long)s.size();
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

long count_lines(const char* path) {
    std::ifstream f(path);
    long n = 0; char c;
    while (f.get(c)) if (c == '\n') ++n;
    return n;
}

double strat_sync(int N) {
    std::ofstream ofs(TMP, std::ios::trunc);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i)
        ofs << std::format("msg {} val {:.3f}\n", i, i * 1.5);
    ofs.flush();
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    ofs.close();
    return ms;
}
double strat_buffered(int N) {
    std::string buf; buf.reserve((std::size_t)N * 40);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i)
        buf += std::format("msg {} val {:.3f}\n", i, i * 1.5);
    { std::ofstream ofs(TMP, std::ios::trunc); ofs << buf; }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
// 返回生产者（业务线程）耗时：格式化 + 入队；昂贵 IO 由后台线程承担
double strat_async(int N) {
    std::mutex m; std::queue<std::string> q; std::condition_variable cv;
    std::atomic<bool> done{false};
    std::thread bg([&] {
        std::ofstream ofs(TMP, std::ios::trunc);
        for (;;) {
            std::string s;
            { std::unique_lock<std::mutex> lk(m);
              cv.wait(lk, [&] { return done.load() || !q.empty(); });
              if (done.load() && q.empty()) break;
              s = std::move(q.front()); q.pop(); }
            ofs << s << '\n';
        }
        ofs.flush();
    });
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::string msg = std::format("msg {} val {:.3f}", i, i * 1.5);
        { std::lock_guard<std::mutex> lk(m); q.push(std::move(msg)); }
        cv.notify_one();
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    { std::lock_guard<std::mutex> lk(m); done.store(true); } cv.notify_one();
    bg.join();
    return ms;
}

int main() {
    const int N = 200'000;
    const int ROUNDS = 5;
    std::vector<double> f1, f2, f3, s1, s2, s3;

    for (int t = 0; t < ROUNDS; ++t) {
        f1.push_back(fmt_ostringstream(N));
        f2.push_back(fmt_snprintf(N));
        f3.push_back(fmt_stdformat(N));
        s1.push_back(strat_sync(N));
        s2.push_back(strat_buffered(N));
        s3.push_back(strat_async(N));
    }
    auto median = [](std::vector<double> v) {
        std::sort(v.begin(), v.end()); return v[v.size()/2];
    };
    auto md = [&](std::vector<double>& v) { return median(v); };

    std::printf("g_sink=%ld  N=%d\n", (long)g_sink, N);
    std::printf("[format  median ms] ostringstream=%.2f  snprintf=%.2f  std_format=%.2f\n",
                md(f1), md(f2), md(f3));
    std::printf("  -> std::format vs ostringstream = %.2fx\n", md(f1) / md(f3));

    long ls = count_lines(TMP);  // 上次写盘的是 async；验证行数
    std::printf("[strategy median ms] sync_flush=%.2f  buffered=%.2f  async(producer)=%.2f\n",
                md(s1), md(s2), md(s3));
    std::printf("  -> buffered vs sync = %.2fx ; async(producer) vs sync = %.2fx\n",
                md(s1) / md(s2), md(s1) / md(s3));
    std::printf("line_count_check(async file)=%ld (expect %d) %s\n",
                ls, N, (ls == N) ? "OK" : "MISMATCH");

    std::remove(TMP);  // 清理临时日志
    return 0;
}
