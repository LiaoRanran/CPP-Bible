// Wave8 D5 bench: std::filesystem::path 词法分解 vs 手写字符串切分（纯 CPU，不触盘）
// 编译: g++ -O2 -std=c++23 _bench_d5_ch91_filesystem.cpp -o _bench_d5_ch91_filesystem.exe
// 运行: ./_bench_d5_ch91_filesystem.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <string>
#include <string_view>
#include <filesystem>

static volatile std::uint64_t g_sink = 0;

void manual_split(const std::string& p, std::string& dir, std::string& name, std::string& ext) {
    size_t sl = p.find_last_of('/');
    size_t bs = p.find_last_of('\\');
    size_t sep = (sl > bs) ? sl : bs;
    std::string_view body = (sep == std::string::npos) ? std::string_view(p)
                                                       : std::string_view(p).substr(sep + 1);
    size_t dot = body.find_last_of('.');
    dir = (sep == std::string::npos) ? std::string() : std::string(p, 0, sep);
    name = (dot == std::string::npos) ? std::string(body) : std::string(body.substr(0, dot));
    ext = (dot == std::string::npos) ? std::string() : std::string(body.substr(dot));
}

int main() {
    const char* samples[] = {
        "/usr/local/include/foo/bar.h",
        "C:\\Program Files\\app\\main.cpp",
        "./build/obj/engine/core.o",
        "/etc/nginx/conf.d/site.conf",
        "D:/work/proj/src/util/str.hpp"
    };
    constexpr int K = (int)(sizeof(samples) / sizeof(samples[0]));
    constexpr int N = 4'000'000;

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        const std::filesystem::path p(samples[i % K]);
        std::string dp = p.parent_path().string();
        std::string fn = p.filename().string();
        std::string ex = p.extension().string();
        g_sink += dp.size() + fn.size() + ex.size();
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("std::filesystem::path: %.3f ms\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());

    auto t2 = std::chrono::steady_clock::now();
    std::string dir, name, ext;
    for (int i = 0; i < N; ++i) {
        manual_split(samples[i % K], dir, name, ext);
        g_sink += dir.size() + name.size() + ext.size();
    }
    auto t3 = std::chrono::steady_clock::now();
    std::printf("manual string split:  %.3f ms\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());

    return 0;
}
