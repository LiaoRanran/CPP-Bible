# 533 · V-iso 施工规格（阴阳同构可落地版 · 实测 + 自攻）

> 投喂轮次：第三轮（做实轮）。上游：`533_…投喂词.md`、`_arch_v2/03_下一代架构蓝图.md`、`_arch_v2/04_蓝图自我对抗.md`、530 T4。
> 纪律：只读正式仓库；全部产出落 `_arch_v2_round2/`；不 commit/push/accept。
> 标签约定：【实测】=本轮沙箱真跑数字；【推断】=由实测外推但未直接验证；【待实验】=还没跑。

---

## 0. 开头一句话（实做后回答，不是理论风险）

**V-iso 最可能塌的一步不是 diff 判据、也不是翻转检测，而是"写阴面前先把 claim 拆成 anchor（机制所在函数）/remove（被删机制行）/retain（claim 主体支架）三要素"——这一步本质是逼 Writer 把自然语言 claim 重写成可干预的因果陈述；强卡（FENCE）五分钟写出，弱卡会在这一步批量卡住，表现为 `negative_control_diff` 高拒收率。** 我实做时当场绊到两个具体的：①旗舰样板卡 FENCE-001 的真阴面**只翻转汇编区间断言、stdout 一个键都不变**——蓝图 v1 原话"读数翻转（run_match key 变化）"根本表达不了这张卡的阴面，v1 必须把探针扩到 artifact 区间计数通道；②阳夹具字节复制、同编译器同 flags，产物 sha 仍不同（仅 `.file` 基名一行差异），坐实"阴面永不锚 sha"。

---

## 1. FENCE-001 阴面实测证据（任务 2，全部数字来自实跑）

### 1.1 复现方法（任何人可重跑）

```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.\.venv\Scripts\python.exe _arch_v2_round2\probe_fence_iso\run_probe.py
```

- 编译器：`tools/toolchain.resolve_gpp()` → `C:\Qt\Tools\mingw1530_64\bin\g++.exe`（GCC 15.3.0 MinGW-w64，与卡 `artifact_compiler` 一致）；PATH 上的裸 g++ 是 13.1.0，未使用。
- 阳面：正式夹具 `Examples/atoms/_atom_fence_vs_atomic.cpp` 字节复制到沙箱 `probe_fence_iso/yang.cpp`。
- 阴面与全部攻击样本：由 `run_probe.py` 对阳面做**带前置断言的程序变换**生成（夹具漂移即 AssertionError，不静默写错）。
- 原始读数：`probe_fence_iso/probe_report.json`。

### 1.2 编译/运行命令与耗时【实测】

| 对象 | 编译命令（均在沙箱目录，-o 指向 build/ 临时名） | 退出码 | 耗时（3 次中位） |
|---|---|---|---|
| 阳面 asm | `g++ -std=c++23 -O2 -S -masm=intel yang.cpp -o build/yang.s` | 0 | **0.0807s** |
| 阳面 exe | `g++ -std=c++23 -O2 yang.cpp -o build/yang.exe` | 0 | 0.200s |
| 阳面运行 | `build/yang.exe` | 0 | 0.079s |
| 真阴面 asm | 同上，源换 `yin_del_fence.cpp` | 0 | 0.0788s |
| 真阴面 exe | 同上 | 0 | 0.1999s |
| 真阴面运行 | 同上 | 0 | 0.0767s |

- EV-CONC-001 官方 replay 现状（`--card … --no-sanitizer`，连跑 3 次）：**0.832 / 0.709 / 0.703s，confirm**（含 3 条卡命令 + P0-A 独立重编译）。
- 单条阴面 asm 编译边际成本（5 次中位）：**+0.0875s**；若走 exe+run 通道：**+0.2602s（编译）+0.08s（运行）**。
- 全量 56 卡 replay（`--no-sanitizer`，2026-09-15 本机）：**136.7s，confirm=56/refute=0/infra=0**。

### 1.3 真阴面长什么样（unified diff，全文）

```diff
--- yang.cpp
+++ yin_del_fence.cpp
@@ -107,3 +107,2 @@
     while (!s_sf_b) {
-        __atomic_signal_fence(__ATOMIC_SEQ_CST);
     }
```

恰好删 1 行：`spin_signal_fence` 循环体内的零指令屏障。同文件 `writer_signal_fence` 里有**同一行文本**——变换按 anchor 函数区间定点删除（见 §2.2 算法），证明定位不能靠文本替换。

### 1.4 翻转实测【实测，核心证据】

探针 = 卡上既有断言的符号区间计数（复用 `_symbol_body`，区间语义与 `contains_in/absent_in` 完全相同）：

| 探针（`_Z17spin_signal_fencev` 区间内计数） | 阳面 | 真阴面 | 翻转 |
|---|---|---|---|
| `s_sf_b` 出现次数 | 2 | **0** | ✅ 标志读连同循环被消除 |
| `je` 出现次数 | 1 | **0** | ✅ 循环回边消失 |
| `lock` 出现次数 | 0 | 0 | （活性对照，不要求翻转） |

- **run_match 三个键（`spin_plain_ret` / `spin_fence_outside_ret` / `functions_present`）翻转数 = 0，stdout 与 `.out` 逐字相同。**
- 即：**"破坏充分"在 artifact 通道成立（2/2 个机制探针全翻），在 run 通道不成立（0/3）**。原因卡里自己写了：`set_all_flags(1)` 先置位，循环体从未执行，返回值 `s_sf_a` 与屏障无关。这不是失败，是这张卡的 claim 边界（结构证据，非运行时行为）。
- 阳面 `build/yang.s` 的 sha256 = `fcdbd3f6…`，与卡值 `8dd19bc6…` 不同；逐行 diff 全库**仅一行差异**：`.file "yang.cpp"` vs `.file "_atom_fence_vs_atomic.cpp"`。⇒ 阴面/沙箱产物**不得锚 sha**（蓝图原则，现在有了实测理由），探针只做符号区间读数。

