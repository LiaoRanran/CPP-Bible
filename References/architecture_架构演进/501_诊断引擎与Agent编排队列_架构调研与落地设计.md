# 501 诊断引擎与 Agent 编排队列 · 架构调研与落地设计

> 日期：2026-09-14
> 触发：用户明确点出"跑得慢、队列设计不好、性能优化和资源分配设计的不好"
> 范围：①统一诊断引擎（把分散的 gate/replay/poison 输出聚合成"问题→根因→修复建议"）②Agent 任务编排队列（优先级、token 预算、并发、熔断）
> 方法：业内先进实践检索 → 与当前系统差距分析 → 可落地架构设计

---

## 一、诊断引擎（Diagnostic Engine）

### 1.1 业内先进实践

| 系统 | 核心机制 | 可借鉴点 |
|---|---|---|
| **LogSage**（arXiv 2506.03691, 2025） | token-efficient 日志预处理去噪 → 结构化诊断 prompt 做 RCA → RAG 复用历史修复 → tool-calling 自动修复 | 日志预处理管道、结构化诊断、历史修复 RAG |
| **AWS DevOps Agent**（2026） | 自动关联 pipeline 失败与具体 commit，识别哪个变更引入问题，生成 mitigation plan | 失败-变更关联（git blame 级） |
| **PipelineIQ**（npm, 2026） | 原始 pipeline 失败 → 高保真 incident ticket（RCA + 修复建议 + 去重）→ 自动生成 Draft PR + 安全护栏 | 去重聚类、自动 PR、安全护栏 |
| **cicd-intelligent-recovery**（GitHub Skill, 2026） | 三循环集成：Loop1 规划 → Loop2 实现 → Loop3 CI/CD 智能恢复，失败模式反馈回 Loop1 | 失败模式反馈闭环 |

**共性架构**（四个系统都有的层）：
```
原始信号 → 去噪/预处理 → 结构化诊断（RCA）→ 历史修复检索（RAG）→ 修复建议/自动修复 → 安全护栏
```

### 1.2 当前系统的差距

当前 13 个工具各跑各的，输出是分散的：

| 工具 | 输出格式 | 问题 |
|---|---|---|
| gate_engine | Finding 列表（rule_id, severity, file, message） | 同根因多 Finding 不聚合 |
| atom_evidence_replay | confirm/refute/infra_error + 逐 key 比对 | refute 原因分散在 stderr |
| poison_drill | pass/fail + 覆盖率 | 失败时只说哪条毒样例挂了，不说为什么 |
| golden_lock | 恶化/改善计数 | 不告诉你哪条规则导致恶化 |
| writer_selfcheck | 7 项 WC pass/fail | 失败项没有修复建议 |

**Agent 的痛点**：跑完一轮门禁后，要自己读 5 个工具的输出、判断哪些是真问题、哪些是存量债、优先级怎么排、先修哪个。这部分完全靠 Agent 的智能，没有结构化辅助。

### 1.3 诊断引擎架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   tools/diagnose.py                      │
│                                                          │
│  ┌──────────┐   ┌───────────┐   ┌────────────┐          │
│  │ 信号聚合  │→ │ 去重聚类  │→ │ 根因分类器  │          │
│  │ (5工具)  │   │ (同根因)  │   │ (规则→类型)│          │
│  └──────────┘   └───────────┘   └─────┬──────┘          │
│                                       │                 │
│  ┌──────────┐   ┌───────────┐   ┌────▼──────┐          │
│  │ 优先级排  │← │ 修复建议库 │← │ 影响面评估  │          │
│  │ 序(P0-P3)│   │ (RAG)     │   │ (多少卡)  │          │
│  └────┬─────┘   └───────────┘   └───────────┘          │
│       │                                                │
│  ┌────▼──────────────────────────────────────────┐     │
│  │        结构化诊断报告 (JSON + Markdown)         │     │
│  │  [{                                           │     │
│  │    id: "DIAG-001",                            │     │
│  │    severity: "block",                         │     │
│  │    root_cause: "EV-RUN-KEY-DECLARED-EXISTS",  │     │
│  │    affected: ["EV-MEM-040", "EV-UB-001"],     │     │
│  │    fix_hint: "...",                           │     │
│  │    historical_fix: "commit 1e8ba16",          │     │
│  │    effort: "S"  // S/M/L                      │     │
│  │  }]                                           │     │
│  └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

