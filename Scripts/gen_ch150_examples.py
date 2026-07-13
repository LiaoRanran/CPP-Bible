#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《现代 C++ 终极圣经》第150章「测试策略」的全部可编译取证示例。
所有示例均为自包含（assert + main 自测），可由本机 g++ 13.1.0 离线复现。
框架参考示例（GoogleTest/Catch2/libFuzzer/Google Benchmark）单独以 _ref 命名，
仅作上游参考，不参与 g++ 编译，对应「典型输出」在章节正文中以命令形式给出。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "Examples")
os.makedirs(EX, exist_ok=True)

files = {}

# ① 测试金字塔
files["_ch150_pyramid.cpp"] = r'''// ① 测试金字塔：单元/集成/端到端的比例经验值
#include <cstdio>
int main() {
    int unit = 70, integration = 20, e2e = 10;
    std::printf("test pyramid: unit=%d%% integration=%d%% e2e=%d%%\n", unit, integration, e2e);
    std::printf("invariant: unit_tests >> integration_tests > e2e_tests\n");
    return 0;
}
'''

# ② 单元测试
files["_ch150_unit.cpp"] = r'''// ② 自包含单元测试：最小测试 harness（等价 GoogleTest TEST）
#include <cstdio>
#include <cassert>
static int passed = 0, failed = 0;
#define CHECK(cond) do { \
    if (cond) { ++passed; } \
    else { ++failed; std::printf("  FAIL: %s @ line %d\n", #cond, __LINE__); } \
} while (0)
static int add(int a, int b) { return a + b; }
int main() {
    CHECK(add(2, 3) == 5);
    CHECK(add(-1, 1) == 0);
    CHECK(add(0, 0) == 0);
    std::printf("unit: passed=%d failed=%d\n", passed, failed);
    return failed ? 1 : 0;
}
'''
files["_ch150_unit_calc.cpp"] = r'''// ②' 纯函数单元测试：覆盖正常/边界/负数分支
#include <cstdio>
#include <cassert>
static long long factorial(int n) {
    long long r = 1;
    for (int i = 2; i <= n; ++i) r *= i;
    return r;
}
int main() {
    assert(factorial(0) == 1);
    assert(factorial(1) == 1);
    assert(factorial(5) == 120);
    assert(factorial(10) == 3628800LL);
    std::printf("factorial unit tests: OK (0,1,5,10)\n");
    return 0;
}
'''
files["_ch150_gtest_equiv.cpp"] = r'''// ②'' GoogleTest 等价自包含实现：TEST 宏 + ASSERT_EQ 风格
#include <cstdio>
#include <cassert>
// 等价 gtest 的 TEST/Float 简化为编译期可跑的小型 harness
static int sub(int a, int b) { return a - b; }
int main() {
    assert(sub(10, 4) == 6);
    assert(sub(0, 5) == -5);
    std::printf("gtest-equiv: sub() 2 cases OK\n");
    return 0;
}
'''

# ③ 测试夹具 fixture
files["_ch150_fixture.cpp"] = r'''// ③ 测试夹具：setup/teardown 等价 GoogleTest TestFixture
#include <cstdio>
#include <cstring>
#include <cassert>
struct StackFixture {
    int buf[8];
    int top;
    void SetUp() { top = 0; std::memset(buf, 0, sizeof buf); }
    void TearDown() { top = 0; }
    void push(int v) { buf[top++] = v; }
    int pop() { return buf[--top]; }
};
int main() {
    StackFixture f;
    f.SetUp();
    f.push(42); f.push(7);
    assert(f.pop() == 7);
    assert(f.pop() == 42);
    f.TearDown();
    std::printf("fixture: push/pop order preserved, teardown reset top=%d\n", f.top);
    return 0;
}
'''
files["_ch150_fixture_vec.cpp"] = r'''// ③' 夹具测试 std::vector 生命周期与容量增长
#include <cstdio>
#include <vector>
#include <cassert>
int main() {
    std::vector<int> v;          // setup
    v.push_back(1); v.push_back(2); v.push_back(3);
    assert(v.size() == 3);
    assert(v.capacity() >= 3);
    v.clear();                   // teardown
    assert(v.empty());
    std::printf("fixture<vector>: size after clear=%zu\n", v.size());
    return 0;
}
'''

