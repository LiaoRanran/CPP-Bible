// 手写 JSON 库自测 —— 无第三方依赖，仅靠断言。
// 编译：g++ -std=c++23 -O2 -Wall -Wextra -o json_test.exe json_test.cpp
// 运行：./json_test.exe（非 0 退出码 = 失败）
#include "json.hpp"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string>

namespace {

int g_fail = 0;
int g_pass = 0;

void check(bool ok, const char* what, const std::string& detail = {}) {
    if (ok) {
        ++g_pass;
    } else {
        ++g_fail;
        std::fprintf(stderr, "[FAIL] %s%s%s\n", what,
                     detail.empty() ? "" : " : ",
                     detail.c_str());
    }
}

void check_throw(const std::string& text, const char* what) {
    try {
        json::parse(text);
        check(false, what, "expected parse_error but none thrown");
    } catch (const json::parse_error&) {
        ++g_pass;
    } catch (const std::exception& e) {
        check(false, what, std::string("wrong exception: ") + e.what());
    }
}

std::string round_trip(const std::string& text) {
    return json::serialize(json::parse(text));
}

void test_roundtrip() {
    // 标量
    check(round_trip("null") == "null", "roundtrip null", round_trip("null"));
    check(round_trip("true") == "true", "roundtrip true");
    check(round_trip("false") == "false", "roundtrip false");
    // 数字：整数回显、浮点、指数
    check(round_trip("0") == "0", "roundtrip 0");
    check(round_trip("-42") == "-42", "roundtrip -42");
    check(round_trip("3.14") == "3.14", "roundtrip 3.14");
    check(round_trip("1e3") == "1000", "roundtrip 1e3 -> 1000");
    check(round_trip("-2.5e-2") == "-0.025", "roundtrip -2.5e-2");
    // 字符串转义（往返一致）
    check(round_trip("\"\"") == "\"\"", "roundtrip empty string");
    check(round_trip("\"hello\"") == "\"hello\"", "roundtrip hello");
    check(round_trip("\"a\\n\\t\\\"\\\\/b\"") == "\"a\\n\\t\\\"\\\\/b\"",
          "roundtrip escapes");
    // 嵌套
    check(round_trip("[]") == "[]", "roundtrip []");
    check(round_trip("{}") == "{}", "roundtrip {}");
    check(round_trip("[1,2,3]") == "[1,2,3]", "roundtrip array");
    check(round_trip("{\"a\":1,\"b\":[true,null]}") == "{\"a\":1,\"b\":[true,null]}",
          "roundtrip nested object");
}

void test_access() {
    json::Value v = json::parse("{\"s\":\"x\",\"n\":1.5,\"a\":[10,20,30],\"o\":{\"k\":true},\"z\":null}");
    check(v.is_object(), "v is object");
    check(v.type() == json::Value::Type::Object, "v type object");

    check(v.at("s").as_string() == "x", "at string");
    check(v["n"].as_number() == 1.5, "at number");
    check(v.at("a").as_array().size() == 3, "array size");
    check(v["a"][1].as_number() == 20, "array index");
    check(v.at("o").at("k").as_bool() == true, "nested bool");
    check(v.at("z").is_null(), "null access");

    // 缺键 / 越界应抛 std::out_of_range（源自 .at()）
    bool threw = false;
    try { (void)v.at("missing"); } catch (const std::out_of_range&) { threw = true; }
    check(threw, "missing key throws out_of_range");

    threw = false;
    try { (void)v.at("a").at(99); } catch (const std::out_of_range&) { threw = true; }
    check(threw, "out-of-range index throws");
}

void test_type_mismatch() {
    json::Value v = json::parse("123");
    bool threw = false;
    try { (void)v.as_string(); } catch (const std::bad_variant_access&) { threw = true; }
    check(threw, "as_string on number throws bad_variant_access");
}

void test_errors() {
    check_throw("", "empty input");
    check_throw("   ", "whitespace only");
    check_throw("nul", "truncated literal");
    check_throw("tru", "truncated true");
    check_throw("01", "leading zero");
    check_throw("-", "bare minus");
    check_throw("1.", "trailing dot");
    check_throw("1e", "bare exponent");
    check_throw("[1,]", "trailing comma array");
    check_throw("{\"a\":1,}", "trailing comma object");
    check_throw("{\"a\" 1}", "missing colon");
    check_throw("{\"a\":1", "unclosed object");
    check_throw("[1,2", "unclosed array");
    check_throw("\"abc", "unterminated string");
    check_throw("\"a\\x\"", "bad escape");
    check_throw("{\"a\":1} x", "trailing garbage");
    check_throw("[1] [2]", "two roots");
}

void test_unicode_ascii() {
    // \uXXXX 仅支持 ASCII（骨架诚实标注）；验证 \u0041 == 'A'
    json::Value v = json::parse("\"\\u0041\"");
    check(v.as_string() == "A", "unicode escape ASCII 'A'");
    // 非 ASCII \uXXXX 应诚实抛错（未静默产出错误字节）
    check_throw("\"\\u00e9\"", "non-ASCII unicode throws (honest)");
}

void test_serialize_control() {
    // 控制字符 < 0x20 序列化为 \u00XX（除已转义者）
    std::string s = "a\x01z";
    json::Value v = s;
    check(json::serialize(v) == "\"a\\u0001z\"", "control char -> \\u0001");
}

}  // namespace

int main() {
    test_roundtrip();
    test_access();
    test_type_mismatch();
    test_errors();
    test_unicode_ascii();
    test_serialize_control();

    std::printf("json_test: %d passed, %d failed\n", g_pass, g_fail);
    return g_fail == 0 ? 0 : 1;
}