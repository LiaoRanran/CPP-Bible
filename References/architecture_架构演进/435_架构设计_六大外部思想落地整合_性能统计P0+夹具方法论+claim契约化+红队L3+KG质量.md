---
id: 435
title: 架构设计 六大外部思想落地整合 性能统计P0+夹具方法论+claim契约化+红队L3+KG质量
status: active
type: architecture-note
created_at: 2026-09-13
---
# 435 架构设计：六大外部思想的落地整合（性能统计P0 + 夹具方法论 + claim契约化 + 红队L3 + KG质量）

> 日期：2026-09-13。基于 434 的六个方向外部调研，设计阙疑的架构改进。最紧急的是性能卡统计严谨性（P0）——在送去对抗之前必须修复。

---

## 一、P0：性能卡统计严谨性升级

### 1.1 问题

PERF-004 报告"7 轮中位数 18.86×"，但同机跨运行波动到 8.78×（2×+）。当前性能卡：
- 只有中位数，没有置信区间
- 样本量 7，远不够（≥30）
- 没有统计显著性检验
- 固定顺序执行，有顺序效应

**这是对抗模型的一击必杀点**——"你的 18.86× 置信区间是多少？p-value 是多少？"答不上来就是不严谨。

### 1.2 性能夹具规范 v2.0

```
性能夹具必须：
1. 样本量 ≥30 轮（不是 7）
2. 报告：中位数 + 95% 置信区间 + 标准差
3. 统计检验：Mann-Whitney U 检验（非参数，适合性能数据）
4. 效应量：Cohen's d 或 Cliff's delta
5. 随机顺序执行（消除顺序效应）
6. 环境记录：CPU 型号、核心数、负载、编译器版本
7. 锚方向不锚倍数，但倍数必须带置信区间
```

### 1.3 性能卡 actual 格式

```yaml
actual:
  run_match:
    - "tight_median_ns=562500600"
    - "tight_ci95_low=550000000"
    - "tight_ci95_high=575000000"
    - "padded_median_ns=29824800"
    - "ratio_median=18.86"
    - "ratio_ci95_low=17.5"
    - "ratio_ci95_high=20.2"
    - "mann_whitney_p=0.0001"
    - "cohens_d=2.5"
    - "sample_size=30"
    - "cpu_model=AMD Ryzen 9 7950X"
    - "nproc=32"
```

### 1.4 gate 规则：EV-PERF-STATS（block）

性能卡必须包含：
- sample_size ≥30
- 置信区间（ci95_low/high）
- 统计检验 p-value
- 否则 block

### 1.5 存量性能卡处理

存量 3 张性能卡（PERF-003/004/CONC-002）：
- 标记为 `stats_legacy: true`（过渡期 warn，不 block）
- 下次重跑时按 v2.0 规范升级
- 卡内诚实声明"本卡统计方法为旧版，样本量不足"

---

## 二、P1：夹具设计方法论（变形测试 + 属性测试）

### 2.1 变形关系（MR）形式化

每个夹具必须声明变形关系：

```yaml
# 夹具 frontmatter 新增
metamorphic_relations:
  - id: MR-01
    description: "布局从 tight 改为 padded，性能应提升 ≥10×"
    input_transform: "change layout from tight to padded"
    expected_output_change: "runtime decreases by ≥10×"
    verified_by: "EV-MEM-045"
```

### 2.2 性质声明（Property Declaration）

每个夹具必须声明验证的性质：

```yaml
properties:
  - id: PROP-01
    type: invariant  # invariant/round_trip/commutativity/identity/idempotence
    description: "arena 元数据不随分配规模变化"
    verified_by: "arena_meta_total_n1=32, arena_meta_total_n2=32"
```

### 2.3 活性对照的形式化

活性对照 = invariant 性质的实例化。当前靠人写，应该自动检查：

```
如果 claim 说"X 随规模变"，夹具必须输出 X(n1) 和 X(n2)，且 X(n1) != X(n2)
如果 claim 说"X 不随规模变"，夹具必须输出 X(n1) 和 X(n2)，且 X(n1) == X(n2)
```

gate 规则：EV-ACTIVE-CONTROL（warn）——性能/机制卡必须有活性对照。

### 2.4 反例自动缩小（Shrinking）

红队发现问题后，自动缩小到最小复现：
- 从完整夹具开始，逐步删除代码
- 每步验证问题是否仍然存在
- 输出最小复现夹具

这是 v8.0 M4（自治进化）的功能，当前先做手动流程。

---

## 三、P1：claim 契约化 v2.0（LLM 可验证性四层）

### 3.1 四段契约 + 断言三元组