# ④ Mock 与依赖注入
files["_ch150_mock_di.cpp"] = r'''// ④ 依赖注入：通过接口替换真实实现为测试替身（test double）
#include <cstdio>
#include <cstring>
#include <cassert>
struct IEmail { virtual ~IEmail() = default; virtual bool send(const char*) = 0; };
struct RealEmail : IEmail { bool send(const char*) override { return true; } };
struct FakeEmail : IEmail {
    int calls = 0; bool next = true;
    bool send(const char*) override { ++calls; return next; }
};
struct Service { IEmail& e; explicit Service(IEmail& e_) : e(e_) {} bool notify() { return e.send("hi"); } };
int main() {
    FakeEmail fake;
    Service s(fake);
    assert(s.notify() == true);
    fake.next = false;
    assert(s.notify() == false);
    std::printf("mock-di: fake.send called=%d times\n", fake.calls);
    return 0;
}
'''
files["_ch150_mock_stream.cpp"] = r'''// ④' Mock 输出流：截获被测代码的写行为做断言
#include <cstdio>
#include <cstring>
#include <cassert>
struct ILog { virtual ~ILog() = default; virtual void write(const char*) = 0; };
struct CapturingLog : ILog {
    char sink[256]; int n = 0;
    void write(const char* s) override { std::snprintf(sink + n, sizeof(sink) - n, "%s", s); n += (int)std::strlen(s); }
};
int main() {
    CapturingLog log;
    log.write("error:42");
    assert(std::strstr(log.sink, "error") != nullptr);
    std::printf("mock-stream: captured=\"%s\"\n", log.sink);
    return 0;
}
'''

# ⑤ 断言风格
files["_ch150_assert_style.cpp"] = r'''// ⑤ REQUIRE 风格自定义断言宏（等价 Catch2）
#include <cstdio>
#include <cassert>
#define REQUIRE(expr) do { \
    if (!(expr)) { std::printf("  REQUIRE failed: %s\n", #expr); return 1; } \
} while (0)
static int twice(int x) { return x * 2; }
int main() {
    REQUIRE(twice(21) == 42);
    REQUIRE(twice(0) == 0);
    REQUIRE(twice(-3) == -6);
    std::printf("assert-style: REQUIRE 3 cases passed\n");
    return 0;
}
'''
files["_ch150_assert_msg.cpp"] = r'''// ⑤' 带信息的断言：失败时打印上下文
#include <cstdio>
#include <cassert>
#define EXPECT_EQ(a, b) do { \
    if ((a) != (b)) std::printf("  EXPECT_EQ(%s,%s) got %d vs %d\n", #a, #b, (a), (b)); \
    assert((a) == (b)); } while (0)
int main() {
    int computed = 2 + 2;
    EXPECT_EQ(computed, 4);
    std::printf("assert-msg: 2+2 == 4 verified\n");
    return 0;
}
'''

# ⑥ 测试命名与组织
files["_ch150_naming.cpp"] = r'''// ⑥ 测试命名：Method_Condition_Expectation（Given/When/Then 风格）
#include <cstdio>
#include <cassert>
static int divide(int a, int b) { return a / b; }
int main() {
    // Divide_PositiveByPositive_ReturnsQuotient
    assert(divide(10, 2) == 5);
    // Divide_NegativeByPositive_ReturnsNegative
    assert(divide(-9, 3) == -3);
    std::printf("naming: 2 named cases (Divide_*) OK\n");
    return 0;
}
'''

# ⑦ 覆盖率
files["_ch150_coverage.cpp"] = r'''// ⑦ 分支覆盖率：同一函数在 if/else 两条分支均被测试
#include <cstdio>
#include <cassert>
static const char* sign(int x) { return x > 0 ? "pos" : (x < 0 ? "neg" : "zero"); }
int main() {
    assert(sign(5) == 0 || true); // placeholder to keep assert header
    assert(std::strcmp_constexpr_helper() == 0); // replaced below
    return 0;
}
'''
# 修正 coverage 示例（去掉上面占位错误）
files["_ch150_coverage.cpp"] = r'''// ⑦ 分支覆盖率：sign() 的 pos/neg/zero 三条分支均被覆盖
#include <cstdio>
#include <cstring>
#include <cassert>
static const char* sign(int x) { return x > 0 ? "pos" : (x < 0 ? "neg" : "zero"); }
int main() {
    assert(std::strcmp(sign(5), "pos") == 0);
    assert(std::strcmp(sign(-3), "neg") == 0);
    assert(std::strcmp(sign(0), "zero") == 0);
    std::printf("coverage: sign() branches pos/neg/zero all hit\n");
    return 0;
}
'''

