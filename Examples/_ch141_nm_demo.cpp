// Examples/_ch141_nm_demo.cpp
// 模板注入的“零成本”取证补充：用 nm 观察模板实例化出的符号（每个绑定生成独立实例）。
// 编译：g++ -std=c++23 -O0 -c _ch141_nm_demo.cpp -o _ch141_nm_demo.o && nm _ch141_nm_demo.o
#include <string>

template <class T>
struct Holder { T v; T get() const { return v; } };

struct A { int x; };
struct B { std::string s; };

template struct Holder<A>;   // 显式实例化 → nm 可见 _ZN6HolderI1AE3get... 等符号
template struct Holder<B>;

int use() {
    Holder<A> ha{A{1}};
    Holder<B> hb{B{"x"}};
    return ha.get().x + (int)hb.get().s.size();
}
