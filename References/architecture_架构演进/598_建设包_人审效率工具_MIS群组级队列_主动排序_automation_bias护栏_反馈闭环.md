# 598 建设包：人审效率工具 —— MIS 群组级队列 + 主动排序 + automation bias 护栏 + 反馈闭环

> 你是苦力建设者，不是调研者。任务是把 595 异族调研已实证的人审效率方案落地为可运行的工具和界面，不是重新调研、不是探索新方向。
> 严格按本仓铁律：一任务一 commit + 正反毒样例 + 存量零误伤 + 新收紧 warn 起步 + 护栏不许裸 except Exception + 改 CORE 必须同 commit --update 带 .tool_checksums。
> 做不完停在任务边界，不留半成品。

---

## 前置依赖（必须先核实）

本包依赖 596 建设包的产出。开工前必须核实以下文件存在且可运行：

1. `tools/attack_edge_generator.py`——候选攻击边自动生成工具
2. `tools/weighted_af_solver.py`——W2 加权 AF 求解器
3. `tools/attack_edge_review.py`——人审确认接口（基础版，596 可能是边级，本包升级为 MIS 群组级）
4. `data/attack_edges_candidates.jsonl`——候选攻击边数据
5. `data/grounded_labels_w2.json`——W2 grounded 标注结果
6. `data/human_attack_edge_annotations.jsonl`——人审标注记录（可能为空）

**如果 596 未完成或上述文件缺失**：
- 任务 0 先记录缺失项
- 任务 1-3 中不依赖 596 的部分（automation bias 检测函数、主动排序算法、反馈闭环数据结构）可以先做
- 依赖 596 的部分（人审界面、W2 集成）停在任务边界，等 596 完成后再做
- 在偏差表如实记录哪些任务因依赖未完成而停摆

**如果 596 的 attack_edge_review.py 是边级（不是 MIS 群组级）**：
- 本包任务 1 将其升级为 MIS 群组级（保留边级接口作为兼容层，标记 deprecated）
- 在偏差表记录升级内容

---

## 背景（595 已实证，先核实再用）

595 异族调研（_arch_v14/）手搓实验核心结论：

1. **MIS 群组级人审降 4.6 倍**：边级 194 次确认 = 1.89 小时；MIS 群组级 42 次确认 = 24.5 分钟。根因：191/194 边命题早已验证（cred≥0.8），瓶颈是"误解到底驳斥卡上哪条命题"（目标歧义），不是"是否相信攻击成立"。
2. **automation bias 可机器检测**：rubber-stamp 评审 agree_rate=1.0、10 陷阱题 0 捕获；careful 0.936、10/10 捕获。检测规则：agree_rate==1.0 且理由过短 → 触发复核。
3. **主动学习式排序**：按歧义度降序（歧义度 = 该 MIS 关联的候选边数 × 目标命题数 × 证据冲突度），先审高歧义的。
4. **人审质量控制**：自一致性（同人审两次结果一致率）+ W2 机器辅助复核（人审结果与 W2 预测不一致时标记）+ 理由质量评估（理由长度/关键词/具体命题引用）。
5. **可视化原型**：_arch_v14/visualization/index.html（SVG 圆形布局，可参考）。

595 探针代码在 `_arch_v14/probes/human_review_v14_probe.py`（只读，可参考实现，但不要直接复制——要按本仓工具规范重写）。

**你的任务是把 595 的手搓方案升级为本仓正式工具和界面**，让人审从"CLI 逐条操作"变成"批量队列 + 机器预标注 + 自动化护栏 + 反馈闭环"。

---

## 任务 0：开工先量（无 commit）

实跑以下基线，记录数字：
1. `gate_engine.py --check` → 规则数 / 命中数 / block/warn/advice
2. `poison_drill.py` → 通过数 / RULE-COVERAGE / 表观/诚实覆盖率
3. `atom_evidence_replay.py --check` → confirm/refute/infra
4. `tool_integrity.py --check` → exit 0
5. `attack_edge_generator.py stats`（如果 596 已完成）→ 候选边数 / 按 MIS 分布 / 按可信度分布
6. `weighted_af_solver.py stats`（如果 596 已完成）→ IN/OUT/UNDEC 分布
7. `attack_edge_review.py stats`（如果 596 已完成）→ 人审进度（待审/已确认/已拒绝）
8. 手动统计：MIS 数量 / 带 related_atoms 的 MIS 数 / 每个 MIS 平均关联候选边数 / 每张卡平均命题数

