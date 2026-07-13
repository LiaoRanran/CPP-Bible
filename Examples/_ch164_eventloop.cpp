// ④ 事件循环（reactor）：单线程事件分发，注册 handler 后 publish 触发
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <functional>

struct Reactor {
    using Handler = std::function<void(const std::string&)>;
    std::unordered_map<std::string, std::vector<Handler>> table;
    void on(const std::string& ev, Handler h) { table[ev].push_back(std::move(h)); }
    void dispatch(const std::string& ev, const std::string& data) {
        auto it = table.find(ev);
        if (it == table.end()) { std::cout << "[reactor] no handler for " << ev << "\n"; return; }
        std::cout << "[reactor] dispatch '" << ev << "' -> " << it->second.size() << " handler(s)\n";
        for (auto& h : it->second) h(data);
    }
};

int main() {
    Reactor r;
    r.on("tick",  [](const std::string& d){ std::cout << "  h1 got tick " << d << "\n"; });
    r.on("tick",  [](const std::string& d){ std::cout << "  h2 got tick " << d << "\n"; });
    r.on("alarm", [](const std::string& d){ std::cout << "  alarm! " << d << "\n"; });
    r.dispatch("tick",  "1");
    r.dispatch("tick",  "2");
    r.dispatch("alarm", "overheat");
    r.dispatch("unknown", "x");
    return 0;
}
