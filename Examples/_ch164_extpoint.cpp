// ⑪ 扩展点设计：责任链 / 管道，运行时插入处理节点（开放封闭原则）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <functional>

struct Middleware {
    virtual ~Middleware() = default;
    virtual bool process(std::string& s) = 0;  // 返回 false 则短路
};
struct AuthMW    : Middleware { bool process(std::string& s) override { std::cout << "  [mw] auth " << s << "\n"; return true; } };
struct LogMW     : Middleware { bool process(std::string& s) override { std::cout << "  [mw] log "  << s << "\n"; return true; } };
struct BlockMW   : Middleware { bool process(std::string& s) override { std::cout << "  [mw] block "<< s << " -> drop\n"; return false; } };

struct Pipeline {
    std::vector<std::unique_ptr<Middleware>> chain;
    template <class T, class... A> void add(A&&... a) {
        chain.push_back(std::make_unique<T>(std::forward<A>(a)...));   // 扩展点：随时挂新节点
    }
    bool run(std::string s) {
        for (auto& mw : chain) if (!mw->process(s)) return false;
        return true;
    }
};

int main() {
    Pipeline p;
    p.add<AuthMW>(); p.add<LogMW>();
    std::cout << "[ext] pipeline allow = " << (p.run("req#1") ? "true" : "false") << "\n";
    p.add<BlockMW>();
    std::cout << "[ext] pipeline allow = " << (p.run("req#2") ? "true" : "false") << "\n";
    return 0;
}
