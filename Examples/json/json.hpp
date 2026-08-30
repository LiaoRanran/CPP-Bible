#pragma once
// 手写 JSON 库骨架 —— 贯穿项目线（台阶二）核心模块
//
// 只用标准库，串联全书多个 part 的知识点：
//   part04 内存：std::variant 递归类型（值语义，无裸 new，无 vptr）
//   part05 OO  ：parse_error 继承 std::runtime_error（异常层级）
//   part06 泛型：std::variant / std::map / 重载构造（类型安全联合）
//   part07 容器：Array=vector / Object=map（有序键）
//   part08 移动：构造与 parse 全程 std::move（零深拷贝）
//   part03 底层：递归下降解析（无第三方依赖）
//
// 里程碑（诚实标注，已实现 / 待扩展）：
//   [M1 ✅] 数字统一存 double；序列化整数回显整数、浮点用 std::to_chars 最短往返
//   [M2 ✅] 可变编辑（非 const 访问器 + set）+ 点路径查询 find + 错误行号（line/col）
//   [M3 ✅] 字符串 \uXXXX 完整 UTF-8 编码（含 UTF-16 代理对，如 \ud83d\ude00 → 😀）
//   [M4 待] 数字精度策略（任意精度 / 保留原始字面量）——当前统一 double，极端值有进位
#include <charconv>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <variant>
#include <vector>

namespace json {

class Value;

using Null   = std::nullptr_t;
using Array  = std::vector<Value>;
using Object = std::map<std::string, Value>;

// 递归变体类型：JSON 的六种取值。std::variant 保证"同一时刻只有一种取值"，
// 比继承 + vtable 更省空间（无 vptr），访问代价是编译期已知的 get<N>。
class Value {
public:
    using storage = std::variant<Null, bool, double, std::string, Array, Object>;

    Value() = default;
    Value(Null)              : v_(nullptr) {}
    Value(bool b)            : v_(b) {}
    Value(int i)             : v_(static_cast<double>(i)) {}
    Value(unsigned int i)    : v_(static_cast<double>(i)) {}
    Value(long long i)       : v_(static_cast<double>(i)) {}
    Value(double d)          : v_(d) {}
    Value(std::string s)     : v_(std::move(s)) {}
    Value(const char* s)     : v_(std::string(s)) {}
    Value(Array a)           : v_(std::move(a)) {}
    Value(Object o)          : v_(std::move(o)) {}

    enum class Type { Null, Bool, Number, String, Array, Object };

    Type type() const noexcept {
        switch (v_.index()) {
            case 0:  return Type::Null;
            case 1:  return Type::Bool;
            case 2:  return Type::Number;
            case 3:  return Type::String;
            case 4:  return Type::Array;
            default: return Type::Object;
        }
    }
    bool is_null()   const noexcept { return type() == Type::Null; }
    bool is_bool()   const noexcept { return type() == Type::Bool; }
    bool is_number() const noexcept { return type() == Type::Number; }
    bool is_string() const noexcept { return type() == Type::String; }
    bool is_array()  const noexcept { return type() == Type::Array; }
    bool is_object() const noexcept { return type() == Type::Object; }

    // 类型不匹配时抛出 std::bad_variant_access（源自 std::get）
    bool               as_bool()   const { return std::get<bool>(v_); }
    double             as_number() const { return std::get<double>(v_); }
    const std::string& as_string() const { return std::get<std::string>(v_); }
    const Array&       as_array()  const { return std::get<Array>(v_); }
    const Object&      as_object() const { return std::get<Object>(v_); }

    // 可变访问（里程碑 2）：返回引用可就地编辑，类型不符仍抛 bad_variant_access
    bool&        as_bool()   { return std::get<bool>(v_); }
    double&      as_number() { return std::get<double>(v_); }
    std::string& as_string() { return std::get<std::string>(v_); }
    Array&       as_array()  { return std::get<Array>(v_); }
    Object&      as_object() { return std::get<Object>(v_); }

    // 越界/缺键用 .at() 抛 std::out_of_range，避免静默 UB
    const Value& at(std::size_t i)        const { return as_array().at(i); }
    const Value& at(const std::string& k) const { return as_object().at(k); }
    Value&       at(std::size_t i)              { return as_array().at(i); }
    Value&       at(const std::string& k)       { return as_object().at(k); }
    const Value& operator[](std::size_t i)      const { return at(i); }
    const Value& operator[](const std::string& k) const { return at(k); }
    Value&       operator[](std::size_t i)            { return at(i); }
    Value&       operator[](const std::string& k)     { return at(k); }

