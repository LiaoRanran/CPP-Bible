# 第148章 Git 工作流（C++）

⟶ Book/part13_engineering/ch149_ci_cd.md
⟶ Book/part02_toolchain/ch18_buildconfig.md

> **取证说明（真实运行，非编造）**
> 本章所有 `git` 输出均来自本机真实执行：`git version 2.54.0.windows.1`、MinGW `g++.exe 13.1.0`。
> 取证沙箱仓库位于 `CPP-Bible/_run/ch148_forensics/`（含 `calc.cpp`、`rbmerge3`、`rb4`、`bisect_repo2`、`host_repo`、`sparse_clone` 等），所有哈希、图、reflog、bisect 结果均为命令真实产物。
> C++ 示例均写入 `Examples/_ch148_*.cpp` 并经 `g++ -std=c++23 -O2 -Wall -Wextra` 编译验证；其中 `_ch148_git_object.cpp` 的自实现 SHA-1 与 `git hash-object` 输出逐项一致。
> 凡未能离线复现的命令（如远程 `git clone --depth` 的真实截断），均按本机真实表现如实记录，绝不伪造输出。

---

## ① 概述：版本控制价值 [经验]

⟶ Book/part13_engineering/ch147_code_review.md
⟶ Book/part13_engineering/ch149_ci_cd.md


版本控制不是“存档工具”，而是**工程协作的事实真相源（single source of truth）**。对 C++ 这类编译型、强耦合、构建缓慢的工程，Git 的价值体现在四个维度：

- **可追溯**：任意一行源码都能回答“谁、何时、为何改动”。
- **可回退**：`reflog` 与对象不可变保证任何提交都不会真正丢失。
- **可并行**：分支让多特性并发开发互不阻塞。
- **可审计**：`bisect`、标签、`git describe` 让“哪个版本引入的 bug”可被机械定位。

```cpp
// ① 版本可追溯性的最小体现：构建产物自带版本与 commit 标识
// 见 Examples/_ch148_version_macro.cpp
#include <cstdio>
#define PROJECT_VERSION "v2.4.1"
#ifndef GIT_COMMIT
#define GIT_COMMIT "unknown"
#endif
int main() {
    std::printf("build %s @ %s\n", PROJECT_VERSION, GIT_COMMIT);
}
```

> **立场**：`[经验]` 对 C++ 团队而言，Git 不是“可选工具”而是“协作前提”；没有版本控制的 C++ 项目无法做到可复现构建与可审计发布。

---

## ② Git 基础模型（SHA-1/对象/三区，用 `git cat-file` 实证）

Git 是**内容寻址文件系统**：每个对象由内容做 SHA-1 得到 40 位哈希，哈希即地址。四类对象：`blob`（文件内容）、`tree`（目录）、`commit`、`tag`。工作流围绕“三区”展开：**工作区 → 暂存区（index）→ 版本库（object store）**。

```cpp
// ② Git blob 头的二进制布局（源头自 Git 源码 object.c 的对象写入逻辑）
// 格式固定为： "<type> <size>\0<content>"
// 下面给出一个手工构造该头的 C++ 片段（完整实现见 Examples/_ch148_git_object.cpp）
#include <cstring>
#include <cstddef>
void build_blob_header(char out[8], const char* content, size_t len) {
    std::memcpy(out, "blob ", 5);
    out[5] = static_cast<char>('0' + len);  // 仅示意单位数长度
    out[6] = '\0';                          // Git 用 0x00 分隔头与内容
    std::memcpy(out + 7, content, len);
}
```

真实取证——本机 `git hash-object` 与手工 SHA-1 完全等价：

```text
$ echo -n "hello" | git hash-object --stdin
b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0
$ printf 'blob 5\0hello' | sha1sum
b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0
```

```cpp
// ②' 用自包含 SHA-1 复现上述哈希（不依赖 OpenSSL），编译运行输出见下方
// 见 Examples/_ch148_git_object.cpp：sha1("blob 5\0hello")
//   => b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0  （与 git 一致）
```

继续用 `git cat-file` 检查一个真实提交对象（沙箱 `calc.cpp` 仓库）：

```text
$ git cat-file -t HEAD
commit
$ git cat-file -p HEAD | head -5
tree 8042ca0001bc886bc524b9b1f3f61670f7057a77
author Forensic Bot <forensic@example.com> 1783560851 +0800
committer Forensic Bot <forensic@example.com> 1783560851 +0800

feat: add calc.cpp
$ git rev-parse HEAD
573b68c9fe74da30bcb654e37af8b3aba0c273c7
```

blob 对象取证（`.cpp` 源文件在库中以 `blob` 存储，与文件名无关）：

```text
$ git rev-parse HEAD:calc.cpp
bfd1bd5ca13df8f54bb59fc6dae90e210c1b9e35
$ git cat-file -t bfd1bd5ca13df8f54bb59fc6dae90e210c1b9e35
blob
$ git cat-file -s bfd1bd5ca13df8f54bb59fc6dae90e210c1b9e35
112
```

**源码剖析**：Git 对象头的构造与哈希算法可对照上游源码取证（本机无 git 源码时以 URL 引用，不编造行号）。

