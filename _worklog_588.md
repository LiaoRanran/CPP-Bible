# _worklog_588 · 变异发现器完备性（matrix 尾注释收口 + 全算子形态审计）

## 开工基线（0.3，fresh 实跑，2026-09-19）
- tool_integrity --check exit 0
- gate `--check`：**规则 63 · 命中 191（block=0 warn=186 advice=5）** ✓
- poison：**124/124**，RULE-COVERAGE 39/63，表观 100%(63/63) · 诚实 95.2%(60/63)
- replay：confirm=56 refute=0 infra_error=0
- mutation 权威文件 `data/mutation/full_baseline_v5.json`（逐算子）：M1 64/1/27 · M2 168/0/27 · M3 65/0/42 · M4 200/0/33 · M5 29/0/56 · M6 709/0/0 · M7 139/0/0
  （格式：blocked/escaped/n_a；总 variants=1568 blocked=1374 escaped=1 n_a=185 equivalent_invalid=8 strict=784）

## 任务 0（commit 81f7cbc）审计脚本 + 台账 + 测试
- 新增 `tools/mutation_shape_audit.py`（只读/幂等，导入真实 `MUTATORS`/`_mut_matrix_values` 测「现正则能否变异」）
- 台账 `data/mutation_shape_coverage.md`（**修前快照**）
- 0a 结论：含 matrix 块卡 **56** 张；**matrix 键行尾注释漏网 1 张 = `evidence/mem/EV-MEM-004.md`**（能产/含 = 55/56），
  现正则 `^(matrix:)\s*\n` 撞 `#` 失配 ⇒ 整块 0 变体
- 0b 结论：全算子×形态覆盖表；矩阵尾注释为**唯一漏网**；值行尾注释（ATOM-MEM-LEAK-001 为真实卡例）/全角括号/
  command 尾注释/actual 项尾注释/id 尾注释均无漏（真实 MUTATOR 实跑 n>0）
- 0c 结论：全库 **LF 83 / CRLF 0 / 混合 0**；LF/CRLF 同构对拍（BASE+EV-MEM-004，各 MUTATORS）变体集逐字一致
- 测试 `tests/test_mutation_shape_588.py`：幂等 + 纯只读 + 宽容探测 EV-MEM-004 + CRLF 不变（4 条全绿）

## 任务 1（commit 62db051）修 M6 matrix 键行尾注释 + 块内注释行
- `_mut_matrix_values` 键行正则放宽为 `^matrix:[ \t]*(?:#[^\n]*)?\r?\n`（覆盖 `matrix:` / 尾注释 / CRLF）；
  块体改「连续缩进行」`(?:[ \t]+[^\n]*\r?\n)+`，遇顶格键自然终止；遍历**先剥尾注释再解析键**
- **CRLF 自省**：旧式 `\s*\n` 的 `\s` 吞 `\r` 本 CRLF 安全；本批收紧为 `[ \t]` 后若不补 `\r?` 会引入 CRLF 回归
  ⇒ 显式补 `\r?`（回归测试 `test_m6_matrix_crlf_eq_lf` 锁死）
- 回归测试 4 条：尾注释卡现产 7 变体、块内注释含冒号不误当键、干净卡变体集不变、CRLF==LF
- 全量 M6（--cards all --limit 999 --operators M6 --jobs 4）：变体 **717→724**（+7=EV-MEM-004 的 3 删键+4 非法值），
  blocked **709→716**，**escaped 仍 0**；删键→EV-MATRIX block、非法值→587 值校验 warn；零新增逃逸、无洗 equivalent

## 任务 2（本轮）GATE_READ_KEYS 补 matrix + classify 显式失效 gate 盘缓存
- `GATE_READ_KEYS` 补 `"matrix"`：`check_evidence_matrix` 真读 matrix 块，此前漏列 = 与 571 `actual` 同类
  「把没问记成不适用」的尺子不诚实
- **产出零影响（deterministic 锁）**：`test_gateradkeys_matrix_no_effect_on_m2m3_output` 逐 83 卡证明
  mut_m2/mut_m3 产出**不因 matrix 在/不在 GATE_READ_KEYS 改变**
- 顺带修 `classify` / `_card_variants`：写变体 / 还原后显式 `ge.invalidate_meta`，消除
  `(path, mtime_ns, size)` 等长同 tick 撞键导致的假 verdict（memory 早已预警的坑）
- 全量实测（--cards all --limit 999 --operators M2,M3）：blocked **206**（M2 141 + M3 65）· escaped **0** · equivalent **27**
- **27 条 equivalent（M2）定性（经监工独立复现更正）**：清 replay manifest 后全量 `--jobs 4` **连跑两次**
  并与已提交 `full_baseline_v6.json` **三方逐变体比对 = 1593 条 0 差异**；**M2 稳定 blocked=141 / equivalent=27 / n_a=27**，
  **不存在 blocked↔equivalent 抖动**。那 27 条经解剖是 **M2 正则命中 frontmatter 注释行内的示意路径**
  （如 EV-CONC-001 第 17 行的注释命令）：P1/P2 canon 相同、正文逐字不变 ⇒ 等价判据**正确剔除**，不进可判分母。
  **141 是正确值，无「真值 168」**。
  ⚠️ **更正记录**：初稿曾把早期一次「无-matrix 配置 233 vs 有-matrix 配置 206」之差误读为
  "ge.run 盘缓存 / 并行池残留陈旧态的非确定性抖动"并登记交人 —— **该交人条目已作废删除**
  （三方逐变体比对 + `--selfcheck-determinism` 均证判定是确定的）。