    // 就地改值 / 改类型（可链式）：v.set("x").set(1.5)
    Value& set(Null)          { v_ = nullptr;              return *this; }
    Value& set(bool b)        { v_ = b;                    return *this; }
    Value& set(int i)         { v_ = static_cast<double>(i); return *this; }
    Value& set(double d)      { v_ = d;                    return *this; }
    Value& set(std::string s) { v_ = std::move(s);         return *this; }
    Value& set(const char* s) { v_ = std::string(s);       return *this; }  // 精确匹配，避免 set("x") 误走 set(bool)
    Value& set(Array a)       { v_ = std::move(a);         return *this; }
    Value& set(Object o)      { v_ = std::move(o);         return *this; }

    // 点路径查询（里程碑 2）："a.b.0.c"；数组下标用非负整数；层级类型不符返回 nullptr
    const Value* find(const std::string& path) const {
        const Value* cur = this;
        std::size_t start = 0;
        while (true) {
            const std::size_t dot = path.find('.', start);
            const std::string seg =
                path.substr(start, dot == std::string::npos ? std::string::npos : dot - start);
            if (seg.empty()) return nullptr;
            if (const Object* obj = std::get_if<Object>(&cur->v_)) {
                auto it = obj->find(seg);
                if (it == obj->end()) return nullptr;
                cur = &it->second;
            } else if (const Array* arr = std::get_if<Array>(&cur->v_)) {
                std::size_t idx = 0;
                for (char c : seg) {
                    if (c < '0' || c > '9') return nullptr;
                    idx = idx * 10 + static_cast<std::size_t>(c - '0');
                }
                if (idx >= arr->size()) return nullptr;
                cur = &(*arr)[idx];
            } else {
                return nullptr;
            }
            if (dot == std::string::npos) break;
            start = dot + 1;
        }
        return cur;
    }
    Value* find(const std::string& path) {
        return const_cast<Value*>(static_cast<const Value*>(this)->find(path));
    }

private:
    storage v_;
};

// 解析错误：携带字节偏移 + 行/列（1-based），供报错定位。
// 双参版本用于非解析阶段（如序列化）抛出的错误，line/col 记为 0。
class parse_error : public std::runtime_error {
public:
    parse_error(std::string msg, std::size_t pos, std::size_t line, std::size_t col)
        : std::runtime_error(msg + " at offset " + std::to_string(pos) +
                             " (line " + std::to_string(line) +
                             ", col " + std::to_string(col) + ")"),
          pos_(pos), line_(line), col_(col) {}
    parse_error(std::string msg, std::size_t pos)
        : parse_error(std::move(msg), pos, 0, 0) {}
    std::size_t pos()  const noexcept { return pos_; }
    std::size_t line() const noexcept { return line_; }
    std::size_t col()  const noexcept { return col_; }
private:
    std::size_t pos_;
    std::size_t line_;
    std::size_t col_;
};

// 递归下降解析器：每个非终结符一个方法，按当前字符分派。
// 这是 JSON 文法最简单、最"可读"的实现方式（对比表驱动/生成器）。
class Parser {
public:
    explicit Parser(std::string text) : text_(std::move(text)) {}

    Value parse() {
        Value v = parse_value();
        skip_ws();
        if (pos_ != text_.size())
            fail("unexpected trailing input");
        return v;
    }

private:
    std::string text_;
    std::size_t pos_ = 0;

    // 抛错并定位到给定字节偏移 → 行/列（1-based）
    [[noreturn]] void fail(const std::string& msg, std::size_t pos) {
        std::size_t line = 1, col = 1;
        for (std::size_t i = 0; i < pos && i < text_.size(); ++i) {
            if (text_[i] == '\n') { ++line; col = 1; }
            else ++col;
        }
        throw parse_error(msg, pos, line, col);
    }
    [[noreturn]] void fail(const std::string& msg) { fail(msg, pos_); }

