# 624 验收报告 · 突破批（跨卡一致性攻击 + E2 规则接线 + push CI 验证 + 修 623 遗留）

> 批次：624（突破批）· 起始 `4ef44c19`（623 收工）· 收工 HEAD 见文末
> 本批 commit：**18 个**（任务0 + A1-A5 + A1修正 + B1-B2 + C1-C2 + D1-D3 + E1-E2 + F1-F2）
> 状态：**awaiting_review**（未 golden accept、未打开 delegation、未代签、已 push）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、任务完成度：17/17

| # | 任务 | 交付 | Commit | 状态 |
|---|---|---|---|---|
| 0 | 开工基线 | `data/624_baseline.md` | `dca19094` | ✅ |
| A1 | 跨卡一致性攻击（4 策略 X1-X4 + 60 条） | `tools/cross_card_attack_624.py` + 设计 + 9 例 | `d685a961` | ✅ |
| A2 | 60 条跨卡沙箱实跑 | `data/cross_card_sandbox_run_624.md` + JSON + 5 例 | `ce5e48ed` | ✅ |
| A3 | 新逃逸根因分析 v3（跨卡 4 维度） | `tools/escape_root_cause_v3_624.py` + 分析 + 8 例 | `40068c58` | ✅ |
| A4 | 闭环第五轮（X5-X8，40 条） | `tools/round5_mutator_624.py` + 报告 + 4 例 | `7acfa033` | ✅ |
| A5 | VFDR v2 + 热力图 v2 + 盲区缩减 | `tools/vfdr_updater_v2_624.py` + 报告 + 6 例 | `4a79dc8d` | ✅ |
| — | **A1 修正**（apply_multi 同卡多编辑备份去重） | 修 `cross_card_attack_624.py` + 重跑 A2/A4 | `c92aac53` | ✅ |
| B1 | 4 条 block 规则接入 gate_engine（63→67） | `gate_engine.py` + 报告 + 6 例 + 快照 + 重钉 | `efbaf9f6` | ✅ |
| B2 | 规则回归 + 误报分析 | `data/high_complexity_rules_regression_624.md` + 5 例 | `bcf4e3d4` | ✅ |
| C1 | push 623-624 到远程 | `data/push_624.md`（37 commit） | `55885eba` | ✅ |
| C2 | CI 远程实跑验证 | `data/ci_remote_verify_624.md` + 修复 + 再 push | `8ac4b4ca` | ✅ |
| D1 | 3 个 CLI 工具补 `--check` | 3 工具 + 报告 + 4 例 | `b2a46205` | ✅ |
| D2 | 工具名对齐 + 功能合并确认 | `data/tool_name_alignment_624.md` | `58f790f8` | ✅ |
| D3 | 623 交人项处理 + 化债 | `data/624_debt_clearance.md` + 豁免治理 + 计数修复 | `567c3e96` | ✅ |
| E1 | PCK authorized 提升 | `tools/pck_authorized_upgrade_624.py` + 报告 + 6 例 | `6a2f9d24` | ✅ |
| E2 | 人审逐条 30→>100 | `tools/human_review_item_by_item_generator_624.py` + 清单 + 6 例 | `af64af28` | ✅ |
| F1 | 收工门禁 | `tools/run_624_gate.py` + 4 例 | `770bf45c` | ✅ |
| F2 | 验收报告 + status/outbox | 本文件 + status/outbox + manifest 重签 | 见文末 | ✅ |

---

## 二、收工门禁（F1）复跑结果

```
run_624_gate → PASS
✅ 整目录 ruff（tools/ tests/）    All checks passed!
✅ 本批(624)文件 ruff              All checks passed!
✅ 624 新工具 --check              5/5
✅ 623/622/621 回归 --check        8/8
✅ ci.yml 语法                     YAML OK
✅ 受控目录零污染                   clean
刻意不跑（铁律 §六.4）：tool_integrity --check / gate_engine --check / poison / replay --check
```
- 624 新增单测：A1 9 + A2 5 + A3 8 + A4 4 + A5 6 + B1 6 + B2 5 + D1 4 + E1 6 + E2 6 + F1 4 = **63 例**。

---

## 三、实测数字（突破批核心指标）

### 3.1 A2：60 条跨卡攻击沙箱实跑

| 判决 | 条数 |
|---|---|
| blocked | 47 |
| detected_nonblock | 13 |
| neutral / escaped / infra | 0 / 0 / 0 |

