# 508 苦力Agent执行提示词：P0性能收尾 + 智能基建（可观测性/知识图谱/质量度量/备份）

> 日期：2026-09-14
> 前置：500批次已完成（gate 55规则 BLOCK=0 WARN=31 · poison 72/72 · replay confirm=56 · pytest 366点 227s · ahead 173）
> 目标：P0性能两项 + 智能基建三项 + 安全备份，共7个子任务
> 执行模式：白天差模型苦力，晚上好模型 review

---

## 〇、铁律（违反即停手报告）

1. **先读磁盘真实代码再动手**——禁止凭历史记忆写代码。每个子任务开工前先 Read 对应文件确认当前行号/格式/字段。
2. **一个子任务一个 commit**——独立、原子、可回滚。commit message 格式：`feat(scope): 简述` 或 `perf(scope): 简述`。
3. **存量零误伤**——改完后 gate BLOCK=0 必须保持；WARN 数只能增加新规则暴露的存量债，不能因新代码新增 BLOCK；pytest 全绿；replay confirm=56 不变。
4. **不 push、不 golden sync**——push 权在人，golden accept 权在人。
5. **不编造数据**——所有耗时/计数/命中率必须实跑输出。实测与设计预期不符时如实记录，不硬凑。
6. **毒样例+pytest 同步**——新规则/新工具必须配毒样例（如适用）和 pytest。
7. **worklog 记录**——每个子任务结束后写 `_worklog_508.md`，含：改动文件、实测数字、与预期偏差、复现命令。
8. **临时件清理**——任务结束后删除所有 `_pt*`/`_po*`/`_rp*`/`_timeit.py` 等临时文件。

---

## 一、P0 性能收尾（任务 1-3）

### 任务 1：pytest-xdist 并行

**目标**：pytest wall 227s → 30-50s。

**步骤**：

1. 先 Read `pyproject.toml` 或 `pytest.ini`（找当前 pytest 配置）。
2. 加 `addopts = -n auto`（或在 CI 命令中加 `-n 16`）。
3. **排查测试隔离**：跑一轮 `pytest -n auto`，看是否有测试因并行而失败（文件锁、临时目录共享、端口冲突）。
4. 有失败的测试加 `@pytest.mark.serial`（串行跑），其余保持并行。
5. 确认 `-m fast` 模式仍工作（11s 基线不退化）。
6. 记录：并行后 wall 时间、serial 标记了几个测试、失败是否清零。

**验证**：
- `pytest -n auto` 全绿
- `pytest -m fast -n auto` wall <15s
- gate/poison/replay 不受影响

**commit**：`perf(tests): pytest-xdist 并行 + 测试隔离标记`

---

### 任务 2：CI matrix 四 job 并行

**目标**：CI 从串行 15min → 并行 wall 5min。

**步骤**：

1. 先 Read `.github/workflows/ci.yml`，看当前 job 结构。
2. 拆为 4 个 parallel job：
   - `pytest`：`pytest -n 16 --maxfail=1`
   - `replay`：`python tools/atom_evidence_replay.py --check --incremental`
   - `gate`：`python tools/gate_engine.py --check && python tools/poison_drill.py`
   - `quality`：`python tools/cppbible.py check --stage quality`
3. 4 个 job 并行跑，不需要 needs（它们之间无依赖）。
4. CI 的 `matrix` 中 Windows/WSL 仍保留跨平台验证。
5. 加 `fail-fast: false`，一个 job 失败不取消其他 job。

**验证**：
- ci.yml YAML 语法正确（`python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`）
- 4 个 job 各自有独立的 if 条件（不要让一个 job 失败影响其他）
- 本地不跑 CI（无网络），只改 YAML 并确保语法正确

**commit**：`ci: matrix 四 job 并行拆分（pytest/replay/gate/quality）`

---

### 任务 3：增量 replay CI 默认

**目标**：CI 中 replay 默认 `--incremental`，全量只在改 tools/ 时触发。

**步骤**：

1. Read `.github/workflows/ci.yml`，找到 replay 步骤。
2. replay 命令加 `--incremental`。
3. 加条件：如果 `tools/` 目录有变更（`git diff --name-only origin/master...HEAD | grep tools/`），则跑全量 `--rebuild-manifest`；否则增量。
4. 记录：CI 中 replay 用增量还是全量的判断逻辑。