    // Unicode code point → UTF-8 字节序列（1~4 字节），按标准编码规则
    static void append_utf8(unsigned cp, std::string& out) {
        if (cp < 0x80) {
            out += static_cast<char>(cp);
        } else if (cp < 0x800) {
            out += static_cast<char>(0xC0 | (cp >> 6));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else if (cp < 0x10000) {
            out += static_cast<char>(0xE0 | (cp >> 12));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        } else {
            out += static_cast<char>(0xF0 | (cp >> 18));
            out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
            out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
            out += static_cast<char>(0x80 | (cp & 0x3F));
        }
    }

    char peek() const noexcept { return pos_ < text_.size() ? text_[pos_] : '\0'; }

    void skip_ws() noexcept {
        while (pos_ < text_.size()) {
            char c = text_[pos_];
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') ++pos_;
            else break;
        }
    }

    bool consume(char c) noexcept {
        if (peek() == c) { ++pos_; return true; }
        return false;
    }

    void expect(char c) {
        if (!consume(c)) fail(std::string("expected '") + c + "'");
    }

    Value parse_value() {
        skip_ws();
        switch (peek()) {
            case 'n': return parse_literal("null", Value(nullptr));
            case 't': return parse_literal("true", Value(true));
            case 'f': return parse_literal("false", Value(false));
            case '"': return Value(parse_string());
            case '[': return parse_array();
            case '{': return parse_object();
            default:  return parse_number();
        }
    }

    Value parse_literal(const char* lit, Value v) {
        for (const char* p = lit; *p; ++p) expect(*p);
        return v;
    }

    // 数字文法：-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?
    Value parse_number() {
        const std::size_t start = pos_;
        if (peek() == '-') ++pos_;
        if (peek() == '0') ++pos_;
        else if (peek() >= '1' && peek() <= '9') { while (peek() >= '0' && peek() <= '9') ++pos_; }
        else fail("invalid number");

        if (peek() == '.') {
            ++pos_;
            if (peek() < '0' || peek() > '9') fail("invalid fraction");
            while (peek() >= '0' && peek() <= '9') ++pos_;
        }
        if (peek() == 'e' || peek() == 'E') {
            ++pos_;
            if (peek() == '+' || peek() == '-') ++pos_;
            if (peek() < '0' || peek() > '9') fail("invalid exponent");
            while (peek() >= '0' && peek() <= '9') ++pos_;
        }

        const std::string num = text_.substr(start, pos_ - start);
        char* end = nullptr;
        const double val = std::strtod(num.c_str(), &end);
        if (end != num.c_str() + num.size()) fail("invalid number", start);
        return Value(val);
    }

    std::string parse_string() {
        expect('"');
        std::string out;
        while (true) {
            const char c = peek();
            if (c == '"') { ++pos_; break; }
            if (c == '\0' || c == '\n' || c == '\r') fail("unterminated string");
            if (c == '\\') { ++pos_; out += parse_escape(); continue; }
            out += c;
            ++pos_;
        }
        return out;  // 由调用方 move 进 Value（NRVO 免拷贝）
    }

    std::string parse_escape() {
        const char c = peek();
        switch (c) {
            case '"':  ++pos_; return "\"";
            case '\\': ++pos_; return "\\";
            case '/':  ++pos_; return "/";
            case 'b':  ++pos_; return "\b";
            case 'f':  ++pos_; return "\f";
            case 'n':  ++pos_; return "\n";
            case 'r':  ++pos_; return "\r";
            case 't':  ++pos_; return "\t";
            case 'u':  return parse_unicode();
            default:   fail("invalid escape sequence");
        }
    }

    // 解析 \uXXXX（含 UTF-16 代理对），编码为 UTF-8 字节串返回
    std::string parse_unicode() {
        ++pos_;                       // 跳过 'u'
        unsigned cp = parse_hex4();
        if (cp >= 0xD800 && cp <= 0xDBFF) {   // 高代理：须紧跟 \uXXXX 低代理
            if (peek() == '\\' && pos_ + 1 < text_.size() && text_[pos_ + 1] == 'u') {
                pos_ += 2;
                const unsigned lo = parse_hex4();
                if (lo < 0xDC00 || lo > 0xDFFF) fail("invalid low surrogate");
                cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
            } else {
                fail("unpaired high surrogate");
            }
        } else if (cp >= 0xDC00 && cp <= 0xDFFF) {   // 低代理单独出现：非法
            fail("unpaired low surrogate");
        }
        std::string out;
        append_utf8(cp, out);
        return out;
    }

    unsigned parse_hex4() {
        unsigned cp = 0;
        for (int i = 0; i < 4; ++i) {
            const char c = peek();
            unsigned d;
            if (c >= '0' && c <= '9')      d = static_cast<unsigned>(c - '0');
            else if (c >= 'a' && c <= 'f') d = static_cast<unsigned>(c - 'a' + 10);
            else if (c >= 'A' && c <= 'F') d = static_cast<unsigned>(c - 'A' + 10);
            else fail("bad unicode escape");
            cp = cp * 16 + d;
            ++pos_;
        }
        return cp;
    }

    Value parse_array() {
        expect('[');
        Array arr;
        skip_ws();
        if (consume(']')) return Value(std::move(arr));
        while (true) {
            arr.push_back(parse_value());
            skip_ws();
            if (consume(']')) break;
            expect(',');
        }
        return Value(std::move(arr));
    }

    Value parse_object() {
        expect('{');
        Object obj;
        skip_ws();
        if (consume('}')) return Value(std::move(obj));
        while (true) {
            skip_ws();
            if (peek() != '"') fail("object key must be a string");
            std::string key = parse_string();
            skip_ws();
            expect(':');
            obj.emplace(std::move(key), parse_value());
            skip_ws();
            if (consume('}')) break;
            expect(',');
        }
        return Value(std::move(obj));
    }
};

// 序列化：Value → JSON 文本（往返可幂等：parse(serialize(v)) == v）
inline void escape_string(const std::string& s, std::string& out) {
    out += '"';
    for (const char c : s) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\b': out += "\\b";  break;
            case '\f': out += "\\f";  break;
            case '\n': out += "\\n";  break;
            case '\r': out += "\\r";  break;
            case '\t': out += "\\t";  break;
            default:
                if (static_cast<unsigned char>(c) < 0x20) {
                    char buf[8];
                    std::snprintf(buf, sizeof buf, "\\u%04x", static_cast<unsigned char>(c));
                    out += buf;
                } else {
                    out += c;
                }
        }
    }
    out += '"';
}

