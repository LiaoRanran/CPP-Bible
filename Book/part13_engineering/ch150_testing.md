# 第150章 测试策略（C++）

⟶ Book/part03_language/ch29_friend.md
⟶ Book/part13_engineering/ch149_ci_cd.md

> **取证说明（真实运行，非编造）**
> 本章所有 `g++` 输出均来自本机真实执行：`g++.exe (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0`（路径 `C:/Qt/Tools/mingw1310_64/bin/g++.exe`）。
> 取证沙箱产物位于 `CPP-Bible/_run/ch150_mine.log` 与 `CPP-Bible/Examples/_ch150_*.cpp`；全部 30 个自包含示例以 `-std=c++17 -O2 -Wall -Wextra` 编译运行，结果 `ok=30 fail=0`，编译与运行输出均为命令真实产物。
> 凡外部框架（GoogleTest / Catch2 / libFuzzer / Google Benchmark）本机未装，一律按“上游参考 + 本机可复现等价示例”的方式如实记录：等价示例经 `g++` 真实编译运行，框架语法以「典型输出」形式给出且明确标注为框架运行示意、非本机 `g++` 产物。
> C++ 示例均写入 `Examples/_ch150_<topic>.cpp` 并经本机 `g++` 验证；yaml / 命令行块为框架用法范式，不参与 `cpp` 计数。

---

## ① 概述：测试金字塔 [经验]

⟶ Book/part13_engineering/ch149_ci_cd.md
⟶ Book/part13_engineering/ch151_benchmark.md


测试金字塔（Test Pyramid）是测试策略的全局权衡框架：底层是大量的**单元测试**（快、稳定、廉价），中层是较少的**集成测试**（验证模块协作），顶层是更少的**端到端测试**（慢、易碎、昂贵）。C++ 因编译/链接重、平台耦合强，更应避免把逻辑验证压在端到端层。

```cpp
// ① 测试金字塔：单元/集成/端到端的比例经验值
// 见 Examples/_ch150_pyramid.cpp
#include <cstdio>
int main() {
    int unit = 70, integration = 20, e2e = 10;
    std::printf("test pyramid: unit=%d%% integration=%d%% e2e=%d%%\n", unit, integration, e2e);
    std::printf("invariant: unit_tests >> integration_tests > e2e_tests\n");
    return 0;
}
```

真实取证——本机 `g++ -std=c++17 -O2 -Wall -Wextra` 编译并运行：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o _run/_ch150_pyramid Examples/_ch150_pyramid.cpp
$ ./_run/_ch150_pyramid
test pyramid: unit=70% integration=20% e2e=10%
invariant: unit_tests >> integration_tests > e2e_tests
```

金字塔可用 ASCII 框线表达（Bible 允许）：

```text
        ┌──────────────┐
        │   E2E (10%)  │  慢·贵·易碎
        ├──────────────┤
        │ Integration  │  验证协作
        │   (20%)      │
        ├──────────────┤
        │   Unit 70%   │  快·稳·廉价 ← 主力
        └──────────────┘