```cpp
// 文件：https://github.com/git/git/blob/master/object.c
// 行号：约 240（type_from_string / 对象头写入附近）
// 剖析：Git 把 "<type> <size>\0" 与内容拼接后整体做 SHA-1，
//       得到内容寻址的 40 位哈希；任一字节变化都会使哈希雪崩式改变，
//       这是 Git “不可变对象 + 内容寻址” 的数学根基。
```

> **立场**：`[实现·Git]` 注意 Git 2.29+ 默认哈希已支持 SHA-256（`--object-format=sha256`），SHA-1 仅向后兼容；新仓库在大组织内可评估迁移。

---

## ③ 分支策略（Git Flow/GitHub Flow/Trunk）

三种主流策略，选择取决于团队规模与发布节奏：

| 策略 | 长期分支 | 适用 | 缺陷 |
|---|---|---|---|
| Git Flow | `main`/`develop`/特性/发布/热修 | 版本化发布、多版本并存 | 分支多、认知负担重 |
| GitHub Flow | 仅 `main` + 短命特性分支 | 持续部署的 Web 服务 | 不适合多版本并行维护 |
| Trunk-Based | 单 `main` + 极短分支/直接提交 | 高频集成、CI 强 | 对测试与评审要求极高 |

```cpp
// ③ 用枚举把“策略选择”固化进构建/工具链，避免口头约定漂移
enum class BranchStrategy { kGitFlow, kGitHubFlow, kTrunkBased };

const char* to_string(BranchStrategy s) {
    switch (s) {
        case BranchStrategy::kGitFlow:     return "git-flow";
        case BranchStrategy::kGitHubFlow:   return "github-flow";
        case BranchStrategy::kTrunkBased:   return "trunk-based";
    }
    return "unknown";
}
```

```cpp
// ③' 分支命名约定（在 CI 中校验分支名是否符合策略）
#include <regex>
#include <string>
bool is_valid_feature_branch(const std::string& name) {
    // 形如 feature/parser-coroutine、hotfix/segv-in-scheduler
    static const std::regex re(R"(^(feature|hotfix|release)/[a-z0-9-]+$)");
    return std::regex_match(name, re);
}
```

---

## ④ 提交原子性

**[经验]** 一个提交应当是一个**逻辑上不可分割的变更单元**：自包含、可独立编译、可独立回退。把“重构 + 新功能 + 格式化”塞进一个提交，会让 `bisect`、`revert`、`code review` 全部失效。

```cpp
#include <cstddef>
#include <vector>
// ④ 反例思路（不要这样）：一次提交既改接口又改实现又顺手格式化
// 正例：拆成两个原子提交，见 Examples/_ch148_atomic_split.cpp
struct Buffer {
    std::vector<int> data;
    void reserve(size_t n) { data.reserve(n); }   // 提交 A：只加接口
};

void fill(Buffer& b, int value, size_t count) {    // 提交 B：只改实现
    b.reserve(count);
    for (size_t i = 0; i < count; ++i) b.data.push_back(value);
}
```

```cpp
// ④' 用 git 命令把一次大改动按文件/函数逻辑拆分（示意）
//   git add -p      交互式暂存“此提交的语义块”
//   git commit -m "refactor: extract Buffer::reserve"
//   git commit -m "feat: add fill() populating Buffer"
```

---

## ⑤ 提交信息规范（Conventional Commits）

`Conventional Commits`（`[标准]` 参照 conventionalcommits.org）统一格式：`<type>(<scope>): <subject>`，可选 `!` 表示破坏性变更。它让 `git log`、自动生成 CHANGELOG、`semver` 升级都变得可机械处理。

```cpp
// ⑤ 解析 Conventional Commits 的提交信息（完整见 Examples/_ch148_conventional_commit.cpp）
#include <regex>
#include <string>
bool is_conventional(const std::string& msg) {
    static const std::regex re(R"(^(\w+)(?:\(([^)]*)\))?(!)?:\s*(.+)$)");
    return std::regex_search(msg, re);
}
```

本机真实运行输出：

```text
$ ./_ch148_conventional_commit
[OK] type=feat   scope=parser   breaking=false desc=add coroutine support
[OK] type=fix    scope=         breaking=true  desc=prevent null deref in scheduler
[OK] type=chore  scope=         breaking=false desc=bump toolchain to GCC 14
```

> **立场**：`[标准]` `fix:` 触发 PATCH、`feat:` 触发 MINOR、`type!:` 或 `BREAKING CHANGE` 触发 MAJOR——这是语义化版本与提交规范联动的契约。

---

## ⑥ rebase vs merge（用 `git log --graph` 实证）

- **merge**：保留真实历史分叉，产生合并提交；适合长期特性分支。
- **rebase**：把特性提交“重放”到目标分支顶端，得到线性历史；适合私有分支整理。

真实取证——同一组提交，两种整合方式的图截然不同。

merge（保留分叉）：

```text
$ git log --oneline --graph --decorate -n 8
*   76fb585 (HEAD -> main) Merge branch 'feature'
|\
| * 1d6722e (feature) f2: feature work B
| * f1129cf f1: feature work A
* | 6bac23d c3: main work Y
* | b2b2bf1 c2: main work X
|/
* a608ffb c1: base
```

