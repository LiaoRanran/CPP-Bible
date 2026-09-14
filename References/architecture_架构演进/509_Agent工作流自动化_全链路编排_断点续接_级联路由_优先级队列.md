# 509 Agent 工作流自动化与全链路编排

> 日期：2026-09-14
> 触发：用户痛点——"Agent 干活一次只能 500 次请求，到顶了就得人为续上"、"队列设计和资源分配不好"、"速度慢"
> 业内：FrugalGPT 级联路由、agentpause 预测式暂停、HIVEMIND OS 式调度、PROGRESS.md 断点续接、Durable Execution
> 性质：架构设计 + 落地规格

---

## 一、当前痛点（实测）

| 痛点 | 现状 | 后果 |
|---|---|---|
| 500 请求上限 | 苦力 Agent 跑到 500 次就停，要人手动开新会话 | 夜间无人值守时进度中断 |
| 断点丢失 | 新会话没有上一会话上下文，要重新读 worklog | 重复劳动 + token 浪费 |
| 队列串行 | 一次只投喂一个任务包，做完才投下一个 | 机器空闲时间浪费 |
| 无优先级 | 所有任务同等排队，紧急修复可能等在低优任务后 | 安全漏洞修复延迟 |
| 无模型路由 | 所有任务都用同一个模型（或手动切换） | 简单任务浪费好模型额度 |
| 无 token 熔断 | cost_tracker 只记账不预警 | 一批跑完才发现超预算 |
| 无进度可见 | 不知道 Agent 跑到哪一步、预计还要多久 | 用户无法决策是否介入 |

---

## 二、业内先进模式

### 2.1 断点续接（解决 500 请求上限）

**模式 A：PROGRESS.md（最简单，零依赖）**
- Agent 每完成一步就更新 `PROGRESS.md`：已完成什么、下一步是什么、关键决策记录
- 新会话提示词第一行："Read PROGRESS.md and continue"
- 优点：零依赖、任何 Agent 都能用
- 缺点：Agent 可能不严格更新

**模式 B：agentpause 预测式暂停**
- 在撞到 rate limit 之前主动暂停（基于已用请求数估算）
- 序列化应用级状态（不是 LLM 上下文，而是文件系统状态）
- 到了重置时间自动恢复
- 关键：不重做已完成的工作

**模式 C：Durable Execution（durable task cache）**
- 每个 LLM 调用/工具调用作为一个 task
- 成功的 task 结果缓存
- 重试时跳过已成功的 task，从失败点继续
- 要求：task 边界清晰、副作用工具幂等

**我们的选择**：A+B 组合。
- PROGRESS.md 我们已经在做（_worklog_*.md），但要规范化为 `data/agent_state/PROGRESS.md`
- agentpause 模式：task_state 工具（494 已建）记录已完成的子任务数，接近 500 时写 checkpoint 并优雅停止

### 2.2 多模型级联路由（FrugalGPT）

**核心洞察**：~80% 的真实查询简单到小模型就能处理，只有 ~20% 需要强模型。

```
任务进来
  │
  ▼
[便宜模型 混元4p/hy4p] ──→ 验证器判断 ──→ 通过？──→ 接受
  │                                         │
  │                                         └─ 不通过
  │                                              │
  ▼                                              ▼
[中档模型 DS v4.1 Flash] ──→ 验证器判断 ──→ 通过？──→ 接受
  │                                         │
  │                                         └─ 不通过
  │                                              │
  ▼                                              ▼
[强模型 Seed-Evolving/本模型] ──→ 直接接受（天花板）
```

**验证器怎么做**（不训练路由模型）：
- 机械规则：gate block=0? poison 全过? pytest 全绿? → 自动通过
- 红队盲读：对"是否需要人审"的判断
- 置信度：Agent 自评 + 门禁结果加权

**成本数学**（参考业内）：
- 大模型 20x 成本，中模型 5x，便宜模型 1x
- 80% 在便宜模型接受，15% 在中模型接受，5% 升级到大模型
- 平均成本 = 0.8×1 + 0.15×5 + 0.05×20 = 0.8 + 0.75 + 1.0 = 2.55x
- vs 全用大模型 20x = **87% 成本节省**

### 2.3 任务队列与调度（HIVEMIND）

**优先级模型**（OS 式调度）：
```
P0 CRITICAL  —— 安全漏洞/门禁红灯/CI 失败（立即抢占）
P1 HIGH      —— 阻断性 bug 修复/新规则开发
P2 NORMAL    —— 新原子生产/新工具开发
P3 LOW       —— 调研/文档优化/非关键改进
```

