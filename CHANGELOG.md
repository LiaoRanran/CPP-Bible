# Changelog

本项目遵循"竣工即记"原则，按日期记录里程碑。版本号语义见 [`RELEASE.md`](RELEASE.md)。

---

### 2026-09-04（续五）ch32 初始化 真机实证深耕（L2 主线）
- **病灶**：ch32 总 59 cpp 块、1570 行，散文密度 75.1%（骨架不贫血），但 **10 个块把散文/跨语言对比/面试题塞进 `std::cout`**（赝品，如 `cout<<"Trap 1: ..."`、`cout<<"Q1: ... 答: ..."`、编造汇编 `cout<<"Assembly (GCC -O2): brace = movaps..."`）。另 #59 玩具块打印一句英文建议。
- **选章依据（避开 prose_density 误伤）**：用 `cout<<"` 玩具代码扫描（ch32=96 处，全库最高之一）定位真稀薄，而非按密度升序（ch71/ch70/ch19 曾误伤深章）。
- **真机取证**（GCC 15.3.0，Examples/_ch32_init.cpp）：`vector(10,2)`=10 元素 vs `vector{10,2}`=2 元素、成员初始化顺序 UB（a 读到未初始化栈）、返回 initializer_list 悬垂（size=3 底层数组已销毁）、brace≈assign（2.335/2.327 ns/op，生成等价代码）、静态零初始化 vs `value{}` 均全 0。
- **修复**：10 块伪代码 → 真机实证（陷阱4/5 补可编译代码、性能块删编造汇编改真机计时、FAQ/法则/面试题文字移正文）；#59 玩具块 → 值初始化演示。cpp 块数不变（7534），节号不动。
- **验证**：ch32 全部 59 块 main-only 编译 0 失败；全量 compile gate **PASS（0 regression）**、exempt_audit PASS；whitespace 0 / gen_metrics ✅ / consistency 100/100。

### 2026-09-04（续四）CI 编译门禁 regression 清零（19 → 0）
- **根因**：CI compile job 用 `--changed` 增量门禁；题注铺开改动覆盖全库 → 回退全量重编 →
  历史既存失败一次性暴露为 19 个 REGRESSION（run #522 红）。非内容新增 bug，是覆盖面扩大。
- **分诊**：16 处骨架体 `{ // …` 未闭合（ch70 同型：`{ /* … */ }` 修法）+ 3 处真 bug——
  ch41 示例62 缺 `#include <memory>`、ch25 示例5 非法伪析构 `u.s.~basic_string()`
  （改 `u.s.std::string::~string()`）、ch123 示例15 条件误写 `c<'0' || c<'0'`（改 `c<'0' || c>'9'`）。
- **验证（本地确定性复现）**：`compile_all --main-only --parallel` → 失败块 80→**61**（全豁免
  覆盖）→ `compile_gate.py` **PASS（0 regression）** → `exempt_audit.py --check` **PASS**。
  文档三道门禁：whitespace 0 / gen_metrics ✅ / consistency 100/100。
- 台账：PROGRESS 6.3 追加、新增 7.6（CI 编译门禁机制 + 本地复现链路 + 块号口径坑）。

