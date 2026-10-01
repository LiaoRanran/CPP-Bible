// 已知无缺陷：RAII 所有权（D3 胸腺正确代码库；人工确认）
// 构造/析构配对，无裸 new/delete 泄漏路径，拷贝/移动语义明确。
#include <memory>
#include <utility>

class Widget {
public:
    Widget() = default;
    explicit Widget(int v) : value_(std::make_unique<int>(v)) {}
    Widget(Widget&& other) noexcept = default;
    Widget& operator=(Widget&& other) noexcept = default;
    Widget(const Widget&) = delete;
    Widget& operator=(const Widget&) = delete;
    ~Widget() = default;

    int value() const { return value_ ? *value_ : 0; }

private:
    std::unique_ptr<int> value_;
};

int main() {
    Widget a(42);
    Widget b = std::move(a);
    return b.value() == 42 ? 0 : 1;
}
