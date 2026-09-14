# 32 条 warn 存量审计报告（499 任务 2）

> 审计对象：`gate_engine.py --check` 在 498 收工后的 32 条 WARN（基线 BLOCK=0 WARN=32 ADVICE=5）。
> 方法：对每条 warn 的命中文件 Read frontmatter + 7 条规则触发逻辑，逐条分类为
> **真债**（文件确实缺东西/有问题）/ **误报**（规则太严或逻辑有问题，文件本身没问题）/
> **可接受**（已知边界/有意为之）。**未修改任何卡文件**（铁律 #3）。
> 每条结论的数字/事实均来自实跑 `gate --check` 输出与文件 Read，无编造。

## 一、开工实测 warn 分布（与提示词基线偏差）

| 规则 | 提示词基线 | 实测 | 涉及文件 |
|---|---|---|---|
| EV-MATRIX-UNBACKED | 15 | **16** | conc 6 + lang 2 + mem 8 |
| EV-OUT-UNDECLARED-KEY | 6 | 6 | conc 5 + lang 1 |
| EV-FALSIFICATION-QUANT | 4 | 4 | hist 1 + mem 3 |
| ATOM-REL-TARGET | 2 | 2 | ub 1（同卡 2 条关系） |
| EV-ASSERT-SYMBOL-MAPPED | 2 | 2 | mem 2 |
| ATOM-PREREQ-READABLE | 1 | 1 | mem 1 |
| EV-SERVES-EXIST | 1 | 1 | mem 1 |
| **合计** | 31 | **32** | |

> ⚠️ **与提示词不符之处 1**：提示词称 EV-MATRIX-UNBACKED=15，实测 **16**（mem 域为 8 张：
> MEM-001/039/040/041/042/043/044/045，非提示词写的 7 张）。提示词总 warn 数 31 也漏算 1。

## 二、分类汇总

| 分类 | 条数 | 占比 | 分布 |
|---|---|---|---|
| 真债 | **1** | 3% | ATOM-PREREQ-READABLE ×1 |
| 误报 | **18** | 56% | EV-MATRIX-UNBACKED ×16 + EV-ASSERT-SYMBOL-MAPPED ×2 |
| 可接受 | **13** | 41% | ATOM-REL-TARGET ×2 + EV-FALSIFICATION-QUANT ×4 + EV-OUT-UNDECLARED-KEY ×6 + EV-SERVES-EXIST ×1 |

**核心结论**：32 条 warn 中真正需要改卡的只有 **1 条**；18 条是**规则逻辑误报**
（单一根因：EV-MATRIX-UNBACKED 把 `actual:` 块整体排除在留痕统计之外）；其余 13 条是
知识库在建过程中的**规划前向引用 / 定性证伪 / 无害诊断冗余**，属可接受。

## 三、32 条逐条清单

| # | 规则 | 文件 | 分类 | 原因 |
|---|---|---|---|---|
| 1 | ATOM-PREREQ-READABLE | atoms/mem/ATOM-MEM-MOVE-002.md | **真债** | frontmatter `prerequisites_readable: false` 且注释"VALUE-001 尚未锻造"，但 `ATOM-MEM-VALUE-001.md` 实际已存在 → 声明与事实矛盾，应改为 `true`（或更新注释） |
| 2 | ATOM-REL-TARGET | atoms/ub/ATOM-UB-GRAY-001.md | 可接受 | 关系 `contrasts: ATOM-UB-ALIAS-001` 目标未锻造（search 0 命中），属规划中前向引用 |
| 3 | ATOM-REL-TARGET | atoms/ub/ATOM-UB-GRAY-001.md | 可接受 | 关系 `prerequisite: ATOM-UB-DEF-001` 目标未锻造（search 0 命中），同上 |
| 4 | EV-ASSERT-SYMBOL-MAPPED | evidence/mem/EV-MEM-017.md | **误报** | 卡断言"lock 前缀应为 0（即断言其**不存在**）"；规则 `bad_other` 分支只查"符号在夹具/工件中出现"，必然对"断言缺失"误报 |
| 5 | EV-ASSERT-SYMBOL-MAPPED | evidence/mem/EV-MEM-035.md | **误报** | 同上：`copyable=0`/`moves` 等均断言"应为 0"，符号本就不该出现 → 规则误报 |
| 6 | EV-FALSIFICATION-QUANT | evidence/hist/EV-HIST-001.md | 可接受 | falsification 为结构性否定（"拷贝即转移"被推翻），定性即充分，强求数字反而失真 |
| 7 | EV-FALSIFICATION-QUANT | evidence/mem/EV-MEM-003.md | 可接受 | 同上（is_copy_constructible 编译期判定，结构性） |
| 8 | EV-FALSIFICATION-QUANT | evidence/mem/EV-MEM-006.md | 可接受 | 同上（decltype 五分类，结构性） |
| 9 | EV-FALSIFICATION-QUANT | evidence/mem/EV-MEM-010.md | 可接受 | 同上（析构严格逆序，结构性，A/B/C 字母表达） |
| 10 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-001.md | **误报** | 见 §四根因：规则 `_raw_without_actual` 剔除 `actual:` 后统计留痕，留痕全在 `actual:` → 误报 |
| 11 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-002.md | **误报** | 同上 |
| 12 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-003.md | **误报** | 同上 |
| 13 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-004.md | **误报** | 同上 |
| 14 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-005.md | **误报** | 同上 |
| 15 | EV-MATRIX-UNBACKED | evidence/conc/EV-CONC-006.md | **误报** | 同上 |
| 16 | EV-MATRIX-UNBACKED | evidence/lang/EV-LANG-001.md | **误报** | 同上 |
| 17 | EV-MATRIX-UNBACKED | evidence/lang/EV-LANG-002.md | **误报** | 同上 |
| 18 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-001.md | **误报** | 同上 |
| 19 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-039.md | **误报** | 同上 |
| 20 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-040.md | **误报** | 同上 |
| 21 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-041.md | **误报** | 同上 |
| 22 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-042.md | **误报** | 同上 |
| 23 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-043.md | **误报** | 同上 |
| 24 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-044.md | **误报** | 同上 |
| 25 | EV-MATRIX-UNBACKED | evidence/mem/EV-MEM-045.md | **误报** | 同上 |
| 26 | EV-OUT-UNDECLARED-KEY | evidence/conc/EV-CONC-002.md | 可接受 | `.out` 含 `run_match_keys` 未声明的诊断键，属无害诊断冗余；卡刻意断言子集 |
| 27 | EV-OUT-UNDECLARED-KEY | evidence/conc/EV-CONC-003.md | 可接受 | 同上 |
| 28 | EV-OUT-UNDECLARED-KEY | evidence/conc/EV-CONC-004.md | 可接受 | 同上 |
| 29 | EV-OUT-UNDECLARED-KEY | evidence/conc/EV-CONC-005.md | 可接受 | 同上 |
| 30 | EV-OUT-UNDECLARED-KEY | evidence/conc/EV-CONC-006.md | 可接受 | 同上 |
| 31 | EV-OUT-UNDECLARED-KEY | evidence/lang/EV-LANG-002.md | 可接受 | 同上 |
| 32 | EV-SERVES-EXIST | evidence/mem/EV-MEM-001.md | 可接受 | `serves: ATOM-MEM-MOVE-001`（search 0 命中，未锻造），属规划前向引用 |

