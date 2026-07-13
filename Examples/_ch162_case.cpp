// 文件：Examples/_ch162_case.cpp
// 行号：38-46（读取配置字段并打印）
// ⑲ 真实案例：解析一份服务器配置文件（贴近工程，非 Hello World）。
#include <iostream>
#include <map>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

struct V;
using Arr = std::vector<V>;
using Obj = std::map<std::string, V>;
struct V { std::variant<std::nullptr_t, bool, double, std::string, Arr, Obj> d{nullptr}; };

static size_t p; static std::string_view sv;
static std::string ps(){ ++p; std::string s; while(p<sv.size()&&sv[p]!='"') s+=sv[p++]; ++p; return s; }
static double pn(){ size_t a=p; while(p<sv.size()&&(std::isdigit((unsigned char)sv[p])||sv[p]=='.'||sv[p]=='-'||sv[p]=='e'||sv[p]=='E'))++p; return std::stod(std::string(sv.substr(a,p-a))); }
static V pv(){
    while(p<sv.size()&&(sv[p]==' '||sv[p]=='\n'||sv[p]=='\t'||sv[p]=='\r'))++p;
    char c=sv[p];
    if(c=='"') return V{ps()};
    if(c=='['){++p;Arr a; while(sv[p]!=']'){a.push_back(pv()); while(sv[p]==',')++p;} ++p; return V{a};}
    if(c=='{'){++p;Obj o; while(sv[p]!='}'){std::string k=ps(); while(sv[p]!=':')++p; ++p; o[k]=pv(); while(sv[p]==',')++p;} ++p; return V{o};}
    if(sv.substr(p,4)=="true"){p+=4;return V{true};}
    if(sv.substr(p,5)=="false"){p+=5;return V{false};}
    if(sv.substr(p,4)=="null"){p+=4;return V{nullptr};}
    return V{pn()};
}
static const std::string& gs(const Obj& o, const std::string& k){ return std::get<std::string>(o.at(k).d); }
static double gn(const Obj& o, const std::string& k){ return std::get<double>(o.at(k).d); }

int main() {
    const std::string cfg =
        R"({"host":"0.0.0.0","port":8080,"tls":true,)"
        R"("backends":["10.0.0.1:9000","10.0.0.2:9000"],"timeout_ms":1500})";
    p = 0; sv = cfg;
    Obj root = std::get<Obj>(pv().d);
    std::cout << "[config] host=" << gs(root,"host")
              << " port=" << (int)gn(root,"port")
              << " tls=" << (std::get<bool>(root.at("tls").d) ? "on" : "off") << "\n";
    const Arr& b = std::get<Arr>(root.at("backends").d);
    std::cout << "[config] backends(" << b.size() << "):\n";
    for (const auto& e : b) std::cout << "  - " << std::get<std::string>(e.d) << "\n";
    std::cout << "[config] timeout_ms=" << (int)gn(root,"timeout_ms") << "\n";
    return 0;
}