### 2026-09-04（续三）围栏配对错位修复（10 章 11 处）+ 题注迁移全库铺开（7309 块）
- **围栏配对错位修复**：10 章 11 处「关闭围栏被写成 `​```text`」（CommonMark 关闭围栏禁止
  info string）→ 渲染层与工具层双错位（前块吞题注行、真裸围栏与后续 cpp 块被吞、门禁覆盖缺失）。
  22 处围栏行修复（错位关闭→裸 ```；错位裸开→`​```text`），扫描器全书 0 错位 / 0 裸围栏。
- **指标回归真相**：`cpp_blocks` 7527 → **7534**（7 个被错位吞掉的 cpp 块恢复独立身份；7527 系
  错位假象，README 已同步）。ch01 52/0、ch07 42/0 全绿（新增门禁覆盖块全过编译）。
- **曝光既存问题（非本次引入，待分诊）**：ch28 5 fail = 全部故意错例（UB 章「编译失败示例」）；
  ch50 13→17 / ch51 4→8（块边界正常化曝光，跨块片段类）；part13/15 首次纳入门禁视野：
  ch145 30（跨块为主，疑真截断候选 #7/#25/#43/#64）、ch147 10、ch163 3。
- **题注迁移全库铺开**：`--titles` 覆盖 147 章，**7309 个 cpp 围栏**加 `title="示例 N · ★…☆"`
  （正文题注行保留）；miss 47 处（题注后隔叙述 / 缺难度星级）保守跳过。全库 96.9% 命中。
- **工具加固**：`codeblock_style.py` stdout GBK 控制台崩溃防护（`reconfigure utf-8`）。
- 门禁：whitespace 0 / gen_metrics ✅ / consistency 100/100；台账 PROGRESS 6.1–6.3 / 7.3–7.5。

### 2026-09-04（续二）围栏题注迁移试点（3 章 184 块）+ 1 处真截断
- **试点 3 章**（全绿章 ch22/ch24/ch70，跨 part03/part06）：围栏加 `title="示例 N · ★…☆"`，
  正文题注行保留（badge/主题/版本标注仍在正文渲染）。命中率 184/188，miss 保守跳过。
- **工具修复 3 处**：`--titles` 难度捕获 `\S+`→`[★☆]+`（原会把 `]`/`</span>` 吃进 title）；
  `example_exercise_audit.py` / `normalize_comments.py` 的 `fence_lang` 取首 token（防带 title
  的块被漏计/漏处理）。
- **全链路验证**：三道门禁全绿、cpp_blocks 7527 不漂、3 章编译保持全绿、exercise_dup_guard
  614 块正常、站点 `superfences`+`attr_list` 已启用。
- **连带修复真截断**：ch24 块 #33 `struct Packet { … // …` 缺 `};` → 补闭合，57/0。
  既存问题（HEAD 同样 fail），PROGRESS 6.1 基线系 07-11 快照。
- 台账：PROGRESS 6.3 / 7.4 已更新。

### 2026-09-04（续）版式铺开剩余 12 part + 修工具 bug
- `codeblock_style.py` **修 CRLF 行尾 bug**：原 `split("\n")` 残留 `\r` 再 `replace("\n"→"\r\n")`
  污染 CRLF 文件为 `\r\r\n`（whitespace 报 W2、gen_metrics 假值）；改 `splitlines()` + `newline.join`。
- 版式铺开剩余 12 part（part01/02/03/04/05/07/08/09/10/13/15/16，共 107 章）：标签 228 + 对齐 3849；
  29 处代码性裸围栏人工定点 `text`。从 HEAD 还原 12 part 后修复版重做，全门禁恢复
  whitespace 0 / consistency 100/100 / cpp_blocks=7527 / d5_coverage=127。README 7534→7527。
- 教训：批量 `--apply` 后必跑 whitespace+gen_metrics+consistency 三道门禁。

## [Unreleased] - 2026-09-04

本轮主线：**代码块版式统一落 4 章 + 围栏题注规则的解析器硬化**（TEACHING §8 四规则标准定稿）；附带扫清 REAL 桶 6 章 11 块真缺陷。

### 代码块版式工具与标准（用户拍板：范围 = 标准 + 4 章试改）
- **新工具 `tools/codeblock_style.py`**（字节级读写保留 CRLF/LF，护栏防误伤）：
  - ① 围栏语言标签统一 + 裸围栏内容信号推断（含「有 `;{}` 却信号不足 → 交人工不误标」保险）；
  - ② 行尾注释对齐：按显示宽度（CJK=2）对齐到「最长代码行 + 2」，超 76 列整块跳过；护栏覆盖整行注释 / doxygen / URL / 字符串内 `//`；
  - ③ 围栏题注 `--titles`（默认关闭）；`--list-bare` 列出裸围栏供人工定标签。
- **试改 4 章**（ch125/ch127/ch133/ch154）：标签 7 处、行尾注释对齐 76 处（diff 83+/83- 纯重排零增删）。编译门禁 ch125 45/0、ch154 41/0、ch127 45/0 无回归；`whitespace 0`、`gen_metrics ✅`（cpp_blocks 未漂移）、`consistency 100/100`。
- **标准定稿**：TEACHING.md §8 扩为四规则——① 围栏标签（含同义标签归一表）② 注释写法（含新增「行尾注释对齐」机械规则）③ 围栏题注目标规范（注明迁移前置条件已满足、迁移方式、全库 147 章按章推进不铺开）④ 反模式清单更新（不手敲对齐列）。

### 围栏解析器硬化（题注前置，防"假全绿"）
- 全部 `^```cpp\s*$` 精确匹配与 `findall("```cpp(.*?)```")` 解析器改为接受围栏信息串并跳过信息串行：`chapter_compile_check.py` / `chapter_lint.py` / `compile_run_sanitize_pipeline.py` / `run_cpp_assertions.py`（导入共享常量自动跟随）/ `verify_exercises.py` / `exercise_dup_guard.py`。

### REAL 桶 6 章 11 块真缺陷（ch51/ch68/ch96/ch101/ch127）
- ch51 8→4：`enable_shared_from_this` 原理块补 `std::` 限定 + `<memory>`；`MatrixBase/Matrix` 补 const 重载与类体闭合；logging 幻影 helper 补定义；运行时选择 `cond?` 顶层语句改 `make(bool)`。
- ch68 3→1：integer_sequence 顶层调用入 main（真机 `sum=10`）；ECS `TypeList` 全幻影名 → 自包含定义 + `static_assert` 成立。
- ch96 7→5：中位数练习补初值 + main，且修正 A/B 两法下标不一致（统一上中位数 `a[n/2]`，真机 `medA=medB=5`）；top-k 用法演绎补 `read_million` 桩 + main。
- ch101 10→7：六类思想总览顶层声明入 main（含递归 lambda 只能在函数内）；两处 STL 衔接片段入 main 并加输出（真机 `9 1`、`find=7 first=7`）。
- ch127 1→0：`AddExpr` 结构体截断补 `};`。

### part14_perf 全 7 章版式铺开（同批相邻章，低风险）
- `codeblock_style.py --apply` 覆盖 ch152/153/155/156/157/158（ch154 已先行）：标签 1 + 对齐 64 +
  人工定点 2 处裸围栏标 `text`（chrono 头文件摘录、SIMD 决策树）。diff 67+/67- 纯重排零增删。
- 编译门禁新增 5 全绿：**ch152 39/0、ch153 39/0、ch155 50/0、ch157 50/0、ch158 42/0**
  （ch156 6 处为既存跨块片段/顶层 if/链接错，非本次引入）。`whitespace 0`、`gen_metrics ✅`。
- 全绿章累计 **21 章**。

### 第三方命名空间 SKIP 决策落地 + 版式铺开 part06/part12
- 门禁新增 `EXTERNAL_NS_RE`（boost/absl/spdlog/rocksdb/leveldb/folly/llvm/clang/glog/gflags/fmt::，
  匹配前剔除纯注释行）：part11 台账 ch128 19→1、ch130 11→2、ch131 13→2、ch132 42→10，
  ch126/ch127 保持 0。原则：第三方生态库代码展示超出本工具链作用域（同 Qt/gtest 先例）。
- `codeblock_style.py` 安全升级：**绝不自动判 `cpp`**（裸围栏自动 cpp 会漂移 cpp_blocks 并把源码
  摘录送进门禁）+ text 信号集（Q:/A:/面试/提案号/ASCII）。
- 版式铺开 part06（13 章）+ part12（9 章）：标签 54（全部 text）+ 对齐 479；part06 已知 8 章基线
  逐字一致（ch61 23/ch62 0/ch63 1/ch67 2/ch68 1/ch70 0/ch71 5/ch72 18 → 0 回归）；
  `gen_metrics ✅`、`whitespace 0`。累计版式已覆盖 part11/14/06/12 + 4 试改章（共 31 章）。

### part11 源码摘录结构截断修复 6 块
- 修 6 块并真机复核：ch124[57] move 构造未闭合、ch128[57] 参数表被 `// s` 吞、ch132[81] main 缺 `}`、
  ch133[9] Arena if 体未闭合、ch133[10] RedisConn ctor lambda 未闭合、ch134[17] FString8 解码循环
  未闭合、ch134[31] BeginPlay 缺闭合。削减：ch124 2→1、ch128 20→19、ch132 43→42、ch133 17→15、
  ch134 13→11。真机：`4` / rc=0 / `5`。余留为第三方生态域（库未装），"第三方命名空间 SKIP"留专项。

