# 592 建设包：数据层诚实化 + 命题闭包工具

> 批次定位：纯数据层 + 只读工具层，不改判决逻辑、不改卡、不改规则。
> 核心目标：把"停在 v1 的 metrics"和"不存在的 overturned 通道"补齐，再加命题闭包工具为 R4 grounded 层铺路。
> 铁律：存量零误伤、新收紧 warn 起步、不信自报只信独立复跑、一任务一 commit + 正反例、护栏不许裸 except Exception。

---

## 开工前基线（必须先实跑，不凭记忆）

```bash
# 1. 门禁现状
.venv\Scripts\python.exe tools\tool_integrity.py --check
.venv\Scripts\python.exe tools\gate_engine.py --check
.venv\Scripts\python.exe tools\poison_drill.py
.venv\Scripts\python.exe tools\atom_evidence_replay.py --check

# 2. v7 基线确认
.venv\Scripts\python.exe -c "import json;d=json.load(open('data/mutation/full_baseline_v7.json',encoding='utf-8'));print(d['variants'],d['blocked'],d['escaped'],d['n_a'],d.get('equivalent'))"

# 3. metrics 现状（确认断流点）
Get-Content data\metrics.jsonl -Tail 3
# 预期：最后一条 2026-09-17T17:40:45，curves.mutation_escape_rate 仍为 v1 的 0.2374

# 4. overturned 通道确认
Test-Path data\overturned_events.jsonl
# 预期：False（573 设计了 CLI 但从未创建文件）

# 5. 命题网络现状
.venv\Scripts\python.exe tools\prop_graph.py stats
# 预期：79 命题 / 27 卡 / inference29 / observation50
```

基线全绿后才开工。任何一项与预期不符，先记录再判断是否阻塞。

---

## 任务 1：metrics curves 从 v1 升到 v7（度量诚实化）

### 问题
`data/metrics.jsonl` 的 `curves.mutation_escape_rate` 停在 v1 的 0.2374（23.7%），而当前 v7 实际是 1/1406 ≈ 0.071%。差 340 倍。这是"度量不诚实"——报告层给看的数字与真实基线脱节。

### 做什么
1. 读 `tools/metrics_collector.py`，找到 `curves` 字段的构造逻辑
2. 把 `mutation_escape_rate` 从硬编码/旧值改为从 `full_baseline_v7.json` 实时读取：
   - point = escaped / (blocked + escaped) = 1 / 1406
   - 用 `tools/stat_bounds.py` 的 `cp_interval(escaped, blocked+escaped, 0.95)` 算双侧 95% 区间
   - 标注 `baseline_version: "v7"`、`frozen_at_commit: "d36d5c8"`（v7 冻结落点）
3. `overturned` 曲线：从 `data/overturned_events.jsonl` 读取计数（任务 2 创建后），文件不存在则为 0 并标注 `channel_initialized: false`
4. `escape_survival` 曲线：按算子统计"逃逸被后续批次收口"的批次数
   - M3 = 1 批（571 浮出 52 → 572 收口）
   - M5 = 1 批（574 浮出 29 → 575 收口）
   - M2 = 0（假逃逸，571 已证实尺子 bug，不计入 survival）
   - M6 = 0（8 条等价变异体，583 已定性，非真逃逸）
   - 其余 = null（缺数据，不许填 0）
5. `monotone_convergence`：写死 `"不可声称（尺子变更史 v1→v7，非同一量时间序列；仅 1 个含曲线时点）"`——与 573/582 的诚实口径一致

### 验收
- `metrics_collector.py` 跑一次，`data/metrics.jsonl` 新增一行，`curves.mutation_escape_rate.point` ≈ 0.000711（1/1406）
- 新增测试 `tests/test_metrics_curves_v7_592.py`：
  - 断言 point = 1/1406（浮点容差 1e-9）
  - 断言 cp_interval 与 stat_bounds 独立复算一致
  - 断言 baseline_version = "v7"
  - 断言 monotone_convergence 包含"不可声称"
  - 断言旧 v1 值 0.2374 不再出现在新行
- 存量测试 `tests/test_metrics_collector_curves.py` 如有硬编码旧值，同步更新并注明"非回归"

---

## 任务 2：overturned 事件通道初始化（空文件 + schema 校验）

### 问题
573 设计了 `--log-overturned` CLI 和 schema，但 `data/overturned_events.jsonl` 从未创建。通道不存在 = 曲线恒 None = 度量缺口。

### 做什么
1. 创建 `data/overturned_events.jsonl`（空文件，0 行）
2. 在 `tools/overturned_events.py`（如不存在则从 573 设计恢复）中加：
   - `ensure_channel()`：文件不存在则创建空文件，存在则校验每行 JSON 合法
   - `count()`：返回事件总数
   - `append(event)`：fail-closed（缺字段/卡解析不到/git 不可用 ⇒ 拒绝写入且不落行）
3. schema（与 573 设计一致）：
   ```json
   {"ts": "ISO8601", "target": "card|proposition|rule", "card": "EV-XXX-001", "old_verdict": "confirm|refute|blocked|escaped", "new_verdict": "...", "by": "human:<git-author>|adversary|system", "reason": "text"}
   ```
4. **系统绝不自动产生推翻**——只提供写入接口，实际写入由人审或 adversary 登记触发