### 1.5 这个机制真有运行时后果吗？（诊断，不是候选阴面）

为排除"删了 fence 其实什么都没影响"的尴尬，另做一对**双改动点**诊断夹具（在置位后加 `s_sf_b = 0;`，属第二改动点，故不参评阴面）：

| 诊断夹具 | 结果【实测】 |
|---|---|
| `diag_yang_hang`（阳面 + 标志保持 0） | 运行 >4s 被超时杀掉，无 stdout（循环保留→真自旋挂死） |
| `diag_yin_hang`（阴面 + 标志保持 0） | **0.144s 正常返回**，stdout 与阳面正常运行逐字一致 |

⇒ 删屏障确实把"可能永久阻塞的循环"变成"立即返回"，机制有真实运行时后果；但观测它必须同时改测试支架（第二变量），**单变量 run 通道阴面对该 claim 结构性不可构造**（判据见 §2.4 与 §3.5）。

### 1.6 诚实结论

FENCE-001 prop-1 的阴面**破坏充分**，但充分性体现在编译器产物层，不是程序输出层。V-iso v1 必须支持两条确定性通道（artifact 区间计数 / run 键值），且探针必须绑定卡上**既有**的 claim 锚点；只认 stdout 翻转的 V-iso 会把全库最强的一类 observation（13 张 asm 卡）整体挡在门外。

---

## 2. V-iso 可施工精确规格（任务 1，苦力照做级）

### 2.1 证据卡 frontmatter：`negative_controls:` 精确 schema

**位置**：证据卡顶层（与 `artifact_assert` 同级）。**缺省 = 字段整体缺失**：replay/gate 行为与现状逐字一致（迁移期零影响）；一旦写出，内部任何字段不合规即 fail-closed `refute:negative_control_bad_schema`（沿用 W2"安全设施不许猜"原则）。

v1 书写格式约束（**已用仓库零依赖解析器实测**，见 §5.1 探针文件；不符则解析即被截断，必须钉死）：列表用 block 风格、每项一个 **block map**（`- id:` 起头、后续字段同缩进）；`retain` 用单行 flow list（`[a, b]`，与现有 `evidence: [...]` 同形态）；`probe` 用**单行** flow map；标量单行。**禁止 flow map 跨行**（实测：`- {id: …,` 跨多行时 `parse_frontmatter` 会把整项截成首行字符串，静默失效），禁止嵌套 block map / 多行标量。

```yaml
negative_controls:
  - id: nc1
    variant: v1
    mutation: delete_mechanism
    fixture: Examples/atoms/_atom_fence_vs_atomic.nc1.cpp
    anchor: spin_signal_fence
    remove: "__atomic_signal_fence(__ATOMIC_SEQ_CST);"
    retain: ["while (!s_sf_b)", "return s_sf_a;"]
    probe: {channel: artifact, symbol: _Z17spin_signal_fencev, text: "s_sf_b", op: becomes_absent}
    note: "删体内零指令屏障→循环被整段消除（EV-CONC-001 实测 s_sf_b 2→0, je 1→0）"
```

字段表（每个字段写死）：

| 字段 | 类型 | 必填 | 默认/缺失行为 | 机器校验（不合规即 bad_schema，除注明外） |
|---|---|---|---|---|
| `id` | 标量 | 是 | — | 正则 `^[a-z0-9][a-z0-9_-]{0,31}$`；卡内唯一；日志/毒样例用它定位 |
| `variant` | 枚举 | 是 | — | v1 仅允许 `v1`；见到 `v2` 或其它值 → bad_schema（v2 未实现不许预写） |
| `mutation` | 枚举 | 是 | — | v1 仅允许 `delete_mechanism`（纯删除形态，理由 §2.2/§3.1） |
| `fixture` | posix 相对路径 | 是 | — | ① 在 ROOT 下且文件存在（不存在→`negative_control_missing`）；② 后缀 `.cpp/.cc/.cxx`；③ 命名规约：阳夹具同目录、主干名 + `.nc<id>` + 后缀（v1 不符只 warn，收集 1 批后升 block）；④ 不许指向阳夹具自身或 `build/` 内 |
| `anchor` | 标识符 | 是 | — | 正则 `^[A-Za-z_][A-Za-z0-9_]{0,63}$`；阳夹具中按 §2.2 算法定位函数定义，**匹配数必须恰为 1**（0→找不到，>1→重名歧义，均拒收，不猜第一个） |
| `remove` | 非空字符串 | 是 | — | 去空白后长度 1..120；必须是某个**被删除代码行**的子串（`remove_hit=false` 即 diff 判据不过，不是 schema 错） |
| `retain` | flow list，1..6 项 | 是 | — | 每项去空白长度 1..80；阴面全文必须**逐字包含**每一项（缺一→diff 判据不过）。语义=claim 主体支架，防"连主体带机制一起删"（实测攻击 A4，§3.1） |
| `probe` | 单个 flow map | 是 | — | 恰好 1 个；字段见下三通道表；多写/少写通道字段 → bad_schema |
| `note` | 标量 | 否 | 空 | 长度 ≤200，只给人看，不参与任何判定（禁止把判定语义藏进自然语言） |

`probe` 三通道（v1 只开前两个；第三个 v1 显式拒收）：