### part11_source 全 11 章版式铺开（用户选"第一条"）
- `codeblock_style.py --apply` 覆盖 part11 全部章：标签 13（全为裸→`text`，含 3 处人工定点 Q&A
  面试文本）+ 对齐 171。diff 241+/241- 纯重排零增删；`whitespace 0`、`gen_metrics ✅`、
  `consistency 100/100`。
- **part11 编译台账首次建档**：ch126 **57/0** 全绿（对齐回归对照组）。其余章为第三方生态源码章
  （boost/absl/spdlog/rocksdb/leveldb/Qt/Unreal 域），失败多为库未安装的"未声明"——超本门禁
  工具链作用域（同 Qt/gtest 先例），另藏匿若干源码摘录结构截断候选（ch124[57]/ch128[57]/
  ch132[81]/ch133[9][10]/ch134[17][31]），留待"第三方命名空间 SKIP + 摘录结构修复"专项。
- 全绿章累计 **22 章**。

## [Unreleased] - 2026-09-03

本轮主线：**全书 cpp 代码块可编译性攻坚**（门禁规则完善 → 整章清扫 → 散点清扫 → 小推进），另有真机纠偏两处。

### 编译门禁规则完善（`tools/chapter_compile_check.py`）
- 新增 7 类 SKIP（与既有 fmt / benchmark / POSIX / module 同族，判定原则统一为「只对本可在宿主工具链独立编译的块判失败」）：① 本地自写头 `#include "..."`（跨块复用 / 包消费演示）② 外部框架（Qt / sqlite3 / gtest / doctest / gmock / Catch2）③ `namespace std` 扩展（特化须在全局作用域）④ `std::` 模板全特化（同 formatter）⑤ libstdc++ 源码摘录（首行 `bits/…` 头路径注释）⑥ 顶层 namespace 回指 `::X`（全局限定名教学）⑦ newlib / `_sbrk` / `_ebss` / picolibc 裸机运行桩（并入 BAREMETAL）。
- `<experimental/scope>` 列入保留头（须全局作用域，ch39 TS `scope_exit` 示例依赖）。
- 前提：GBK 解码修复后门禁首次具备「看见全部含中文诊断的失败块」的能力，本日清扫全部建立在此之上。

### ch70 标签分发整章清扫（48 blocks → 0 fail）
- 12 块同源缺陷：函数体写成 `{ // 整型路径` **括号从不闭合**（后续 `template<>` 被吞进函数体，报 `template declaration at block scope`）；`if constexpr` 骨架语法残；跨块标签类型；调用语句散在命名空间作用域。读者复制必编译失败。
- 修法：骨架体统一闭合为 `{ /* 原注释语义 */ }`；示例 5/25/26 的顶层调用语句入 `main` 并补最小真定义；示例 14/15 补自包含标签结构。围栏数未增删（README `cpp_blocks` 不漂移）。
- 真机验证：示例 5 打印 `random_access: O(1) 路径`（最具体匹配）、示例 25 `integral 路径`、示例 26 `strong(random_access) 被选中`。

### REAL 桶散点清扫（两批 18 章全扫分诊）
- **批 1（ch13/16/17/20/23/24/39/42/50）**：ch13 2→**0**、ch16 4→**0**、ch17 1→**0**、ch24 3→**0**、ch42 1→**0**；ch20 7→5、ch23 3→1、ch39 9→1、ch50 17→13。
- **批 2（ch51/61/68/71/72/81/96/100/101）**：分诊完毕。保留类不予修改——ch61 以**故意二义性错例**（`call of overloaded … is ambiguous`）为主，ch100/ch101/ch72 为「循环体 / 调用体散命名空间 + 类型跨块」的片段式教学。真截断清单锁定：ch51 [3/10/28]、ch81 [11/25]、ch68 [6/19]、ch71 [24/32]、ch96 [40]、ch101 [0]。
- **小推进**：ch71 7→5（补 `SafeQueue` / `Guarded` 两处类体截断）、ch81 3→1（补 `string_view` 遍历与反向遍历两处闭合）；真机输出 `hello world / hello world / hello`、`olleh`。
- 累计：本日新达全绿章 **13 章**（ch13/16/17/24/42/62/70 + 早前 ch22/30/31/40/45/46）。

### 真机纠偏（本日两处，均写回正文）
- **C++23 P2266 抓现行**：`std::string& f(){ std::string s = …; return s; }` 在 `-std=c++23` 下**直接编译错误**（返回语句的局部变量按右值处理，无法绑定非 const 左值引用）；`-std=c++20` 仅 `-Wreturn-local-addr` 警告。ch20 示例 17 改为「注释演示反模式 + 保留 ✅ 版本」，并把这一标准代差写进块内注释。
- **`float` 的 `has_unique_object_representations` 本机 = 0**：原 ch42 示例 38 注释称「int/float 通常为 1」，实测 `int=1 / float=0 / pad=0`（浮点属实现定义），注释已改为实测值。

## [Unreleased] - 2026-09-02

本轮主线：**30 章真深耕启动**（叙述密度治理定调）；另有早前批次 Part0 前置篇收官、TEACHING 三气质样板、CI site 修复（见下）。

### 30 章真深耕启动（诊断 → 样板 → 清污 → 落档）
- **定调**：外部锐评 + 本仓诊断共识——停止「形式完备」推进，转入「少而准」：30 章真深耕。
  量化证据：全书纯叙述约 32%（全行口径）/ 正文行口径 65.5%，最贫血 20 章平均 48.9%。
- **工具**：`tools/prose_density.py` 叙述密度测量（全书/单章 + 最贫血排名，`--top N`）。
- **样板章验收**：ch22 auto/decltype 字段卡→因果叙述，密度 52.4%→**65.5%**；随行清编造编译器符号、
  围栏误闭合、徽章前缀。范式四要点（因果叙述/清编造/实证锚定/格式随行）实战验证。
- **标题截断污染清零**：全书 536 处示例标题生成期截断（未闭合括号/断词/悬挂标点），
  `tools/caption_truncation_audit.py` 三级置信度修复 535 + 人工重建 1，全量清零并进 preflight 门禁防回归。
