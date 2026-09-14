---
id: 484
title: 成本与Token经济学详细方案 预算门禁 ROI评估 级联路由 成本趋势
status: active
type: architecture-note
created_at: 2026-09-14
---
# 484 成本与 Token 经济学详细落地方案
## 预算门禁 + ROI 评估 + 级联路由正式化 + 成本趋势

> 生成时间：2026-09-14
> 前置：cost_tracker.py 183 行已存在（421 批次），有 record/report/cpva/backfill 功能，但未接入任何决策流程
> 用户核心诉求："烧多少 token 一点不浪费，性能和质量都压满"

---

## 一、现状评估

### 已有

- `tools/cost_tracker.py`（183 行）：记录每颗原子的 token 消耗估算（chars/3）
- 6 个阶段：fixture / evidence_cards / redteam / gate_fix / human_review / other
- CPVA 基线：27 颗原子平均 5765 tok/颗
- 数据存储：`data/cost/<atom_id>.json`

### 缺失

1. **没有预算**：每颗原子可以无限烧 token，没有上限
2. **没有门禁**：超预算不报警、不阻断
3. **没有 ROI**：只记录花了多少，不评估值不值
4. **没有趋势**：只看单颗，不看批次趋势
5. **没有级联路由**：任务难度分类和模型路由没有正式化
6. **没有实时监控**：Agent 生产过程中不知道已经花了多少

---

## 二、成本预算体系

### 2.1 预算分级

按原子的域/类型/复杂度设定 token 预算：

| 类型 | 复杂度 | 预算（tok） | 说明 |
|---|---|---|---|
| beginner 机制 | 低 | 6,000 | 单夹具、单卡、无性能数据 |
| beginner 陷阱 | 低 | 8,000 | 含 sanitizer 演示 |
| intermediate 机制 | 中 | 12,000 | 双平台、多断言 |
| intermediate 性能 | 中高 | 18,000 | 含性能打印、双构建 |
| advanced 并发 | 高 | 25,000 | 含 TSan、多线程 |
| advanced UB | 高 | 20,000 | 含多编译器差分 |
| 跨域综合 | 极高 | 35,000 | 多夹具、多卡、跨域 |

### 2.2 预算使用规则

- **80% 预警**：token 消耗达到预算的 80% → warn，提醒"快超预算了"
- **100% 阻断**：token 消耗达到预算的 100% → block，必须人审批追加预算
- **追加预算**：人审批后可以追加，每次追加不超过原预算的 50%
- **超支记录**：最终超支的原子，在 worklog 中记录原因（是预算定低了？还是任务膨胀了？）

### 2.3 具体实现

扩展 cost_tracker.py：
```python
def check_budget(atom_id, current_tokens):
    """检查预算，返回 (status, message)
    status: ok / warning / exceeded
    """
    budget = get_budget(atom_id)  # 根据原子类型查预算表
    ratio = current_tokens / budget
    if ratio >= 1.0:
        return 'exceeded', f'超预算：{current_tokens}/{budget}（{ratio:.0%}），需人审批追加'
    elif ratio >= 0.8:
        return 'warning', f'接近预算：{current_tokens}/{budget}（{ratio:.0%}）'
    return 'ok', ''
```

接入 Writer 自检层：每完成一个阶段，自动记录 token 消耗并检查预算。

---

## 三、ROI 评估体系

### 3.1 教学价值量化

每颗原子的"教学价值" = 误解数 × 证据卡数 × 断言数 × 跨平台系数

| 因子 | 权重 | 说明 |
|---|---|---|
| 误解数 | ×2 | 每关联一条误解，价值 ×2 |
| 证据卡数 | ×1 | 每张卡价值 ×1 |
| 断言数 | ×0.5 | 每条断言价值 ×0.5（上限 ×5） |
| 跨平台 | ×1.5 | 双平台验证的原子价值 ×1.5 |
| DAL 等级 | ×1.2 | DAL A/B 的原子价值 ×1.2（教学结论重要） |

### 3.2 ROI 计算

```
ROI = 教学价值 / token 消耗（千 tok）
```

| ROI 等级 | 范围 | 含义 |
|---|---|---|
| 极高 | >5.0 | 花得值，应该多做这类 |
| 高 | 3.0-5.0 | 正常 |
| 中 | 1.5-3.0 | 可以接受 |
| 低 | <1.5 | 花多了，分析原因 |

### 3.3 具体实现

扩展 cost_tracker.py：
```python
def calculate_roi(atom_id):
    """计算原子的 ROI"""
    atom = load_atom(atom_id)
    cost = get_total_tokens(atom_id)
    value = (
        len(atom.get('misconceptions', [])) * 2
        + len(atom.get('evidence', [])) * 1
        + min(get_assertion_count(atom_id) * 0.5, 5)
    )
    if is_cross_platform(atom_id):
        value *= 1.5
    if atom.get('dal') in ('A', 'B'):
        value *= 1.2
    return value / (cost / 1000)
```

每批次生成 ROI 报告，找出 ROI 最低的原子，分析原因。

---

## 四、级联路由正式化

### 4.1 任务难度分类标准

| 难度 | 定义 | 判定标准 | 路由 |
|---|---|---|---|
| 机械 | 有明确规则、可机器验证 | 改字段、补测试、跑门禁、格式调整 | 苦力（成本 1×） |
| 语义 | 需要理解但有验证器 | 写卡、改 claim、红队、写夹具 | 苦力→验证→不通过升级（成本 1×→10×） |
| 创造 | 无明确规则、需要架构判断 | 新工具、新范式、架构设计、新域首颗 | 直接好模型（成本 10×） |

