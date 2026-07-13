// 文件：Examples/_ch99_scan.cpp
// 行号：9 (demo_partial) / 15 (demo_scan) / 21 (demo_exclusive)
#include <numeric>
#include <vector>
#include <iostream>

void demo_partial() {
    std::vector<int> v{1,2,3,4,5};
    std::vector<int> out(v.size());
    std::partial_sum(v.begin(), v.end(), out.begin());   // 含前项(就地累积)
    for (int x : out) std::cout << x << " ";
    std::cout << "\n";
}

void demo_scan() {
    std::vector<int> v{1,2,3,4,5};
    std::vector<int> out(v.size());
    std::inclusive_scan(v.begin(), v.end(), out.begin());   // 与 partial_sum 等价
    std::exclusive_scan(v.begin(), v.end(), out.begin(), 0); // 不含当前项
    for (int x : out) std::cout << x << " ";
    std::cout << "\n";
}

void demo_exclusive() {
    std::vector<int> v{1,2,3,4};
    std::vector<int> out(v.size());
    std::transform_exclusive_scan(v.begin(), v.end(), out.begin(), 100,
                        std::plus<>(), [](int x){ return x * 10; });
    for (int x : out) std::cout << x << " ";
    std::cout << "\n";
}

int main() { demo_partial(); demo_scan(); demo_exclusive(); }
