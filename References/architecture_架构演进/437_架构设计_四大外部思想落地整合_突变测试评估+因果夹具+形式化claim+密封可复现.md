---
id: 437
title: 架构设计 四大外部思想落地整合 突变测试评估+因果夹具+形式化claim+密封可复现
status: active
type: architecture-note
created_at: 2026-09-13
---
# 437 架构设计：四大外部思想的落地整合（突变测试评估 + 因果夹具 + 形式化claim + 密封可复现）

> 日期：2026-09-13。基于 436 的四个方向外部调研，设计阙疑的架构改进。核心：用突变测试评估 gate 质量，用因果推断指导夹具设计，用形式化验证深化 claim 契约，用密封构建保证可复现性。

---

## 一、P0：性能卡 v2.0 完整规范（因果推断 + 可复现性）

### 1.1 因果推断框架下的性能实验

```
处理（Treatment）= 改变一个变量（布局/同步原语/优化档）
对照（Control）= 不改变该变量
结果（Outcome）= 运行时间
处理效应（ATE）= E[Y(treatment) - Y(control)]
```

### 1.2 性能夹具必须满足的因果推断条件

1. **可识别性**：只有处理变量变化，其他变量不变（唯一变量原则）
2. **随机化**：执行顺序随机（消除顺序效应）
3. **充分样本量**：≥30 轮（中心极限定理）
4. **控制混杂**：记录 CPU 负载、电源模式、其他进程

### 1.3 性能卡 actual 格式 v2.0

```yaml
actual:
  run_match:
    # 处理效应
    - "ate_ratio_median=18.86"
    - "ate_ratio_ci95_low=17.5"
    - "ate_ratio_ci95_high=20.2"
    # 统计检验
    - "mann_whitney_u_p=0.0001"
    - "cohens_d=2.5"
    # 样本量
    - "sample_size=30"
    - "randomized_order=1"
    # 环境信息（可复现性）
    - "cpu_model=AMD Ryzen 9 7950X"
    - "nproc=32"
    - "os=Windows 11 23H2"
    - "compiler=gcc 15.3.0"
    - "optimization=-O2"
    - "power_mode=high_performance"
    - "avg_load_pct=5"
```

### 1.4 gate 规则：EV-PERF-RIGOR（block）

性能卡必须包含：
- sample_size ≥30
- 置信区间（ci95_low/high）
- 统计检验 p-value
- 环境信息（cpu_model、os、compiler、optimization）
- 否则 block

### 1.5 存量性能卡处理

存量 3 张性能卡（PERF-003/004/CONC-002）：
- 标记 `stats_legacy: true`（过渡期 warn）
- 卡内诚实声明"本卡统计方法为旧版，样本量不足，环境信息不完整"
- 下次重跑时按 v2.0 规范升级

---

## 二、P1：gate 规则质量评估（突变测试方法论）

### 2.1 核心指标：拦截率（Intercept Rate）

```
拦截率 = 被拦住的攻击用例数 / 总攻击用例数
```

这等同于突变测试的"变异得分"。

### 2.2 三级评估标准

| 拦截率 | 等级 | 含义 |
|---|---|---|
| <35% | 弱 | 只拦住直白违规，挡不住组合攻击 |
| 35-60% | 中等 | 拦住大部分形式违规，语义攻击有盲区 |
| 60-80% | 不错 | 形式+部分语义攻击可拦 |
| ≥80% | 健壮 | 可送对抗 |

**阙疑当前**：402 对抗 35% = 弱水平。v7.0 目标 ≥60%。

### 2.3 攻击用例库的分级

```
L1 毒样例（人工设计的违规）：P1-P33，验证"规则能拦住设计的违规"
L2 攻击用例（真实对抗中发现的）：419 库，验证"规则能拦住真实攻击"
L3 自动生成变异体（LLM 自动生成）：v8.0，持续扩展攻击面
```

### 2.4 自动毒样例生成（v8.0）

用 LLM 自动生成变异体（违规的卡/夹具/工件），然后跑 gate：
- 拦住了 → 已有规则覆盖，不需要新毒样例
- 没拦住 → 新毒样例候选，需要新规则或规则改进

这是 v9.0 自治红队的基础。

---

## 三、P1：夹具设计方法论 v2.0（变形测试 + 因果推断）

### 3.1 夹具必须声明的三个要素

```yaml
# 1. 变形关系（Metamorphic Relation）
metamorphic_relation:
  input_transform: "布局从 tight 改为 padded"
  expected_output_change: "运行时间减少 ≥10×"

# 2. 因果设计（Causal Design）
causal_design:
  treatment: "内存布局"
  control: "相邻布局（tight）"
  treatment_group: "隔离布局（padded）"
  controlled_vars: ["线程数=4", "迭代数=1e7", "编译器=gcc 15.3", "优化档=-O2"]
  randomization: "执行顺序随机"

# 3. 性质声明（Property Declaration）
properties:
  - type: invariant
    description: "padded 布局的变量不在同一缓存行"
    verified_by: "padded_shares_line=0"
  - type: differential
    description: "padded 比 tight 快"
    verified_by: "ate_ratio > 1"
```