// 序列化：Value → JSON 文本。
// indent >= 0：多行美化（每层缩进 indent 空格）；indent < 0（默认）：紧凑单行。
inline void serialize_into(const Value& v, std::string& out, int indent, int level) {
    auto nl = [&](int lvl) {
        if (indent >= 0) {
            out += '\n';
            out.append(static_cast<std::size_t>(indent) * static_cast<std::size_t>(lvl), ' ');
        }
    };
    switch (v.type()) {
        case Value::Type::Null:
            out += "null";
            break;
        case Value::Type::Bool:
            out += v.as_bool() ? "true" : "false";
            break;
        case Value::Type::Number: {
            const double d = v.as_number();
            // 无损整数（long long 范围内）按整数回显，如 1e3 -> 1000
            if (d >= static_cast<double>(std::numeric_limits<long long>::min()) &&
                d <= static_cast<double>(std::numeric_limits<long long>::max()) &&
                d == static_cast<double>(static_cast<long long>(d))) {
                char buf[32];
                std::snprintf(buf, sizeof buf, "%lld", static_cast<long long>(d));
                out += buf;
            } else {
                // std::to_chars 最短往返表示：3.14 -> "3.14"，而非 %.17g 的
                // "3.1400000000000001"。对齐值语义（parse(serialize(x)) == x）。
                char buf[40];
                auto res = std::to_chars(buf, buf + sizeof buf, d);
                if (res.ec == std::errc()) {
                    out.append(buf, res.ptr);
                } else {
                    throw parse_error("cannot serialize non-finite number", 0);
                }
            }
            break;
        }
        case Value::Type::String:
            escape_string(v.as_string(), out);
            break;
        case Value::Type::Array: {
            const Array& a = v.as_array();
            out += '[';
            if (!a.empty()) {
                for (std::size_t i = 0; i < a.size(); ++i) {
                    if (i) out += ',';
                    nl(level + 1);
                    serialize_into(a[i], out, indent, level + 1);
                }
                nl(level);
            }
            out += ']';
            break;
        }
        case Value::Type::Object: {
            const Object& o = v.as_object();
            out += '{';
            if (!o.empty()) {
                std::size_t i = 0;
                for (const auto& [k, val] : o) {
                    if (i++) out += ',';
                    nl(level + 1);
                    escape_string(k, out);
                    out += ':';
                    if (indent >= 0) out += ' ';
                    serialize_into(val, out, indent, level + 1);
                }
                nl(level);
            }
            out += '}';
            break;
        }
    }
}

inline std::string serialize(const Value& v, int indent = -1) {
    std::string out;
    serialize_into(v, out, indent, 0);
    return out;
}

// 顶层便捷入口
inline Value parse(const std::string& text) { return Parser(text).parse(); }

}  // namespace json