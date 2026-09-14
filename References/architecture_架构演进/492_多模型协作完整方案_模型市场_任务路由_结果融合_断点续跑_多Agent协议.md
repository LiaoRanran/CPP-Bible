---
id: 492
title: 多模型协作完整方案 模型市场 任务路由 结果融合 断点续跑 多Agent协议
status: active
type: architecture-note
created_at: 2026-09-14
---
# 492 多模型协作完整方案
## 模型市场 + 任务路由 + 结果融合 + 断点续跑 + 多 Agent 协议

> 生成时间：2026-09-14
> 用户痛点："Agent 干活一次只能 500 次请求，到顶了就得我人为给它续上，有无全自动接管的办法"
> 现状：用户已经在人工做多模型协作（苦力/好模型/对抗模型），但全靠人判断"这个任务该给谁"

---

## 一、问题：多模型协作全靠人

### 现状

用户已经在用多个模型：
- **苦力**（便宜模型）：干杂活、修复、提交
- **好模型**（ds v4.1 flash）：落地系统基线、复杂架构
- **对抗模型**（Seed-Evolving/Trae/混元）：红队对抗
- **架构师**（当前模型）：调研消化、架构规划

但：
- 任务分配靠人判断（"这个任务该给谁？"）
- 没有模型能力档案（哪个模型擅长什么？成功率多少？）
- 没有结果融合（多个模型做同一任务，结果怎么对比？）
- **没有断点续跑**（Agent 500 次请求到顶，必须人手动续）
- 多 Agent 同时干活会冲突（487 任务队列在解决）

### 用户明确提出的痛点

> "Agent 干活一次只能 500 次请求这样，到顶了就得我人为的给它续上，有无全自动接管的办法"

---

## 二、模型市场

### 2.1 模型能力档案

`docs/kernel/model_marketplace.yaml`：

```yaml
models:
  cheap_agent:
    alias: 苦力
    model_family: qwen-hy4p  # 模型族（同族共享盲区）
    cost_per_1k_tok: 0.01     # 相对成本
    speed: fast               # fast/medium/slow
    request_limit: 500        # 单次会话请求上限
    strengths:
      - 机械任务（改字段、补测试、跑门禁）
      - 格式调整、文件整理
      - 简单代码修改
    weaknesses:
      - 架构设计、新工具开发
      - 复杂 claim 改写
      - 跨文件重构
    success_rate:
      mechanical: 0.85
      semantic: 0.60
      creative: 0.15
    known_blind_spots:
      - "relations 字段处理（402/414 反复出盲区）"
      - "YAML 解析边界（缩进走私）"

  strong_agent:
    alias: 好模型
    model_family: ds-v4.1-flash
    cost_per_1k_tok: 0.1      # 10×苦力
    speed: medium
    request_limit: 1000
    strengths:
      - 架构设计、范式突破
      - 新工具开发
      - 复杂 claim 改写
      - 跨文件重构
    weaknesses:
      - 成本高，不适合机械任务
      - 速度中等
    success_rate:
      mechanical: 0.95
      semantic: 0.90
      creative: 0.75

  adversarial_agent:
    alias: 对抗模型
    model_family: seed-evolving
    cost_per_1k_tok: 0.05
    speed: slow
    request_limit: 2000
    strengths:
      - 红队、对抗测试
      - 找漏洞、逃逸路径
      - 独立验证
    weaknesses:
      - 不适合生产
      - 速度慢
    independence_requirement: "必须与建设者不同模型族"

  architect_agent:
    alias: 架构师
    model_family: doubao
    cost_per_1k_tok: 0.08
    speed: medium
    request_limit: unlimited
    strengths:
      - 调研消化、架构规划
      - 代码级深度分析
      - 跨领域联系
    weaknesses:
      - 不直接改代码（只出方案）
```

### 2.2 模型族独立性

对抗模型必须与建设者不同模型族（373 纪律）：
- 同模型族共享盲区（368→373→402→452 都是同模型族，模式高度固化）
- 不同模型族的对抗更有信息量

---

## 三、任务路由

### 3.1 任务难度三级分类（484 的细化）

| 难度 | 定义 | 判定标准 | 路由 | 预期成本 |
|---|---|---|---|---|
| 机械 | 有明确规则、可机器验证 | 改字段、补测试、跑门禁、格式调整、文件整理 | 苦力 | 1× |
| 语义 | 需要理解但有验证器 | 写卡、改 claim、红队、写夹具、修 bug | 苦力→验证→不通过升级 | 1×→10× |
| 创造 | 无明确规则、需要架构判断 | 新工具、新范式、架构设计、新域首颗 | 直接好模型 | 10× |

