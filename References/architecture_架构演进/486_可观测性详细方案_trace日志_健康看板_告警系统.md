---
id: 486
title: 可观测性详细方案 trace日志 健康看板 告警系统
status: active
type: architecture-note
created_at: 2026-09-14
---
# 486 可观测性详细方案：trace 日志 + 健康看板 + 告警系统
## 从黑盒到白盒：系统运行时的全链路可观测

> 生成时间：2026-09-14
> 前置：metrics_snapshot.py 474 行已有基础，golden_state.json 有 metrics 字段，data/cost/ 已存在
> 问题：系统运行时是黑盒，出问题只能靠人翻 worklog 和 git log

---

## 一、现状评估

### 已有

- `metrics_snapshot.py`（474 行）：快照指标（原子数/卡数/规则数/毒样例数）
- `golden_state.json`：基线指标，有 metrics/accepted/dirty 字段
- `gen_metrics.py`：生成指标报告
- `cost_tracker.py`：成本追踪
- worklog：人工写的 markdown 工作记录

### 缺失

1. **没有结构化 trace 日志**：每次 Agent 操作没有详细记录（时间/操作/输入/输出/耗时/token）
2. **没有实时健康视图**：不知道系统当前状态（门禁绿/红、replay 进度、待处理问题）
3. **没有告警**：门禁红了、replay confirm 下降了、token 超预算了，不会自动报警
4. **没有性能追踪**：replay 哪张卡最慢、编译占多少时间、缓存命中率多少
5. **没有操作审计**：谁在什么时候改了什么文件，没有结构化记录（只有 git log）

---

## 二、结构化 trace 日志

### 2.1 设计原则

- **JSONL 格式**：每行一个 JSON 对象，方便 grep/jq/解析
- **只追加**：日志文件只追加，不修改
- **低开销**：记录日志的耗时 <1ms，不影响主流程
- **可追溯**：每条日志有唯一 ID 和 parent_id（操作间的依赖关系）

### 2.2 日志格式

```json
{
  "trace_id": "uuid",
  "parent_id": "uuid或null",
  "timestamp": "2026-09-14T10:30:00.123Z",
  "agent": "writer:cheap_agent",
  "operation": "write_evidence_card",
  "target": "evidence/mem/EV-MEM-040.md",
  "status": "success",
  "duration_ms": 1523,
  "tokens_used": 2340,
  "details": {
    "assertions": 12,
    "artifact_sha": "4f482fdc...",
    "replay_result": "confirm"
  },
  "error": null
}
```

### 2.3 日志类型

| 类型 | operation 示例 | 记录时机 |
|---|---|---|
| Agent 操作 | write_atom / write_card / run_redteam / fix_gate | Agent 完成每个操作 |
| 门禁运行 | gate_check / replay_check / poison_drill / pytest | 每次门禁运行 |
| 编译运行 | compile_fixture / run_binary | replay 中的每次编译运行 |
| 工具调用 | cost_tracker.record / evidence_graph.query | 每次工具调用 |
| 人审操作 | human_review / accept / reject | 每次人审 |
| 系统事件 | batch_start / batch_end / push / ci_run | 系统级事件 |

### 2.4 工具：trace_logger.py（约 100 行）

```python
# 伪代码
import json, time, uuid
from pathlib import Path
from datetime import datetime, timezone

TRACE_DIR = Path("data/traces")

class TraceLogger:
    def __init__(self, agent_name):
        self.agent = agent_name
        self.trace_file = TRACE_DIR / f"{datetime.now().strftime('%Y%m%d')}.jsonl"
    
    def log(self, operation, target=None, status='success', 
            duration_ms=None, tokens_used=None, details=None, error=None):
        entry = {
            'trace_id': str(uuid.uuid4()),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'agent': self.agent,
            'operation': operation,
            'target': target,
            'status': status,
            'duration_ms': duration_ms,
            'tokens_used': tokens_used,
            'details': details or {},
            'error': error,
        }
        with open(self.trace_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        return entry['trace_id']
    
    def span(self, operation, target=None):
        """上下文管理器，自动记录耗时"""
        start = time.time()
        trace_id = self.log(operation, target, status='started')
        try:
            yield trace_id
            self.log(operation, target, status='success', 
                     duration_ms=int((time.time()-start)*1000))
        except Exception as e:
            self.log(operation, target, status='error',
                     duration_ms=int((time.time()-start)*1000), error=str(e))
            raise
```

### 2.5 接入点

- Writer 自检层：每个操作记录 trace
- replay：每次编译/运行记录 trace（性能分析用）
- gate_engine：每次规则命中记录 trace
- 人审：每次签署记录 trace

---

## 三、健康看板

### 3.1 实时状态

`tools/health_dashboard.py`（约 150 行）生成 markdown 或 HTML 报告：

```
# 阙疑系统健康看板
生成时间：2026-09-14 10:30:00

## 系统状态
- 门禁：🟢 绿（block=0, warn=32）
- Replay：🟢 56/56 confirm
- 毒样例：🟢 61/61
- 测试：🟢 272 passed
- 工作树：🟡 干净（ahead 138, 未 push）

## 资产统计
- 原子：28（27 verified + 1 draft）
- 证据卡：56
- 误解：79
- 规则：50
- 毒样例：61

## 性能
- 全量 replay：4.5min（热缓存 1.2min）
- 单卡平均：4.8s
- 最慢卡：EV-MEM-017（13.7s）
- ccache 命中率：87%

## 成本（本批次）
- 总 token：124,500
- 平均每颗：6,200
- 超预算：0
- ROI 平均：3.2

## 待处理
- 待 push：138 commits
- 待裁决：2 项（E12 签收绑定、分类学错位）
- 待修复：0 阻断
- 告警：0

## 趋势（近 5 批）
- 原子数：20→22→24→26→28 ↑
- replay confirm：40→44→48→52→56 ↑
- 规则数：29→33→37→46→50 ↑
- 平均成本：5,200→5,500→5,765→6,100→6,200 ↑（需关注）
```

