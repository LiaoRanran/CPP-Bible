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
**施工点（待执行，未落码）：**
1. `drill()` 内：新增模块全局 `_LAST_BEHAVIORAL_COVERED: set | None = None`；drill 开头置 `set()`；每个载荷算完 `ok` 后，若 `ok` 则 `_LAST_BEHAVIORAL_COVERED |= set(who)`（只收运行时 who 实含且通过的规则 ID）。
2. 新增 `behavioral_covered() -> set`：若 `_LAST_BEHAVIORAL_COVERED is None` 则跑一次 `drill()` 填充后返回；否则直接返回（避免 `__main__` 双跑）。
3. 改写 `rule_coverage()`：`cov = behavioral_covered()`；`uncovered = sorted(all_rules - cov - set(load_exemptions()))`；返回 `(len(cov), len(all_rules), uncovered)`。
4. **ghost 自检**：`rule_coverage()` 内扫源码 `"([A-Z][A-Z0-9-]+)" in who` 得 `text_claimed`，`ghosts = text_claimed - {r.id for r in RULES}`；非空则 `print` 警告（防评论/字符串再污染，对应 hole A 的"自检"要求）。
5. 改掉误导注释：1559/1615/1837 三处"RULE-COVERAGE 正则只认字面量 'RULE-ID' in who、勿参数化" → 改为"覆盖以运行时 who 实含为准；静态文本仅作 ghost 自检，不再计入分子"。`rule_coverage` docstring（2126）同步更新。
6. `__main__`（2264）改：`covered, total, uncovered = rule_coverage()` 保持调用顺序即可（rule_coverage 内部跑 drill 填 `_LAST_BEHAVIORAL_COVERED`，随后 2271 的 `drill()` 不再双跑——见下）。⚠ 当前 `__main__` 先 `rule_coverage()` 后 `drill()`；改造后 `rule_coverage()` 已跑 drill，故把 2271 的 `passed,total_d,failures = drill()` 改为读取已填充的全局（或直接复用），**避免钻探跑两遍**。具体：让 `rule_coverage()` 返回前顺带把 `drill()` 的结果存到全局 `_LAST_DRILL`，`__main__` 取 `_LAST_DRILL` 而非再调 `drill()`。
7. 新增回归锁 `tests/test_poison_coverage_581.py`：
   - (a) `drill()` 后断言 `behavioral_covered() ⊆ RULES`（无 ghost 进分子）；`len(behavioral_covered()) == len(behavioral_covered() & RULES)`。
   - (b) 源码 `"X" in who` 但非 RULES 的死文本 == 0（ghost 自检红）。
   - (c) 注入 1 行注释文本，`behavioral_covered()` 不应涨（防回归 hole A）——实现：复制源码注入 `# ok = "FAKE-GHOST-581" in who` 到临时模块并 import，断言 covered 不变。
8. 验收：重跑 `python -m tools.poison_drill` → RULE-COVERAGE 应显示 **37/63**（幽灵消失）；`python tools/tool_integrity.py --check` exit 0；新 pytest 通过。
**commit**：`poison_drill.py` + `tools/.tool_checksums`（--update 重钉）+ `tests/test_poison_coverage_581.py`。

## 任务 2（hole B）：豁免二人锁 + legacy 单列 + 机器核原因
**施工点（待执行）：**
1. `poison_exemptions.yaml` 结构升级（保持 `_EXEMPT_LINE` 零依赖解析兼容）：每条加字段 `redteam_seen`（红队真见过该攻击面，bool），存量 27 条**全部标 `redteam_seen: legacy`**（严守"严禁编造 redteam_seen"；legacy 表示历史存量、未见证）。
2. `load_exemptions()` 解析 `redteam_seen`；返回结构可带该字段。`rule_coverage()` 在 uncovered 计算外，另输出"豁免中 redteam_seen=legacy 条数"（仅统计，不阻断）。
3. 机器核原因：沿用 0.3 脚本逻辑落 `reason_verified` 字段（backed/missing-test/weak-test），写入 `poison_surface_map.json`（build_surface_map 增加 `exemptions` 段：{id, legacy, reason_verified, cited_tests}）。
4. 新增报告：`print_coverage_report()`（或扩 `--by-type`）输出两张表：① 规则覆盖率（行为级 covered / 63）② 27 豁免逐条核验（id · legacy · reason_verified · 测试名）。诚实显示"覆盖率掉就掉"——若某豁免被移除且无人补载荷，covered 自然下降，不补假载荷。
**commit**：`poison_exemptions.yaml` + `poison_drill.py`（load_exemptions/build_surface_map 扩展）+ `.tool_checksums`。

## 任务 3：重钉 + 测试 + 自证门
**施工点（待执行）：**
1. 每改完一个 CORE_TOOLS 任务，跑 `python tools/tool_integrity.py --update` 重钉 `.tool_checksums`，同 commit。
2. 全量自测：`python -m tools.poison_drill`（RULE-COVERAGE 37/63、118/118）、`python tools/tool_integrity.py --check` exit 0、`pytest tests/test_poison_coverage_581.py -q` 通过。
3. 验收门（任务书）：覆盖率不可伪造（hole A/B 封死）、豁免有见证/机器可核（legacy 诚实单列）、不降判决可信度。**不 push、不 golden accept。**

---
## 当前进度
- ✅ 第 0 步：基线实测 + PoC-2 复现 + covered 对账（37 真实/1 幽灵）+ 27 豁免三桶（7/12/8）→ 本 worklog。
- ⏳ 任务 1/2/3：施工点已在上文逐条列清，待一任务一 commit 执行。
