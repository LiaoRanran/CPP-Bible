---
id: 421
title: 苦力Agent执行提示词 412成本追踪 cost tracker CPVA基线
status: active
type: architecture-note
created_at: 2026-09-13
---
# 421 苦力Agent执行提示词：412 成本追踪（cost_tracker.py，先测量再优化）

> 投喂对象：苦力Agent。前置条件：无（可与 414/420 并行）。任务：实现成本追踪工具，记录每颗原子的 token 消耗，建立 CPVA（Cost Per Verified Atom）基线。零风险——只记录，不改动生产逻辑。

---

## 铁律

1. **不 push**：只 commit
2. **工具改动分离提交**
3. **零风险**：只记录数据，不改动 gate/replay/poison 的任何逻辑
4. **配 pytest**
5. **先 Read 再改**：Read `tools/cppbible.py` 确认 cmd_check 元组格式

---

## 背景

412 调研建立了 CPVA（Cost Per Verified Atom）指标，但阙疑目前没有任何成本数据——不知道每颗原子花了多少 token，不知道哪些环节最费，不知道优化有没有效果。

**没有测量就没有优化。** 本任务 = 先测量，建立基线。

---

## 实现步骤

### Step 1：创建 tools/cost_tracker.py

```python
#!/usr/bin/env python3
"""
成本追踪工具：记录每颗原子的 token 消耗（字符数估算），建立 CPVA 基线。
零风险：只记录，不改动生产逻辑。

用法：
  python tools/cost_tracker.py record --atom ATOM-MEM-RAII-001 --stage fixture --chars 15000
  python tools/cost_tracker.py report [--atom ATOM-MEM-RAII-001]
  python tools/cost_tracker.py cpva
输出：JSON
"""
```

### Step 2：数据模型

成本数据存在 `data/cost/` 目录（新建，gitignore 或入库均可，建议入库作为历史基线）：

```
data/cost/
  ATOM-MEM-RAII-001.json
  ATOM-MEM-MOVE-001.json
  ...
```

每个原子一个 JSON：

```json
{
  "atom_id": "ATOM-MEM-RAII-001",
  "domain": "mem",
  "created_at": "2026-09-10",
  "verified_at": "2026-09-11",
  "stages": {
    "fixture": {"chars": 15000, "tokens_est": 5000, "windows": 2, "duration_min": 30},
    "evidence_cards": {"chars": 25000, "tokens_est": 8333, "windows": 3, "duration_min": 45},
    "redteam": {"chars": 30000, "tokens_est": 10000, "windows": 1, "duration_min": 60},
    "gate_fix": {"chars": 8000, "tokens_est": 2667, "windows": 1, "duration_min": 15},
    "human_review": {"chars": 5000, "tokens_est": 1667, "windows": 1, "duration_min": 10}
  },
  "total_chars": 83000,
  "total_tokens_est": 27667,
  "total_windows": 8,
  "total_duration_min": 160,
  "cpva": 27667
}
```

### Step 3：token 估算方法

由于无法直接获取 API token 消耗，用字符数估算：
```
tokens_est = chars / 3  # 中文约 1.5 字符/token，英文约 4 字符/token，混合取 3
```

这个估算不精确，但**相对值有意义**——可以比较不同原子、不同阶段的成本比例。

### Step 4：核心功能

#### 4.1 record（记录单步成本）

```python
def record(atom_id, stage, chars, windows=1, duration_min=None):
    """
    记录某颗原子某阶段的成本。
    stage: fixture / evidence_cards / redteam / gate_fix / human_review / other
    """
    # 1. 读取或创建该原子的成本文件
    # 2. 更新 stages[stage]
    # 3. 重算 total
    # 4. 保存
```

#### 4.2 report（单原子报告）

```python
def report(atom_id=None):
    """
    输出单颗原子或全部原子的成本报告。
    """
    # 如果指定 atom_id，输出该原子的分阶段成本
    # 如果不指定，输出全部原子的汇总
```

#### 4.3 cpva（全局指标）

