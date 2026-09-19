# _worklog_572 · 收 M3 的 52 条真洞：断言数人审基线 + 恒真样板收口

> 任务书：`References/architecture_架构演进/572_M3真洞收口_断言数人审基线_恒真样板.md`
> 承接：`403bb16`（571）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付

| 任务 | 结果 | commit |
|---|---|---|
| 0 · 52 条逐条定性 | **(a) 17 / (b) 35 / (c) 0** | 无代码（§1） |
| 1 · 人审断言计数基线（堵 (a)） | 新规则 `EV-ASSERT-COUNT-BELOW-BASELINE`（warn）· 存量零命中 | `69ca9bc` |
| 2 · 恒真样板收口（堵 (b)） | **单点**接进既有 `EV-ASSERT-SYMBOL-MAPPED`（warn，不新造规则） | `69ca9bc` |
| 3 · 复跑验证 (c) 登记 | **M3 逃逸 52 → 0**；judged 65 不变；(c)=0 ⇒ 无需登记 | `69ca9bc` |
| 附 · 冻结值随新规则更新 | 删键变体规则集 = `[基线规则, EV-OUT-UNDECLARED-KEY]` | `0a4dc80` |

## 1 · 任务 0：52 条逐条定性（实跑，`_t0_572.py`）

| 类 | 条数 | 形状 | 计数证据（变异前→后） |
|---|---|---|---|
| **(a) 条目变少可对基线** | **17** | 删一条 flow 式 `artifact_assert` 条目 **11** + 删一条 `run_match_keys` 声明 **6** | 如 EV-CONC-003 (4,8)→(3,8)；EV-CONC-002 (9,2)→(9,1) |
| **(b) 恒真样板可识别** | **35** | `contains` 被改成 `contains_any` 并**追加** `.file` | 计数不变（4,8）→(4,8)，但 35 条的追加符号**全部**被 553 `_is_universal_symbol` 判为通用 |
| **(c) 结构性堵不住** | **0** | —— | —— |

三分类**逐卡**明细见 `_t0_572.py` 输出（52 行，含卡 id / 变异点 / 前后计数 / 通用符号）。

## 2 · 任务 1（堵 (a)）：人审断言计数基线

**取法（怎么取基线）**：人审过的 **56 张 EV 卡**当前的
`(artifact_assert 条数, run_match_keys 键数)`（两种写法都按 frontmatter 解析后计数：条目数
`len(artifact_assert)`、键数 `len(actual.run_match_keys)`）写进 **`tools/assert_count_baseline.json`**
（入库、进 git diff ⇒ 改动留痕）。刷新命令：`gate_engine.py --update-assert-baseline`
（**只增不减**：取 max —— 下调基线等于承认"这张卡可以少查几项"，必须是人审的显式动作）。
实测生成：**56 卡 · 断言 118 条 · 键 56 个**。

**规则**（`check_evidence_assert_count_baseline`，warn）：
* 当前计数 **<** 基线 ⇒ warn（文案点明"现有断言仍成立，但卡被悄悄删项时复算与门禁都看不出来"）；
* 当前 **>** 基线（补强）⇒ 不算违例；
* 基线**缺该卡**（新卡未进人审基线）/ 文件**缺失或损坏** ⇒ 不报（环境容错，同 S1 的"git 不可用不报警"）。
* **存量零误伤**：基线就取自当前人审卡 ⇒ 当前计数不可能 < 基线（**实测 gate 命中数与改前逐字相同**）。

## 3 · 任务 2（堵 (b)）：恒真样板**单点**接入（不新造规则）

**根因定位**：`check_evidence_assert_symbol_mapped` 里 `if any_of and mapped: continue` ——
只要断言里**另有**一个真实出处候选就放行，于是"往 any-of 里**追加**一个通用候选把断言拉向平凡"
这一步**完全无感**（571 的 35 条逃逸全是这个形状）。

**改法**：就在这一分支里显式点出通用候选 ⇒ **warn**（同一条规则 id、**不 block**、不新造规则）。

**踩过的坑（先量后动的价值）**：宽匹配（把 `text` 也算上）会**误伤存量** —— 实测 4 处
（`EV-CONC-001` 两处 `je`、`EV-LANG-001` 一处 `call`）看似命中，但它们是 `contains_in/absent_in`
的**锚定文本**（区间内助记符并非恒有，414 已裁决为强断言）。而 `_assert_targets` 对锚定 kind
返回的是 **symbol**（不是 text）⇒ 本规则的候选检查天然只覆盖非锚定 kind ⇒ **存量 0 命中**
（与实测一致：gate warn 仍 136）。