- **落档**：30 章名单（A 机制 12 / B 性能并发 8 / C 源码精读 5 / D 教学骨干 5）+ 单章验收五条 +
  节奏红线（串行/小批量，禁一波流）→ `CONTENT_DEPTH_ROADMAP.md`「当前主线」节 + `NEXT_LLM.md` SOP-5。

### Part0 前置篇收官（asm A1–A6 + C C1–C9）
- 新增 C4 函数与栈帧、C5 指针与内存、C6 结构体与内存布局、C7 预处理、C8 标准库、C9 互操作六章，
  全部为 GCC 15.3 真机证据（`objdump -d -M intel` / `gcc -std=c11` 编译运行），与 C1–C3 同体例。
  Part0 独立于主书 147 章门禁，不参与主书统计。

### TEACHING.md 铺开：三气质样板（3 批共 9 章，稀疏推进）
- 按「历史 / 工程 / 悬疑」三种气质各挑样章贴 1 个显式盒子定调，每批 3 章、**保持稀疏不齐刷刷**
  （守红线：宁 30 章有，不可 147 章齐刷刷）：
  - 第一批：ch01（历史注脚·零开销原则的源头）/ ch77（迭代器失效）/ ch28（返回局部引用被编译器蒸发）。
  - 第二批：ch04（C++11 的技术债清算）/ ch81（c_str() 悬垂）/ ch27（strict aliasing UB）。
  - 第三批：ch03（C++98 整库采纳 STL 的代价）/ ch76（sort 比较器须严格弱序）/ ch20（vector<bool> 返回 proxy 而非 bool&）。

### CI site job 修复（长期红灯已转绿）
- **`site` job「health audit」失败根因**：`docs/references/book_items/effective-modern-cpp-items.md`
  的通用 lambda 示例未加反引号，`[](auto x)` 被 Markdown 解析成空链接 `<a href="auto x">`，
  `site_audit` 检查 3 视为站内资源 → 文件不存在 → exit 1（7 个 failure run 的共同根因）。修复：反引号包裹。
- **本地假红根因**：`rewrite_links` 收集顶层 `docs` 后整目录复制，把 gitignored 的
  `docs/references/external/` 素材一并带进 nav，导致本地 `mkdocs build --strict` 断链、
  `site_audit` 报 10715 处缺失。修复：新增 `_gitignored_dirs()`，按 `.gitignore` 剔除忽略目录（外部 md 51→29）。
- 复验：run #473 八个 job 全绿，`Site front-end health audit` 由 failure 转 success，
  `deploy` 由长期 skipped 转 success，GitHub Pages 部署恢复。

---

## [Unreleased] - 2026-09-01

内容侧「学习目标 → 问题驱动论证」打磨专项 **60 章全面收官**；本轮另修掉两处真实缺陷（站点欢迎页 part 表标题全空、README 数字与事实源漂移）。

### 内容打磨：① 学习目标 → ① 我们真正要回答的问题（60 章收官）

- **范式**：把「① 学习目标」的纯罗列清单，改写为「① 我们真正要回答的问题」论证式导读——每条先立判断再给论据，逐条回指正文节号（均核证属实），保留前向导航链接与示例代码。
- **批次（10 批）**：`fd6897a` ch121 试点 → `bc4fd45` 历史 9 章 → `e2ffc76` OO 6 章 → `dc8ed07` STL/现代 4 章 → `65b3bf1` STL 容器 4 章 → `f80c7cd` 模板 12 章 → `5cf5362` STL 板块 10 章 → `957870a` 语言 5 章 → `008c265` 现代 4 章 → `c246651` 性能 3 章 → `c53848b` 收尾 ch31（运算符重载）+ ch109（内存屏障与 fence）。
- **收尾两章的六问**（回指节号逐条核证）：ch31 讲成员/非成员的两条硬判据、`operator<<` 为何不能是成员、前后置 `++` 的哑元与拷贝代价、C++20 `<=>` 与 rewrite candidates、不该重载的运算符与零开销实证（附录 I ABI）、隐式转换与自赋值两类高发缺陷；ch109 讲 fence 与逐操作 `memory_order` 的判据、栅栏必须成对且位置夹准、「x86 上 fence 免费」的陷阱（附录 J 真机：`acq/rel/acq_rel` 编译为空、`seq_cst` 落 `lock or` 而非 `mfence`）、附录 D5 实测的非显然结论（`relaxed store + fence(seq_cst)` 8.2× 比 `seq_cst store` 17.3× 便宜约一半）、`consume` 与 `signal_fence` 两个边角、滥用 `seq_cst` 的代价由弱内存架构付。
- **内容准确性修正（禁虚构红线）**：ch85 原声称「C++20 透明哈希」——透明哈希对 unordered 容器并未进入标准库，已改诚实表述；ch83 消除反引号内 `Book/` 前缀；ch80 的 ⑨ 节回指由错误的「栈布局」修正为「调用栈/时序图」；ch76:1311 过时回指「见 ① 学习目标」随改名同步更新。

### 缺陷修复（本轮）

- **站点欢迎页 part 表标题全空（`d0d5dda`）**：`DEFAULT_PART_TITLES`（16 条中文 part 标题）注释写明「INDEX.md 未提供 `## Part N:` 时启用」，但 `parse_part_titles()` 从不回落它——兜底是定义了却没接上的死代码。本站点的 `INDEX.md` 是项目文档索引而非章节总目，通篇无 `Part` 字样，故解析恒为空。因 `build_nav()` 自带兜底而 `build_part_table()` 没有，只有欢迎页退化成空白列。改根因：`parse_part_titles()` 以该字典为初值、INDEX.md 解析结果覆盖其上。重生成后日志 `part 16`、16 行标题全部填充。
- **README 数字漂移**：`README:5` 写死 `7531` 个 cpp 块，事实源实测 `7525`（CI 硬门禁 `gen_metrics.py --check` 项），已回填。

### UNVERIFIED 章审计收口（8 章）

