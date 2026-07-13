// 文件：Examples/_ch160_frag.cpp
// 行号：1
// 内存碎片实证：交替分配不同大小并随机释放，制造外部碎片
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>

int main() {
    std::mt19937 rng(20240709);
    std::vector<void*> live;
    const int rounds = 200000;
    size_t peak_bytes = 0, live_bytes = 0;
    for (int i = 0; i < rounds; ++i) {
        int sz = 16 + (rng() % 12) * 16; // 16..192 字节
        void* p = std::malloc(sz);
        live.push_back(p);
        live_bytes += sz; peak_bytes = std::max(peak_bytes, live_bytes);
        // 随机释放约一半
        if (live.size() > 1 && (rng() & 1)) {
            int idx = rng() % live.size();
            std::free(live[idx]);
            live_bytes -= 16 + (idx % 12) * 16; // 近似
            live[idx] = live.back(); live.pop_back();
        }
    }
    // 全部释放
    for (void* p : live) std::free(p);
    std::printf("malloc 碎片实验完成: rounds=%d peak_live_bytes=%zu\n", rounds, peak_bytes);
    return 0;
}
