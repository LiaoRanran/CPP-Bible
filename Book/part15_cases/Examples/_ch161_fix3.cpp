// 文件：Examples/_ch161_fix3.cpp
// 主题：③ 自定义 sink —— 内存环形缓冲（容量封顶，旧日志被覆盖）
#include <array>
#include <cstddef>
#include <cstdio>
#include <string>
#include <string_view>

template <std::size_t N>
struct RingSink {
    std::array<std::string, N> buf{};
    std::size_t idx = 0, count = 0;
    void write(std::string_view msg) {
        buf[idx] = std::string(msg);
        idx = (idx + 1) % N;
        if (count < N) ++count;
    }
    void dump() const {
        for (std::size_t i = 0; i < count; ++i)
            std::printf("ring[%zu]=%s\n", i, buf[i].c_str());
    }
};

int main() {
    RingSink<3> ring;
    ring.write("a"); ring.write("b"); ring.write("c"); ring.write("d"); // d 覆盖 a
    std::printf("count=%zu (封顶3)\n", ring.count);
    ring.dump();
    return 0;
}