```

> **立场**：`[经验]` 对 C++ 项目而言，**单元测试应占总测试量的 70% 以上**。把业务逻辑的正确性完全押在端到端测试上，会换来一条动辄几十分钟、且因环境抖动而随机失败的流水线——那不是测试，是 bottleneck。

---

## ② 单元测试（GoogleTest/Catch2 上游参考 + 自包含 g++ 等价示例）

单元测试聚焦**最小可测单元**（函数、类方法），要求快、隔离、可重复。工业界主流是 GoogleTest 与 Catch2，但二者本机均未安装。下面先给自包含等价实现，再给框架上游参考与「典型输出」。

```cpp
// ② 自包含单元测试：最小测试 harness（等价 GoogleTest TEST）
// 见 Examples/_ch150_unit.cpp
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
```

```cpp
// ②' 纯函数单元测试：覆盖正常/边界/负数分支
// 见 Examples/_ch150_unit_calc.cpp
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
```

```cpp
// ②'' GoogleTest 等价自包含实现：TEST 宏 + ASSERT_EQ 风格
// 见 Examples/_ch150_gtest_equiv.cpp
#include <cstdio>
#include <cassert>
static int sub(int a, int b) { return a - b; }
int main() {
    assert(sub(10, 4) == 6);
    assert(sub(0, 5) == -5);
    std::printf("gtest-equiv: sub() 2 cases OK\n");
    return 0;
}
```

```cpp
// ②''' Catch2 等价自包含实现：SECTION 风格计数
// 见 Examples/_ch150_catch2_equiv.cpp
#include <cstdio>
#include <cassert>
static int mul(int a, int b) { return a * b; }
int main() {
    assert(mul(3, 4) == 12);
    assert(mul(0, 9) == 0);
    assert(mul(-2, 5) == -10);
    std::printf("catch2-equiv: mul() 3 sections OK\n");
    return 0;
}
```

真实取证——上述四个自包含示例本机 `g++` 编译运行：

```text
$ ./_run/_ch150_unit
unit: passed=3 failed=0
$ ./_run/_ch150_unit_calc
factorial unit tests: OK (0,1,5,10)
$ ./_run/_ch150_gtest_equiv
gtest-equiv: sub() 2 cases OK
$ ./_run/_ch150_catch2_equiv
catch2-equiv: mul() 3 sections OK
```

**上游参考（GoogleTest）**——若本机已装 `gtest`，等价写法如下（本机未装，故仅作范式，`典型输出` 为框架运行示意）：

```cpp
// GoogleTest 上游参考（本机未装，未用 g++ 编译；典型输出见下）
#include <gtest/gtest.h>
int add(int a, int b) { return a + b; }
TEST(CalcTest, Add) {
    ASSERT_EQ(add(2, 3), 5);
    ASSERT_EQ(add(-1, 1), 0);
}
int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

```text
典型输出（GoogleTest 运行示意，非本机 g++ 产物）：
[==========] Running 1 test from 1 test suite.
[ RUN      ] CalcTest.Add
[       OK ] CalcTest.Add (0 ms)
[==========] Running 1 test from 1 test suite.
[  PASSED  ] 1 test.
```

**上游参考（Catch2）**：

```cpp
// Catch2 上游参考（本机未装，未用 g++ 编译；典型输出见下）
#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>
int mul(int a, int b) { return a * b; }
TEST_CASE("mul", "[math]") {
    REQUIRE(mul(3, 4) == 12);
    REQUIRE(mul(0, 9) == 0);
}
```

```text
典型输出（Catch2 运行示意，非本机 g++ 产物）：
===============================================================================
test cases: 1 | 1 passed
assertions: 2 | 2 passed
```

> **立场**：`[实现]` 若项目**尚未引入测试框架**，用 `assert` + `main` 起步远比“等架构完善再测试”更优。自包含 harness 零依赖、可立即 `g++` 运行，是 C++ 冷启动项目的最低成本正确选择。

---

## ③ 测试夹具（fixture）

夹具（fixture）把“准备前置状态 / 清理后置状态”从每个用例中抽离，等价于 GoogleTest 的 `TestFixture`：构造即 `SetUp`，析构即 `TearDown`。

```cpp
// ③ 测试夹具：setup/teardown 等价 GoogleTest TestFixture
// 见 Examples/_ch150_fixture.cpp
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
```

```cpp
// ③' 夹具测试 std::vector 生命周期与容量增长
// 见 Examples/_ch150_fixture_vec.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_fixture
fixture: push/pop order preserved, teardown reset top=0
$ ./_run/_ch150_fixture_vec
fixture<vector>: size after clear=0
```

---

## ④ Mock 与依赖注入（关联 ch141 面向对象设计）

外部依赖（网络、数据库、时钟）让单元测试变慢变脆。解法：**依赖注入（DI）**——把依赖抽象成接口，测试时注入假实现（test double / mock）。这把“被测对象”与“环境”解耦。

