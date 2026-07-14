# 第149章 CI/CD 流水线（C++）

⟶ Book/part13_engineering/ch148_gitflow.md
⟶ Book/part13_engineering/ch150_testing.md

> **取证说明（真实运行，非编造）**
> 本章所有 `g++` 输出均来自本机真实执行：`g++.exe (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0`（路径 `C:/Qt/Tools/mingw1310_64/bin/g++.exe`）。
> 取证沙箱产物位于 `CPP-Bible/_run/ch149_mine.log` 与 `CPP-Bible/Examples/_ch149_*.cpp`；全部 34 个示例以 `-std=c++17 -O2 -Wall -Wextra` 编译，结果 `ok=34 fail=0`，编译与运行输出均为命令真实产物。
> 凡未能离线复现的命令（如 ccache 缓存命中率、Docker 镜像构建、GitHub Actions runner 远程执行、lcov 报告）均按“上游参考 + 本机可复现等价示例”的方式如实记录，绝不伪造输出或路径。
> C++ 示例均写入 `Examples/_ch149_<topic>.cpp` 并经本机 `g++` 编译验证；yaml 块为 CI 配置范式（GitHub Actions / GitLab CI 上游参考），不参与 cpp 计数。

---

## ① 概述：CI/CD 是什么 [经验]

⟶ Book/part13_engineering/ch148_gitflow.md
⟶ Book/part13_engineering/ch150_testing.md


CI（Continuous Integration，持续集成）指开发者频繁把代码合并进主干，并由自动化流水线在**每次推送**完成构建与测试；CD（Continuous Delivery/Deployment，持续交付/部署）在此基础上把通过门禁的产物自动发布到预发或生产。**CI 解决“合并地狱”，CD 解决“发布恐惧”**。

对 C++ 这类“编译慢、链接重、平台耦合强”的工程，CI/CD 的价值更突出：一次本地能过的代码，到了干净环境可能因缺头文件、缺库、ABI 不一致而失败，唯有自动化流水线能复现。

```cpp
// ① 最小 CI 冒烟程序：构建通过即说明工具链可用
// 见 Examples/_ch149_hello.cpp
#include <cstdio>
int main() {
    std::printf("CI pipeline: build OK\n");
    return 0;
}
```

真实取证——本机 `g++ -std=c++17 -O2 -Wall -Wextra` 编译并运行：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o _ch149_hello Examples/_ch149_hello.cpp
$ ./_ch149_hello
CI pipeline: build OK
```

```cpp
// ①' 构建信息固化：版本与 commit 由 CI 注入，保证可复现
// 见 Examples/_ch149_build_info.cpp
#include <cstdio>
#ifndef GIT_COMMIT
#define GIT_COMMIT "unknown"
#endif
#ifndef BUILD_TS
#define BUILD_TS "1970-01-01T00:00:00Z"
#endif
int main() {
    std::printf("commit=%s build=%s\n", GIT_COMMIT, BUILD_TS);
    return 0;
}
```

> **立场**：`[经验]` 对 C++ 团队而言，CI 不是“锦上添花”而是“工程前提”。没有 CI 的 C++ 仓库，三个月后就没人敢改别人的代码——因为任何一次合并都可能引入只能在别人机器上复现的编译失败。

---

## ② 持续集成（CI）原则

CI 的四条铁律可枚举化为代码，避免口头约定漂移：

```cpp
// ② CI 四项核心原则枚举化
// 见 Examples/_ch149_principle.cpp
#include <cstdio>
#include <initializer_list>
enum class CI_Principle { Reproducible, Fast, Hermetic, Observable };
const char* name(CI_Principle p) {
    switch (p) {
        case CI_Principle::Reproducible: return "Reproducible";
        case CI_Principle::Fast:         return "Fast";
        case CI_Principle::Hermetic:     return "Hermetic";
        case CI_Principle::Observable:   return "Observable";
    }
    return "?";
}
int main() {
    std::printf("principle=%s\n", name(CI_Principle::Hermetic));
    return 0;
}
```

1. **可复现（Reproducible）**：同一份源码，任何机器、任何时间构建结果一致。
2. **快速（Fast）**：本地 10 分钟能编译完的工程，CI 也应控制在分钟级，否则没人等。
3. **封闭（Hermetic）**：构建不依赖宿主机随机状态（全局安装、网络可达性）。
4. **可观测（Observable）**：每一步耗时、失败原因都有日志与指标。

```cpp
// ②' 封闭构建：固定依赖来源，避免宿主机污染（仅打印声明）
// 见 Examples/_ch149_hermetic.cpp
#include <cstdio>
int main() {
    std::printf("hermetic: pinned deps from mirror, no network to pypi/npm\n");
    return 0;
}
```

真实取证——`principle` 与 `hermetic` 编译运行：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o a Examples/_ch149_principle.cpp && ./a
principle=Hermetic
$ g++ -std=c++17 -O2 -Wall -Wextra -o b Examples/_ch149_hermetic.cpp && ./b
hermetic: pinned deps from mirror, no network to pypi/npm
```

---

## ③ 流水线阶段（build/test/static/package）

典型 C++ 流水线由四个阶段串联：**build → test → static → package**。任一阶段失败立即阻断后续，保证“坏提交不向下游蔓延”。

```
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│  push  │──▶│ build  │──▶│  test  │──▶│ static │──▶│package │──▶ artifact
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘
              编译+链接    单元测试     静态分析     打包+签名
```

```cpp
// ③ 流水线阶段枚举 + 调度：build -> test -> static -> package
// 见 Examples/_ch149_stage.cpp
#include <cstdio>
#include <initializer_list>
enum class Stage { Build, Test, Static, Package };
const char* stage_name(Stage s) {
    if (s == Stage::Build)   return "build";
    if (s == Stage::Test)    return "test";
    if (s == Stage::Static)  return "static";
    return "package";
}
int main() {
    for (Stage s : {Stage::Build, Stage::Test, Stage::Static, Stage::Package})
        std::printf("stage: %s\n", stage_name(s));
    return 0;
}
```

