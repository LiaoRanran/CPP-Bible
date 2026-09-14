---
id: 430
title: 苦力Agent大任务包 v7.0工具层全量落地 8子任务串行
status: active
type: architecture-note
created_at: 2026-09-13
---
# 430 苦力Agent大任务包：v7.0 工具层全量落地（8 子任务串行）

> 投喂对象：苦力Agent。任务：按依赖顺序完成 v7.0 工具层剩余 8 个子任务。每个子任务独立 commit、验证全绿、不 push。前置：417（relations 矛盾检测）已完成，414 的 F07/F08 已完成。

---

## 铁律（所有子任务通用）

1. **不 push**：只 commit
2. **每个子任务独立 commit**，message 含子任务编号
3. **每个子任务完成后跑全量门禁**：gate --check / replay --check / poison_drill / pytest
4. **存量零误伤**：gate block=0，replay confirm=56，pytest 全绿
5. **先 Read 再改**：每个子任务开始前，Read 对应的提示词文档 + 相关源码
6. **遇到阻塞立即停**：报告阻塞点，不硬凑、不降级
7. **工具改动分离提交**：不混架构文档/提示词的改动

---

## 子任务清单（按依赖顺序）

### 子任务 1：414 P0-2 — F01 cl 卡永久免检链修复

**提示词文档**：`References/architecture_架构演进/414_苦力Agent执行提示词_402对抗修复批_P0三阻断+P1五高危.md`

**问题**：含 `cl` 命令的卡在 replay 所有校验前 return `infra_error:msvc_unavailable`，gate 只认卡面 `verdict:confirm` → 含 cl 的卡永不复算，`--accept` 一次即永久挂账。

**修法**：
- gate 侧：对 `infra_error:msvc_unavailable` 的卡，`verdict: confirm` 不被接受（给 warn 或 block）
- 或：replay 的 infra_error 必须在卡内声明 `expected_infra_error: msvc_unavailable`，否则 gate 给 warn
- 毒样例：P38（含 cl 命令 + verdict:confirm → gate warn/block）

**验收**：
- 含 cl 的卡不能静默通过
- 存量 56 张卡 0 误伤（存量没有含 cl 的卡）
- pytest 含 TestClMsvcInfra（≥2 例）

---

### 子任务 2：414 P0-3 — F02 编译后覆写修复（426 时序约束第一个应用）

**提示词文档**：`References/architecture_架构演进/414_苦力Agent执行提示词_402对抗修复批_P0三阻断+P1五高危.md`
**架构参考**：`References/architecture_架构演进/426_架构设计_时序约束通用框架_不变量约束优于存在性检查.md`

**问题**：EV-ARTIFACT-PRODUCER 只检查"编译行在 command 中 + -o 绑定"，不检查编译后时序。攻击者可以 `g++ -S -o artifact.asm fixture.cpp && python -c "shutil.copy('other.asm', 'artifact.asm')"`。

**修法**（按 426 时序不变量）：
- 在 gate_engine.py 的 EV-ARTIFACT-PRODUCER 中，新增时序检查：
  1. 找到编译行（含 -o artifact 的 g++/clang++ 行）
  2. 提取编译行之后的命令文本
  3. 检测编译行之后是否有对 artifact 路径的写操作
  4. 写操作检测支持：cp/mv/python -c "shutil.copy"/powershell Copy-Item/cmd copy/> 重定向/>> 追加
- 不是黑名单（列不全），是"artifact 路径出现在写位置"的语义检测
- 如果无法确定语义，给 warn（保守）

**毒样例**：
- P32：编译后 python 覆写 → block
- P33：编译后 powershell 覆写 → block

**验收**：
- P32/P33 被 EV-ARTIFACT-PRODUCER block
- 存量 56 张卡 0 误伤
- pytest 含 TestArtifactProducerTemporal（≥4 例：python/powershell/cp/重定向）
- 402 的 F02 攻击用例复跑 → 被拦住

---

### 子任务 3：414 P1-4~7 — 剩余高危修复

**提示词文档**：`References/architecture_架构演进/414_苦力Agent执行提示词_402对抗修复批_P0三阻断+P1五高危.md`

按文档中的 P1-4（F03 contains_in text 不受通用符号约束）、P1-5（F04 中文/全角 .out 键）、P1-6（F06 虚构 .out 留痕）、P1-7（F09 重复 YAML 键）依次修复。

每个 P1 项：
- 修规则
- 配毒样例
- 写 pytest
- 验证存量 0 误伤

**验收**：
- 4 个 P1 项全部修复
- 毒样例各 ≥1 条
- pytest 各 ≥2 例
- 存量 0 误伤

---

### 子任务 4：425 上游依赖遍历

**提示词文档**：`References/architecture_架构演进/425_苦力Agent执行提示词_415L2上游依赖遍历_改原子前先看谁依赖它.md`

**前置已满足**：417 已完成（relations 解析已扩展）。

**核心**：
- `tools/impact_analysis.py`
- `upstream <atom_id>`：列出所有直接依赖该原子的原子
- 区分"依赖"（prerequisite/specializes/realizes）和"引用"（contrasts/see_also）
- 注册到 cppbible.py
- 零风险：只读 relations

**验收**：
- 对存量 27 颗原子全部能运行，不报错
- `cppbible impact upstream <id>` 可执行
- pytest 含 TestImpactAnalysis（≥5 例）
- 存量 0 误伤

---

### 子任务 5：420 Writer 自检层

