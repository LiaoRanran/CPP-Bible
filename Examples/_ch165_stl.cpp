// _ch165_stl.cpp : STL 容器/算法/lambda 练习（中级）
#include <algorithm>
#include <iostream>
#include <map>
#include <vector>

int main() {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};

    std::sort(v.begin(), v.end());                 // 算法
    for (int x : v) std::cout << x << " ";
    std::cout << "\n";

    int cnt = std::count_if(v.begin(), v.end(),
                            [](int x) { return x > 3; }); // lambda
    std::cout << "count>3 = " << cnt << "\n";

    auto it = std::find(v.begin(), v.end(), 8);
    std::cout << "found8 = " << (it != v.end()) << "\n";

    std::map<std::string, int> m{{"a", 1}, {"b", 2}};
    m["c"] = 3;
    std::cout << "m[b] = " << m["b"] << "\n";
    return 0;
}
