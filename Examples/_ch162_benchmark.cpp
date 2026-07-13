// 文件：Examples/_ch162_benchmark.cpp
// 行号：46-54（chrono 计时区间）
// ⑪ 性能基准：用 std::chrono 高精度时钟测量真实解析耗时（本机 g++ -O2）。
#include <chrono>
#include <cstdio>
#include <iostream>
#include <map>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

// —— 极简递归下降解析（仅用于基准，覆盖全部 JSON 类型）——
struct V;
using Arr = std::vector<V>;
using Obj = std::map<std::string, V>;
struct V { std::variant<std::nullptr_t, bool, double, std::string, Arr, Obj> d{nullptr}; };

static size_t p;
static std::string_view sv;
static V parse_value();
static std::string parse_str(){
    ++p; std::string s;
    while(p<sv.size()&&sv[p]!='"') s+=sv[p++];
    ++p; return s;
}
static double parse_num(){
    size_t a=p; while(p<sv.size()&&(std::isdigit((unsigned char)sv[p])||sv[p]=='.'||sv[p]=='-'||sv[p]=='e'||sv[p]=='E'))++p;
    return std::stod(std::string(sv.substr(a,p-a)));
}
static V parse_value(){
    while(p<sv.size()&&(sv[p]==' '||sv[p]=='\n'||sv[p]=='\t'||sv[p]=='\r'))++p;
    char c=sv[p];
    if(c=='"') return V{parse_str()};
    if(c=='['){++p;Arr a; while(sv[p]!=']'){a.push_back(parse_value()); while(sv[p]==',')++p;} ++p; return V{a};}
    if(c=='{'){++p;Obj o; while(sv[p]!='}'){std::string k=parse_str(); while(sv[p]!=':')++p; ++p; V v=parse_value(); o[k]=std::move(v); while(sv[p]==',')++p;} ++p; return V{o};}
    if(sv.substr(p,4)=="true")  { p+=4; return V{true}; }
    if(sv.substr(p,5)=="false") { p+=5; return V{false}; }
    if(sv.substr(p,4)=="null")  { p+=4; return V{nullptr}; }
    return V{parse_num()};
}

int main() {
    const std::string doc =
        R"({"users":[{"id":1,"name":"alice","score":9.81},)"
        R"({"id":2,"name":"bob","score":8.42},)"
        R"({"id":3,"name":"carol","score":7.03}],"ok":true,"count":3})";
    const int N = 200000;

    // ⑪ 计时：解析 N 次
    auto t0 = std::chrono::high_resolution_clock::now();
    volatile double sink = 0;
    for (int i = 0; i < N; ++i) {
        p = 0; sv = doc;
        V root = parse_value();
        if (std::holds_alternative<Obj>(root.d))
            sink += static_cast<double>(std::get<Obj>(root.d).size());
    }
    auto t1 = std::chrono::high_resolution_clock::now();

    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cout << "解析次数 N = " << N << "\n";
    std::cout << "总耗时   = " << ms << " ms\n";
    std::cout << "单文档均 = " << (ms * 1000.0 / N) << " us\n";
    std::cout << "吞吐     ≈ " << (N / (ms / 1000.0)) << " 文档/秒\n";
    return 0;
}