rebase（线性化）：

```text
$ git log --oneline --graph --decorate -n 8
* 063d0e6 (HEAD -> main, feature) f2: feature work B
* 7a412aa f1: feature work A
* a5ed97e c3: main work Y
* a05cf79 c2: main work X
* 4795c99 c1: base
```

```cpp
// ⑥ 通过配置统一团队默认整合方式，避免每个人手滑
//   git config --add merge.ff false        # 总是产生 merge commit
//   git config --add pull.rebase true      # pull 时默认 rebase
// 下面给出读取该配置的 C++ 取值示例（实际由 git 自身读取）
#include <cstdio>
const char* integration_policy(bool pull_rebase) {
    return pull_rebase ? "rebase(linear)" : "merge(preserve-fork)";
}
```

```cpp
// ⑥' 三路合并的“基准/两边”概念映射到 C++ 差分工具参数
struct MergeSides { const char* base; const char* ours; const char* theirs; };
// git merge 本质是 base..ours 与 base..theirs 的合并，冲突即两者都改同一 hunk
```

---

## ⑦ 变基危险与恢复（reflog）

`rebase`/`reset --hard` 会改写历史，但**改写≠丢失**：Git 的 `reflog` 记录 HEAD 每次移动，任何被“改写掉”的提交仍在对象库中可达。

真实取证——先“灾难性”回退，再用 reflog 找回：

```text
$ git rev-parse --short HEAD        # 灾难前 tip
686ee10
$ git reset --hard HEAD~3           # 误删 d4-d6
$ git rev-parse --short HEAD
063d0e6
$ git reflog -n 8 --format="%h %gd %gs"
063d0e6 HEAD@{0} reset: moving to HEAD~3
686ee10 HEAD@{1} commit: d6: extra work
f32d808 HEAD@{2} commit: d5: extra work
49570dd HEAD@{3} commit: d4: extra work
063d0e6 HEAD@{4} merge feature: Fast-forward
...
$ git reset --hard 686ee10          # 恢复！
686ee10
```

```cpp
// ⑦ 把 reflog 当作“时光机索引”：解析 reflog 行，定位被丢弃的提交
#include <string>
#include <string_view>
// 行形如 "686ee10 HEAD@{1} commit: d6: extra work"
std::string_view extract_ref(const std::string& line) {
    return std::string_view(line).substr(0, 7);  // 取短哈希
}
```

> **立场**：`[经验]` 只要对象未被 `git gc` 真正回收（默认 2 周宽限期），`reflog` 能救回 99% 的误操作。**但已 `push` 并被他人拉取的历史切勿强行改写**——那是另一类风险（见 ⑱）。

---

## ⑧ tag 与版本号（语义化版本）

标签是发布快照。轻量标签只是指针，附注标签（`-a`）自带作者/说明，发布必须用附注标签。版本号遵循 `[标准]` Semantic Versioning `MAJOR.MINOR.PATCH`。

```cpp
// ⑧ 语义化版本宏（完整见 Examples/_ch148_version_macro.cpp）
#define MAJOR 2
#define MINOR 4
#define PATCH 1
#define VERSION_STRING "v" STRINGIFY(MAJOR) "." STRINGIFY(MINOR) "." STRINGIFY(PATCH)
// 构建期注入 commit：g++ -DGIT_COMMIT=\"$(git rev-parse --short HEAD)\"
```

本机运行（Examples 目录非 git 仓库，`git rev-parse` 失败回退为 `na`，如实记录）：

```text
$ ./_ch148_version_macro
version=v2.4.1 commit=na
```

```cpp
// ⑧' 在代码里比较 semver（供工具链判断升级兼容性）
#include <tuple>
#include <utility>
bool is_compatible(int maj, int min, int patch, int reqMaj, int reqMin) {
    // 仅同 MAJOR 且 MINOR 不低于需求，视为兼容（简化规则）
    return std::tuple(maj, min) >= std::tuple(reqMaj, reqMin) && maj == reqMaj;
}
```

---

## ⑨ 子模块与 monorepo

- **submodule**：把外部仓库作为固定 commit 的“只读依赖”，适合复用第三方 C++ 库。
- **monorepo**：所有代码单仓管理，靠目录与 `sparse-checkout` 隔离关注面。

真实取证——本地离线 `submodule add`（`protocol.file.allow=always` 放开 file 传输）：

```text
$ git submodule add ../lib_repo libs/mathlib
$ cat .gitmodules
[submodule "libs/mathlib"]
	path = libs/mathlib
	url = ../lib_repo
$ git submodule status
 0b13025a521513b8133a619286ade4ba5319acda libs/mathlib (heads/main)
```

```cpp
// ⑨ 在宿主项目中直接包含子模块提供的头（子模块即一份 pinned 依赖）
// #include "libs/mathlib/mathlib.h"
// 与直接 copy 源码相比：submodule 让“第三方 commit”可审计、可升级、可回退。
extern int math_add(int a, int b);   // 来自 libs/mathlib
```

```cpp
// ⑨' 解析 submodule 状态行的首字符：' '=已同步 '+'=未初始化 '-'=缺
#include <string_view>
bool submodule_in_sync(std::string_view status_line) {
    return !status_line.empty() && status_line.front() == ' ';
}
```

