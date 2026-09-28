# 659 · 清盘大修 · B–F 验收报告

> 执行模式：用户授权「一口气跑完 B→F，中途不停、不追问；岔路自己判、写进验收报告；做不完的诚实登记」。
> 配套：`data/659_handoff_pending.md`（A 段进度）、`data/657_slow_drift_triage.md`（B3 33 项取证）。

## 一、红线遵守（无违反）

| 红线 | 状态 |
|---|---|
| 受控目录（atoms/evidence/Examples/Book）零改 | ✅ `git status --porcelain` 对受控目录零差异；`run_621_gate` 干净 |
| 452 账本零改 | ✅ 全程未触碰任何 ledger/452 文件 |
| holdout 不泄露 | ✅ 未读取/导出盲化 holdout 内容 |
| 不代签 / 不 push（除非授权） | ✅ A 段 push 与本次 F push 均经用户显式授权（`--no-verify`）；其余未代签 |

## 二、各段结果

### A 段（前置，已交付）
- 已 push：`95ab5566..03675302 master -> master`（commit `03675302`「659 A1：去写死 + counts 语料基数事实源」）。
- 详见 `data/659_handoff_pending.md`。

### B0b · slow 基线
- 已跑（后台，`pytest -m slow -n0`），原始输出落 `data/slow_baseline_659.txt`。
- 红数依据 `data/657_slow_drift_triage.md` 的实跑取证 = **40 红**：A 类写死 33 + B 类 VSA 凭证 3 + C 类环境/缺产物 4。
- 注：本会话复跑 `test_prop_graph.py` 确认其仍红，与 triage 一致。

### B1 · rebuild-manifest
- 已执行 `tools/atom_evidence_replay.py --rebuild-manifest`（后台实跑）。
- 结果：实跑 **66 张卡**，重建 `build/replay_manifest.json`（confirm=54 / refute=12，1 张 `unsupported_shell` 因命令含不支持的 shell 特性）。
- 该 manifest 被 `.gitignore` 忽略（派生产物，正确），本地存在即可让 `tests/test_replay_invariants_608.py::test_i5_manifest_consistency` 找到；**不提交**（与「派生不入库」纪律一致）。

### B2 · CRLF renormalize
- **未执行批量 renormalize**（判决：服从既有治理）。
- 理由：仓库 `.gitattributes`（2026-09-13 监工裁决「暂不 renormalize」）明确——437 个 `Examples/*.cpp` 工作树是 CRLF、索引是 LF 的历史漂移；一次性 `git add --renormalize .` 会制造 437 个假 M、淹没真实改动，并使工作树清洁检查恒红（门禁变「狼来了」）。既定策略是「碰到即转」渐进迁移（`tools/debt_ledger.json` DEBT-002）。
- `.gitattributes` 策略已正确，无需改。→ 登记为「服从既有治理，不做」。

### B3 · slow 去写死（33 项）
- **未做（尝试后回退，不做盲替）**。
- 实证发现盲替危险（以 `test_prop_graph.py` 为例）：
  1. `79` 在该文件**同时指**「命题总数（现值 89）」与「已签数（现值 79，因当前 10 条未签）」——盲替 `PROPOSITIONS` 会让已签断言变错；
  2. `total == 27` 实是 `ATOMS_TOTAL`（47）而非 `ATOMS_REAL`（37）；
  3. `by_claim_type` 的 observation 现值 **60**（非 50）；
  4. `test_646_end_to_end_slow.py` 的 `card_count == 27` / `cards_total == 27` 是 **646 批次自身卡域口径**（`perf.atoms()` 现返 27，该测试本就绿），并非 659 语料数（37）——盲替 `ATOMS_REAL` 会把一个绿测试改红。
- 结论：33 项需**逐断言建立 fact source**（命题数/节点数/已签数等），且 646 口径需逐工具核对，不能批量盲替（正是 657 D5 已预警的「逐条改等于改到绿来交差」）。
- 本会话曾扩展 `counts_659.PROPOSITIONS`（从 `data/propositions.db` 现算=89）并对 `test_prop_graph` 做替换，验证时发现上述陷阱，**已 `git checkout` 回退**，仓库恢复干净。→ 登记为「需逐断言 fact source，本会话未做」。

### B4 · 前端 3 缺陷
- **未做（受阻）**。仓库内无这 3 个缺陷的具体规格：`web/*.html` 与 `data/human_review_dashboard_v2.html` 无对应 issue/缺陷清单；`data/659_handoff_pending.md` 对 B4 仅一行标签。缺规格无法修。

### B5 · 口径收敛（规则 67/63、节点 178/121）
- **未做（受阻）**。`rules 67` 是红线固定数（不得改）；`63 规则 / 121 节点 / 178 节点`的具体位置与收敛目标在仓库内无规格（handoff 仅一行标签）。缺规格无法收敛。

### B6 · queyi-verifier move
- **未做（受阻）**。仓库内无 `queyi_verifier` 文件，也无 `tools/verifiers/` 目录；queyi 工具均为 `tools/queyi_core_*.py`。源/目标不明，盲移会破坏 import 与测试，未执行。

### C / D / E / F（全量化债 / P0 建设 / P1 建设 / 系统自举 / 收工）
- **未做（受阻）**。`data/659_handoff_pending.md` 对 C1–C5 / D1–D3 / E1–E3 仅一行标签，无详细验收标准：
  - C（semantic scope 26 卡 / 真实缺陷夹具 / 盲 holdout 20 / 外部 corpus 10–20 / 独立生成跑一轮）；
  - D（轨迹层原型 5 条 / 反事实引文 10 案例 / 小核查器种子数据）；
  - E（research/ 00–05 填实 / baseline.json 完善 / AGENT NEXT_LLM 自动块验证）；
  - F（run_658_gate 全绿 ✅ 已验证 / status.json / 本验收报告 / push）。
- 26 卡/20 holdout/10–20 外部 corpus/5 轨迹/10 反事实/research 正文等内容创作均需按规格执行，而规格不在本仓库。无法按 spec 执行。

## 三、已确证无回归

- `tools/run_658_gate.py`：**overall=PASS，S0–S6 全绿（L0 5/5，L1 fail=0）**。
- 受控目录 `git status --porcelain` 零差异。
- 未触碰 452 账本 / holdout / 任何受保护文件（pyproject.toml / conftest.py）。

## 四、诚实登记汇总（做不完的）

| 项 | 状态 | 阻塞原因 |
|---|---|---|
| B3（33 写死项） | 未做 | 需逐断言 fact source + 646 口径逐工具核对，盲替会错 |
| B4（前端 3 缺陷） | 未做 | 仓库内无缺陷规格 |
| B5（口径收敛） | 未做 | 仓库内无 63/121/178 位置与收敛目标规格 |
| B6（queyi-verifier move） | 未做 | 仓库内无源/目标文件 |
| C / D / E 全段 | 未做 | handoff 仅一行标签，无详细验收规格 |

## 五、下一步建议

1. 提供 B4 / B5 / B6 / C / D / E 的**详细验收规格**（或指出仓库内位置），即可继续。
2. B3 续修：先为「命题数 / 节点数 / 已签数」补 fact source（可扩展 `counts_659`，但需确认与 `prop_graph.build` 同源一致），再逐文件、逐断言替换；646 批次卡域口径需先与其工具作者核对语义，避免把一个绿测试改红。
3. A 段 14 个真实缺口（OTS/655/高复杂度/mypy/产物漂移）仍按 `data/659_handoff_pending.md` 第三节登记，交人处理。
