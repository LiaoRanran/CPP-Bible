---
id: 443
title: 落地规格 第一批P0P1三项 夹具方法论v2+claim契约化v2+warn债务治理
status: active
type: architecture-note
created_at: 2026-09-13
---
# 443 落地规格：第一批 P0/P1 三项（夹具方法论 v2.0 + claim 契约化 v2.0 + warn 债务治理）

> 日期：2026-09-13。基于 442 的依赖排序，第一批 3 项无依赖的 P0/P1 落地规格。本文档是"苦力 Agent 照着做就能完成"的级别，不是架构设计。每项包含：目标、schema 定义、gate 规则、存量处理、验证标准。

---

## 任务 1：夹具方法论 v2.0（P1）

### 1.1 目标

把"单变量对照"从"口头纪律"变成"机器可检查的夹具设计规范"。所有新生产的性能/机制卡夹具必须遵循此规范。

### 1.2 夹具 frontmatter 扩展

在 Examples/atoms/_atom_*.cpp 的头部注释中，增加结构化设计声明：

```cpp
/*
 * ATOM FIXTURE DESIGN v2.0
 * -------------------------
 * metamorphic_relation:
 *   input_transform: "内存布局从 tight 改为 alignas(64) padded"
 *   expected_output_change: "运行时间中位数减少 ≥10×"
 *
 * causal_design:
 *   treatment: "内存布局"
 *   control: "相邻布局（tight）"
 *   treatment_group: "隔离布局（padded）"
 *   controlled_vars:
 *     - "线程数=4"
 *     - "迭代数=1e7"
 *     - "编译器=gcc 15.3.0"
 *     - "优化档=-O2"
 *   randomization: "执行顺序随机（7 轮中 tight/padded 交替）"
 *
 * properties:
 *   - type: invariant
 *     description: "padded 布局的变量不在同一缓存行"
 *     verified_by: "padded_shares_line=0"
 *   - type: differential
 *     description: "padded 比 tight 快"
 *     verified_by: "ate_ratio > 1"
 *   - type: activity_control
 *     description: "所有计数器都在累加（活性对照）"
 *     verified_by: "counters_all_advanced=1"
 *
 * single_variable_verification:
 *   method: "diff treatment_group.cpp control_group.cpp，仅布局不同"
 *   status: "verified"
 */
```

### 1.3 gate 规则：EV-FIXTURE-DESIGN（warn）

**触发条件**：证据卡的 fixture 字段指向的 .cpp 文件，头部没有 `ATOM FIXTURE DESIGN v2.0` 结构化声明。

**检查项**（全部满足才不 warn）：
1. 有 metamorphic_relation 段（含 input_transform + expected_output_change）
2. 有 causal_design 段（含 treatment/control/treatment_group/controlled_vars）
3. 有 properties 段（至少 1 个 invariant + 1 个 differential + 1 个 activity_control）
4. 有 single_variable_verification 段

**级别**：warn（不 block，因为存量卡没有）

**存量处理**：存量 50 个夹具标记 `fixture_design_legacy: true`，不强制升级。新卡必须有。

### 1.4 验证标准

- 新生产的夹具必须有 v2.0 设计声明
- gate 规则对存量卡不 warn（legacy 标记豁免）
- 红队可以检查"设计声明与实际代码是否一致"（如 controlled_vars 写了线程数=4，代码里真的是 4 线程吗？）

---

## 任务 2：claim 契约化 v2.0（P1）

### 2.1 目标

把 claim 从"一句话"变成"可验证的四段契约"。所有新原子必须遵循。

### 2.2 原子 frontmatter 的 claim 字段扩展

```yaml
claim:
  # 四段契约
  precondition: "4 线程，各累加 1e7 次，x86-64 缓存行 64B"
  assertion: "相邻布局比隔离布局慢约一个数量级"
  invariant: "唯一变量 = 内存布局，其他变量不变"
  falsification: "如果隔离布局也慢（ate_ratio ≤ 1），则 claim 不成立"

  # 断言三元组（可检索、可验证）
  triple:
    subject: "多线程独立变量的内存布局"
    predicate: "因共享缓存行而变慢"
    object: "约一个数量级（10×）"

  # 竞争假设（≥2，红队要求）
  alternative_hypotheses:
    - "慢是因为线程调度，不是缓存行"
    - "慢是因为 false sharing 之外的其他因素"

  # 失效后果（DAL 关联）
  failure_consequence: "DAL B — 学生学到错误的性能优化方向"
```

### 2.3 gate 规则：ATOM-CLAIM-CONTRACT（warn）

**触发条件**：原子的 claim 字段不是结构化对象（还是字符串）。

**检查项**：
1. claim 有 precondition/assertion/invariant/falsification 四段
2. claim 有 triple（subject/predicate/object）
3. claim 有 alternative_hypotheses（≥2）
4. claim 有 failure_consequence

**级别**：warn（存量卡的 claim 是字符串，标记 legacy 豁免）

