# 596 建设包：攻击关系数据地基 + W2 加权 AF 落地 —— grounded 论证层从"退化"变"可用"

> 你是苦力建设者，不是调研者。任务是把 594 异族调研已实证的 W2 模型落地为可运行的工具和数据，不是重新调研、不是探索新方向。
> 严格按本仓铁律：一任务一 commit + 正反毒样例 + 存量零误伤 + 新收紧 warn 起步 + 护栏不许裸 except Exception + 改 CORE 必须同 commit --update 带 .tool_checksums。
> 做不完停在任务边界，不留半成品。

---

## 背景（593+594 已实证，先核实再用）

593 异族调研（_arch_v12/）手搓 grounded 求解器，在本仓 79 命题图上实测：三种自然攻击构造全部退化（零攻击全接受 / 单向语义倒置 / 对称全不确定），瓶颈是缺可信加权攻击边而非算法。

594 异族调研（_arch_v13/）找到唯一能解除退化的模型 **W2**，并手搓验证：
- **候选攻击边自动生成**：以 MIS 误解库 `related_atoms`/`misconceptions` 关联为种子，纯标准库生成 194 条单向候选边（MIS→命题方向），零 Oracle 风险
- **W2 模型**：可信度加权击败 + 命题反向反驳误解（对称边）→ IN=79（命题全 IN）/ OUT=42（误解全 OUT）/ UNDEC=0，非退化且语义正确
- **W1 阈值加权彻底失败**：语义倒置在 θ=0→1.0 全程持续
- **可靠权重来源**：不是从文本挖（否定词密度中位数 0），而是本仓既有可信度字段（`verified_by` / `machine_verified`）
- **反例验证**：移除 MIS-CONC-001 攻击 → OUT 的 MIS 42→41，判决翻转=是，攻击边"可后果"

594 探针代码在 `_arch_v13/probes/grounded_v13_probe.py`（只读，可参考实现，但不要直接复制——要按本仓工具规范重写为可维护、有测试、有 CLI 的正式工具）。

**你的任务是把 594 的手搓探针升级为本仓正式工具和数据**，让 grounded 论证层从"调研概念"变成"可运行、可验证、可人审"的正式功能。

---

## 任务 0：开工先量（无 commit）

实跑以下基线，记录数字，作为后续任务的对账基准：
1. `gate_engine.py --check` → 规则数 / 命中数 / block/warn/advice
2. `poison_drill.py` → 通过数 / RULE-COVERAGE / 表观/诚实覆盖率
3. `atom_evidence_replay.py --check` → confirm/refute/infra
4. `tool_integrity.py --check` → exit 0
5. `prop_graph.py stats` → 命题数 / 卡数 / 类型分布 / 签署状态
6. 手动统计：MIS 误解库文件数 / 带 `related_atoms` 的 MIS 数 / `related_atoms` 关联的原子卡数 / 命题数
7. 手动统计：命题卡面 `verified_by` 字段填写情况 / `machine_verified` 字段情况（如果有）

**关键核实**：594 说 42 个 MIS 带 `related_atoms`、生成 194 条候选边。你必须独立复算这个数字，不能直接抄 594 的结论。如果数字不一致，以你的实跑为准并在偏差表说明。

---

## 任务 1：候选攻击边自动生成工具（commit 1）

新建 `tools/attack_edge_generator.py`：

### 功能
- 输入：MIS 误解库目录（默认 `misconceptions/`）+ 原子卡目录（默认 `atoms/`）+ 命题来源（默认从原子卡 `claim_structured` 读取）
- 输出：候选攻击边列表，每条边包含：
  - `id`: 唯一标识（如 `ae-MIS-CONC-001->prop-3`）
  - `source`: 攻击源（MIS id）
  - `target`: 被攻击目标（命题 id，格式 `卡id::prop-N`）
  - `kind`: 攻击类型（`misconception_refutation` / `related_atom` / `misconception`）
  - `evidence`: 证据（MIS 的 `refutations` 文本片段，取前 200 字）
  - `confidence`: 初始可信度（来自 MIS 卡面字段，如 `verified_by` 存在则高，否则中；具体分级见下）
  - `direction`: `mis_to_prop`（MIS 攻击命题）或 `prop_to_mis`（命题反驳 MIS，对称边用）
  - `generated_at`: 生成时间（ISO 格式）
  - `generator_version`: 工具版本（如 `1.0`）