**关键核实**：595 说 42 个 MIS 带 related_atoms、194 条候选边、每个 MIS 平均 4.6 条边。你必须独立复算，不能直接抄 595 的结论。

---

## 任务 1：人审接口升级为 MIS 群组级（commit 1）

升级 `tools/attack_edge_review.py`（596 基础版）为 MIS 群组级：

### 新增命令

- `python tools/attack_edge_review.py queue` → 列出 MIS 群组级待审队列（按歧义度降序），每个 MIS 显示：
  - `mis_id`: MIS 编号
  - `candidate_count`: 关联的候选边数
  - `target_propositions`: 目标命题列表（卡id::prop-N）
  - `ambiguity_score`: 歧义度（见下）
  - `review_status`: 未审/已确认/已拒绝/部分确认
  - `w2_prediction`: W2 机器预测（该 MIS 下所有边的预期标注）
- `python tools/attack_edge_review.py review <mis_id>` → 进入 MIS 群组级人审交互：
  1. 展示该 MIS 的完整信息（brief / refutations 全文 / related_atoms / misconceptions）
  2. 展示该 MIS 关联的所有候选边（列表：edge_id / target 命题 / evidence 摘要 / 当前可信度）
  3. 展示目标命题列表（每张卡的 claim_structured，供人审判断"误解驳斥哪条命题"）
  4. 展示 W2 机器预测（如果不做任何修改，W2 会给这些边什么标注）
  5. 人审做一次"目标映射"判断：这个 MIS 驳斥卡上哪条命题？（输入命题 id 或 "none"）
  6. 自动批量确认该 MIS 下所有目标匹配的边（approve），目标不匹配的边标记为 reject
  7. 记录 review_seconds / reason_len / reviewer（git 作者）/ timestamp
- `python tools/attack_edge_review.py review-all` → 批量人审（逐个 MIS 展示，人审逐个确认，支持 `q` 退出、`s` 跳过当前、`b` 回到上一个）
- `python tools/attack_edge_review.py stats` → 人审统计（待审/已确认/已拒绝/部分确认 / 通过率 / 平均 review_seconds / 平均 reason_len / automation bias 触发次数）

### 歧义度计算（主动学习式排序）

```
ambiguity_score(mis) = candidate_count × target_proposition_count × evidence_conflict
```

- `candidate_count`: 该 MIS 关联的候选边数
- `target_proposition_count`: 这些边的目标命题去重数
- `evidence_conflict`: 证据冲突度（0-1），该 MIS 的 refutations 与目标命题的 evidence_refs 是否有冲突（简单实现：refutations 中是否包含目标命题的 artifact_assert 符号，包含则 1.0，否则 0.5）
- 按 ambiguity_score 降序排列，先审高歧义的

### 保留边级兼容接口（标记 deprecated）

- `approve <edge_id>` / `reject <edge_id>` / `modify <edge_id>` 保留，但输出警告 "deprecated: use review <mis_id> for MIS-group review"
- 边级操作仍然写入 human_attack_edge_annotations.jsonl（格式不变）

### 纪律
- 人审必须过 git 作者绑定（与 596 同款）
- 理由必填（缺 --reason 或交互时空输入 → 拒绝写入）
- fail-closed（git 不可用 / MIS 不存在 / 目标命题不存在 → 拒绝写入）
- 不自动产生人审标注（系统绝不自动 approve/reject）
- 人审标注只追加不覆盖（历史可追溯）

### 测试（tests/test_attack_edge_review_mis_group_598.py）
- 正例：review 一个 MIS，输入目标命题 id → 该 MIS 下所有匹配边被 approve，不匹配的被 reject
- 正例：queue 按歧义度降序排列
- 反例 1：review 不存在的 mis_id → 拒绝写入
- 反例 2：目标命题 id 不存在 → 拒绝写入
- 反例 3：理由为空 → 拒绝写入
- 反例 4：git 作者不匹配 → 拒绝写入（用 monkeypatch 模拟）
- 兼容层：边级 approve/reject 仍然可用，但输出 deprecated 警告
- 幂等：review 同一个 MIS 两次 → 追加两条记录（不覆盖）
- stats：人审后统计数字正确

---

## 任务 2：automation bias 护栏（commit 2）

在 `tools/attack_edge_review.py` 中内置 automation bias 检测：

### 检测规则（595 已实证）

