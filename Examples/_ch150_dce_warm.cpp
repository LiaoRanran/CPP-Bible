// ⑮' 预热实证：同一负载首次往往更慢，基准应丢弃首批
#include <cstdio>
#include <chrono>
#include <vector>
int main() {
    double first = 0, second = 0;
    for (int round = 0; round < 2; ++round) {
        auto t0 = std::chrono::steady_clock::now();
        std::vector<int> v; volatile unsigned s = 0;
        for (int i = 0; i < 2'000'000; ++i) v.push_back(i);
        s = v.size(); (void)s;
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (round == 0) first = ms; else second = ms;
    }
    std::printf("warmup: round1=%.3f ms round2=%.3f ms (discard round1)\n", first, second);
    return 0;
}
