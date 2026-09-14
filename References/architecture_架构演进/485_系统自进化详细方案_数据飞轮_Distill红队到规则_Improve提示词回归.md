---
id: 485
title: 系统自进化详细方案 数据飞轮 Distill红队到规则 Improve提示词回归
status: active
type: architecture-note
created_at: 2026-09-14
---
# 485 系统自进化详细方案：数据飞轮四阶段自动化
## Distill（红队→规则→毒样例）+ Improve（提示词版本+回归测试）

> 生成时间：2026-09-14
> 来源：385 数据飞轮四阶段 + 460 规则自动进化 + 477 遗漏成果第 6 项
> 现状：Produce（Writer）和 Coach（红队+门禁+人审）已有，Distill 和 Improve 完全缺失

---

## 一、问题：系统的进化完全依赖人

当前每次红队发现的问题：
1. 人读红队报告
2. 人判断"这是不是新问题"
3. 人写规则
4. 人写毒样例
5. 人改提示词
6. 人验证没退化

人忘了记 → 教训丢了；人记错了 → 规则写错了；人懒得验证 → 改提示词引入退化。

系统没有"从错误中自动学习"的能力。每一轮对抗都是从零开始，上一轮的教训没有自动化沉淀。

---

## 二、数据飞轮四阶段

```
Produce（生产）→ Coach（评估）→ Distill（提炼）→ Improve（改进）
     ↑                                            ↓
     └────────────── 反馈循环 ──────────────────┘
```

### 已有

- **Produce**：Writer 生成原子（已有完整流程）
- **Coach**：红队 + 门禁 + 人审（已有完整流程）

### 缺失（本方案要做的）

- **Distill**：从红队发现和门禁失败中自动提炼可复用知识
- **Improve**：提示词版本管理 + 回归测试 + 规则效果追踪

---

## 三、Distill：红队发现→规则候选→毒样例自动化

### 3.1 红队报告结构化

当前红队报告是自由文本，先要求红队按结构化格式输出：

```markdown
## 发现 1：[标题]

### 错误类型
[从错误类型库中选择：assertion_self_proof / metric_inconsistency / artifact_stale / env_dependent / trivial_assertion / ...]

### 根因
[一句话根因]

### 复现
- 文件：path/to/file
- 行号：N
- 命令：`...`
- 输出：`...`

### 修复建议
[具体怎么修]

### 严重度
[阻断/高级/建议]
```

### 3.2 错误类型库

建立 `docs/kernel/error_patterns.json`，记录所有已知错误类型：

```json
{
  "assertion_self_proof": {
    "name": "断言自证",
    "description": "断言和夹具输出同错，断言只是复述夹具输出",
    "historical_cases": ["ALLOC-002", "LEAK-002"],
    "detection_rule": "EV-SELF-SATISFIED-ASSERT",
    "prevention": "TDD顺序反转（先写断言再写夹具）"
  },
  "metric_inconsistency": {
    "name": "口径不统一",
    "description": "不同策略的元数据口径不一致，导致结论方向反转",
    "historical_cases": ["ALLOC-002"],
    "detection_rule": null,
    "prevention": "夹具设计时统一口径"
  }
}
```

### 3.3 工具：error_pattern_miner.py（约 150 行）

```python
# 伪代码
def mine_from_redteam_report(report_path):
    """从红队报告中提取错误模式"""
    report = parse_report(report_path)
    patterns = []
    for finding in report.findings:
        pattern = {
            'error_type': finding.error_type,
            'root_cause': finding.root_cause,
            'reproduction': finding.reproduction,
            'fix': finding.fix_suggestion,
            'severity': finding.severity,
            'source': report_path,
            'date': today(),
        }
        patterns.append(pattern)
    return patterns

def match_existing_rules(pattern):
    """检查错误模式是否已有对应规则"""
    for rule in get_all_rules():
        if rule.detects(pattern.error_type):
            return rule
    return None

def generate_rule_candidate(pattern):
    """如果没有对应规则，生成规则候选"""
    return {
        'rule_id': f'EV-AUTO-{next_id()}',
        'name': f'自动检测：{pattern.error_type}',
        'description': pattern.root_cause,
        'severity': pattern.severity,
        'detection_logic': generate_detection_logic(pattern),  # 草稿，人审核
        'source_pattern': pattern,
        'status': 'candidate',  # candidate → approved → deployed
    }

def generate_poison_candidate(pattern, rule_candidate):
    """生成毒样例草稿"""
    return {
        'id': f'P-AUTO-{next_id()}',
        'name': f'{pattern.error_type} 毒样例',
        'rule': rule_candidate.rule_id,
        'fixture': generate_poison_fixture(pattern),  # 草稿，人审核
        'expected': {'block': True, 'rule': rule_candidate.rule_id},
        'status': 'candidate',
    }
```

### 3.4 工作流

1. 红队完成报告（结构化格式）
2. `python tools/error_pattern_miner.py --report <report>` 自动提取错误模式
3. 匹配现有规则 → 已有规则的，记录到规则的命中历史
4. 没有对应规则的 → 生成规则候选 + 毒样例草稿
5. 人审核规则候选 → 通过则入库（配正式毒样例 + pytest）
6. 不通过 → 记录原因（是误报？还是规则设计有问题？）

### 3.5 验收

- 红队报告 100% 结构化
- 每个错误模式都有记录（不管有没有对应规则）
- 规则候选有人审核，不自动入库
- 历史错误模式可查询（"这个问题以前出现过吗？"）

---

## 四、Improve：提示词版本管理 + 回归测试