### 验收
- `data/overturned_events.jsonl` 存在且为空
- `overturned_events.ensure_channel()` 幂等（跑两次不报错）
- 新增测试 `tests/test_overturned_channel_592.py`：
  - 空文件 count() = 0
  - 合法事件 append 后 count() = 1，文件多一行
  - 缺字段事件 append 被拒绝（fail-closed），文件行数不变
  - 冒名 human（git 作者不匹配）被拒绝
  - 临时目录测试，不碰真实 data/overturned_events.jsonl

---

## 任务 3：prop_closure 命题闭包工具（582 N2 落地）

### 问题
582 调研设计了 `tools/prop_closure.py`（命题级闭包双实现：Python 迭代 vs SQL WITH RECURSIVE 对账），但从未落地。命题闭包是 R4 grounded 论证层的前置基础设施——没有闭包就无法算"全局可接受集"。

### 做什么
1. 创建 `tools/prop_closure.py`（纯只读、幂等、不改卡、不改命题库）
2. 数据来源：`data/propositions.db`（prop_graph 已建的 SQLite 库）
3. 闭包定义：从给定命题集合 S 出发，沿 `evidence →` 边（命题引用卡、卡引用命题）递归展开，返回所有可达命题
4. 双实现对账：
   - **Python 实现**：BFS/DFS 迭代，从 propositions.db 读边
   - **SQL 实现**：`WITH RECURSIVE closure(id) AS (SELECT ? UNION SELECT target FROM edges JOIN closure ON edges.source=closure.id)`
   - 两者结果必须逐元素相同（集合相等），不一致则 fail-loud
5. CLI：
   - `python tools/prop_closure.py stats`：全库闭包统计（79 命题的平均闭包大小、最大闭包、孤立命题）
   - `python tools/prop_closure.py from --id prop-1`：从指定命题出发的闭包
   - `python tools/prop_closure.py cross-check`：双实现全量对账（79 命题逐个比对）
6. 只读硬纪律：源码无写调用（除了可能的临时 db 复制），唯一 subprocess = 只读

### 验收
- `prop_closure.py stats` 输出 79 命题的闭包统计
- `prop_closure.py cross-check` exit 0（双实现 79/79 一致）
- 新增测试 `tests/test_prop_closure_592.py`：
  - 小手工图（5 命题 6 边）的闭包正确性
  - 双实现对账一致
  - 孤立命题闭包 = {自身}
  - 循环引用不无限递归（BFS 去重）
  - 临时 db，不碰真实 data/propositions.db
- prop_graph.py 一行不改（闭包是独立工具）

---

## 任务 4：命题网络台账更新（79 命题完整性校验）

### 做什么
1. 跑 `prop_graph.py stats` 和 `prop_closure.py stats`，生成 `data/prop_network_inventory.md`：
   - 79 命题列表（id / claim_type / 引用卡 / 闭包大小 / signed_by / liveness 锚状态）
   - 27 卡列表（id / 命题数 / verified_by / oracle 状态）
   - 边统计（命题→卡、卡→命题、总边数）
   - 完整性校验：
     - 引用卡不存在的命题（应为 0）
     - 无命题的卡（原子卡 27 张全有命题，应为 0）
     - 闭包大小异常（>50 或 =1 的命题列出）
2. 这个台账是 R4 grounded 层的输入基线，纯只读生成

### 验收
- `data/prop_network_inventory.md` 存在，包含上述四节
- 引用卡不存在 = 0、无命题卡 = 0（与 589 验收一致）
- 79 命题逐条列出

---

## 收工总验收（fresh，退出码定论）

```bash
# 1. 核心门禁
.venv\Scripts\python.exe tools\tool_integrity.py --check          # exit 0
.venv\Scripts\python.exe tools\gate_engine.py --check              # 63/191 逐字不变
.venv\Scripts\python.exe tools\poison_drill.py                      # 124/124
.venv\Scripts\python.exe tools\atom_evidence_replay.py --check      # confirm=56

# 2. 本批新增
.venv\Scripts\python.exe tools\metrics_collector.py                  # curves 升 v7
.venv\Scripts\python.exe tools\prop_closure.py cross-check           # exit 0
.venv\Scripts\python.exe tools\prop_closure.py stats                 # 79 命题

# 3. 测试
pytest -m "not slow" -n auto                                          # exit 0
pytest tests/test_metrics_curves_v7_592.py tests/test_overturned_channel_592.py tests/test_prop_closure_592.py -n0  # 全绿

# 4. 卫生
ruff check tools/metrics_collector.py tools/overturned_events.py tools/prop_closure.py tests/test_*_592.py  # All passed
git diff --quiet -- atoms evidence Examples Book                       # exit 0
```

---

## 不做什么（任务书硬边界）

- 不改 gate_engine.py / atom_evidence_replay.py / poison_drill.py（CORE 五文件）
- 不改任何卡（atoms/ evidence/ Examples/ Book）
- 不做 R4 grounded 论证层的实际推理（只做前置基础设施：闭包 + 台账）
- 不做 M1 TCE 攻坚（冻结项）
- 不做 golden accept（人审权力）
- 不 push、不替人签
- 不清理根目录 149 临时件（卫生债，单独批次）
- 不补 50 条活性锚（知识活，需人审内容）

---

## 偏差表模板（§6，必须如实填写）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | | | |
| D2 | | | |

## 交人项（§7）

- metrics 新行需人审确认 curves 数字正确
- overturned 通道初始化后，首次真实推翻事件需人审触发
- prop_network_inventory.md 中闭包异常的命题需人审确认

## 工作日志

写 `_worklog_592.md`（按惯例不入库），含任务 0-4 记录、§6 偏差表、§7 验收结果、交人项。