- **ch05（C++14）翻转为 `[VERIFIED]`**：§⑩「C++14 零新增运行时开销」补真实汇编证据——新增 `_asm_demo/ch05_generic_lambda.cpp` 及权威 GCC 15.3.0 编译产物 `_o0.s`（泛型 lambda 实例化为两个独立符号 `_ZZ11use_genericvENKUlT_E_clIiEEDaS_` / `clIdEEDaS_`）与 `_o2.s`（实例全部内联/常量折叠为 `mov eax, 19`，零 call），章内 asm 围栏为真实节选；`book_asm_freshness` 复验 0 漂移。验证横幅现状 73 章（66 VERIFIED / 7 UNVERIFIED）。
- **其余 7 章（ch02/16/132/148/149/150/165）审计结论：UNVERIFIED 依红线保留**——逐章正则扫描具体数字/基准词候选并人工复核，均为组织史实、外部工具（IDE/git/ccache/RocksDB）经验值或已显式标注「示意，非本机实测」的内容，无机器可验断言，不可为指标伪造证据链。逐章结论落档 `HANDOVER.md`「UNVERIFIED 章审计结论」。

### 工具链类型化（mypy 清零，60→0）

- 用 `uvx mypy tools/`（110 文件）逐文件清除真实类型债务；**60 错误 → 0（`Success: no issues found in 110 source files`，仅 1 条 `annotation-unchecked` 信息提示非错误）**。
- 修复类别（均为真实债务，非 `# noqa` 豁免）：`var-annotated`/`list-item`/`dict-item`（共 ~30 处纯注解，零运行时风险）、`union-attr`（4 处 `.group()` 绑定后判空）、`no-any-return`/`return-value`（5+5 处 str()/bytes() 包裹与 `run_site`/`run_pdf` 返回类型补 `-> list`）、`attr-defined`（`consistency_check` 的 `Sequence[str]`→`list[str]`、compile_p0 文件句柄被循环变量遮蔽重命名 `f`→`fh`）。
- mypy 已接入 CI（`quality` job 硬门禁，钉版 2.3.1，配置走 pyproject `[tool.mypy]`，无 `# noqa` 豁免）；CI 钉版 ruff 0.6.9 仍全绿，本批改动引入 0 个新 lint。

### 工具链类型检查固化进 CI（mypy 硬门禁）

- 在 `ci.yml` 的 `quality` job 紧接 Ruff 之后新增 `Mypy` 步骤：钉版 `mypy==2.3.1`，跑 `mypy tools/`（读 pyproject `[tool.mypy]`：`python_version=3.11` / `warn_return_any` / `warn_unused_configs`）。
- 原 Ruff 注释里「mypy 暂不接入——接入必红，留给下一批」已作废（triage 已完成，60→0）。
- CI 跑在 Linux；已排查 `tools/` 无 Windows-only 标准库导入（`msvcrt`/`winreg` 等），与本机 Windows 解析一致，不会跨平台误红。
- 收益：固化 60→0 的类型清洁度，未来任一处重新引入类型债务即 BLOCK，防回归。

### 门禁复验

- `cppbible.py check --stage quality`：**17/17** 全绿。
- `consistency_check.py`：147 章 ERROR=0 WARN=0（100/100）。
- `gen_metrics.py --check`：文档数字与事实源全部一致。
- `ruff 0.6.9 check tools/`：All checks passed。
- 推送 preflight：**7/7** 通过（`65b3bf1..d0d5dda master -> master`）。

---

## [Unreleased] - 2026-08-31

全量「类比（analogy）」补写收官里程碑。将 analogy 教学标记从 75/147 补齐至 147/147，写作质量三件套（one_liner / pitfall / analogy）全部满标。

### 类比补写（part06→16 再 part01→05，共 72 章）
- 每章在「史料来源」锚点后注入 `!!! note "类比：…"`，含 2 个独立映射（类比 / 好比 / 类似于）+ `> 失效边界` 引用块，遵循 `docs/content_writing_analysis.md` §7 rubric。
- 逐档提交并推送，每档 `cppbible.py check --stage quality` 16/16 全绿、`whitespace_fix.py --apply` 零缺陷：
  part13(`92d7f13`) / part14(`fc42b92`) / part15(`d17900a`) / part16(`68061b5`) / part01(`6e0990a`) / part02(`f911423`) / part03(`33b79c5`) / part04(`bc70270`) / part05(`9035522`)。

---

## [Unreleased] - 2026-08-30

全量仓库审计 + 治理加固里程碑。交付 `REPOSITORY_AUDIT_AND_ROADMAP_2026-08-30.md` 与仓库外备份，并修复一批门禁/工具缺陷。已分主题提交并推送远端（至 `4c5cb32`），CI 远端验收中。

### 备份与恢复验证

- 仓库外全量备份至 `C:\RepositoryBackups\CPP-Bible\20260830-090558`（工作树 tar.zst + Git bundle + SHA-256）。
- 验证通过：归档与 bundle SHA-256 复算一致、全量恢复文件/目录差异 0、恢复仓库 `git fsck` 退出 0、`git bundle verify` 通过、ACL 已隔离（关闭继承）。
- 已知残留：备份与源同机同盘（`C:`），第二故障域需加密外置介质/对象存储。

### 质量与工具修复

- **章节口径统一（P0）**：`compile_all.py`、`density_audit.py` 曾把 `Book/` 下全部 Markdown 当章节（151），`consistency_check.py` 把 `assets/history/MANIFEST.md` 当章节；三工具统一只扫描 `chNN_*.md`，章节数固定 147。密度审计修正为 147 章均分 25.7/30，一致性 WARN 33→30（索引文件不再计数）。
- **legacy 审计工具修复（P1）**：`audit_py_tools.py` / `audit_cpp_defects.py` / `chapter_number_audit.py` 根路径改为按 `__file__` 推导，输出写入正确目录；扫描集合为空时退出码 2（原静默假绿 0）。已在任意 cwd 与空仓库副本验证。
- **Windows 中文控制台编码修复**：`xref_check.py` 打印 `⟶` 抛 `UnicodeEncodeError`、`cppbible.py` 按 GBK 解码子进程 UTF-8 输出导致日志线程崩溃——均已统一为 UTF-8 输出/解码。Linux CI 无影响；本机 quality 现可完整复现跑通。
- **内容修复**：清理 11 个章节 12 处 W2 连续空行（`whitespace_fix --apply`）；修复 `ch92_chrono.md:147` 无连线的 Mermaid 图块（补语义边）；`fix_ch36.py` 语法错误修正（仅 `py_compile` 验证，未执行）。
- **CI 发布依赖图（工作树，待远端验收）**：`site/pdf/epub` 由 `needs: quality` 改为 `needs: [compile, publish-check]`；`deploy` 由 `needs: site` 改为 `needs: [site, pdf, epub]`。依据：GitHub Actions `#373` 实测 deploy 于 10:08 完成而 GCC 编译 10:38 才完成，且 EPUB 失败仍发布，证明原依赖可绕过编译。