## 4 · 任务 3：复跑验证

全量 M3（`--cards all --operators M3 --limit 999`，报告 `data/mutation/_572_m3.json`）：

| | v2（571） | 572 收口后 |
|---|---|---|
| M3 逃逸 | **52**（(a)17 + (b)35） | **0** |
| M3 可判 | 65 | **65**（不变） |
| 逃逸按点 | 删条目 11 / 删键 6 / 追加样板 35 | **（空）** |

* (a) 17 条由**基线规则**收（删项 ⇒ 计数 < 基线 ⇒ warn）；
* (b) 35 条由**单点接入**收（追加通用候选 ⇒ warn）；
* **(c) = 0** ⇒ 没有"结构性堵不住"的条目需要登记（任务书要求的登记条款本次无内容）。

**毒样例**（新增 4 条，poison **110 → 114**）：
`P72` 断言数少于基线须 warn ✅ / `P72-阴` 计数等于基线须放行 ✅ /
`P73` any-of 混入通用候选须 warn 不 block ✅ / `P73-阴` any-of 候选全有真实出处须放行 ✅。
（P73 第一版载荷**写错**：沙箱卡里具体候选没有出处 ⇒ 走了 block 路径；改用卡内 `symbol_map`
给候选真实出处后才是真考到"混入通用候选"这一步——记下来免得后人重复踩。）

## 5 · 收工验收（fresh）

| 项 | 实测 |
|---|---|
| 三分类计数表 | (a) 17 / (b) 35 / (c) 0（§1） |
| gate（**存量零误伤硬约束**） | `规则 63 条 · 命中 141 (block=0 warn=136 advice=5)` —— 命中数与改前**逐字相同**；warn 增量**0**（无新命中卡 id 可列） |
| M3 复跑 | 逃逸 **52 → 0**（judged 65 不变） |
| poison | **114/114** · RULE-COVERAGE **38/63** |
| replay | `confirm=56 refute=0 infra_error=0` |
| pytest fast / slow | **exit 0 / exit 0**（slow 首跑 exit=1 已查清并重冻结，见 §6） |
| ruff | `All checks passed!` |
| `tool_integrity.py --check` | exit 0（改 gate/poison ⇒ 同 commit 重钉） |
| 受控目录 | `git diff --quiet -- evidence/ atoms/` exit 0 |

## 6 · 偏差表

1. **任务 1/2 合一个 commit**（`69ca9bc`）：两者都改 `gate_engine.py` 与 `poison_drill.py`
   （本环境无交互式 `git add -p`）⇒ 合一并在 message 里按任务分节，可逐节 review。
2. **slow 首跑 exit=1**：新基线规则**额外**命中"删 run_match_keys"的变体 ⇒ 既有冻结结论的规则集
   从 `[EV-OUT-UNDECLARED-KEY]` 变为 `[EV-ASSERT-COUNT-BELOW-BASELINE, EV-OUT-UNDECLARED-KEY]`
   （**两道闸同时看得见是预期**，不是回归）⇒ 按实测重冻结（`0a4dc80`），复跑 exit 0。
3. **新规则 id 的覆盖债已当场还清**：新增 `EV-ASSERT-COUNT-BELOW-BASELINE` 同时配了 P72/P72-阴
   （RULE-COVERAGE 分母 62→63、分子 37→38）——不是"新造规则欠覆盖率"。
4. **不补黑名单**：全程只复用 553 的 `_is_universal_symbol`（(b) 的 35 条追加符号全部被判通用）；
   (c) 为 0 ⇒ 没有任何"硬凑符号"的补丁。
5. **P73 载荷第一版写错**（见 §4）——如实记录，避免后人以为规则没生效。

## 7 · 交人 / 下一批

* 本批**不做**（按任务书）：任务 2 overturned 事件通道、任务 3 ruff 914 分批（`select` 已钉，
  可直接逐族 `--fix`）、V-iso 阴面扩覆盖、自动 KG、PoC#3/#4/#5。
* **基线维护纪律（新）**：任何"有意精简断言/键"的改动都必须显式跑
  `gate_engine.py --update-assert-baseline` 并在 commit message 说明；否则门禁会红——
  这是设计目标（**卡片变弱必须留痕**）。