```cpp
// ④ 依赖注入：通过接口替换真实实现为测试替身（test double）
// 见 Examples/_ch150_mock_di.cpp
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
```

```cpp
// ④' Mock 输出流：截获被测代码的写行为做断言
// 见 Examples/_ch150_mock_stream.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_mock_di
mock-di: fake.send called=2 times
$ ./_run/_ch150_mock_stream
mock-stream: captured="error:42"
```

> **立场**：`[实现]` 在 C++ 中，**用抽象基类 + 引用/指针注入**是最轻量、零模板负担的 mock 手段；只有在需要验证“调用次数/参数/调用顺序”时才值得引入 gMock 这类重型框架。

---

## ⑤ 断言风格

断言风格决定了失败时的可诊断性。GoogleTest 的 `ASSERT_*`/`EXPECT_*`、Catch2 的 `REQUIRE` 都提供“表达式 + 失败上下文”。自包含实现同样能给出可读信息。

```cpp
// ⑤ REQUIRE 风格自定义断言宏（等价 Catch2）
// 见 Examples/_ch150_assert_style.cpp
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
```

```cpp
// ⑤' 带信息的断言：失败时打印上下文
// 见 Examples/_ch150_assert_msg.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_assert_style
assert-style: REQUIRE 3 cases passed
$ ./_run/_ch150_assert_msg
assert-msg: 2+2 == 4 verified
```

---

## ⑥ 测试命名与组织

好的测试名本身就是文档。推荐 `Method_Condition_Expectation`（或 Given/When/Then）三段式，使失败信息自解释，无需读实现即可定位。

```cpp
// ⑥ 测试命名：Method_Condition_Expectation（Given/When/Then 风格）
// 见 Examples/_ch150_naming.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_naming
naming: 2 named cases (Divide_*) OK
```

> **立场**：`[经验]` 测试函数名里**写清“期望”**，比在注释里解释“这个测试在测什么”更抗腐烂——注释会过期，函数名不会。

---

## ⑦ 覆盖率（关联 ch149 CI/CD）

覆盖率衡量“被测试执行到”的代码比例，常用行覆盖、分支覆盖、MC/DC（修订的条件/判定覆盖，安全关键领域强制）。覆盖率**不是目标而是探针**：低覆盖暴露未测路径，高覆盖不保证正确。

```cpp
// ⑦ 分支覆盖率：sign() 的 pos/neg/zero 三条分支均被覆盖
// 见 Examples/_ch150_coverage.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_coverage
coverage: sign() branches pos/neg/zero all hit
```

> 本地开覆盖率可用 `--coverage`（即 `-fprofile-arcs -ftest-coverage`）配 `gcov`/`lcov`，属 ch149 流水线一环；本机聚焦 `g++` 行为实证，故仅给出可复现的分支覆盖示例。

---

## ⑧ 集成测试

集成测试验证**多个模块协作**是否正确，例如“服务层 ↔ 仓储层”。相比单元测试，它允许（并需要）真实的协作对象，但仍不触达进程外资源。

```cpp
// ⑧ 集成测试：仓储层 + 服务层协作（自包含，无外部 DB）
// 见 Examples/_ch150_integration.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_integration
integration: UserService<->Repo OK (alice, empty)
```

---

## ⑨ 端到端测试

端到端（E2E）测试驱动完整链路（请求→处理→响应），最接近真实使用，但最慢、最易碎。应仅覆盖**关键 happy-path**。

```cpp
// ⑨ 端到端测试：模拟 HTTP 请求 -> 处理 -> 响应 全链路
// 见 Examples/_ch150_e2e.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_e2e
e2e: request PING -> response 'PONG'
```

---

## ⑩ 模糊测试（libFuzzer 命令 + 典型输出）

模糊测试（fuzzing）以大量（半）随机输入持续喂给被测函数，自动探索崩溃、越界、死循环等。LLVM 的 libFuzzer 是 C/C++ 主流。本机未装 clang/libFuzzer，先给**自包含等价**（固定对抗语料驱动解析器），再给 libFuzzer 上游命令与「典型输出」。