**五层设计**：

1. **信号聚合层**：调用 gate/replay/poison/golden_lock/selfcheck，收集原始输出（JSON 模式，403 已落地 --json）。
2. **去重聚类层**：按 `(rule_id, root_cause_pattern)` 聚合。例如 EV-OUT-UNDECLARED-KEY 命中 6 张卡 → 聚合成 1 个诊断项，affected 列 6 张卡。
3. **根因分类器**：规则 → 根因类型映射表（纯机械，零 LLM）：
   - `EV-ASSERT-*` → "断言问题"（符号不可映射/判别力不足/恒真）
   - `EV-OUT-*` → "留痕问题"（未声明键/陈旧/不存在）
   - `EV-ARTIFACT-*` → "工件问题"（版本不匹配/不存在/被篡改）
   - `ATOM-*` → "原子元数据问题"（缺字段/ID冲突/状态非法）
   - `PED-*` → "教学法问题"（pedagogy 格式）
   - `MATRIX-*` → "矩阵问题"（缺 matrix 字段）
4. **修复建议库**：每个根因类型对应已知修复模式（从历史 commit 中提取）。例如：
   - "断言问题-符号不可映射" → "检查卡内 symbol_map 是否声明了跨形态映射；MinGW 下 operator new 是 _Znwy 不是 _Znwm"
   - "工件问题-版本不匹配" → "重生成工件并更新 artifact_sha256；参考 commit d8b6b18d"
   - 初始版本硬编码 10-15 条最常见修复模式，后续从 commit 历史自动提取。
5. **优先级排序**：
   - P0：block 级且影响 verified 原子（直接阻断生产）
   - P1：block 级且影响 draft 原子 / warn 级且影响面 >3 张卡
   - P2：warn 级且影响面 ≤3 张卡 / advice 级
   - P3：存量债（已在 golden_lock 基线中接受的 warn）

**输出**：`diagnose_report.json`（机器可读）+ `diagnose_report.md`（人读），Agent 拿到报告后直接按 P0→P3 顺序修，不需要自己分析 5 个工具的输出。

### 1.4 落地路径（分三阶段）

| 阶段 | 内容 | 工作量 |
|---|---|---|
| L1 | 信号聚合 + 去重聚类 + 根因分类 + 优先级排序（纯机械，零 LLM） | 1 个苦力批次 |
| L2 | 修复建议库（硬编码 15 条常见模式）+ 历史 commit 关联 | 1 个苦力批次 |
| L3 | RAG 历史修复检索（从 docs/kernel/ 和 git log 中自动提取修复模式） | 好模型批次 |

---

## 二、Agent 编排队列（Task Orchestration Queue）

### 2.1 业内先进实践

| 系统 | 核心机制 | 可借鉴点 |
|---|---|---|
| **Astraea**（alphaXiv 2512.14142, 2025） | 多级优先级队列 Q0-Qn；新请求 Q0 快速响应；I/O 密集型提升优先级；计算密集型超 token 阈值降级 | 多级队列、token 感知升降级 |
| **HIVEMIND**（arXiv 2604.17111, 2026） | OS 启发的调度；token 预算管理（85% 警告/100% 终止）；熔断器状态机（closed→open→half-open） | token 预算、熔断器 |
| **Kairos**（arXiv 2508.06948, 2026） | workflow-aware 优先级调度器 + memory-aware dispatcher；优化端到端延迟 | 工作流感知调度 |
| **Stanford DAG-Aware**（CS244c, 2026） | DAG 感知调度；最高优先级超预算时跳过调度下一个能 fit 的（skip 策略）；bisect-sorted index O(log n) 预算查询 | 跳过策略、预算感知 |
| **Databricks Lakebase** | Postgres 任务队列：`SELECT ... WHERE status='pending' ORDER BY priority DESC, created_at FOR UPDATE SKIP LOCKED` | 简单可靠的队列实现 |
| **Zylos Token Economics**（2026） | session ceiling（单会话上限）、per-agent daily cap、硬约束+软评分两阶段路由 | token 经济学 |

