// _ch135_observer.cpp
// 取证目标（第⑰节）：观察者模式（行为型）组合示例。
#include <cstdio>
#include <vector>
#include <functional>

struct Subject {
    std::vector<std::function<void(int)>> obs;
    void attach(std::function<void(int)> f) { obs.push_back(std::move(f)); }
    void notify(int v) { for (auto& f : obs) f(v); }
};

int main() {
    Subject s;
    s.attach([](int v){ std::printf("got %d\n", v); });
    s.notify(7);
}
