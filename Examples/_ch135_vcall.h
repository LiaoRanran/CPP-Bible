// _ch135_vcall.h  (取证第⑮节：跨 TU 无法去虚化的真实 vtable 调用)
struct Animal {
    virtual ~Animal() = default;
    virtual int speak() const = 0;
};
struct Dog : Animal { int speak() const override; };
int via_virtual(const Animal& a); // 在另一 TU 定义，编译器看不到动态类型