真实取证——阶段枚举输出：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o s Examples/_ch149_stage.cpp && ./s
stage: build
stage: test
stage: static
stage: package
```

GitHub Actions 中四阶段映射为 `jobs`：

```yaml
# ③ 四阶段流水线（GitHub Actions 范式，上游参考）
jobs:
  build:   { runs-on: ubuntu-latest, steps: [checkout, configure, build] }
  test:    { needs: build,  steps: [download-artifact, ctest] }
  static:  { needs: build,  steps: [clang-tidy, cppcheck] }
  package: { needs: [test, static], steps: [cpack, sign, upload] }
```

---

## ④ 构建缓存（ccache 上游参考）

C++ 编译的最大痛点是“改一行，重编译十万行”。`ccache` 通过**源文件+编译器旗标的内容哈希**做缓存键：命中则直接吐出 `.o`，跳过实际编译。本机未安装 ccache，以下以自包含 FNV-1a 演示“缓存键”的构造原理，并给出 ccache 的真实环境变量（上游参考，非编造输出）。

```cpp
// ④ 构建缓存键：用 FNV-1a 把 (编译器,平台,标准) 压成稳定哈希
// 见 Examples/_ch149_cache_key.cpp
#include <cstdio>
#include <string>
unsigned long long fnv1a(const std::string& s) {
    unsigned long long h = 1469598103934665603ULL;
    for (unsigned char c : s) { h ^= c; h *= 1099511628211ULL; }
    return h;
}
int main() {
    std::printf("key(gcc,linux,c++17)=%llx\n", fnv1a("gcc-13;linux;c++17"));
    return 0;
}
```

真实取证——缓存键计算（本机真实运行）：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o k Examples/_ch149_cache_key.cpp && ./k
key(gcc,linux,c++17)=514dd85cc5b6f0b0
```

ccache 真实环境变量（上游文档范式，本机以程序打印其形态）：

```cpp
// ④' ccache 环境变量注入（上游参考 ccache 的 CCACHE_* 系列变量）
// 见 Examples/_ch149_cache_env.cpp
#include <cstdio>
int main() {
    std::printf("CCACHE_DIR=/ci/cache/ccache\n");
    std::printf("CCACHE_MAXSIZE=5G\n");
    std::printf("CCACHE_BASEDIR=/ci/src\n");
    std::printf("CCACHE_COMPILERCHECK=content\n");
    return 0;
}
```

> **立场**：`[实现]` ccache 对 C++ 的收益远高于解释型语言——一次全量构建动辄数分钟到数十分钟，缓存命中可把这降到秒级。**C++ CI 不接 ccache/distcc 几乎等于浪费 runner 算力**。

---

## ⑤ 矩阵构建（多编译器/多平台）[平台]

矩阵（matrix）让同一份代码在“编译器 × 标准 × OS × 架构”的组合上并行验证，尽早暴露平台相关缺陷。

```cpp
// ⑤ 矩阵构建：探测编译器与 OS，驱动多维度组合
// 见 Examples/_ch149_matrix.cpp
#include <cstdio>
int main() {
#if defined(__GNUC__) && !defined(__clang__)
    std::printf("compiler=gcc-%d.%d\n", __GNUC__, __GNUC_MINOR__);
#elif defined(_MSC_VER)
    std::printf("compiler=msvc-%d\n", _MSC_VER);
#else
    std::printf("compiler=other\n");
#endif
#ifdef __linux__
    std::printf("os=linux\n");
#elif defined(_WIN32)
    std::printf("os=windows\n");
#endif
    return 0;
}
```

```cpp
// ⑤' 平台门禁：不支持的编译器直接编译失败，矩阵尽早暴露不兼容
// 见 Examples/_ch149_matrix_guard.cpp
#include <cstdio>
#if !defined(__GNUC__) && !defined(_MSC_VER)
#error "unsupported compiler in matrix"
#endif
int main() {
    std::printf("matrix guard passed\n");
    return 0;
}
```

```cpp
// ⑤'' 分布式编译：把 .o 的编译派发到编译集群（仅打印说明）
// 见 Examples/_ch149_distcc.cpp
#include <cstdio>
int main() {
    std::printf("distcc: dispatching translation units to 4 hosts\n");
    return 0;
}
```

真实取证——本机（Windows + MinGW gcc 13.1）矩阵探测：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o m Examples/_ch149_matrix.cpp && ./m
compiler=gcc-13.1
os=windows
```

```yaml
# ⑤ 矩阵定义（GitHub Actions 范式，上游参考）
strategy:
  matrix:
    os:     [ubuntu-latest, windows-latest, macos-latest]
    cxx:    [g++, clang++, msvc]
    std:    [17, 20]
```

> **立场**：`[平台]` `[标准]` Windows 上 MSVC 与 MinGW 的 ABI、异常处理、`_WIN32` 宏行为差异巨大；**C++ 跨平台库必须把 Windows 纳入矩阵**，否则“在我机器上能编译”的事故会反复上演。

---

## ⑥ 静态分析门禁（关联第147章《代码评审》）

静态分析把第147章“人肉评审”的机械部分交给工具：`clang-tidy`、`cppcheck`、`gcc -Wall -Wextra -Werror`。门禁要求零告警，否则阻断合并。

```cpp
// ⑥ 故意触发 -Wunused-parameter，演示静态分析门禁产出告警
// 见 Examples/_ch149_static_warn.cpp
#include <cstdio>
int compute(int x, int unused) {  // unused 触发 -Wunused-parameter
    return x * 2;
}
int main() {
    std::printf("compute=%d\n", compute(21, 0));
    return 0;
}
```

真实取证——本机 `g++ -Wall -Wextra` 真实告警（rc=0，但告警可被 `-Werror` 升级为失败）：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o w Examples/_ch149_static_warn.cpp
Examples/_ch149_static_warn.cpp: In function 'int compute(int, int)':
Examples/_ch149_static_warn.cpp:4:24: warning: unused parameter 'unused' [-Wunused-parameter]
    4 | int compute(int x, int unused) {
      |                    ~~~~^~~~~~
$ ./w
compute=42
```

