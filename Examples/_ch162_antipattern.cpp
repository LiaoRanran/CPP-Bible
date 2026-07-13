// 文件：Examples/_ch162_antipattern.cpp
// 行号：10-18（不安全的下标访问反模式）
// ⑰ 反模式（不安全解析）：用 operator[] 盲目访问，越界即 UB。
#include <iostream>
#include <string>
#include <vector>

// ❌ 反模式：假设输入永远是 "数字,数字,数字" 并直接下标访问
std::vector<int> unsafe_split(const std::string& s) {
    std::vector<int> out;
    size_t i = 0;
    while (i < s.size()) {
        // 反例：没有检查 s[i] 是否为数字，也没有边界保护
        int v = 0;
        while (s[i] >= '0' && s[i] <= '9') { v = v * 10 + (s[i] - '0'); ++i; } // 越界 UB
        out.push_back(v);
        if (s[i] == ',') ++i;
    }
    return out;
}

int main() {
    // 良性输入能跑，但一旦 s[i] 越界就是未定义行为
    for (int x : unsafe_split("12,34,56"))
        std::cout << x << " ";
    std::cout << "\n";
    return 0;
}