| channel | 必填字段 | 取值/校验 | 翻转算子 `op` |
|---|---|---|---|
| `artifact` | `symbol`、`text`、`op` | `symbol` 须为 Itanium 修饰名且通过 `_Z<len><anchor>` 嵌入校验（§2.2，无需 demangler）；`text` 复用现有非空+非样板检查（`_is_boilerplate_text` 命中即 bad_schema）；区间切分复用 `_symbol_body`，阴面产物中符号缺失 = 计数 `None`（fail-closed，不当 0 混过） | `changes` / `decreases` / `increases` / `becomes_absent`（阴=0 且阳>0）/ `becomes_present`（阳=0 阴>0） |
| `run_key` | `key`、`op` | `key` 必须已在卡 `actual.run_match_keys` 声明（旧形态卡须在任一 `actual.run_*` 的逐字行中可解析），**且 key 字符串须包含 anchor 标识符子串**（FENCE 三个键均不含 `spin_signal_fence` ⇒ 该卡此通道机器上不可用，正是 §1.6 的结构化信号）；键值按现有 `partition("=")` 提取 | `changes`（值不同）/ `becomes_absent`（阳面有键、阴面键缺失） |
| `run_rc` | — | — | **v1 显式不开放**：写了即 bad_schema。崩溃冒充（除零/空指针）无法机器绑定到机制，蓝图 04-C1c 的 half-credit 留 v2（须配 crash_signature + sanitizer 复编） |

**v1 边界为什么这么划**：①只许纯删除 mutation——任何"改 1 行"攻击物理上都含插入行（§3.1 实测），delete-only 把一整类攻击移出可信计算基；②只开确定性读数通道——计时/统计、崩溃类探针在 v1 不可复算，开了就是新的恒真判据；③replace 型机制破坏（`atomic<int>`→`int` 涉及声明点+使用点等多处）需要多点替换白名单与 AST 级 diff，列入 v2，v1 不为它放宽单点阈值。

### 2.2 阴面最小 diff 机器判据（硬护栏：算法 + 阈值 + 实测校准）

原型已沙箱实现：`_arch_v2_round2/iso_judge.py`（纯标准库，约 150 行，施工时进 `tools/viso_diff.py`）。

**算法（对阳面/阴面源码文本，顺序执行）**：

1. **归一化**：CRLF/CR→LF；分别准备物理行序列与 token 序列。token = 注释剥离（`/* */` 与行尾 `//`）后，字符串/字符字面量整体一个 token，标识符/数字/其余非空白各一个（正则 `"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[A-Za-z_]\w*|\d+(?:\.\d+)?|\S`）。
2. **行级变更组**：`difflib.SequenceMatcher(autojunk=False)` 取 opcodes，非 equal 组间隔 ≤3 相等行则并组（hunk）；统计：`hunks`、`inserted_lines`（A）、`deleted_lines`，删除行再分为代码行/纯注释行/空行。
3. **token 级变动量**：对两 token 序列做 SM，统计非 equal 段 token 总数 `tokens_changed` 与 `token_change_ratio = tokens_changed / len(阳面 tokens)`。**token 变动为 0 = 零语义 diff**（注释/空白/缩进走私），直接拒。
4. **anchor 定位**：在阳面找 `\b<anchor>\s*\(`；从 `(` 配平括号，`)` 后先遇 `{` 判为定义、先遇 `;` 判为调用；定义数必须恰为 1。从定义后第一个 `{` 起做花括号配平（不处理字符串内花括号，命中即按拒处理并计入误伤统计——v1 夹具均为房屋风格简单自由函数），得函数体行区间 `[head, end)`。
5. **覆盖率**：被删代码行号落在 anchor 区间内的比例 `anchor_coverage`。
6. **remove/retain 核对**：至少一条被删代码行含 `remove` 文本；阴面全文逐字包含每一条 `retain`。
7. **符号同源**：artifact 通道校验 Itanium 嵌入：`_Z(\d+)([A-Za-z0-9_]+)` 取出长度前缀，名前 n 字符须恰为 anchor。
8. **破坏充分性不在本函数判**：由 §2.3 replay 实编译/实跑后比对探针读数——Writer 自说"破坏了机制"不算数。

**v1 阈值（全部 AND，任一不过即拒）**：

| 判据 | 阈值 | 实测校准（§3.1 攻击画廊，真阴面/六个攻击样本） |
|---|---|---|
| hunks | = 1 | 真阴=1；全部样本=1（hunk 数单独拦不住人，只作结构信号） |
| inserted 代码行 A | = 0 | 真阴=0；43 替换=1、注释走私=1、冒名=3 ⇒ **改名/替换类一行攻击在此被结构性击毙** |
| 代码删除行 D | 1 ≤ D ≤ 3 | 真阴=1；冒名=95、loop_kill=3（3 不致命，被 retain 拦） |
| 纯注释删除行 | = 0 | 冒名/走私样本命中 |
| tokens_changed | ≤ 40 | 真阴=5；loop_kill=12（过）；冒名=439（毙） |
| token_change_ratio | ≤ 0.02 | 真阴=0.0112（过）；loop_kill=0.0268（毙，第二道）；冒名=0.9799（毙） |
| anchor_coverage | = 1.0 | 真阴=1.0；删错位置=0、43=0、冒名=0.074 |
| remove_hit | = true | 真阴 true；删错位置/43/走私/冒名 false |
| retain 全保留 | = true | 真阴 true；loop_kill 缺 `while (!s_sf_b)`、冒名两条全缺 |
| probe 同源/翻转 | 见 §2.3 | 真阴 s_sf_b 2→0、je 1→0 |

**为什么绝对阈值与比率要 AND**：攻击者可以把阳夹具灌水撑大 denominator 稀释比率（故 3 行/40 token 的绝对值不可稀释）；小夹具上比率先于绝对值触发（故保留比率）。两条腿都不单独承重。

**判定输出**：`(ok, reasons[], metrics{…})`，reasons 必须逐条人话（进 replay 日志与毒样例断言），metrics 全量进 JSON 报告（warn 观察期用于校准阈值，不允许静默调参）。

