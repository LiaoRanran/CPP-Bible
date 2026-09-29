# C7 · 新规则怎么加（666 批）

> 规则引擎是这套系统的**判决层**：67 条规则（`tools/gate_engine.py::RULES`）。
> 加规则的最大风险不是"漏判"，而是"**误报把门禁噪声化**，最后没人看"（狼来了）。
> 因此流程的核心是：**反例驱动 + 存量零误报 + 人审**。

## 1. 五步流程

### 第 1 步 · 提议（必须带反例）
- 写清**痛点**：哪条真错漏了？给出**最小复现**（一个卡片段 / 一段代码 / 一条证据）。
- **禁止**"我觉得应该有这条规则"。没有反例的提议直接退回。

### 第 2 步 · 起草（AI 可做，人只审）
- 在 `tools/gate_engine.py` 里加一个 `Rule` 对象，填齐：
  `id`（命名空间见下）、`title`、`kind`、`quadrant`、`severity`、`scope`、`check`、`basis`、`fix_hint`。
- **命名空间**（已有的按前缀归类）：
  `ATOM-*`（卡面） / `EV-*`（证据） / `PED-*`（教学） / `SYS-*`（系统） / `*` 其他沿用既有前缀。
- `basis` **必须给可点开的出处**（标准条款 / 项目内文档路径），空 `basis` 的 block 规则不许上线。

### 第 3 步 · 反例驱动测试（两道）
1. **正向**：新增夹具必须**被新规则抓住**（写进 `tests/`，与 `poison_drill` 的毒样例同批）。
2. **反向（关键）**：在**存量**上跑一遍，`severity=block` 的规则**必须 0 误报**；
   `warn` 允许有存量命中，但必须能逐条解释（写进报告，不许"反正是 warn"）。

```bash
.venv\Scripts\python.exe -c "import sys;sys.path.insert(0,'tools');import gate_engine as g;[print(f.severity,f.rule_id,f.atom) for f in g.run(include_advice=True) if f.rule_id=='<新 id>']"
```

### 第 4 步 · 审批（**人**）
- `severity=block` 的新规则**必须人签**（谁签、何时、依据）—— 写进 `data/_gate_rules.json` 的登记 + CHANGELOG。
- `warn` / `advice` 可由维护者批（AI 不得自批）。

### 第 5 步 · 上线与记账（四件事，缺一不可）
1. 导出规则清单：`data/_gate_rules.json`（条数必须与 `len(ge.RULES)` 一致 —— 口径见 `docs/caliber_convergence_658.md`）；
2. 更新快照/基线（`tests/__snapshots__/test_output_snapshots.ambr` 等）**并交代旧值**（见 C6 §5）；
3. 更新受影响的计数断言（**从事实源现算**，不写死新值 —— 见 666 A2 的原则）；
4. CHANGELOG 条目 + `research/AI_USAGE_LOG.md`（若 AI 参与）。

## 2. 谁审批

| 严重度 | 审批人 | 备注 |
|---|---|---|
| `block` | **人**（须署名） | 误报成本最高：会挡住所有人的合并 |
| `warn` | 维护者 | 允许存量命中，但必须能解释 |
| `advice` | 维护者 | 只出报告 |

**AI 永远只能到"起草"**：机器不得把规则升级为 `block`、不得修改 `severity` 的语义。

## 3. 怎么测试（本地三类）

```bash
# 1) 单测：新规则的正反例
.venv\Scripts\python.exe -m pytest -n0 -q tests/test_gate_engine*.py
# 2) 毒样例：规则是否真能拦住注入的缺陷
.venv\Scripts\python.exe tools/poison_drill.py --selftest
# 3) 存量基线：条数与分布（快照）
.venv\Scripts\python.exe -m pytest -n0 -q tests/test_output_snapshots.py
```

## 4. 怎么回滚

| 情形 | 做法 |
|---|---|
| 规则误报 | **先降级 `severity`**（block → warn），保留 id 与历史判决可引用 |
| 规则完全错 | 保留 id，`check` 改为"只登记不判"（返回空 findings），并在 `basis` 写明作废原因 |
| 必须删除 | **禁止直接删**（历史判决/报告会引用该 id）；改为"退役"状态 + 注释 + CHANGELOG |

## 5. 红线

- 不许用新规则**掩盖**旧规则的错误（例如把 block 降成 warn 来让门禁变绿 —— 降级必须走 ADR + 人签）。
- 不许在**存量未跑**的情况下上线 block 规则。
- 不许把"文件里出现了某字符串"当成判据（会被注释/文档误报）；判据要基于**结构**（AST / frontmatter 解析）。