**共性设计**：
- 优先级队列（不是 FIFO）
- Token 预算（每任务/每会话/每日上限）
- 熔断器（连续失败暂停）
- 并发控制（同时跑几个）
- 跳过策略（高优先级阻塞时不浪费资源）

### 2.2 当前系统的差距

- **无队列**：用户手动投喂提示词，Agent 串行执行，一个任务卡住就全停
- **无优先级**：所有任务平等，清理任务和阻断修复任务抢资源
- **无 token 预算**：Agent 可能无限循环（虽然有 500 请求上限，但没有 token 级预算）
- **无并发**：同时只能跑 1 个 Agent（苦力/好模型/对抗是用户手动开的不同会话）
- **无熔断**：连续失败不暂停，可能白烧 token
- **无状态持久化**：Agent 中断后进度丢失（靠 _worklog_*.md 手动记录）

### 2.3 编排队列架构设计

```
┌──────────────────────────────────────────────────────┐
│              tools/task_queue.py                       │
│                                                       │
│  ┌────────────┐  ┌──────────┐  ┌────────────────┐    │
│  │ 任务提交    │→ │ 优先级队列│→ │ Dispatcher     │    │
│  │ (CLI/API)  │  │ P0-P3    │  │ (取最高优先级)  │    │
│  └────────────┘  └────┬─────┘  └───────┬────────┘    │
│                       │                │             │
│                  ┌────▼────┐    ┌──────▼──────┐      │
│                  │ Token   │    │ 并发控制     │      │
│                  │ 预算器  │    │ (N workers)  │      │
│                  │ 85%警告 │    │              │      │
│                  │ 100%终止│    └──────┬──────┘      │
│                  └────┬────┘           │             │
│                       │          ┌────▼──────┐      │
│                  ┌────▼────┐     │ 熔断器     │      │
│                  │ 状态持久化│     │ (连续失败) │      │
│                  │ (SQLite) │     └───────────┘      │
│                  └─────────┘                        │
└──────────────────────────────────────────────────────┘
```

**核心数据结构**（SQLite 或 JSON 文件，零外部依赖）：

```python
Task = {
    id: "T-001",
    title: "修复 _assert_haystack 整仓 rglob",
    prompt_file: "References/.../500_...md",  # 提示词路径
    priority: "P0",  # P0阻断修复 > P1新规则 > P2分析 > P3清理
    status: "pending|running|done|failed|cancelled",
    agent_type: "cheap|strong|adversarial",  # 用什么模型
    token_budget: 50000,  # token 上限
    token_used: 0,
    attempts: 0,
    max_attempts: 2,
    depends_on: ["T-000"],  # DAG 依赖
    created_at: "...",
    started_at: "...",
    finished_at: "...",
    result: "commit hashes / report path",
    error: "..."
}
```

**关键机制**：

1. **优先级队列**：P0（阻断修复/门禁红）> P1（新规则/新工具）> P2（分析报告/审计）> P3（清理/索引）。同优先级 FIFO。
2. **Token 预算**：每任务设 token_budget（默认 50K for 差模型，200K for 好模型）。85% 时 Agent 收到警告（应开始收尾），100% 时强制终止并标记 failed。
3. **并发控制**：配置 `max_workers`（当前 1，未来可 2-3）。Dispatcher 每次取最高优先级且依赖已满足的任务。
4. **熔断器**：同一类型任务连续失败 3 次 → 该类型暂停 30 分钟，避免白烧 token。
5. **跳过策略**（借鉴 Stanford）：最高优先级任务的 token 预算超过当前可用额度时，跳过它调度下一个能 fit 的，不浪费空闲。
6. **状态持久化**：SQLite（`data/task_queue.db`），Agent 中断后可恢复。`task_state.py`（494 已建）可扩展为完整队列。
7. **DAG 依赖**：任务可声明 depends_on，依赖未完成的任务不调度。

**CLI 接口**：
```bash
python tools/task_queue.py submit --prompt 500_xxx.md --priority P0 --agent cheap
python tools/task_queue.py list --status pending
python tools/task_queue.py run --worker-id 1  # 单个 worker 取任务执行
python tools/task_queue.py stats  # 队列统计
```

