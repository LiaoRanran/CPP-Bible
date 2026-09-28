# 656 验收报告：核心 PBT/变异/性能 + 前端工程化 + 学习 MVP

> 任务书：`_auto/inbox/656.md`　｜　批次：656　｜　状态：**awaiting_review**　｜　日期：2026-09-28
> 门禁：**run_656_gate PASS 13/13**（fast / full / ruff / mypy / 核心器械自检 / 前端产物 / 数据管线 /
> Node 真求值 / jsdom DOM 冒烟 / 学习卡数据 / 保护器联调 / 受控零污染 / 信任根）

## 一、B1 核心 stateful PBT（P1–P12）

**产出**：`tests/test_core_pbt_656.py`（**28 例**）+ `tests/test_core_boundary_656.py`（**24 例**），合计 **52 例**。

| 性质 | 落点 | 与 651 的差别 |
|---|---|---|
| P1 半格（交换/结合/幂等/封闭） | 穷举 4³ + hypothesis 随机 | 651 只有穷举 |
| P2 worst-wins | 随机序列折叠 = 最坏分量 | 新增随机域 |
| P3 账本前缀保持 | **真实 `AuthorityLedger`** | 651 只在模型层 |
| P4 Merkle 一致/包含 + **篡改必拒** | 真实 `ledger_checkpoint_651`，随机叶子集 | 新增反向性质 |
| P5 保护器标记置换不变 | + `conflict_detector_647` 判定确定性 | 挂真实保护器 |
| **P6 判决单调性** | 真实 `classify`：加担子不得变好 | **新性质**（见 §五.1） |
| **P7 冲突检测** | 真实 647：确定性 + 规则顺序无关 + 自反 | 新性质 |
| **P8 追加不可变** | JSONL 前缀字节不变 + **无 update/delete 入口** | 新性质 |
| **P9 哈希链防篡改** | 改任一事件任一字段 ⇒ `verify_chain` 必假；GENESIS/序号/`validate` 必填 | 新性质 |
| **P10 迁移合法性** | 655 B §2 的 6 类合法迁移 + `fail→pass` 只能人审（INV-12） | 新性质 |
| **P11 并发安全** | 8 线程 × 6 次并发追加：不丢/seq 唯一/链成立 | 新性质 |
| **P12 确定性/可重放** | 同输入同 `self_hash`；seq 变则 hash 变 | 新性质 |
| 状态机 | `RuleBasedStateMachine`：随机 append/reject/modify + 3 条 invariant | 新形态 |

**诚实登记（B1）**：P6 的"单调性"**不能**用 651 那个线性秩（`fail < unknown < pass_with_exception < pass`）——
实测撞到反例：去掉边界会让 `fail → unknown`，线性秩下会误判为"变好"。正确模型是**偏序**：
信息量维 `unknown < {三态}`、好坏维 `fail < pass_with_exception < pass`，且 **`fail` 与 `unknown` 不可比**。
已写进测试文件注释与 `docs/core_rust_boundary_656.md` §五。

## 二、B2 变异测试（检出率**多少就写多少**）

**产出**：`tools/mutation_test_656.py`（4 算子：比较翻转 / 常量 ±1 / 布尔反转 / 删检查；
进程内替换 + **子进程模式**；`core` / `all` 双作用域）+ `data/656_mutation_report{,_core}.{md,json}`

| 作用域 | 含义 | 变异体 | 被杀 | 存活 | 导入崩 | 超时 | **检出率（可跑口径）** |
|---|---|---:|---:|---:|---:|---:|---:|
| `core` | 只改核心判决路径函数体 | 60 | 30 | 18 | 10 | 2 | **62.5%** |
| `all` | 整文件随机抽样 | 60 | 15 | 37 | 8 | 0 | **28.8%** |