### 4.2 路由规则

1. **机械任务**：直接给苦力，完成后跑门禁验证
   - 通过 → 完成，成本 1×
   - 失败 ≤2 次 → 苦力自己修
   - 失败 >2 次 → 标记"需要升级"，停止

2. **语义任务**：先给苦力，完成后跑门禁+红队验证
   - 通过 → 完成，成本 1×
   - 红队发现阻断 → 升级到好模型，成本 1× + 10×
   - 预期 60% 语义任务苦力能完成

3. **创造任务**：直接给好模型
   - 不浪费苦力的时间（苦力做创造任务大概率做不好）

### 4.3 模型能力档案

```yaml
# docs/kernel/model_marketplace.yaml
models:
  cheap_agent:
    alias: 苦力
    cost_per_1k_tok: 0.01  # 相对值
    strengths: [机械任务, 格式调整, 跑门禁, 补测试]
    weaknesses: [架构设计, 新工具开发, 复杂claim改写]
    success_rate:
      mechanical: 0.85
      semantic: 0.60
      creative: 0.15

  strong_agent:
    alias: 好模型
    cost_per_1k_tok: 0.1  # 10×苦力
    strengths: [架构设计, 新工具开发, 复杂claim改写, 范式突破]
    weaknesses: [成本高, 不适合机械任务]
    success_rate:
      mechanical: 0.95
      semantic: 0.90
      creative: 0.75

  adversarial_agent:
    alias: 对抗模型
    cost_per_1k_tok: 0.05
    strengths: [红队, 对抗测试, 找漏洞]
    weaknesses: [不适合生产]
```

### 4.4 路由工具

`tools/model_router.py`（约 80 行）：
- 输入：任务描述
- 输出：建议模型、预估成本、预估成功率
- 不自动路由，只给建议（人决定）

---

## 五、成本趋势与告警

### 5.1 趋势指标

每批次记录：
- 平均每颗原子 token 消耗
- 平均每轮红队 token 消耗
- 平均每轮对抗 token 消耗
- 级联路由升级率（多少任务从苦力升级到好模型）
- ROI 平均值和中位数

### 5.2 告警规则

| 告警 | 条件 | 级别 |
|---|---|---|
| 单颗原子超预算 | token > 预算 100% | block |
| 批次平均成本上升 | 比上一批高 >30% | warn |
| 升级率过高 | >40% 语义任务需要升级 | warn（苦力能力不足或任务分类不准） |
| ROI 下降 | 批次平均 ROI <1.5 | warn |
| 单卡 replay 耗时 >30s | 性能退化 | warn |

### 5.3 成本报告

每批次结束自动生成 `docs/kernel/cost_report_<batch>.md`：
- 本批次总成本
- 每颗原子的成本和 ROI
- 与上一批的对比
- 超预算原子和原因
- 级联路由统计
- 成本趋势图

---

## 六、实施计划

### 第一阶段（零/低成本，立即做）

1. **预算表**：写 `docs/kernel/cost_budget.yaml`，定义各类型原子的预算
2. **预算检查**：扩展 cost_tracker.py，加 check_budget 函数
3. **接入 Writer 自检**：每完成一个阶段记录 token 并检查预算
4. **模型能力档案**：写 `docs/kernel/model_marketplace.yaml`
5. **路由规则**：写 `docs/kernel/routing_rules.md`，定义任务难度分类和路由规则

### 第二阶段（中等成本，下一批做）

6. **ROI 计算**：扩展 cost_tracker.py，加 calculate_roi 函数
7. **成本报告**：每批次自动生成成本报告
8. **路由工具**：写 `tools/model_router.py`，给任务难度分类建议
9. **趋势追踪**：扩展 metrics_snapshot.py，加成本指标

### 第三阶段（高成本，积累数据后做）

10. **成本门禁**：超预算自动 block（需要人审批流程）
11. **自动路由**：根据任务难度自动选择模型（需要稳定的路由规则）
12. **成本优化建议**：根据历史数据，给出"哪类任务最烧钱、怎么优化"的建议

---

## 七、预期效果

| 指标 | 当前 | 第一阶段后 | 第三阶段后 |
|---|---|---|---|
| 单颗原子平均成本 | 5765 tok | 5765 tok（有预算但不强制） | <5000 tok（超预算被拦） |
| 语义任务苦力完成率 | 未知（人工路由） | 60%（正式化后） | 70%（路由优化后） |
| 成本可观测性 | 无 | 有（每颗原子有记录） | 有（实时监控+告警） |
| ROI 评估 | 无 | 有（每批次报告） | 有（自动优化建议） |
| 总成本 | 未知 | 可量化 | 降低 30-50%（级联路由） |

---

## 八、和现有系统的集成

- **cost_tracker.py**：扩展，不重写
- **Writer 自检层**（420 批次做的 writer_selfcheck.py）：加预算检查项
- **metrics_snapshot.py**：加成本指标
- **CI**：加成本报告步骤（不阻断，只报告）
- **golden_lock**：加成本基线（成本恶化也告警）

---

## 九、风险与缓解

| 风险 | 缓解 |
|---|---|
| 预算定低了，好原子做不完 | 预算表先宽松，积累数据后再收紧；人审批可追加 |
| ROI 公式不准 | 先观察，公式可以迭代；ROI 只作参考，不作阻断 |
| 级联路由分类不准 | 先人工审核路由建议，积累数据后再自动 |
| token 估算不准（chars/3） | 相对值有意义；如果有 API 可以取精确值，再升级 |
| 成本门禁影响质量 | 超预算不直接删卡，而是人审批追加；质量优先于成本 |
