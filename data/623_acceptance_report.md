# 623 验收报告 · 压力批（高复杂度带攻击 + CI 存量债修复 + Authority/W2 通道打通 + 高复杂度带 block 级规则）

> 批次：623（压力批）· 起始 `bd545b0`（622 收工）· 收工 HEAD 见文末
> 本批 commit：**17 个任务 commit**（任务0 + A1-A5 + B1-B2 + C1-C2 + D1-D2 + E1-E2 + F1-F2）
> 状态：**awaiting_review**（未 golden accept、未打开 delegation、未代签人审、未 push）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、任务完成度：17/17（一任务一 commit）

| # | 任务 | 交付 | Commit | 状态 |
|---|---|---|---|---|
| 0 | 开工基线台账 | `data/623_baseline.md` | `7e91fa02` | ✅ |
| A1 | 高复杂度带 mutation 生成器（4 策略 H1-H4） | `tools/high_complexity_mutator_623.py` + 80 条 + 10 例 | `3a54c167` | ✅ |
| A2 | 80 条高复杂度带 mutation 沙箱实跑 | `data/high_complexity_sandbox_run_623.md` + JSON + 5 例 | `6aac21fc` | ✅ |
| A3 | 新逃逸根因分析 v2 | `tools/escape_root_cause_v2_623.py` + `data/escape_root_cause_high_complexity_623.md` + 3 例 | `17eb0e45` | ✅ |
| A4 | 闭环第三轮（40 条定向） | `tools/round3_mutator_623.py` + `data/adversarial_loop_round3_623.md` + 3 例（含修正 `8c0c5d60`） | `217aeef4` | ✅ |
| A5 | VFDR 更新 + 规则触达热力图 | `tools/vfdr_updater_623.py` + `data/vfdr_report_623.md` + `data/rule_touch_heatmap_623.md` + 4 例 | `708e7782` | ✅ |
| B1 | 治理 manifest 重签 | `data/ci_governance_fix_623.md`（16 文档重签 + tool_integrity 重钉 + verify 绿） | `51055451` | ✅ |
| B2 | tools/ 存量 ruff 债修复 | `data/ci_ruff_fix_623.md`（9 处 + 整目录 ruff 全绿） | `41cc78e9` | ✅ |
| C1 | 收工门禁加整目录 ruff | `tools/run_623_gate.py` + `tests/test_run_623_gate.py`（4 例） | `a17b22dd` | ✅ |
| C2 | 尺子入根扩展审计 | `tools/ruler_coverage_audit_623.py` + `data/ruler_coverage_audit_623.md` + 3 例 | `a8f6ad36` | ✅ |
| D1 | Authority→annotations 同步 | `tools/authority_to_annotations_sync_623.py` + 4 例 | `86ce9765` | ✅ |
| D2 | W2 重算（通道打通后） | `tools/w2_recompute_623.py` + `data/w2_recompute_623.md` + 3 例 | `5af1c4e6` | ✅ |
| E1 | 高复杂度带攻击面分析 | `tools/high_complexity_attack_surface_623.py` + `data/high_complexity_attack_surface_623.md` + 4 例 | `bd32fde2` | ✅ |
| E2 | 高复杂度带 block 级规则 | `data/gate_rules_high_complexity_block_623.yaml` + `data/high_complexity_block_rules_623.md` + 4 例 | `c824c3a9` | ✅ |
| F1 | 622 交人项处理 + 化债 | `data/623_debt_clearance.md` + tests/ 13 处 ruff 债清理 | `f1c0fe19` | ✅ |
| F2 | 收工门禁 + 验收报告 | 本文件 + `run_623_gate.py` 复跑 + status/outbox | 见文末 | ✅ |

---

## 二、收工门禁（F2）复跑结果

```
run_623_gate (whole-dir) → All checks passed!  ✓ ruff 全绿
解释器：.venv\Scripts\python.exe
[1] 整目录 ruff（tools/ tests/，538 个 .py）   ✅ 全绿（F1 清完 tests/ 13 处债后）
[2] 本批新文件 ruff（tools/*_623.py tests/test_*623*.py） ✅ 全绿
[3] 受控目录零污染（atoms/ evidence/ Examples/ Book/） ✅ git diff --quiet 干净
[4] 623 新增单测（tests/test_*623*.py）          ✅ 47 passed
刻意不跑（623 §六.4 铁律）：tool_integrity --check / gate_engine --check / poison / replay --check
B1 governance_doc_guard.py verify 绿（属修复验证，非监工门禁）
```

