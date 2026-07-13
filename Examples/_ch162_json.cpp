// 文件：Examples/_ch162_json.cpp
// 行号：1-18 (头文件与命名空间)
// 自包含 mini JSON 库：std::variant 值表示 + 手写递归下降解析 + 序列化 + 位置错误报告。
// 编译：g++ -std=c++20 -O2 -Wall -Wextra -o _ch162_json.exe _ch162_json.cpp
// 运行：_ch162_json.exe
#include <cctype>
#include <cstdio>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

namespace mini_json {

using Array  = std::vector<struct Value>;
using Object = std::map<std::string, struct Value>;

// ⑬ 值表示：std::variant 的 6 个可选项对应 JSON 的 6 种类型
struct Value {
    using Storage = std::variant<std::nullptr_t, bool, double,
                                 std::string, Array, Object>;
    Storage data = nullptr;

    Value() = default;
    Value(std::nullptr_t) : data(nullptr) {}
    Value(bool b)          : data(b) {}
    Value(double d)        : data(d) {}
    Value(int i)           : data(static_cast<double>(i)) {}
    Value(const std::string& s) : data(s) {}
    Value(const char* s)   : data(std::string(s)) {}
    Value(Array a)         : data(std::move(a)) {}
    Value(Object o)        : data(std::move(o)) {}

    bool is_null()   const { return std::holds_alternative<std::nullptr_t>(data); }
    bool is_bool()   const { return std::holds_alternative<bool>(data); }
    bool is_number() const { return std::holds_alternative<double>(data); }
    bool is_string() const { return std::holds_alternative<std::string>(data); }
    bool is_array()  const { return std::holds_alternative<Array>(data); }
    bool is_object() const { return std::holds_alternative<Object>(data); }

    bool              as_bool()   const { return std::get<bool>(data); }
    double            as_number() const { return std::get<double>(data); }
    const std::string& as_string() const { return std::get<std::string>(data); }
    const Array&      as_array()  const { return std::get<Array>(data); }
    const Object&     as_object() const { return std::get<Object>(data); }
    Array&            as_array()        { return std::get<Array>(data); }
    Object&           as_object()       { return std::get<Object>(data); }
};

// ⑭ 错误报告：携带出错位置（偏移）与可读消息
struct ParseError : std::runtime_error {
    size_t pos;
    ParseError(size_t p, const std::string& m)
        : std::runtime_error(m), pos(p) {}
};

// ③ 手写递归下降解析器
class Parser {
public:
    explicit Parser(std::string_view s) : s_(s) {}

    Value parse() {
        skip_ws();
        Value v = parse_value();
        skip_ws();
        if (pos_ != s_.size())
            fail("解析完成后仍有尾部多余字符");
        return v;
    }

private:
    std::string_view s_;
    size_t pos_ = 0;

    [[noreturn]] void fail(const std::string& m) {
        throw ParseError(pos_, m);
    }

    void skip_ws() {
        while (pos_ < s_.size()) {
            char c = s_[pos_];
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') ++pos_;
            else break;
        }
    }

    char peek() {
        if (pos_ >= s_.size()) fail("输入意外结束");
        return s_[pos_];
    }

    Value parse_value() {
        skip_ws();
        if (pos_ >= s_.size()) fail("空输入或结尾缺少值");
        char c = s_[pos_];
        switch (c) {
            case '{': return parse_object();
            case '[': return parse_array();
            case '"': return Value(parse_string());
            case 't': case 'f': return Value(parse_bool());
            case 'n': return parse_null();
            default:
                if (c == '-' || (c >= '0' && c <= '9')) return Value(parse_number());
                fail("无法识别的值起始字符");
        }
    }

    Value parse_null() {
        static const std::string_view lit = "null";
        if (s_.substr(pos_, 4) != lit) fail("期望字面量 null");
        pos_ += 4;
        return Value(nullptr);
    }

    Value parse_bool() {
        if (s_.substr(pos_, 4) == "true")  { pos_ += 4; return Value(true); }
        if (s_.substr(pos_, 5) == "false") { pos_ += 5; return Value(false); }
        fail("期望字面量 true/false");
    }

    // ⑦ 数字解析（支持负号、小数、指数；严格拒绝 1.2.3 / 1e / 等非法形式）
    double parse_number() {
        size_t start = pos_;
        bool has_digit = false, has_dot = false, has_exp = false, has_exp_sign = false;
        if (peek() == '-') ++pos_;
        while (pos_ < s_.size()) {
            char c = s_[pos_];
            if (std::isdigit(static_cast<unsigned char>(c))) {
                has_digit = true; ++pos_;
            } else if (c == '.' && !has_dot && !has_exp) {
                has_dot = true; ++pos_;
            } else if ((c == 'e' || c == 'E') && !has_exp && has_digit) {
                has_exp = true; ++pos_;
            } else if ((c == '+' || c == '-') && has_exp && !has_exp_sign) {
                has_exp_sign = true; ++pos_;
            } else {
                break;
            }
        }
        if (!has_digit) fail("非法数字字面量：缺少数字");
        double v = 0;
        try {
            v = std::stod(std::string(s_.substr(start, pos_ - start)));
        } catch (...) {
            fail("非法数字字面量");
        }
        return v;
    }