1. **agree_rate 检测**：一个人审会话（连续 review 多个 MIS）中，如果 agree_rate == 1.0（全部确认，无拒绝/跳过）→ 标记为"疑似 rubber-stamp"
2. **理由过短检测**：单条人审记录的 reason_len < 阈值（默认 10 个字符，可配置）→ 标记为"理由过短"
3. **速度过快检测**：单条人审记录的 review_seconds < 阈值（默认 5 秒，可配置）→ 标记为"速度过快"
4. **组合触发**：agree_rate == 1.0 且（理由过短比例 > 50% 或 速度过快比例 > 50%）→ **触发复核**（该会话的所有人审记录标记为 "needs_review"，输出警告）

### 新增命令

- `python tools/attack_edge_review.py audit` → automation bias 审计：
  - 扫描所有人审记录（human_attack_edge_annotations.jsonl）
  - 按会话分组（按 timestamp 连续，间隔 > 30 分钟算新会话）
  - 计算每个会话的 agree_rate / 平均 reason_len / 平均 review_seconds
  - 标记疑似 rubber-stamp 的会话（agree_rate == 1.0 且理由过短或速度过快）
  - 输出审计报告（会话数 / 疑似 rubber-stamp 数 / 触发复核的记录数 / 建议复核的 MIS 列表）
- `python tools/attack_edge_review.py audit --json` → JSON 格式输出（供可视化使用）

### 陷阱题机制（可证伪性）

- 在候选攻击边中预埋"陷阱题"（已知应该被拒绝的边，如 MIS 与目标命题完全无关的边）
- 陷阱题比例：默认 5%（可配置），预埋时标记 `is_trap: true`（不在 queue 中展示，人审不知道哪些是陷阱）
- 如果人审确认了陷阱题 → 记录为 "trap_caught"，automation bias 审计时统计陷阱题捕获率
- 595 实证：rubber-stamp 0/10 捕获，careful 10/10 捕获 → 陷阱题捕获率是 automation bias 的有效指标

**陷阱题生成规则**（纯标准库，不修改正式候选边）：
- 从候选边中随机选 5%，将 target 命题改为一个与该 MIS 无关的命题（从其他卡随机选）
- 陷阱题写入独立文件 `data/attack_edges_traps.jsonl`（不混入 candidates，避免污染数据）
- 人审时 queue 命令混合展示真实边和陷阱边（人审不知道哪些是陷阱）
- 人审结果与陷阱题标注比对 → 计算捕获率

### 纪律
- automation bias 检测是"提示"不是"否决"——标记为 needs_review 的记录仍然有效，只是建议复核
- 陷阱题不污染正式数据（独立文件，不混入 candidates）
- 陷阱题比例可配置（默认 5%，人审者可以选择关闭陷阱题，但关闭时 audit 会标记 "traps_disabled"）
- 不许裸 except Exception（检测函数的异常必须冒出来，不能静默通过）

### 测试（tests/test_automation_bias_598.py）
- 正例：agree_rate == 1.0 且理由过短 → 触发复核
- 正例：careful 评审（agree_rate < 1.0 且理由充分）→ 不触发复核
- 反例：agree_rate < 1.0（有拒绝）→ 不触发复核（即使理由过短）
- 反例：理由充分但 agree_rate == 1.0 → 不触发复核（只标记"全同意"，不触发复核）
- 陷阱题：预埋 5% 陷阱题，人审全部确认 → 捕获率 0%，audit 标记 "low_trap_capture"
- 陷阱题：人审全部拒绝陷阱题 → 捕获率 100%，audit 通过
- audit：扫描人审记录，按会话分组，输出审计报告
- 可证伪性：有一条测试专门验证"护栏不许裸 except Exception"（注入 NameError，必须抛出不能静默）

---

## 任务 3：人审反馈闭环（commit 3）

实现人审反馈闭环：人审拒绝 → 反馈给攻击边生成器和 W2 权重 → 下一轮候选边质量上升。

### 反馈机制

1. **人审拒绝 → 攻击边生成器反馈**：
   - 如果一个 MIS 下的所有边都被拒绝（人审判断该 MIS 不驳斥任何命题）→ 记录该 MIS 为 "low_quality_source"
   - 下一轮 attack_edge_generator 生成候选边时，降低 "low_quality_source" MIS 的权重（或跳过）
   - 反馈文件：`data/attack_edge_feedback.jsonl`（只追加，记录 MIS id / 反馈类型 / 反馈原因 / timestamp）