- 623 新工具 `--check`（实现者）：A1 / C2 / E1 支持 `--check`，其余以单测为验收载体（D1/D2/E2/w2/attack_surface/block_rules 以 pytest 验证）。
- 623 新增单测合计 **47 例**（A1 10 + A2 5 + A3 3 + A4 3 + A5 4 + C1 4 + C2 3 + D1 4 + D2 3 + E1 4 + E2 4 = 47）。

---

## 三、实测数字（压力批核心指标）

### 3.1 A2：80 条高复杂度带 mutation 沙箱实跑（真跑 gate）

| 判决 | 条数 | 占比 |
|---|---|---|
| **blocked** | **46** | 57.5% |
| **detected_nonblock**（warn/advice 级） | **16** | 20% |
| neutral | 12 | 15% |
| **escaped（严格口径）** | **4** | 5% |
| infra_error | 2 | 2.5% |

- **实际触达规则数：25/63（39.7%）**，较 622 的 9/63（14.3%）**+16 条（+178%）**。
- **新逃逸发现：4 条（严格口径）**——经 A3 证实**全部为 warn 级 findings 随内容被删而消失的假象**，真实危险逃逸（dangerous）= **0**。
- 总耗时 527.1s，单条均值 6.59s；infra_error 仅 2.5%（vs 622 的 46%，A1 schema-aware 修复生效）。

### 3.2 A3：新逃逸根因分析 v2

- 4 条 escaped 均为 `M1 删 claim_structured` 导致基线 findings 内容消失，非 block 级检测被击败 ⇒ **真实危险逃逸 0**。
- 给出口径修正建议（strict vs dangerous 双轴）。

### 3.3 A4：闭环第三轮（40 条定向 mutation）

| 判决 | 条数 |
|---|---|
| blocked | 12 |
| detected_nonblock | 14 |
| neutral | 14 |
| escaped（dangerous） | 0 |

- R3 触达 **6 条**规则；**三轮累计触达 26/63（41.3%）**；新逃逸 0。
- 暴露**架构天花板**：gate-only + 单卡 field-edit 无法表达编译/复算/git/多卡构造（约 14 条 block 规则不可触达）。

### 3.4 A5：VFDR + 规则触达热力图

| 批次 | 总 mutation | blocked | detected_nonblock | escaped(dangerous) | **VFDR(检测率)** |
|---|---|---|---|---|---|
| 622 A2 | 50 | 13 | 0 | 0 | 26.0% |
| **623 A2** | 80 | 46 | 16 | 0 | **77.5%** |
| **623 R3** | 40 | 12 | 14 | 0 | **65.0%** |

- **VFDR 622 26% → 623 77.5%/65%**，性质从"flat-zero 不可测"变为"可测且检测率 65-77%"。
- 累计触达 **26/63**（block 21/40、warn 5/16、advice 0/7），**37 条盲区**（需编译/复算/git/多卡/词表黑盒，见 `data/rule_touch_heatmap_623.md`）。
- **诚实登记未达 30/40 的根因**：gate-only 单卡 field-edit 载体上限（主因），留 624 决策。

### 3.5 B1：治理 manifest 重签

| 项 | 值 |
|---|---|
| 操作 | `governance_doc_guard.py update --force`（机械重录 16 处新增受控文档：`_arch_v21/*` + `_auto/inbox/*.md`） |
| 重钉 | 同步 `tool_integrity.py --update`（Merkle 根 + `.tool_checksums`） |
| 校验 | `governance_doc_guard.py verify` **转绿** |

> 硬边界：仅机械重录，**不构成语义认可**；high 清单仍需人读 diff。

### 3.6 B2：tools/ 存量 ruff 债

- 修复 **9 处**（F401 删未用 import os/json ×3、E702 拆单行、E402/I001 提 import 至顶、F841 删未用变量 `primary`）。`ruff check tools/` **全绿**。
- 较提示词"6 处"多发现 3 处（实测 9 处）。

### 3.7 C1：收工门禁加整目录 ruff