**误报风险（诚实清单）**：
1. 花括号配平不认字符串/注释里的括号 → 复杂夹具误拒；fail-closed 方向（重写夹具，不放过），误伤计数入观察期指标，连续 2 批有真卡被误拒才允许升 v2 词法分析。
2. 3 行上限可能拒掉合法的多行机制（如加锁段跨声明+使用）→ v2 replace/多点形态承接；warn 期统计被拒但红队认为合法的样本数。
3. 阈值 0.02 是按**一个真样本 + 一个邻近攻击样本（0.0112 vs 0.0268）**定的，间隔仅 2.4 倍——这是当前最薄的安全裕度；B1 批次 13 张 asm 卡落地后必须用真实阴性夹具分布复核（【待实验】，列为 G-iso 开门前置）。
4. anchor 重名（重载）一律拒收，逼 Writer 用唯一名夹具——与现有"每函数独占全局"的夹具风格一致，零新增负担。

### 2.3 replay 新分支：触发、归类、编译失败分流

**注册位置**：`tools/atom_evidence_replay.py`，新函数 `check_negative_controls(meta, …)`，在 `replay_card` 中 **④ artifact_sha/④b P0-A（或跨编译器 artifact_assert 替代分支）通过之后、⑤ sanitizer 之前**调用。理由：阳面必须先被证明成立，阴面才有意义；放 sanitizer 前保证 `--no-sanitizer` 与门禁主路径都执行它。不改任何既有 return 点（沿用 508 旁路/集中插入风格）。

**编译行提取（不许另造）**：直接复用 `_artifact_compile_lines(command, …)` 的 token 级编译器识别（`_token_is_compiler`）与 `-o` 目标识别逻辑：
- artifact 通道：取卡 command 中产出 `.asm`（与主 artifact 同后缀规则）的编译行，把**源路径字面量替换为阴面 fixture**（要求阳 fixture 路径串在该行中出现，否则 `negative_control_command_missing`），`-o` 改指 tempdir，`CCACHE_DISABLE=1`（与 P0-A 同），执行 `-S` 行。
- run_key 通道：取产出 exe 的编译行做同款替换并执行，随后在 tempdir 运行 exe（超时沿用 600s 分类常量），按现有 `partition("=")` 提键。
- 阴面**不做 sha 校验、不做 sanitizer、不还原任何正式文件**（全程只在 tempdir；不获取 replay 锁之外的新锁，在既有 P0-G1 锁内串行执行）。

**三分类关系（它算 refute，不开新类）**：沿用现有"修复方式是改环境还是改卡"原则——阴面装置是卡 frontmatter 声明的一部分，坏了修卡，故全部阴面失败都是 **`refute:*`**，不是第四分类、不是 infra。

| 触发条件（短路顺序） | verdict(reason) | 类 |
|---|---|---|
| 卡写了 `negative_controls` 但字段不合 §2.1 | `refute:negative_control_bad_schema` | refute |
| 阴面 fixture 路径不存在 | `refute:negative_control_missing` | refute |
| 提取不到所需通道编译行 | `refute:negative_control_command_missing` | refute |
| 编译器进程未启动/超时（阴阳共用同一次工具链可用性判定） | `infra_error:compiler_missing` / `infra_error:compile_timeout` | **infra**（环境故障；编译器连阳面都跑不了时走这条） |
| 阳面同次 rc=0、阴面编译 rc≠0（编译器被证明活着且拒绝阴面源码） | `refute:negative_control_broken` | **refute**（夹具写坏是内容问题；这是"真破坏 vs 写坏"的机器分界：**同一次 replay 内阳面 rc=0 就是编译器健康的实测证据**，不解析 stderr 文本） |
| §2.2 diff 判据不过 | `refute:negative_control_diff`（reasons 全量入日志） | refute |
| 阴面编译运行全绿，但探针读数相对阳面**未翻转**或方向与 `op` 不符 | `refute:negative_control_passed`（断言在坏夹具上也成立=零判别力；方向不符细分 `negative_control_wrong_direction` 以便排障，统计上同属 passed 桶） | refute |
| 全部通过 | 日志 `✅ negative_control <id> flip verified（<通道> <读数> 阳→阴）`，不改变 confirm | confirm |

**关键语义**：`negative_control_passed` 用的是"阴面通过了原断言"的字面意——这是 V-iso 的核心判决：断言在机制被删后依然成立，等于招认自己没有判别力。它与既有 56 卡的 confirm 完全兼容（字段缺失整段跳过）。

**增量指纹（必做，否则阴面被改后沿用旧 confirm）**：`card_fingerprint`（:1486）现有 卡‖fixture‖artifact‖.out 四级哈希，追加遍历 `negative_controls[*].fixture` 全部文件字节（缺文件→`MISSING`，与现有口径一致）。阴面结果随 manifest 缓存，指纹不变且上次 confirm 才允许 skip（复用 `select_incremental`，零新机制）。

### 2.4 存量 56 卡迁移：分类判据 + 分批顺序与数量

**盘点【实测】**（脚本 `survey_cards.py` / `survey_props.py`，原始输出可复跑）：56 卡 = asm 型 13、run 型 43；仅 8 卡用 `run_match_file` 新形态（CONC×6、LANG×2），其余 48 卡为旧形态 `actual.run_*`；50 个 observation 命题 / 29 个 inference 命题；EV-MEM-030、EV-MEM-031、EV-UB-002 无 claim_structured 命题引用；EV-MEM-035、EV-MEM-039 仅服务 inference。

**observation 的阴面资格三档机械判据**（对每条 observation 命题的每张证据卡判定）：