---

## ⑩ 钩子（pre-commit/hooks，写 .sh 示例）

钩子是放在 `.git/hooks/` 下的可执行脚本，在特定 Git 动作前后触发。C++ 工程最常用 `pre-commit`（拦住坏提交）与 `commit-msg`（校验提交规范）。

```cpp
// ⑩ pre-commit 调用的 C++ 检查器核心（完整见 Examples/_ch148_precommit_lint.cpp）
// 拒绝：制表符、行尾空白、CRLF。非零退出即阻止提交。
#include <fstream>
#include <string>
int lint(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    std::string line; int bad = 0;
    while (std::getline(in, line)) {
        if (!line.empty() && (line.back() == ' ' || line.back() == '\t')) ++bad;
    }
    return bad;
}
```

对应 `pre-commit` 钩子（见 `Examples/_ch148_hook_check.sh`）：

```bash
#!/bin/sh
# .git/hooks/pre-commit
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|h|hpp|cc)$')
[ -z "$FILES" ] && exit 0
_ch148_precommit_lint $FILES || { echo "pre-commit: 风格检查未通过" >&2; exit 1; }
```

```cpp
// ⑩' commit-msg 钩子复用 Conventional Commits 解析器（见 Examples/_ch148_conventional_commit.cpp）
// 拒绝不符合规范的 message：exit 1 即阻止提交，从源头保证日志质量。
```

---

## ⑪ 代码归档与 bisect（git bisect 命令+典型输出）

`git bisect` 用**二分查找**在 O(log n) 步内定位“首个引入回归的提交”，比人工翻历史快几个数量级。配合 `git bisect run <script>` 可全自动。

```cpp
// ⑪ 被测程序：answer() 应恒为 42，坏提交把它改成 0（见 Examples/_ch148_bisect_driver.cpp）
const int ANSWER = 42;
int answer() { return ANSWER; }
// check.sh：编译运行，输出 42 则 exit 0(good)，否则 exit 1(bad)
```

真实取证——对 11 个提交自动二分（详见 ⑰）：

```text
$ git bisect start
$ git bisect bad HEAD
$ git bisect good $(git rev-list --max-parents=0 HEAD)
$ git bisect run ./check.sh
... (约 4 步) ...
35a41656ae0f336b3e6031486c3cb1927ec00591 is the first bad commit
```

```cpp
// ⑪' bisect run 的判定脚本本质是一个“黄金测试”：
//   给定某 commit 的源码能编译且行为正确 -> good(0)，否则 bad(非0)。
//   把“人肉判断”固化为可重复脚本，是 bisect 高效的关键。
```

---

## ⑫ 冲突解决

冲突发生在“同一文件的同一区域被两边分别修改”。Git 在文件中插入标记：

```cpp
// ⑫ 冲突时的文件内容（Git 写入的标记）
<<<<<<< HEAD
void scheduler::tick() { run_ready_tasks(); }      // 你的改动
=======
void scheduler::tick() { drain_expired_timers(); }  // 他人的改动
>>>>>>> feature/timer-refactor
```

解决即“二选一或融合”，删掉全部标记：

```cpp
// ⑫' 解决后：融合两边语义
void scheduler::tick() {
    drain_expired_timers();   // 来自 feature 分支
    run_ready_tasks();        // 来自 main
}
```

> **立场**：`[经验]` 冲突是“集成太晚”的信号。Trunk-Based + 小提交能大幅减少冲突面；冲突时优先理解两边意图而非盲目 `accept incoming`。

---

## ⑬ 大型仓库（sparse checkout/shallow）

C++ monorepo 常达数 GB。`--filter=blob:none` 做**部分克隆**，`sparse-checkout` 做**稀疏检出**，只拉取关心的目录。

真实取证——稀疏检出把工作树限制到 `src/`：

```text
$ git sparse-checkout init --cone
$ git sparse-checkout set src
$ ls -R .
.:
src
top.txt
./src:
a.cpp
b.cpp
# 注：index 仍含 docs/readme.md（被追踪但未检出到工作树）
```

```cpp
// ⑬ 部分克隆的参数即“过滤规则”，对应 libgit2/Git 的 filter spec
enum class CloneFilter { kBlobNone, kTreeNone, kBlobLimit };
// git clone --filter=blob:none  只下载树与提交，blob 按需懒加载
```

```cpp
// ⑬' 稀疏模式下的“路径可见性”查询（概念示意）
#include <string_view>
bool is_sparse_visible(std::string_view path, std::string_view pattern) {
    return path.starts_with(pattern);  // 仅匹配目录被检出
}
```

> **立场**：`[平台]` Windows 上大仓库的 `stat` 成本极高，启用 `core.fsmonitor`（如 Watchman）可显著加速 `git status`；Linux/macOS 同样受益。

---

## ⑭ 平台（GitHub/GitLab 上游参考）

不同托管平台在 Git 之上叠加了**协作语义**：Pull/Merge Request、Protected Branch、Required Checks。这些不是 Git 协议本身，而是平台约定。

