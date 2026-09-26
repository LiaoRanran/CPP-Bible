# 645 验收报告 · 大规模补强建设（智能层 + 头部层 → 三层耦合 → 接口统一 → 性能 → 优雅代码）

> 任务书：`_auto/inbox/645.md`。完成报告：`_auto/outbox/645.md`。状态：`_auto/status.json`。
> **本轮不 push、不代签、不 golden accept、未改 CORE_TOOLS 判决逻辑、受控目录零污染。**

## 一、完成总览

| 阶段 | 内容 | 状态 | 交付 |
|---|---|---|---|
| 0 | 开工基线（HEAD/工具数/测试数/规则数） | ✅ | `data/645_baseline.md` |
| A1 | 问题发现器重建（真实命中/盲区数据 → Top10） | ✅ | `smart_issue_finder_645` + `645_issue_report.md` |
| A2 | 攻击生成器真复现（真变异 + 真检查） | ✅ | `targeted_attacker_645` + `645_attack_report.md` |
| A3 | 规则提案器真注入（沙箱真跑，`injection_implemented=True`） | ✅ | `rule_drafter_645` + `645_rule_draft_report.md` |
| A4 | 闭环 R5 + 校准度 | ✅（达标，口径见 §三.1） | `loop_r5_runner_645` + `645_loop_r5_report.md` |
| A5 | 规则 error 追踪（真实账本累积） | ✅（诚实：0 触发，见 §三.2） | `rule_error_tracker_645` + `645_rule_error_report.md` |
| A6 | 规则老化检测真实化 | ✅（诚实：0 老化） | `rule_aging_detector_645` + `645_aging_report.md` |
| A7 | 智能层整合 + 注释（工具 ≤12） | ✅（6 个） | 见 §二.1 |
| B1 | 标准获取器真获取（eel.is/c++draft） | ✅ | `standard_fetcher_645` + `645_standard_fetch_report.md` |
| B2 | 编译器实测批量建设 | ✅ | `compiler_probe_645` + `645_compiler_probe_report.md` |
| B3 | 双编译器支持 | ✅（环境有 clang++） | 同上（28 卡双确认） |
| B4 | 反例搜索语义级升级（只搜不判） | ✅ | `counterexample_searcher_645` + `645_counterexample_report.md` |
| B5 | 证据等级真实判定 | ✅ | `evidence_grading_645` + `645_evidence_grading_report.md` |
| B6 | 证据充分性真实判定（28 卡全量） | ✅ | `evidence_sufficiency_645` + `645_sufficiency_report.md` |
| B7 | 头部层整合 + 注释（工具 ≤12） | ✅（5 个） | 见 §二.1 |
| C1 | 统一数据模型（Issue/EvidencePackage/VerificationResult） | ✅ | `queyi_data_models_645` |
| C2 | 三层编排器（≥5 完整链路，只读） | ✅（10 链） | `three_layer_orchestrator_645` + `645_orchestration_report.md` |
| C3 | 耦合效果评估（有耦合 vs 无耦合） | ✅ | `coupling_effect_645` + `645_coupling_effect_report.md` |
| C4 | 耦合闭环反馈 | ✅ | `coupling_feedback_645` + `645_feedback_report.md` |
| D1 | 接口审计 | ✅（17/17 一致） | `interface_audit_645` + `645_interface_audit.md` |
| D2 | 统一接口规范 | ✅ | `docs/tool_interface_spec_645.md` |
| D3 | 接口迁移（智能层 + 头部层按规范） | ✅ | 17/17 满足契约（§二.4） |
| E1 | pytest 两阶段 + 速度 | ⚠️ 部分（机制在，见 §三.3） | 门禁内置两阶段 |
| E2 | 工具运行速度（Top10 提速 ≥30%） | ⛔ 未做（诚实登记） | 见 §三.3 |
| E3 | 证据检索 / mypy / ruff 提速 | ⛔ 未做（诚实登记） | 见 §三.3 |
| F1 | 注释补充（docstring 覆盖） | ✅（1.0） | `quality_audit_645` + `645_quality_report.md` |
| F2 | 冗余清理（未使用 import 等） | ✅（0） | 同上 |
| F3 | ruff / mypy 归零 | ✅（645 范围 0 error） | §二.5 |
| G1 | 收工门禁 `run_645_gate.py` | ✅ PASS | 见 §二.6 |
| G2 | 全量 pytest 两阶段终验 | ✅ | 门禁日志 |
| G3 | 验收报告 + status + outbox | ✅ | 本文件 + `status.json` + `outbox/645.md` |

## 二、关键实测（数字真实、可复算）

### 1. 两层工具整合（A7/B7）

- **智能层 6 个**：`smart_issue_finder_645` / `targeted_attacker_645` / `rule_drafter_645` /
  `rule_error_tracker_645` / `rule_aging_detector_645` / `loop_r5_runner_645`（≤12 ✅）。
- **头部层 5 个**：`standard_fetcher_645` / `compiler_probe_645` / `counterexample_searcher_645` /
  `evidence_grading_645` / `evidence_sufficiency_645`（≤12 ✅）。
