# 623 F1 · 622 交人项处理 + 化债

> 批次：623 · 任务 F1 · 前置：622 收工（`bd545b0`，17/17，awaiting_review）
> 解释器：`.venv\Scripts\python.exe`
> 铁律：不修改 CORE_TOOLS 逻辑、不修改原始卡、一任务一 commit、不 golden accept、不 push

---

## 一、622 交人项（16 条）处理状态

### 1.1 本批已机器化处理的 4 条（623 B1/B2/C1/D1/D2/E1/E2）

| 622 交人项 | 623 处理 | 交付 | 状态 |
|---|---|---|---|
| #13 CI 两条存量债（治理 manifest + tools/ ruff） | B1 治理重签 + B2 tools/ ruff 全绿 | `51055451` / `41cc78e9` | ✅ 已化 |
| #14 收工门禁加"整目录 ruff" | C1 `run_623_gate.py` 对 tools/&tests/ 整目录跑 ruff | `a17b22dd` | ✅ 已化 |
| #15 Authority↔annotations/W2 投影通道 | D1 同步工具 + D2 W2 重算 | `86ce9765` / `5af1c4e6` | ✅ 已化 |
| #16 高复杂度带 block 级规则 | E1 攻击面分析 + E2 4 条 block 规则定义 | `bd32fde2` / `c824c3a9` | ✅ 规则定义已化（**未接线 gate_engine**，见 §二.3） |

### 1.2 仍留交人（12 条，需人拍板或留 624）

| # | 622 交人项 | 623 进展 | 留交人理由 |
|---|---|---|---|
| 1 | 沙箱 apply API 是否纳入 CORE_TOOLS | 仅实现，未升核心 | 工具升级属架构决策，交人/624 |
| 2 | 新逃逸是否修复 / 60+ warn→block | E2 已定义 4 条 block 规则 | **未接线 gate_engine.py**（铁律禁改 CORE_TOOLS），是否上线待人 |
| 3 | 原子卡 verdict 是否写回原始卡 | 622 C2 仅提取 | 写回受控卡=改原始卡，铁律禁止，交人 |
| 4 | 30 条逐条人审最终认可 | D1/D2 已同步并产生 8 原子翻转 | 执行已按用户授权，最终认可交人 |
| 5 | W2 判决变化是否接受 | D2 实测 8 原子 UNRESOLVED→IN | 是否接受新判决交人 |
| 6 | Verification Horizon 是否入核心 metrics | E1/E2 已定义+量化 | 指标纳入属决策，交人（建议同时纳入"最低桶检出率"） |
| 7 | 新 mutation 是否纳入 v8 基线 | A1/A2/A4 共 120 条未入库 | 基线升级属 624 |
| 8 | ABSTAIN 是否对外展示（写 PCK 渲染） | 未渲染 | 渲染件改需人审 |
| 9 | 人审脱敏数据是否开源 | 未处理 | 合规决策，交人 |
| 10 | 攻击目标权重拍板（W1 vs W2） | 未处理 | 策略决策，交人 |
| 11 | Authority 是否正式替换人审通道 | D1 已打通投影通道 | 正式替换属治理决策，交人 |
| 12 | PCK 是否成为权威源 | 未处理 | 治理决策，交人 |

---

## 二、本批化债内容

### 2.1 CI 存量债（B1/B2）
- **治理 manifest 重签**：`governance_doc_guard.py update --force` 机械重录 16 处新增受控文档（`_arch_v21/*` + `_auto/inbox/*.md`），同步 `tool_integrity.py --update` 重钉 Merkle 根与 `.tool_checksums`，`governance_doc_guard.py verify` 转绿。
- **tools/ 存量 ruff 债**：修复 618/619 文件 9 处（F401 删未用 import ×3、E702 拆单行、E402/I001 提 import 至顶、F841 删未用变量）。`ruff check tools/` 全绿。
- **硬边界遵守**：`update --force` 仅机械重录，不构成语义认可；high 清单仍需人读 diff。

### 2.2 门禁口径统一（C1）
- `run_623_gate.py` 对 **整个 tools/（及 tests/）** 跑 ruff（非仅本批新文件），统一为 CI 同口径；保留"本批新文件"检查用于快速定位。
- 单测含"只跑本批漏检存量债"陷阱验证，证明 B2 修复后真实整目录绿。

### 2.3 tests/ 存量 ruff 债（F1 本步补清）
- C1 门禁升级后覆盖 `tests/`，但发现 **13 处 ruff 债**（5 处在 623 新测试文件、8 处在 618/619/其他历史测试文件）。
- 全部为风格类（F401 未用 import ×4、I001 import 排序 ×4、E702 单行多语句 ×5），**不改任何逻辑**。
- 已用 `ruff --fix` 自动修复 8 处，手动拆分 5 处 E702 分号；修复文件：
  - 623：`test_adversarial_loop_round3_623.py`、`test_high_complexity_block_rules_623.py`、`test_w2_recompute_623.py`
  - 历史：`test_618_c4.py`、`test_619_b3.py`、`test_619_gate.py`、`test_escape_rate_estimand.py`、`test_verify_independence_level.py`
- 修复后 `ruff check tools/ tests/` 与 `ruff check tools/*_623.py tests/test_*623*.py` **均全绿**；`pytest tests/test_*623*.py` 47 例全过。

### 2.4 仍登记为债（本批未清，留 624）
- 高复杂度带 block 规则未接线（§1.2 #2）—— 铁律禁改 `gate_engine.py`，接线留人/624。
- 未达 A2>30 / 累计>40 触达目标（实测 25 / 26），根因=gate-only 单卡 field-edit 载体上限（详见 A5 §四），属架构天花板，非债可清，留 624 决策。

---

## 三、本批新文件清单（F1 提交范围）

- `data/623_debt_clearance.md`（本文件）
- 上述 8 个测试文件的 ruff 风格修复（已 `git add` 指定文件，未带无关改动）

> **未纳入本提交的环境/并行改动**（非本批产出，留原状）：
> `_adv_v80/probes/p57.cpp`（仅 CRLF 提示）、`data/metrics_612.md`（1 行预存改动）、
> 未跟踪的 `_arch_v19/`、`_arch_v19_brief.md`、`_arch_v20/`、`_arch_v20_brief.md`（并行 PM 产物）。
> 这些不在 623 任务范围，未 stage、未提交。

---

## 四、结论

622 的 16 条交人项中，**4 条（#13/#14/#15/#16 的规则定义部分）已机器化处理**，
其余 12 条因涉及 CORE_TOOLS 逻辑修改、受控卡写回、治理/策略决策，留交人或 624。
本批同步化清了 C1 整目录门禁暴露的 `tests/` 13 处 ruff 债，使收工门禁可真正转绿。
