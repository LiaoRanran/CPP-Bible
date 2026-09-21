# 619 批次独立验收报告（CodeBuddy）

> 角色：独立监工。只跑检查 + 写本报告；不写源码、不改任何东西、不 commit、不 push。
> 验收对象：619 批次（commits bfc5fcd~d2f412b，13 任务，7 个新工具，57 例单测自报）
> 仓库根：`C:\CodeLearnling\note\note\C++\CPP-Bible`
> 解释器：`.venv\Scripts\python.exe`
> 验收完成 HEAD：`git rev-list --count HEAD` = 1553
> 验收日期：2026-09-21

---

## 一、四道监工门禁

| 门禁 | exit code | 关键输出 | 与基线一致？ |
|---|---|---|---|
| tool_integrity | 0 | 5 核心工具 + 5 信任根 + Merkle + 10 尺子全 OK | 一致 ✅ |
| gate | **1** | 规则 63 · 命中 **195**（block=**2** warn=188 advice=5） | **不一致 ❌**（基线 191 / block=0） |
| poison | 0 | 124/124；RULE-COVERAGE 39/63；表观 100%；诚实 95.2% | 一致 ✅ |
| replay | 0 | confirm=56 refute=0 infra_error=0 | 一致 ✅ |

**说明**：
- `tool_integrity` / `poison` / `replay` 三项与基线完全一致（poison 124/124、replay 56/0/0 均复现）。
- `gate` **失败（exit 1）**，且出现 **2 条 BLOCK 级违规**，命中也从基线 191 升到 195：
  - `EV-ARTIFACT-FILE-EXISTS` @ `evidence/conc/EV-CONC-003.md`：卡声明的工件 `Examples/atoms/_atom_lock_cost.asm` 不存在。
  - `EV-ARTIFACT-FILE-EXISTS` @ `evidence/conc/EV-CONC-004.md`：同上。
  - 即：619 冻结基线声称 `gate block=0`，但当前活体 gate 已出现 2 条 block。这是本次验收最关键的回归信号。

---

## 二、受控目录污染

```powershell
git diff --quiet -- atoms evidence Examples Book   →   EXIT:0
```

**结果：零污染 ✅**（无未提交改动落到受控目录）。

---

## 三、新工具 --check

| 工具 | exit code | 关键输出 |
|---|---|---|
| adversarial_objective_619 | 0 | A1 selftest: PASS |
| adversarial_attacker_619 | 0 | A2 selftest: PASS |
| vfdr_619 | 0 | A3 selftest: PASS |
| pck_certificate_verifier_619 | 0 | B2 selftest: PASS |
| pck_pilot_generator_619 | 0 | B3 selftest: PASS |
| pck_renderer_619 | 0 | B4 selftest: PASS |
| snapshot_manifest | 0 | snapshot_manifest --check: PASS |

**结果：7/7 --check 全部通过 ✅**

---

## 四、新单测

```powershell
.venv\Scripts\python.exe -m pytest tests/test_619_a1.py tests/test_619_a2.py tests/test_619_a3.py `
  tests/test_619_b2.py tests/test_619_b3.py tests/test_619_b4.py tests/test_619_gate.py -v