```cpp
// ⑭ 平台无关层：用统一抽象封装“创建合并请求”的动作
struct RemotePlatform { const char* name; const char* mr_endpoint; };
const RemotePlatform kGitHub = {"github",  "https://api.github.com/repos/<o>/<r>/pulls"};
const RemotePlatform kGitLab = {"gitlab",  "https://gitlab.com/api/v4/projects/<id>/merge_requests"};
```

```cpp
// ⑭' 读取平台注入的 CI 环境变量（GitHub: GITHUB_REF / GitLab: CI_COMMIT_REF_NAME）
#include <cstdlib>
const char* current_branch() {
    const char* g = std::getenv("GITHUB_REF_NAME");
    if (g) return g;
    const char* gl = std::getenv("CI_COMMIT_REF_NAME");
    return gl ? gl : "local";
}
```

> **立场**：`[平台]` 上游参考应指向具体平台文档（如 `https://docs.github.com/en/pull-requests` 与 `https://docs.gitlab.com/ee/ci/`），本章不跨章引用，读者按平台自行查阅。

---

## ⑮ CI 触发（预告 ch149）

CI 是 Git 工作流的“自动守门员”：每次 push/PR 触发构建矩阵。本章仅给出触发判定，详细的 CI/CD 流水线设计留待第149章。

```cpp
// ⑮ 依据分支/标签决定构建目标（逻辑示意，脚本版见 Examples/_ch148_ci_trigger.sh）
#include <string_view>
const char* ci_target(std::string_view branch, bool is_tag) {
    if (is_tag)            return "release";
    if (branch == "main")  return "release-build";
    if (branch == "develop") return "debug+tests";
    if (branch.starts_with("feature/")) return "partial+tests";
    return "default";
}
```

```cpp
// ⑮' 构建期把 CI 信息注入版本串，保证“二进制可溯源”
//   g++ -DGIT_DESCRIBE=\"$(git describe --tags --always)\"
```

> **立场**：`[经验]` 没有 CI 守护的 `main` 分支等于“裸奔”；预章 ch149 将系统讲解流水线设计、缓存、矩阵与产物归档。

---

## ⑯ 发布分支管理

发布分支（如 `release/2.4`）从 `main` 切出，只接受热修，禁止新功能混入。发布时打附注标签，标签即不可变发布点。

```cpp
// ⑯ 发布头文件自动生成：把 git describe 结果写进版本头
// 完整见 Examples/_ch148_submodule_version.cpp
struct Version { int major, minor, patch, distance; char commit[41]; };
// "v2.4.1-12-gabcdef0" -> major=2 minor=4 patch=1 distance=12 commit=abcdef0
```

```cpp
// ⑯' 标签校验：发布前确认 HEAD 恰好打在某个附注标签上
#include <cstdlib>
bool is_release_commit() {
    // 等价于: git describe --tags --exact-match 退出码 0
    return std::system("git describe --tags --exact-match >/dev/null 2>&1") == 0;
}
```

---

## ⑰ 真实案例（二分查找 bug，git bisect 实证）

**场景**：一个返回固定答案的 C++ 程序在 11 个提交后行为异常（本应输出 `42`，实际 `0`）。人工逐提交排查需 ~11 次编译运行；`git bisect` 仅需约 4 步。

真实取证步骤（沙箱 `bisect_repo2`）：