**排序规则**：
1. 优先级高的先跑
2. 同优先级：短作业优先（SJF，预估 token 少的先跑）
3. 同优先级同长度：FIFO

**依赖 DAG**：
- 任务间依赖（如"知识图谱"依赖"frontmatter 解析稳定"）
- 阻塞任务自动跳过，独立任务继续执行
- 循环检测

**并行度**：
- Claude Code 官方建议：每轮最多 3 个并行 subagent
- 超过 3 个分批，批次间串行
- 我们：同时最多 2 个苦力（一个改代码 + 一个跑测试/调研）

### 2.4 Token 预算与熔断

**每层预算**（不是总预算，是每步预算）：
```
每批任务：
  ├── 单个子任务预算：~500 请求（接近上限就 checkpoint）
  ├── 单批总预算：~3000 请求
  └── 当日总预算：~5000 请求（到 80% 告警）
```

**熔断规则**：
- 子任务跑到 450 请求：写 checkpoint，优雅停止
- 连续 3 次同一错误：kill，换模型或换策略
- gate 红灯 >3 次不收敛：暂停，报告人审
- token 用量超预算 120%：强制暂停

---

## 三、落地设计

### 3.1 Agent 状态管理（解决 500 上限）

**新建 `tools/agent_state.py`**：

```
data/agent_state/
├── PROGRESS.md          # 当前任务进度（Agent 每步更新）
├── checkpoint.json      # 机器可读的检查点（已完成子任务列表）
├── active_agents.json    # 当前活跃 Agent 列表
└── task_history.jsonl   # 所有任务历史
```

**PROGRESS.md 模板**：
```markdown
# 当前任务：<任务名>
## 已完成
- [x] 子任务 1（commit abc123）
- [x] 子任务 2（commit def456）
## 进行中
- [ ] 子任务 3：<具体步骤>
## 下一步
1. <第一步>
2. <第二步>
## 关键决策
- <决策>：<理由>
## 注意事项
- <坑1>：<怎么避免>
```

**checkpoint.json 结构**：
```json
{
  "task_id": "508",
  "model": "hunyuan-4p",
  "requests_used": 450,
  "requests_limit": 500,
  "subtasks_done": ["task1", "task2", "task3"],
  "subtasks_pending": ["task4", "task5"],
  "next_step": "Read PROGRESS.md and continue",
  "last_commit": "abc123",
  "updated_at": "2026-09-14T20:00:00"
}
```

**自动续接流程**：
1. Agent 跑到 ~450 请求：agent_state.py 检测到接近上限
2. 写 checkpoint.json + 更新 PROGRESS.md
3. 优雅退出（完成当前子任务后停止，不半路切断）
4. 人或自动系统开新会话，提示词第一行：`Read data/agent_state/PROGRESS.md and continue the interrupted work.`
5. 新 Agent 读 PROGRESS.md，从 pending 继续

### 3.2 任务队列（解决串行问题）

**新建 `tools/task_queue.py`**（扩展 494 的 task_state）：

```
task_queue.py submit --title "任务名" --priority P2 --model cheap --prompt-file <path>
task_queue.py pop                    # 取最高优先级可执行任务
task_queue.py list                   # 列出所有任务
task_queue.py complete <task_id>      # 标记完成
task_queue.py fail <task_id> <reason> # 标记失败
task_queue.py retry <task_id>         # 重新入队
```

**队列存储**：`data/task_queue.jsonl`（每行一个任务）

**任务结构**：
```json
{
  "id": "508",
  "title": "P0性能+智能基建",
  "priority": "P1",
  "model": "cheap",
  "prompt_file": "References/.../508_*.md",
  "status": "pending|running|done|failed",
  "depends_on": [],
  "estimated_tokens": 3000,
  "created_at": "...",
  "started_at": "...",
  "completed_at": "..."
}
```

**调度逻辑**：
1. 扫描队列，取 status=pending 且 depends_on 全部 done 的任务
2. 按优先级排序（P0>P1>P2>P3）
3. 同优先级按 estimated_tokens 升序（短作业优先）
4. 分配给空闲 Agent（同一时间最多 2 个并行）
5. 任务开始时标记 running + started_at

### 3.3 模型路由（解决"简单任务用好模型"）

**新建 `config/model_routes.yaml`**：

