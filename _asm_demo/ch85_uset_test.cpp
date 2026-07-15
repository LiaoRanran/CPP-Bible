#include <unordered_set>

// 批 L5：unordered_set 哈希+div 取桶 + next 单链追逐（键即值@0）
int main() {
    std::unordered_set<int> s;
    for (int i = 0; i < 100; ++i) s.insert(i);
    volatile bool found = (s.find(42) != s.end());
    (void)found;
    return 0;
}