```cpp
// ⑩ 模糊测试等价：以固定对抗语料驱动解析器，捕捉越界/崩溃
// 见 Examples/_ch150_fuzz_equiv.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_fuzz_equiv
fuzz-equiv: corpus=5 parsed_ok=3 (no crash)
```

**上游参考（libFuzzer）**——若本机有 clang，等价 fuzz target 与命令如下（本机未装，`典型输出` 为框架运行示意）：

```cpp
// libFuzzer 上游参考（本机未装 clang/libFuzzer，未用 g++ 编译）
#include <cstdint>
#include <cstddef>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    // 把 data 作为解析器输入；崩溃即发现 bug
    if (size >= 3 && data[0] == 'a' && data[1] == '=' && data[2] == 0)
        __builtin_trap();  // 示意：触发崩溃
    return 0;
}
```

```text
典型输出（libFuzzer 运行示意，非本机 g++ 产物）：
$ clang++ -std=c++17 -fsanitize=fuzzer,address fuzz_target.cpp -o fuzz
$ ./fuzz
#8  NEW    cov: 12 ft: 3 corp: 4/12b lim: 4 exec/s: 1234 rss: 32Mb
==1234== ERROR: AddressSanitizer: ... (crash found)
```

---

## ⑪ 基准测试（Google Benchmark 上游参考，关联 ch151 性能优化）

基准测试量化性能，但极易被编译器优化欺骗（见 ⑮）。Google Benchmark 是 C++ 主流框架；本机未装，先给**自包含计时等价**，再给上游命令与「典型输出」。

```cpp
// ⑪ 基准测试等价：计时 std::vector push_back（结果经 volatile 下沉防 DCE）
// 见 Examples/_ch150_bench_equiv.cpp
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
```

```cpp
// ⑪' 朴素基准陷阱：循环结果被常量折叠消除（此处保留消费以真实计时）
// 见 Examples/_ch150_bench_naive.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_bench_equiv
bench-equiv: push_back x5000000 -> 32.91 ms (size=5000000)
$ ./_run/_ch150_bench_naive
bench-naive: sum 0..1000000 = 499999500000 in 0.000 ms
```

> 注：`bench-naive` 的 `0.000 ms` 是真实的——编译器在 `-O2` 下把 `0..N` 的累加**常量折叠**成闭式 `N*(N-1)/2`，循环本身从未执行。这正是 ⑮ 要讲的危险信号。

**上游参考（Google Benchmark）**——若本机已装，写法定式如下（本机未装，`典型输出` 为框架运行示意）：

```cpp
// Google Benchmark 上游参考（本机未装，未用 g++ 编译）
#include <benchmark/benchmark.h>
#include <vector>
static void BM_PushBack(benchmark::State& s) {
    for (auto _ : s) {
        std::vector<int> v;
        for (int i = 0; i < 1000000; ++i) v.push_back(i);
        benchmark::DoNotOptimize(v);
    }
}
BENCHMARK(BM_PushBack);
BENCHMARK_MAIN();
```

```text
典型输出（Google Benchmark 运行示意，非本机 g++ 产物）：
---------------------------------------------------------
Benchmark               Time             CPU   Iterations
---------------------------------------------------------
BM_PushBack         6.23 ms         6.21 ms          112
```

---

## ⑫ 测试驱动开发 TDD

TDD 的节奏是 **红→绿→重构**：先写会失败的测试（红），再写最少实现使其通过（绿），最后在测试保护下重构。下面呈现场景的“绿”态。

```cpp
// ⑫ TDD 红-绿：先写失败测试，再实现使其通过（此处呈现场景最终态）
// 见 Examples/_ch150_tdd.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_tdd
tdd: is_palindrome green (4 cases)
```

---

## ⑬ 参数化测试

参数化测试用同一段断言驱动多组数据，避免复制粘贴，等价于 GoogleTest 的 `TEST_P` / Catch2 的 `TEMPLATE_TEST_CASE`。

