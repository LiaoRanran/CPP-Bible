// _ch163_net_perf.cpp — 第163章 真实基准/汇编锚定
// 用途 ① 运行时基准：替换书内网络 ~N 估算（localhost TCP 连接/RTT/吞吐、上下文切换、syscall 下限）
//      ② 静态证据：[[gnu::noinline]] 锚点供 asm 抓取（call send/recv 边界）
// 编译: g++ -O2 -std=c++17 _ch163_net_perf.cpp -o _ch163_net_perf -lws2_32 && ./_ch163_net_perf
// 汇编: g++ -S -O2 -std=c++17 -m64 _ch163_net_perf.cpp -o _ch163_net_perf.asm
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <atomic>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <mutex>
#include <condition_variable>
#include <x86intrin.h>
#pragma comment(lib, "ws2_32.lib")

static double g_tsc_ghz = 0.0;
static inline uint64_t rdtsc() { return __rdtsc(); }
static void calibrate_tsc() {
    auto t0 = std::chrono::steady_clock::now();
    uint64_t c0 = rdtsc();
    std::this_thread::sleep_for(std::chrono::milliseconds(120));
    uint64_t c1 = rdtsc();
    auto t1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(t1 - t0).count();
    g_tsc_ghz = (double)(c1 - c0) / secs / 1e9;
}
static inline double tsc_to_ns(uint64_t cyc) { return cyc / g_tsc_ghz; }

static const int PORT = 54331;
static const char* ADDR = "127.0.0.1";

// 静态证据锚点：一个网络写调用的编译边界（call send）
[[gnu::noinline]] int sock_send(SOCKET s, const char* buf, int n) { return send(s, buf, n, 0); }
[[gnu::noinline]] int sock_recv(SOCKET s, char* buf, int n) { return recv(s, buf, n, 0); }

// 服务器线程：accept 后回声（echo），客户端关连接则退出
static void server_thread(std::atomic<bool>* ready) {
    SOCKET ls = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in sa{}; sa.sin_family = AF_INET; sa.sin_port = htons(PORT);
    inet_pton(AF_INET, ADDR, &sa.sin_addr);
    bind(ls, (sockaddr*)&sa, sizeof(sa));
    listen(ls, 1);
    *ready = true;
    SOCKET c = accept(ls, nullptr, nullptr);
    char buf[65536];
    for (;;) {
        int n = recv(c, buf, sizeof(buf), 0);
        if (n <= 0) break;
        int sent = 0;
        while (sent < n) { int k = send(c, buf + sent, n - sent, 0); if (k <= 0) break; sent += k; }
    }
    closesocket(c); closesocket(ls);
}

int main() {
    WSADATA wsa; WSAStartup(MAKEWORD(2, 2), &wsa);
    calibrate_tsc();
    std::printf("TSC freq: %.3f GHz\n", g_tsc_ghz);

    std::atomic<bool> ready{false};
    std::thread srv(server_thread, &ready);
    while (!ready) std::this_thread::yield();
    std::this_thread::sleep_for(std::chrono::milliseconds(20)); // 让 accept 就绪

    SOCKET cli = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in ca{}; ca.sin_family = AF_INET; ca.sin_port = htons(PORT);
    inet_pton(AF_INET, ADDR, &ca.sin_addr);

    // 1) connect 延迟（steady_clock，毫秒级）
    auto c0 = std::chrono::steady_clock::now();
    connect(cli, (sockaddr*)&ca, sizeof(ca));
    auto c1 = std::chrono::steady_clock::now();
    double connect_us = std::chrono::duration<double, std::micro>(c1 - c0).count();
    std::printf("localhost TCP connect : %.1f us\n", connect_us);

    // 2) 小消息 RTT（send 1B + recv 1B），steady_clock
    const int N = 200'000;
    char b = 'x'; char r = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { send(cli, &b, 1, 0); recv(cli, &r, 1, 0); }
    auto t1 = std::chrono::steady_clock::now();
    double rtt_us = std::chrono::duration<double, std::micro>(t1 - t0).count() / N;
    std::printf("localhost RTT (1B echo): %.3f us/op\n", rtt_us);

    // 3) 批量吞吐（发送 64MB，服务端回声，客户端边发边收以排空）
    const size_t TOTAL = 64 * 1024 * 1024;
    const int CHUNK = 64 * 1024;
    char* big = new char[CHUNK];
    std::memset(big, 0xA5, CHUNK);
    auto tb0 = std::chrono::steady_clock::now();
    size_t sent = 0;
    while (sent < TOTAL) {
        int k = send(cli, big, CHUNK, 0); if (k <= 0) break;
        sent += k;
        // 排空回声，避免服务端发送缓冲阻塞
        int got = 0;
        while (got < k) { int m = recv(cli, big, k - got, 0); if (m <= 0) break; got += m; }
    }
    auto tb1 = std::chrono::steady_clock::now();
    double secs = std::chrono::duration<double>(tb1 - tb0).count();
    double mbps = (double)TOTAL / (1024.0 * 1024.0) / secs;
    std::printf("localhost bulk xfer : %.1f MB/s (%.2f GB/s)\n", mbps, mbps / 1024.0);
    delete[] big;

    // 4) syscall 下限：steady_clock::now() 采样开销（proxy，非 I/O syscall）
    const int M = 5'000'000;
    uint64_t s0 = rdtsc();
    uint64_t sink = 0;
    for (int i = 0; i < M; ++i) { auto now = std::chrono::steady_clock::now(); sink += (uint64_t)now.time_since_epoch().count(); }
    uint64_t s1 = rdtsc();
    (void)sink;
    std::printf("clock-read proxy     : %.2f ns/call (RDTSC, not I/O syscall)\n", tsc_to_ns(s1 - s0) / M);

    // 5) 线程上下文切换（mutex+cv 往返，含同步开销）
    std::mutex m; std::condition_variable cv; int turn = 0; std::atomic<bool> done{false};
    std::thread peer([&]() {
        for (;;) {
            std::unique_lock<std::mutex> lk(m);
            cv.wait(lk, [&]() { return turn == 1 || done.load(); });
            if (done.load()) break;
            turn = 0; lk.unlock(); cv.notify_one();
        }
    });
    const int K = 50'000;
    auto x0 = std::chrono::steady_clock::now();
    for (int i = 0; i < K; ++i) {
        std::unique_lock<std::mutex> lk(m); turn = 1; cv.notify_one();
        cv.wait(lk, [&]() { return turn == 0; });
    }
    auto x1 = std::chrono::steady_clock::now();
    done.store(true); { std::lock_guard<std::mutex> lk(m); cv.notify_one(); }
    peer.join();
    double ctx_us = std::chrono::duration<double, std::micro>(x1 - x0).count() / K;
    std::printf("thread switch (m+cv) : %.2f us/rt (%.2f us/switch, 含同步开销)\n", ctx_us, ctx_us / 2.0);

    // 强制发射 asm 锚点
    volatile auto fp1 = &sock_send; (void)fp1;
    volatile auto fp2 = &sock_recv; (void)fp2;

    closesocket(cli);
    WSACleanup();
    srv.join();
    std::printf("== 第163章 网络真实基准 (GCC 13.1 / MinGW-w64 / x86-64, localhost) ==\n");
    return 0;
}