- **度量指标口径修正（15 条验收标准 · 教学标记）**：`tools/metrics_snapshot.py` 原用 `text.count(单一字面量)` 按「总出现次数」对目标，导致两类失真：①只认一种写法（如只数「一句话结论」，漏掉「一句话总结」等别名）；②按总次数而非「章覆盖」计（一章写 10 处陷阱就顶 10 章，147 目标会在 15 章即「达标」，掩盖其余章无内容）。现改为每标记 `(多写法正则, 每章门槛)` 结构，新增「达标章数」口径（`teaching_markers_chapters`）作为看板真正度量：`one_liner/pitfall` 目标 147=全章覆盖、每章 ≥1；`analogy` 目标 147=每章 ≥2。修正后实测：`pitfall 147/147`（每章都讲坑）、`one_liner 16/147`（仅 16 章有结论标签，真实缺口）、`analogy 1/147`（近乎无类比，最强短板）。`build/metrics.json`（gitignored）由 `main()` 自动再生。

### 门禁复验结果

- `cppbible.py check --stage quality`：16/16 全绿（审计初 15/16）。
- `cppbible.py check --stage compile`：5/5 全绿（Compile All / Compile Gate / Exempt Audit / D5 Compile Gate / Assertions）。
- Mermaid 静态校验 511/511（审计初 1 处错误）。

### 升级与优化（阶段 A：工具链 · 合规 · 规范 · 环境）

- 新增《[UPGRADE_PLAN_2026-08-30.md](UPGRADE_PLAN_2026-08-30.md)》全面升级方案：7 目标现状-差距-行动矩阵、ABCD 四阶段、资源需求清单。
- **许可（已裁决 MIT）**：新增 `LICENSE`（MIT）；README 许可行由 CC BY-NC-SA 修正为 MIT，消除与 pyproject 的冲突。
- **依赖锁定（已选 uv）**：生成 `uv.lock`（解析 45 包）；`tools/bootstrap.ps1` 改 uv 优先（回退 pip）；新增 `.env.example` 与 `SECURITY.md`。
- **CI 工具链升级**：全部 actions 升级到最新主版本（checkout/setup-python@v7、upload-artifact@v7、upload-pages-artifact@v5、deploy-pages@v5），消除 Node20 弃用告警。
- **规范流程**：新增 `.github/PULL_REQUEST_TEMPLATE.md`（含门禁自检清单）与 `.github/ISSUE_TEMPLATE/`（bug / 内容勘误）；新增 `.pre-commit-config.yaml`（trailing-whitespace、ruff、mypy）。
- 用户裁决：UI 深度「先搞内容」，阶段 C 调整为内容深化与质量收口。

### 工具栈升级 + 门禁 + 前端工具（2026-08-30 追加）

- **依赖锁定（uv）**：全部依赖升级到最新并写入 `uv.lock`（mkdocs-material 9.7.7、ruff 0.16.5、mypy 2.3.1、mkdocs-mermaid2-plugin 1.2.3、pagefind 1.5.2、pypandoc 1.17）；导出 `requirements.lock.txt`（hash 校验），CI `site` job 改为锁定安装。
- **CI actions 再升级**：site/pdf/epub/publish-check/deploy 等全部升级到最新主版本（checkout/setup-python@v7、upload-artifact@v7、upload-pages-artifact@v5、deploy-pages@v5）。
- **新门禁 `cppbible env`**：工具链自检（Python/GCC 15.3.0/objdump/c++filt/uv/git + 锁文件存在性），缺失或版本不符即非零；已接入 bootstrap 第 4 步。
- **前端工具 `tools/site_audit.py`**：站点产物健康自检（首页/章节页可达/静态资源完整性/徽章注入/Mermaid/pagefind），已接入 CI `site` job（构建后、上传前阻断）；附最小 fixture 自测（GOOD=PASS、BAD=FAIL）。
- **内容债任务单**：[docs/references/content_debt_tasklist.md](docs/references/content_debt_tasklist.md) —— 55 处悬空章号引用（按语义建议映射）、7 处前置问题（6 倒置 + 1 悬空）、30 一致性 WARN 执行顺序。

### 内容债清零（2026-08-30 完成）

- **55 处悬空章号引用全部清零**：ch33→ch28、ch34→ch40、ch54/56→ch49、ch59→ch60、ch73→ch51、ch75→ch67（映射）；ch74/ch114/ch102-105 无对应现章，按语义改写至 ch123/ch113/ch93/ch107。20 章节共 89± 行修改，权威映射见 [docs/references/chapter_mapping.md](docs/references/chapter_mapping.md)。
- **7 处前置问题清零**：悬空前置 ch114→ch113；6 处历史/导读章前瞻引用列入 `FORWARD_PRE_EXEMPT` 白名单（作者设计意图，逐项注释依据）。
- **30 处一致性 WARN 清零（根因为工具误报）**：L1 徽章化迁移后 `consistency_check` 仍只认字面 `[标准]` 括号，对 30 个仅用徽章 span 的章误报；新增 `STANCE_BADGE_RE` 兼容两种载体后 `ERROR=0 / WARN=0`（恢复 100/100 基线）。抽样验证（ch04/ch22/ch60/ch165：徽章 52-99、字面 0）确认为规则过时而非内容缺失。
- **门禁转硬 + 两项健壮性修复**：`dangling_ref_linter` / `prereq_topo_check` 由软转硬；修复 `--json` 输出目录不存在时崩溃（CI 干净 checkout 无 outputs/ 抛 FileNotFoundError，曾致 #375 误红——本地 pass/CI fail 的根因）；已全库排查其余写 JSON 工具均带 mkdir，无同类隐患。
- 复验：`quality` 16/16、`dangling=0`、`topology=0`、consistency `ERROR=0 / WARN=0`。

### D5 覆盖口径统一（2026-08-30 完成）

