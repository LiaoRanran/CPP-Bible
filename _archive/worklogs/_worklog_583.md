# _worklog_583 · 知识资产层落地第一批：N5 等价变异体 + N1 四轴快照 + N3 换代影响面

> 任务书：`References/architecture_架构演进/583_苦力建设_知识资产层N5N1N3_只读视图与等价变异体.md`
> 规格来源：`_arch_v9/05_攻击生成系统化.md`（N5）· `_arch_v9/01_双时序账本.md`（N1）· `_arch_v9/03_换验证者交接契约.md`（N3）
> commit 链：`323600f`（任务0 修 580 遗留假红）→ `6549c8d`（N5）→ `89b1c56`（N1）→ `ca2b318`（N3）→ `cb49817`（任务0 收尾：SERIAL_EXTRA）
> 铁律遵守：判决路径**一行未改**；不加规则、不动 severity；不 golden accept、不 push；registry 全程只读。

---

## 〇、开工基线（任务 0，实测）

| 项 | 任务书基线 | 实测 | 判定 |
|---|---|---|---|
| HEAD | `f0bf657` 附近 | **`f0bf657`**（581 Task3） | ✓ |
| `tool_integrity --check` | exit 0 | `OK：5 个核心工具与基准一致` **exit 0** | ✓ |
| `gate --check` | 63 / 191 | `规则 63 条 · 命中 191 (block=0 warn=186 advice=5)` | ✓ |
| poison | 118/118 · RULE-COVERAGE 38/63 · 表观 103.2% / 诚实 60.3% · legacy 27 · exit 0 | 逐项一致（`-m tools.poison_drill` 亦可用，exit 0） | ✓ |
| replay | confirm=56 / refute=0 | `confirm=56 refute=0 infra_error=0` | ✓ |
| fast `-n auto` | exit 0 | **首次 exit 1**（见下"偏差 D1"）→ 修后 exit 0 | ⚠→✓ |
| `git status --short` 预存 M | `data/mutation/full_baseline_v4.json`、`v5.json`、`evidence/conc/EV-CONC-001.md` | 三项在，**未提交、未还原** | ✓ |

**侦察（按任务书"函数名以磁盘为准"）**：`_card_variants 592` · `_variant_index 749` · `classify 478` ·
`_report 635` · `MUTATORS 440` · `GATE_READ_KEYS 154` · `_findings_key 100` · `_snapshot 110`；
两解析器实测入口 **P1 = `atom_evidence_replay.parse_frontmatter`（仓内自写 YAML 子集解析器，*不是* PyYAML safe_load）**、
**P2 = `gate_engine._fm_hardening_uncached`（硬化四信号；`_UniqueKeyLoader` 是 `check_frontmatter_hardening()` 的
内嵌类，模块外取不到）** —— 任务书对 P1 的假设需更正（见偏差 D2）。

---

## 一、任务 1（N5）：`equivalent` 字段 + M6 八条定性

### 1.1 判据实现（`tools/mutation_fuzz.py`，只加不改）

```
equivalent(T, T') ⟺ P1 视角相同 ∧ P2 视角相同 ∧ 缩进信号相同 ∧ 正文逐字不变 ∧ op ∉ {M1, M7}
```
* `_frontmatter_text/_body_text`：切出 frontmatter 与正文（正文相等是**保守闸**：M6 的 flow 正则可能命中正文行）；
* `_canon`：键排序、去空白/注释差异，**不做跨类型归一**（`1` vs `true`、`"00000000"` vs `0` 是 556/557 走私信号）；
* `_p2_view`：按 gate 内嵌 loader 的**语义**最小复刻（SafeLoader + 重复键抛 `ConstructorError`），
  **配漂移护栏用例**（拿 gate 真实入口 `check_frontmatter_hardening()` 在临时沙箱上交叉核对：
  flow 形态零信号、重复键出 `[dup-key]`）；
* `equivalent_variant`：任一视角存疑即 `False`；**M1/M7 恒 False**（它们还读工件/命令，需 TCE，冻结）。

### 1.2 判别力（真形态表，`_probe583.py` 实测）