```yaml
claim:
  precondition: "4 线程，各累加 1e7 次，相邻布局 vs 隔离布局"
  assertion: "相邻布局比隔离布局慢，95% CI [17.5×, 20.2×]"
  invariant: "唯一变量 = 内存布局"
  falsification: "如果隔离布局也慢，则 claim 不成立"
  triple:  # (Subject, Predicate, Object)
    subject: "多线程独立变量"
    predicate: "因共享缓存行而变慢"
    object: "约一个数量级"
```

### 3.2 四层验证

| 层 | 验证内容 | 机器可验证 |
|---|---|---|
| L1 结构 | claim 有四段 + triple | ✅ |
| L2 内容 | precondition 在夹具中实现 | ✅ |
| L3 逻辑 | assertion 数值在 .out 中，invariant 真的唯一 | ✅ |
| L4 语义 | claim 的 C++ 语义对不对 | ❌（红队/人审） |

### 3.3 gate 规则：ATOM-CLAIM-CONTRACT（block）

新原子必须：
- claim 有 precondition/assertion/invariant/falsification 四段
- assertion 的数值必须在 .out 中出现
- invariant 必须有对应的活性对照
- 否则 block

存量原子过渡期 warn。

---

## 四、P1：红队成熟度 L2→L3

### 4.1 L3 的核心标志

- 攻击用例回归库（419）——可测量拦截率
- 检测覆盖率——A1-A10 每类 ≥2 条毒样例（424）
- MTTR（Mean Time to Remediate）——从发现到修复的平均时间

### 4.2 红队质量度量

```json
{
  "redteam_maturity": "L3",
  "attack_coverage": {"A1": 5, "A2": 3, ..., "A10": 2},
  "intercept_rate": 0.65,
  "mttr_days": 3.5,
  "false_positive_rate": 0.05
}
```

### 4.3 红队提示词的质量保证

红队提示词必须包含：
- can't-miss 清单（≥10 条）
- 错误预测 ≥3 条
- 每条阻断必须配"替代解释 ≥1"
- 两阶段盲读协议
- 攻击面 A1-A10 覆盖检查

---

## 五、P2：知识图谱质量四维评估

### 5.1 Consistency（已有）

- 417 ATOM-REL-CONFLICT（矛盾检测）
- ATOM-REL-DAG（无环）
- ATOM-REL-TARGET（目标存在）

### 5.2 Completeness（新增）

gate 规则：ATOM-REL-COMPLETENESS（advice）
- 每颗原子至少有 1 条 prerequisite 或 specializes
- 每颗 verified 原子至少被 1 颗其他原子引用（或被误解引用）
- 孤立原子给 advice

### 5.3 Currency（新增）

- 428 data_freshness 字段
- performance/tool_observation 类原子的 last_verified 过期 warn

### 5.4 Correctness（已有）

- replay 双平台 confirm
- 红队/人审

---

## 六、落地优先级

### 第一批（P0，送对抗前必须做）

- [ ] 性能卡统计严谨性升级（1.1-1.5）
- [ ] 存量 3 张性能卡标记 legacy + 诚实声明

### 第二批（P1，v7.0→v7.5）

- [ ] 夹具变形关系形式化（2.1）
- [ ] 活性对照自动检查（2.3）
- [ ] claim 契约化 v2.0（3.1-3.3）
- [ ] 红队 L3 度量（4.1-4.3）

### 第三批（P2，v8.0）

- [ ] 性质测试自动生成（属性测试）
- [ ] 反例自动缩小（shrinking）
- [ ] 知识图谱完整性评估（5.2）
- [ ] claim L4 语义验证（需 LLM 辅助）

---

## 七、为什么这些改进是"送去对抗前必须做的"

| 改进 | 不做的后果 | 对抗模型的攻击 |
|---|---|---|
| 性能统计 P0 | 性能数据不可信 | "18.86× 的置信区间是多少？" |
| 夹具方法论 | 夹具设计靠经验，无理论基础 | "你的唯一变量真的唯一吗？" |
| claim 契约化 | claim 不可机器验证 | "你的 claim 怎么证伪？" |
| 红队 L3 | 红队质量不可度量 | "你的红队拦截率是多少？" |
| KG 质量 | relations 可能不完整 | "这颗原子为什么没有 prerequisite？" |

**核心判断**：当前阙疑在"形式自律"上已经很强（42 规则、47 毒样例、三分类 replay），但在"语义严谨性"上还有明显缺口——性能统计、claim 可验证性、夹具理论基础。这些是对抗模型一定会攻击的点，必须在送对抗前补上。

累计 59 份（374-435）。