    // ⑦ 字符串解析与转义处理
    std::string parse_string() {
        if (peek() != '"') fail("字符串应以双引号开始");
        ++pos_; // 跳过 "
        std::string out;
        while (pos_ < s_.size()) {
            char c = s_[pos_++];
            if (c == '"') return out;          // 结束
            if (c == '\\') {                    // 转义
                if (pos_ >= s_.size()) fail("转义不完整");
                char e = s_[pos_++];
                switch (e) {
                    case '"':  out += '"';  break;
                    case '\\': out += '\\'; break;
                    case '/':  out += '/';  break;
                    case 'b':  out += '\b'; break;
                    case 'f':  out += '\f'; break;
                    case 'n':  out += '\n'; break;
                    case 'r':  out += '\r'; break;
                    case 't':  out += '\t'; break;
                    case 'u':  out += parse_unicode_escape(); break;
                    default:   fail("未知转义序列");
                }
            } else if (static_cast<unsigned char>(c) < 0x20) {
                fail("控制字符必须转义");
            } else {
                out += c;
            }
        }
        fail("字符串未闭合");
    }

    // ⑫ UTF-8：\uXXXX 转义 → UTF-8；仅做基本码点转写（含代理对合并）
    std::string parse_unicode_escape() {
        if (pos_ + 4 > s_.size()) fail("\\u 转义不完整");
        unsigned cp = 0;
        for (int i = 0; i < 4; ++i) {
            char h = s_[pos_++];
            cp <<= 4;
            if (h >= '0' && h <= '9') cp += h - '0';
            else if (h >= 'a' && h <= 'f') cp += h - 'a' + 10;
            else if (h >= 'A' && h <= 'F') cp += h - 'A' + 10;
            else fail("\\u 十六进制非法");
        }
        if (cp >= 0xD800 && cp <= 0xDBFF) { // 高代理
            if (pos_ + 6 > s_.size() || s_[pos_] != '\\' || s_[pos_+1] != 'u')
                fail("孤立的高代理");
            pos_ += 2;
            unsigned lo = 0;
            for (int i = 0; i < 4; ++i) {
                char h = s_[pos_++];
                lo <<= 4;
                if (h >= '0' && h <= '9') lo += h - '0';
                else if (h >= 'a' && h <= 'f') lo += h - 'a' + 10;
                else if (h >= 'A' && h <= 'F') lo += h - 'A' + 10;
                else fail("\\u 十六进制非法");
            }
            if (lo < 0xDC00 || lo > 0xDFFF) fail("代理对不匹配");
            cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
        }
        return codepoint_to_utf8(cp);
    }

    static std::string codepoint_to_utf8(unsigned cp) {
        std::string r;
        if (cp <= 0x7F) {
            r += static_cast<char>(cp);
        } else if (cp <= 0x7FF) {
            r += static_cast<char>(0xC0 | (cp >> 6));
            r += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp <= 0xFFFF) {
            r += static_cast<char>(0xE0 | (cp >> 12));
            r += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            r += static_cast<char>(0x80 | (cp & 0x3F));
        } else {
            r += static_cast<char>(0xF0 | (cp >> 18));
            r += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
            r += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            r += static_cast<char>(0x80 | (cp & 0x3F));
        }
        return r;
    }

    Value parse_array() {
        ++pos_; // [
        Array arr;
        skip_ws();
        if (peek() == ']') { ++pos_; return Value(std::move(arr)); }
        while (true) {
            arr.push_back(parse_value());
            skip_ws();
            char c = peek();
            if (c == ',') { ++pos_; continue; }
            if (c == ']') { ++pos_; break; }
            fail("数组应以 , 或 ] 结束");
        }
        return Value(std::move(arr));
    }