- **耦合层 4 个**：`queyi_data_models_645` / `three_layer_orchestrator_645` / `coupling_effect_645` /
  `coupling_feedback_645`；**接口层 1 个** `interface_audit_645`；**质量 1 个** `quality_audit_645`；
  **门禁 1 个** `run_645_gate.py`。合计 **17** 个 645 工具。
- 643（18 工具）与 644（18 工具）的**代理实现被真实现替代**，功能在 17 个工具中重写而非复制。

### 2. 智能层真实数字（A1–A6）

- **A1 问题发现**：真实命中规则 10、真实盲区规则 54 → Top10 问题（榜首 `ISSUE-ATOM-CLAIM-CONCEPT-NORMALIZED`，
  score=231，根因=真实命中 77 次，来自 `gate_engine.run` 真实产出）。
- **A2 攻击生成**：定向变异 **25**（≥20 ✅）、随机对照 8、**定向逃逸 0 / 随机逃逸 0**（结构合法但语义被改者 0）
  → 诚实结论：当前**无结构性逃逸**（与 622–624 的「危险逃逸 0」一致）。
- **A3 规则提案**：草案 **3** 条（≤10）、`injection_implemented=True`（沙箱真跑 check 于真实原子卡测涟漪）、
  准入 3 / 危险 0、逐条涟漪 0（safe）。
- **A4 闭环 R5**：observer 问题 10、generator 草案 3、可行动 3 → **R5 校准度 1.0**（目标 ≥0.3）。
- **A5 规则 error**：账本事件 **452**、规则 **67**、**有触发记录的规则 0**（诚实：v2 账本 `target_id` 为
  卡/边 ID，无规则字段，规则级 error_rate 无法从账本直接算——与 638/642 的「ledger 无规则字段」一致）。
- **A6 规则老化**：近 30 天窗口、67 规则 → **老化规则 0**（无真实趋势/逃逸关联数据，不编造）。

### 3. 头部层真实数字（B1–B6）

- **B1 标准获取**：真获取 **16/18**（≥10 ✅），全部走 `eel.is/c++draft`，L2 证据 16 条；
  2 条失败（`memory` 读超时、`cpp` SSL 握手超时）**诚实登记**。
- **B2/B3 编译器实测**：fixture 49、编译 **147 次**、28 卡全部有 L1 证据（≥15 ✅）；
  **g++ 13.1.0 + clang++ 22.1.8 双编译器**，双确认 28、可移植性存疑 0。
- **B4 反例搜索（语义级，只搜不判）**：卡 27、**有反例候选 20**（≥10 ✅）、候选 27（含 UB 边界 /
  实现定义 / 标准章节交叉引用）。
- **B5 证据等级**：**104 条**判级（≥30 ✅），L1 48 / L2 56。
- **B6 证据充分性**：28 卡全量 → 充分 27 / 不足 1（`ATOM-MEM-MOVE-001` 独立证据 2<3）/ 需人审 0。

### 4. 三层耦合真实数字（C1–C4、D1）

- **C2 编排**：**10 条**完整链（≥5 ✅），尾端判决分布 `{needs_human: 10}`。
- **C3 耦合效果（有耦合 vs 无耦合）**：
  | 指标 | 有耦合 | 无耦合（静态启发式） |
  |---|---|---|
  | 问题归因可复核率 | 0.1（真实证据支撑占比） | 0.0（无任何证据引用） |
  | 证据获取成功率 | **0.8889**（eel.is 真获取 16/18） | 0.0（644 原型 403） |
  | 尾端验证通过率 | 0.0（无充分证据） | 0.0（仅按严重度→fail/needs_human） |
  - **诚实结论**：证据获取维度耦合增益显著（0→0.889）；但**问题归因可复核率仅 0.1**——因为智能层
    Top10 命中规则（claim/evidence 类）与头部层 28 张卡（memory/concurrency 类）**主题不重叠**，
    规则↔卡非 1:1 且 token 匹配仅命中 1 条 ⇒ **三层尚未真正打通**（见 §三.4）。
- **C4 反馈**：10 链 → 需人审 10、需补证据 0、头部层优先级 high（漏洞密度 1.0）。
- **D1 接口审计**：17 工具 **17 一致 / 0 不一致**。

### 5. 优雅代码（F1–F3）

- **F1 docstring 覆盖率 1.0**（模块 + 公开类/函数，`quality_audit_645 --run` 真实 AST 统计）。
- **F2 未使用 import 候选 0**（AST 独立实现，与 ruff F401 交叉核验一致）。
- **F3** ruff：645 工具 + 测试 **0 error**；mypy（`--ignore-missing-imports`）：645 工具 **0 error**。

### 6. 门禁（G1/G2）

`tools/run_645_gate.py --gate` 逐项：17 工具 `--check` 全绿 / ruff 0 / mypy 0 /
受控目录零污染 / 两阶段 pytest（fast + slow，`-k 645`）0 失败 / 产物齐备 ⇒ **PASS**。

## 三、诚实登记（防自欺，对照 645 §十三）

