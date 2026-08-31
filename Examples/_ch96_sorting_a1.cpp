#include <iostream>
#include <algorithm>
#include <vector>
#include <random>

int main() {
    std::vector<int> v(1000);
    std::mt19937 gen(42);
    std::uniform_int_distribution<int> dist(0, 1000000);
    for (int& x : v) x = dist(gen);

    // sort：全序
    std::vector<int> a = v;
    std::sort(a.begin(), a.end());
    if (!std::is_sorted(a.begin(), a.end())) { std::cerr << "SORT FAIL" << std::endl; return 1; }

    // partial_sort：前 10 个最小且有序
    std::vector<int> b = v;
    std::partial_sort(b.begin(), b.begin() + 10, b.end());
    if (!std::is_sorted(b.begin(), b.begin() + 10)) { std::cerr << "PARTIAL FAIL" << std::endl; return 1; }
    for (int i = 10; i < (int)b.size(); ++i)
        if (b[i] < b[9]) { std::cerr << "PARTIAL BOUND FAIL" << std::endl; return 1; }

    // nth_element：中位归位，左 <= 右
    std::vector<int> c = v;
    std::nth_element(c.begin(), c.begin() + 500, c.end());
    for (int i = 0; i < 500; ++i)
        if (c[i] > c[500]) { std::cerr << "NTH LEFT FAIL" << std::endl; return 1; }
    for (int i = 501; i < (int)c.size(); ++i)
        if (c[i] < c[500]) { std::cerr << "NTH RIGHT FAIL" << std::endl; return 1; }

    std::cout << "sort ok: is_sorted=" << std::boolalpha << std::is_sorted(a.begin(), a.end()) << std::endl;
    std::cout << "partial top10[0]=" << b[0] << " (should be global min)" << std::endl;
    std::cout << "nth median c[500]=" << c[500] << std::endl;
    std::cout << "functional checks passed" << std::endl;
    return 0;
}