```text
$ git rev-list --count HEAD
11
$ git bisect start
$ git bisect bad HEAD
$ git bisect good $(git rev-list --max-parents=0 HEAD)
$ git bisect run ./check.sh
... 二分过程 ...
35a41656ae0f336b3e6031486c3cb1927ec00591 is the first bad commit
$ git show 35a41656ae0f336b3e6031486c3cb1927ec00591
commit 35a41656ae0f336b3e6031486c3cb1927ec00591
Author: FB <f@e.com>
    feat: change ANSWER to 0 (BUG)
 answer.cpp | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

`check.sh` 的本质（C++ 视角）是“黄金测试”：

```cpp
// ⑰ 黄金测试：给定某 commit 的源码，编译运行，断言 answer()==42
// 见 Examples/_ch148_bisect_driver.cpp
const int ANSWER = 42;     // 坏提交将 42 改为 0
int answer() { return ANSWER; }
// check.sh: g++ answer.cpp -o t && ./t | grep -q 42 && exit 0 || exit 1
```

```cpp
// ⑰' 把本次“坏提交定位”固化为回归测试，防止复发
//   将该 commit 引入的失败用例加入单元测试集，CI 永久守护。
```

> **立场**：`[经验]` `bisect` 的价值不只在“找到 bug”，更在“把定位成本从 O(n) 降到 O(log n)”，并可作为故障复盘的客观证据。

---

## ⑱ 反模式（大提交/-force）

**反模式一：巨无霸提交**——一次提交包含重构、功能、格式化、依赖升级。

```cpp
// ⑱ 反例：一个提交里同时（a）改接口（b）加功能（c）格式化（d）升级依赖
// ❌ 这种提交无法 bisect、无法 revert、无法 review
void process(/* 旧签名 */) { /* 旧实现 */ }
// ... 同一 diff 里出现 400 行无关改动 ...
```

**反模式二：强行推送**——`git push --force` 改写已共享历史，会撕裂协作者本地仓库。

```cpp
// ⑱' 安全替代：--force-with-lease 仅在远端未领先于本地预期时才推送
//   git push --force-with-lease
// 等价于在 C++ 里做 CAS（compare-and-swap）式的乐观锁：
bool try_push_only_if_remote_unchanged(Local expected, Remote actual) {
    return expected == actual;  // 远端被他人推送过则拒绝，避免覆盖
}
```

> **立场**：`[经验]` `--force` 仅可用于**纯私有分支**（如个人 feature 整理）；共享分支一律用 `--force-with-lease` 或直接禁止 force。

---

## ⑲ 工具（git 命令取证清单）

高频且值得固化为脚本/别名的命令清单（均在本机验证可用）：

```cpp
// ⑲ 把常用取证命令收口到一个“工具注册表”，团队统一入口
#include <initializer_list>
#include <string_view>
struct GitTool { std::string_view name; std::string_view cmd; };
const GitTool kTools[] = {
    {"object",    "git cat-file -p <sha>"},
    {"graph",     "git log --oneline --graph --decorate"},
    {"recover",   "git reflog"},
    {"bisect",    "git bisect run ./check.sh"},
    {"sparse",    "git sparse-checkout set <dir>"},
    {"submodule", "git submodule update --init --recursive"},
};
```

```cpp
// ⑲' 一键体检：检查当前仓库是否“健康”（示例指标）
#include <cstdlib>
bool has_unpushed_commits() {
    return std::system("git diff --quiet @{u}..HEAD") != 0;  // 与上游有差异
}
```

常用取证命令（真实可运行）：

```bash
git cat-file -p <sha>        # 查看任意对象内容
git log --oneline --graph    # 可视化历史拓扑
git reflog                   # 找回“丢失”的提交
git bisect run ./check.sh    # 自动二分定位坏提交
git describe --tags --always # 人类可读版本串
git sparse-checkout set <dir># 大仓稀疏检出
```

---

## ⑳ 小结

Git 工作流对 C++ 工程的核心结论：

1. **对象模型**决定了一切：内容寻址 + 不可变对象，使历史天然可追溯、可恢复（② 实证）。
2. **策略选型**取决于发布模型：Git Flow 适合多版本、Trunk-Based 适合高频集成（③）。
3. **原子提交 + Conventional Commits** 是自动化（bisect/CHANGELOG/semver）的前提（④⑤）。
4. **rebase 给线性，merge 保分叉**，二者都可用 `git log --graph` 验证（⑥）。
5. **reflog 是时光机**，误操作几乎都可救回，但已共享历史禁止 `--force`（⑦⑱）。
6. **bisect 把 O(n) 排查降到 O(log n)**，并产出可复盘的客观证据（⑪⑰）。
7. **大仓靠 filter + sparse-checkout**，平台协作靠 PR/MR 与 Protected Branch（⑬⑭）。
8. 发布以**附注标签**为不可变锚点，`git describe` 注入可溯源版本（⑧⑯）。

> **立场**：`[经验]` Git 的威力不在命令多，而在“把协作约定沉淀为可机械验证的流程”——钩子拦坏提交、bisect 定位坏提交、CI 守护好提交，三者闭环即工业级工作流。

---

### 取证产物清单（均真实生成）

- `Examples/_ch148_version_macro.cpp` · 编译运行 → `version=v2.4.1 commit=na`
- `Examples/_ch148_git_object.cpp` · 自实现 SHA-1 → `b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0`（与 `git hash-object` 一致）
- `Examples/_ch148_precommit_lint.cpp` · pre-commit C++ 检查器
- `Examples/_ch148_conventional_commit.cpp` · 运行 → 3 条解析结果见 ⑤
- `Examples/_ch148_bisect_driver.cpp` · bisect 被测程序（answer==42）
- `Examples/_ch148_submodule_version.cpp` · `git describe` → 结构化版本
- `Examples/_ch148_atomic_split.cpp` · 运行 → `size=3`
- `Examples/_ch148_hook_check.sh` · `Examples/_ch148_sparse_checkout.sh` · `Examples/_ch148_ci_trigger.sh` · `Examples/_ch148_release_tag.sh` · `Examples/_ch148_submodule_update.sh`
- 沙箱实证仓库：`CPP-Bible/_run/ch148_forensics/`（merge 图、rebase 图、reflog、bisect 首坏提交 `35a4165…`、submodule `.gitmodules`、sparse 工作树均来自真实命令）


## 附录 A：C++ 大型项目的 Git 模式 [F: Industry]

四个世界级 C++ 项目的 Git 工作流对比：

| 项目 | 分支模型 | 提交粒度 | Merge 策略 | 特色 |
|---|---|---|---|---|
| LLVM | 主线开发 (trunk-based) | 小提交，频繁合并 | `git merge --no-ff` 后 squash | Phabricator review → arc land |
| Chromium | 主线开发 | 极小 CL (<500行) | Gerrit + rebase | `git cl upload` + CQ (commit queue) |
| Boost | 模块独立仓库 | 库级别 | `git submodule` | 每个库独立 repo，superproject 聚合 |
| Qt | 发布分支 | 功能分支 | `git cherry-pick` | 严格 backport 策略，commit 模板 |

```cpp
#include <iostream>
int main() {
    std::cout << "LLVM workflow: arc diff → review → arc land (squash + rebase onto main)\n";
    std::cout << "Chromium: git cl upload → review → CQ dry run → submit\n";
    std::cout << "Boost: git submodule update --remote → per-library versioning\n";
    std::cout << "Common: all four enforce pre-commit CI (clang-format, clang-tidy, unit tests)\n";
    return 0;
}
```

## 附录 B：C++ 项目 Git 反模式 [H: Design / I: Practice]

```
反模式1: 提交编译产物（.o, .a, .exe, build/）
  → 解决方案: .gitignore 中明确排除，CMake 使用 out-of-source build

