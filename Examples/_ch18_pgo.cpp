// _ch18_pgo.cpp —— PGO（基于剖面的优化）示例
// classify 中 if (p[i] > 0) 分支在真实负载下大概率成立，
// -fprofile-use 据此把热路径排到 fall-through、冷路径变跳转。
#include <cstddef>

int classify(const int* p, std::size_t n) {
    int cnt = 0;
    for (std::size_t i = 0; i < n; ++i) {
        if (p[i] > 0)
            ++cnt;          // 热路径
        else
            cnt -= 1000;    // 极冷路径
    }
    return cnt;
}

int main() {
    int buf[1024];
    for (int i = 0; i < 1024; ++i) buf[i] = i - 100;   // 大多 > 0
    volatile int r = 0;
    for (int t = 0; t < 100000; ++t) r = classify(buf, 1024);
    return r;
}
