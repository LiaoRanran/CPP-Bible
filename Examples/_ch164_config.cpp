// ⑤ 配置系统：解析 INI 风格 key=value（与框架内 Config 同源实现）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <unordered_map>
#include <fstream>

struct Config {
    std::unordered_map<std::string, std::string> kv;
    bool load(const std::string& p) {
        std::ifstream f(p); if (!f) return false;
        std::string line;
        while (std::getline(f, line)) {
            auto b = line.find_first_not_of(" \t\r\n");
            if (b == std::string::npos) continue;
            auto e = line.find_last_not_of(" \t\r\n");
            line = line.substr(b, e - b + 1);
            if (line[0] == '#') continue;
            auto eq = line.find('=');
            if (eq == std::string::npos) continue;
            std::string k = line.substr(0, eq), v = line.substr(eq + 1);
            auto kb = k.find_first_not_of(" \t"), ke = k.find_last_not_of(" \t");
            auto vb = v.find_first_not_of(" \t"), ve = v.find_last_not_of(" \t");
            kv[k.substr(kb, ke - kb + 1)] = v.substr(vb, ve - vb + 1);
        }
        return true;
    }
};

int main() {
    Config c;
    if (!c.load("mini.conf")) { std::cout << "load failed\n"; return 1; }
    std::cout << "[config] entries=" << c.kv.size() << "\n";
    for (auto& [k, v] : c.kv) std::cout << "  " << k << " = " << v << "\n";
    return 0;
}