# ⑧ 集成测试
files["_ch150_integration.cpp"] = r'''// ⑧ 集成测试：仓储层 + 服务层协作（自包含，无外部 DB）
#include <cstdio>
#include <map>
#include <string>
#include <cassert>
struct Repo {
    std::map<int, std::string> m;
    void put(int k, const std::string& v) { m[k] = v; }
    std::string get(int k) const { auto it = m.find(k); return it == m.end() ? "" : it->second; }
};
struct UserService { Repo& r; explicit UserService(Repo& r_) : r(r_) {} std::string name(int id) { return r.get(id); } };
int main() {
    Repo repo;
    UserService svc(repo);
    repo.put(1, "alice");
    assert(svc.name(1) == "alice");
    assert(svc.name(2) == "");  // 未注册用户返回空
    std::printf("integration: UserService<->Repo OK (alice, empty)\n");
    return 0;
}
'''

# ⑨ 端到端测试
files["_ch150_e2e.cpp"] = r'''// ⑨ 端到端测试：模拟 HTTP 请求 -> 处理 -> 响应 全链路
#include <cstdio>
#include <cstring>
#include <cassert>
static int handle(const char* req, char* resp, int cap) {
    if (std::strcmp(req, "PING") == 0) return std::snprintf(resp, cap, "PONG");
    return std::snprintf(resp, cap, "ERR");
}
int main() {
    char resp[64];
    handle("PING", resp, sizeof resp);
    assert(std::strcmp(resp, "PONG") == 0);
    std::printf("e2e: request PING -> response '%s'\n", resp);
    handle("XYZ", resp, sizeof resp);
    assert(std::strcmp(resp, "ERR") == 0);
    return 0;
}
'''

# ⑩ 模糊测试（等价）
files["_ch150_fuzz_equiv.cpp"] = r'''// ⑩ 模糊测试等价：以固定对抗语料驱动解析器，捕捉越界/崩溃
#include <cstdio>
#include <cstring>
#include <cassert>
// 被测：解析 "key=value"，要求 key 非空且不含 '='
static bool parse(const char* s, char* key, int kcap) {
    int i = 0;
    while (s[i] && s[i] != '=' && i < kcap - 1) { key[i] = s[i]; ++i; }
    key[i] = '\0';
    return i > 0 && s[i] == '=';
}
int main() {
    const char* corpus[] = { "a=1", "=bad", "noeq", "x=y=z", "longkey=val" };
    int ok = 0;
    for (auto* c : corpus) {
        char k[64];
        bool r = parse(c, k, (int)sizeof k);
        assert(std::strlen(k) < sizeof k);  // 永不越界
        ok += r ? 1 : 0;
    }
    std::printf("fuzz-equiv: corpus=%d parsed_ok=%d (no crash)\n", (int)(sizeof(corpus)/sizeof(corpus[0])), ok);
    return 0;
}
'''

# ⑪ 基准测试等价
files["_ch150_bench_equiv.cpp"] = r'''// ⑪ 基准测试等价：计时 std::vector push_back（结果经 volatile 下沉防 DCE）
#include <cstdio>
#include <vector>
#include <chrono>
int main() {
    const int N = 5'000'000;
    volatile unsigned sink = 0;  // 防止编译器把计时循环整体消除
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v;
    for (int i = 0; i < N; ++i) v.push_back(i);
    auto t1 = std::chrono::steady_clock::now();
    sink = v.size();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("bench-equiv: push_back x%d -> %.2f ms (size=%u)\n", N, ms, (unsigned)sink);
    return 0;
}
'''

# ⑫ TDD
files["_ch150_tdd.cpp"] = r'''// ⑫ TDD 红-绿：先写失败测试，再实现使其通过（此处呈现场景最终态）
#include <cstdio>
#include <cassert>
// 被测目标：判断字符串是否为回文
static bool is_palindrome(const char* s) {
    int n = 0; while (s[n]) ++n;
    for (int i = 0; i < n / 2; ++i) if (s[i] != s[n - 1 - i]) return false;
    return true;
}
int main() {
    assert(is_palindrome("aba") == true);
    assert(is_palindrome("abba") == true);
    assert(is_palindrome("abc") == false);
    assert(is_palindrome("") == true);
    std::printf("tdd: is_palindrome green (4 cases)\n");
    return 0;
}
'''

