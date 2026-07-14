// UB-L5 const_cast mutation：cast away const 后修改真正 const 的对象
// 编译: g++ -std=c++23 -O2 -Wall -Wcast-qual -o ccm ub_const_cast_mutation.cpp
#include <cstdio>

const int G = 5;                 // 真正 const 对象，可能置于只读段

int main() {
    const_cast<int&>(G) = 10;   // ❌ 修改真正 const 对象 → UB（可能段错误）
    std::printf("G = %d\n", G);
    return 0;
}
