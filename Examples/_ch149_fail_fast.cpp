// 见 Examples/_ch149_fail_fast.cpp
// ⑯ 失败快速：矩阵任一作业失败立即中止其余作业
#include <cstdio>
#include <vector>
int main() {
    std::vector<int> results = {0, 0, 1, 0};  // 1 = 失败
    bool fail_fast = true;
    int done = 0;
    for (int r : results) {
        if (r != 0) {
            std::printf("job failed at #%d -> abort remaining (fail-fast=%d)\n", done, fail_fast);
            return 1;
        }
        ++done;
    }
    std::printf("all %d jobs passed\n", done);
    return 0;
}