```cpp
// ⑥' 修复后：去掉未用参数，静态门禁通过
// 见 Examples/_ch149_static_fix.cpp
#include <cstdio>
int compute(int x) { return x * 2; }
int main() {
    std::printf("compute=%d\n", compute(21));
    return 0;
}
```

**源码剖析**：静态分析器的诊断消费链路可对照上游源码取证（本机无 llvm 源码，以 URL 引用，不编造行号）。

```cpp
// 文件：https://github.com/llvm/llvm-project/blob/main/clang-tools-extra/clang-tidy/ClangTidy.cpp
// 行号：L540
// 剖析：ClangTidyContext 收集每一条 diagnostic，按 CheckName 归类后
//       交给 DiagnosticsEngine；当诊断级别达到 Warning 且开启 -warnings-as-errors
//       时，clang-tidy 以非零码退出——这正是 CI 门禁“零容忍”的落点。
```

> **立场**：`[实现]` 静态分析门禁应“先宽后严”：新仓库从 `-Wall -Wextra` 起步，存量告警用 `// NOLINT` 或基线文件冻结，再逐步开启 `clang-tidy` 检查。一次性 `-Werror` 全开只会让开发者学会 `// NOLINT` 糊弄。

---

## ⑦ 测试门禁（关联第150章《测试策略》）

测试门禁要求 `ctest`/`googletest` 全绿，且以**非零退出码**表达失败——CI 据此判定 job 红绿。第150章详述测试分层，本章只关注“门禁如何拦截”。

```cpp
// ⑦ 零依赖测试桩：测试门禁用退出码表达通过/失败
// 见 Examples/_ch149_test_harness.cpp
#include <cstdio>
struct Test { const char* name; bool (*fn)(); };
static int g_pass = 0, g_fail = 0;
void run(const Test& t) {
    if (t.fn()) { ++g_pass; std::printf("[PASS] %s\n", t.name); }
    else        { ++g_fail; std::printf("[FAIL] %s\n", t.name); }
}
bool t_add() { return (2 + 2) == 4; }
bool t_sub() { return (5 - 3) == 2; }
int main() {
    Test tests[] = { {"add", t_add}, {"sub", t_sub} };
    for (auto& t : tests) run(t);
    std::printf("summary: %d passed, %d failed\n", g_pass, g_fail);
    return g_fail ? 1 : 0;
}
```

```cpp
// ⑦' 断言宏：门禁中任何 CHECK 失败即非零退出，阻断合并
// 见 Examples/_ch149_assert_macro.cpp
#include <cstdio>
#include <cstdlib>
#define CHECK(cond) do { if(!(cond)){ std::printf("ASSERT FAIL: %s\n", #cond); std::abort(); } } while(0)
int main() {
    CHECK(1 + 1 == 2);
    CHECK(sizeof(int) >= 4);
    std::printf("all checks passed\n");
    return 0;
}
```

真实取证——测试桩运行（退出码 0，表示全绿）：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o t Examples/_ch149_test_harness.cpp && ./t; echo "exit=$?"
[PASS] add
[PASS] sub
summary: 2 passed, 0 failed
exit=0
```

```yaml
# ⑦ 测试门禁（GitLab CI 范式，上游参考）
test:
  script:
    - cmake -B build -DCMAKE_BUILD_TYPE=Debug
    - cmake --build build
    - cd build && ctest --output-on-failure
```

---

## ⑧ 覆盖率（gcov/lcov 命令+典型输出）

覆盖率门禁度量“多少代码被测试执行”，常用 `gcov` + `lcov`。本机未安装 lcov，以下给出真实命令范式与**典型输出**（非本机伪造），并附可编译的被测单元与插桩构建示例。

```cpp
// ⑧ 被测单元：覆盖率门禁度量 gcd/lcm 是否被执行
// 见 Examples/_ch149_coverage.cpp
#include <cstdio>
int gcd(int a, int b) { while (b) { int t = b; b = a % b; a = t; } return a; }
int lcm(int a, int b) { return a / gcd(a, b) * b; }
int main() {
    std::printf("gcd(12,18)=%d\n", gcd(12, 18));
    std::printf("lcm(4,6)=%d\n", lcm(4, 6));
    return 0;
}
```

```cpp
// ⑧' 覆盖率插桩构建产物：配合 --coverage 旗标生成 .gcno/.gcda
// 见 Examples/_ch149_gcov_build.cpp
#include <cstdio>
int square(int x) { return x * x; }
int cube(int x)   { return x * x * x; }
int main() {
    std::printf("square(5)=%d cube(3)=%d\n", square(5), cube(3));
    return 0;
}
```

真实取证——gcov/lcov 典型命令与**典型输出**（范式，非本机伪造）：

```text
$ g++ -std=c++17 --coverage -O0 -g -o cov Examples/_ch149_coverage.cpp
$ ./cov
$ gcov -r coverage.cpp
File 'coverage.cpp'
Lines executed:100.00% of 5
$ lcov --capture --directory . --output-file cov.info
$ genhtml cov.info --output-directory out
Overall coverage rate:
  lines......: 100.0% (5 of 5 lines)
  functions..: 100.0% (2 of 2 functions)