- **A 档·可做 v1 阴面**，需同时满足：
  1. 存在**可绑定锚点**的既有探针：artifact 通道——卡 `artifact_assert` 有 `contains_in/absent_in`（或全工件 `contains/absent`，此时 anchor 省略为文件级，仅允许单夹具单函数的卡）且符号通过 Itanium 嵌入对到夹具中某个唯一定义的自由函数；或 run 通道——声明键中含夹具自由函数名子串；
  2. 该 anchor 函数体内存在**可纯删除的机制构造**（v1 机械初筛只做提示：`__atomic_`、`atomic_signal/thread_fence`、`std::atomic`、`volatile`、`virtual`、`new/delete`、`lock/unlock`、`throw`、`std::move`、`std::make_unique/shared` 等词表命中；词表只排序不判决，最终以探针实测翻转为准）。
- **B 档·结构性无单变量阴面（分类信号，自动建议归 inference，不自动降级）**：
  1. 纯存在性/环境事实：探针只有全局符号存在性（如"`_ZNSt8auto_ptr` 被实例化"）、`impl_*` 实现可用性（"该编译器在 -std=c++17 仍可编译 X"）、版本支持类——机制不在夹具内、无可删构造，且 A1 的锚点绑定必然失败；
  2. 计时/性能读数（wall-clock、吞吐、QPS）：删除导致的是分布漂移而非确定性翻转，v1 不可复算（v2 统计探针）；
  3. 多机制交互命题（删任一单独不翻转）——v2 多点阴面承接。
- **C 档·机器判不准**：进红队人工队列，**禁止脚本自动改 claim_type**（防把强 claim 错降级，§3.5）。

**分批迁移顺序（warn 先行，存量 0 block）**：

| 批次 | 对象（observation 命题） | 数量【推断，依据实测盘点】 | 为什么这个顺序 |
|---|---|---|---|
| B0 样板 | FENCE-001 prop-1，nc1 即本轮实测阴面正式落位 | 1 命题 / 1 阴面 | 天然对照已在卡内，本轮已有全部实测数字与攻击画廊，零探索风险 |
| B1 asm 档 | CONC FENCE/LOCK/RACE 3 原子（6 卡）、LANG-INLINE（2 卡 2 命题）、MEM-MOVE-002 p2、MEM-PERF-001 p1、MEM-SHARED-002 ×2、MEM-UNIQUE-002 ×2 | **11 命题 / 13 卡** | 全是区间符号断言，探针绑定最硬；单卡边际成本最低（0.09s）；同构性高，做完即知阈值是否需调 |
| B2 run·夹内双路径档 | RAII-001×2、RAII-002×3、LEAK-001×2、LEAK-002×2、ALLOC-001×3、ALLOC-002×2（EV-MEM-009/010/023/024/025/026/027/028/036/037/040/041/042/043） | **14 命题 / 14 卡** | 这些夹具本来就内置"安全路径/泄漏路径"双对照（如 RAII 卡 g_live=0/1），阴面=删掉安全路径里的机制行使键值翻转，苦力只需把已有第二条路径改写成单变量删除件 |
| B3 run·单路径档 | HIST×3、ALIGN×2、MOVE-002 p1、NEW×2、PERF-002/003/004（4）、RVREF×2、SHARED-001×2、UNIQUE-001×2、VALUE-001×2、VALUE-002×2、WEAK×2、UB-GRAY×1 | **24 命题 / 约 22 卡** | 形态杂、B 档比例预计最高（HIST 的 impl 可用性、PERF 计时）；逐卡过三档判据，B 档只出"建议改 inference"清单交人签，C 档排队 |
| 不迁 | EV-MEM-030/031、EV-UB-002（无命题引用）；EV-MEM-035/039（仅 inference） | 5 卡 | 无 observation 闸压，随各自原子补 claim_structured 时再判 |

warn 观察期规则：`OBSERVATION-NEEDS-CONTROL` 注册即 warn，对每条 observation 命题报"有/无合格阴面"，其 warn 计数曲线就是迁移进度；**升 block 的唯一入口是蓝图 G-iso 开关**（迁移卡 0 误伤 + 毒样例 100% 拦截，阈值用 B1 真实分布复核后），不许批次施工自行升级。

### 2.5 毒样例设计（阴阳成对，进 poison_drill 沙箱真编译）

沿用 `tools/poison_drill.py` 现有体例（tempdir 沙箱、真调 g++、断言 verdict/拦截规则）。每个样本含**夹具对+卡+期望判决**：

| 编号 | 构造（阳/阴） | 期望机器结果 | 证什么 |
|---|---|---|---|
| N1 阳过阴也过 | 阳=hello 风格双路径夹具；阴=阳面**逐字复制**（注释改一行） | `refute:negative_control_passed`（同时 diff 侧 zero-semantic 拒） | 零判别力断言的原型：阴面没被破坏 |
| N2 冒名阴面 | 阳=B0 夹具；阴=完全不同的程序（本轮 yin_impostor：删 95 行/插 3 行） | `refute:negative_control_diff`，reasons 含覆盖率/token/retain 至少 3 条 | 建设者硬要求：巨大 diff 冒充必被识破（实测 6 条理由同时命中） |
| N3 阴面写坏 | 阴面在 anchor 内留一个未闭合括号（同一次 replay 阳面 rc=0） | `refute:negative_control_broken`，**不得**落 infra | 真破坏 vs 夹具写坏的分流；防"写坏即逃生舱" |
| N4 形式阴面 | 42→43 式替换（插 1 行）或删 anchor 外赋值行 | 前者 `negative_control_diff`（A=1/coverage=0）；后者 diff 拒且探针不翻转 | 走形式阴面与 claim 无关 |
| N5 阴面缺失 | 卡声明 nc1 但文件不存在 | `refute:negative_control_missing` | fail-closed |
| N6 连主体删除 | anchor 内删 while+fence+} 三行（本轮 yin_loop_kill，能编译、探针同样翻转） | `refute:negative_control_diff`（retain 缺 `while (!s_sf_b)`；token 比率 0.0268 兜底） | 最锋利攻击：探针翻转本身不能证明删的是机制 |
| N7 干净卡 | 存量 56 卡（无字段）+ B0 正式卡（合规 nc1） | 前者 confirm 不变；后者 confirm 且日志含 flip verified | clean_pass_rate=100%，零误伤 |