- `run_623_gate.py` 对 `tools/`（及 `tests/）**整目录**跑 ruff，口径与 CI 对齐；保留"本批新文件"检查用于快速定位。
- 单测含"只跑本批漏检存量债"陷阱验证（B2 后真实绿）。

### 3.8 C2：尺子入根扩展审计

- `CRITICAL_RULERS` = 11（3 CORE + 8 RULER）。审计 `.tool_checksums`：**11/11 已钉，0 裸露**。
- 坐实 `_arch_v19` p03 "8/11 裸露" 已由 615 B3 `RULER_TOOLS` + 623 B1 重钉修复；**新增保护项 0**（无新裸露需纳入）。

### 3.9 D1：Authority→annotations 同步

| 项 | 值 |
|---|---|
| 输入 | Authority 日志 418 决策 / annotations 388 边 |
| 同步 | `sync()` 按 `edge_id` 合并 → `data/human_attack_edge_annotations.synced.jsonl` |
| 结果 | **0 新增、51 元更新**（418→映射为 388 边，已存在的按较新决策覆盖） |
| 护栏 | 备份 + 校验 + 不删已有 + 标注 source |

### 3.10 D2：W2 重算（通道打通后）

| 视图 | 原子数 | IN | OUT | UNRESOLVED |
|---|---|---|---|---|
| 原 annotations | 67 | 59 | 0 | **8** |
| synced（D1 后） | 67 | **67** | 0 | 0 |

- **原 → synced 变化 8 原子**（全部 `UNRESOLVED → IN`）：`ATOM-LANG-INLINE-001 / MIS-LANG-001 / MIS-MEM-001/003 / MIS-UB-001/004/008/014`。
- 根因：原 annotations 34 条 `modify` 动作被 W2 当 UNRESOLVED；D1 把 Authority 决策（ACCEPT→approve）合并后 34 条 `modify` 转为 `approve` ⇒ 8 原子翻 IN。
- **结论**：622 D2 "W2 变化 0" 确为**通道断伪影**；通道打通后实测 8 变化（非提示词假设的"仍 0"）。

### 3.11 E1：高复杂度带攻击面分析

- 复现 622 E2：高复杂度带（>60）仅触发 **warn 级**规则（`EV-SERVES-EXIST` / `ATOM-REL-TARGET` / `ATOM-REL-UNKNOWN`），**无 block 级兜底**。
- **attack_surface_score = 87.5**（高复杂度攻击面广泛但仅 warn 拦截）。

### 3.12 E2：高复杂度带 block 级规则

- 交付 **4 条 block 规则定义**（独立文件 `data/gate_rules_high_complexity_block_623.yaml`）：
  `EV-SERVES-EXIST-HC` / `ATOM-REL-TARGET-HC` / `ATOM-REL-UNKNOWN-HC` / `CARD-PATH-NOT-CANONICAL-HC`。
- **铁律遵守**：**未接线 `gate_engine.py`**（禁改 CORE_TOOLS 逻辑）；规则数仍 63，**未达"63→66-68"**（接线留人/624）。
- 4 例单测验证：规则数 3-5、全部 block 级、由真实 warn 规则升级、字段齐全。

---

## 四、偏差表（诚实登记）

| 项 | 提示词/计划 | 实际 | 说明 |
|---|---|---|---|
| **A2 单轮触达** | **>30 规则** | **25/63** | 未达；根因=载体上限（A5 §四），留 624 |
| **三轮累计触达** | **>40 规则** | **26/63** | 未达；同上 |
| 新逃逸 | 期望"真正发现" | **0 危险逃逸**（4 strict 假象） | 攻击面打到 25/63 仍 0 危险逃逸，说明 gate 规则层对触达到的攻击很硬 |
| VFDR | 期望"不再恒 0" | **77.5% / 65%** | 超额：从 flat-zero 变为可测且检测率 65-77% |
| W2 判决 | 期望"看是否变化" | **8 原子变化** | 超额：证伪 622 D2 通道断假设 |
| B2 ruff 债 | 6 处 | **9 处** | 多发现 3 处，全修 |
| C2 新增保护 | 扩展保护项 | **0 新增（11/11 已保护）** | _arch_v19 8/11 早已修复，无需新增 |
| E2 规则数 | 63→66-68 | **63（未接线）** | 铁律禁改 CORE_TOOLS，接线留人/624 |
| CI 状态 | push 后转绿 | **本地 verify/ruff 全绿，未 push** | 铁律"不 push"；远程绿需人 push |
| 复杂度评分 | 每条 >60 | 启发式代理（算子类型映射） | 非 AST/语义精确度量 |

---

## 五、核心诚实结论（本批最重要）

### 5.1 闭环真正突破，但撞上架构天花板

- 从 622 的 **9/63（14.3%）** 跃升到 **26/63（41.3%）**，检测率 **26%→77.5%**；但**未达 30/40 目标**。
- 根因已定位且不可靠"再加 mutation"解决：**gate-only + 单卡 field-edit** 表达不出约 14 条 block 规则所需的编译/复算/git/多卡构造。这是**载体天花板**，非生成器缺陷——下一次突破需沙箱支持多卡/编译/replay 复算层（留 624）。

### 5.2 两条通道被打穿

- **Authority↔annotations↔W2**：D1 打通投影通道，D2 实测 **8 原子从 UNRESOLVED→IN**，坐实 622 D2 "变化 0" 是通道断伪影。
- 30 条逐条人审**真正影响了判决**（此前从未进入 solver）。

### 5.3 CI 存量债本地已清，远程待 push

- B1 治理重签 + B2 tools/ ruff 全绿 + F1 清 tests/ 13 处债 ⇒ **本地 ruff/verify 全绿**。
- 远程 CI 转绿需 `git push`（铁律禁止本批 push，交人执行）。

### 5.4 高复杂度带规则缺口已定义，未接线

- E2 给出 4 条 block 级规则定义，但**未接入 gate_engine**（铁律），属"交付设计、接线留人"，供 624 或人审决策。

---

## 六、局限性 / 未做项（诚实登记）

1. **受载体天花板限制**：约 37 条规则未触达，其中 ~14 条 block 规则需编译/复算/git/多卡构造（单卡 field-edit 不可达）。
2. **判决只含 gate（规则层）**：未含 replay 复算层 ⇒ 可能漏"规则过但复算不过"的逃逸。
3. **复杂度是启发式代理**（算子类型映射），非 AST/语义精确度量。
4. **E2 block 规则未接线 gate_engine**（铁律禁改 CORE_TOOLS），故未实测其 block 效果，仅定义+单测。
5. **D1 同步未反向写回原 annotations**（产出 `.synced.jsonl` 供 solver 读取），原文件保持只读来源。
6. **未 push**（铁律）；远程 CI 是否转绿待人执行。
7. **未做雷1/雷8**（622 §六.8 明确留 625+）；本批属压力批非建设批。
8. **样本量小**：A2 80 + R3 40 = 120 条，分桶后部分桶样本极少。

---

## 七、交人项（不可代决）

### 7.1 本批交付待人拍板
1. **A2/A4 未达 30/40 触达目标**——是否接受"载体天花板"诊断、是否立项 624 升级沙箱支持多卡/编译/replay 层。
2. **E2 4 条 block 规则是否接线 gate_engine**（改 CORE_TOOLS，需人授权）。
3. **D2 8 原子判决变化（UNRESOLVED→IN）是否最终接受**。
4. **B1 治理重签是否认可**（机械重录，high 清单内容仍需人读 diff）。
5. **是否 push 让远程 CI 转绿**（铁律禁止本批 push）。
6. **Verification Horizon 是否纳入核心 metrics**（建议同时纳入"最低桶检出率"）。

### 7.2 622 遗留仍留人（见 F1 §1.2，共 12 条）
沙箱入 CORE_TOOLS / 原子卡 verdict 写回 / ABSTAIN 对外展示 / 人审数据开源 / 攻击目标权重 / Authority 正式替换 / PCK 权威源 / 新 mutation 入 v8 基线 等。

---

## 八、收工

- 17/17 任务全部完成，**一任务一 commit**，无 golden accept、无 delegation、无人审代签。
- 收工门禁（`run_623_gate.py` 整目录 ruff）**PASS**；受控目录零污染。
- 状态置 `awaiting_review`；历史追加 623 条；outbox 见 `_auto/outbox/623.md`。
- **做不完的登记**：触达天花板、E2 接线、push、12 条遗留交人项 → 留 624。