### 3.2 路由决策树

```
任务来了
  │
  ├─ 有明确规则且可机器验证？→ 是 → 机械 → 苦力
  │
  ├─ 需要理解但有验证器？→ 是 → 语义
  │    ├─ 苦力做 → 门禁验证
  │    │    ├─ 通过 → 完成（成本 1×）
  │    │    └─ 失败 ≤2 次 → 苦力自己修
  │    │    └─ 失败 >2 次 → 升级好模型（成本 1×+10×）
  │
  └─ 无明确规则、需要架构判断？→ 创造 → 直接好模型
```

### 3.3 路由工具

`tools/model_router.py`（约 100 行）：
- 输入：任务描述
- 输出：建议模型、预估成本、预估成功率、升级条件
- 不自动路由，只给建议（人决定）
- 记录实际路由结果，用于能力回溯

### 3.4 路由优化

根据历史数据动态调整：
- 某类任务苦力成功率 >80% → 保持路由
- 某类任务苦力成功率 <50% → 建议直接升级
- 某类任务好模型也做不好 → 标记"高难度"，需要人介入

---

## 四、断点续跑（用户核心痛点）

### 4.1 问题

Agent 单次会话有请求上限（500 次），到顶后：
- 上下文丢失
- 必须人手动开新会话、重新描述任务
- 任务进度可能丢失

### 4.2 改法：任务状态持久化 + 自动续跑

#### 任务状态文件

每个任务有状态文件 `data/tasks/<task_id>.json`：

```json
{
  "task_id": "fix_472_p0",
  "type": "fix_gate",
  "description": "修复 472 批次 P0 问题",
  "status": "in_progress",
  "assigned_to": "cheap_agent",
  "created_at": "2026-09-14T10:00:00Z",
  "updated_at": "2026-09-14T10:30:00Z",
  "current_step": 3,
  "total_steps": 8,
  "steps_completed": ["分析问题", "写修复代码", "跑 pytest"],
  "steps_pending": ["跑 gate", "跑 replay", "写毒样例", "提交", "写报告"],
  "context_summary": "已修复 EV-FIXTURE-NO-ECHO-DATA，pytest 全绿，待跑 gate",
  "artifacts": ["tools/gate_engine.py", "tests/test_gate_engine.py"],
  "request_count": 480,
  "request_limit": 500
}
```

#### 续跑协议

1. Agent 每次操作后更新任务状态文件
2. 当 request_count 接近上限（>450）时，Agent 主动：
   - 更新状态文件（记录当前进度和上下文摘要）
   - 输出"续跑提示词"（包含任务状态文件路径和下一步）
3. 人开新会话，把续跑提示词喂给新 Agent
4. 新 Agent 读取任务状态文件，从断点继续

#### 自动续跑（远期）

如果有外部调度器（如 GitHub Actions、cron）：
- 检测到任务状态为 `needs_continue`
- 自动开新会话，喂续跑提示词
- 不需要人介入

### 4.3 工具：task_state.py（约 120 行）

```python
def create_task(task_type, description):
    """创建任务，返回 task_id"""

def update_progress(task_id, step, context_summary):
    """更新任务进度"""

def check_request_limit(task_id, current_count):
    """检查是否接近请求上限，返回续跑提示词"""
    if current_count > 450:
        return generate_continue_prompt(task_id)
    return None

def generate_continue_prompt(task_id):
    """生成续跑提示词"""
    task = load_task(task_id)
    return f"""
    你是续跑 Agent。任务 {task_id} 在上一个会话中执行到第 {task.current_step}/{task.total_steps} 步。
    
    已完成：{task.steps_completed}
    待完成：{task.steps_pending}
    当前进度：{task.context_summary}
    
    请从 {task.steps_pending[0]} 开始继续。任务状态文件：data/tasks/{task_id}.json
    每次操作后更新状态文件。接近 500 次请求时，主动输出续跑提示词。
    """

def load_task(task_id):
    """加载任务状态"""
```

### 4.4 上下文压缩

续跑时，新 Agent 不需要完整历史，只需要：
- 任务状态文件（进度+上下文摘要）
- 相关文件的当前状态（git diff）
- 下一步要做什么

上下文从"完整对话历史"压缩到"任务状态+当前 diff"，节省 80%+ token。

---

## 五、结果融合

### 5.1 问题

多个模型做同一任务（如红队对抗），结果可能不同。怎么对比和融合？

### 5.2 改法：多模型结果对比