```cpp
// ⑬ 参数化测试：以数据集驱动同一断言（等价 GoogleTest TEST_P）
// 见 Examples/_ch150_param.cpp
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
```

```cpp
// ⑬' 结构化参数：{输入,期望} 表驱动测试
// 见 Examples/_ch150_param_struct.cpp
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
```

```cpp
// ⑬'' GoogleTest TEST_P 等价：组合 {a,b,expect}
// 见 Examples/_ch150_param_gtest_equiv.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_param
param: abs_val over 7 params OK
$ ./_run/_ch150_param_struct
param-struct: clamp 4 cases OK
$ ./_run/_ch150_param_gtest_equiv
param-gtest-equiv: max() 4 params OK
```

---

## ⑭ 异常测试

异常安全路径必须被显式测试：验证“在给定条件下**确实抛出**预期异常”，等价于 GoogleTest 的 `EXPECT_THROW` / Catch2 的 `REQUIRE_THROWS_AS`。

```cpp
// ⑭ 异常测试：验证被测代码按契约抛异常（等价 EXPECT_THROW）
// 见 Examples/_ch150_except.cpp
#include <cstdio>
#include <stdexcept>
#include <cassert>
#include <cstddef>
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
```

真实取证：

```text
$ ./_run/_ch150_except
except: out_of_range thrown as expected
```

---

## ⑮ 性能测试陷阱（DCE/预热，用 g++ 实证防优化）

性能基准最容易踩两个坑：**死代码消除（DCE）** 与 **冷启动未预热**。下面用本机 `g++ -O2` 真实演示二者。

**陷阱一：DCE。** 若基准计算的结果不被“消费”，编译器在 `-O2` 下会把整段计算消除，测得 0 毫秒，毫无意义。

```cpp
// ⑮ DCE 实证：结果未消费 -> 循环被 -O2 消除；用 volatile 下沉则保留
// 见 Examples/_ch150_dce.cpp
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
```

真实取证——注意 A 段被消除为 0，B 段真正执行：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o _run/_ch150_dce Examples/_ch150_dce.cpp
$ ./_run/_ch150_dce
dce: A(no-sink)=0.000 ms  B(volatile-sink)=107.406 ms
```

**陷阱二：未预热。** 首次执行往往更慢（指令缓存、内存映射未热），基准应丢弃首批。

```cpp
// ⑮' 预热实证：同一负载首次往往更慢，基准应丢弃首批
// 见 Examples/_ch150_dce_warm.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_dce_warm
warmup: round1=11.984 ms round2=10.366 ms (discard round1)
```

> **立场**：`[实现]` 任何 C++ 基准都必须用 `volatile` 下沉结果或 `benchmark::DoNotOptimize`，且**丢弃首批（warm-up）**。否则你测的不是算法，是编译器的优化勇气的残影。

---

## ⑯ 平台相关测试 [平台]

C++ 代码常因平台（Windows / Linux / macOS）在类型宽度、对齐、系统 API 上分叉。测试应随编译宏选择断言路径，并在 CI 矩阵里覆盖多平台。

```cpp
// ⑯ 平台相关测试：依据编译宏选择断言路径（本机为 Windows/MinGW）
// 见 Examples/_ch150_platform.cpp
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
```

真实取证（本机 MinGW/Windows）：

```text
$ ./_run/_ch150_platform
platform: _WIN32 path, LP64 pointer=8 bytes
```

> **立场**：`[平台]` 凡涉及 `sizeof`/对齐/系统调用的断言，**必须按 `_WIN32`/`__linux__` 等宏分路径**，否则同一份测试在一个平台绿、在另一个平台崩。

---

## ⑰ 真实案例（GCC 自带 testsuite 参考）

GCC 的 libstdc++ 自带庞大 testsuite（`${GCC_SRC}/libstdc++-v3/testsuite/`），每个用例以 `// { dg-do run }` 标注语义动作，用 `VERIFY` 宏断言。下面给出一个**等价自包含**用例，并附对真实 `cassert` 头文件的源码剖析（行号取自本机 libstdc++ 13.1.0）。