```

- **收集 53 个测试项，53 passed，0 failed，0 skipped ✅**
- 各文件函数数：a1=12, a2=7, a3=8, b2=9, b3=5, b4=5, gate=7 → 合计 53。
- **与自报不一致**：619 验收报告 §三 写「pytest（619 新增单测）✅ 57 例全绿」，但其任务清单 §一 逐任务累加（12+7+8+9+5+5+7=53）与本次实测均为 **53**，不是 57。属自报计数误差；功能结果仍为全绿，无失败。

---

## 五、代码审查

### tools/adversarial_objective_619.py（A1）
- 只读性：纯函数、`--check` 不写盘；仅 `--baseline` 读盘。✅
- `--check` 完整性：覆盖权重和=1、4 子目标可计算、确定性、真逃逸>warn_only、n_a 不进分母、warn_only 不双计、帕累托含真逃逸、summarize。✅（仅用 4 条合成记录，未跑真实 1593 条，但 `--check` 应快，可接受）
- 单测：12 例，覆盖 W1/W2、n_a、equivalent、边界。✅
- 硬编码：`WEIGHTS`/`GENERIC_RULES`/`PROVENANCE_TIERS` 为领域常量，已在 `data/adversarial_objective_619.md` 记录。✅
- 结论：**PASS**

### tools/adversarial_attacker_619.py（A2）
- 只读性：`--check` 只读；`main()`（无 `--check`）会写 `data/adversarial_attacker_619.md`，属 data/ 目录（非受控目录），符合 619「不写受控目录」硬边界。✅
- `--check` 完整性：用 4 条 mini 基线验证 top20/帕累托/n_a 剔除/契约；**未验证真实 1593 条上的 W1=57、W2=1 排名**（需读大文件）。头条结论需运行 `main` 才可见。⚠ 小问题
- 单测：7 例。✅
- 错误处理：`escape_rank` 对空结果返回 None，已处理；纯只读分析，fail-closed 不适用。✅
- 与自报一致：独立复现 W1=57/1406、W2=1（见第七节）。✅
- 结论：**PASS（小问题：--check 未覆盖头条排名声明）**

### tools/vfdr_619.py（A3）
- 只读性：纯状态机，`--check` 不写盘；`main()` 写 `data/vfdr_619.md`（data/）。✅
- `--check` 完整性：覆盖合法转移、非法转移拒绝、确定性、三历史教训达 CLOSED、history 4 步、`OPEN+FIX_SHIPPED` 抛错。✅
- 单测：8 例。✅
- 错误处理：`transition()` 对非法转移抛 `ValueError`（fail-closed，拒绝而非放行）。✅
- 结论：**PASS**

### tools/pck_certificate_verifier_619.py（B2）
- 只读性：`load_cert` 读盘、`validate_cert` 纯函数；`--check` 不写盘。✅
- `--check` 完整性：覆盖合法证书 ok、单验证器/批量授权注释、非法捕获 schema_version/evidence/claim.type/cs_upper_bound/provenance.commit、顶层非 mapping 拒绝。✅
- 单测：9 例。✅
- 错误处理：结构错误一律 `ok=False`（fail-closed，绝不给畸形证书开绿灯）。✅
- 与自报一致：独立对 10 张试点证书验证 → 10/10 PASS（见第七节）。✅
- 结论：**PASS**

### tools/pck_pilot_generator_619.py（B3）
- 只读性：只读 `atoms/evidence/`，`--check` 不写盘；`main()` 写 `data/pck_pilot/*.yaml` 与 `data/pck_pilot_619.md`（均 data/，非受控目录）。**未写受控目录** ✅
- `--check` 完整性：检查 10 张试点卡路径存在、样本过 B2、单验证器注释、负向测试存在。⚠ 「样本含负向测试」仅断言 `len>=0`（恒真），校验偏弱。
- 单测：5 例。✅ 但单测偏弱（负向测试断言恒真）。
- 硬编码：`PILOT_CARDS` 列表、`CS_UPPER=0.009062` 硬编码（后者为 616 冻结 estimand L1 上界，文档化；可从 manifest 取，属小改进点）。⚠
- 错误处理（潜在）：`negative_tests[].result` 直接取 `r.get("verdict")`，但 B2 允许的 result 集合为 `{blocked,escaped,n_a}`；若某卡在 v7 中有 `warn_only`/`strict` 等 verdict，生成的证书会被 B2 判 FAIL。当前 10/10 通过 ⇒ 全部 verdict 落在允许集，暂无触发。⚠ 潜在边界
- 与自报一致：10/10 复现。✅
- 结论：**PASS（小问题：selftest 断言偏弱、CS_UPPER 硬编码、负向测试 verdict 域未收敛）**

### tools/pck_renderer_619.py（B4）
- 只读性：读盘 + 纯渲染；`--check` 不写盘。✅
- `--check` 完整性：覆盖标题/PASS 徽标/诚实注释/批量授权/负向表/FAIL 徽标/结构错误列出。✅
- 单测：5 例。✅
- 错误处理：畸形证书仍渲染但显式标 FAIL + 列出错误（诚实，非隐藏）。✅
- 结论：**PASS**

### tools/snapshot_manifest.py（C1）
- 只读性：`--check` 只读自验证；`main()` 写 `data/SNAPSHOT_MANIFEST.json`（data/）。✅
- `--check` 完整性：覆盖字段齐全、live_counts 正、gate hits=block+warn+advice、mutation 数学、poison passed=total、replay confirm>0、JSON 可序列化。✅
- 错误处理：`--check-clean` 在工作树脏时拒绝快照（fail-closed）。✅
- **重大一致性问题**：`FROZEN_VERIFICATION` 中 `gate: hits=191, block=0, warn=186, advice=5` **仍为 616 冻结基线**，但本次实跑活体 gate = 195 命中 / **2 block**。即该「权威」manifest 所称 `block=0` 已被 619 时代的 2 条 BLOCK 违规推翻。619 因硬边界「不跑监工门禁」而未察觉此漂移。❗
- 结论：**PASS（大问题：冻结基线 gate.block=0 与活体 2 block 矛盾，权威 manifest 已失准）**

---

## 六、数字核对

| 数字 | 619 自报 | 我重算 | 一致？ |
|---|---|---|---|
| 总 commit 数 | 1550 | **1553** | ❌（+3，疑 HEAD 在自报后前进） |
| 工具数 | 232 | **233** | ❌（+1） |
| 测试数 | 225 | **225** | ✅ |
| 原子卡 | 28 | **28** | ✅（自报注：实际卡 27，1 个非卡） |
| 证据卡 | 56 | **56** | ✅（EV-*.md；目录含 README.md 故总 57 含 README） |
| 619 新工具 | 7 | **7** | ✅ |
| 619 新单测 | 57 | **53** | ❌（自报 §三 写 57，但其 §一 逐任务累加与 pytest 实测均为 53） |
| PCK 试点证书 | 10 | **10** | ✅ |
| gate 规则/命中 | 63/191 | **63/195** | ❌（活体 block=2，基线 block=0） |
| poison | 124/124 | **124/124** | ✅ |
| replay | 56/0/0 | **56/0/0** | ✅ |

重算方法（实跑）：
- commit：`git rev-list --count HEAD` → 1553
- 工具：`(Get-ChildItem tools/*.py).Count` → 233
- 测试：`(Get-ChildItem tests/test_*.py).Count` → 225
- 原子卡：`(Get-ChildItem atoms -Recurse -Filter *.md).Count` → 28
- 证据卡：`(Get-ChildItem evidence -Recurse -Filter EV-*.md).Count` → 56

---

## 七、诚实性检查

1. **有没有编造数据**：抽查 3 个具体数字，独立验证均真实——
   - 「A2 真逃逸 W1 排 57/1406」：实跑 `adversarial_attacker_619.analyze` → `escape_rank=57, n_ranked=1406` ✅
   - 「replay confirm=56」：实跑 `atom_evidence_replay.py --check` → confirm=56 ✅
   - 「poison 124/124」：实跑 `poison_drill.py` → 124/124 ✅
   - 未见编造。自报与实跑的小差异（commits 1550→1553、tools 232→233、619 新单测 57→53）均为计数/HEAD 漂移，非捏造。

2. **有没有偷偷跑监工门禁**：619 验收报告 §二/§三 明确声明「未跑监工门禁」，且 `snapshot_manifest` 冻结基线仍停在 `gate block=0`（若 619 跑过 gate 应看到 2 block 并修/更新）。**无违反证据 ✅**。注：正因未跑，才没发现下面第 7 条的回归。

3. **A2 排名可复现性**：
   - W1（0.40/0.25/0.20/0.15）→ escape_rank=**57**/1406 ✅ 复现
   - W2（文档定义 0.50/0.20/0.15/0.15）→ escape_rank=**1**/1406 ✅ 复现（Top1 = `evidence/conc/EV-CONC-001.md` M1，composite=0.500）
   - 自报「W1 排 57、W2 排第 1」**完全可复现**。