```python
def cpva():
    """
    计算全局 CPVA：
    - 总 token / verified 原子数
    - 按域分解（mem/conc/ub/lang/hist）
    - 按阶段分解（fixture/evidence/redteam/...）
    - 趋势（最近 5 颗 vs 最早 5 颗）
    """
    return {
        "total_verified_atoms": 27,
        "total_tokens_est": 750000,
        "cpva_overall": 27778,
        "cpva_by_domain": {"mem": 30000, "conc": 25000, "ub": 28000},
        "cpva_by_stage": {
            "fixture": 25, "evidence_cards": 30, "redteam": 35,
            "gate_fix": 8, "human_review": 2
        },
        "cpva_recent_5": 25000,
        "cpva_first_5": 35000,
        "trend": "improving"  # improving / stable / worsening
    }
```

#### 4.4 自动采集（可选，P1）

从 git log 自动估算：
```python
def auto_collect_from_git(atom_id):
    """
    从 git log 估算某颗原子的成本：
    - 找到该原子相关的所有 commit
    - 统计 commit 数（≈ windows）
    - 统计改动行数（≈ chars）
    - 这是粗略估算，用于回填存量原子的成本
    """
```

### Step 5：存量原子回填（P0 的一部分）

对 27 颗 verified 原子，用 git log 粗略回填成本：
```bash
python tools/cost_tracker.py backfill --all
```

这会给每颗原子一个粗略的成本基线，不需要精确，但能让 CPVA 有数据。

### Step 6：注册到 cppbible.py

在 `tools/cppbible.py` 中新增 `cost` 命令：
```bash
cppbible cost report   # 成本报告
cppbible cost cpva     # CPVA 指标
```

### Step 7：pytest

```python
class TestCostTracker:
    def test_record_and_report(self):
        # record 一条 → report 能读到
        ...

    def test_cpva_calculation(self):
        # 构造 3 颗原子的成本数据 → cpva 计算正确
        ...

    def test_token_estimation(self):
        # chars=3000 → tokens_est=1000
        ...

    def test_backfill_from_git(self):
        # 对一颗已知原子 backfill → 数据非空
        ...

    def test_json_output_format(self):
        # 输出格式与四工具 --json 一致
        ...
```

### Step 8：验证闭环

不是"工具写了"，是：
```
跑一颗真实原子（或回填 27 颗）→ CPVA 有数值 → 按域/阶段分解有意义
```

**验收标准**：27 颗 verified 原子全部有成本数据，CPVA 可计算，按域/阶段分解非空。

---

## 验收标准

- [ ] `tools/cost_tracker.py` 存在，record/report/cpva/backfill 四个功能
- [ ] `data/cost/` 目录存在，27 颗原子全部有成本文件（backfill 后）
- [ ] `cppbible cost report` 和 `cppbible cost cpva` 可执行
- [ ] CPVA 可计算，按域/阶段分解非空
- [ ] pytest 含 TestCostTracker（≥5 例）
- [ ] 输出 JSON 格式与四工具一致
- [ ] 零风险：不改动 gate/replay/poison 的任何逻辑
- [ ] 独立 commit，message 含 `feat(tools): 412 成本追踪 cost_tracker.py CPVA基线`

---

## 不做的事

- 不做精确 token 统计（需要 API 接入，超出范围）
- 不做成本优化建议（先测量，优化是下一批）
- 不做实时监控（先离线分析）
- 不改动 gate/replay/poison
- 不 push
- 不混 414/417/420 的改动

---

## 为什么这是 P0

412 指出：阙疑的成本优势是"门禁零 token"，但成本盲区是"没有追踪"。红队是成本热点但不能砍。**没有测量就没有优化**——先知道每颗原子花了多少、哪步最费，才能谈模型路由、前缀缓存、上下文管理等优化。

本工具零风险（只记录），但价值极高——它让 412 的五杠杆优化（模型路由/前缀缓存/上下文管理/批处理/投机解码）从"理论"变成"有数据支撑的决策"。
