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
// 骨架范围（诚实标注，后续里程碑扩展）：
//   - 数字统一存 double；序列化时整数回显为整数、浮点用 std::to_chars 最短往返
//   - 字符串支持全部必要的反向转义；\uXXXX 仅支持 BMP 内、且当前仅编码 ASCII
//     （非 ASCII 转义抛 parse_error，见 parse_unicode 的诚实标注）
//   - 提供只读访问 + 构造；可变编辑 / 路径查询 / 错误行号 留待里程碑 2
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

    // 越界/缺键用 .at() 抛 std::out_of_range，避免静默 UB
    const Value& at(std::size_t i)      const { return as_array().at(i); }
    const Value& at(const std::string& k) const { return as_object().at(k); }
    const Value& operator[](std::size_t i)      const { return at(i); }
    const Value& operator[](const std::string& k) const { return at(k); }

private:
    storage v_;
};

// 解析错误：携带字节偏移，便于定位（里程碑 2 追加行/列）
class parse_error : public std::runtime_error {
public:
    explicit parse_error(std::string msg, std::size_t pos)
        : std::runtime_error(msg + " at offset " + std::to_string(pos)), pos_(pos) {}
    std::size_t pos() const noexcept { return pos_; }
private:
    std::size_t pos_;
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
            throw parse_error("unexpected trailing input", pos_);
        return v;
    }

private:
    std::string text_;
    std::size_t pos_ = 0;

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
        if (!consume(c)) throw parse_error(std::string("expected '") + c + "'", pos_);
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
        else throw parse_error("invalid number", pos_);

        if (peek() == '.') {
            ++pos_;
            if (peek() < '0' || peek() > '9') throw parse_error("invalid fraction", pos_);
            while (peek() >= '0' && peek() <= '9') ++pos_;
        }
        if (peek() == 'e' || peek() == 'E') {
            ++pos_;
            if (peek() == '+' || peek() == '-') ++pos_;
            if (peek() < '0' || peek() > '9') throw parse_error("invalid exponent", pos_);
            while (peek() >= '0' && peek() <= '9') ++pos_;
        }

        const std::string num = text_.substr(start, pos_ - start);
        char* end = nullptr;
        const double val = std::strtod(num.c_str(), &end);
        if (end != num.c_str() + num.size()) throw parse_error("invalid number", start);
        return Value(val);
    }

    std::string parse_string() {
        expect('"');
        std::string out;
        while (true) {
            const char c = peek();
            if (c == '"') { ++pos_; break; }
            if (c == '\0' || c == '\n' || c == '\r') throw parse_error("unterminated string", pos_);
            if (c == '\\') { ++pos_; out += parse_escape(); continue; }
            out += c;
            ++pos_;
        }
        return out;  // 由调用方 move 进 Value（NRVO 免拷贝）
    }

    char parse_escape() {
        const char c = peek();
        switch (c) {
            case '"':  ++pos_; return '"';
            case '\\': ++pos_; return '\\';
            case '/':  ++pos_; return '/';
            case 'b':  ++pos_; return '\b';
            case 'f':  ++pos_; return '\f';
            case 'n':  ++pos_; return '\n';
            case 'r':  ++pos_; return '\r';
            case 't':  ++pos_; return '\t';
            case 'u':  return parse_unicode();
            default:   throw parse_error("invalid escape sequence", pos_);
        }
    }

    char parse_unicode() {
        ++pos_;  // 跳过 'u'
        unsigned cp = 0;
        for (int i = 0; i < 4; ++i) {
            const char c = peek();
            unsigned d = 0;
            if (c >= '0' && c <= '9')       d = static_cast<unsigned>(c - '0');
            else if (c >= 'a' && c <= 'f')  d = static_cast<unsigned>(c - 'a' + 10);
            else if (c >= 'A' && c <= 'F')  d = static_cast<unsigned>(c - 'A' + 10);
            else throw parse_error("bad unicode escape", pos_);
            cp = cp * 16 + d;
            ++pos_;
        }
        // 骨架简化：仅编码 BMP 内的 ASCII code point；非 ASCII \uXXXX 的 UTF-8
        // 编码（含代理对）留待里程碑 3，这里诚实抛错而非静默产出错误字节。
        if (cp < 0x80) return static_cast<char>(cp);
        throw parse_error("non-ASCII \\uXXXX not yet supported", pos_);
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
            if (peek() != '"') throw parse_error("object key must be a string", pos_);
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

inline void serialize_into(const Value& v, std::string& out) {
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
                    // 非有限值（nan/inf）无合法 JSON 表示，显式拒绝
                    throw parse_error("cannot serialize non-finite number", 0);
                }
            }
            break;
        }
        case Value::Type::String:
            escape_string(v.as_string(), out);
            break;
        case Value::Type::Array: {
            out += '[';
            bool first = true;
            for (const Value& e : v.as_array()) {
                if (!first) out += ',';
                first = false;
                serialize_into(e, out);
            }
            out += ']';
            break;
        }
        case Value::Type::Object: {
            out += '{';
            bool first = true;
            for (const auto& [k, val] : v.as_object()) {
                if (!first) out += ',';
                first = false;
                escape_string(k, out);
                out += ':';
                serialize_into(val, out);
            }
            out += '}';
            break;
        }
    }
}

inline std::string serialize(const Value& v) {
    std::string out;
    serialize_into(v, out);
    return out;
}

// 顶层便捷入口
inline Value parse(const std::string& text) { return Parser(text).parse(); }

}  // namespace json