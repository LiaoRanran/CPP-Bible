# 581 施工日志 · 苦力：覆盖率不可伪造（行为级 covered + 豁免二人锁）

- 开工：2026-09-18 ｜ HEAD = `0da17b2c794911f00da31323d8ce42a28c84260f`
- 角色：建设者（本任务书明确授权改 `poison_drill.py`、跑 `tool_integrity.py --update`、一任务一 commit）
- 纪律：不改任何卡、不碰 580 的 `--jobs` 与 mutation 判决、不 golden accept、不 push；诚实覆盖率掉就如实掉，严禁编造 redteam_seen / 补假载荷。
- 交付物：`_arch_v8/` 报告（见下）+ 本 worklog + 代码改动分任务 commit。

---

## 第 0 步 · 基线实测（先实跑，不抄任务书/564；数字以实跑为准）

### 0.1 基线数字（2026-09-18，`.venv` Python 3.13.13，32 核）
| 项 | 命令 | 结果 |
|---|---|---|
| git HEAD | `git rev-parse HEAD` | `0da17b2c794911f00da31323d8ce42a28c84260f` |
| gate 规则数 | `gate_engine --check` | 63 规则 · 命中 191（block=0 warn=186 advice=5） |
| 毒样例覆盖 | `python -m tools.poison_drill` 末尾 | **RULE-COVERAGE 38/63**，uncovered=0；118/118 制衡层有效；零覆盖攻击面：无 |
| 工具完整性 | `python tools/tool_integrity.py --check` | OK（5 核心工具与基准一致） |
| **PoC-2 复现** | `python _arch_v7/probes/poc2_poison_self_attest.py` | ✅ 两洞当红：<br>[A] 注入 0 真载荷、仅 1 行文本 → covered 新增 `FAKE-COVERAGE-NO-PAYLOAD` ✓<br>[B] 自写豁免 → `load_exemptions` 接受、移出 uncovered ✓ |

> 注：跑 `poison_drill` / `tool_integrity --check` 未污染正式目录（`git status` 仅显示开工前既存的修改，无新增 M/?? 于 atoms/evidence/Examples/tools/tests）。**之前 580 调研跑全量 pytest 套件会 `git checkout` 冲掉未提交编辑的破坏性副作用，与本条 CLI 无关。**

### 0.2 covered 逐条对账（脚本 `_t581/s0_covered.py`，只读）
- `rule_coverage()` 返回 covered=38；但源码 `"X" in who` 命中 38，其中 **1 个是幽灵**：`RULE-ID`（非规则 ID，来自 1559/1615/1837 三处**注释**文本 `"RULE-ID" in who` 被正则抓到）。⇒ **真实 covered = 37**。
- 豁免数学：`63 − 37（真实covered）− 27（豁免）= −1` ⇒ **`ATOM-REL-DAG` 是冗余豁免**（已被真实载荷覆盖，豁免台账里重复计）。
- 结论：当前 covered 含 1 幽灵、豁免含 1 冗余；行为级改造后 covered 应收敛到 37（幽灵消失），`ATOM-REL-DAG` 豁免保留但标 legacy（冗余无害）。

### 0.3 存量 27 条豁免分三桶（脚本 `_t581/s0_exempt.py`，机器核；reason 提 `test_*` 名 → tests/ 查 `def` 存在 + 该测试文件是否真含 rule_id 字符串）
| 桶 | 条数 | 条目 |
|---|---|---|
| **backed**（测试存在且真断言该规则） | 7 | ATOM-AUDIENCE, ATOM-FM-REQUIRED, ATOM-MISCONCEPTION-LEVELS, ATOM-REL-DAG, ATOM-STATUS-VALUE, EV-MATRIX, MIS-LIBRARY |
| **missing-test**（reason 未点名任何 `test_*`，仅说"pytest 任务X 已补"） | 12 | ATOM-NO-UNVERIFIED, ATOM-REL-TARGET, ATOM-SUPERIORITY-WORDS, EV-FM-REQUIRED, EV-SERVES-EXIST, HUMAN-GOLDEN-REVIEW, HYBRID-TEACHING-DEPTH, LLM-SUPERIORITY-QUALITY, PED-MISCONCEPTION, PED-MOTIVATION, PED-PREDICT-FIRST, PED-SOCRATIC |
| **weak-test**（测试存在但源码未断言该 rule_id） | 8 | ATOM-DAL-MATCH, ATOM-GRAY-ZONE, ATOM-ID-FORMAT, ATOM-MISCONCEPTION-REF, ATOM-PREREQ-READABLE, ATOM-STATUS-TRANSITION, DOC-ZERO-PLACEHOLDER, META-MANIFEST |
| **unverifiable 合计** | **20** | 12 + 8 |

> 诚实口径声明：weak-test 的判定是"测试文件源码未出现该 rule_id 字符串"。个别测试可能用常量引用/间接方式断言，故 weak 是**强信号非绝对**；按任务书口径仍落 weak 桶，不自行拔高成 backed。所有 27 条 id 均指向真实规则（EXEMPT_NON_RULE_ID=[]，无幽灵豁免）。