2. **人审确认 → W2 权重反馈**：
   - 如果人审确认了一条边 → 该边的可信度升级（low→medium, medium→high）
   - 如果人审拒绝了一条边 → 该边的可信度降级（high→medium, medium→low, low→drop）
   - 人审修改可信度 → 直接使用人审指定的可信度
   - 权重反馈写入 `data/attack_edge_weights.jsonl`（只追加，记录 edge_id / 旧权重 / 新权重 / 反馈原因 / timestamp）
3. **W2 求解器集成反馈**：
   - `weighted_af_solver.py solve` 增加 `--include-human-feedback` 开关（默认开启）
   - 开启时，使用人审反馈后的权重（从 attack_edge_weights.jsonl 读取最新权重）
   - 关闭时，使用原始候选边的权重
   - 输出中增加 `human_feedback_applied: true/false` 和 `weights_updated: N`（N 条边的权重被人审反馈更新）

### 新增命令

- `python tools/attack_edge_review.py feedback` → 查看人审反馈统计：
  - 被标记为 "low_quality_source" 的 MIS 数
  - 权重被升级的边数 / 被降级的边数
  - 下一轮候选边预计减少数（跳过 low_quality_source 的 MIS）
- `python tools/attack_edge_generator.py generate --include-feedback` → 生成候选边时应用人审反馈（跳过 low_quality_source 的 MIS，使用人审更新后的权重）
- `python tools/weighted_af_solver.py solve --include-human-feedback` → W2 求解时应用人审反馈后的权重

### 飞轮效应（自我减负）

人审反馈闭环的目标是"人审越标越少"：
- 第一轮：194 条候选边，42 个 MIS 群组，人审 24.5 分钟
- 第二轮：应用反馈后，low_quality_source 的 MIS 被跳过，候选边可能降到 150 条，35 个 MIS 群组，人审 20 分钟
- 第三轮：继续反馈，候选边可能降到 120 条，30 个 MIS 群组，人审 17 分钟
- ...

**飞轮效应的验证**：连续生成 3 轮候选边（每轮应用上一轮的反馈），统计候选边数和 MIS 群组数是否逐轮下降。

### 纪律
- 反馈只追加不覆盖（历史可追溯）
- 人审反馈是"建议"不是"强制"——attack_edge_generator 可以选择 `--no-feedback` 忽略反馈（用于对比实验）
- W2 求解器的 `--include-human-feedback` 默认开启，但可以关闭（用于对比实验）
- 不许自动产生反馈（系统绝不自动标记 low_quality_source 或自动更新权重，必须有人审记录作为依据）
- 反馈文件入库（data/attack_edge_feedback.jsonl / data/attack_edge_weights.jsonl）

### 测试（tests/test_human_feedback_loop_598.py）
- 正例：人审拒绝一个 MIS 的所有边 → 该 MIS 被标记为 low_quality_source
- 正例：人审确认一条边 → 该边权重升级（low→medium）
- 正例：人审拒绝一条边 → 该边权重降级（medium→low）
- 正例：下一轮 generate --include-feedback → 跳过 low_quality_source 的 MIS，候选边数减少
- 正例：W2 solve --include-human-feedback → 使用人审更新后的权重，结果与不使用反馈不同
- 反例：没有人审记录 → 不产生反馈（low_quality_source 为空，权重不变）
- 反例：generate --no-feedback → 不应用反馈，候选边数与原始一致
- 飞轮效应：连续 3 轮 generate --include-feedback，候选边数逐轮下降（用沙箱数据验证）
- 可证伪性：反馈函数不许裸 except Exception

---

## 任务 4：人审数据可视化（commit 4）

生成人审数据的 HTML 可视化页面（纯标准库生成自包含 HTML，无外部依赖，参考 _arch_v14/visualization/index.html）：

### 页面内容

1. **人审进度总览**：
   - 候选边总数 / 已确认 / 已拒绝 / 待审 / 部分确认
   - MIS 群组总数 / 已审 / 待审
   - 通过率 / 拒绝率 / 平均 review_seconds / 平均 reason_len
2. **automation bias 监控**：
   - 会话数 / 疑似 rubber-stamp 会话数
   - 陷阱题捕获率（折线图，按会话）
   - 触发复核的记录数 / 建议复核的 MIS 列表
3. **反馈闭环监控**：
   - low_quality_source MIS 数
   - 权重升级/降级边数
   - 候选边数逐轮变化（折线图，展示飞轮效应）
4. **论证图（可复用 595 原型）**：
   - SVG 圆形布局，内圈 MIS/OUT 红、外圈命题/IN 绿
   - 攻击边颜色按人审状态（已确认=绿、已拒绝=灰、待审=红、陷阱题=虚线）
   - 点击节点展示详情（MIS brief / 命题 claim_text / 人审记录）

