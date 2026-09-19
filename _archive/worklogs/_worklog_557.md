# _worklog_557 · 人审解锁（L4 校准引擎第一块）+ L1 验证网补密 + 影响闭包

> 任务书：`References/architecture_架构演进/557_投喂词_人审解锁L4校准引擎第一块_warn分桶排序_L1补密Viso毒样例_M3区间_影响闭包.md`
> 解释器：`.venv\Scripts\python.exe`（有 PyYAML）。铁律：不 push / 不 --no-verify / **绝不 golden accept** / 存量零误伤。

---

## §0 开工基线（实测，`.venv\Scripts\python.exe`）

| 项 | 实测 |
|---|---|
| `gate_engine.py --check` | **规则 61 · 命中 141（block=0 warn=136 advice=5）** |
| `poison_drill.py` | **96/96**，status=pass，unknown=[]，覆盖 11/11 |
| `atom_evidence_replay.py --check` | **confirm=56 refute=0 infra_error=0** |
| `pytest -m "not slow" --collect-only` | **310 个测试点**（fast 组）；实跑全绿 |
| `git status`（受控） | 仅 pre-existing `evidence/conc/EV-CONC-001.md M` 与未跟踪 `tools/env_check.py`（非本批所改） |

### warn 分布（实测，按规则 id；**注：与提示词清单口径不同**）

| 规则 | warn | advice | 合计 |
|---|---|---|---|
| ATOM-CLAIM-CONCEPT-NORMALIZED | 77 | 0 | 77 |
| INFERENCE-NOT-MACHINE-VERIFIED | 28 | 0 | 28 |
| EV-MATRIX-UNBACKED | 16 | 0 | 16 |
| EV-OUT-UNDECLARED-KEY | 6 | 0 | 6 |
| EV-FALSIFICATION-QUANT | 4 | 0 | 4 |
| EV-ASSERT-SYMBOL-MAPPED | 2 | 1 | 3 |
| ATOM-REL-TARGET | 2 | 0 | 2 |
| EV-ENV-DEPENDENT-KEY | 0 | 2 | 2 |
| EV-OUT-STALE-MTIME | 0 | 2 | 2 |
| EV-SERVES-EXIST | 1 | 0 | 1 |
| **合计** | **136** | **5** | **141** |

---

## 偏差表（提示词假设 X / 磁盘实测 Y）

| # | 提示词假设 | 磁盘实测 | 处置 |
|---|---|---|---|
| D1 | Part 0#4「warn 按规则 id 的分布」列出 10 项（含 EV-ASSERT-SYMBOL-MAPPED 3、EV-ENV-DEPENDENT-KEY 2、EV-OUT-STALE-MTIME 2），并另记「5 条 advice」 | 该 10 项之和 = **141**，实为 **warn+advice 合计**；纯 warn 仅 **136**（其中 EV-ASSERT-SYMBOL-MAPPED=2 warn+1 advice；EV-ENV-DEPENDENT-KEY / EV-OUT-STALE-MTIME 全为 **advice**） | 分桶口径取**非 block 命中 = 141**，并在报告显式给出 warn/advice 拆分；桶③按提示词含 advice 类规则，故必须含 advice |
| D2 | Part A 目标「只看约 15 条真信号」 | 实测桶③ = **27 条**（含 7 条 `EV-MATRIX-UNBACKED` 的 (b) 真信号） | 如实报 27；桶③内部已按权重排序给出人审顺序 |
| D3 | 收工#1「四桶计数之和 == warn 总数」 | 因桶③含 advice 类规则 ⇒ 四桶之和 == **非 block 命中 141**（warn 136 + advice 5） | 报告同时给 `n_nonblock / n_warn / n_advice`，两种口径均可对账 |
| D4 | Part A A2 排序「KIL 高 × 首次出现 × 可证伪性」 | 全仓 `\bKIL\b` 仅命中 References 文档，**无 KIL 数据**；亦无「首次出现」历史 | 用**规则权重 + 卡 id** 兜底排序（确定性），报告注明「KIL 数据缺失，兜底排序」 |
| D5 | Part B「`tests/poison/` 加毒样例」 | 磁盘**无** `tests/poison/` 目录；毒样例**内联**在 `tools/poison_drill.py::drill()`（P43b/c 先例） | 依磁盘惯例内联新增（B2 已照此；B1 同） |
| D6 | Part B B1「poison 全过且**覆盖分子同步增加**」 | `RULE-COVERAGE` 分子只数 **gate 规则**（`ge.RULES`）；nc 判决是 **replay 路径字符串**、非 gate 规则 ⇒ N1–N7 **不会**增加该分子 | 如实报「分子不变（36/61）」；N1–N7 的覆盖应由 533 §2.5 的**双指标**（trap_block_rate/clean_pass_rate）另立计数器 |