## 四、EV-MATRIX-UNBACKED 16 条 matrix 字段状态表

> 规则触发逻辑（gate_engine.py L974–1018）：`body = _raw_without_actual(raw)` 后统计
> `out`/`run` 留痕；`backed = (len(outs)+len(runs)>=2) or (has_notice and (outs or runs)) or has_law`。
> **关键**：`_raw_without_actual` 把 `actual:` 整块剔除。这 16 张卡的编译器矩阵留痕（run_*/.out）
> **全部写在 `actual:` 块内**，因此规则统计到的留痕数 = 0 → 误报。规则把"权威证据块"
> 排除在"证据"之外，是单一逻辑缺陷。

| 卡 | matrix 字段状态 | actual 块是否含留痕 |
|---|---|---|
| EV-CONC-001~006 | 存在且有内容（含多编译器列表） | 是（run_match_keys + .out） |
| EV-LANG-001~002 | 存在且有内容 | 是 |
| EV-MEM-001/039~045 | 存在且有内容 | 是 |
| **结论** | 16/16 的 `matrix:` 字段**均存在且有内容** | 16/16 的留痕**全在 `actual:`**，被规则排除 |

> 其余 7 条 warn（非 MATRIX）：与提示词分布一致，无新增。

## 五、优先修复建议（按严重度，最多 5 条）

1. **【真债·唯一需改卡】ATOM-MEM-MOVE-002**：把 `prerequisites_readable: false` 改为 `true`
   （或删除该字段），并修正注释"VALUE-001 尚未锻造"——该原子已存在。1 行改动，零风险。
2. **【规则缺陷·高价值，超出苦力权限】EV-MATRIX-UNBACKED**：让 `_raw_without_actual` 后的
   留痕统计**也计入 `actual:` 块内的 run_*/.out 引用**（或单独对 `actual:` 做留痕计数）。
   修后 16 条 warn 直接消失，门禁从 WARN=32 降到 WARN=16。⚠️ 铁律 #3 禁止苦力改规则，
   此处仅记录建议，交好模型裁决。
3. **【规则增强·可选】EV-ASSERT-SYMBOL-MAPPED**：区分"断言符号应存在"与"断言符号应缺失
   （=0）"。当前 `bad_other` 对"缺失型断言"误报 2 条（MEM-017/035）。可加约定：falsification
   中显式写"=0/应为 0"的断言，其符号免 `bad_other` 检查。
4. **【可接受·不修】ATOM-REL-TARGET ×2 / EV-SERVES-EXIST ×1**：目标原子（ALIAS-001/DEF-001/
   MOVE-001）属规划前向引用，待对应原子锻造后自动消失；当前为 KB 在建的正常状态。
5. **【可接受·不修】EV-FALSIFICATION-QUANT ×4 / EV-OUT-UNDECLARED-KEY ×6**：结构性证伪与
   .out 诊断冗余属无害，无需改卡。

## 六、不确定项（按铁律 #4 记录）

- **MATRIX 误报的边界**：若个别卡在 `actual:` 之外**连 prose 也未提及编译器/实测**，则那条
  可能属"真债（缺叙述性留痕）"而非纯误报。16 张同因（留痕全在 `actual:`）高度提示规则逻辑问题，
  但严谨起见建议好模型逐卡复核 prose；本报告按"规则排除 actual: 致误报"主因归类。
- **OUT-UNDECLARED-KEY 的另一种归类**：若认为"run_match_keys 应覆盖 .out 全部发射键"是硬要求，
  则 6 条可改判为"真债（低）"。本报告采"卡刻意断言子集=可接受"，两种归类均可，交好模型定。