分文件（core）：`four_state_verdict_638` 8/19 = 42.1%｜`ledger_checkpoint_651` 12/14 = 85.7%｜
`decision_event_v2_626` 10/15 = 66.7%。分文件（all）：17.6% / 55.6% / 11.8%。

**未达标（诚实登记，任务书目标 80%）**：`core` 62.5%、`all` 28.8%。差额的去向已逐类查清：
1. **等价变异**：如把 `h = rec.get("mutation_set_hash")` 的取值写法换掉但语义不变；
2. **CLI / 报告 / 迁移计划等路径**：本就没有单测（`all` 口径把它们混进来，故数字更低）；
3. **超时与导入崩**：环境类（分别在"可跑口径"外单列，不掺进检出率）。

**本轮按任务书要求补的测试（3 条，直接来自存活体分析）**：
`test_p4_tampered_leaf_must_fail_verification`（换叶子/换下标/换根 ⇒ 必 False）、
`test_p9_genesis_and_length`、`test_p9_validate_rejects_bad_shapes`（MODIFY/ABSTAIN/REPLACE/target_id 必填）。

**器械自检（这条最重要）**：`--check` 里有一个"**射程自检**"——故意把 `_HASH_RE` 从
`^[0-9a-fA-F]{64}$` 放宽成 `^.*$`，**必须被杀**。首版它**存活** ⇒ 当场暴露"变异体根本没进射程"
（测试模块在 import 期就绑定了对象引用，换 `sys.modules` 不生效）⇒ 改成"每个变异体重新 import 杀测试"后
才真的杀掉。**没有这条自检，就会交出一个"检出率 0% 但其实是坏的"工具。**

## 三、B3 边界清理（核心审计 ⇒ 显式处理 + 测试）

审查对象：`four_state_verdict_638` / `decision_event_v2_626` / `ledger_checkpoint_651`。
**实测到并修掉的四类边界**（每条都有回归锁）：

| # | 问题（原来会怎样） | 修法 | 锁 |
|---|---|---|---|
| 1 | `classify(None)` / `has_boundary("x")` ⇒ **抛 `AttributeError`**（把"判不出来"变成"崩掉"） | 非 dict 入参 ⇒ 显式 `unknown`（含原因） | `test_classify_non_dict_is_unknown`（6 参数化） |
| 2 | `classify_card(None/"")` ⇒ `open()` 抛 `TypeError`，**不属于 `OSError`** ⇒ 漏出捕获 | 空/非字符串路径 ⇒ 显式 `unknown`；捕获扩到 `(OSError, TypeError, ValueError)` | `test_classify_card_bad_path_is_unknown`（5 参数化） |
| 3 | **`inclusion_path(0, [])` 无限递归** ⇒ `RecursionError`（空树/越界是**合法查询**，不该炸） | 空树或越界 ⇒ 返回 `[]`（空证明） | `test_merkle_empty_ledger_no_crash` |
| 4 | `AuthorityLedger.append` **隐式假设单线程**（取 prev → 分 seq → 追加三段不加锁 ⇒ 并发算同一 `prev_hash`/`seq`，哈希链悄悄分叉） | 临界区加**可重入锁**；`verify_chain` 持同一把锁（不再验到"写了一半"的链） | `test_ledger_append_is_internally_locked`（8×6 并发，**不加外部锁**） |

冲突证据类边界一并锁死：`pass_with_exception` 缺 `explanation` ⇒ 降级 `unknown`；
`verdict` 写 `block/fail/reject/refuted/false` ⇒ 必走 `fail`（不许溜进 pass）；`unknown` 词 ⇒ `unknown`。

## 四、B4 性能（先量再说）

**产出**：`tools/core_profile_656.py` + `data/656_core_profile_report.{md,json}`

| 路径 | 口径 | mean | p95 |
|---|---|---|---|
| `classify_card` | **单卡端到端**（读卡 + 抽字段 + 分类），47 张卡 | 27.89 ms / 47 张 ⇒ **0.5934 ms/张** | 28.39 ms |
| `classify` | 纯内存判决 | **0.0022 ms** | — |
| `AuthorityLedger.append` ×20 | 哈希链写路径 | 0.61 ms | — |