---

## Part A · 人审经济学（P0）—— 纯读，零规则改动

**交付**：新增 `tools/review_triage.py`（四桶分桶器 + `--review-order` + `--json`）+ `tests/test_review_triage.py`（6 例，fast）；`.gitignore` 加 `/data/review/`（大 JSON 不入库）。
**运行**：`.venv\Scripts\python.exe tools\review_triage.py`（摘要）/ `--json`（落 `data/review/triage_<gitshort>.json`）/ `--review-order`（桶③人审顺序）。

### A1/A3 四桶对账表（实测，commit=35f3cc2）

| 桶 | 计数 | 规则明细 | 语义 |
|---|---|---|---|
| ① 迁移过程债 | **105** | ATOM-CLAIM-CONCEPT-NORMALIZED ×77、INFERENCE-NOT-MACHINE-VERIFIED ×28 | 新规则上线后的**存量迁移信号**，随回填/人签清零，**非内容退化** |
| ② 规则设计待甄别 | **9** | EV-MATRIX-UNBACKED（(a) 刻意排除 actual） | 规则预期：锚落在被刻意排除段 |
| ③ 真信号 | **27** | 见下 | 人必须逐条看 |
| ④ 已登记豁免/重复 | **0** | `golden_state.json` 无 `warn_classify`（无已分类）；无完全重复 | — |
| **合计** | **141** | == 非 block 命中（warn 136 + advice 5） | **对账一致，不漏不重** |

### A1 桶②逐条定性（`EV-MATRIX-UNBACKED` 16 条 → (a)9 / (b)7）

证据口径：规则实现 `gate_engine.py::check_evidence_matrix_backed` 只用 `.out 路径 / run #号 / 10+ 位数字` 三锚，且**刻意排除 `actual:`/`artifact_sha256:` 段**（`_raw_without_actual`，L948-973，A3①：声明不是留痕）。判定 = 把被排除段算进来是否就 ≥2 锚：

- **(a) 设计预期（留桶②，9 条）**：`EV-CONC-001`(body=1 excl=2)、`EV-CONC-002`(1/2)、`EV-CONC-006`(1/1)、`EV-LANG-001`(1/1)、`EV-LANG-002`(1/1)、`EV-MEM-001`(0/2)、`EV-MEM-039`(1/1)、`EV-MEM-042`(1/1)、`EV-MEM-043`(1/1)
  ⇒ 卡的留痕锚在 `actual`（声明段）里，规则**按设计**不认 ⇒ **建议登记豁免或细化规则措辞**（若"actual 里的 .out 也算留痕"是期望语义，则应改规则口径）。
- **(b) 真信号（转桶③，7 条）**：`EV-CONC-003`(0/1)、`EV-CONC-004`(0/1)、`EV-CONC-005`(0/1)、`EV-MEM-040`(0/0)、`EV-MEM-041`(0/0)、`EV-MEM-044`(0/0)、`EV-MEM-045`(1/0)
  ⇒ 即便算上被排除段仍 **<2 锚** ⇒ **卡确实缺两处可核对留痕 → 真信号**（补双平台 .out / 双 CI run / ::notice::+其一，或写明标准条文）。

