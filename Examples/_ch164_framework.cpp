// ⑨/⑱ 自包含迷你框架 MiniFW（本机 g++ -std=c++23 -O2 可编译运行）
// 文件：Examples/_ch164_framework.cpp
// 行号： 47-58（Registry 自注册 AutoReg + MINIFW_REGISTER 宏）
//        60-86（Framework::start/run/stop 生命周期）
//      118-143（main：加载配置 → 启动 → 事件循环 → 关闭）
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
#include <memory>
#include <fstream>
#include <sstream>
#include <cassert>

// ── 组件接口（模块化：接口与实现分离）─────────────────────
struct IComponent {
    virtual ~IComponent() = default;
    virtual std::string name() const = 0;
    virtual void start() = 0;
    virtual void onTick(int tick) { (void)tick; }
    virtual void stop()  = 0;
};
using ComponentFactory = std::function<std::shared_ptr<IComponent>()>;

// ── 全局注册表（自注册插件架构的核心）─────────────────────
struct Registry {
    std::unordered_map<std::string, ComponentFactory> factories;
    void add(const std::string& n, ComponentFactory f) { factories[n] = std::move(f); }
    std::shared_ptr<IComponent> create(const std::string& n) const {
        auto it = factories.find(n);
        return it == factories.end() ? nullptr : it->second();
    }
    const auto& all() const { return factories; }
};

Registry& registry() { static Registry r; return r; }

// 静态初始化期自注册：任意编译单元 inclusion 即登记（插件式）
struct AutoReg {
    AutoReg(Registry& r, const std::string& n, ComponentFactory f) { r.add(n, std::move(f)); }
};
#define MINIFW_REGISTER(Cls, Key) \
    static ::AutoReg _minifw_reg_##Cls { ::registry(), (Key), [] { return std::make_shared<Cls>(); } }

// ── 事件总线（reactor）───────────────────────────────────
struct EventBus {
    struct Event { std::string type; std::string payload; };
    std::unordered_map<std::string, std::vector<std::function<void(const Event&)>>> subs;
    void subscribe(const std::string& t, std::function<void(const Event&)> h) {
        subs[t].push_back(std::move(h));
    }
    void publish(const Event& e) {
        auto it = subs.find(e.type);
        if (it != subs.end()) for (auto& h : it->second) h(e);
    }
};

// ── 配置系统（INI 风格 key=value）────────────────────────
struct Config {
    std::unordered_map<std::string, std::string> kv;
    bool load(const std::string& path) {
        std::ifstream f(path); if (!f) return false;
        std::string line;
        while (std::getline(f, line)) {
            // 去首尾空白
            auto b = line.find_first_not_of(" \t\r\n");
            if (b == std::string::npos) continue;
            auto e = line.find_last_not_of(" \t\r\n");
            line = line.substr(b, e - b + 1);
            if (line[0] == '#' || line[0] == ';') continue;
            auto eq = line.find('=');
            if (eq == std::string::npos) continue;
            std::string k = line.substr(0, eq), v = line.substr(eq + 1);
            auto kb = k.find_first_not_of(" \t"), ke = k.find_last_not_of(" \t");
            auto vb = v.find_first_not_of(" \t"), ve = v.find_last_not_of(" \t");
            kv[k.substr(kb, ke - kb + 1)] = v.substr(vb, ve - vb + 1);
        }
        return true;
    }
    std::string get(const std::string& k, const std::string& d = "") const {
        auto it = kv.find(k); return it == kv.end() ? d : it->second;
    }
    size_t size() const { return kv.size(); }
};

// ── 依赖注入容器（std::any 擦除类型）─────────────────────
struct Container {
    std::unordered_map<std::string, std::shared_ptr<void>> services;
    template <class T>
    void add(const std::string& k, std::shared_ptr<T> p) {
        services[k] = std::static_pointer_cast<void>(p);
    }
    template <class T>
    std::shared_ptr<T> get(const std::string& k) const {
        auto it = services.find(k);
        return it == services.end() ? nullptr : std::static_pointer_cast<T>(it->second);
    }
};

// ── 框架主体：拥有配置/注册表/事件/DI，管理生命周期 ───────
struct Framework {
    Registry& reg;
    EventBus bus;
    Config   cfg;
    Container di;
    std::vector<std::shared_ptr<IComponent>> active;

    explicit Framework(Registry& r) : reg(r) {}

    bool loadConfig(const std::string& p) {
        if (!cfg.load(p)) { std::cerr << "[MiniFW] config load FAILED: " << p << "\n"; return false; }
        std::cout << "[MiniFW] config loaded: " << cfg.size() << " entries ("
                  << "app=" << cfg.get("app") << ")\n";
        return true;
    }
    void start() {
        std::cout << "[MiniFW] startup: instantiating "
                  << reg.all().size() << " registered component(s)...\n";
        for (auto& kv : reg.all()) {
            auto c = kv.second();
            c->start();
            // 扩展点：把组件也挂到 DI，供其他模块按接口取用
            di.add<IComponent>(c->name(), c);
            active.push_back(c);
        }
        bus.publish({"startup", ""});
    }
    void run(int ticks) {
        for (int t = 1; t <= ticks; ++t) {
            std::cout << "[MiniFW] run: tick " << t << "\n";
            bus.publish({"tick", std::to_string(t)});
            for (auto& c : active) c->onTick(t);
        }
    }
    void stop() {
        std::cout << "[MiniFW] shutdown: stop components\n";
        for (auto& c : active) c->stop();
        active.clear();
    }
};

// ── 两个内置组件（演示模块化）────────────────────────────
struct Logger : IComponent {
    std::string name() const override { return "logger"; }
    void start() override { std::cout << "[MiniFW] logger.start()\n"; }
    void onTick(int t) override { std::cout << "[MiniFW]   logger.onTick " << t << "\n"; }
    void stop()  override { std::cout << "[MiniFW] logger.stop()\n"; }
};
struct Network : IComponent {
    std::string name() const override { return "network"; }
    void start() override { std::cout << "[MiniFW] network.start()\n"; }
    void onTick(int t) override { std::cout << "[MiniFW]   network.onTick " << t << "\n"; }
    void stop()  override { std::cout << "[MiniFW] network.stop()\n"; }
};
MINIFW_REGISTER(Logger,  "logger");
MINIFW_REGISTER(Network, "network");

int main(int argc, char** argv) {
    Framework fw{registry()};
    fw.bus.subscribe("startup", [](const EventBus::Event&) {
        std::cout << "[MiniFW]   (event) startup fired -> handler ok\n";
    });
    std::string cfgpath = argc > 1 ? argv[1] : "mini.conf";
    if (!fw.loadConfig(cfgpath)) return 1;
    fw.start();
    fw.run(3);
    // DI 钩子：按名字取回组件（验证容器注入生效）
    auto lp = fw.di.get<IComponent>("logger");
    std::cout << "[MiniFW] DI resolved: " << (lp ? lp->name() : "?") << "\n";
    fw.stop();
    return 0;
}
