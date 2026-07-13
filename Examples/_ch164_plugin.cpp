// ③ 插件架构：跨平台"自注册"插件（静态初始化期登记，无需 LoadLibrary）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <unordered_map>
#include <functional>
#include <memory>

struct IPlugin {
    virtual ~IPlugin() = default;
    virtual std::string id() const = 0;
    virtual void exec() = 0;
};
using PluginFactory = std::function<std::shared_ptr<IPlugin>()>;

struct PluginHub {
    std::unordered_map<std::string, PluginFactory> makers;
    void install(const std::string& n, PluginFactory f) { makers[n] = std::move(f); }
    void run_all() {
        for (auto& [n, f] : makers) { std::cout << "[plugin] run " << n << ": "; f()->exec(); }
    }
};
PluginHub& hub() { static PluginHub h; return h; }

struct AutoInstall {
    AutoInstall(const std::string& n, PluginFactory f) { hub().install(n, std::move(f)); }
};
#define PLUGIN_REGISTER(Cls, Key) \
    static ::AutoInstall _pi_##Cls { (Key), [] { return std::make_shared<Cls>(); } }

struct GreetPlugin : IPlugin {
    std::string id() const override { return "greet"; }
    void exec() override { std::cout << "hello from plugin\n"; }
};
struct MetricPlugin : IPlugin {
    std::string id() const override { return "metric"; }
    void exec() override { std::cout << "emit metric=42\n"; }
};
PLUGIN_REGISTER(GreetPlugin,  "greet");
PLUGIN_REGISTER(MetricPlugin, "metric");

int main() {
    std::cout << "[plugin] loaded " << hub().makers.size() << " plugin(s)\n";
    hub().run_all();
    return 0;
}