施工验收：`poison_drill.py` 输出中 N1–N6 trap_block_rate=100%、N7 clean_pass_rate=100%，任一率下降即 CI 红（双指标接蓝图 V-honeypot）。

### 2.6 与 530 T4（活性判据）合并后的完整判定伪代码

```python
def observation_machine_eligible(prop, ev_index, *, g_iso_on: bool) -> Eligibility:
    cards = [ev_index[r] for r in prop.evidence_refs if r in ev_index]
    # 第 0 层（现行 block，不动）：observation 必须有工件断言载体
    if not any(_has_artifact_assertion(c) for c in cards):
        block("OBSERVATION-NEEDS-ARTIFACT")          # 526 规则2，零容忍
        return NOT_ELIGIBLE
    # 第 1 层（530 T4，warn）：活性三条件至少其一
    #   ① falsification 含量化对照取值（复用 EV-FALSIFICATION-QUANT 判定）
    #   ② 工件断言命中非通用、夹具特有符号（复用 EV-ASSERT-SYMBOL-MAPPED 出处判定）
    #   ③ run_match 键不在环境量集合（复用 EV-ENV-DEPENDENT-KEY 键表）
    live = any(
        t4_quantified_falsification(c)
        or t4_fixture_specific_symbol(c)
        or t4_non_env_run_key(c)
        for c in cards)
    if not live:
        warn("OBSERVATION-LIVENESS：缺活性对照，建议补对照或改 inference")
    # 第 2 层（V-iso，warn 观察期 → G-iso ON 后 block）：阴面翻转
    nc_cards = [c for c in cards if c.get("negative_controls")]
    iso = (bool(nc_cards)
           and all(replay_negative_controls(c) == "nc_all_confirmed" for c in nc_cards))
    if not iso:
        (block if g_iso_on else warn)("OBSERVATION-NEEDS-CONTROL：缺合格阴面翻转")
    # 三层齐备才允许 observation 走机验全自动；任一层 warn 期都不自动改 claim_type
    return ELIGIBLE if (live and iso) else HUMAN_QUEUE
```

边界纪律：① 三层判定只产出 block/warn 与"建议改 inference"，**改 claim_type 永远是人/红队动作**；② B 档"结构性无阴面"是排队理由不是降级判决；③ 规则注册点 = `gate_engine.py:_register_all` fact 列表（:2749），severity 走 sev 字典 warn 起步，与 T4 互不依赖、可各自合入。

---

## 3. 对自己设计的攻击（任务 3，每条给出真能绕过的原因或实测证伪）

### 3.1 最小 diff 能不能被"改 1 行语义天翻地覆"绕过？

**构造了 6 个攻击样本实跑（§1、probe_report.json），结论：v1 的 delete-only 形态让经典打法物理失效，残余 3 条如实列出。**

