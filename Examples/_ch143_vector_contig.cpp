#include <vector>
#include <cstdio>

// ⑨ std::vector 保证元素连续，这是 DOD 的基石
int main() {
    std::vector<int> v(4);
    v[0] = 0; v[1] = 1; v[2] = 2; v[3] = 3;
    // 连续布局：相邻元素地址差恰好为 sizeof(int)
    std::printf("contiguous? &v[3]-&v[0] = %td (期望 3)\n",
                static_cast<long>(&v[3] - &v[0]));
    return 0;
}
