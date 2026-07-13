// 文件：Examples/_ch161_fix13.cpp
// 主题：⑰ 反模式修正 —— 先判级别再构建字符串，避免关闭时白做功
#include <cstdio>
#include <string>

enum class Lv { info = 2, off = 5 };
constexpr Lv THR = Lv::off;  // 生产中可能临时关闭

inline bool enabled(Lv m) { return static_cast<int>(m) >= static_cast<int>(THR); }

int main() {
    int id = 42;
    double v = 3.14;
    if (enabled(Lv::info)) {                 // 先判级别，再构建
        std::string s = "id=" + std::to_string(id) + " val=" + std::to_string(v);
        std::printf("[info] %s\n", s.c_str());
    } else {
        std::printf("skipped: level disabled\n");
    }
    return 0;
}
