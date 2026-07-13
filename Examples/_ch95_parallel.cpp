// ch95 示例：并行执行策略 std::execution::par 的取证
// 编译（仅生成汇编，不链接）：
//   g++ -std=c++23 -O2 -S -masm=intel _ch95_parallel.cpp -o _ch95_parallel.asm
// 注意 [实现·libstdc++13]：std::execution::par 在 libstdc++ 中由 PSTL 后端实现，
// 后端默认是 Intel Threading Building Blocks (TBB)。要真正并发运行需链接 -ltbb；
// 仅 -S 查看汇编不需要链接，可见算法把执行分派给 __pstl 后端。
#include <algorithm>
#include <execution>
#include <vector>

void par_for_each(std::vector<double>& v) {
    std::for_each(std::execution::par,
                  v.begin(), v.end(),
                  [](double& x) { x = x * x + 1.0; });
}