4. **PCK 试点证书验证**：独立对 `data/pck_pilot/*.yaml` 逐张跑 B2 验证器 → **10/10 PASS**（ATOM-CONC-FENCE-001、ATOM-CONC-LOCK-001、ATOM-HIST-AUTOPTR-001、ATOM-LANG-INLINE-001、ATOM-MEM-LEAK-001、EV-CONC-001、EV-CONC-002、EV-HIST-001、EV-LANG-001、EV-MEM-001）。✅ 复现。

**诚实性结论：通过 ✅**（自报头条可复现，无捏造；小计数误差已列出）

---

## 八、验收结论

1. **总体结论**：**PASS with minor issues**（功能与诚实性通过；但存在 1 个需 620 前修复的 gate 回归 + 若干小计数偏差）
2. **四道门禁**：3 绿 1 红 —— `gate` **红（exit 1，2 BLOCK）**；tool_integrity / poison / replay 全绿
3. **新工具**：7/7 --check 通过
4. **单测**：全绿（53 例实测通过；自报 57 为计数误差）
5. **代码审查问题清单（按严重程度）**：
   - 🔴 **[gate 回归]** `evidence/conc/EV-CONC-003.md`、`EV-CONC-004.md` 引用不存在的工件 `Examples/atoms/_atom_lock_cost.asm`，触发 2 条 `EV-ARTIFACT-FILE-EXISTS` BLOCK，推翻冻结基线 `block=0`。
   - 🟠 **[权威 manifest 失准]** `snapshot_manifest.py` 的 `FROZEN_VERIFICATION` 仍记 `gate hits=191/block=0`，与活体 195/2 block 矛盾；README/qmd 引用此 manifest 会读到错误门禁数。
   - 🟡 **[B3 selftest 偏弱]** 「样本含负向测试」断言 `len>=0`（恒真）；`CS_UPPER` 硬编码；`negative_tests.result` 未收敛到 B2 允许域（潜在越界）。
   - 🟡 **[A2 --check 不覆盖头条]** 头条 W1=57/W2=1 排名未在 `--check` 内验证（需跑 `main` 读 1593 条）。
   - 🟡 **[自报计数误差]** 619 报告 §三 写 57 例单测（实际 53）；commits 1550→1553、tools 232→233 与 HEAD 漂移（均非功能问题）。
