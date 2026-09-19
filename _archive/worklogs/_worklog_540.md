# 540 建设日志：T0 侦察结论（未改码）+ T1/T2 交接

> 依据：`References/architecture_架构演进/540_进化闭环_修M3M4逃逸+mutation性能优化.md`
> 纪律：不 push / 不 golden accept / 不改 56 卡；**做不完停在 T 边界、不留半成品**。本批**未做任何代码改动**（无 commit），只做 T0 的 Read 侦察并把精确施工点交出去。

## 幂等进度看板

```
T0 扩恒真/判别力到 contains/contains_any   [~] 侦察完成（结论见 §1）；**未改码**（原因：本会话预算见底，改核心规则必须配正反例毒样例+全量 pytest）
T1 mutation_fuzz 性能优化                  [~] 其中 2 项经核实**已满足**（见 §2.1）；基线缓存与 cppbible 接入未做
T2 M2 跨平台路径弱检测（P2）               [ ] 未做
```

## 0. 开工基线（按 539 收工实测，HEAD=`f034d2c`）

`gate 60 规则 · 141 命中 (block=0 warn=136 advice=5)` · `poison 90/90` · `replay confirm=56` · `pytest -m fast -q` **280**（slow 组另含 `test_mutation_fuzz.py` 5 例）· mutation smoke（`--limit 2 --operators M2,M3,M4,M5,M6`）：**变体 28 / blocked 14（严格 13）/ escaped 12 / n_a 2 / 严格率 46.2%**（逃逸分布 M2 6 · M3 4 · M4 2）。

---

## 1. T0 侦察结论（**重要：与 540 的假设不同**）

540 §T0 的背景假设是"M4 漏网因为黑名单缺 `.file`"。**实测磁盘不是这样**：

1. `tools/gate_engine.py:1463` 的 `UNIVERSAL_SYMBOLS` **已经包含** `.file` / `.section` / `.text` / `.data` / `.bss` / `.align` / `.p2align` / `.quad`（530 T2 落的），并有 `_is_universal_symbol()`（:1486）与裸 `.`-伪指令 / 裸寄存器判定（:1479）。
2. 通用符号的**恒真断言拦截路径已存在**：`:1599-1621` 遍历卡上所有 `artifact_assert` 条目，经 `_assert_targets(r)` 取 `texts`，凡 `_is_universal_symbol(t)` 一律进 `bad_universal` ⇒ `:1645` 出 **block**（`EV-ASSERT-SYMBOL-MAPPED`）。
3. ⇒ 所以 M4 的逃逸**不是"缺黑名单"**，而是**形状/通道没走到那条路径**。两个候选根因（下一步必须先分辨，别盲改）：
   - **(a) `contains_any` 的目标解析**：`:1508` 对 `contains_any/absent_any` 走 `any_of=True` 分支，`texts` 来自 `text` 的候选列表。我的 M4 载荷是**单行 flow map** `{kind: contains_any, symbol: main, text: ".file"}`——若零依赖解析器对该形态**静默截断/丢字段**，该条目根本没进 `meta["artifact_assert"]`，后续自然零命中（**这最可能**，与 533 `schema_parse_probe.txt` 记录的"跨行 flow map 被截断"同族）。
   - **(b) kind 门控**：`:1630-1644` 的 `text` 侧无判别力检查（空/纯中文 → block、通用助记符 → advice）**显式只覆盖 `contains_in/absent_in`**（`:1632` `if kind not in ("contains_in", "absent_in"): continue`）——即 540 说的"扩到 `contains/contains_any`"这条**确实是缺口**，但它是**第二条**原因，不是 M4 漏网的第一原因。