**提示词文档**：`References/architecture_架构演进/420_苦力Agent执行提示词_413Writer自检层_7项确定性检查零token.md`

**核心**：
- `tools/writer_selfcheck.py`
- 7 项确定性检查（WC-01 工件同代 / WC-02 断言标签在工件 / WC-03 .out 与 command 同代 / WC-04 活性对照 / WC-05 双平台断言 / WC-06 注释无取值串 / WC-07 自旋有界）
- 零 token：纯文件解析，不调用 LLM
- 验证闭环：用第五批 E1/E2 错误回放，拦住 ≥80%

**验收**：
- 7 项检查全部实现
- 第五批 E1/E2 回放拦截率 ≥80%
- pytest 含 TestWriterSelfcheck（≥7 例）
- 存量 0 误伤（对 verified 原子不报错）

---

### 子任务 6：421 成本追踪

**提示词文档**：`References/architecture_架构演进\421_苦力Agent执行提示词_412成本追踪_cost_tracker_CPVA基线.md`

**核心**：
- `tools/cost_tracker.py`
- 记录每原子/每批次的 token 估算（字符数/3）和窗口数
- 输出 CPVA（Cost Per Verified Atom）基线
- 零风险：只记录，不影响生产流程
- 数据存 `data/cost/`

**验收**：
- `data/cost/` 目录生成
- 对存量 27 颗原子可回溯成本（从 git log 估算）
- CPVA 基线报告生成
- pytest 含 TestCostTracker（≥4 例）
- 不修改任何生产文件

---

### 子任务 7：423 闪卡导出

**提示词文档**：`References/architecture_架构演进\423_苦力Agent执行提示词_405闪卡导出工具_原子+误解→AnkiCSV.md`

**核心**：
- `tools/flashcard_export.py`
- 27 颗 verified 原子 → 27 张 claim 卡
- 80 条误解 → 80 张反例卡
- 合计 107 张
- 输出 Anki CSV + Markdown
- 零风险：只读不写生产文件

**验收**：
- `data/flashcards/anki.csv` 生成，107 张卡
- `data/flashcards/markdown/` 生成，107 个 .md
- 每张卡 Front/Back 非空
- CSV 格式可被 Anki 导入
- pytest 含 TestFlashcardExport（≥6 例）
- `cppbible flashcards export` 可执行

---

### 子任务 8：424 毒样例 A1-A10 分类 + 补 A4/A8/A10

**提示词文档**：`References/architecture_架构演进\424_苦力Agent执行提示词_409毒样例A1-A10分类+补A4A8A10盲区.md`

**前置已满足**：子任务 2（F02）已完成，P32/P33 可验证。

**核心**：
- 给现有 47 条毒样例加 `attack_type:` 标签（A1-A10）
- 补 A4（时序穿链）≥2 条：P32/P33（子任务 2 已建，这里补分类标签）
- 补 A8（间接注入）≥2 条：P34/P35
- 补 A10（供应链）≥2 条：P36/P37
- 毒样例总数 47→53
- `poison_drill.py --by-type` 可执行

**验收**：
- 现有 47 条全部有 attack_type 标签
- A4/A8/A10 每类 ≥2 条
- 毒样例总数 53
- 每条新毒样例实跑验证（预期结果匹配）
- `poison_drill.py --by-type` 输出分类统计
- pytest 含 TestPoisonAttackType（≥6 例）

---

## 全量验收（8 子任务全部完成后）

| 指标 | 目标 |
|---|---|
| gate 规则 | 42→~50 |
| 毒样例 | 47→53 |
| replay confirm | 56（无回归） |
| pytest | 全绿（新增 ≥30 例） |
| 工具注册 | 7 个新工具全部在 cppbible.py |
| 闪卡 | 107 张可导出 |
| CPVA | 有基线数据 |
| 存量误伤 | 0 |

---

## 停止条件

遇到以下情况立即停止，报告阻塞点：
1. 任何子任务导致存量 gate block > 0 或 replay confirm < 56
2. 任何子任务的 pytest 失败且 2 轮修复未解决
3. 发现提示词文档与源码实际状态不符（如 417 的实现与 425 假设不同）
4. 发现新的 P0 阻断（比当前任务更紧急）

---

## 提交规范

每个子任务一个 commit，message 格式：
```
feat(tools): <子任务编号> <简短描述>
```

例：
```
feat(tools): 414 P0-2 F01 cl卡免检链修复
feat(tools): 414 P0-3 F02 编译后覆写时序检查
feat(tools): 425 上游依赖遍历
...
```

8 个子任务 = 8 个 commit（或更多，如果子任务内部分离）。

---

## 不做的事

- 不 push
- 不修改架构文档（414/420/421/423/424/425 是提示词，不是要改的对象）
- 不实现 426 的通用 InvariantChecker 框架（那是晚上好模型的活；子任务 2 只手写 F02 的时序检查）
- 不实现 419 攻击用例回归库（晚上好模型的活）
- 不实现 428 freshness 字段（P2，留待后续）
- 不实现 429 错误模式库（P2，留待后续）
- 不混不同子任务的改动

---

## 为什么这个大任务包合理

- 按依赖顺序：F01/F02（P0）→ P1 → 425（依赖417）→ 420/421/423（零风险）→ 424（依赖F02）
- 每个子任务独立可验证，不会"一个失败全批挂"
- 存量零误伤是硬约束，每个子任务都要验证
- 8 个子任务完成后，v7.0 工具层 7 个工具全部落地，可送去对抗

累计 54 份（374-430）。