- **根因**：`d5_gap_scanner` 用正文「附录 D5」字面量匹配（=113），`metrics_snapshot` 用标题正则 `^#{2,4}\s*D5\b`（=119）；实测 6 章（ch05/ch11/ch15/ch128/ch146/ch151）标题为 `## D5 真实性能基准：…`/`## D5 性能附录：…` 变体，被字面量口径漏判。
- **修复**：两工具统一为 `^#{2,4}\s*(?:附录\s*)?D5\b` 标题正则（`D5_HEADING_RE`），口径收口为 **119/147（81%）**；该指标在 metrics 中为非阻塞 dashboard，无 CI 影响。
- 复验：quality 16/16 保持全绿。

### 事实源同步（2026-08-30 完成）

- **STATE/ISSUES/README 三文件接入单一事实源**：README 头部数字更新为 metrics 派生值（23.7 万行 / 7530 cpp / 密度 25.7 / D5 119）；STATE.json 刷新 last_commit=4c5cb32、density 24.9→25.7、新增 d5_coverage/mermaid/cpp/lines 指标与 `fact_source` 声明；ISSUES.md 10 项逐条复核——9 项已解决（附证据：ch121 cpp=50、ch122 cpp=45 双门禁 0 fail、ch118 945 行、ch81 1175 行、crossref 0 断链、GCC 硬编码已清），仅 #9 部分遗留（ch01/02/08/09/10 fragment 待批），并新增 2026-08-30 口径遗留清单。
- **UPGRADE_PLAN 状态同步**：D5 口径统一、deploy 依赖解锁两项 P1 标记完成；阶段 A+ CI 远端验收标记进行中。

### CI site/epub 失败修复（2026-08-30）

- **site job「Install MkDocs stack (locked)」必红**：`requirements.lock.txt` 含 uv export 默认注入的 `-e .`（editable），pip 在带 `--hash` 的锁文件中处于哈希校验模式，与 editable 安装不兼容（本地 `pip install --dry-run` 复现同一报错）。修复：改用 `uv export --no-emit-project` 重新导出（site job 仅用独立 tools 脚本与 mkdocs/pagefind CLI，不依赖项目包安装，移除 `-e .` 无副作用）；ci.yml 内生成命令注释同步。
- **site job「Site front-end health audit」误报（本地复现定位）**：`site_audit.py` 三处误报——(1) `Path(base)/"/绝对路径"` 会丢弃 base 从盘根解析，404.html 的 `/Appendix/ub/` 等 174 个绝对目录链接全部误判缺失；(2) ch61 Mermaid 内联 SVG 文本含字面 `<a href="x">` 被当资源引用；(3) `/.`（主题 logo 根链接）与 `/pagefind/*`（索引产物由检查 6 专责）。修复后本地全站 1595 个资源引用全通过，fixture 自测维持 GOOD=PASS/BAD=FAIL。
- **epub job「Generate EPUB」步骤被 cancelled → 根因 OOM（WSL 7.4GB 复现实测）**：全书 `combined.md` 已增至 **13MB**（14.7万行→23.7万行时代翻倍），单本 pandoc `--split-level=1` 峰值内存 >7GB，在 CI（7GB runner）与 WSL（7.4GB）上均被 OOM Killer 杀死——runner 检测到 shell 进程消失将步骤误标为 cancelled 而非 failure（4/4 复现、心跳防御无效的原因：整个进程组连心跳 bash 一起被杀）。旧 `book.epub`（6.1MB，8/11）为书体量翻倍前的产物，run #373 起 epub 实际持续失败。修复：`generate_epub.sh` 新增 `--by-part` 分册模式（与 pdf job 对称，复用 `rewrite_links` API 按 part 切分），本地 WSL 16 册全部生成成功（44K-882K/册）；CI 改用分册 + `if: always()` 上传生成日志 artifact；EPUB rights 元数据 CC BY-NC-SA → MIT（与 LICENSE 裁决一致）。随 `b90fa5d` 远端复验。

### 现状与遗留

- **CI 全链路首次真绿（`b90fa5d`，run 33304567016）**：quality / Compile(GCC-15) / Compile(Clang-19) / publish-check / site / pdf / epub / deploy 八 job 全部 success。自 #373 起的「deploy 绕过编译失败发布」P0 风险彻底闭环；epub 自 #373 起的静默失败同步修复。
- 内容债已清零（55 悬空 + 7 前置 + 30 WARN + D5 口径）+ 事实源冲突已同步；仍遗留：分支保护未启用、断言 55 WARN、ch01/02/08/09/10 cpp 完整化、legacy 候选人工复核、第二故障域备份（需介质），详见审计报告 §7/§8/§10。

---

## [1.1.0] - 2026-07-15

第三阶段"质量收尾 + 高含金量升级"首个发布。在 1.0.0 全绿基线上，追加实测/工程价值内容，并修复一处编译器特性支持的事实性错误。

### 新增（高含金量）

- **性能数据实测化（P0-1）**：ch27/ch50/ch93 关键数据点由 `[示意]` 升级为 GCC 15.3.0 本机 `[实测]`——多继承 vptr 布局（主 `0x0`/次 `0x8`/槽宽 `0x8`）、同步代价（atomic 3.5ns / mutex 7.6ns / thread 125µs）、转型代价（virtual 0.5ns / dynamic_cast 6.9ns，慢 13.6×）。测量程序落 `_emp_bench/`。
- **编译器版本矩阵（P0-2）**：新增 `docs/compiler-matrix.md`（GCC 列本机实测，Clang/MSVC 标 `[DOC]`）+ 验证工具 `tools/verify_compiler_features.py`，正文引用统一指向本表，禁止在正文写死三编译器版本号。
- **UB / Sanitizer 反例库（P0-3）**：`Appendix/ub/` 15 例（内存 5 + 并发 5 + 生命周期 5），每例配真实 ASan/TSan/UBSan 输出与修复。
- **WG21 提案跟踪表（B3）**：新增 `WG21/TRACKER.md`（C++20/23/26 提案 → feature-test 宏 → 三编译器支持）+ `tools/generate_wg21_tracker.py`（解析并对比本机探测基线出 diff）。
- **面试题嵌入式分类（B2）**：`Interview/` 拆 `general/`（20 题 + 难度分级 + 🔧 嵌入相关标注）+ `embedded/`（E1-E10 STM32F4 硬核题：无堆容器 / 跨 TU ABI / volatile MMIO / 中断安全 / placement new / 内存池 / DMA 抽象 / 零开销寄存器映射 / 全局构造顺序）。
- **汇编实证扩展（B4，累计 8→12 例）**：ch42/48/52/117 各加「附录 E 编译实证」，全部 GCC 15.3 `-O2` objdump 真实生成——
  - ch42 严格别名：翻转 `-fstrict-aliasing` 开关的生成码分歧（缓存返回值 vs 重载内存）；
  - ch48 RTTI：`typeid` 读 `vtable[-1]` 的 `type_info`、`dynamic_cast` 尾调 `__dynamic_cast`；
  - ch52 EBO：空基类偏移 0 vs 空成员偏移 4（sizeof 4 vs 8 汇编可见）；
  - ch117 复制消除：prvalue 直接写返回槽零 copy/move 调用，删 move 仍编译。