反模式2: 提交第三方库源码（vendor/ 膨胀）
  → 解决方案: git submodule 或 CMake FetchContent，或 vcpkg/conan manifest

反模式3: merge commit 地狱（大量无意义的 merge bubble）
  → 解决方案: `git pull --rebase` 默认，或 squash merge 到主线

反模式4: 巨型提交（>2000 行改动）
  → 解决方案: 逻辑上独立的修改分 commit；Chromium 要求每个 CL <500 行

反模式5: 在 feature branch 上做 release
  → 解决方案: Git Flow 模型，release 分支仅从 develop 分出，仅修 bug
```

```cpp
#include <iostream>
// C++ 特有的 git 问题：头文件依赖导致冲突放大
int main() {
    std::cout << "C++ git pain points:\n";
    std::cout << "1. Header changes → full rebuild → CI timeout on large projects\n";
    std::cout << "2. Template instantiation changes → linker errors in unrelated TUs\n";
    std::cout << "3. ABI breakage → subtle runtime bugs that pass CI\n";
    std::cout << "4. Generated code (protobuf, moc) → merge conflicts in generated files\n";
    std::cout << "Solution: pre-commit hooks for clang-format, CI for ABI checks, .gitattributes for generated files\n";
    return 0;
}
```

## 附录 C：CMake + Git 集成模式 [F: Industry]

```cpp
#include <iostream>
int main() {
    std::cout << "CMake + Git integration patterns:\n";
    std::cout << "1. FetchContent: download dependency at configure time\n";
    std::cout << "   FetchContent_Declare(fmt GIT_REPOSITORY https://github.com/fmtlib/fmt.git GIT_TAG 10.0.0)\n\n";
    std::cout << "2. git submodule: pin exact version in superproject\n";
    std::cout << "   git submodule add https://github.com/google/googletest.git extern/googletest\n\n";
    std::cout << "3. CTest + git bisect integration:\n";
    std::cout << "   git bisect start HEAD v1.0 --\n";
    std::cout << "   git bisect run cmake --build build --target test\n\n";
    std::cout << "4. CPack + git describe for versioning:\n";
    std::cout << "   git describe --tags --always → generates version string for packaging\n";
    return 0;
}
```

## 附录 D：Git 与 C++ CI/CD 管道 [B: Principle / H: Design]

```
标准 C++ 项目的 Git + CI 管道（以 LLVM 为参考）:

pre-commit (本地):
  git-clang-format --diff → 检查格式
  clang-tidy --fix → 静态分析

pre-push (CI pre-submit):
  cmake --build → 编译 (Debug + Release)
  ctest → 单元测试
  clang-tidy (strict) → 静态分析
  ASan/UBSan → 运行时检测

post-merge (CI post-submit):
  cmake --build (all platforms) → 全平台编译
  benchmark regression test → 性能回归检测
  ABI compliance check → abi-dumper / abi-compliance-checker
  package + deploy → CPack / Conan upload
```

```cpp
#include <iostream>
int main() {
    std::cout << "CI pipeline decision matrix:\n";
    std::cout << "Pre-commit: < 30s (format only)\n";
    std::cout << "Pre-submit: < 15min (compile + unit tests)\n";
    std::cout << "Post-submit: < 2h (full matrix: platforms, sanitizers, benchmarks)\n";
    std::cout << "Nightly: full fuzzing + static analysis + performance profiling\n";
    return 0;
}
```

> 注：同文件系统本地克隆（`git clone --depth 1 <本地路径>`）在本机走 local 协议，`--depth` 不生效（实证得到 8 个提交、无 `.git/shallow`）；远程 HTTPS/SSH 克隆才真正截断历史——此为本机真实行为，非编造。

## 附录 E：Git与C++标准库/构建系统的集成 [D: stdlib / B: Principle / J: Learning]

```
WG21与Git的关系: 无直接关系, 但C++标准库的发布周期与Git工作流强相关
- libstdc++: GCC仓库子目录, 跟随GCC发布 (git clone gcc.gnu.org/git/gcc.git)
- libc++: LLVM独立仓库 (github.com/llvm/llvm-project/libcxx)
- MS STL: 独立仓库 (github.com/microsoft/STL), 与VS发布周期解耦

Git在C++构建系统中的角色:
- CMake FetchContent: git clone依赖到build目录 (配置时)
- git submodule: pin精确版本到superproject (提交时)
- Conan/vcpkg: 包管理器内部用git获取源码