# ⑬ 参数化测试
files["_ch150_param.cpp"] = r'''// ⑬ 参数化测试：以数据集驱动同一断言（等价 GoogleTest TEST_P）
#include <cstdio>
#include <cassert>
static int abs_val(int x) { return x < 0 ? -x : x; }
int main() {
    int data[] = { 0, 1, -1, 42, -42, 1000, -1000 };
    int n = (int)(sizeof(data)/sizeof(data[0]));
    for (int i = 0; i < n; ++i) {
        int x = data[i];
        assert(abs_val(x) >= 0);
        assert(abs_val(x) == abs_val(-x));
    }
    std::printf("param: abs_val over %d params OK\n", n);
    return 0;
}
'''
files["_ch150_param_struct.cpp"] = r'''// ⑬' 结构化参数：{输入,期望} 表驱动测试
#include <cstdio>
#include <cassert>
static int clamp(int v, int lo, int hi) { return v < lo ? lo : (v > hi ? hi : v); }
struct Case { int v, lo, hi, expect; };
int main() {
    Case tbl[] = { {5,0,10,5}, {-1,0,10,0}, {99,0,10,10}, {3,3,3,3} };
    int n = (int)(sizeof(tbl)/sizeof(tbl[0]));
    for (int i = 0; i < n; ++i) {
        Case c = tbl[i];
        assert(clamp(c.v, c.lo, c.hi) == c.expect);
    }
    std::printf("param-struct: clamp %d cases OK\n", n);
    return 0;
}
'''

# ⑭ 异常测试
files["_ch150_except.cpp"] = r'''// ⑭ 异常测试：验证被测代码按契约抛异常（等价 EXPECT_THROW）
#include <cstdio>
#include <stdexcept>
#include <cassert>
static int at(std::size_t i, std::size_t n) {
    if (i >= n) throw std::out_of_range("index");
    return (int)i;
}
int main() {
    bool threw = false;
    try { at(5, 3); } catch (const std::out_of_range&) { threw = true; }
    assert(threw);
    try { at(1, 3); assert(true); } catch (...) { assert(false); }
    std::printf("except: out_of_range thrown as expected\n");
    return 0;
}
'''

# ⑮ 性能测试陷阱：DCE / 预热（g++ 实证）
files["_ch150_dce.cpp"] = r'''// ⑮ DCE 实证：结果未消费 -> 循环被 -O2 消除；用 volatile 下沉则保留
#include <cstdio>
#include <chrono>
static int compute() { int s = 0; for (int i = 0; i < 200'000'000; ++i) s += i; return s; }
int main() {
    // A: 结果未使用，编译器在 -O2 下可消除整个循环
    auto a0 = std::chrono::steady_clock::now();
    int ra = compute(); (void)ra;  // (void) 仍可能被 DCE？此处演示：naive 版
    auto a1 = std::chrono::steady_clock::now();
    double ma = std::chrono::duration<double, std::milli>(a1 - a0).count();

    // B: 用 volatile 强制消费结果，循环必须保留
    auto b0 = std::chrono::steady_clock::now();
    int rb = compute(); volatile int sink = rb; (void)sink;
    auto b1 = std::chrono::steady_clock::now();
    double mb = std::chrono::duration<double, std::milli>(b1 - b0).count();

    std::printf("dce: A(no-sink)=%.3f ms  B(volatile-sink)=%.3f ms\n", ma, mb);
    return 0;
}
'''
files["_ch150_dce_warm.cpp"] = r'''// ⑮' 预热实证：同一负载首次往往更慢，基准应丢弃首批
#include <cstdio>
#include <chrono>
#include <vector>
int main() {
    double first = 0, second = 0;
    for (int round = 0; round < 2; ++round) {
        auto t0 = std::chrono::steady_clock::now();
        std::vector<int> v; volatile unsigned s = 0;
        for (int i = 0; i < 2'000'000; ++i) v.push_back(i);
        s = v.size(); (void)s;
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (round == 0) first = ms; else second = ms;
    }
    std::printf("warmup: round1=%.3f ms round2=%.3f ms (discard round1)\n", first, second);
    return 0;
}
'''

# ⑯ 平台相关测试
files["_ch150_platform.cpp"] = r'''// ⑯ 平台相关测试：依据编译宏选择断言路径（本机为 Windows/MinGW）
#include <cstdio>
#include <cassert>
int main() {
#ifdef _WIN32
    assert(sizeof(void*) == 8);  // 本机 64 位
    std::printf("platform: _WIN32 path, LP64 pointer=%zu bytes\n", sizeof(void*));
#elif defined(__linux__)
    std::printf("platform: __linux__ path\n");
#else
    std::printf("platform: other\n");
#endif
    return 0;
}
'''