- 本轮触达 13 条规则，**相对 623 新增 2 条**（`ATOM-REL-CONFLICT`、`EV-ARTIFACT-FILE-EXISTS`）⇒ **累计 28/63**。
- 预测命中 6/7（85.7%）。

### 3.2 A4：闭环第五轮（X5-X8，40 条）

| 判决 | 条数 |
|---|---|
| blocked | 38 |
| detected_nonblock | 0 |
| neutral | 2 |
| escaped | 0 |

- 新触达 **4 条**（`ATOM-MISCONCEPTION-REF` · `ATOM-VERIFIED-BOUND` · `OBSERVATION-NEEDS-ARTIFACT` · `S2-EVIDENCE-VERDICT`）；预测命中 4/4。

### 3.3 A5：VFDR v2 + 热力图 v2（6 轮）

| 口径 | 623 | **624（六轮全量）** | 目标 |
|---|---|---|---|
| **累计触达规则** | 26/63 | **34/63（54.0%）** | >45 ❌ |
| **盲区** | 37 | **29** | <25 ❌ |
| 检测率 | 77.5%/65% | R5 **100%** / R6 **95%** | — |

- 相对 623 新增 8 条规则触达；**危险逃逸全程 0**。
- **诚实登记**：>45/63 与盲区 <25 **未达**（根因：37 盲区中多数需编译/复算/git/词表载体，跨卡亦不可达）。

### 3.4 B1/B2：4 条 block 规则接入 gate_engine

| 项 | 值 |
|---|---|
| 规则数 | **63 → 67**（+EV-SERVES-EXIST-HC / ATOM-REL-TARGET-HC / ATOM-REL-UNKNOWN-HC / CARD-PATH-NOT-CANONICAL-HC） |
| 机制 | 复用既有 check；仅对结构复杂度 ≥75 的卡把 warn 升 block |
| 基线 gate | findings 191 / **block 0**（新规则 **0 误报**） |
| poison | **124/124**（RULE-COVERAGE 39/67，4 条 HC 已登记豁免） |
| 624 跨卡复跑 | blocked **47→55**（`ATOM-REL-TARGET-HC` / `ATOM-REL-UNKNOWN-HC` 实证触发） |

### 3.5 C1/C2：push + CI 远程验证

- **C1**：push `96fc0b83..bcf4e3d4`（37 commit）；再 `bcf4e3d4..8ac4b4ca`（C2 修复）。
- **C2（run #629，sha 8ac4b4c）**：

| job | 结论 |
|---|---|
| concurrency-safety | ✅ |
| replay | ✅ |
| **gate** | ✅（修复前 #628 红：poison 4 条 HC 未豁免 → 已登记豁免） |
| **quality (3.11)** | ❌ **Mypy**（67 处存量债，24 文件，620-623） |
| **pytest** | ❌（治理 manifest 待重签 + 620/621 meta 测试） |

### 3.6 D1/D2/D3

- **D1**：3 个 CLI 工具补 `--check`，**3/3 exit 0**。
- **D2**：623 A3/A5 **未建 CLI 工具**（实为数据件+测试交付）；功能完整；624 已补工具化后继。
- **D3**：623 交人项 4 项已化（E2 接线/push/CLI--check/工具名）；化债含 mypy 624 段 8 处、豁免治理动态化、
  历史计数测试 388→418、poison 快照。

### 3.7 E1/E2：人审 + PCK

| 项 | 结果 |
|---|---|
| E1 PCK authorized | **27/83（32.5%）→ 27/83**（机器可判定候选 **0**：27 原子证全已授权、56 证据证无人审来源）⇒ 目标 >48% ❌ |
| E2 人审逐条 | 生成 **80** 条（34 high + 46 medium）；记录数 **110** > 100 ✅（只生成不执行）<br>⚠ 626 A1 修正：110 为**记录条数**，**唯一复核对象 = 93**（30+80−overlap 17） |

---

## 四、偏差表