### 2.4 claim 长度约束

assertion 字段 ≤50 字（298 纪律）。precondition/invariant/falsification 不限制长度。

### 2.5 存量处理

存量 27 颗原子的 claim 是字符串，标记 `claim_legacy: true`，不强制迁移。新原子必须用结构化 claim。

### 2.6 验证标准

- 新原子的 claim 必须是结构化对象
- assertion ≤50 字
- alternative_hypotheses ≥2
- 红队可以检查"falsification 是否真的是 assertion 的逻辑否定"

---

## 任务 3：warn 分类+债务台账（P1）

### 3.1 目标

把 32 条 warn 从"数字"变成"可管理的债务"。每条 warn 有分类、有负责人、有处理计划。

### 3.2 debt_ledger.yaml 扩展

当前 debt_ledger.py 只记录"到期债务"。扩展为完整的技术债务台账：

```yaml
# data/debt_ledger.yaml
- id: DEBT-001
  type: warn
  rule: EV-MATRIX-*
  count: 17
  classification: false_positive  # real_issue / false_positive / legacy_debt / accepted
  description: "MATRIX 规则对已真实跨平台卡的误报——这些卡确实在两个平台跑过，但 MATRIX 规则只看卡面字段"
  estimated_fix_cost: 4  # 小时
  risk: medium  # low / medium / high
  status: accepted  # open / accepted / fixed
  accepted_by: human:liaoranran
  accepted_at: "2026-09-12"
  fix_plan: "v8.0 改进 MATRIX 规则，加入跨平台验证标记"

- id: DEBT-002
  type: warn
  rule: EV-MEM-035 absent lock
  count: 1
  classification: accepted
  description: "EV-MEM-035 的 absent lock 断言，符号只现于夹具注释，是注释剥离的代价"
  risk: low
  status: accepted
  accepted_by: machine:gate_engine
  accepted_at: "2026-09-13"

- id: DEBT-003
  type: warn
  rule: EV-SERVES-EXIST
  count: 1
  classification: real_issue
  description: "EV-MEM-001 的 serves 引用了不存在的概念"
  risk: medium
  status: open
  fix_plan: "第六批修复"
```

### 3.3 技术债务指数（TDI）

```
TDI = (real_issue_count + 0.5 * legacy_debt_count) / total_warn_count
```

| TDI | 等级 | 动作 |
|---|---|---|
| 0-0.3 | 绿色 | 持续监控 |
| 0.3-0.6 | 黄色 | 纳入下个迭代 |
| 0.6-1.0 | 红色 | 阻断送对抗 |

**当前估算**：32 条 warn 中，17 条 MATRIX 误报（false_positive）、1 条 EV-MEM-035（accepted）、1 条 EV-SERVES-EXIST（real_issue）、13 条其他（待分类）。TDI ≈ (1 + 0.5*?) / 32，需要实际分类后计算。

### 3.4 gate 规则：WARN-CLASSIFIED（advice）

**触发条件**：存在未分类的 warn（debt_ledger.yaml 中没有对应条目）。

**检查项**：每条 gate 输出的 warn，必须在 debt_ledger.yaml 中有对应条目（按 rule 名匹配）。

**级别**：advice（不 block 不 warn，只是提醒）

### 3.5 golden_lock 与债务台账的联动

- golden_lock accept warn 时，自动在 debt_ledger.yaml 中创建条目（classification=accepted）
- 债务台账中的 real_issue 修复后，自动从台账中移除（status=fixed）
- 每次 golden_lock sync 时，检查债务台账与实际 warn 是否一致

### 3.6 验证标准

- 32 条 warn 全部分类（在 debt_ledger.yaml 中有条目）
- TDI 计算正确
- 新产生的 warn 自动进入台账（golden_lock accept 时）
- 债务台账与实际 warn 一致（没有"台账有但实际没有"或"实际有但台账没有"）

---

## 执行顺序

三项无依赖，可并行：
1. 任务 1（夹具方法论）：改 gate_engine.py 加 EV-FIXTURE-DESIGN 规则 + 写规范文档
2. 任务 2（claim 契约化）：改 gate_engine.py 加 ATOM-CLAIM-CONTRACT 规则 + 写规范文档
3. 任务 3（warn 债务治理）：扩展 debt_ledger.py + 分类 32 条 warn + 改 gate_engine.py 加 WARN-CLASSIFIED

每项独立 commit，验证全绿（gate block=0、replay 56/56、poison 全过、pytest 全过）。

---

## 验收标准

全部完成后：
- gate 规则 42→45（+3）
- 毒样例 +3（每条新规则 1 个毒样例）
- pytest +3（每条新规则 1 个测试）
- 32 条 warn 全部分类
- TDI 有基线值
- 存量卡标记 legacy，新卡必须遵循新规范
- 门禁全绿（block=0，warn 可能增加，因为新规则对存量卡给 warn——但存量卡有 legacy 豁免，所以 warn 数不变）

累计 67 份（374-443）。