### 0.4 与任务书假设的偏差（诚实记，不遮）
| 任务书假设 | 实跑 | 处置 |
|---|---|---|
| covered 36/61（引 564） | **38/63**（真实 37，含 1 幽灵） | 以实跑为准；改造后报 37 |
| 27 豁免 = 63−36 | 真实 37 covered + 27 豁免 = 64 ≠ 63 | 因 1 冗余豁免（ATOM-REL-DAG），改造后修正口径 |
| "ghost 自检预计 0 或极少" | 找到 1 个真幽灵 `RULE-ID` | 改造后 ghost 自检必须报 0 |
| "missing/weak 占多数" | 20/27 unverifiable | ✓ 印证 |
| 存量豁免无冗余 | 发现 1 冗余（ATOM-REL-DAG） | 标 legacy，不动逻辑 |

---

## 任务 1（hole A）：covered 从"源码文本 grep"改为"运行时行为收集"
**状态：✅ 已落码并验证（commit 见下）**

### 落地要点
1. `drill()`：新增模块全局 `_CUR_WHO`（set）/ `_LAST_BEHAVIORAL_COVERED` / `_LAST_DRILL`；drill 开头置空；新增 `_CovList(list)`，每次 `append` 时若 `ok` 则 `_LAST_BEHAVIORAL_COVERED |= set(_CUR_WHO)`（只收运行时 who 实含且通过的规则 ID）。
2. 新增 `_mk_who(iterable)`：集中把 `_CUR_WHO` 维护为 set 并返回 `sorted`（修掉早期 `_CUR_WHO` 变 list 导致 `|= set` 类型错误的坑）；所有 `who = _mk_who(...)` 调用（~37 处）与 `_static_who`/`_atom_who` helper（`globals()['_CUR_WHO'] = set(...)`）统一写 `_CUR_WHO`。
3. 新增 `behavioral_covered()`：`_LAST_BEHAVIORAL_COVERED is None` 则跑 `drill()` 填充分享给 `__main__`，避免双跑；`rule_coverage()` 改用 `behavioral_covered()` 作分子。
4. **ghost 自检**：`rule_coverage()` 扫源码 `"([A-Z][A-Z0-9-]+)" in who`，`ghosts = text_claimed - 注册规则`；非空则 `print` 警告（不计入分子）。
5. `__main__`：`rule_coverage()` 内部已跑 drill 并把 `(passed,total,failures)` 存 `_LAST_DRILL`，`__main__` 直接取 `_LAST_DRILL` 不重跑。

### ⚠ 实现中发现的真实 bug（行为级收集漏洞，非规则漏打）
3 个探针计算 `who` 时**未走 `_mk_who`、也未写 `_CUR_WHO`**，导致 `results.append` 时 `_CUR_WHO` 是上一层残留值 → 这 3 条真实命中的规则被漏收（drill 实测 118/118 全过，证明它们合法覆盖）：
- **P17**：`who = {f.rule_id for f in ge.check_evidence_id_unique()}` → 改 `who = _mk_who(...)`；
- **P71**：`_who71 = {f"{rule_id}/{sev}"...}` → append 前置 `_CUR_WHO = {f.rule_id for f in _fs71}`；
- **P72**：`_who72 = {...}` → append 前置 `_CUR_WHO = {f.rule_id for f in _fs72}`。
修前行为级 = 35（比文本 37 还低）；修后 = **38**（详见下）。

### 实测验收（2026-09-18，`.venv`）
- `python -m tools.poison_drill` → **RULE-COVERAGE 38/63**；`118/118 制衡层有效`；`零覆盖攻击面：无`；`未覆盖且未豁免：无`；**EXIT=0**.
- 比文本 grep 的 37 更准：行为级**多抓到 2 条文本漏计的真实覆盖** `ATOM-DAL-MATCH`、`ATOM-STATUS-TRANSITION`（其 `who` 检查走 `ok = not who`/其它模式，文本正则没抓到）。仅 `ATOM-REL-DAG` 仍是"文本有但行为级无"——但它已在豁免台账（冗余豁免，见 0.4），不影响门禁。
- `tool_integrity --check` exit 0（改完已 `--update` 重钉 `.tool_checksums`）。
- `pytest tests/test_poison_coverage_581.py -v` → **3 passed (13.31s)**：(a) behavioral ⊆ RULES；(b) 源码死文本 ghost == 0；(c) 注入 `# ok="FAKE-GHOST-581" in who` 后 covered 不涨、FAKE-GHOST-581 不进分子（临时模块 ROOT 钉回仓库根以隔离路径错位假失败）。

**commit**：`tools/poison_drill.py` + `tools/.tool_checksums`（--update 重钉）+ `tests/test_poison_coverage_581.py`。

## 任务 2（hole B）：豁免二人锁 + legacy 单列 + 机器核原因
**状态：✅ 已落码并验证（commit 见下）**