```yaml
# 模型分级
tiers:
  cheap:
    models: ["hunyuan-4p", "hy4p"]
    use_for:
      - 机械代码修改
      - 文档整理
      - 测试编写
      - 数据迁移
      - 重复性检查
  mid:
    models: ["ds-v4.1-flash"]
    use_for:
      - 新工具开发
      - 规则设计
      - 红队分析
      - 架构设计
  strong:
    models: ["seed-evolving", "本模型"]
    use_for:
      - 对抗测试
      - 架构决策
      - 复杂调试
      - 人审决策

# 级联策略
cascade:
  start_tier: cheap
  escalate_on:
    - gate_block_gt_3    # gate block > 3 次不收敛
    - redteam_block_gt_2 # 红队 block > 2
    - retry_count_gt_3   # 同一错误重试 > 3 次
  max_escalations: 2
```

**任务提交时自动选模型**：
- 提示词中标注 `model_route: cheap/mid/strong`
- 系统根据任务类型自动分配
- 如果 cheap 模型 3 次失败，自动升级到 mid
- 如果 mid 3 次失败，升级到 strong

### 3.4 Token 预算与熔断

**扩展 cost_tracker.py（421 已有基础）**：

```
预算层级：
├── 单次会话：500 请求（硬上限，接近即 checkpoint）
├── 单批任务：3000 请求
├── 单日：5000 请求（到 80% 告警）
└── 单周：30000 请求

熔断规则：
1. requests_used >= 450 → 写 checkpoint，优雅停止
2. 同一错误连续 3 次 → kill 当前子任务，换模型或换策略
3. gate 红灯 >3 次 → 暂停，报告人审
4. 日预算 80% → WARN；100% → 暂停所有 P2/P3
```

**cost_tracker 扩展字段**：
- `model`：用了哪个模型
- `tier`：cheap/mid/strong
- `task_id`：哪个任务
- `step`：哪个步骤

---

## 四、与现有系统的集成

| 现有工具 | 集成点 | 改动 |
|---|---|---|
| task_state.py（494） | 升级为 task_queue.py | 加优先级+依赖+调度 |
| cost_tracker.py（421） | 加 tier/task_id/step | 按模型和任务分类统计 |
| writer_selfcheck.py（420） | 作为级联验证器 | gate 结果决定是否升级 |
| cppbible.py | quality 步骤加预算检查 | 到预算暂停 |
| prompt 文件 | frontmatter 加 model_route | 自动选模型 |
| _worklog_*.md | 规范化为 PROGRESS.md | 自动续接 |

---

## 五、落地优先级

| 优先级 | 任务 | 工作量 | 解决什么痛点 |
|---|---|---|---|
| **P0** | PROGRESS.md 规范化 + checkpoint | 1h | 500 上限断点丢失 |
| **P0** | agent_state.py 自动续接 | 2h | 无人值守夜间运行 |
| **P1** | task_queue.py 优先级调度 | 3h | 串行+无优先级 |
| **P1** | model_routes.yaml + 级联 | 2h | 简单任务浪费好模型 |
| **P2** | cost_tracker 预算熔断 | 2h | token 失控 |
| **P2** | 并行 Agent 协调（最多2个） | 2h | 机器空闲浪费 |

**P0 两项（3h）解决最痛的"500 上限要人为续"问题**。夜间可以让苦力跑到 checkpoint 自动停，人早上开新会话一句"Read PROGRESS.md and continue"就续上。

---

## 六、预期效果

| 指标 | 当前 | 落地后 |
|---|---|---|
| 夜间无人值守 | 跑到 500 次停，等人续 | 跑到 450 自动 checkpoint，早上一句续 |
| 任务排队 | 手动投喂，串行 | 队列自动调度，P0 优先 |
| 模型选择 | 手动选 | 自动级联：80% 便宜模型干，20% 升级 |
| token 浪费 | 无感知 | 每步预算+熔断+分类统计 |
| 并行度 | 1 | 2（一个改代码+一个跑测试） |
| 断点恢复 | 重新读 worklog | 读 PROGRESS.md 一句话续 |

---

## 七、一句话总结

Agent 工作流自动化的核心是**三句话**：
1. **跑到顶自动停，留好路标让人一句话续**——PROGRESS.md + checkpoint，不重做工作
2. **便宜模型先干，干不动再升级**——FrugalGPT 级联，80% 成本节省
3. **紧急任务插队，机器别闲着**——优先级队列 + 并行调度

这解决了用户最痛的"500 次就要人为续"和"速度慢"两个问题。P0 两项 3h 就能落地。

---

*文档编号 509。Agent 工作流自动化与全链路编排设计。P0 两项可立即执行，与 508 并行不冲突（508 是基建，509 是调度基建上的工作流）。*