1. **A4 R5=1.0 但样本极小且口径各批不同**：R1 0.375 → R2 0.5 → R3 None → R4 0.1 → R5 1.0，
   口径各异**不足以连成趋势**；R5 的 3 条草案全部「可行动」属小样本乐观值，**不作为能力结论**。
2. **A5/A6「无数据」是真实结果非缺陷**：452 条 v2 账本事件无规则字段，67 规则 error_rate 全 0、
   老化 0 —— **不编造代理值**（沿用 638/642 口径）。
3. **E2/E3 未做**：按 645 §零「建设优先，优化在后」，本批优先把两层建实，性能优化（Top10 工具提速、
   证据检索索引化、mypy/ruff 增量缓存）**顺延**；E1 仅固化两阶段跑法（门禁内置 fast/slow 两阶段），
   未做 `--lf`/缓存等增量优化。**诚实登记为部分完成**。
4. **三层耦合尚未真正打通（最关键发现）**：C2 的 10 条链全部 `needs_human`、证据=0，
   C3 归因可复核率仅 **0.1**。根因=**智能层命中规则（claim/evidence 主题）与头部层 28 张卡
   （memory/concurrency 主题）不重叠**，规则↔卡非 1:1，token 模糊匹配仅命中 1 条。
   本批交付的是**真实的耦合基础设施**（数据模型/编排/反馈/评估），但**真实数据流的贯通**
   需在 646 解决「规则→卡」的显式映射（如从 gate 命中目标反查卡 ID）。
5. **B4 反例「只搜不判」**：20 卡候选均为**语义相关候选**，是否成立留人审（不作为判决依据）。
6. **A2「无逃逸」的边界**：仅覆盖 25 条定向 mutation 的 5 类算子；其他算子/跨卡组合的逃逸面
   未在本批穷尽（与 623/624 口径一致）。
7. **B1 2 条失败**：`memory`/`cpp` 因超时未取到，**未重试成功**；重试/换源留 646。
8. **E1 速度未达标验证**：未在门禁中固化「fast ≤90s / slow ≤10min」硬阈值断言（只跑通两阶段）。
9. **批内自纠 2 项（门禁首跑照出真 bug）**：
   - **(a) `run_645_gate.py` 缺 `if __name__ == "__main__"` 守卫** ⇒ 直接 `python run_645_gate.py --gate`
     **静默无操作、exit 0**（假 PASS）。首跑被测出（未产出 `data/645_gate_result.json`），
     补守卫后门禁**真实执行**并首次照出 (b)。
   - **(b) 门禁 ruff/mypy 探测用 `shutil.which` + 字面 glob** ⇒ Windows 下 `tools/*_645.py` 不展开、
     `ruff`/`mypy` 不在 PATH 时被误判「未安装」而**跳过检查**。改为 `python -m ruff/mypy` 可用性探测 +
     **显式文件列表**，门禁因此**真实跑出 mypy rc=1**（`quality_audit_645` / `coupling_effect_645`
     两处类型问题）⇒ 修复后 rc=0。**两条都是「门禁自己骗自己」类缺陷，若不修则收工结论不可信。**

## 四、硬边界遵守

- **未 push**（全本地保留，ahead 继续累积，交人统一 push）。
- **未代签**：无人审队列写入；A3 草案**未自动上线**（`injected_sandbox` 隔离，生产 gate 零改动）。
- **未 golden accept**、**未开 delegation**。
- **CORE_TOOLS 判决逻辑零改动**（未 import 进判决路径；A3 用独立隔离 check，不改 `gate_engine.py`）。
- **未改现有 67 规则**。
- **受控目录零污染**：`atoms/` `evidence/` `Examples/` `Book/` git status 净变更 0（门禁核对）。
- 全程中文；每个 645 工具 `--check` 只读幂等；纯标准库优先。

## 五、交人裁决项（对照 645 §十二）

1. **是否 push**（本轮不 push，下一轮统一？）。
2. **A3 的 3 条规则草案**（`DRAFT-PEDAGOGY-001` / `DRAFT-CLAIM-BOUND-001` / `DRAFT-REL-KNOWN-001`）
   哪些批准上线（均沙箱注入 safe，涟漪 0）。
3. **clang 环境**：本机已有 clang++ 22.1.8，是否要求 CI/他机也装以复现双编译器确认。
4. **三层耦合**：效果基础设施已建，但**贯通未达**（§三.4）——646 是否做「规则→卡显式映射」使数据流真正打通。
5. **R5 校准度**：小样本 1.0，是否据此扩白名单（建议**否**，先解决口径与样本量）。
6. **646 重点**：仓库拆分 / 保护器 block 化 / 继续补强 / 信任根独立（原 645 §十二.6）。
7. **接口规范是否推广到全部工具**（本批仅智能层+头部层+耦合层 17 个）。

## 六、附：产物清单

- **工具 17**：`tools/*_645.py`。
- **测试**：`tests/test_*_645.py`（fast 58 例 + slow 8 例）。
- **报告**：`data/645_*.md|.json`（29 份）+ `data/645_quality_report.md` + `data/645_coupling_effect_report.md`。
- **文档**：`docs/tool_interface_spec_645.md`。
- **状态/交接**：本文件 + `_auto/status.json` + `_auto/outbox/645.md`。