> 注意：`golden_lock --classify` 是**按规则**落一桶（每规则只准一桶），而 `EV-MATRIX-UNBACKED` 内含 (a)/(b) 两类 ⇒ **无法在单规则分类里表达**。建议（人裁决二选一）：① 先修 7 张 (b) 卡，再把该规则整体落 `accepted`；② 或认定"actual 锚应算"是设计缺陷 ⇒ 落 `false_positive`（改规则口径）。**本工具不代选。**

### A2 桶③人审顺序（KIL 缺失，规则权重 + 卡 id 兜底；确定性，同输入同输出）

权重序（高→低）：EV-OUT-UNDECLARED-KEY 90 → EV-MATRIX-UNBACKED(b) 85 → EV-FALSIFICATION-QUANT 80 → EV-ASSERT-SYMBOL-MAPPED 70 → ATOM-REL-TARGET 60 → EV-ENV-DEPENDENT-KEY 50 → EV-OUT-STALE-MTIME 40 → EV-SERVES-EXIST 30。

| # | 规则 | 卡 | 为何真信号 / 建议动作 |
|---|---|---|---|
| 1-6 | EV-OUT-UNDECLARED-KEY | EV-CONC-002/003/004/005/006、EV-LANG-002 | `.out` 读数键未在 `run_match_keys` 声明 ⇒ 跨平台读数口径漏声明；补声明或删多余键 |
| 7-13 | EV-MATRIX-UNBACKED (b) | EV-CONC-003/004/005、EV-MEM-040/041/044/045 | 多编译器声明却无可核对留痕（处处 <2 锚）⇒ 补留痕或改声明 |
| 14-17 | EV-FALSIFICATION-QUANT | EV-HIST-001、EV-MEM-003/006/010 | 证伪对照缺量化取值 ⇒ 判据不可复算（伪证伪） |
| 18-20 | EV-ASSERT-SYMBOL-MAPPED | EV-CONC-001(advice)、EV-MEM-017/035 | 断言文本定位不到 ⇒ 断言可能悬空 |
| 21-22 | ATOM-REL-TARGET | ATOM-UB-GRAY-001（×2） | relations 目标不存在 ⇒ 知识图断链（**注**：golden 历史 accept 记为 G5 迁移前债务） |
| 23-24 | EV-ENV-DEPENDENT-KEY | EV-CONC-003/004（advice） | 环境量进读数键 ⇒ 跨机不可复算 |
| 25-26 | EV-OUT-STALE-MTIME | EV-CONC-001/002（advice） | `.out` 比源夹具旧 ⇒ 疑似陈旧留痕 |
| 27 | EV-SERVES-EXIST | EV-MEM-001 | serves 指向的原子尚未锻造 ⇒ 若该原子按阶段门待批则属预期中间态 |

### A3 供人复制的 accept 命令（**仅建议；accept 执行权在监工，本工具任何情况下不得自行调用**）

理由里的数字取**本批实测终值**（非照抄提示词）：`warn_findings: 59 → 136`（+77 条，全库实测）。

```bash
# 建议（逐规则分类；数字须以你复跑 --check 的当期值为准）：
.venv\Scripts\python.exe tools/golden_lock.py check ^
  --accept "557 人审：warn 59→136 一次性分类留痕（136 warn = 桶①迁移债 105 + 桶②设计预期 9 + 桶③真信号 27 + 桶④ 0）" ^
  --classify "ATOM-CLAIM-CONCEPT-NORMALIZED=legacy,INFERENCE-NOT-MACHINE-VERIFIED=legacy,EV-OUT-UNDECLARED-KEY=real,EV-FALSIFICATION-QUANT=real,EV-ASSERT-SYMBOL-MAPPED=real,ATOM-REL-TARGET=legacy,EV-ENV-DEPENDENT-KEY=false_positive,EV-OUT-STALE-MTIME=false_positive,EV-SERVES-EXIST=legacy,EV-MATRIX-UNBACKED=<real|false_positive|accepted 三选一，见桶②>"
```
> `EV-MATRIX-UNBACKED` 的桶由人按桶②的 (a)/(b) 定性裁决（本工具不代选）。advice 类规则（EV-ENV-DEPENDENT-KEY / EV-OUT-STALE-MTIME）是否需分类取决于 `golden_lock` 是否把 advice 计入 warn 计量——请以 `golden_lock.py buckets` 实盘为准。