### 修复（事实性）

- **deducing this 特性支持误判**（重大）：1.0.0 期间 P0-2 误用不存在的宏名 `__cpp_deducing_this` / `__cpp_explicit_this`（均探测为 UNDEF），错误结论"GCC 15.3 不支持 deducing this"。本机 `-dM` 实探证明正确宏名 `__cpp_explicit_this_parameter` = 202110 **已支持**。全链修正 5 处：`WG21/TRACKER.md`、`docs/compiler-matrix.md`、`_cpp_probe_gcc.json`、`tools/verify_compiler_features.py`、`Book/…/ch10_version_matrix.md`。
- 附带修正：`__cpp_lib_flat_map` = 202207（已支持）、`std::mdspan` / `inplace_vector` 确为 UNDEF、P2300 `std::execution` 宏尚未定名（并澄清 `__cpp_lib_execution` = 201902 是 C++17 并行算法，与 P2300 无关）。

### 质量审计（A 系）

- **交叉引用审计（A1）**：`tools/crossref_audit.py` 实跑 147 章 / 1190 引用 / 断链 0 / part 覆盖率 100%。
- **CI 豁免消化（A2）**：定向重测 66 个豁免块（GCC 13.1，CI 同款 flags）全部合法失败（modules / 外部库 / POSIX / MSVC / 多文件 / 故意错误演示），0 stale；新增防呆工具 `tools/prune_exempt.py`。全量 `--main-only` 复扫：147 章 / 112 通过 / 66 失败块与基线一致。

### 一致性审计（C 系）

- **术语一致性（C1）**：修复索引层 32 处断链引用——`GLOSSARY.md`（ABI/CRTP/data race/deadlock/EBO/UB/vtable 共 7 条）、`CROSSREF.md`（生命周期/虚函数链/协程链/CRTP 链 4 条核心链）、`MISCONCEPTIONS.md`（章节区间头 + 条目章号共 21 处）全部映射到真实章号；`glossary.json` 129 术语 0 断链；术语变体审计（运行期/运行时/范本/解构/指标/多形/内连）确认均为有意用法，0 实际错误。
- **Mermaid 图表审计（C2）**：新增 `tools/mermaid_audit.py`（静态结构校验）+ `tools/mermaid_parse_check.mjs`（官方 `mermaid.parse` + jsdom 真实解析）；全量 88 图块静态 + 官方解析双重校验 0 失败。
- **章编号一致性（C3）**：新增 `tools/chapter_number_audit.py`——校验文件名 `chNN` ↔ H1 `第NN章`、序列连续性、重号、part 区间重叠、mkdocs nav 悬空引用；147 章 0 错、18 个缺号确认为有意预留（33/34/53-59/73-75/102-106/114）。

### 质量基线（不变）

- `consistency_check.py` 147 章 ERROR=0 / WARN=0；CI 编译门禁保持全绿。

---

## [1.0.0] - 2026-07-14

首个可发布快照。147 章全部竣工，质量门禁"本地 + CI"双向全绿。

### 发布质量基线

- **规模**：147 章 / 16 part / 约 14.7 万行 / 6840 个可编译 cpp 块
- **密度审计 v3**：均分 **24.2/30**，浅章（<15 分）**0** 个 —— 密度深化封顶，主线转向质量收尾
- **一致性**：`consistency_check.py` ERROR=0 / WARN=0
- **交叉引用**：0 断链
- **断言**：编译期 + 运行期断言全 PASS

### 2026-07-14 加固（相对 07-13 候选）

- **CI 编译门禁上线**：`compile_all.py --main-only` → `compile_gate.py`（双层豁免：显式清单 + 错误模式）。
  新真实 `SYNTAX` / `TYPE_MISMATCH` 错误一旦引入，CI 立即变红。
- **跨平台回归修复**（本地 mingw 软过、Linux gcc13 暴露）：
  - `ch30` 补 `<csignal>`（`sig_atomic_t`，Linux gcc 不隐式带）
  - `ch35` / `ch36` 补 `<cstdint>`（`uintptr_t`）
  - `ch62` `W<int>` 成员 `double` → `char`（LP64 下 `static_assert` 失败，LLP64 巧合掩盖）
  - 门禁 WINDOWS 模式补 `winsock2.h | ws2tcpip.h`
- **EPUB 去封面**：移除 `--epub-cover-image` 与 `assets/cover.png`（独立作品，无外部封面依赖）；
  EPUB / PDF 构建经 CI 实证干净。
- **豁免清单元数据化**：`compile_exempt.json` 由 `gen_compile_exempt.py` 从审计报告生成，
  66 块 **0 UNCLASSIFIED**。

### 已知设计性豁免（非 bug）

多文件示例、C++20 Modules（`import std;` 需 MSVC 17.5+ / Clang 18+，GCC / MinGW 诚实豁免）、
POSIX / Windows 专用 API、外部库、故意展示的错误 / UB、跨块依赖 —— 详见 `tools/compile_exempt.json`。

---

## [1.0.0-rc] - 2026-07-12 / 07-13

初版竣工候选（详见 [`RELEASE.md`](RELEASE.md)）：

- 清理 311 个 `.bak` 与 6 个临时探针
- 去重审计清零（DUP%=0.0 / WTR%=0.00）
- 单章 lint GPA 98.7（A=146）
- 本地门禁全绿，待 CI 实跑确认