**验证**：
- ci.yml 语法正确
- 增量模式在 498 已验证（无改动 0.3s，改 1 卡 2.3s），不需要重新验证

**commit**：`ci: replay 默认增量，改 tools/ 时全量`

---

## 二、智能基建（任务 4-6）

### 任务 4：可观测性 L1

**目标**：统一日志格式 + Trace ID + log_query CLI。

**步骤**：

1. 先 Read `tools/trace_logger.py`（已有基础），看当前日志格式。
2. 新建 `tools/observability.py`：
   - 日志格式：JSON Lines，每行一个 JSON 对象
   - 必填字段：`timestamp`（ISO 8601）、`level`（INFO/WARN/ERROR）、`tool`（工具名）、`trace_id`（从环境变量 `TRACE_ID` 读，无则自动生成 `batch-YYYYMMDD-HHMMSS-xxxx`）、`surface`（操作面，固定 `tool`）、`message`、`duration_ms`（可选）
   - 三面分类：操作面（工具自动写）、认知面（Agent 写 worklog）、上下文面（工具启动时写环境快照）
   - 日志写到 `data/logs/YYYY-MM-DD.jsonl`
   - 日志轮转：保留 30 天
3. 新建 `tools/log_query.py`：
   - `log_query.py --trace-id <id>`：按 trace_id 过滤
   - `log_query.py --tool <name>`：按工具过滤
   - `log_query.py --level ERROR`：按级别过滤
   - `log_query.py --grep "关键词"`：grep 消息
   - `log_query.py --since "2026-09-14 20:00"`：按时间范围
   - 输出彩色格式化（纯标准库，不依赖 rich）
4. 在 `tools/gate_engine.py` 和 `tools/atom_evidence_replay.py` 中接入日志（每个检查项开始/结束各一条 INFO，错误一条 ERROR）。
5. 在 `cppbible.py` 的 quality 步骤中，启动时设置 `TRACE_ID` 环境变量并写一条上下文面日志（记录工具版本、git HEAD、参数）。

**验证**：
- 跑一次 `python tools/gate_engine.py --check`，确认 `data/logs/` 下生成了 JSON Lines 文件
- 跑 `python tools/log_query.py --tool gate_engine --level ERROR`，能正确过滤
- 存量 gate/replay 行为不变（BLOCK/WARN 数不变）

**commit**：`feat(observability): 统一日志 JSON Lines + Trace ID + log_query CLI`

---

### 任务 5：知识图谱 L1

**目标**：解析 atoms/evidence/misconceptions → SQLite 图数据库 + 5 个查询 CLI。

**步骤**：

1. 先 Read `tools/impact_analysis.py`（已有单层依赖分析），复用其 frontmatter 解析逻辑。
2. 新建 `tools/knowledge_graph.py`：

   **Schema**（SQLite）：
   ```sql
   CREATE TABLE IF NOT EXISTS nodes (
       id TEXT PRIMARY KEY,
       type TEXT NOT NULL,  -- ATOM/EVIDENCE/MISCONCEPTION/FIXTURE/ARTIFACT/RULE
       path TEXT,
       title TEXT,
       status TEXT
   );
   CREATE TABLE IF NOT EXISTS edges (
       src TEXT NOT NULL,
       dst TEXT NOT NULL,
       type TEXT NOT NULL,  -- PREREQUISITE/SPECIALIZES/REALIZES/EVOLVED_FROM/SERVES/REFERENCES/USES/FIXTURES/ASSERTS/CONTRADICTS
       PRIMARY KEY (src, dst, type),
       FOREIGN KEY (src) REFERENCES nodes(id),
       FOREIGN KEY (dst) REFERENCES nodes(id)
   );
   CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(src);
   CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(dst);
   CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(type);
   CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
   ```

   **PRAGMA**：
   ```python
   conn.execute("PRAGMA journal_mode=WAL")
   conn.execute("PRAGMA synchronous=NORMAL")
   conn.execute("PRAGMA cache_size=-64000")
   conn.execute("PRAGMA mmap_size=268435456")
   ```

   **图构建**：
   - 遍历 `atoms/` 下所有 .md，解析 frontmatter → ATOM 节点
   - 遍历 `evidence/` 下所有 .md → EVIDENCE 节点
   - 遍历 `misconceptions/` 下所有 .md → MISCONCEPTION 节点
   - 解析 relations 字段 → edges（prerequisite/specializes/realizes/evolved_from/contradicts）
   - 解析 serves 字段 → edges（SERVES）
   - 解析 fixture 字段 → edges（USES/FIXTURES）
   - 解析 artifact 字段 → edges（ASSERTS）

   **5 个查询 CLI**：
   - `knowledge_graph.py deps <ATOM-ID>`：直接依赖
   - `knowledge_graph.py impact <FILE>`：上游影响（改了这个文件影响哪些原子）
   - `knowledge_graph.py orphans`：孤立节点（无入边无出边）
   - `knowledge_graph.py chain <ATOM-ID>`：完整依赖链（多跳）
   - `knowledge_graph.py stats`：图统计（节点数/边数/类型分布）

