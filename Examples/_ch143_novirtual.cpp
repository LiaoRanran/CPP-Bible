// ⑩ 避免虚函数：虚调用经 vtable 间接跳转，破坏分支预测、挤占指令缓存
struct Shape {
    virtual float area() const = 0;
    virtual ~Shape() = default;
};
struct Circle : Shape {
    float r;
    float area() const override { return 3.14159f * r * r; }
};

float sum_virtual(const Shape& s) { return s.area(); }   // 间接调用

// 等价但无虚函数的 DOD 形态：编译器可直接内联
struct Circle2 { float r; float area() const { return 3.14159f * r * r; } };
float sum_static(const Circle2& s) { return s.area(); }  // 可被内联