### 3.2 gate 规则：EV-FIXTURE-DESIGN（warn）

性能/机制卡的夹具必须有：
- metamorphic_relation（变形关系）
- causal_design（因果设计，含 controlled_vars）
- 至少 1 个 property（性质声明）
- 否则 warn

### 3.3 唯一变量的机器验证

gate 规则：EV-SINGLE-VARIABLE（warn）
- 对处理组和对照组的源码做 diff
- 如果 diff 超过 1 个逻辑块，warn（可能不是唯一变量）
- 这是"唯一变量"原则的机器验证

---

## 四、P2：claim 契约化深化（形式化验证）

### 4.1 claim 四段 + 逻辑一致性检查

```yaml
claim:
  precondition: "4 线程，各累加 1e7 次"
  assertion: "相邻布局比隔离布局慢 ≥10×"
  invariant: "唯一变量 = 内存布局"
  falsification: "如果隔离布局也慢，则 claim 不成立"
```

### 4.2 逻辑一致性检查（轻量形式化）

用 SMT solver（如 Z3）验证：
- precondition 和 invariant 是否矛盾？
- assertion 是否可满足？
- falsification 是否是 assertion 的逻辑否定？

**当前阶段**：只做结构检查（有没有这四段），不做逻辑验证。
**v8.0**：引入 Z3 做轻量逻辑验证。

### 4.3 断言三元组（可检索、可验证）

```yaml
claim_triple:
  subject: "多线程独立变量"
  predicate: "因共享缓存行而变慢"
  object: "约一个数量级"
```

三元组使得 claim 可以：
- 被检索（"哪些 claim 是关于缓存行的？"）
- 被验证（subject 是否在夹具中存在？predicate 是否有证据？）
- 被关联（相似 subject 的 claim 可以互相引用）

---

## 五、P2：密封可复现性（Hermetic Reproducibility）

### 5.1 环境信息完整记录

每张卡必须有：
```yaml
environment:
  cpu_model: "AMD Ryzen 9 7950X"
  nproc: 32
  os: "Windows 11 23H2"
  compiler: "gcc 15.3.0"
  optimization: "-O2"
  artifact_sha256: "..."
```

gate 规则：EV-ENV-COMPLETE（warn）——卡中缺少 environment 字段给 warn。

### 5.2 构建确定性

当前已做到：
- 工件 sha256 记录 ✅
- command 字段记录构建命令 ✅
- 双平台 replay 验证 ✅

待做（v8.0）：
- Docker 构建环境锁定
- 编译器版本精确到 patch level
- 库版本记录

### 5.3 性能数据的环境控制

性能夹具必须：
- 记录运行时的 CPU 负载（avg_load_pct）
- 记录电源模式（power_mode）
- 建议在 high_performance 模式下运行
- 多次运行取中位数+置信区间

---

## 六、落地优先级

### 第一批（P0，送对抗前必须做）

- [ ] 性能卡 v2.0 规范（1.1-1.5）
- [ ] 存量 3 张性能卡标记 legacy + 诚实声明

### 第二批（P1，v7.0→v7.5）

- [ ] gate 规则质量评估（拦截率指标，2.1-2.3）
- [ ] 夹具设计方法论 v2.0（3.1-3.3）
- [ ] 环境信息完整记录（5.1）

### 第三批（P2，v8.0）

- [ ] claim 逻辑一致性验证（SMT solver，4.2）
- [ ] 自动毒样例生成（2.4）
- [ ] Docker 密封构建（5.2）
- [ ] 断言三元组检索（4.3）

---

## 七、为什么这些改进是"送去对抗前必须做的"

| 改进 | 不做的后果 | 对抗模型的攻击 |
|---|---|---|
| 性能统计 P0 | 性能数据不可信 | "你的 ATE 置信区间是多少？" |
| 拦截率评估 | gate 质量不可度量 | "你的 42 条规则拦截率是多少？" |
| 夹具方法论 | 夹具设计无理论基础 | "你的唯一变量真的唯一吗？" |
| 环境信息 | 实验不可复现 | "你的 CPU 型号是什么？" |
| claim 契约化 | claim 不可验证 | "你的 claim 怎么证伪？" |

**核心判断**：434-435 发现了"语义严谨性缺口"，436-437 给出了完整的理论基础和落地路径。性能统计 P0 是最紧急的——它是对抗模型的第一攻击点。

累计 61 份（374-437）。
