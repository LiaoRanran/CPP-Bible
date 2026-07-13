// 文件: Examples/_ch137_adapter.cpp
// 对象适配器：把 LegacyRectangle 适配成客户期望的 Rectangle 接口
#include <iostream>

struct LegacyRectangle {
    void oldDraw(int x1, int y1, int x2, int y2) {
        std::cout << "LegacyRectangle (" << x1 << ',' << y1
                  << ")-(" << x2 << ',' << y2 << ")\n";
    }
};

struct Rectangle {
    virtual ~Rectangle() = default;
    virtual void draw(int x, int y, int w, int h) = 0;
};

class RectangleAdapter : public Rectangle {
    LegacyRectangle& legacy_;
public:
    explicit RectangleAdapter(LegacyRectangle& l) : legacy_(l) {}
    void draw(int x, int y, int w, int h) override {
        legacy_.oldDraw(x, y, x + w, y + h);  // 把 (x,y,w,h) 转成对角坐标
    }
};

int main() {
    LegacyRectangle leg;
    RectangleAdapter adapter{leg};
    Rectangle& r = adapter;
    r.draw(0, 0, 10, 20);
}