6. **数字核对**：一致 7 项（测试225、原子28、证据56、新工具7、PCK10、poison、replay）；**不一致 4 项**（commits、tools、619 新单测、gate 命中/block）。
7. **诚实性**：通过（头条声明全部独立复现，无捏造）。
8. **建议（620 开工前须修复）**：
   - **必修**：修复/补产 `Examples/atoms/_atom_lock_cost.asm`，消除 EV-CONC-003/004 的 2 条 BLOCK；使活体 gate 回到 `block=0`。
   - **必修**：重新生成 `data/SNAPSHOT_MANIFEST.json`（或从冻结段剔除已失准的 gate 数字），避免权威源误导。
   - **建议**：B3 收敛 `negative_tests.result` 取值域、将 `CS_UPPER` 改为从 manifest/基线读取；A2 在 `--check` 内加真实排名声明的最小断言。
   - **建议**：统一 619 单测计数口径（53 而非 57），并澄清 commits/tools 数字随 HEAD 漂移的引用时点。

---

> 本报告为独立验收方产出，仅记录如实结果，不代签任何决策（golden accept / 人审等）。

---

## 更正附录（2026-09-21，620 开工复测后追加，原作者 = 本报告作者）

**被更正的结论**：原报告 §八 将「EV-CONC-003/004 引入 2 条 BLOCK 级 gate 违规（block 0→2）」
列为 🔴 必修项，并据此判定「冻结基线 block=0 被推翻」「snapshot_manifest 权威源失准」。

**更正结论**：上述判定**不成立**。稳态下 `gate_engine --check` =
**63 规则 / 191 命中 / block=0 / warn=186 / advice=5**（连跑 3 次一致，exit 0），
与冻结基线逐字一致；`snapshot_manifest` 的 FROZEN_VERIFICATION **未失准**。

**更正依据（证据链）**：
1. `Examples/atoms/_atom_lock_cost.asm` 实际存在（28190 字节）且已被 git 跟踪；
2. 两卡 `artifact` 引用与磁盘路径逐字一致，`artifact_sha256` 与 replay 独立重编译结果逐字相符；
3. 该文件 `LastWriteTime = 2026/9/21 22:44:25`——恰在本次验收会话期间，
   由 `atom_evidence_replay.py --check` 的 recompile 步骤「删旧写新」重写；
4. 本次验收将 `gate_engine --check` 与 `atom_evidence_replay --check` **并行**发起，
   gate 采样到 replay 重编译「删旧未写新」的窗口 ⇒ 瞬时误报。
   EV-CONC-003/004 共用同一工件，故一次竞态同时命中两卡（191→195 = +2 BLOCK +2 WARN）。

**受影响条目**：
- §一 gate 行：应为「一致 ✅（block=0）」，非「不一致 ❌」；
- §五 snapshot_manifest「大问题：冻结基线 block=0 与活体 2 block 矛盾」→ 撤销；
- §六 数字核对「gate 63/191 vs 63/195」→ 应为 63/191 一致；
- §八 问题清单 🔴🟠 两条 → 撤销（保留 🟡 各项小问题）。
- §八 建议「必修：修复 EV-CONC-003/004」→ 撤销（详见 `data/620_block_fix_report.md`）。

**仍然成立的原报告结论**：受控目录零污染、7 个新工具 --check 全过、
单测实测 53 例全绿（自报 57 为计数误差）、poison 124/124、replay 56/0/0、
A2 排名 W1=57/1406 与 W2=1 可复现、PCK 试点 10/10 PASS、诚实性通过。

**教训**：监工门禁之间**不可并发执行**（gate 与 replay 会争抢同一工件文件）。
后续验收须串行执行并对 gate 多次复跑确认稳定性。