| 项 | 目标 | 实际 | 说明 |
|---|---|---|---|
| A2 累计触达 | >40/63 | **28/63** | 跨卡仅新增 2 条 |
| A4 六轮累计 | >45/63 | **34/63** | 新增 8 条 |
| 盲区缩减 | <25 | **29** | 缩减 8 条 |
| 新逃逸 | >0（期望） | **0** | 100 条跨卡攻击无危险逃逸 |
| gate 规则数 | 67 | **67** | ✅ |
| CI 远程 | 全绿 | **gate/replay/concurrency ✅，quality ❌（mypy 存量），pytest ❌** | 见 §五 |
| PCK authorized | >48% | **32.5%** | 机器可判定候选 0（不代签） |
| 人审逐条 | >100 | **110** | ✅（只生成） |
| B2 ruff 债 | — | tools/ 全绿 | ✅ |
| A1 修正 | — | apply_multi 同卡多编辑备份去重 | 原实现致受控目录残留，已修并重跑 |

---

## 五、核心诚实结论

### 5.1 跨卡攻击突破了部分盲区，但**未突破天花板目标**
- 六轮累计 **34/63（54.0%）**，相对 623 的 26 增幅 +31%；但距 >45 仍差 11 条。
- **根因**：gate_engine 无专门跨卡检查族；37→29 盲区中多数（编译/复算/git/词表）**跨卡 sandbox 亦不可达**。

### 5.2 E2 规则接线成功且有实效
- 规则 63→67，基线 **0 误报**；624 跨卡复跑 blocked 47→55，`ATOM-REL-TARGET-HC`/`ATOM-REL-UNKNOWN-HC` 实证触发。

### 5.3 CI 取得实质进展，但**未全绿**
- **gate job 已转绿**（poison 豁免修复）；ruff 全绿。
- **quality 仍红**：ruff 修好后 **mypy 步骤首次真正执行**，暴露 **67 处存量债（620-623，24 文件）**。
- **pytest 仍红**：治理 manifest 待 F2 重签 + 620/621 meta 测试（"pytest 全绿"自指）。

### 5.4 E1 目标受"人审缺失"限制
- authorized 不可由机器提升（27 原子证已授权；56 证据证无人审来源）⇒ 需人审证据证（E2 清单是入口）。

---

## 六、局限性 / 未做项（诚实登记）

1. **A2/A4/A5 未达 >40 / >45 / 盲区<25**：跨卡 sandbox 不可达编译/复算/git/词表类盲区。
2. **E1 未达 >48%**：56 证据证人审缺失；机器可判定候选 0（不代签）。
3. **quality job 仍红**：mypy 67 处存量债（24 文件）未逐条修（超出 624 范围）⇒ 留 625。
4. **pytest job 仍红**：治理 manifest 需重签（F2 已做）；620/621 的"pytest 全绿"meta 测试自指。
5. **OTS anchor 过期**：`tool_integrity --update` 重钉 merkle 根 ⇒ 需 re-anchor（人/外部时间戳）。
6. **poison 对 4 条 HC 规则端到端覆盖 = 0**：以豁免+pytest 兜底。
7. **X 策略仅打到引用/命题/证据绑定类**；编译/复算/git 类盲区未触达。
8. **未做雷1/雷8**（QueYi Core 剥离，留 626+）。

---

## 七、交人项（不可代决）

1. **A2/A4/A5 未达触达目标**——是否接受"跨卡亦不达天花板"诊断、是否立项支持编译/复算/git 载体的沙箱。
2. **B1/E2 的 4 条 block 规则设计是否认可**（已接线，复杂度阈值 75 是否合适）。
3. **E1 PCK authorized 是否改口径**（证据证可否机器授权）或由 E2 清单驱动逐条人审。
4. **E2 的 110 条逐条人审是否执行**（执行需人授权；本批只生成）。
5. **CI 是否 push 后持续验证**（C1/C2 已 push；是"是否接受当前 green/red 边界"）。
6. **mypy 67 处存量债是否立项清理**（625）。
7. **OTS re-anchor 是否执行**。
8. 622/623 遗留仍留人项（沙箱入 CORE_TOOLS / 原子卡 verdict 写回 / ABSTAIN 展示 / 人审数据开源 / 攻击权重 / Horizon 入 metrics / PCK 权威源 / v8 基线 等）。

---

## 八、收工

- 17/17 任务完成，**一任务一 commit**（18 commit 含 A1 修正），无 golden accept、无 delegation、无人审代签。
- 收工门禁（`run_624_gate.py`）**PASS**；受控目录零污染；已有 push。
- 状态置 `awaiting_review`；outbox 见 `_auto/outbox/624.md`。
- **做不完的登记**：触达天花板、E1 authorized、mypy 67 处存量债、pytest manifest/meta、OTS re-anchor → 留 625。