3. SQLite 文件存 `data/knowledge_graph.db`。
4. 跑一次构建，确认 stats 输出合理（28 atoms + 56 evidence + 80 misconceptions ≈ 164 节点）。
5. 验证 deps/impact 查询与现有 `impact_analysis.py` 结果一致（至少对几个已知原子对比）。

**验证**：
- `python tools/knowledge_graph.py stats` 输出节点数≈164、边数合理
- `python tools/knowledge_graph.py orphans` 不报错
- gate BLOCK=0 不变（知识图谱不影响现有门禁）
- pytest 加 3 个测试：图构建不报错、deeps 查询返回正确类型、orphans 不崩溃

**commit**：`feat(kg): 知识图谱 L1 — SQLite 图构建 + 5 查询 CLI`

---

### 任务 6：质量度量 L1

**目标**：25 指标自动采集 + metrics.jsonl + 阈值告警。

**步骤**：

1. 先 Read `tools/gen_metrics.py`（已有基础），看现有指标。
2. 新建 `tools/metrics_collector.py`：

   **5 类 25 指标**：
   ```
   质量类（Quality）：
   - gate_block_count
   - gate_warn_count
   - gate_rule_count
   - poison_pass_count
   - poison_total_count
   - poison_coverage_pct
   - replay_confirm_count
   - replay_refute_count
   - replay_infra_error_count

   资产类（Assets）：
   - atoms_total
   - atoms_verified
   - atoms_draft
   - evidence_total
   - evidence_confirm
   - misconceptions_total
   - asm_files_count

   性能类（Performance）：
   - pytest_wall_seconds
   - replay_wall_seconds
   - gate_wall_seconds
   - ci_total_seconds（估算）

   成本类（Cost）：
   - cost_tracker_total_tokens（从 cost_tracker.py 读）
   - cost_tracker_atoms_per_batch
   - cost_tracker_avg_per_atom

   健康类（Health）：
   - git_ahead_count
   - git_untracked_count
   - debt_ledger_open_count
   - golden_state_atoms_match
   ```

3. 每个指标从对应工具的 `--json` 输出或直接调用获取：
   - gate/poison/replay → 调用工具并解析输出
   - pytest → 从最新 pytest 运行结果读（如果有的话）
   - cost_tracker → 读 data/cost_tracker.json（如果存在）
   - git → `git rev-list --count origin/master..HEAD` 等
4. 每次采集追加一条到 `data/metrics.jsonl`（一行 JSON，含 timestamp + 所有指标）。
5. 阈值告警（硬阈值，只 WARN 不 BLOCK）：
   - gate_block_count > 0 → ERROR
   - replay_refute_count > 0 → ERROR
   - pytest_wall_seconds > 300 → WARN
   - poison_coverage_pct < 50 → WARN
6. `metrics_collector.py history --last 10` 输出最近 10 次采集的趋势。

**验证**：
- 跑一次 `python tools/metrics_collector.py`，确认输出 25 个指标
- `data/metrics.jsonl` 追加了一行
- 硬阈值触发正确（当前 gate_block=0 应该不告警）
- pytest 加 2 个测试：采集不崩溃、jsonl 可解析

**commit**：`feat(metrics): 质量度量 L1 — 25 指标采集 + jsonl + 阈值告警`

---

## 三、安全备份（任务 7）

### 任务 7：数据备份

**目标**：关键数据文件自动备份，支持一键恢复。

**步骤**：

1. 新建 `tools/backup.py`：
   - `snapshot()`：备份白名单文件到 `data/backups/YYYY-MM-DD-HHMMSS/`
   - 白名单：
     - `data/golden_state.json`
     - `data/metrics.jsonl`
     - `data/knowledge_graph.db`（任务 5 完成后）
     - `Examples/atoms/artifact_versions.json`
     - `tools/golden_state.json`（如果存在于 tools/）
   - `list()`：列出所有备份
   - `restore <backup_dir>`：从备份恢复（用 shutil.copy2，不删原文件，覆盖前先 .bak）
   - `cleanup()`：保留最近 10 份，更老的删除