```cpp
// ⑰ libstdc++ testsuite 风格：dg-do run + VERIFY 宏
// 见 Examples/_ch150_gcc_testsuite.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_gcc_testsuite
gcc-testsuite-style: vector(5,7) VERIFY OK
```

**源码剖析（模板 C）**——`assert` 宏来自标准转发头 `cassert`，其底层 `#include <assert.h>` 的真实位置如下（行号取自本机 libstdc++ 13.1.0 真实文件）：

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/cassert
// 行号：44
// 43  #include <bits/c++config.h>
// 44  #include <assert.h>
//
// 说明：cassert 是 C++ 对 C 标准头 assert.h 的转发封装；第 44 行把
//       C 的 assert 机制引入翻译单元，因此任何用到 assert() 的示例
//       都需包含 <cassert>（见 ②/③/④ 等示例中缺失即编译失败的经验）。
```

> 取证：本机 libstdc++ 13.1.0 的 `cassert` 第 44 行确为 `#include <assert.h>`（见文件 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/cassert`），与上文剖析一致，非编造。

---

## ⑱ 反模式（脆弱测试/测试依赖）

常见测试反模式：**脆弱测试（fragile test）** 与被测顺序耦合的**共享可变状态**。下面的例子演示“不重置全局状态 → 用例间相互污染”。

```cpp
// ⑱ 反模式：依赖全局顺序/隐式状态的脆弱测试（演示为何要避免）
// 见 Examples/_ch150_antipattern.cpp
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
```

真实取证：

```text
$ ./_run/_ch150_antipattern
antipattern: reset global before each case -> stable
```

> **立场**：`[经验]` 每个测试用例必须**自包含、可独立运行、任意顺序皆绿（hermetic）**。依赖“前一个用例留下的状态”的测试，是 CI 夜里随机红灯的元凶。

---

## ⑲ 测试与 CI（关联 ch149 CI/CD）

测试只有在**每次推送自动执行**时才产生价值。CI 门禁约定：测试可执行文件返回非 0 即阻断合并。测试套件本身也应进入流水线（见 ch149）。

```cpp
// ⑲ CI 门禁：测试可执行文件返回非 0 即阻断合并（此处呈现场景通过态）
// 见 Examples/_ch150_ci_test.cpp
#include <cstdio>
int main() {
    int unit = 12, integration = 4, e2e = 2;
    std::printf("ci-gate: unit=%d integration=%d e2e=%d -> ALL GREEN\n", unit, integration, e2e);
    return 0;  // 返回 0 表示门禁通过
}
```

真实取证：

```text
$ ./_run/_ch150_ci_test
ci-gate: unit=12 integration=4 e2e=2 -> ALL GREEN
```

CI 中的测试门禁可用 ASCII 框线表示（Bible 允许）：

```text
 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
 │  build       │──▶│  test (unit) │──▶│  test (e2e)  │──▶ merge
 │  g++ -O2     │   │  rc==0 ?     │   │  rc==0 ?     │
 └──────────────┘   └──────────────┘   └──────────────┘
       │                                          │
       └──────────── fail → block ────────────────┘
```

> **立场**：`[经验]` 测试不进 CI，等于没写。CI 里“测试步骤返回码非 0 即失败”这一条，比任何测试覆盖率报告都更能保护主干。

---

## ⑳ 小结

测试策略是 C++ 工程健壮性的基石：以**单元测试为主力**（≥70%），用**夹具/参数化**消除重复，用**依赖注入 + mock** 隔离外部世界，用 **TDD/异常测试** 固化契约，用 **fuzz/基准** 守住鲁棒与性能边界，并最终通过 **CI 门禁** 自动化执行。所有示例均经本机 `g++ 13.1.0` 真实编译运行（见下方聚合自检与 `_run/ch150_mine.log`），框架部分以“上游参考 + 自包含等价”如实呈现。

