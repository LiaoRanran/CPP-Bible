// 自包含信号槽等价机制（观察者 + 类型擦除），等价于 moc 生成的 connect/emit。
// 目标：在没有 Qt 运行库时，用纯 C++ 复现「信号持有槽列表、emit 即遍历回调」。
#include <iostream>
#include <vector>
#include <functional>

// 等价 Qt 的 SIGNAL/SLOT 元数据：moc 会为每个 signal 生成一个指向回调表的入口；
// 这里用 std::function 做类型擦除，等价于 moc 生成的 QSlotObject 闭包。
struct SignalClick {
    using Slot = std::function<void(int)>;
    std::vector<Slot> slots;
    void connect(Slot f) { slots.push_back(std::move(f)); }   // 等价 QObject::connect
    void emit(int v) { for (auto& s : slots) s(v); }          // 等价 emit clicked(x);
};

class Button {
public:
    SignalClick clicked;                  // 等价 Qt: signals: void clicked(int);
    void press(int x) { clicked.emit(x); } // 等价 emit clicked(x);
};

class Label {
public:
    void on_clicked(int x) { std::cout << "[slot] clicked at " << x << "\n"; }
};

int main() {
    Button b;
    Label l;
    b.clicked.connect([&l](int x) { l.on_clicked(x); }); // 等价 connect(&b,&Button::clicked,&l,&Label::on_clicked)
    b.press(42);
    return 0;
}