### 生成规则（严格按 594 实证）
1. 遍历所有 MIS 文件，读取 `related_atoms` 和 `misconceptions` 字段
2. 对每个 `related_atoms` 中的原子卡 id，找到该卡的所有命题（`claim_structured`）
3. 对每个命题，生成一条 `mis_to_prop` 候选攻击边（MIS 攻击命题）
4. 同时生成一条 `prop_to_mis` 对称边（命题反驳 MIS）——这是 W2 模型的关键，594 实证没有对称边就会退化
5. 可信度分级：
   - `high`: MIS 卡面有 `verified_by` 字段且非空（人审过）
   - `medium`: MIS 卡面有 `machine_verified: true` 或等效字段
   - `low`: 无任何可信度字段（默认）
6. 去重：同一 (source, target, kind) 只保留一条（取可信度最高的）

### CLI
- `python tools/attack_edge_generator.py generate` → 生成候选攻击边，输出到 `data/attack_edges_candidates.jsonl`（覆盖写，因为是派生数据）
- `python tools/attack_edge_generator.py stats` → 统计：总边数 / 按 kind 分布 / 按 confidence 分布 / 按 source MIS 分布 / 按 target 命题分布
- `python tools/attack_edge_generator.py --check` → 校验：生成的边数与独立复算一致 / 每条边字段完整 / source MIS 存在 / target 命题存在 / 无重复边

### 纪律
- 纯只读生成（不修改 MIS/原子卡/命题）
- 纯标准库（不装 scipy/numpy/networkx）
- 幂等（同输入同输出）
- 不写入卡面（候选边是独立数据文件，不是卡面字段）
- 生成的 `data/attack_edges_candidates.jsonl` 入库（派生数据，但需要版本控制以便对账）

### 测试（tests/test_attack_edge_generator_596.py）
- 正例：用沙箱 MIS + 原子卡生成候选边，断言边数 / 字段 / 可信度分级
- 反例 1：MIS 无 `related_atoms` → 不生成边
- 反例 2：`related_atoms` 指向不存在的原子卡 → 跳过并告警（不崩溃）
- 反例 3：重复 `related_atoms` → 去重后只一条
- 幂等：连续生成两次，输出逐字一致
- `--check`：生成后校验通过

---

## 任务 2：W2 加权 AF 求解器（commit 2）

新建 `tools/weighted_af_solver.py`：

### 功能
- 输入：命题列表（默认从 `prop_graph.py` 读取 79 命题）+ 攻击边列表（默认从 `data/attack_edges_candidates.jsonl` 读取）
- 输出：grounded 标注结果，每个命题/误解节点：
  - `id`: 节点 id
  - `type`: `proposition` 或 `misconception`
  - `label`: `IN` / `OUT` / `UNDEC`
  - `defenders`: 为它辩护的节点列表（IN 且攻击它的攻击者都被 OUT）
  - `attackers`: 攻击它的节点列表
  - `defeated_attackers`: 被它击败的攻击者列表（W2 模型的"可信度加权击败"）

### W2 模型实现（严格按 594 实证）
1. **可信度加权击败**：一个攻击边 A→B 能击败 B，当且仅当：
   - A 的可信度 > B 的可信度（严格大于，不是 ≥）
   - 且 A 是 IN（被接受）
   - 可信度取值：`high=3` / `medium=2` / `low=1` / 无字段=1（与 low 同级）
