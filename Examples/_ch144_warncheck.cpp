// 用于演示 -Wall -Wextra 零警告（工业级干净编译）
#include <memory>
#include <vector>

namespace demo {

class Buffer {
public:
    explicit Buffer(std::size_t n) : data_(std::make_unique<int[]>(n)), size_(n) {}

    int at(std::size_t i) const noexcept {
        // 调用方保证边界，noexcept 表达此契约
        return data_[i];
    }

    std::size_t size() const noexcept { return size_; }

private:
    std::unique_ptr<int[]> data_;
    std::size_t size_;
};

int total(const Buffer& b) noexcept {
    int s = 0;
    for (std::size_t i = 0; i < b.size(); ++i) s += b.at(i);
    return s;
}

} // namespace demo

int main() {
    demo::Buffer b(4);
    return demo::total(b);
}