### 落地要点
1. `poison_exemptions.yaml`：27 条全部加 `redteam_seen: legacy`（脚本精确替换 `date: ...}` → `date: ..., redteam_seen: legacy}`，验证 27 条命中，无替签）。
2. `load_exemptions()`：
   - `_EXEMPT_LINE` 正则加可选组 `(?:,\s*redteam_seen:\s*(\S+))?`；返回 `dict[id, dict]`（date/reason/redteam_seen/reason_verified）。
   - **fail-closed**：`date > 2026-09-18` 且缺 `redteam_seen` ⇒ 该条**排除出豁免台账**（规则回到 uncovered，不静默放行）。
   - 存量（date<=2026-09-18）无签名 ⇒ 归 `legacy`（单列、诚实口径不计入，不静默删除）。
3. `verify_exemption_reason(rule_id, reason)`（新增，581 把"豁免≠免检"变机器闸）：
   - 从 reason 抽 `test_*` 名 → 在 `tests/` 找 `def test_*` → 是否存在且文件源码含 `rule_id` 字符串；
   - 返回 `backed` / `missing-test`（测试不存在或没点名任何 test） / `weak-test`（测试在但未断言该 rule_id）。
4. `coverage_report()`（新增）：算**表观/诚实**双口径 + `legacy_exempt` / `unverifiable` 单列（防只报好看的那个）。
5. `build_surface_map`：**新增顶层键 `exemption_lock`**（含 behavioral_covered / signed_exempt / legacy_exempt / unverifiable / apparent / honest），**不动 `rule_coverage` 子字典** ⇒ 既有 syrupy 快照零破坏（task 3 也据此不更新快照）。
6. `__main__`：打印表观/诚实双口径、27 条 legacy 单列、20 条 unverifiable 点名（含桶别）；JSON 输出加 `exemption_lock`。

### 实测验收（2026-09-18，`.venv`）
- `python -m tools.poison_drill` → RULE-COVERAGE **38/63**（27 豁免）；
  **表观覆盖率 103.2%**（38 行为 + 0 签核 + 27 legacy / 63，含与 covered 重叠的冗余豁免 ATOM-REL-DAG，故 >100% 即要暴露的虚高）；
  **诚实覆盖率 60.3%**（38 行为 + 0 签核 / 63，legacy 不计入已覆盖）；
  **20 条背书不可核验被点名**（weak-test 8 + missing-test 12）。
- **机器核验独立复现 0.3 三桶结果**（非硬编码）：backed=7 / missing-test=12 / weak-test=8（合计 27）。
- `pytest tests/test_poison_exemptions_581.py -q` → **9 passed**：反例1（新豁免无签名→仍 uncovered，fail-closed）、反例2（reason 点名不存在测试→unverifiable 点名）、正例（带合法 redteam_seen→移出 uncovered）、27 全 legacy 锁、双口径可算、三桶计数吻合。
- 既有快照/相关测试全过：`test_output_snapshots.py`（5 快照）、`test_poison_attack_type.py`、`test_poison_coverage_581.py` 无回归；`tool_integrity --check` OK。
- 注：`test_golden_lock_json` 失败与本任务无关（golden_lock 工具，任务书要求"不 golden accept"，属预存状态，未触碰）。

**commit**：`tools/poison_exemptions.yaml` + `tools/poison_drill.py` + `tools/.tool_checksums`（--update 重钉）+ `tools/poison_surface_map.json`（--write-surface-map 落盘，含 exemption_lock）+ `tests/test_poison_exemptions_581.py` + `tests/conftest.py`（两新测试模块加入 SLOW_MODULES 串行）。

## 任务 3：重钉 + 测试 + 自证门
**施工点（待执行）：**
1. 每改完一个 CORE_TOOLS 任务，跑 `python tools/tool_integrity.py --update` 重钉 `.tool_checksums`，同 commit。
2. 全量自测：`python -m tools.poison_drill`（RULE-COVERAGE 37/63、118/118）、`python tools/tool_integrity.py --check` exit 0、`pytest tests/test_poison_coverage_581.py -q` 通过。
3. 验收门（任务书）：覆盖率不可伪造（hole A/B 封死）、豁免有见证/机器可核（legacy 诚实单列）、不降判决可信度。**不 push、不 golden accept。**

---
## 当前进度
- ✅ 第 0 步：基线实测 + PoC-2 复现 + covered 对账 + 27 豁免三桶（7/12/8）→ 本 worklog。
- ✅ **任务 1（hole A）**：行为级 covered 落地，实测 RULE-COVERAGE **38/63**、118/118、EXIT=0；回归锁 `tests/test_poison_coverage_581.py` 3 passed；已一任务一 commit（poison_drill.py + .tool_checksums + 测试）。
- ✅ **任务 2（hole B）**：豁免二人锁 + legacy 单列 + 机器核原因落地，实测表观 103.2% / 诚实 60.3%（legacy 不计入）、20 条不可核验背书点名；机器核验复现三桶 7/12/8；回归锁 `tests/test_poison_exemptions_581.py` 9 passed；已一任务一 commit。
- ⏳ 任务 3：重钉 + 全量自测 + 验收门 → 待执行。