**下一步（照做即可，不用重新设计）**：
```powershell
# ① 先分辨根因 (a)：把 M4 变体写盘，看解析后 artifact_assert 里到底有没有那条注入
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'tools'); import mutation_fuzz as mf, atom_evidence_replay as rp; t=open('evidence/conc/EV-CONC-001.md',encoding='utf-8').read(); v=dict(mf.mut_m4(t))[[k for k in dict(mf.mut_m4(t)) if '.file' in k][0]]; import json; print(json.dumps(rp.parse_frontmatter(v).get('artifact_assert'), ensure_ascii=False)[:600])"
```
- 若注入条目**不在**解析结果里 ⇒ 根因是解析器对 flow map 的截断（按 533 的块式书写约束处理：要么修解析器，要么让 M4 生成**块式**注入形态，并按 540 §5 把"flow map 静默截断"也做成一条 warn/毒样例）。
- 若注入条目**在**但没被拦 ⇒ 根因 (b)：把 `:1630-1644` 的 `text` 侧检查从 `contains_in/absent_in` 扩到 `contains/contains_any`（540 T0 扩展 2），并且 **M3 的专门点**（同命题用全文 `contains` 且该断言在工件全区间成立 ⇒ warn「全文存在性断言，判别力弱」）落在同一处。
- 验收复跑（540 原文口径）：`tools/mutation_fuzz.py --limit 2 --operators M2,M3,M4,M5,M6`，**M3/M4 逃逸应降到接近 0**（M2 类本批不修，仍 escaped 属预期）；新 warn 命中数如实报、不 `--accept`；配 poison 正反例 + pytest；gate block 不增、replay confirm=56。

> **为什么这一批没直接改**：改的是**核心规则**（`gate_engine.py` 是 `.tool_checksums` 钉住的 5 个文件之一，改了要重钉）且要配"正反例毒样例 + 全量 pytest（含 slow）"，本会话上下文预算不足以一次做完并验证——按纪律**停在边界**，宁可不改也不留半成品规则。

---

## 2. T1 性能优化 · 侦察结论

### 2.1 540 列的四条里，两条**已经满足**

1. **分算子跑**：`--operators M1,M2,...` 已实现（539 落地），默认全算子、`--limit` 默认 5 ✓（540 要求的 `--full` 未加：当前用 `--limit` 足够）。
2. **只 M1/M7 跑 replay**：`REPLAY_OPS = {"M1","M7"}`（539 落地，注释在 `tools/mutation_fuzz.py` 顶部）——M2/M3/M4/M5/M6 纯 gate、不碰 replay ✓。

### 2.2 真正的大头（实测观察，未定论）

- `--limit 2` 就跑 >4 分钟 ⇒ 主因是**每个变体都跑一次完整 `ge.run()`**（含跨卡规则、全库扫描），而不是 replay（replay 只在 M1/M7 触发）。
- 540 §T1.3 的"基线缓存"要落成：把基线 `ge.run()` 结果按卡缓存（当前主循环里 `baseline` 只算一次，但**每个变体仍各跑一次整轮门禁**——变体的 `_snapshot()` 无法省，除非改成"只跑与该卡相关的规则子集"，即按 `rule.scope`/`target` 过滤）。
- 建议下一轮的两条实招（按性价比排序）：
  1. **按卡批处理**：一张卡的全部变体共用一次"全库扫描"，只对**该卡产出 findings 的规则**（`Finding.target == 卡路径`）做 diff —— 需要把 `ge.run()` 拆成"按目标文件跑"的入口（`rule.scope == "evidence"` 的规则大多只看单卡）；
  2. **算子分组落多个报告再合并**（写进 CLI，避免一次调用过长）。
- cppbible 接入（540 §T1.4）：模式同 `poison`/`cost` 子命令，未做。

---

## 3. 收工

- **本批无 commit**（未改任何正式代码）；本地仍 **ahead 16 个提交（未 push）**。
- 门禁终值：与 §0 基线**逐字一致**（未改码 ⇒ 无回归；已实测项：gate 60/141/block=0/warn=136/advice=5、poison 90/90、mutation smoke 数字同上）。
- **交人项**：
  1. T0 的**根因分辨**必须先做（§1 的一行命令），否则可能改错地方（540 说"黑名单补 `.file`"，实测黑名单里已经有了）。
  2. T0 若走扩展 2，请连同 533 的"flow map 静默截断"一起处理——它可能就是 M4 漏网的真因，且是**解析器级**问题（影响面比单条规则大）。
  3. T1 的 2.2 两条实招属工具内部重构，改动面比 T0 小、收益直接（全量 392 变体从"不现实"到可跑），建议排在 T0 之前或并行。