2. **对称边**：命题反驳 MIS 的边（`prop_to_mis`）必须存在——594 实证没有对称边就会退化（S1 语义倒置）
3. **grounded 不动点迭代**：
   - 初始：所有节点 UNDEC
   - 迭代：节点被标 IN 当且仅当所有攻击它的节点都被标 OUT；节点被标 OUT 当且仅当存在一个攻击它的 IN 节点且该攻击边满足"可信度加权击败"
   - 重复直到不动点（最多 100 轮，超过则报错）
4. **与 594 实证对账**：用任务 1 生成的 194 条候选边 + 79 命题 + 42 MIS，跑 W2 求解器，断言结果为 IN=79（命题全 IN）/ OUT=42（误解全 OUT）/ UNDEC=0。如果数字不一致，以你的实跑为准并在偏差表说明。

### CLI
- `python tools/weighted_af_solver.py solve` → 跑 W2 求解，输出到 `data/grounded_labels_w2.json`（覆盖写）
- `python tools/weighted_af_solver.py stats` → 统计：IN/OUT/UNDEC 分布 / 按节点类型分布 / 平均辩护者数 / 平均攻击者数
- `python tools/weighted_af_solver.py --check` → 校验：与 594 实证对账（IN=79/OUT=42/UNDEC=0）/ 不动点收敛 / 所有节点有标注

### 与现有工具的关系
- 不修改 `prop_graph.py`（它是命题状态图，W2 求解器是独立工具）
- 不修改 `gate_engine.py` / `atom_evidence_replay.py` / `poison_drill.py`（CORE 五文件不动）
- 可以 import `prop_graph.py` 的命题读取函数（如果有），但不要依赖它的内部状态
- 如果 `prop_graph.py` 没有合适的命题读取函数，在 W2 求解器里自己实现（纯标准库读原子卡）

### 纪律
- 纯只读求解（不修改命题/攻击边/卡面）
- 纯标准库
- 幂等
- 不动点迭代必须有最大轮数保护（防止无限循环）
- `data/grounded_labels_w2.json` 入库

### 测试（tests/test_weighted_af_solver_596.py）
- 正例：用沙箱命题 + 攻击边跑 W2，断言 IN/OUT/UNDEC 分布
- 反例 1：无对称边（只有 mis_to_prop）→ 退化（语义倒置，与 594 S1 一致）
- 反例 2：W1 阈值加权（用阈值代替可信度加权击败）→ 退化（与 594 W1 失败一致）
- 反例 3：可信度相等（A 和 B 可信度相同）→ A 不能击败 B（严格大于）
- 不动点：迭代收敛（轮数 < 100）
- 与 594 实证对账：用真实数据跑，断言 IN=79/OUT=42/UNDEC=0（如果实跑数字不同，以实跑为准并在测试里用实跑数字）
- `--check`：求解后校验通过

---

## 任务 3：grounded 标注实测与对照（commit 3）

### 功能
用任务 2 的 W2 求解器对真实 79 命题 + 42 MIS 跑 grounded 标注，生成对照报告：

1. **grounded 标注结果**：`data/grounded_labels_w2.json`（任务 2 已生成）
2. **与现有判决对照**：
   - 命题的 grounded label（IN/OUT/UNDEC）vs 命题的 `claim_type`（observation/inference）
   - 命题的 grounded label vs 该命题引用卡的 replay verdict（confirm/refute）
   - MIS 的 grounded label（应该全 OUT）vs MIS 的 `refutations` 数量
3. **辩护链展示**：对每个 IN 命题，展示它的辩护链（哪些 MIS 攻击它、这些 MIS 为什么被 OUT、哪些命题反驳了这些 MIS）
4. **异常检测**：
   - 有没有命题被标 OUT？（理论上 W2 模型下命题全 IN，如果有 OUT 说明数据有问题）
   - 有没有 MIS 被标 IN？（理论上 MIS 全 OUT，如果有 IN 说明数据有问题）
   - 有没有 UNDEC？（理论上 W2 模型下 UNDEC=0，如果有 UNDEC 说明攻击边不完整）