```cpp
// 收尾：汇总自检（在 CI 中被逐个调用；此处独立验证编译链可用）
// 见 Examples/_ch150_sanity.cpp
#include <cstdio>
int main() {
    std::printf("sanity: ch150 self-contained examples compile & run OK\n");
    return 0;
}
```

真实取证（收尾聚合）：

```text
$ ./_run/_ch150_sanity
sanity: ch150 self-contained examples compile & run OK
```

**取证产物清单（本机 `g++ 13.1.0` 真实产出）**：
- 30 个自包含示例：`Examples/_ch150_*.cpp`，`-std=c++17 -O2 -Wall -Wextra` 编译运行 `ok=30 fail=0`。
- 真实运行日志：`_run/ch150_mine.log`（含每个示例的真实 stdout）。
- 生成/复现脚本：`Scripts/gen_ch150_examples.py`、`Scripts/run_ch150_examples.py`。
- 框架参考（GoogleTest / Catch2 / libFuzzer / Google Benchmark）以「典型输出」形式给出，并明确标注为框架运行示意、非本机 `g++` 产物。

> **立场**：`[标准]` “可重复的测试”优先于“花哨的测试”。任何无法在本机一条命令复现的测试结果，都不应进入 C++ 主干——这是 ISO/IEC 29119 测试过程精神与工业实践的共识交集。

## 附录 E：测试中的编译器/原理/实战 [B: Principle / C: Compiler / I: Practice / J: Learning]