```python
def compare_results(results):
    """对比多个模型的结果"""
    # 1. 一致性检查：多个模型都发现的问题 = 高置信
    # 2. 差异性分析：只有一个模型发现的问题 = 需验证
    # 3. 融合：合并所有发现，去重，按置信度排序
    return {
        'high_confidence': [f for f in findings if f.found_by >= 2],
        'needs_verification': [f for f in findings if f.found_by == 1],
        'model_disagreement': find_disagreements(findings),
    }
```

### 5.3 应用场景

- **红队对抗**：2-3 个不同模型族的对抗模型同时跑，结果融合
- **架构设计**：好模型出方案，对抗模型批判，融合后更完善
- **claim 审核**：多个模型独立审核 claim，一致性高的才通过

---

## 六、多 Agent 协作协议

### 6.1 三权分立（已有，正式化）

| 角色 | 职责 | 不能做 |
|---|---|---|
| Writer | 生产原子/卡/夹具 | 不能置 verified、不能改规则 |
| Redteam | 独立盲读、找问题 | 不能改卡、不能置 verified |
| Gatekeeper | 跑门禁、跑 replay | 不能改内容、不能置 verified |
| 人（监工） | 签署、裁决、push | — |

### 6.2 交付物切分

每个角色的交付物明确：
- Writer：草稿原子 + 证据卡 + 夹具 + 工件
- Redteam：红队报告（结构化格式，485）+ 毒样例候选
- Gatekeeper：门禁结果 + replay 结果
- 人：签署 + 裁决记录 + push

### 6.3 交接协议

角色之间的交接必须有明确的交接文档：
- Writer → Redteam：交付物清单 + 已知限制 + 建议重点
- Redteam → Gatekeeper：红队报告 + 修复建议
- Gatekeeper → 人：门禁结果 + 待裁决项

---

## 七、实施计划

### 第一阶段（零/低成本，立即做）

1. **模型能力档案**：写 `docs/kernel/model_marketplace.yaml`，录入 4 个模型
2. **任务状态文件**：`tools/task_state.py`，创建/更新/加载任务状态
3. **续跑提示词模板**：接近请求上限时自动生成续跑提示词
4. **路由规则文档**：`docs/kernel/routing_rules.md`，三级分类标准

### 第二阶段（中等成本，下一批做）

5. **model_router.py**：任务难度分类和路由建议
6. **结果融合工具**：多模型结果对比和融合
7. **多 Agent 交接协议**：正式化交接文档模板
8. **能力回溯**：记录每个模型的任务成功率，动态调整路由

### 第三阶段（高成本，需要外部调度器）

9. **自动续跑**：外部调度器检测到 needs_continue，自动开新会话
10. **自动路由**：根据任务难度自动选择模型（不需要人判断）
11. **多模型并行**：重要任务自动派 2-3 个模型，结果融合

---

## 八、预期效果

| 指标 | 当前 | 第一阶段后 | 第三阶段后 |
|---|---|---|---|
| 任务分配 | 靠人判断 | 路由建议 | 自动路由 |
| 断点续跑 | 人手动开新会话 | 状态文件+续跑提示词 | 自动续跑 |
| 上下文丢失 | 每次续跑丢失 | 状态文件保留 | 完整保留 |
| 模型能力数据 | 无 | 有档案 | 有回溯+动态调整 |
| 多模型结果 | 各自独立 | 可对比 | 自动融合 |
| 人介入频率 | 每次续跑都要人 | 只在升级/裁决时 | 几乎不需要 |

---

## 九、和现有系统的集成

- **487 任务队列**：任务状态文件是队列的扩展（队列管分配，状态管进度）
- **484 成本经济学**：路由建议考虑成本（苦力 1× vs 好模型 10×）
- **485 自进化**：模型成功率数据喂给路由优化
- **486 可观测性**：任务进度加入健康看板
- **488 权限模型**：多 Agent 协作的角色权限
- **红队提示词**：加模型族独立性要求

---

## 十、风险与缓解

| 风险 | 缓解 |
|---|---|
| 任务状态文件不同步 | 每次操作后立即更新；git 跟踪状态文件 |
| 续跑 Agent 理解偏差 | 续跑提示词包含完整上下文摘要+当前 diff+下一步 |
| 路由建议不准 | 先人工审核，积累数据后再自动 |
| 模型能力档案过时 | 每次任务后更新成功率，档案有版本号 |
| 自动续跑需要外部调度器 | 先做手动续跑（状态文件+提示词），自动续跑远期 |
| 多模型并行成本高 | 只在重要任务（红队对抗、架构设计）用并行 |