⇒ **单卡判决路径 0.59 ms < 1 ms（达标）**。Top10 热点（cProfile·tottime）：
`re.Pattern.search` > `_io.open` > `read` > `classify_card` > `utf_8_decode` > `relpath` ——
**花费在 I/O 与正则扫描**，不在判决逻辑本身。

**优化（Top3 里只做 1 个，另 2 个明确不做）**：
- ✅ #1 预编译边界正则（`classify_card` 每卡现编 3 个 ⇒ 模块级 `_BOUNDARY_RE`，语义不变）：
  **0.6089 → 0.5934 ms/张（−2.5%，接近噪声）**。收益在噪声内就说在噪声内，不吹。
- ❌ #2 用前缀裁剪替掉 `os.path.relpath`（占 ~0.001s）：会引入路径语义差异风险。
- ❌ #3 多趟正则合并成一趟：收益同样在噪声内。
- **不做 MVP 模型重写**（任务书提及"判决模型重写（MVP）"）：B4 的数证明瓶颈在 I/O，重写判决模型没有收益；留给后续批次。

## 五、B5 Rust 边界（**只做准备，一行 Rust 不写**）

**产出**：`docs/core_rust_boundary_656.md` —— 七层"核心"切分（判决合成/哈希链/Merkle 进候选；
规则引擎/卡解析/报告留 Python）、**函数清单 + 冻结签名**、**进 Rust 的三条判据**（纯 / 热 / 有性质可锁）、
**两阶段接口**（先 JSON-in/JSON-out CLI + 与 Python 的 10⁴ 随机差分测试；稳定后再 PyO3，且保留 CLI 作独立复核通道）、
**12 条不变量与对应测试映射**、以及 4 条"本批没做"的诚实登记（含"`combine` 还住在测试文件里，
要搬得先下沉到内核"）。

## 六、C 前端工程化

| 要求 | 结果 |
|---|---|
| 设计系统 / tokens | `web/css/design-tokens.css`：色板（语义命名）/ 排版 / 间距 / 圆角 / 阴影 / 动效 / 层级 + 兼容旧变量别名；**唯一变量源** |
| WCAG 2.2 AA 对比度检查 | 已实现（管线 `--check` 里**现算** 8 组对比度）；**实测抓出真问题**：`--color-text-mute` 原 `#6b747c` 只有 **4.09:1**（AA 正文需 4.5）⇒ 提到 `#787f87` = **4.80:1**（surface 上 4.60:1 也达标） |
| 组件库 | `web/components/`：`qy-nav`（统一导航）/ `qy-card` / `qy-panel`（指标，支持动画更新）/ `qy-button` / `qy-tag` / `qy-status`（四态指示器）；**四个页面**（index / starmap / verify / card）统一接线 |
| 数据管线 | `tools/web_data_pipeline_656.py`：一条命令 ⇒ 跑齐 4 个生成器 → schema 校验 → `web/data/index.json`（**逐文件 sha256 索引**）→ 漂移检查 → 对比度 → 组件接线 → 卡片契约 → `dist/` 构建 |
| 构建脚本 | 保守压缩（只删整行注释/空行/行尾空白）+ **`node --check` 复检**（检不过**退回原样复制**并在 manifest 标 `minified=false`）+ 内容哈希版本号 + `dist/manifest.json`；实测 93 473B → 81 039B（19 个资源，全部压缩成功） |
| 部署 workflow | `.github/workflows/deploy.yml`：Pages 部署前依次跑 管线 `--check` / Node 真求值 / **jsdom DOM 冒烟**（Node 20，本机 Node 18 只能 SKIP）/ 构建；**任一环节红则不发布** |

## 七、D 学习 MVP