2. 在 `cppbible.py quality` 的最后一步自动调用 `backup.snapshot()`。
3. 在 `.gitignore` 中加 `data/backups/`（备份不入库）。

**验证**：
- `python tools/backup.py snapshot` 生成备份目录
- `python tools/backup.py list` 列出备份
- 备份目录中白名单文件都存在
- pytest 加 2 个测试：snapshot 不崩溃、restore 不崩溃（用临时目录）

**commit**：`feat(backup): 关键数据自动备份 + 一键恢复`

---

## 四、收工验证（全部任务完成后）

按顺序跑以下命令，记录输出：

```powershell
# 1. 门禁
python tools/gate_engine.py --check
# 期望：BLOCK=0，WARN 数与开工前一致或只多新规则暴露的存量债

# 2. 毒样例
python tools/poison_drill.py
# 期望：exit 0，全部 pass

# 3. 回放
python tools/atom_evidence_replay.py --check --incremental
# 期望：confirm=56，refute=0，infra_error=0

# 4. pytest
python -m pytest -n auto --tb=short
# 期望：全绿，记录 wall 时间

# 5. 新工具验证
python tools/knowledge_graph.py stats
python tools/metrics_collector.py
python tools/backup.py list
python tools/log_query.py --help

# 6. git 状态
git status --porcelain
git log --oneline origin/master..HEAD | Measure-Object -Line
```

**收工门禁标准**：
- gate BLOCK=0
- poison 全过 exit 0
- replay confirm=56
- pytest 全绿
- 新工具不崩溃
- 工作树干净（无临时件残留）

---

## 五、交付物清单

| 交付物 | 路径 | 说明 |
|---|---|---|
| 提交 | 7 个 commit | 每个任务一个 |
| worklog | `_worklog_508.md` | 实测数字、偏差、复现命令 |
| 新工具 | `tools/observability.py` | 统一日志 |
| 新工具 | `tools/log_query.py` | 日志查询 |
| 新工具 | `tools/knowledge_graph.py` | 知识图谱 |
| 新工具 | `tools/metrics_collector.py` | 质量度量 |
| 新工具 | `tools/backup.py` | 数据备份 |
| 修改 | `.github/workflows/ci.yml` | matrix 并行 + 增量 replay |
| 修改 | `pyproject.toml` 或 `pytest.ini` | xdist 配置 |
| 修改 | `tools/gate_engine.py` / `tools/atom_evidence_replay.py` | 接入日志 |
| 修改 | `.gitignore` | data/backups/ |
| pytest | `tests/test_observability.py`（新） | 日志测试 |
| pytest | `tests/test_knowledge_graph.py`（新） | 图谱测试 |
| pytest | `tests/test_metrics.py`（新） | 度量测试 |
| pytest | `tests/test_backup.py`（新） | 备份测试 |

---

## 六、已知风险与注意事项

1. **pytest-xdist 测试隔离**：如果有测试依赖文件顺序或共享临时目录，并行会失败。用 `@pytest.mark.serial` 标记，不要改测试逻辑。
2. **知识图谱 YAML 解析**：现有 28 原子 + 56 证据卡的 relations 字段格式可能不统一（字符串 vs 列表 vs mapping）。要做兼容处理，不要求改存量卡。
3. **metrics_collector 调用各工具**：不要 fork 新进程，直接 import 并调用函数（如果可行）；必须 fork 的话用 subprocess 并捕获输出。
4. **备份 restore 不删原文件**：恢复时覆盖前先 .bak，不做不可逆操作。
5. **可观测性接入 gate/replay 时不要改变现有逻辑**：只加日志调用，不改检查逻辑。如果加日志导致性能下降 >10%，记录 WARN 但不 BLOCK。
6. **ci.yml 本地无法验证**：只改 YAML 并确保语法正确，不跑 CI。
7. **不 golden sync、不 push**：完成后报告 ahead 数，人审后再推。

---

*文档编号 508。这是 P0 性能收尾 + 智能基建第一批的执行提示词。完成后系统从"13 个工具集合"升级为"有统一日志、知识图谱、质量度量、自动备份的五层架构雏形"。*