### 2.4 落地路径（分三阶段）

| 阶段 | 内容 | 工作量 |
|---|---|---|
| L1 | 任务队列核心（提交/列表/取任务/状态更新）+ SQLite 持久化 + 优先级 | 1 个苦力批次 |
| L2 | Token 预算 + 熔断器 + 并发控制 + 跳过策略 | 1 个好模型批次 |
| L3 | DAG 依赖 + 自动重试 + 队列统计仪表盘 | 1 个好模型批次 |

---

## 三、与现有系统的集成点

### 3.1 诊断引擎 ↔ 现有工具

- 403 已落地 `--json` 输出（4 工具）→ 诊断引擎直接消费 JSON，不需要解析文本
- `impact_analysis.py`（425 已建）可复用：诊断引擎发现问题后，调用 impact_analysis 评估影响面
- `trace_logger.py`（498 已建）可记录诊断引擎的每次运行

### 3.2 编排队列 ↔ 现有工具

- `task_state.py`（494 已建）已有 4 子命令和 >450 自动 needs_continue → 扩展为完整队列
- `cost_tracker.py`（421 已建）已有 token 追踪 → 队列的 token 预算直接消费 cost_tracker 数据
- `cppbible.py quality` 门禁 → 队列的每个任务完成后自动跑 quality，失败则标记 failed

### 3.3 诊断引擎 ↔ 编排队列（闭环）

```
门禁红 → 诊断引擎生成结构化报告 → 每个诊断项自动创建队列任务（P0-P3）
  → Worker 取任务执行修复 → 修复后自动跑门禁 → 通过则任务 done
  → 不通过则 attempts+1，超 max_attempts 则 failed + 通知人审
```

这就是"自愈闭环"的雏形：从发现问题到修复验证全自动化，人只在 failed 时介入。

---

## 四、优先级建议

| 优先级 | 项目 | 理由 |
|---|---|---|
| **P0** | 诊断引擎 L1（信号聚合+去重+分类+排序） | 直接减少 Agent 分析 5 个工具输出的 token 消耗，提升修复效率 |
| **P1** | 编排队列 L1（任务队列核心+优先级+持久化） | 解决"手动投喂、串行执行"的根本问题 |
| **P2** | 诊断引擎 L2（修复建议库） | 减少 Agent 搜索历史修复的时间 |
| **P3** | 编排队列 L2（token 预算+熔断+并发） |  token 经济学，防止白烧 |
| **P4** | 诊断引擎 L3 + 队列 L3（RAG + DAG + 仪表盘） | 高级功能，等基础稳定后做 |

---

## 五、关键设计决策（已预判的坑）

1. **诊断引擎零 LLM**：L1/L2 全机械（规则映射、字符串匹配），不调用大模型。原因：诊断本身是确定性的，用 LLM 反而引入不确定性和 token 消耗。RAG 只在 L3 引入。
2. **队列用 SQLite 不用 Redis**：零外部依赖，单文件，Windows/WSL 都能用。并发量小（同时 ≤3 worker），SQLite 足够。
3. **Token 预算用估算不用精确**：API 返回的 token 计数最准，但本地 Agent 没有 API 访问。用 cost_tracker 的估算值（输入字符数/4 + 输出字符数/3），85% 警告留足余量。
4. **不做自动修复**：诊断引擎只给建议和创建任务，不自动改代码。自动修复由 Worker Agent 执行，保持"诊断与执行分离"。
5. **队列不替代提示词**：队列只是调度层，每个任务的执行逻辑仍由提示词文件定义。队列负责"什么时候跑、用什么模型跑、跑多久"，不负责"怎么跑"。

---

## 六、与 499/500 的衔接

- 500 批次修完 M5/M8 后，变异测试会产生新的逃逸报告 → 诊断引擎 L1 可以直接消费这些报告，自动生成修复任务
- 500 的 pytest 快慢标记（任务 6）→ 队列的 token 预算可以参考测试分类估算任务耗时
- 499 的 warn 审计 → 诊断引擎的根因分类器可以直接用审计报告的分类结果初始化

---

*文档编号 501，下一批次可直接用作文档输入。*
