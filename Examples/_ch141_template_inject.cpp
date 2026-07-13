// Examples/_ch141_template_inject.cpp
// 模板参数注入（编译期绑定）：依赖类型作为模板参数，零运行时开销，可被内联/去虚化。
#include <iostream>

struct RealClock { int now() const { return 100; } };
struct MockClock  { int now() const { return 0;   } };

template <class Clock>
class Scheduler {
    Clock clock_;                      // 依赖类型在编译期确定
public:
    int tick() const { return clock_.now(); }
};

int main() {
    Scheduler<RealClock> s;
    Scheduler<MockClock> m;            // ✅ 同一份代码，绑定不同实现
    std::cout << s.tick() << " " << m.tick() << "\n";
}