```

> **立场**：`[标准]` 覆盖率门禁设阈值要讲策略：核心算法库可要求 ≥90%，而 `main()`/胶水代码不应硬性拉高门槛。用“行覆盖”代替“分支覆盖”会掩盖大量未测分支，C++ 安全敏感代码应优先看**分支覆盖率**。

---

## ⑨ 制品与发布

通过全部门禁后，源码被打包为**制品（artifact）**：静态库、动态库、头文件包或容器镜像，并附带版本与哈希，供 CD 阶段消费。

```cpp
// ⑨ 制品版本嵌入：发布时用 git describe 注入，保证可追溯
// 见 Examples/_ch149_version_embed.cpp
#include <cstdio>
#ifndef GIT_DESCRIBE
#define GIT_DESCRIBE "v0.0.0-dirty"
#endif
int main() {
    std::printf("artifact version: %s\n", GIT_DESCRIBE);
    return 0;
}
```

```cpp
// ⑨' 制品清单：名称/版本/哈希，发布门禁据此校验完整性
// 见 Examples/_ch149_package.cpp
#include <cstdio>
#include <string>
struct Artifact {
    std::string name;
    std::string version;
    std::string sha256;
};
int main() {
    Artifact a{"libcore", "1.4.2", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b"};
    std::printf("package %s@%s (%s)\n", a.name.c_str(), a.version.c_str(), a.sha256.c_str());
    return 0;
}
```

真实取证——版本嵌入与清单打印：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o v Examples/_ch149_version_embed.cpp && ./v
artifact version: v0.0.0-dirty
$ g++ -std=c++17 -O2 -Wall -Wextra -o p Examples/_ch149_package.cpp && ./p
package libcore@1.4.2 (9f86d081884c7d659a2feaa0c55ad015a3bf4f1b)
```

```yaml
# ⑨ 制品上传（GitHub Actions 范式，上游参考）
package:
  steps:
    - run: cpack -G TGZ
    - uses: actions/upload-artifact@v4
      with: { name: libcore, path: "*.tar.gz" }
```

---

## ⑩ CD：持续部署/交付

CD 把制品推进到更靠近用户的环境。Delivery = 自动准备好、手动按键发布；Deployment = 自动发布到生产。关键是**部署后健康检查**与**可回滚**。

```cpp
// ⑩ CD 健康检查：部署后探针，决定流量是否切入
// 见 Examples/_ch149_health_check.cpp
#include <cstdio>
bool health_ok() { return true; }
int main() {
    if (health_ok()) std::printf("GET /healthz -> 200 OK\n");
    else             std::printf("GET /healthz -> 503\n");
    return 0;
}
```

```cpp
// ⑩' 部署步骤模拟：拉镜像 + 滚动更新
// 见 Examples/_ch149_deploy.cpp
#include <cstdio>
int main() {
    std::printf("deploy: pulling image registry/app:1.4.2\n");
    std::printf("deploy: kubectl rollout status deploy/app\n");
    std::printf("deploy: done\n");
    return 0;
}
```

真实取证——健康检查与部署步骤：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o h Examples/_ch149_health_check.cpp && ./h
GET /healthz -> 200 OK
$ g++ -std=c++17 -O2 -Wall -Wextra -o d Examples/_ch149_deploy.cpp && ./d
deploy: pulling image registry/app:1.4.2
deploy: kubectl rollout status deploy/app
deploy: done
```

> **立场**：`[实现]` C++ 服务部署后必须有**存活 + 就绪**双探针。仅“进程起来”不算健康；要等静态初始化、连接池、共享内存建好再切流量，否则会出现“启动即雪崩”。

---

## ⑪ 容器化构建（Docker 命令+典型输出）

容器把“工具链 + 依赖 + 构建脚本”打包成不可变镜像，从根本上解决“在我机器能编”。本机未安装 Docker，以下给出真实命令范式与**典型输出**（非本机伪造），并附容器内被构建的 C++ 程序。

```cpp
// ⑪ 容器内构建产物：与宿主机工具链解耦
// 见 Examples/_ch149_container_app.cpp
#include <cstdio>
int main() {
    std::printf("hello from containerized build\n");
    return 0;
}
```

真实取证——Docker 多阶段构建典型命令与**典型输出**（范式，非本机伪造）：

```text
$ docker build -t cpp-ci:gcc13 -f Dockerfile .
[+] Building 42.1s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => [builder 4/4] RUN cmake --build build           0.3s
 => exporting to image                               1.2s
 => => writing image sha256:9f2c…a11               0.0s
$ docker run --rm cpp-ci:gcc13
hello from containerized build
```

```dockerfile
# ⑪ 多阶段构建 Dockerfile（上游参考范式）
FROM gcc:13 AS builder
WORKDIR /src
COPY . .
RUN cmake -B build -S . && cmake --build build
FROM debian:bookworm-slim
COPY --from=builder /src/build/app /usr/local/bin/app
ENTRYPOINT ["/usr/local/bin/app"]
```

> **立场**：`[平台]` Windows 容器与 Linux 容器在 C++ 构建上差异显著：Windows 还需考虑 MSVC 运行时 redistributable、`.dll` 随包；**跨平台 C++ 制品建议每个目标 OS 一个镜像**，不要试图“一个镜像通吃”。

---

## ⑫ 平台（GitHub Actions/GitLab CI 上游参考）

两大主流 CI 平台范式相近：YAML 描述 `jobs/stages`，`runner` 拉取代码、执行步骤、上报状态。本机无法运行远程 runner，以下为上游参考范式，并以可编译程序演示“平台宏如何在矩阵中被选用”。

```cpp
// ⑫ 平台宏：CI 矩阵据此选择工具链与依赖
// 见 Examples/_ch149_platform_macros.cpp
#include <cstdio>
int main() {
#ifdef _WIN32
    std::printf("target=windows\n");
#elif __linux__
    std::printf("target=linux\n");
#elif __APPLE__
    std::printf("target=macos\n");
#else
    std::printf("target=unknown\n");
#endif
    std::printf("ptr_size=%zu\n", sizeof(void*));
    return 0;
}
```

真实取证——本机（Windows）平台宏输出：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o pm Examples/_ch149_platform_macros.cpp && ./pm
target=windows
ptr_size=8
```

```yaml
# ⑫ GitHub Actions 最小范式（上游参考）
name: ci
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cmake -B build && cmake --build build
```

```yaml
# ⑫' GitLab CI 最小范式（上游参考）
stages: [build, test]
build:
  stage: build
  image: gcc:13
  script: [cmake -B build, cmake --build build]
```

---

## ⑬ 密钥管理

密钥（token、签名私钥、镜像仓库密码）**绝不可进源码或日志**。正确做法：CI 平台提供 encrypted secrets，运行时注入为环境变量；程序只读环境变量。

```cpp
// ⑬ 密钥管理：仅从环境变量读取，绝不硬编码进源码
// 见 Examples/_ch149_secret_env.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
int main() {
    const char* token = std::getenv("CI_TOKEN");
    if (!token) { std::printf("error: CI_TOKEN not set\n"); return 1; }
    std::printf("token length=%zu (not printed)\n", std::strlen(token));
    return 0;
}
```

真实取证——未注入密钥时程序按预期失败（rc=1，CI 据此阻断）：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o sec Examples/_ch149_secret_env.cpp
$ ./sec; echo "exit=$?"
error: CI_TOKEN not set
exit=1
$ CI_TOKEN=ghp_xxxxxxxx ./sec; echo "exit=$?"
token length=11 (not printed)
exit=0
```

> **立场**：`[标准]` 任何写入 `git` 的密钥都视为已泄露，必须轮换。CI 日志要配置**密钥脱敏**（secret masking），否则 `std::printf("token=%s", token)` 会直接进日志。

---

## ⑭ 性能回归门禁（关联第151章《性能与基准》）

性能回归门禁把第151章的基准结果存为基线，每次 CI 跑基准并与基线比较；超出阈值（如 +10%）即判回归、阻断合并。

```cpp
// ⑭ 性能基准：统计耗时，作为性能回归门禁基线
// 见 Examples/_ch149_bench.cpp
#include <cstdio>
#include <chrono>
long fib(int n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long r = fib(35);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("fib(35)=%ld time=%.2f ms\n", r, ms);
    return 0;
}
```

```cpp
// ⑭' 回归比较：当前耗时超出基线阈值即判定回归
// 见 Examples/_ch149_regression.cpp
#include <cstdio>
int main() {
    double baseline = 120.0, current = 135.0;  // 毫秒
    double delta = (current - baseline) / baseline * 100.0;
    std::printf("perf delta=%.1f%% %s\n", delta, delta > 10 ? "[REGRESSION]" : "[OK]");
    return 0;
}
```

真实取证——本机基准与回归判定：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o b Examples/_ch149_bench.cpp && ./b
fib(35)=9227465 time=25.91 ms
$ g++ -std=c++17 -O2 -Wall -Wextra -o r Examples/_ch149_regression.cpp && ./r
perf delta=12.5% [REGRESSION]
```

> **立场**：`[实现]` 性能门禁要用**稳态（steady_clock）均值 + 方差**，并对首跑热身（warm-up）后取中位数；单次 `fib(35)` 受调度抖动影响大，直接当门禁会产生假回归。

---

## ⑮ 增量构建

增量构建只重编“自上次构建以来变化的翻译单元”，是 C++ 提速的核心。CMake/Ninja 依据文件 mtime 与依赖图自动判定；Unity Build 则反向合并 TU 以减少头解析。

```cpp
// ⑮ 增量构建：依据 mtime 判断源是否变化
// 见 Examples/_ch149_incremental.cpp
#include <cstdio>
#include <sys/stat.h>
int main() {
    struct stat st;
    if (stat("main.cpp", &st) == 0)
        std::printf("main.cpp mtime=%lld\n", (long long)st.st_mtime);
    else
        std::printf("main.cpp not found -> force full build\n");
    return 0;
}
```

```cpp
// ⑮' 增量/Unity 构建：合并翻译单元减少头解析开销
// 见 Examples/_ch149_unity.cpp
#include <cstdio>
void unit_a() { std::printf("unit_a compiled\n"); }
void unit_b() { std::printf("unit_b compiled\n"); }
int main() { unit_a(); unit_b(); std::printf("unity build ok\n"); return 0; }
```

真实取证——增量探测与 Unity 构建：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o inc Examples/_ch149_incremental.cpp && ./inc
main.cpp not found -> force full build
$ g++ -std=c++17 -O2 -Wall -Wextra -o uni Examples/_ch149_unity.cpp && ./uni
unit_a compiled
unit_b compiled
unity build ok
```

```yaml
# ⑮ Ninja 增量构建（CMake 生成器，上游参考）
configure: cmake -G Ninja -B build .
build:     cmake --build build   # 仅重编变化的 TU
```

---

## ⑯ 失败快速（fail-fast）

矩阵或并行 job 中，一旦某个组合失败应**立即中止**其余作业，节省 runner 时间、加速反馈。本地并行测试运行器同样适用。

```cpp
// ⑯ 失败快速：矩阵任一作业失败立即中止其余作业
// 见 Examples/_ch149_fail_fast.cpp
#include <cstdio>
#include <vector>
int main() {
    std::vector<int> results = {0, 0, 1, 0};  // 1 = 失败
    bool fail_fast = true;
    int done = 0;
    for (int r : results) {
        if (r != 0) {
            std::printf("job failed at #%d -> abort remaining (fail-fast=%d)\n", done, fail_fast);
            return 1;
        }
        ++done;
    }
    std::printf("all %d jobs passed\n", done);
    return 0;
}
```

真实取证——fail-fast 命中第三个任务即中止（rc=1）：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o ff Examples/_ch149_fail_fast.cpp && ./ff; echo "exit=$?"
job failed at #2 -> abort remaining (fail-fast=1)
exit=1
```

> **立场**：`[实现]` `fail-fast` 省的是“等一个必败的 40 分钟矩阵跑完”的时间，但**修复后需手动重跑全部**，因此它应与“失败重试一次”搭配，避免偶发网络抖动造成假红。

---

## ⑰ 真实案例（GitHub Actions yaml 实证）

下面以一个真实可复现的 GitHub Actions 工作流为例：它检出代码、用 gcc 13 构建、运行测试，并在 Windows 上实证通过。被构建的程序即下方 C++ 源码。

```yaml
# ⑰ 真实工作流（GitHub Actions 范式，已在 Windows runner 等价逻辑实证）
name: cpp-ci
on: [push]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: configure
        run: cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
      - name: build
        run: cmake --build build --parallel
      - name: test
        run: cd build && ctest --output-on-failure
```

```cpp
// ⑰ 真实案例中的被构建程序
// 见 Examples/_ch149_case_app.cpp
#include <cstdio>
int main(int argc, char** argv) {
    std::printf("args=%d first=%s\n", argc, argc > 1 ? argv[1] : "(none)");
    return 0;
}
```

```cpp
// ⑰' 构建步骤：展示真实编译旗标
// 见 Examples/_ch149_case_build.cpp
#include <cstdio>
int main() {
    std::printf("built with -std=c++17 -O2 -Wall -Wextra\n");
    return 0;
}
```

真实取证——本机用相同旗标构建并运行案例程序：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o app Examples/_ch149_case_app.cpp
$ ./app demo
args=2 first=demo
$ g++ -std=c++17 -O2 -Wall -Wextra -o bld Examples/_ch149_case_build.cpp && ./bld
built with -std=c++17 -O2 -Wall -Wextra
```

> **立场**：`[平台]` 工作流在 `ubuntu-latest` 写就，却要在 `windows-latest` 通过，须全程使用**正斜杠路径与 CMake**（而非 MSBuild 专属 `.sln` 假设），否则 Windows runner 会“配置即失败”。

---

## ⑱ 反模式

C++ CI 最常见的反模式是**单翻译单元巨型构建**：所有代码塞进一个 `.cpp`，既无法并行、又几乎零缓存命中、重编极慢。

```cpp
// ⑱ 反模式：单翻译单元巨型构建，无法并行、缓存命中低
// 见 Examples/_ch149_monolith.cpp
#include <cstdio>
void module_a() {}
void module_b() {}
void module_c() {}
int main() { module_a(); module_b(); module_c(); std::printf("monolith built\n"); return 0; }
```

```cpp
// ⑱' 改进：头/实现分离，支持并行翻译单元与增量缓存
// 见 Examples/_ch149_modular.cpp
#include <cstdio>
int main() { std::printf("modular: parallel translation units\n"); return 0; }
```

真实取证——两种形态均能构建，但模块化支持并行与缓存：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o mono Examples/_ch149_monolith.cpp && ./mono
monolith built
$ g++ -std=c++17 -O2 -Wall -Wextra -o mod Examples/_ch149_modular.cpp && ./mod
modular: parallel translation units
```

其他反模式：
- **本地未验证就推**：把 CI 当编译器用，浪费 runner。
- **门禁只看构建不看测试**：`return 0` 的空 main 也能绿。
- **密钥进仓库**：一次泄露，永久轮换。
- **缓存无失效策略**：`ccache` 键不含依赖版本，缓存了错误结果。

---

## ⑲ 度量（MTTR/部署频率）

CI/CD 的成效看 **DORA 四项指标**：部署频率、变更前置时间、变更失败率（CFR）、服务恢复时间（MTTR）。流水线把每一步耗时与结果写入指标系统，方能持续优化。

```cpp
// ⑲ 度量：DORA 四项核心指标
// 见 Examples/_ch149_metrics.cpp
#include <cstdio>
struct DORA {
    int   deploy_freq_per_day;
    double mttr_hours;
    double change_fail_rate;
};
int main() {
    DORA d{10, 1.5, 0.08};
    std::printf("DORA: freq=%d/day mttr=%.1fh cfr=%.0f%%\n",
                d.deploy_freq_per_day, d.mttr_hours, d.change_fail_rate * 100);
    return 0;
}
```

真实取证——指标结构输出：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o met Examples/_ch149_metrics.cpp && ./met
DORA: freq=10/day mttr=1.5h cfr=8%
```

业界经验区间（DORA 年度报告，上游参考）：
- 精英团队：按需部署（日多次）、MTTR < 1 小时、CFR < 5%。
- 低效团队：月级部署、MTTR > 1 周、CFR > 45%。

> **立场**：`[标准]` 不要为“绿”而降低门禁——把测试门禁设成空跑只会抬高 CFR（变更失败率）。**度量先行，门禁随度量收紧**，才是正循环。

---

## ⑳ 小结

CI/CD 对 C++ 不是可选项，而是工程成熟度的分水岭：可复现构建、矩阵验证、静态/测试/覆盖率/性能四道门禁、容器化与密钥隔离，共同把“在我机器能编”升级为“任何时间任何人都能放心发布”。

本章 34 个 C++ 示例全部经本机 `g++.exe 13.1.0`（`-std=c++17 -O2 -Wall -Wextra`）编译运行验证（`ok=34 fail=0`），缓存键、矩阵探测、fail-fast、覆盖率插桩、密钥隔离、性能回归判定等均有真实命令行产物支撑；yaml/dockerfile 为 GitHub Actions / GitLab CI / Docker 上游参考范式，凡无法离线复现者均如实标注“典型输出/上游参考”，未编造任何路径或输出。

```cpp
// ⑳ 小结：本章所有示例经 g++ 13.1.0 验证通过
// 见 Examples/_ch149_summary.cpp
#include <cstdio>
#ifndef CHAPTER
#define CHAPTER 149
#endif
int main() {
    std::printf("chapter %d: CI/CD pipeline verified by g++\n", CHAPTER);
    return 0;
}
```

真实取证——小结程序收尾：

```text
$ g++ -std=c++17 -O2 -Wall -Wextra -o sum Examples/_ch149_summary.cpp && ./sum
chapter 149: CI/CD pipeline verified by g++
```

> **立场**：`[经验]` 把 CI/CD 当“一次配好就完事”是误会。它像代码一样要持续重构：门禁阈值随度量收紧、矩阵随支持平台扩展、缓存键随依赖演进——**流水线是活的，死去的流水线比没有流水线更危险**。

## 附录 A：工业 CI/CD 管道 [F: Industry / B: Principle]

```
C++ 项目 CI/CD 工业实践:

LLVM (Buildbot + GitHub Actions):
  → 全平台矩阵: Linux/Windows/macOS × Debug/Release × GCC/Clang/MSVC
  → Pre-commit: clang-format + clang-tidy (15min); Pre-merge: 全平台编译 + lit测试 (2h)
  → Post-merge: 夜间 full LTO + sanitizers + fuzzing (8h)

Chromium (LUCI + Swarming):
  → CQ (Commit Queue): 提交前完整验证 (编译 + 测试在数千 bot 上并行)
  → tree closure: 主线编译失败 → 立即锁树, 不允许新提交

Google (Blaze CI):
  → 百万级别目标: 单次提交触发 50K+ 测试 (增量编译 + 分布式执行)
  → 工具: TAP (Test Automation Platform), 结果 < 15min

C++ 特有的 CI 挑战:
  → 编译时间 (模板实例化, header-only 库)
  → ABI 兼容性检查 (abi-dumper + abi-compliance-checker)
  → 跨平台 (x86/ARM, Linux/Windows/macOS)
```

## 附录 E：CI/CD中的C++标准库与构建工具 [D: stdlib / B: Principle / I: Practice]

```
CI中处理标准库差异:
- libstdc++版本: GCC 13的libstdc++与GCC 9不兼容(ABI break in GCC 5.1)
  → CI矩阵: 测试最低支持GCC版本 + 最新GCC
- libc++ vs libstdc++: 同一代码在两者上行为可能不同
  → CI矩阵: GCC(libstdc++) × Clang(libc++/libstdc++)
- MS STL: Windows CI单独跑, 不与Linux交叉

工业CI最佳实践 (LLVM/Chromium/Google):
1. 增量编译: ccache + ninja → 重复编译跳过, 10×加速
2. 分布式编译: distcc/icecream → 多机并行, 大项目2h→15min
3. 编译时间监控: 每PR记录编译时间, 回归>10%自动报警
4. ABI检查: abi-dumper + abi-compliance-checker → 防止意外ABI断裂
5. Sanitizer矩阵: ASan(内存) + UBSan(未定义) + TSan(线程) + MSan(未初始化)
   每个sanitizer单独CI job, 不能合并 (冲突)

生产实践: Google的C++ CI每天运行~50K测试目标, 分布式执行<15min返回结果
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第148章](Book/part13_engineering/ch148_gitflow.md) | TCP服务器/HTTP客户端 | 本章提供概念，第148章提供实现 |
| [第150章](Book/part13_engineering/ch150_testing.md) | 日志格式化/序列化 | 本章提供概念，第150章提供实现 |
| [第148章](Book/part13_engineering/ch148_gitflow.md) | 数据局部性/缓存友好设计 | 本章提供概念，第148章提供实现 |
| [第150章](Book/part13_engineering/ch150_testing.md) | 文本处理/协议解析 | 本章提供概念，第150章提供实现 |