- 未动 gate/replay/poison；mutation_fuzz 非 CORE ⇒ 无需 tool_integrity 重钉

## 任务 3（本轮）CRLF 健壮性 + 其余漏网收口
- **3.1 CRLF**：全库 83 卡 × 全 7 算子 LF/CRLF（归一 `\r`）对拍，**查实 M3 在 14 张卡上产出不一致**
  （`mut_m3` 两处 `(?=\n)` 前瞻 + 手工 `+1` 删行：CRLF 下前瞻撞 `\r` 失配 ⇒ 变体不产；
  且即便补前瞻，`+1` 只吃 `\r` 会留空行）。修法：正则改**消费**整行行尾 `\r?\n`，删行不再手工 `+1`
  （LF 行为逐字不变）。修后全库 × 全算子 CRLF 对拍 **0 差异**。
  全量 M3 核验：blocked=65 / escaped=0 / n_a=42 —— **与修前逐字一致**（零 LF 回归）。
- **3.2 其余漏网（本批共 2 条，≤3 达标）**：
  ① M6 matrix 键行尾注释（EV-MEM-004）—— 任务 1 已修；
  ② **M4 `artifact_assert:` 键行尾注释**（同类、任务 3 新发现）：锚定正则
     `^(\s*)artifact_assert:\s*$` 无尾注释位 ⇒ 全库 **6 张**（EV-HIST-001 / EV-MEM-001/002/004 /
     EV-UB-001/002）**整块 0 变体**（此前被记成 n_a，把"没问到"记成了"不适用"）。已修为
     `[ \t]*(?:#[^\n]*)?\r?\n`（消费行尾、兼容 CRLF、允许尾注释）。
  发现手段：**通用尾注释漏网探测器**（剥掉全库每张卡的键行尾注释后再跑各算子，凡"剥后变体更多"
  即被藏起来的变体）—— 全库扫得仅 M4 命中（6 卡 0→4），M1/M2/M3/M5/M6/M7 无隐藏。
- **量效（全量 M4）**：变体 233→251，blocked **200→224**（+24 = 6 卡 × 4 注入，**全 strict 拦截**），
  n_a 33→27，**escaped 仍 0**；24 条新变体无一逃逸 ⇒ 无需交人条目。
- 回归锁：`test_all_mutators_crlf_eq_lf_over_corpus`（全库全算子 CRLF）、
  `test_m4_artifact_assert_tail_comment`、`test_m4_lf_path_unchanged`

## 任务 4（本轮）收工总验收（全套 fresh 实跑 + 退出码）
- **v6 基线重冻结** `data/mutation/full_baseline_v6.json`（跑前已清 `build/replay_manifest.json`）：
  变体 **1593** · blocked **1378**（严格 811）· **escaped = 1** · n_a 179 · malformed 0 · equivalent 35
  可判分母 **1379** · 逃逸率 **1/1379**；逐算子（可判 = blocked+escaped，n_a 单列）：
  | 算子 | 可判 | 严格 | 逃逸 | n_a |
  |---|---|---|---|---|
  | M1 | 65 | 64 | **1（EV-CONC-001 冻结 TCE）** | 27 |
  | M2 | 141 | 0 | 0 | 27 |
  | M3 | 65 | 5 | 0 | 42 |
  | M4 | **224**（588 修 +24） | 224 | 0 | 27 |
  | M5 | 29 | 0 | 0 | 56 |
  | M6 | **716**（588 修 +7） | 379 | 0 | 0 |
  | M7 | 139 | 139 | 0 | 0 |
  M5 提示可判 29 < 59（样本不足，未宣称逃逸率上界）；equivalent=35（8 条 M6 block→flow + 27 条 M2 注释行内示意路径变体，等价判据正确剔除，见任务 2）
- 两个 selfcheck：`--selfcheck-determinism` exit **0**（关键子集 M1/M6/M7 两次逐变体一致）；
  `--selfcheck-equivalent` exit **0**（所有 equivalent 的 new_block/new_warn 均空）
- gate `--check`：**规则 63 · 命中 191 (block=0 warn=186 advice=5)** —— 与开工逐字不变 ✓
- poison：**124/124** · RULE-COVERAGE 39/63 · 表观 100% · 诚实 95.2%（逐字不变）✓
- 台账/快照零 diff：`git diff --quiet -- tools/poison_surface_map.json tests/__snapshots__` exit **0** ✓
- 受控目录零污染：`git diff --quiet -- evidence atoms Examples Book` exit **0** ✓
  （两条 CRLF 假脏 full_baseline_v4.json / EV-CONC-001.md 全程未提交未还原，仍在）
- fast 套件 `pytest -m "not slow" -n auto`：**450 passed / 1 skipped / exit 0**
  （首跑 1 例 `test_gate_summary_counts` 失败 = `-n auto` 并发窗口假红，串行单跑 5 snapshots 全绿、重跑 exit 0）
- slow 套件 `pytest -m slow -n0`：**333 passed / 1 failed**，唯一红 = `test_golden_lock_json`
  （`golden_lock check` = `warn_findings: 136 → 186` 恶化，**预存在待人工 accept 状态，与 588 无关**；
   gate 63/191 未变、replay confirm 56/infra 0）—— 即任务书「**slow 仅 golden 预期红**」

## 588 交人条目（不在本批处理）
1. M5 可判样本 29 < 59：要宣称「逃逸率 ≤5%@95%」需补样（既有提示，非 588 新增）。

（原第 1 条「verdict 分类非确定性 / 需专门修缓存一致性」经监工独立复现**证伪**——三方逐变体比对 1593 条 0 差异，
M2 稳定 141/27/27；**已作废删除**，见任务 2 更正记录。）