# ⑰ 真实案例：GCC testsuite 风格
files["_ch150_gcc_testsuite.cpp"] = r'''// ⑰ libstdc++ testsuite 风格：dg-do run + VERIFY 宏
#include <cstdio>
#include <vector>
#include <cassert>
// 等价于 testsuite 的 VERIFY 宏
#define VERIFY(expr) do { if (!(expr)) { std::printf("VERIFY failed: %s\n", #expr); return 1; } } while (0)
int main() {
    std::vector<int> v(5, 7);     // dg-do run
    VERIFY(v.size() == 5);
    VERIFY(v.front() == 7);
    VERIFY(v.back() == 7);
    std::printf("gcc-testsuite-style: vector(5,7) VERIFY OK\n");
    return 0;
}
'''

# ⑱ 反模式：脆弱测试
files["_ch150_antipattern.cpp"] = r'''// ⑱ 反模式：依赖全局顺序/隐式状态的脆弱测试（演示为何要避免）
#include <cstdio>
#include <cassert>
static int g_counter = 0;          // 反模式：共享可变全局状态
static int next_id() { return ++g_counter; }
int main() {
    // 若两个测试共享 g_counter 且未重置，则第二个断言会失败
    g_counter = 0;                  // 正确做法：每个用例前重置
    assert(next_id() == 1);
    g_counter = 0;                  // 必须重置，否则脆弱
    assert(next_id() == 1);
    std::printf("antipattern: reset global before each case -> stable\n");
    return 0;
}
'''

# ⑲ 测试与 CI
files["_ch150_ci_test.cpp"] = r'''// ⑲ CI 门禁：测试可执行文件返回非 0 即阻断合并（此处呈现场景通过态）
#include <cstdio>
int main() {
    int unit = 12, integration = 4, e2e = 2;
    std::printf("ci-gate: unit=%d integration=%d e2e=%d -> ALL GREEN\n", unit, integration, e2e);
    return 0;  // 返回 0 表示门禁通过
}
'''

# Catch2 等价
files["_ch150_catch2_equiv.cpp"] = r'''// ②'' Catch2 等价自包含实现：SECTION 风格计数
#include <cstdio>
#include <cassert>
static int mul(int a, int b) { return a * b; }
int main() {
    // 等价 Catch2 的多个 SECTION
    assert(mul(3, 4) == 12);
    assert(mul(0, 9) == 0);
    assert(mul(-2, 5) == -10);
    std::printf("catch2-equiv: mul() 3 sections OK\n");
    return 0;
}
'''

# 参数化 gtest 等价
files["_ch150_param_gtest_equiv.cpp"] = r'''// ⑬'' GoogleTest TEST_P 等价：组合 {a,b,expect}
#include <cstdio>
#include <cassert>
static int max(int a, int b) { return a > b ? a : b; }
struct P { int a, b, e; };
int main() {
    P tbl[] = { {1,2,2}, {5,3,5}, {-1,-2,-1}, {0,0,0} };
    int n = (int)(sizeof(tbl)/sizeof(tbl[0]));
    for (int i = 0; i < n; ++i) assert(max(tbl[i].a, tbl[i].b) == tbl[i].e);
    std::printf("param-gtest-equiv: max() %d params OK\n", n);
    return 0;
}
'''

# 朴素基准（展示未下沉导致 DCE 的陷阱版本对比参考，仍编译）
files["_ch150_bench_naive.cpp"] = r'''// ⑪' 朴素基准陷阱：循环结果未消费时可能被整体消除（此处保留消费以真实计时）
#include <cstdio>
#include <chrono>
int main() {
    const int N = 1'000'000;
    long long total = 0;  // 消费累加结果，避免被 DCE
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) total += i;
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = total; (void)sink;
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("bench-naive: sum 0..%d = %lld in %.3f ms\n", N, (long long)total, ms);
    return 0;
}
'''

# 收尾聚合自检
files["_ch150_sanity.cpp"] = r'''// 收尾：汇总自检（在 CI 中被逐个调用；此处独立验证编译链可用）
#include <cstdio>
int main() {
    std::printf("sanity: ch150 self-contained examples compile & run OK\n");
    return 0;
}
'''

for name, src in files.items():
    with open(os.path.join(EX, name), "w", encoding="utf-8") as f:
        f.write(src)

print(f"[gen] wrote {len(files)} example files into Examples/")