### 生成命令

- `python tools/attack_edge_review.py dashboard` → 生成 HTML 可视化页面到 `data/human_review_dashboard.html`
- `python tools/attack_edge_review.py dashboard --output <path>` → 指定输出路径

### 纪律
- 纯标准库生成（不装 d3/echarts/chart.js，用内联 SVG + vanilla JS）
- 自包含 HTML（所有数据内联，无外部依赖，可直接用浏览器打开）
- 页面是派生数据，入库（data/human_review_dashboard.html）
- 不修改任何正式文件（只读取人审记录和候选边数据）

### 测试（tests/test_human_review_dashboard_598.py）
- 正例：dashboard 命令生成 HTML 文件，文件非空，包含关键 section（进度总览 / automation bias / 反馈闭环 / 论证图）
- 正例：HTML 是自包含的（无外部 src/href 引用）
- 反例：没有人审数据 → dashboard 仍然生成（显示"暂无数据"），不崩溃
- 幂等：连续生成两次，HTML 逐字一致（除时间戳外）

---

## 任务 5：收工总验收（无 commit，纯验收）

按以下清单逐项验收，全部用退出码定论（$LASTEXITCODE）：

1. `tool_integrity.py --check` → exit 0（本批未改 CORE，无需重钉；但如果改了 conftest.py 则需要 --check-test-config）
2. `gate_engine.py --check` → exit 0，规则数/命中数/block/warn/advice 与任务 0 基线逐字相同
3. `poison_drill.py` → exit 0，通过数/RULE-COVERAGE/表观/诚实覆盖率与基线逐字相同
4. `atom_evidence_replay.py --check` → exit 0，confirm/refute/infra 与基线逐字相同
5. `attack_edge_review.py queue` → exit 0，输出 MIS 群组级队列（按歧义度降序）
6. `attack_edge_review.py stats` → exit 0，输出人审统计
7. `attack_edge_review.py audit` → exit 0，输出 automation bias 审计报告
8. `attack_edge_review.py feedback` → exit 0，输出反馈统计
9. `attack_edge_review.py dashboard` → exit 0，生成 HTML 可视化页面
10. `attack_edge_generator.py generate --include-feedback` → exit 0（如果 596 已完成），应用反馈后候选边数减少
11. `weighted_af_solver.py solve --include-human-feedback` → exit 0（如果 596 已完成），应用反馈后权重更新
12. `pytest -m "not slow" -n auto` → exit 0（含本批新增测试）
13. `pytest -m slow -n0` → exit 1，唯一红 = test_golden_lock_json（预期红）
14. `ruff check`（本批全部新增/改动 .py）→ All checks passed
15. `git diff --quiet -- atoms evidence Examples Book` → exit 0（受控目录零污染）
16. `git status --short` → 仅本批文件（+ 两条 CRLF 假脏）

---

## 明确不做（任务书边界）

- 不修改 `gate_engine.py` / `atom_evidence_replay.py` / `poison_drill.py` / `toolchain.py` / `cppbible.py`（CORE 五文件不动）
- 不修改 `weighted_af_solver.py` 的核心求解逻辑（只增加 `--include-human-feedback` 开关，不动 W2 模型本身）
- 不修改 `attack_edge_generator.py` 的核心生成逻辑（只增加 `--include-feedback` 开关，不动生成规则）
- 不做 LLM 辅助人审（LLM-as-judge 冻结）
- 不做多人协作（单用户阶段）
- 不做 Web 服务（dashboard 是静态 HTML，不是 Web 应用）
- 不 push / 不 golden accept / 不替人签

---

## 偏差表模板（写进 _worklog_598.md §6）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 596 已完成，所有依赖文件存在 | （实跑结果） | 如缺失，停在任务边界 |
| D2 | 595 说 42 MIS / 194 边 / 平均 4.6 边/MIS | （实跑结果） | 以实跑为准 |
| D3 | automation bias 阈值（reason_len < 10 / review_seconds < 5） | （实测合理值） | 按实测调整 |
| D4 | 陷阱题比例 5% | （实测效果） | 按实测调整 |
| ... | ... | ... | ... |

---

## 过程文档

- `_worklog_598.md`：按惯例不入库，含任务 0 基线 / 各任务实跑数字 / §6 偏差表 / §7 收工验收 / 交人项
- 每个任务一个 commit，message 里写明任务编号和一句话结果
- 改了 CORE 或 conftest.py 必须同 commit --update 带 .tool_checksums