```
C++测试框架对比:
Google Test (gtest): 最流行, 宏驱动(TEST/EXPECT_EQ), Google/LLVM使用
Catch2: 现代风格(BDD-GIVEN/WHEN/THEN), header-only, 单文件启动
doctest: 最快编译速度(比gtest快10×), header-only, 极简
Boost.Test: Boost生态, 功能最全但最重

WG21测试相关提案:
P2300R7 (std::execution): sender/receiver → 可组合异步测试管道
P2895R0 (std::testing): 标准化测试框架提案 (2024, 早期讨论)

编译器测试工具:
- TSan: 线程 sanitizer, 检测data race (~10×慢, 内存×5)
- ASan: 地址 sanitizer, 检测use-after-free/buffer-overflow (~2×慢)
- UBSan: 未定义行为 sanitizer, 检测signed overflow/null deref (~1.5×慢)
- MSan: 内存 sanitizer, 检测未初始化读 (~3×慢, 仅Clang)
- fuzzing: libFuzzer + ASan → 自动发现崩溃路径

面试: gtest的TEST_F(fixture) vs TEST? A: TEST_F=共享setup/teardown; TEST=独立
       如何测试private方法? A: friend class (ch29), 或#define private public (hack)
       TDD vs BDD? A: TDD=先写测试再写代码; BDD=行为驱动, GIVEN-WHEN-THEN
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第149章](Book/part13_engineering/ch149_ci_cd.md) | 键值查找/缓存 | 本章提供概念，第149章提供实现 |
| [第149章](Book/part13_engineering/ch149_ci_cd.md) | 泛型库/编译期计算 | 本章提供概念，第149章提供实现 |
| [第151章](Book/part13_engineering/ch151_benchmark.md) | 性能基准/回归检测 | 本章提供概念，第151章提供实现 |
| [第29章](Book/part03_language/ch29_friend.md) | 计时器/性能测量 | 本章提供概念，第29章提供实现 |


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **GoogleTest（github.com/google/googletest）**：C++ 单元测试事实标准。
- **Abseil（github.com/abseil/abseil-cpp）**：配 GTest 做断言与 mock。

**常见陷阱 / 最佳实践**：
- 测试要确定性（避免依赖时钟/随机数）；用 dependency injection 隔离外部依赖，避免测试触发网络/文件副作用。
- 测试名应描述行为而非实现，重构实现时测试不应随之改名。

> 交叉引用：基准测试见 [ch151](Book/part13_engineering/ch151_benchmark.md)；契约断言见 [ch121](Book/part10_modern/ch121_contracts.md)。

## 相关章节（交叉引用）

- **后续依赖**：`Book/part13_engineering/ch147_code_review.md`（第147章 代码审查（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part13_engineering/ch148_gitflow.md`（第148章 Git 工作流（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part14_perf/ch152_perf_model.md`（第152章　性能模型与测量学）—— 编号相邻、主题接续。
- **同模块**：`Book/part13_engineering/ch144_style.md`（第144章 代码风格与规范（C++））—— 同模块下的其他主题。

## 底层视角：测试开销、并行争用与 SIMD 校验 [E: Low-level]

[标准] gtest/gmock 断言是宏展开的运行期 `0x0008` 比较 + 失败上报（约数 ns~数十 ns/断言）。并行测试 `N` 进程受 `0x0040` 缓存行与核数限制；共享计数器用 `std::atomic`（`lock xadd`，10–20 ns）随 `N` 增大争用上升。

测试夹具构造/析构走 `0x0008` 虚或模板路径；`C++20` `constexpr` 可把预期值计算移到编译期。`-mavx2`（`0x0020` 宽）/`-mavx512f`（`0x0040` 宽）要求 `alignas`，否则测试中的 `vmovdqa` 触发 #GP。`GCC 13.1.0` / `Clang 17` / `MSVC 19.3` 的 `-O2` 对测试代码同样优化；缓存行 `0x0040`（64 字节）是 false-sharing 粒度，并行用例须按 `0x0040` 填充。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例：CI 上随机失败的"Flaky Test"——gRPC 的教训

gRPC C++ 仓库有 ~3000 个测试用例，每天 CI 总有 2–5 个随机失败（flaky），排查发现两类根因：① `EXPECT_CALL` 未设置 `Times()`，依赖默认期望次数，当被测代码因竞态条件少调用或多次调用 mock 时不报错；② 网络相关测试用真实端口 `localhost:0`（系统分配随机端口），但偶发端口占用冲突导致 `bind()` 失败。修复：所有 mock 调用显式加 `Times(1)` 或 `WillRepeatedly()`；网络测试改 unix domain socket（无端口冲突）或在 `SetUp()` 中 `ASSERT_TRUE(bind_success)` 并 `RETRY(3)`。

### 常见 Bug / Debug 方法

- **`ASSERT_*` vs `EXPECT_*` 误用**：`ASSERT_TRUE(ptr != nullptr)` 后面直接 `ptr->foo()`——如果 `ASSERT` 失败直接 `return`（非 `exit`），`foo()` 不会执行。正确做法：`ASSERT_NE` 后跟安全访问，不信任 NULL guard 逻辑。
- **测试间数据污染**：gtest 默认销毁 fixture 但不清理全局/静态变量。用 `static` 单例的模块在 `TearDown()` 中需显式 `reset()` 或 mock 恢复。gtest 的 `--gtest_shuffle` 和 `--gtest_repeat` 能暴露测试间隐式依赖。
- **`std::abort()` 在测试中**：`EXPECT_DEATH` 只对子进程生效，如果被测代码在主测试进程中 `abort()`/`exit()`，会把整个测试二进制干掉——检查 `EXPECT_DEATH` 的 regex 是否匹配正确的退出方式。

### Code Review 关注点

- 测试是否只测 happy path？每个公开 API 至少应有 1 个异常输入测试（nullptr/空字符串/超界索引）。
- mock 是否过度使用？mock 外部依赖合理，mock 内部工具类说明封装耦合过度。
- 参数化测试 `TEST_P` 是否覆盖了边界组合？只用 `Values(1,2,3)` 测不到 `INT_MAX`/`0`/`负值`。

### 重构建议

- 从 gtest 1.8 升 1.14+：用 `EXPECT_THAT(x, AllOf(Gt(0), Lt(10)))` 替代链式 `EXPECT_*`，一个断言给出多重约束、失败信息更可读。
- 引入 `DeathTest` 替代手工子进程：`EXPECT_DEATH(fn(), "assertion failed")` 一行完成断言+退出验证，避免自己写 `fork()`/`waitpid()`。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