**红线自证**：本 Part 全程**未改 gate_engine 规则、未改卡、未 accept、未改 severity**（`git diff` 受控目录仅新增 `tools/review_triage.py`、`tests/test_review_triage.py`、`.gitignore` 一行）。

---

## Part B ·（P1）parser 跨键 YAML 陷阱定性（B2 已做）+ V-iso N1–N7（B1 未做，停点见末）

### B2 陷阱词 × 门禁键 实测矩阵（135 组合：9 键 × 15 陷阱）

探测口径：自定义 `parse_frontmatter` vs PyYAML `safe_load`，再看硬化层是否 block（沙箱隔离）。
**修前**：非分歧/同空 72 · 分歧且被拦 35 · **分歧且放行 28**（灰色态）。

| 键（门禁关心？） | 分歧且放行（修前） | 处置 |
|---|---|---|
| `id` / `verdict` / `status` / `artifact_sha256` | 0（全部经 `[parse-diverge]` 拦） | 已闭合（556 前） |
| `negative_controls` | 0（`[nc-form]` 拦） | 已闭合（556） |
| **`serves` / `command` / `relations`** | **21**（7 值 × 3 键） | **B2 补 `[type-diverge]` 拦下** |
| `hypothesis`（非门禁键） | 7 | **不硬化**（门禁不读 ⇒ 无害，已证安全） |

逐值（触发隐式类型的陷阱）：`00000000`→int 0、`on`/`off`→bool、`0x1F`→int、`1_000`→int、`.inf`→float、`12:30`→秒数（`yes/no/null/~` 两解析器**有时一致**或不产生非空 str，故未列入放行集）。

**修法（`gate_engine._fm_hardening_uncached`）**：新增 `[type-diverge]` block —— 对门禁键
`serves/command/relations`，当「自定义=非空字符串 且 safe_load=隐式标量(bool/int/float) **且
`str()` 不等**」时出 block（仅**语义**分歧才拦；`id: 3` 这类 str 相等的类型差异不拦，因 gate 自身按
`str().strip()` 比较、判决自洽）。rule_id 仍 `EV-FM-YAML-HARDENING`。

**零误伤实测**：`type-diverge` 全库命中 **0**；`gate --check` 仍 **规则 61 · 命中 141（block=0 warn=136 advice=5）**。
**毒样例**：`poison_drill` 新增 **P43f**（`command: 00000000` ⇒ `[type-diverge]` block），登记 `ATTACK_TYPES`（P43f→A6）；毒钻探 **97/97**，覆盖 11/11，RULE-COVERAGE **36/61 不变**；台账重写（96→97、A6 6→7）+ `tool_integrity --update` + T2 快照同步（仅 A6/drill 两项）。
**xfail 转正**：556 的 `test_non_gate_key_yaml11_trap_should_block`（hypothesis）→ **`..._is_harmless` 确定性通过**（断言分歧存在 + 门禁不读该键 ⇒ 无害），不留永久 xfail；另加 `test_gate_key_type_diverge_blocked`（serves/command/relations `00000000` 必 `[type-diverge]` block）。
**差分**：生成器并入 `serves/command/relations`；新增谓词 **P6**（门禁键的 YAML1.1 **语义**类型分歧必 block）。`test_no_gray_state_between_parsers` 连跑 4 次（不同 seed）全绿。

### B1 V-iso N1–N7 进 poison —— **未做（停点）**

原委：N1–N7 的**判决分支**已由 `tests/test_negative_controls.py`（10 例，替身编译器）全覆盖；
B1 要求的是**真实 sandbox + 真编译**的载荷化（533 §2.5 + 双指标 trap_block_rate/clean_pass_rate）。
本轮把预算用于 A（P0 主线）与 B2（零误伤已验证的硬化），**B1 未动**，按硬纪律停在此处、不留半成品。