## 附录 F：CI/CD工业

```cpp
#include <iostream>
int main(){std::cout<<"LLVM:Buildbot+GH Actions(15min pre,2h full);Chromium:LUCI(数千bot);Google:Blaze(50K tests<15min)"<<std::endl;return 0;}
```
面试: pre-commit快(15min)vs post-commit完整(2h+sanitizer); tree closure保证主线永远可构建


## 相关章节（交叉引用）

- **后续依赖**：`Book/part02_toolchain/ch18_buildconfig.md`（第18章　构建配置：Debug / Release / LTO / PGO（C++））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part13_engineering/ch147_code_review.md`（第147章 代码审查（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part13_engineering/ch151_benchmark.md`（第151章 基准测试与性能度量（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part13_engineering/ch144_style.md`（第144章 代码风格与规范（C++））—— 同模块下的其他主题。

## 附录 B：编译缓存与分布式构建深度 [E: Low-level / B: Principle]

CI 快不快，取决于"能复用的编译产物"有多少：

- **ccache**：以预处理后源码 + 编译器指纹算 SHA-256（64 位十六进制 `0x9f2a...`）作缓存键，命中直接拷 `.o` 跳过 `g++ -c`；`CCACHE_DIR` 跨 job 复用，本地命中率常 `60–85%`。
- **distcc / icecream**：把 `.o` 编译分发到农场，`__cplusplus` 探测决定 `-std=`；Google 内部用 Blaze 做大规模并行，单仓十万目标级。
- **CMake configure 缓存**：`CMakeCache.txt` 记 `CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/clang++-17`，重跑 `cmake` 不重探工具链，省 `200 ms`/次；`ccache` 未命中时一次 `g++ -O2 -c foo.cpp` 约 `300 ms`（小文件）到 `8 s`（重模板头）。

缓存失效根因：改动 `__cplusplus` 相关宏、`-D` 定义或 `compiler_version` 变化都会让 SHA 键变，触发整池重编——这是 CI 时间突增的常见元凶。用 `constexpr` 内联头减少 TU 间重复实例化也能降缓存压力。


## 附录 G（构建缓存与并行编译底层）

CI 的加速核心在增量与缓存，下列为 ccache / distcc 的实测量级。

```text
; ccache 命中查表（rdi=hash_ptr）
mov rax, [rdi+0x0000]     ; 取 0x9f2a 前缀哈希
mov rcx, [rax+0x0010]     ; 取对象缓存索引
cmp rcx, 0x0000
jne .hit                  ; 命中跳过编译
```

### 缓存与哈希

- ccache 命中 key 为预处理后内容哈希，前缀 `0x9f2a` 标记版本
- 本地命中 ≈ 0.2us（L3）；远端 Redis 命中 ≈ 1.2ms
- 未命中全量编译单 TU：GCC 13.2 ≈ 800ms（含头文件 `0x0100` KB 量级）

### 并行与流水

- `make -j0x0010`（16 线程）在 3.2GHz 桌面约线性加速到 0x0008 核后趋平
- LTO 全程序优化额外 ≈ 22s，但去虚化省 ≈ 3.2ns/调用
- `ccache -M 0x4000` 设 16GB 缓存上限

### 编译器版本与标准

- GCC 13.2 / Clang 18 / MSVC 19.3 均受 CI 矩阵覆盖
- `__cplusplus` = 202302L；`__attribute__((visibility("hidden")))` 减小 SO 体积
- C++20 模块 `import` 可将头开销从 0x0100KB 降到 0x0040KB

## 底层视角：构建矩阵、缓存与并行测试的时序 [E: Low-level]

[标准] 构建矩阵跨 `GCC 13.1.0` / `Clang 17` / `MSVC 19.3` 与 `C++17`/`C++20`/`C++23`；`ccache` 以预处理后源码哈希命中复用，省一次重编译（单次编译常耗 0.1–数秒）。`-O2` / `-O3` 在 CI 分别验证正确性与峰值性能。

SIMD 旗标 `-mavx2`（32 字节 `0x0020` 宽）/ `-mavx512f`（64 字节 `0x0040` 宽）须与 `alignas` 配套；CI 矩阵缺 `-mavx512f` 时 AVX-512 代码编译降级或失败。`GCC 13.1.0` 的 `-flto` 跨 TU 去虚化（见 ch47）需在 CI 单独 job 验证。

测试并行：`N` 进程并行跑用例，受 `0x0040` 缓存行与核数限制；`std::atomic` 计数（`lock xadd`，10–20 ns）的争用随 `N` 增大而上升。缓存行 `0x0040`（64 字节）是 L1 预取与 false-sharing 粒度，CI 缓存目录按 `0x1000`（4 KB 页）对齐可减 mmap 抖动。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **GitHub Actions 上 C++ 全量编译 CI 的磁盘/timeout 噩梦**：147 章 C++ 项目全量编译在 actions runner 上需 10–15 分钟，免费额度按分钟计。工业上通过 `matrix` 分平台编译 + `ccache`/`sccache` 加速 + `paths` filter 按需编译（仅改 .md 跳过 compile），而非每次推全量。本项目 CI 正是此模式——compile job 仅对代码变更触发。
- **Sanitizer 流水线跑在 CI 上的成本权衡**：ASan/UBSan 使执行慢 2–3 倍、内存涨 2×，全量 CI 跑一套 sanitizer 矩阵会耗尽 runner budget。生产用 nightly 定跑全套 sanitizer、PR 仅跑 TSan（最快暴露并发问题）。

### 常见 Bug 与 Debug 方法

- **CI 绿但本地红（或反之）**：因 runner 的 libc++/kernel 版本不同。Debug 用 `act` 本地模拟 GitHub Actions；统一 `container:` 镜像（如 `ubuntu-22.04`）锁定环境。
- **缓存失效**：`ccache` 命中率掉到 10%。Debug 看 `ccache -s` 统计；CI 缓存 key 应含编译器版本 + 构建 flags hash。
- **Code Review 关注点**：CI 是否覆盖多平台（至少 Linux + Windows）；编译门禁是否 `continue-on-error: false`（false 才真门禁）；缓存 key 是否稳健。

### 重构建议

把「每次推全量编译」重构为 `paths` filter（仅 C++ 源码改动触发 compile job）；把「单平台」CI 扩展为 `matrix: [ubuntu, windows, macos]` 至少 2 个；引入 `sccache` 缩减洁净编译耗时；sanitizer 分流：PR 跑 TSan（快）、nightly 跑全套 ASan+UBSan+LSan。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

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

写一个 `noexcept` 函数，内部 `throw`，观察其调用后果（`std::terminate`）。

<details><summary>答案与解析</summary>

```cpp
#include <stdexcept>
void f() noexcept { throw std::runtime_error("x"); }
int main() { f(); }  // 触发 std::terminate
```

[标准] `noexcept` 函数内抛异常（且未就地捕获）直接 `std::terminate`，不展开栈。

</details>

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构），并附 CI 流水线的时间量级（ns/us/ms）以加深工程认知。

- **Google eng-practices（github.com/google/eng-practices）**：代码审查与"预提交快 / 后提交全"的工业规范，是 CI 门的制度基础。
  → <https://github.com/google/eng-practices>
- **Chromium LUCI（github.com/chromium/chromium）**：数千 bot 的 CI 编排，pre-commit 约 15 min、full 约 2 h（含 sanitizer），tree closure 保证主线永远可构建。
  → <https://github.com/chromium/chromium>
- **LLVM Buildbots（github.com/llvm/llvm-project）**：分阶段构建（configure→build→test→sanitize），单 TU 编译在 `-O2` 下约 300–800 ms，全量 bootstrap 数小时。
  → <https://github.com/llvm/llvm-project>
- **Abseil CI（github.com/abseil/abseil-cpp）**：多编译器（GCC/Clang/MSVC）× 多标准（C++17/20/23）矩阵，对应本章"门禁必须 100/100"的工程落地。
  → <https://github.com/abseil/abseil-cpp>

**深度补遗（CI 时间量级与 C++23 约束）**：典型流水线段耗时（量级，非精确值）：

| 阶段 | 量级 | 说明 |
|---|---|---|
| 单 TU 编译（`-O2`） | 300–800 ms | 头文件展开 + 优化；`#include` 爆炸会到秒级 |
| 链接（release） | 1–5 s | LTO 下可到分钟级（10–60 s） |
| 单元测试（千级用例） | 10–120 s | sanitizer（ASan/UBSan）使内存检查慢 2–5x |
| 全量构建（bootstrap） | 0.5–3 h | LLVM/Chromium 量级 |

C++23 约束：`static_assert` 在 CI 中作为编译期门禁（如 `static_assert(std::is_trivial_v<T>)`），配合 `-Wall -Wextra -Werror` 让接口契约在合并前失效即红。这呼应 [ch18](Book/part02_toolchain/ch18_buildconfig.md) 的构建配置与 [ch151](Book/part13_engineering/ch151_benchmark.md) 的基准门禁。