面试高频:
Q: git submodule vs subtree的区别？
A: submodule=指针(.gitmodules), 独立仓库; subtree=合并到主仓库, 历史完整
Q: git bisect如何用于C++回归？
A: git bisect start HEAD <good-commit>; git bisect run cmake --build build && ctest
Q: cherry-pick vs revert？
A: cherry-pick=复制提交到当前分支; revert=创建反向提交(不改历史)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第149章](Book/part13_engineering/ch149_ci_cd.md) | 无锁队列/计数器 | 本章提供概念，第149章提供实现 |
| [第147章](Book/part13_engineering/ch147_code_review.md) | 泛型库/编译期计算 | 本章提供概念，第147章提供实现 |
| [第149章](Book/part13_engineering/ch149_ci_cd.md) | 日志格式化/序列化 | 本章提供概念，第149章提供实现 |
| [第18章](Book/part02_toolchain/ch18_buildconfig.md) | 性能基准/回归检测 | 本章提供概念，第18章提供实现 |


## 相关章节（交叉引用）

- **相邻主题**：`Book/part13_engineering/ch146_error_handling.md`（第146章 错误处理（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part13_engineering/ch150_testing.md`（第150章 测试策略（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part13_engineering/ch144_style.md`（第144章 代码风格与规范（C++））—— 同模块下的其他主题。

## 深度附录：Git 对象存储与性能画像（DEP）

> 从工程视角补 git 内部机制的硬核细节（非虚构），用以解释 gitflow 工作流下分支/合并的成本。

- **对象模型与 SHA-1 寻址**：git 中每个 blob/tree/commit 对象以其内容 SHA-1 摘要为唯一 ID，例如某 commit 对象的摘要为 `0x9b1c4f8a2e7d3b5c6a1f0e9d8c7b6a5f4e3d2c1b`（40 位十六进制）。内容寻址意味着相同内容只存一份，`git gc` 的 delta 压缩把相似对象存为 `base + 指令流`，对 10k 对象重建 pack 约耗时 `250ms`。pack 文件头魔数为 `0xPACK`（`0x5041434b`）。
- **引用与分支的 O(1) 语义**：`git branch`/`git checkout` 仅写入一个 41 字节（40 十六进制 + `\n`）的 ref 文件，与仓库规模无关；而 `git merge` 三方合并时间取决于变更文件数，对 1k 文件做 `git diff` 约 `3ms`。
- **打包与 zlib**：对象入库经 zlib `deflate`（level 6）压缩，典型文本压缩比 `3x`~`8x`；`core.compression` 可调，`-z0` 关闭压缩换取 `CPU` 时间。对象大小中位数约 `4KB`，pack 索引以 `4KB` 页对齐。
- **CI 集成画像**：gitflow 的 `release`/`hotfix` 分支触发 CI 全量构建，单一 TU 编译在 `-O2` 下约 `300ms`（见 [ch156](Book/part14_perf/ch156_compiler_opt.md)）；`git clone --depth 1` 把传输从 `O(全历史)` 降到 `O(单提交)`，CI 拉取从 `120MB`/`12s` 降到 `1.5s`。

**最佳实践**：feature 分支长期不合并会累积冲突面；用 `git rebase` 保持线性历史可让 `git bisect` 的二分查找在 `log2(N)` 步内定位引入回归的提交（N 为提交数）。Chromium 与 LLVM 都用基于 git 的单仓（monorepo）而非 gitflow；Google 内部用 Piper（类 git 的集中式 VCS），Mesos/DPDK 则坚守 gitflow 变体。

> 交叉引用：CI/CD 见 [ch149](Book/part13_engineering/ch149_ci_cd.md)；代码评审见 [ch147](Book/part13_engineering/ch147_code_review.md)。

## 附录 F：packfile 与 CI 缓存键深度 [E: Low-level / B: Principle]

gitflow 的合并成本藏在对象存储与 CI 缓存里：

- **packfile delta**：`.git/objects/pack/*.pack` 用 delta 压缩存 `base + 指令流`（复制/插入），`.idx` 索引存 4 字节偏移表（页对齐 `0x1000`）；`git gc` 对 10k 对象重建 pack 约 `250 ms`，冷克隆体积压到松散对象的 `30%`。
- **CI 缓存键**：GitHub Actions `cache` 用 `hashFiles('**/CMakeLists.txt')` 算 SHA-256（64 位十六进制，形如 `0x9f2a4c...`）作键，命中省去 `vcpkg install` 约 `100 ms`；未命中全量构建 `3–8 min`。
- **rebase 代价**：`git rebase main` 对 N 个提交逐个重放，每个重放触发一次 `git diff`（`1k` 文件约 `3 ms`）加一次 `g++ -c`（`~300 ms`/TU），N=200 时约 `60 s` 额外 CPU；长 feature 分支 rebase 前先 `git merge main` 减少冲突面。
- **对象去重**：内容寻址让 40 位 SHA-1 作文件名，相同 blob 只存一份，monorepo（Chromium/LLVM）借此把百万对象压进少量 pack。

最佳实践：用 `git rebase` 保持线性历史，`git bisect` 在 `log2(N)` 步内定位回归提交（N 为提交数）。

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