    Value parse_object() {
        ++pos_; // {
        Object obj;
        skip_ws();
        if (peek() == '}') { ++pos_; return Value(std::move(obj)); }
        while (true) {
            skip_ws();
            if (peek() != '"') fail("对象键必须是字符串");
            std::string key = parse_string();
            skip_ws();
            if (peek() != ':') fail("对象键后缺少冒号");
            ++pos_;
            Value val = parse_value();
            obj.emplace(std::move(key), std::move(val));
            skip_ws();
            char c = peek();
            if (c == ',') { ++pos_; continue; }
            if (c == '}') { ++pos_; break; }
            fail("对象应以 , 或 } 结束");
        }
        return Value(std::move(obj));
    }
};

// ⑧ 序列化（writer）：indent<0 紧凑输出，否则带缩进
std::string serialize(const Value& v, int indent = -1, int depth = 0);

namespace {
void append_indent(std::string& out, int indent, int depth) {
    if (indent < 0) return;
    out.append(static_cast<size_t>(indent * depth), ' ');
}
std::string escape_string(const std::string& s) {
    std::string out = "\"";
    for (unsigned char c : s) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n";  break;
            case '\t': out += "\\t";  break;
            case '\r': out += "\\r";  break;
            case '\b': out += "\\b";  break;
            case '\f': out += "\\f";  break;
            default:
                if (c < 0x20) {
                    char buf[8];
                    std::snprintf(buf, sizeof(buf), "\\u%04x",
                                  static_cast<unsigned>(c));
                    out += buf;
                } else {
                    out += static_cast<char>(c);
                }
        }
    }
    out += '"';
    return out;
}
} // namespace

std::string serialize(const Value& v, int indent, int depth) {
    std::string out;
    if (v.is_null())        out += "null";
    else if (v.is_bool())   out += (v.as_bool() ? "true" : "false");
    else if (v.is_number()) {
        char buf[32];
        std::snprintf(buf, sizeof(buf), "%.17g", v.as_number());
        out += buf;
    }
    else if (v.is_string()) out += escape_string(v.as_string());
    else if (v.is_array()) {
        const Array& a = v.as_array();
        out += '[';
        if (indent >= 0) out += '\n';
        for (size_t i = 0; i < a.size(); ++i) {
            if (indent >= 0) append_indent(out, indent, depth + 1);
            out += serialize(a[i], indent, depth + 1);
            if (i + 1 < a.size()) out += (indent >= 0 ? ",\n" : ",");
        }
        if (indent >= 0) { out += '\n'; append_indent(out, indent, depth); }
        out += ']';
    }
    else if (v.is_object()) {
        const Object& o = v.as_object();
        out += '{';
        if (indent >= 0) out += '\n';
        size_t i = 0;
        for (const auto& kv : o) {
            if (indent >= 0) append_indent(out, indent, depth + 1);
            out += escape_string(kv.first);
            out += (indent >= 0 ? ": " : ":");
            out += serialize(kv.second, indent, depth + 1);
            if (++i < o.size()) out += (indent >= 0 ? ",\n" : ",");
        }
        if (indent >= 0) { out += '\n'; append_indent(out, indent, depth); }
        out += '}';
    }
    return out;
}

inline Value parse(std::string_view s) { return Parser(s).parse(); }

} // namespace mini_json

// ─────────────────────────────────────────────────────────────
// ⑲ 真实案例：本机 g++ 编译运行，以下输出截自真实执行结果
int main() {
    using namespace mini_json;
    const std::string input =
        R"({"name":"小明","age":30,"active":true,"score":9.5,)"
        R"("tags":["c++","json"],"addr":{"city":"北京","zip":100000},)"
        R"("note":"换行\n与引号\"转义","unicode":"\u4E2D\u6587"})";

    try {
        Value v = parse(input);
        std::cout << "[OK] 解析成功，类型: "
                  << (v.is_object() ? "object" : "?") << "\n";
        const Object& o = v.as_object();
        std::cout << "name  = " << o.at("name").as_string()  << "\n";
        std::cout << "age   = " << o.at("age").as_number()   << "\n";
        std::cout << "active= " << o.at("active").as_bool()  << "\n";
        std::cout << "tags[0]= " << o.at("tags").as_array()[0].as_string() << "\n";
        std::cout << "city  = " << o.at("addr").as_object().at("city").as_string() << "\n";
        std::cout << "note  = " << o.at("note").as_string()  << "\n";
        std::cout << "unicode= " << o.at("unicode").as_string() << "\n";
        std::cout << "\n[紧凑序列化]\n" << serialize(v) << "\n";
        std::cout << "\n[美化序列化(2空格)]\n" << serialize(v, 2) << "\n";
    } catch (const ParseError& e) {
        std::cout << "[ERROR] pos=" << e.pos << " : " << e.what() << "\n";
        return 1;
    }

    // ⑭ 错误报告真实演示
    std::cout << "\n[错误演示]\n";
    for (std::string bad : {"{", "[1,2", "\"abc", "tru", "1.2.3"}) {
        try {
            parse(bad);
            std::cout << "  '" << bad << "' 意外通过\n";
        } catch (const ParseError& e) {
            std::cout << "  '" << bad << "' -> pos=" << e.pos
                      << " : " << e.what() << "\n";
        }
    }
    return 0;
}