**产出**：`tools/teach_card_656.py` + `web/card.html` + `web/card.js` + `web/data/{cards.json, cards_index.json, card.json}`

| 要求 | 结果 |
|---|---|
| 卡页面三段（前置/学习/自测） | ✅ `card.html` 三段式；学习段含：断言 / **边界**（含边界三元组缺项提示）/ 四态现算 / 命题（含 `external_basis`、活性、签署）/ 证据（含**可复制的复现命令**、artifact sha256）/ 反例（W2 攻击边） |
| 前置依赖查询 | ✅ `relations[].prerequisite` 是**真实字段**（如 ATOM-CONC-RACE-001 ← ATOM-MEM-RAII-002 一类声明），1 跳展开 + 可点击跳转；无声明时**明说**"台账层面没有声明先修链"；另给"同域 verified 可横向对照（**不是**先修声明）" |
| 学习进度本地存储 | ✅ localStorage（`queyi.progress.v1`）：标记已学/撤销、自测记分、全局进度 `本机已学 x/47`；**不上传、无后端**；隐私模式禁写时静默降级 |
| 自测题从真实数据生成 | ✅ **7 类题**由字段机械生成（四态及理由 / 边界范围 / 命题类型与证据 / inference 的外部依据 / 复现命令 / 证据卡 verdict / 前置卡），**每题带 `source`（字段出处）**，不写任何 AI 生成的内容 |
| 用真实数据、不造演示数据 | ✅ 47 张卡 368 KB，证据引用 **0 处缺失**；页面显式摊开台账现状 |

**过程中发现并如实呈现的台账现状（重要）**：**47 张卡里 0 张带边界三元组**
（`mutation_set_hash/mutation_count/generator_version`）⇒ 按 638 的"边界优先"语义，**四态必然全部 `unknown`**。
页面**照实显示**并在顶部写明原因（同时给 `unknown` 计数），不挑一个好看的态。
这与 655 B 的发现一致，属台账现状而非页面缺陷。

## 八、E 收工

### 8.1 门禁

`python tools/run_656_gate.py` ⇒ **PASS 13/13**：
fast / full / ruff / mypy / 核心器械自检（含变异射程自检 + 性能器械）/ 前端产物（27 项文件齐备）/
数据管线（schema / 索引漂移 / WCAG AA / 组件接线 / 卡片契约）/ Node 真求值 / jsdom DOM 冒烟（本机 SKIP 计 PASS）/
学习卡数据（只读校验）/ 保护器联调（`mode_switch_effective` 4 个、`not_effective` 0）/
受控 atoms 指纹一致 / 信任根 `tool_integrity --check` 4 节 OK。

### 8.2 回归

受影响面（`decision_event_v2` / `decision_event_647` / `four_state_verdict_638` / `four_state_636` /
`authority_schema_v2_626` / `653_tools` / `655_tools` / `verdict_spec_v1_655`）⇒ **全绿**（100%，
无 F/E 标记）。本批改动三个核心模块（加锁 / 空入参 / 空树）未引起任何既有用例失败。

### 8.3 自纠明细（全部已修，均为本批自查发现）

| # | 问题 | 发现方式 |
|---|---|---|
| 1 | `teach_card_656 --check` **会写文件**（刷新 `cards_index.json` 的时间戳）⇒ "索引漂移"检查必然误报 | 门禁 `pipeline` 阶段 **FAIL**（12/13）⇒ 改成只读 + 与磁盘产物逐字段比对 |
| 2 | 变异测试 `enclosing_func` 只匹配顶格 `def` ⇒ **类方法（`AuthorityLedger.append` 等）全被漏掉**，第三目标候选数变 0 | 结果里出现 "候选 0 ⇒ 抽取 0"，当场发现 ⇒ 允许缩进后 core 检出率才有意义 |
| 3 | 变异测试进程内模式会**跑飞**（某变异体让测试死循环，40 分钟不结束） | 后台运行观察 ⇒ 改子进程模式 + 硬超时（跑飞即杀并计 `timeout`） |
| 4 | `pytest` 的 `tmp_path` fixture 在进程内没有 ⇒ 基线"未绿"误判 | 基线自检直接报错 ⇒ 用真实临时目录顶替 |
| 5 | `teach_card_656` `json.dumps` 撞 `datetime.date`（YAML 把 `verified_at` 解析成日期） | `--all` 首次运行 TypeError ⇒ 加 `default=str` |
| 6 | 静态检查：`ruff F541/FURB167/F601`、`mypy` 赋值类型冲突 | 门禁阶段 3 逐条修 |