| 形态 | P1 同? | P2 同? | equivalent | 说明 |
|---|---|---|---|---|
| 重复键（**同值**） | True | **False** | **False** | ← 双解析器缺一不可的**正例**（P2 抛 `ConstructorError`） |
| 重复键（异值）/ 全角键名 / YAML1.1 类型陷阱 | False | False | **False** | 解析视角即分叉 |
| **块式 → flow（matrix）** | True | True | **True** | ← M6 逃逸的那一类（**等价变异体**） |
| flow → 块式 | True | True | **True** | 同上（反向） |
| 缩进提升（**嵌套子键**，2→3 空格） | True | True | **True** | 解析后同值且无硬化信号 ⇒ 等价（正确） |
| 缩进提升（**id 多缩一格**，真卡首行） | False | False | **False** | 结构走私（真卡上由 EV-FM-YAML-HARDENING 拦） |
| 正文被改 / 空操作 / 无 frontmatter | — | — | **False** | 保守面 |

### 1.3 机器验收（任务书 §1.3 五条）

| # | 验收 | 实测 |
|---|---|---|
| 1 | 加字段前后 5 字段逐字相等；三总数与 v5 权威一致 | **A/B 同输入**（判据开 vs 打桩恒 False）：`_variant_index` 逐条相等、三总数相等 ✓；全量 **989（严格 619）/ 9 / 185**，逐算子 `by_operator` 与 v5 **逐字相等** ✓ |
| 2 | **保守性自证**（防"把真逃逸洗成等价"） | 凡 `equivalent=True` 者 `new_block/new_warn` 必为空 ⇒ 自检通过（`--selfcheck-equivalent` 可复跑，违规 exit 2）；另有**反例测试**（伪造一条冲突记录 ⇒ 自检必须报错） |
| 3 | 双解析器缺一不可 | 见 §1.2 的"重复键（同值）"正例 + 漂移护栏用例 |
| 4 | 1183 变体四计数表 | 见下 |
| 5 | 两次跑一致 | `--selfcheck-determinism`（关键子集）✓ + 判据为纯函数（同输入同输出） |

**等价四计数（全量 jobs=4，`data/mutation/_583_eq.json`）**

| op | 变体 | **equivalent** | out_of_scope | malformed | 可判(blocked+escaped) |
|---|---|---|---|---|---|
| M1 | 92 | 0 | 0 | 0 | 65 |
| M2 | 195 | 0 | 27 | 0 | 168 |
| M3 | 107 | 0 | 42 | 0 | 65 |
| M4 | 233 | 0 | 0 | 0 | 200 |
| M5 | 85 | 0 | 0 | 0 | 29 |
| **M6** | 332 | **8** | 0 | 0 | 332 |
| M7 | 139 | 0 | 0 | 0 | 139 |
| 合计 | 1183 | **8** | 69 | 0 | 998 |

⇒ 8 条等价变异体**全部落在 M6**；M6 的 28 条 blocked 变体**零误标**（判别力证据）。

### 1.4 M6 八条逃逸定性（只读分析，未改任何判决）

| 卡 | 变异点 | 改的键 | 定性 |
|---|---|---|---|
| EV-HIST-001 / EV-MEM-032 / -033 / -034 / -035 / -036 / -037 / EV-UB-002 | 块式 → flow 写法（matrix） | `matrix` | **equivalent（无效变异：攻击集缺陷，非门禁洞）** |
| （M1）EV-CONC-001 | 删 negative_controls | — | 需 TCE/工件比对 ⇒ **冻结**（M1 走 replay，canon 不足以判） |

**结论（如实）**：**M6 那 8 条"逃逸"全部是等价变异体**——M6 把 `matrix:` 的块式映射改写成 flow 映射，
而仓内解析器与硬化解析器**都**把它解析成同一个 dict（`{compiler:..., stdlib:..., std:..., opt:..., arch:...}`），
硬化四信号也一条不变 ⇒ **任何只读 frontmatter 的规则都不可能给出不同 finding**。
**不是门禁缺规则，而是攻击集在制造无效变异**。⇒ 修法方向（**下一包**，本批不做）：让 M6 只变异"解析后确实不同"的形态，
或把 `equivalent` 计数从"变体总数"里单列（本批已单列）。

---

## 二、任务 2（N1）：`tools/prop_asof.py` 只读四轴快照

* 四轴来源：① 断言时间 = **卡的 git 提交时间**（字段名硬约束 `asserted_at_approx_from_card_commit`，
  **B 级证据**，报告顶部固定打印免责）② 验证者 = 卡面 `verified_by_oracle` × `data/oracle_registry.json`
  ③ 推翻 = `data/overturned_events.jsonl`（**可缺 ⇒ 0 事件，不报错**）④ 锚 = `propositions.db.anchor_source`（`mode=ro`）。