### 3.2 性能分析

从 trace 日志中提取性能数据：
- replay 单卡耗时分布（最快/最慢/平均/P95）
- 编译耗时占比（预期 99.5%）
- ccache 命中率
- 门禁各步骤耗时

### 3.3 接入方式

- 本地：`python tools/health_dashboard.py` 生成报告
- CI：每轮 CI 生成健康看板，作为 artifact
- 定期：每天自动生成一份，存入 data/health/

---

## 四、告警系统

### 4.1 告警规则

| 告警 | 条件 | 级别 | 动作 |
|---|---|---|---|
| 门禁红 | gate block >0 | P0 | 立即报警，阻断后续操作 |
| replay confirm 下降 | 比基线少 >0 | P0 | 立即报警 |
| 单颗原子超预算 | token > 预算 100% | P1 | 报警，需人审批追加 |
| 批次成本上升 | 比上一批高 >30% | P2 | 警告，分析原因 |
| 单卡 replay >30s | 性能退化 | P2 | 警告 |
| 规则零命中 >3 个月 | 死规则 | P3 | 建议修剪 |
| 工作树脏 >24h | 有未提交改动 | P2 | 提醒提交 |
| 未 push >50 commits | 推送积压 | P2 | 提醒 push |

### 4.2 工具：alert_check.py（约 80 行）

```python
def check_alerts():
    """检查所有告警规则，返回告警列表"""
    alerts = []
    
    # P0: 门禁红
    gate_result = run_gate_check()
    if gate_result.block > 0:
        alerts.append(Alert('P0', 'gate_red', f'门禁红：block={gate_result.block}'))
    
    # P0: replay confirm 下降
    baseline = load_golden_state()
    current = run_replay_check()
    if current.confirm < baseline.replay_confirm:
        alerts.append(Alert('P0', 'replay_regression', 
            f'replay confirm 下降：{baseline.replay_confirm}→{current.confirm}'))
    
    # P1: 超预算
    for atom in get_atoms():
        cost = get_atom_cost(atom)
        budget = get_budget(atom)
        if cost > budget:
            alerts.append(Alert('P1', 'over_budget', 
                f'{atom} 超预算：{cost}/{budget}'))
    
    # ... 更多告警规则
    
    return alerts
```

### 4.3 告警输出

- 本地：`python tools/alert_check.py` 输出告警列表
- CI：告警作为 CI 步骤，P0 告警导致 CI 失败
- 通知：告警写入健康看板的"待处理" section

---

## 五、实施计划

### 第一阶段（零/低成本，立即做）

1. **trace_logger.py**：写基础日志工具（100 行）
2. **接入 replay**：replay 的每次编译/运行记录 trace
3. **health_dashboard.py**：写基础健康看板（150 行），从 golden_state.json 和 metrics 读取数据
4. **alert_check.py**：写 P0 告警（门禁红、replay 下降）

### 第二阶段（中等成本，下一批做）

5. **接入 Writer 自检**：每个 Agent 操作记录 trace
6. **性能分析**：从 trace 日志提取性能数据，加入健康看板
7. **完整告警**：P1/P2/P3 告警规则
8. **趋势图**：健康看板加近 5 批趋势

### 第三阶段（高成本，积累数据后做）

9. **操作审计**：所有文件变更记录 trace（对接 git hook）
10. **实时监控**：长运行任务的实时进度显示
11. **异常检测**：基于历史数据的自动异常检测（不只是阈值告警）

---

## 六、预期效果

| 指标 | 当前 | 第一阶段后 | 第三阶段后 |
|---|---|---|---|
| 问题定位时间 | 翻 worklog+git log（10+ min） | trace 日志 grep（<1 min） | 健康看板直接显示 |
| 性能瓶颈 | 未知 | replay 单卡耗时分布 | 全链路性能追踪 |
| 告警 | 无 | P0 告警（门禁红/replay 下降） | 全级别告警+异常检测 |
| 系统状态 | 跑命令才知道 | 健康看板一眼看清 | 实时监控 |
| 操作审计 | 只有 git log | Agent 操作有 trace | 全操作审计 |

---

## 七、和现有系统的集成

- **metrics_snapshot.py**：扩展，加 trace 数据来源
- **golden_state.json**：加健康指标基线
- **replay**：接入 trace_logger，记录编译/运行耗时
- **Writer 自检层**：接入 trace_logger，记录操作
- **CI**：加健康看板生成步骤和告警检查步骤
- **cost_tracker.py**：trace 中的 token 数据自动喂给 cost_tracker

---

## 八、风险与缓解

| 风险 | 缓解 |
|---|---|
| trace 日志量太大 | 按天分割，旧日志归档；只记录关键操作，不记录调试信息 |
| 健康看板数据过时 | 每次生成时实时跑命令，不缓存 |
| 告警噪音太多 | P0 才阻断，P1/P2/P3 只警告；告警规则可调 |
| 接入 trace 影响性能 | trace 记录耗时 <1ms，异步写入；性能敏感路径可关闭 |
| 隐私问题 | trace 只记录操作元数据，不记录提示词和输出内容 |