### 8.4 红线守护（均有器械证据）

- **未改** `CORE_TOOLS` 判决逻辑、**未改** 67 条规则、**未改**历史账本、**未改**受控内容目录
  （`atoms/ evidence/ Examples/ Book/` 在本批**零 diff**：B3 的加锁与空入参只动 `tools/` 下的纯函数；
  受控 atoms 指纹门禁前后一致）；
- **未代签 / 未 golden accept / 未 push**；
- 本批只新增文件与工具内部改动（`tools/{four_state_verdict_638,decision_event_v2_626,ledger_checkpoint_651}.py`
  三处改动均**不改语义**、均有回归锁，且三者**不在信任根 pin 列表内**，故 `tool_integrity --check` 仍 4 节 OK）。

## 九、交人项

1. **变异测试 80% 目标未达成**（core 62.5% / all 28.8%）：是否接受"核心 62.5% + 逐类登记"，或
   后续批次专门补 CLI/报告路径的测试（本批已把存活体全量列出，可直接当 TODO 清单）。
2. **边界三元组落卡**（47 张 0 张带）：这是让四态**从 unknown 变成有意义**的前提；属台账数据变更，
   需监工决定由哪批做、以及"补边界 ⇒ 迁移/新事件"的口径（655 B §2 迁移 #1）。
3. **B4 的 MVP 判决模型重写**：本批用数据证明瓶颈在 I/O ⇒ **不做**；是否同意这个结论？
4. **Rust 阶段 1（CLI + 差分测试）**是否立项（B5 已给签名与判据）。
5. **Pages 部署**：workflow 已就绪，需仓库开启 Pages（Source = GitHub Actions）才会真正发布。
6. **jsdom / Node 版本**：CI 用 Node 20 才能跑真 DOM 冒烟；本机 Node 18 只 SKIP（同因 `mermaid_parse_check` 本机不可跑）。
7. **`web/dist/`**：已在 `.gitignore`（构建产物），是否需要在发布前把 `dist/manifest.json` 作为 artifact 归档。
8. 是否 push（现状 `origin/master..HEAD` 未推）。

## 十、产物清单

- 核心器械：`tools/mutation_test_656.py`、`tools/core_profile_656.py`、`tools/run_656_gate.py`
- 测试：`tests/test_core_pbt_656.py`（28）、`tests/test_core_boundary_656.py`（24）
- 文档：`docs/core_rust_boundary_656.md`
- 前端：`web/css/design-tokens.css`、`web/components/{index,qy-nav,qy-card,qy-panel,qy-button,qy-tag,qy-status}.js`、
  `web/card.html`、`web/card.js`、`web/{index,starmap,verify}.html` 与 `web/{starmap,verify}.js`（接线改动）
- 管线/部署：`tools/web_data_pipeline_656.py`、`.github/workflows/deploy.yml`
- 学习数据：`tools/teach_card_656.py`、`web/data/{cards,cards_index,card,index}.json`
- 报告：`data/656_mutation_report{,_core}.{md,json}`、`data/656_core_profile_report.{md,json}`、
  `data/656_{mutation_core,mutation_all,gate,regression}.txt`、本报告

---
_656 收工：门禁 13/13 PASS；B2 检出率**未达标**已逐类登记；自纠 6 项；红线未破；未 push。_