| 攻击 | 为什么可能绕过 | 实测/推演结果 |
|---|---|---|
| A1 变量改别名+顺手删关键锁，压成一行 | 替换在文本层是 1 行改动 | 任何"改"= 1 删 + 1 插，`inserted_lines=1` 直接拒（yin_formal_43 实测即此形态） |
| A2 删 1 行"牵一发"（如 anchor 内初始化/守卫行） | 纯删除、在 anchor 内、探针可能翻转 | **残余成立**：机器只能保证"删的是 anchor 内、且卡声明探针翻转"；这行是不是 claim 口述的那个机制，是语义判断。防线：remove/retain 由人签卡时确认 + 红队只看 1 个 hunk（工作量从读全卡降到读 1–3 行）。不假装机器能闭环 |
| A3 文件级一行作恶：`#define`/using 改名一行改全局语义 | 宏/using 是文件作用域 | 删除点在 anchor 函数区间外 ⇒ coverage=0 拒 |
| A4 连主体带机制一起删（最锋利） | 纯删除、能编译、探针**同样翻转**（实测 s_sf_b 2→0、je 1→0） | retain 逐条缺失被拒；token 比率 0.0268>0.02 第二道。⇒ **"翻转"单独不可信，retain 是这一击的唯一硬拦点** |
| A5 一行塞多条语句/续行符 `\` 折叠 | 物理行=1 但逻辑多改动 | tokens_changed 按剥离后的逻辑 token 计，单行上限随 40 token 总量封顶（v1 可加"单删除行 ≤12 token"细分，FENCE 实测 5） |
| A6 缩进/注释走私（六轮 E07 同族） | 物理 diff 有内容、语义无改动 | token 变动=0 即拒（yin_smuggle_comment 实测） |
| A7 给阳夹具灌水稀释比率 | 2% 比率可被大 denominator 稀释 | 3 行/40 token 绝对值不可稀释（AND 关系） |

**残余总评**：机器层封死的是"形态、位置、支架、翻转"四件事；唯一留给语义层的是 A2——"被删行是否恰为 claim 所述机制"。这与全系统信任轴一致（结构归机器、语义归人签），且人审成本被压到看一个 ≤3 行的 hunk。

### 3.2 走形式的阴面（42→43）机器层怎么识别？

三层串联，实测每层都能独立击毙一类形式主义：
1. **形态层**：常量替换产生插入行 → delete-only 直接拒；
2. **位置层**：纯删除但删在 anchor 外（实测 yin_del_unrelated 删 `s_sf_a = 8;`）→ coverage=0 + remove 未命中；
3. **相关层（最关键）**：即使删除发生在 anchor 内，探针被**预先钉死在卡的既有 claim 锚点**上（artifact 断言编号/声明 run 键），无关改动翻不动它——实测 yin_del_unrelated 的 run 键 8→0 真翻转了，但 asm 探针（s_sf_b/je）纹丝不动 ⇒ 拒收。
   "Writer 给卡加一条弱断言再让阴面翻它"的接力攻击：要同时改阳卡断言（受 sha/P0-A/卡指纹约束）、闯既有判别力检查（`contains_in` 的 k/N 背景噪音规则、P4 自证断言规则）、再获人签——V-iso 不是孤军，是叠在六轮既得防线之上。残余：此链依赖卡人签不失效，属 Oracle 铁律范畴。

### 3.3 成本曲线：56 卡全做阴面，nightly 加多少？

【实测】单点：asm 通道 +0.0875s/阴面，run 通道 +0.34s/阴面（0.26 编译+0.08 运行）。
【推断】上限（51 张服务 observation 的卡每卡 1 阴面）：13 asm 卡×0.09 + 38 run 卡×0.34 ≈ **14.1s**，加到 136.7s 全量基线 ≈ **+10.3%**。
**不确定性区间 7–21s**：exe 编译实测在 0.20–0.26s 抖动、ccache 冷热未知、多 TU 卡（LANG 系列）单卡更重；B 档排除与"多命题共卡共享阴面”会把实际值压低 20–30%，**点估计 ≈10–12s（+8%）【待 B1/B2 后用真实分布复核】**。对照蓝图曾写"+2.3s/关键命题"——那是按整卡真编译估的，实测 asm 阴面只要一次 `-S`（0.09s），**旧估计高估约 25 倍**。
PR 通道：增量 replay 只为指纹变更的卡付阴面成本（每触达卡 +0.09/0.34s），30s 预算无压力。
**不该做阴面的 observation**：① 计时/性能键（PERF 类，翻转不确定=CI 假红源）；② 多 TU 重编译卡（成本爆炸，改在 nightly 低频做）；③ B 档存在性事实（结构性不可做，做了就是假阴面）。

### 3.4 活雷会不会腐化？怎么保证雷集是活的？

**会，且腐化方式很具体**：雷被修复后它在 nightly 依然"被拦截"——只是拦截者从目标规则变成了更早的另一条规则，trap_block_rate 永远 100%，绿灯摆设。四条机器化保鲜措施：
1. **拦截者归因指纹**：每颗雷记录出生时的实际拦截判决（verdict reason + rule_id 集合 + 关键日志行 hash）；nightly 复跑比对，归因漂移 → `mine_drifted` warn（雷还红，但红得不对）。
2. **雷的季度轮换**：雷集每季度必须注入当季红队新逃逸（血换的案例），超过 2 个季度无漂移事件、无轮换、无重确认的雷自动标 `stale` 并从 trap 率分母剔除（不允许靠僵尸雷凑 100%）。
3. **Canary 反向验证（活雷活性的机器证明）**：每季度在沙箱里**故意修好**一颗雷的载荷（把攻击改成合规形态），trap_block_rate 必须下降；不下降说明这颗雷本就没有判别力（雷集的"阴面"——以其雷之道还治其雷）。
4. **沙箱铁律**：活雷只准在 tempdir 真跑（P0-A 同款隔离），禁止落 Examples/atoms（沿用蓝图 04-C2b）。

### 3.5 边界漏网：真有判别力但结构上构造不出单变量阴面的 observation 吗？

**有，三类，实测/推演各一：**
1. **交互效应命题**："X 与 Y 同时存在才导致 Z"，删 X 或删 Y 单独都不翻转（冗余/协同）。单变量探针结构性不存在 → v2 多点阴面。
2. **分布型命题**：性能、缓存命中、调度延迟——确定性翻转不存在，只有统计分布。归 v2 统计探针（N 次运行+效应量），v1 强行做必产生 flaky 绿。
3. **历史/实现可用性命题**：EV-HIST-001 的"GCC 15.3 在 -std=c++17 下仍提供 auto_ptr"——机制在编译器实现里，夹具内无物可删。这类归 inference **是正确分类**（它本来就是环境事实，不是机制观测）。

**错降级防护（硬要求）**：B 档判据命中时系统只做两件事——warn `OBSERVATION-NEEDS-CONTROL` + 生成带证据的人工队列项（写明"未找到锚点探针"的机器依据）；**claim_type 不得自动变更**。理由：机器只能证明"当前夹具里没找到可绑定锚点"，证明不了"结构上不存在"（可能是夹具写得差而非命题性质）。错降级率（红队复查中被推翻的比例）列为观察期指标，>10% 说明 B 档判据本身要回炉。FENCE 自身就是警示：只看 run 通道会误判它"无阴面"，是 §1.4 的 artifact 通道把它救回 A 档。

---

## 4. 苦力执行批次（一任务一 commit；每条挂"为什么现在做"+ 机器验收）

| # | 任务（独立 commit） | 为什么现在做 | 机器验收判据 |
|---|---|---|---|
| C1 | 新增 `tools/viso_diff.py`（移植 iso_judge.py）+ 单测：真阴面通过、6 个攻击样本全拒、Itanium 嵌入校验、重名 anchor 拒 | 判据是最大赌注的硬护栏，先于任何卡迁移独立可测 | `pytest tests/test_viso_diff.py` 全绿；判据函数纯函数无 IO |
| C2 | replay 接入 §2.3 分支（含指纹纳入阴面 fixture、manifest 缓存），字段缺失路径行为不变 | 没分支就没有阴性判决，一切都是文档 | 既有 `tests/test_atom_evidence_replay.py` 全绿；56 卡 replay 结果逐字不变（confirm=56） |
| C3 | gate 注册 `OBSERVATION-NEEDS-CONTROL`（warn，sev 字典起步）与 530 T4 合并判定 | warn 先看见全库缺口曲线，迁移才可排期 | gate block=0；warn 条目快照入库；poison 无 uncovered |
| C4 | B0：阴面落正式路径 `Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`（即本轮 yin_del_fence）+ EV-CONC-001 frontmatter | 样板成本已被本轮预付，数字全部现成 | 该卡 replay 日志含 `nc1 flip verified`（s_sf_b 2→0, je 1→0）；56 卡仍 0 block；sha/卡其余字段不动 |
| C5 | poison_drill 增 N1–N7（§2.5） | 双指标率是 G-iso 的开门凭据 | trap_block_rate=100%（N1–N6）且 clean_pass_rate=100%（N7），CI 红线 |
| C6 | B1 批 13 asm 卡迁移（建议按 4 原子分 4 个 commit：CONC/LANG/MOVE+PERF/SHARED+UNIQUE） | 同构性最高、单卡 0.09s，是阈值复核的数据来源 | 每卡 nc flip verified；`negative_control_diff` 误伤登记为 0；阈值用该批分布复核并留记录 |
| C7 | B2 批 14 run 双路径卡（可分 3 commit：RAII/LEAK/ALLOC） | 夹内对照已存在，边际生产成本最低 | 同 C6；run 通道键值翻转有日志阳→阴读数 |
| C8 | B3 批 + B 档清单（只出"建议改 inference"名录，人签才改） | 收口供 50 命题全量过闸；暴露真 B 档比例 | 每条 observation 三档有归属；claim_type 零自动变更；错降级率指标上线 |
| C9 | V-honeypot 活性四件套（归因指纹/drift/轮换台账/canary）接 §3.4 | 与 V-iso 同期上线才防止雷具腐化 | 季更任务存在；canary 演练脚本可让 trap 率人为下降并告警 |

**三档划分**：
- **现在做**：C1–C6、C9（纯机械、零模型依赖、数字已实测或可立即实测）；C7/C8 紧随但允许按批节奏。
- **攒数据（不启用）**：`negative_control_diff` 拒收理由分布、NC 一次通过率、错降级率、nightly 阴面实测加时、阈值裕度复核——全部进 nightly 指标；**G-iso 升 block 的 enter 条件 = 迁移卡 0 误伤 + N1–N6 100% + NC 一次通过率 ≥70%（低于说明赌注在三要素提取步骤塌了，回去改夹具指引而非放松判据）**。
- **等模型/等 v2**：replace_mechanism 多点阴面、统计型探针、AST 级 diff、LLM 协助生成 retain 候选（只可建议、人签定稿）、run_rc 崩溃绑定。一律只许在 v2 字段/接口里预留，v1 代码里见到 v2 值即 bad_schema。

---

## 5. 附录

### 5.1 本轮产出物（全在 `_arch_v2_round2/`）

- `533_V-iso施工规格.md`（本文件）
- `iso_judge.py`：最小 diff 判据原型（§2.2，施工进 tools/viso_diff.py）
- `survey_cards.py` / `survey_props.py`：56 卡与 79 命题结构盘点（可复跑）
- `schema_parse_probe.txt`：frontmatter 书写格式的解析器实测件（块式 map 通过、跨行 flow map 被截断）
- `probe_fence_iso/run_probe.py`：夹具变换+编译运行+判据+计时一体脚本
- `probe_fence_iso/{yang,yin_del_fence,yin_formal_43,yin_del_unrelated,yin_loop_kill,yin_smuggle_comment,yin_impostor,diag_yang_hang,diag_yin_hang}.cpp`：全部夹具样本
- `probe_fence_iso/probe_report.json`：全部原始读数；`build/` 内生成物；`full_replay_56.log`：全量基线日志

### 5.2 正式目录零改动证据

`git status --porcelain -- Examples atoms evidence`（2026-09-15，本轮结束时）：**无输出**；官方工件 sha 复验 = `8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3`（与卡一致，replay 删件/还原正常）。

`tools/ tests/` 下存在**并行会话的在制改动**（会话中两次快照名单不同：先是 gate_engine/poison_drill 等，后变为 `M tools/golden_lock.py`、`?? tests/test_golden_classify.py`——属 530 T5 warn 会计施工），均非本轮产生：本轮全部写操作只落在 `_arch_v2_round2/`，未对 tools/tests 执行过写。本轮新增仅 `_arch_v2/`（前轮）与 `_arch_v2_round2/`（本轮）两个未跟踪目录；`build/replay_manifest.json` 为 gitignore 内构建产物。

### 5.3 与蓝图/04 自攻的差异记录（本轮实证导致的修正）

1. v1 探针从"run_match 键翻转"扩为 artifact 区间计数 + run 键两通道（§1.4 实测所逼）。
2. 阴面边际成本估计从 +2.3s 修正为 +0.09s（asm）/+0.34s（run）（§3.3）。
3. 04-C1b 原把单变量判定整体留给红队；本轮把可机器部分收紧为 delete-only+anchor+retain+同源探针四道，红队只剩"被删行是否即 claim 机制"一个语义点（A2 残余）。
4. 04-C1c 的 rc≠0 half-credit 方案在 v1 不实施，run_rc 通道整体推迟 v2（v1 不收崩溃当翻转）。
5. 保留资产全部未动：fail-closed 三分类、P0-A 独立重编译、人签、毒样例沙箱体例；新层只复用、不替换。