**精确施工点（下次照做）**：
1. 位置：`tools/poison_drill.py::drill()`，在 P43f 之后新增 N1–N7（用现有 `sandbox()`；每个用例把
   阳夹具 / 阴夹具 / 阳面 `.asm` 写进 sandbox，再调 `replay.check_negative_controls(meta, workdir=…,
   env={}, art_path=…)` —— 签名见 `atom_evidence_replay.py:1183`，**真编译**）。
2. 七类构造与期望判决见 `_arch_v2_round2/533_V-iso施工规格.md` §2.5（N1 `negative_control_passed` /
   N2 `_diff`（reasons≥3）/ N3 `_broken`（**不得 infra**）/ N4 `_diff` / N5 `_missing` /
   N6 `_diff`（retain 缺 `while (!s_sf_b)`）/ N7 干净卡 confirm 不变 + B0 卡 flip verified）。
3. 载荷命名 `N1 …`–`N7 …`；**双指标**（533 §2.5）：`trap_block_rate`（N1–N6）与 `clean_pass_rate`（N7），
   任一 <100% 即红。注意现有 RULE-COVERAGE 只认 gate 规则字面量（nc 判决非 gate 规则）⇒ N1–N7
   **不进** RULE-COVERAGE 分子，需另立计数器（否则"覆盖分子同步增加"无从体现——与提示词假设不符，
   已记 D6）。
4. N7 的 B0 卡需用真实 `Examples/atoms/_atom_fence_vs_atomic.cpp(+.nc1.cpp)` 拷进 sandbox。

---

## Part D ·（P2）impact_analysis 多跳闭包 —— **未做**

---

## §收工总验收（fresh run，逐项实测）

| 判据 | 实测 |
|---|---|
| **Part A** | ✅ `review_triage.py` 四桶之和 **141 == 非 block 命中**（对账闭合、不漏不重）；桶②每条带 body/excluded 锚计数证据；桶③排序确定（`test_review_triage` 断言两次逐字一致）；`pytest tests/test_review_triage.py` **6/6 绿**；**全程无 accept、无 severity 改动、无卡改动**（`git diff` 受控目录仅新增该工具/测试/.gitignore） |
| **Part B（B2）** | ✅ 陷阱词×键矩阵落盘（135 组合，见上）；`[type-diverge]` 硬化 zero-false-positive（全库 0 命中）；毒样例 P43f；xfail **转确定性通过**（hypothesis 已证无害）；poison **97/97**、覆盖 11/11、RULE-COVERAGE 36/61（分子不变，口径见 D6） |
| **Part B（B1）** | ⏸ **未做**（停点 + 精确施工点已列上节） |
| **Part C / Part D** | ⏸ 未做 |
| `gate --check` | ✅ **规则 61 · 命中 141（block=0 warn=136 advice=5）**——与开工逐字一致 |
| `replay --check` | ✅ **confirm=56 refute=0 infra_error=0** |
| `pytest -m "not slow" -n auto` | ✅ **连续 2 轮全绿**（另：收工途中一度出现 `test_observability` 3 例假红，根因是本批 `review_triage` import 期改 `CPPBIBLE_OBS` 污染同进程环境，已修 `aa6cdb6` 后连跑全绿） |
| `pytest -m slow -n0` | ✅ 除 **pre-existing `test_golden_lock_json`** 外全绿（deselect 后 100%） |
| 受控目录 | ✅ 零污染（仅 pre-existing `EV-CONC-001.md M` 与未跟踪 `tools/env_check.py`） |

### 本批 commit（不 push）
`5e2ab73`（Part A 分桶器）→ `d26bd42`（Part B2 type-diverge + xfail 转正）→ `aa6cdb6`（Part A-fix：修 env 污染假红）。

### 待监工裁决
1. `golden_lock` warn 59→136 的**逐规则分类签署**（Part A 已产可复制命令与建议分类表；`EV-MATRIX-UNBACKED` 的桶由人按桶②(a)/(b) 定性三选一）——accept 权唯人，本批未代签。
2. Part B1（V-iso N1–N7 真编译毒载荷）与 Part C/D 的排期。