* 实测：**79 命题 / 27 命题所属卡 / 全库 83 张卡缺 `verified_by_oracle`（清单已列出，机器不代填）/ stale 0 /
  推翻事件 0（文件不存在）**。例：`ATOM-CONC-FENCE-001/prop-1 | observation | 2026-09-14T21:46:21 | missing | 0 | evidence`。
* 硬纪律：源码无写操作（唯一 subprocess = **只读 `git log`**）；命题库缺失 / git 不可用 ⇒ **fail-loud exit 2**（不返回空表）。
* 8 条 pytest：两次跑逐字同 / 只读静态断言 / 行数 == `prop_graph.stats()` / 字段名约束 / 两类 fail-loud / overturned 缺省 / 全库清单口径。

## 三、任务 3（N3）：`tools/oracle_rotation.py` 换代影响面

* 输出：① 卡面 vs registry 的不一致/缺失清单 ② **强制重验集合** ③ 换代后需重跑的**四份基线清单**
  （gate/replay/poison/mutation，**只列不跑**）④ 立场文案（继承默认 fail-closed；本批不实现继承/签名）。
* 实测：**83/83 张卡强制重验**（0 张卡填 oracle ⇒ 无法细分）；与 `metrics_collector.oracle_report()`
  **双实现对账：缺字段 83=83、stale 0=0、卡集合相同** ✓。
* registry 无 `judges`/`invalidates_on_change` ⇒ 报告显式写"无法细分 ⇒ 一律全体"，并给出**建议字段（不落盘）**。
* 7 条 pytest：对账 / 只读静态断言（无 subprocess、无判决入口）/ 两次跑一致 / registry 字节不变 /
  保守面文案 / 坏 `--to` exit 2 / JSON 载荷四段。

---

## 四、偏差表（任务书假设 X / 实测 Y）

| # | 任务书假设 | 实测 | 处置 |
|---|---|---|---|
| **D1** | fast `-n auto` 基线 exit 0 | **初始 exit 1**：`test_580_jobs1_equals_jobsN_everywhere` 的 `root_fingerprint_ok` 断言红。**与 579 同类**：该断言覆盖真实仓全树，`-n auto` 全套里被别的 worker 的**合法 replay**（删-重建真实工件）干扰 ⇒ 假红（单文件并行/串行/静默树全套均绿） | 按 579/580 先例补 `conftest.replay_serial`（**仅测试面**），独立 commit `323600f`；修后 fast exit 0（静默树复跑） |
| **D2** | P1 = PyYAML `safe_load` 路径 | **P1 实为仓内自写子集解析器**（`replay.parse_frontmatter`，`_parse_block`）；PyYAML 只在 **P2**（硬化 loader）里 | canon 按**真实入口**写（任务书本身要求"先 grep 确认再写 canon"）；P2 的 loader 是内嵌类 ⇒ 最小复刻 + 漂移护栏用例 |
| **D3** | v5 权威 = `989（严格 619）/9/185` | `full_baseline_v5.json` 文件里 `strict_blocked=**630**`、`replay_runs=64/replay_skipped=140`；而**新跑** = `619` / `65/139` | **归因**：619 才是清态值（579 两次跑、580 三方对账、本批全量均为 619；任务书自身也写 619）⇒ 文件里的 630 是 **578 时代"真实工件被变异"产生的幻影 strict**（正是 579 根隔离修掉的那类）。**未改文件**（任务书要求历轮预存 M 原样） |
| **D4** | 逐变体 5 字段"加字段前后完全相等" | 对 v5 文件对比出 926 条差异，**逐条查证后全部是 finding 串里的路径形态**：v5 是沙箱**绝对路径**、现在是**仓内相对形**（579 的 `_rel()` 有意变更）+ 目录分隔符 | 采纳更硬的证据替代：**A/B 同输入**（判据开/关）逐条相等（`test_583_equivalent_flag_does_not_change_verdicts`）；全量三总数/逐算子与权威一致 |
| **D5** | （新发现）`GATE_READ_KEYS` 是否覆盖读取面 | **`matrix` 不在 `GATE_READ_KEYS` 里**（M2 的"是否在门禁读取面"判据据此分类），但 `check_evidence_matrix()` 规则**确实读** `matrix` ⇒ M2 的 `out_of_scope` 分类对 matrix 类字段可能偏保守 | **不改**（会改 M2 分类=改判决口径）；写入交人清单 |
| **D6** | ruff 全仓 All checks passed | 本批改动文件**全绿**；全仓还剩 **6 条**，全在 581 的文件（`poison_drill.py` I001+2×E702、`test_poison_coverage_581.py` F401、`test_poison_exemptions_581.py` I001+F401） | 越界不修（581 已验收），列入交人清单 |