### 产出
- `data/grounded_audit_report.md`：对照报告（Markdown 格式，含表格）
  - §1 grounded 标注总览（IN/OUT/UNDEC 分布）
  - §2 与 claim_type 对照（observation/inference 各多少 IN/OUT/UNDEC）
  - §3 与 replay verdict 对照（confirm/refute 各多少 IN/OUT）
  - §4 辩护链示例（选 3 个命题展示完整辩护链）
  - §5 异常检测（OUT 命题 / IN MIS / UNDEC 节点清单）
  - §6 与 594 实证对账（数字是否一致，不一致说明原因）

### 纪律
- 纯只读（不修改任何数据）
- 报告是派生数据，入库
- 异常检测必须 fail-loud（如果有 OUT 命题或 IN MIS，在报告里明确标红，不要静默忽略）

### 测试（tests/test_grounded_audit_596.py）
- 正例：用真实数据跑审计，断言报告生成成功 / 包含所有章节
- 反例：如果 grounded 标注有异常（OUT 命题/IN MIS/UNDEC），审计报告必须包含异常清单（不能静默通过）
- 幂等：连续生成两次，报告逐字一致（除时间戳外）

---

## 任务 4：人审确认接口（最小版本）（commit 4）

### 功能
新建 `tools/attack_edge_review.py`，提供候选攻击边的人审确认 CLI：

- `python tools/attack_edge_review.py list` → 列出所有待审候选攻击边（id / source / target / kind / confidence / 证据摘要 / 人审状态）
- `python tools/attack_edge_review.py list --status pending` → 只列待审的
- `python tools/attack_edge_review.py show <edge_id>` → 展示一条候选边的完整信息（证据全文 / 关联命题 / 关联 MIS）
- `python tools/attack_edge_review.py approve <edge_id> --reason "<理由>"` → 人审确认一条攻击边
- `python tools/attack_edge_review.py reject <edge_id> --reason "<理由>"` → 人审拒绝一条攻击边
- `python tools/attack_edge_review.py modify <edge_id> --confidence high|medium|low --reason "<理由>"` → 人审修改攻击边的可信度
- `python tools/attack_edge_review.py stats` → 人审进度统计（待审/已确认/已拒绝/已修改 / 通过率 / 拒绝率）

### 人审标注数据
- `data/human_attack_edge_annotations.jsonl`：人审标注记录（只追加，不覆盖）
  - 每条记录：`edge_id` / `action`（approve/reject/modify）/ `reason` / `reviewer`（git 作者名，从 `git config user.name` 读取）/ `timestamp` / `new_confidence`（modify 时）
- fail-closed：
  - 人审必须过 git 作者绑定（reviewer 必须与该文件最后一次 git 提交作者一致，与 573 overturned 通道同款）
  - 缺 `--reason` → 拒绝写入（理由必填，防止 rubber-stamp）
  - edge_id 不存在 → 拒绝写入
  - git 不可用 → 拒绝写入
- 不自动产生人审标注（系统绝不自动 approve/reject）

### 与 W2 求解器的关系
- 人审确认的攻击边 → 可信度升级（approve 时 confidence 升一级：low→medium, medium→high）
- 人审拒绝的攻击边 → 从 W2 求解器的输入中排除（不参与 grounded 标注）
- 人审修改可信度 → 直接使用人审指定的可信度
- W2 求解器的 `solve` 命令增加 `--include-human-reviewed` 开关（默认开启，使用人审标注后的攻击边；关闭则只用原始候选边）

### 纪律
- 人审标注只追加不覆盖（历史可追溯）
- fail-closed（git 作者绑定 / 理由必填 / edge_id 校验）
- 不自动产生标注
- `data/human_attack_edge_annotations.jsonl` 入库（初始为空文件）

