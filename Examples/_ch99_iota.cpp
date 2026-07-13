// 文件：Examples/_ch99_iota.cpp
// 行号：8 (fill_seq) / 14 (fill_steps)
#include <numeric>
#include <vector>
#include <iostream>

void fill_seq() {
    std::vector<int> v(5);
    std::iota(v.begin(), v.end(), 0);   // 0 1 2 3 4
    for (int x : v) std::cout << x << " ";
    std::cout << "\n";
}

void fill_steps() {
    std::vector<double> v(5);
    std::iota(v.begin(), v.end(), 1.5); // 1.5 2.5 3.5 4.5 5.5
    for (double x : v) std::cout << x << " ";
    std::cout << "\n";
}

int main() { fill_seq(); fill_steps(); }