---

## 五、收工总验收（fresh，串行 poison/replay，退出码定论）

| # | 项 | 实测 | 判定 |
|---|---|---|---|
| 1 | `tool_integrity.py --check` | `OK：5 个核心工具与基准一致` **exit 0** | ✓（本批**未碰** CORE_TOOLS，故无需重钉——`mutation_fuzz`/`prop_asof`/`oracle_rotation`/`conftest` 都不在其中） |
| 2 | `gate_engine.py --check` | `规则 63 条 · 命中 191 (block=0 warn=186 advice=5)` | ✓ 与基线逐字不变（本批不加规则） |
| 3 | `poison_drill.py` | `118/118` + `RULE-COVERAGE 38/63` + `表观 103.2% / 诚实 60.3%` + `legacy 豁免 27` + `零覆盖攻击面：无` + **exit 0** | ✓ 与基线逐字不变 |
| 4 | `atom_evidence_replay.py --check` | `confirm=56 refute=0 infra_error=0` | ✓ |
| 5 | `pytest -m "not slow" -n auto` | **exit 0**（首轮 exit 1，红因见 D1；修正后复跑绿） | ✓ |
| 6 | `pytest -m slow -n0` | **exit 1，唯一失败 = 预期红 `test_golden_lock_json`**（warn 186 未 accept）；579/580 两模块已按 SERIAL_EXTRA 并入 slow 且**未出现在失败清单** | ✓ |
| 7 | 确定性 | `--selfcheck-determinism`（M6 子集 12 变体）**exit 0**：`✓ 确定性自检：两次跑逐变体一致` + `✓ 等价判据保守性自证`；另有 A/B 同输入（判据开/关）逐条相等用例 | ✓ |
| 8 | 受控目录 / 树 | `git diff --quiet -- atoms/ evidence/ Examples/` **exit 0**；`git status` 里本批产物 = 4 个 commit 涉及的文件 + `_worklog_583.md`（历轮预存 `full_baseline_v4/v5.json`、`EV-CONC-001.md` 原样保留，**未提交未还原**） | ✓ |
| 9 | ruff（本批改动文件） | `All checks passed!` | ✓（全仓余 6 条均在 581 文件，见 D6） |

**附：收工时刻的本批文件清单** —— `tools/mutation_fuzz.py`（仅报告层 +equivalent）、`tools/prop_asof.py`（新）、
`tools/oracle_rotation.py`（新）、`tests/test_mutation_equivalent_583.py`（新，12 例）、`tests/test_prop_asof_583.py`（新，8 例）、
`tests/test_oracle_rotation_583.py`（新，7 例）、`tests/test_mutation_parallel_580.py` + `tests/conftest.py`（测试卫生）、
产物 `data/mutation/_583_eq.json` 与 `data/mutation/m6_triage_583.json`（在 gitignore 的 `data/mutation/` 下，**不入 git**）。

## 六、交人清单

1. **M6 算子该修**（下一包）：本批证明那 8 条逃逸是**无效变异** ⇒ 让 M6 的 flow 变形只作用于"解析后确实不同"的形态
   （例如先做 `canon` 预检，等价则跳过并计入 `equivalent`），可让 M6 的可判分母从 332 收敛到 ~323。
2. **`GATE_READ_KEYS` 补 `matrix`**（M2 的读取面判据）：会影响 M2 的 `out_of_scope` 分类 ⇒ **需监工裁决**（改口径）。
3. **83 张卡的 `verified_by_oracle` 待填**（人/强模型的活）：填了之后 N3 的影响面才能从"全体"缩到"实际批"。
4. **推翻通道**至今 0 条事件（文件都不存在）：`escape_survival_batches` 仍无分母。
5. 581 遗留的 6 条 ruff（见 D6）。
6. N2/N4/N6（prop_closure 双实现 / MIS 出处锚 / α 花费区间）**未做**——按任务书留在后续包。