### 4.1 问题

提示词改了之后，不知道是变好还是变坏了。
- 470 提示词从 v1 迭代到 v2.7（17 轮打磨），但每轮改了什么、效果如何，没有系统记录
- 改了提示词后，用历史案例验证没退化？没有
- 提示词越来越长，但哪些部分有效、哪些是噪音？没有归因分析

### 4.2 提示词版本管理

所有提示词文件纳入 git 管理（已经在仓库里了），但增加：

1. **版本号**：每个提示词文件开头有 `version: vX.Y`
2. **变更日志**：每次改提示词，在文件末尾加 `## vX.Y 变更` 记录
3. **变更原因**：每次变更必须记录"为什么改"（是红队发现？是效果不好？是新需求？）

### 4.3 提示词回归测试

建立 `tests/prompt_regression/` 目录，存放历史案例：

```
tests/prompt_regression/
  case_001_alloc_002/          # ALLOC-002 口径反转案例
    input.md                    # 输入（任务描述）
    expected_output.md          # 期望输出（关键断言不能少）
    evaluation_criteria.md      # 评估标准（哪些必须有、哪些不能有）
  case_002_leak_002/            # LEAK-002 观测反转案例
  ...
```

`tools/prompt_regression.py`（约 120 行）：
```python
def run_regression(prompt_path, case_dir):
    """用历史案例测试提示词，检查是否退化"""
    # 1. 用提示词处理 case 的 input
    # 2. 对比 output 和 expected_output
    # 3. 检查 evaluation_criteria 中的必须项和禁止项
    # 4. 返回 pass/fail + 差异
```

### 4.4 提示词归因分析（458 PC1）

ProCut 式：量化提示词每段的效用，剪枝低效用组件。

方法：
1. 把提示词分成 N 段
2. 每次去掉一段，跑回归测试
3. 去掉后测试全过 → 这段是噪音，可以删
4. 去掉后测试失败 → 这段有效，保留

目标：压缩 30-78% token，不降低效果。

### 4.5 规则效果追踪

每条规则上线后追踪：
- 命中次数（真实门禁中拦了多少次）
- 误报次数（被 accept 或驳回的次数）
- 命中率趋势（上升/下降/稳定）
- 最后命中时间

`tools/rule_effectiveness.py`（约 80 行）：
- 从 git log 和 golden_state.json 提取规则命中历史
- 生成规则效果报告
- 连续 3 个月零命中的规则 → 建议修剪（对接 482 修剪机制）

---

## 五、实施计划

### 第一阶段（零/低成本，立即做）

1. **红队报告结构化**：改红队提示词，要求按结构化格式输出
2. **错误类型库**：写 `docs/kernel/error_patterns.json`，录入已知的 10+ 种错误类型
3. **提示词版本号**：所有提示词文件加 version 和变更日志
4. **规则效果追踪**：写 `tools/rule_effectiveness.py`，从 git log 提取命中历史

### 第二阶段（中等成本，下一批做）

5. **error_pattern_miner.py**：从红队报告自动提取错误模式，生成规则候选
6. **提示词回归测试**：建立 5-10 个历史案例，写 `tools/prompt_regression.py`
7. **规则候选审核流程**：规则候选 → 人审核 → 入库的标准流程

### 第三阶段（高成本，积累数据后做）

8. **提示词归因分析**：ProCut 式压缩，量化每段效用
9. **自动规则生成**：错误模式 → 规则候选 → 毒样例草稿的全自动管道（人审核后入库）
10. **进化效果评估**：系统进化速度（每轮红队发现的新问题比例、规则命中率趋势）

---

## 六、预期效果

| 指标 | 当前 | 第一阶段后 | 第三阶段后 |
|---|---|---|---|
| 红队发现→规则的转化率 | 未知（靠人） | 有记录（结构化） | 自动生成候选（人审核） |
| 重复错误率 | 未知 | 可追踪 | <10%（同类错误不重犯） |
| 提示词退化 | 无检测 | 有版本号 | 回归测试拦截 |
| 规则效果 | 无追踪 | 有命中历史 | 自动建议修剪 |
| 提示词长度 | 持续增长 | 有变更日志 | 归因分析压缩 30%+ |

---

## 七、和现有系统的集成

- **红队提示词**（365B）：加结构化输出要求
- **gate_engine.py**：规则加 `error_type` 字段，关联错误类型库
- **golden_lock**：加规则效果基线（命中率下降也告警）
- **CI**：加提示词回归测试步骤（改提示词后自动跑）
- **修剪机制**（482）：规则效果追踪的数据直接喂给修剪机制

---

## 八、风险与缓解

| 风险 | 缓解 |
|---|---|
| 自动生成的规则候选质量差 | 人审核后才入库，候选不直接生效 |
| 提示词回归测试案例太少 | 先建 5 个关键案例，逐步增加 |
| 错误类型库不全 | 持续积累，红队每次发现新类型就录入 |
| 归因分析成本高（要跑很多次） | 先手动分析关键提示词，自动化放后期 |
| 结构化红队报告增加红队负担 | 格式模板化，红队只填字段，不增加太多工作量 |

---

## 九、关键设计原则

1. **人在回路**：Distill 和 Improve 都是"自动生成候选，人审核后入库"，不自动改规则/提示词
2. **可追溯**：每个规则/提示词的变更都有来源（哪个红队发现、哪个案例驱动）
3. **不退化**：任何变更必须通过回归测试，不允许"改了之后不知道变好变坏"
4. **数据驱动**：规则效果、提示词效果、错误模式都有数据，不凭感觉