### 测试（tests/test_attack_edge_review_596.py）
- 正例：approve 一条边 → 标注文件追加一条记录 / stats 显示已确认
- 反例 1：缺 --reason → 拒绝写入
- 反例 2：edge_id 不存在 → 拒绝写入
- 反例 3：git 作者不匹配 → 拒绝写入（用 monkeypatch 模拟）
- 幂等：approve 同一条边两次 → 追加两条记录（不覆盖，历史可追溯）
- W2 集成：人审拒绝一条边后，W2 求解器 `--include-human-reviewed` 不使用该边
- `--check`：标注文件格式校验通过

---

## 任务 5：收工总验收（无 commit，纯验收）

按以下清单逐项验收，全部用退出码定论（$LASTEXITCODE），不拿"没看到 failed"当绿：

1. `tool_integrity.py --check` → exit 0（本批未改 CORE，无需重钉；但如果改了 conftest.py 则需要 --check-test-config）
2. `tool_integrity.py --check-test-config` → exit 0（如果改了 conftest.py）
3. `gate_engine.py --check` → exit 0，规则数/命中数/block/warn/advice 与任务 0 基线逐字相同（存量零误伤）
4. `poison_drill.py` → exit 0，通过数/RULE-COVERAGE/表观/诚实覆盖率与基线逐字相同
5. `atom_evidence_replay.py --check` → exit 0，confirm/refute/infra 与基线逐字相同
6. `attack_edge_generator.py generate` → exit 0，生成候选边
7. `attack_edge_generator.py --check` → exit 0
8. `attack_edge_generator.py stats` → 输出统计（边数/按 kind/按 confidence）
9. `weighted_af_solver.py solve` → exit 0，生成 grounded 标注
10. `weighted_af_solver.py --check` → exit 0（与 594 实证对账）
11. `weighted_af_solver.py stats` → 输出 IN/OUT/UNDEC 分布
12. `attack_edge_review.py stats` → exit 0，显示人审进度（初始全待审）
13. `pytest -m "not slow" -n auto` → exit 0（含本批新增测试）
14. `pytest -m slow -n0` → exit 1，唯一红 = test_golden_lock_json（预期红，待人审 accept）
15. `ruff check`（本批全部新增/改动 .py）→ All checks passed
16. `git diff --quiet -- atoms evidence Examples Book` → exit 0（受控目录零污染）
17. `git status --short` → 仅本批文件（+ 两条 CRLF 假脏）

---

## 明确不做（任务书边界）

- 不修改 `gate_engine.py` / `atom_evidence_replay.py` / `poison_drill.py` / `toolchain.py` / `cppbible.py`（CORE 五文件不动）
- 不修改 `prop_graph.py`（W2 求解器是独立工具）
- 不修改 MIS/原子卡/证据卡卡面（候选边和人审标注是独立数据文件）
- 不做 grounded 标注的 Web 界面（595 调研后再决定，本批只做 CLI）
- 不做 mutation 端到端反例验证（需要先 populate 数据，留后续批次）
- 不做主动学习/ML 模型（本仓不用 ML，纯规则）
- 不做多人协作/联邦学习（单用户阶段）
- 不 push / 不 golden accept / 不替人签

---

## 偏差表模板（写进 _worklog_596.md §6）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 594 说 42 MIS 带 related_atoms、194 条候选边 | （实跑数字） | 以实跑为准 |
| D2 | W2 结果 IN=79/OUT=42/UNDEC=0 | （实跑数字） | 以实跑为准 |
| D3 | 可信度分级 high/medium/low | （MIS 卡面实际字段情况） | 按实际字段调整 |
| ... | ... | ... | ... |

---

## 过程文档

- `_worklog_596.md`：按惯例不入库，含任务 0 基线 / 各任务实跑数字 / §6 偏差表 / §7 收工验收 / 交人项
- 每个任务一个 commit，message 里写明任务编号和一句话结果
- 改了 CORE 或 conftest.py 必须同 commit --update 带 .tool_checksums
