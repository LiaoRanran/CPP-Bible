# 581 · 苦力建设任务书：让 RULE-COVERAGE 不可伪造（行为级 covered + 豁免二人锁/legacy 单列）

> 执行者：苦力（弱模型/夜间好模型均可）。这是**建设轮**，允许改 `tools/`、`tests/`、`tools/poison_exemptions.yaml`、`tools/poison_surface_map.json`、`tools/.tool_checksums`；**不许改任何卡**（atoms/ evidence/ Examples/ Book/）、不许 golden accept、不许 push。
> 一包一主题：本批只收口异族 564 实锤的 **PoC-2（毒样例供给链）**。PoC-1（规则 staging 双钥分离）、PoC-3（人签事件流）、密码学签名**明确不在本批**。
> 仓库根：`C:\CodeLearnling\note\note\C++\CPP-Bible`；解释器只用 `.venv\Scripts\python.exe`；ruff 用 `C:\Users\ASUS\.local\bin\uv.exe tool run --from ruff==0.16.5 ruff check`。
> 开工前先读：`_arch_v7/03_验证器自身安全.md`（PoC-2 与建议 3/4 原文）、`_arch_v7/probes/poc2_poison_self_attest.py`（已实证的复现脚本）。

---

## 0. 为什么做这批（先理解，别跳过）

系统现在大量决策依赖三个数：**RULE-COVERAGE（规则覆盖率）、零覆盖攻击面、mutation 拦截率**。异族 564 实锤（2026-09-17，脚本可复跑）：覆盖率这个尺子本身能被一行文本注水——

- **洞 A（covered 文本自证）**：`tools/poison_drill.py` 的 `rule_coverage()`（约 2126 行）里
  `covered = set(re.findall(r'"([A-Z][A-Z0-9-]+)" in who', drill_src))`
  是在 poison_drill **自己的源码文本**里 grep 字面量 `"RULE-ID" in who`。它证明的是"源码里出现过这个字符串"，**不是**"存在一个真毒载荷、实跑时真被这条规则拦"。注入 0 个真载荷、只加一行注释 `# "FAKE-ID" in who`，covered 就 +1。
- **洞 B（豁免台账自批）**：`tools/poison_exemptions.yaml` 是零依赖行解析的自声明台账（`load_exemptions()` 约 2107 行）。存在时**无签名、无复核**，自写一条 `- {id: EV-X, reason: ..., date: ...}` 就把该规则永久移出 uncovered 分母、CI 转绿。台账文字纪律写了"豁免≠免检、必须另有 pytest 正反例兜底"，但**没有任何机器强制**——reason 里"pytest xxx 已覆盖"是手写声明，没人核那个测试真存在、真断言这条规则。

后果：表观覆盖率接近 100%（covered 靠真载荷 + 27 条豁免），但其中"真有载荷/真有测试背书"的比例是本批要算清楚的。**尺子能注水，跑再快的 mutation（580 已 3.47×）也是在松地基上量。**

修法总原则（来自 564 建议 3/4，本批照做，不另起炉灶）：
- covered 必须是 **who 断言 + 实跑结果 + 规则注册** 三方一致的产物，纯注释/字符串/没真跑/跑了没命中，一律不算；
- 豁免必须有"异族眼睛"背书（`redteam_seen`）；存量 27 条苦力**不得替异族签字**，按 legacy 单列、给诚实口径，不偷偷让 CI 红也不继续伪装成已覆盖。

---

## 第 0 步：开工先量 + 红基线（数字以你实跑为准，不许照抄本文件或 564）

1. 记录开工基线并贴进 worklog：`git rev-parse HEAD`、gate（规则数/命中 block/warn/advice）、`python -m tools.poison_drill` 末尾的 `RULE-COVERAGE x/y` 与零覆盖攻击面、`python tools/tool_integrity.py --check`（**脚本方式**，`-m` 会 ModuleNotFoundError）。
2. **复现两洞（红基线）**：跑 `.venv\Scripts\python.exe _arch_v7\probes\poc2_poison_self_attest.py`，确认洞 A（注释文本谎报覆盖）、洞 B（自写豁免移出分母）当前仍成立。若已不成立，停下在 worklog 说明，不要硬改。该探针只读 + TEMP/monkeypatch，不应污染正式目录；跑完 `git status --short` 确认。
3. **covered 逐条对账**：对当前 `rule_coverage()` 报出的每个 covered 规则 ID，判定它是否同时满足：(a) 有一个**注册进 drill 载荷表、会真跑**的载荷；(b) 该载荷的通过判据 `ok = ... "RULE-ID" in who` 含它；(c) 实跑时该载荷确实通过、`who` 真的含它。把"只在源码文本出现、不满足 a/b/c"的列为**幽灵覆盖声明**（预计为 0 或极少，以实测为准）。
4. **27 条豁免逐条机器核**：解析 `poison_exemptions.yaml` 每条 reason 里声称的 pytest 测试名（形如 `test_xxx`），机器核对：测试函数在 `tests/` 下**是否存在**；存在的话其函数体/夹具是否**真的断言了该 rule_id**（grep 该 ID 在对应测试里的命中，区分注释与断言）。分三桶落盘到 worklog：
   - `backed`：测试存在且真断言该规则；
   - `missing-test`：reason 声称的测试根本不存在；
   - `weak-test`：测试存在但没断言该规则（背书不成立）。
   这一步只统计、不改台账。

> 第 0 步所有数字写进 `_worklog_581.md`，作为改前/改后对照基线。PowerShell 内联 `python -c` 嵌套引号必坏，统计脚本写成独立 .py（放沙箱 `_t581/`，跑完可留探针不留垃圾到正式目录）。

---

## 任务 1（洞 A）：covered 从"源码文本 grep"升级为"实跑行为收集"

改 `rule_coverage()` 及其数据来源，**不再**用正则扫 `drill_src` 文本来认定 covered：

1. 在 drill **执行载荷的主循环**（统计 passed/total、`stats` 那一带，约 1993 行附近；载荷通过判据形如 93/147/184 行的 `ok = "EV-X" in who`）里，对每个**实际通过**（真跑、且拦截判据成立）的载荷，收集它 `who` 断言里命中的规则 ID，汇总成 `behavioral_covered: set[str]`。
   - 只有"载荷真跑 + 判据通过 + who 实含该 ID"三者同时成立，ID 才进 `behavioral_covered`。
   - 注意现在多处注释反复强调"RULE-COVERAGE 正则只认字面量 `"RULE-ID" in who`、变量名须恰为 who、勿参数化"（约 1399/1559/1614/1837 行）——这些注释是旧静态口径的约束，改造后要相应更新为"行为收集"口径，别留下误导性注释。
2. `rule_coverage()` 返回的 covered 改用 `behavioral_covered`。纯注释、未注册载荷、跑了但没命中、字符串里出现但无载荷的 ID，**一律不算**。
3. 保留一个**静态幽灵自检**（建议 warn/报告项，不改变 poison 退出码语义）：源码里出现 `"X" in who` 文本、但 X 不在 `behavioral_covered` 也不在合法豁免里的，报告为"幽灵覆盖声明"并列 ID，防止以后有人靠加文本骗覆盖。
4. 不改变现有"nc 判决走 replay 路径、不进 RULE-COVERAGE 分子"的既有口径（约 1198/1291/2076 行，557 D6 已定）；V-iso 双指标（trap/clean）维持独立计数器，别动。

**正反例回归锁（新增 pytest，建议放 tests/test_poison_coverage_581.py）**：
- 反例（洞 A 必须被抓）：在 drill 源码副本/沙箱里注入一行注释形态 `# "FAKE-COVERAGE-NO-PAYLOAD" in who`、不注册任何载荷 ⇒ `rule_coverage()` 的 covered **不得**增加、FAKE ID 进幽灵声明；
- 正例：一个真载荷实跑被某规则拦 ⇒ 该 ID 进 behavioral_covered；
- 锁：当前所有真跑通过载荷覆盖的规则 ID 集合，改造前后应一致（若有"幽灵"被剔除，必须在 worklog 逐条说明是哪条、为什么它本来就不该算）。

---

## 任务 2（洞 B）：豁免二人锁 + 存量 legacy 单列 + reason 背书机器核验

改 `load_exemptions()` / 台账 schema / surface_map，**fail-closed 方向**，但存量不搞一夜崩盘：

1. **schema 加字段**：豁免条目在现有 `{id, reason, date}` 外，新增可选 `redteam_seen: <异族只读会话标识+日期>`（例如 `arch_v7/2026-09-17`；单用户阶段异族=新开会话换模型的只读轮，标识可识别即可，**不做密码学验证**——密码学签名是冻结项）。零依赖行解析器要能解析这个新字段（沿用现有 flow-map 正则风格，别引 PyYAML）。
2. **新增豁免强制二人锁**：`date` 晚于本批合入日（2026-09-18）的豁免条目，缺 `redteam_seen`（空/占位/无法解析）⇒ 该豁免**无效**，该规则回到 uncovered、poison 退出码按欠账处理（fail-closed）。带合法 `redteam_seen` 的才移出分母。
3. **存量 27 条不许替签**：`date <= 2026-09-18` 且无 `redteam_seen` 的，苦力**严禁编造** redteam_seen；统一归类为 `legacy`。legacy 条目不立即让 CI 红，但：
   - 在 `poison_surface_map.json` 与 poison 末尾报告里**单列** `legacy_exempt` 计数与清单，和"真二人锁豁免 `signed_exempt`"分开；
   - 同时打印两个覆盖率，不许只报好看的那个：
     - **表观覆盖率** = (behavioral_covered + signed_exempt + legacy_exempt) / 规则总数（旧口径延续，便于对比）；
     - **诚实覆盖率** = (behavioral_covered + signed_exempt) / 规则总数（legacy 不计入已覆盖，只单列说明）；
   - worklog 里写明：legacy 要等以后异族只读轮次逐条复核后补 `redteam_seen` 才能转 signed（这是人/异族活，机器不代签）。
4. **reason 背书机器核验（把文字纪律变机器闸）**：对每条豁免（含 legacy），用第 0 步第 4 小步的三桶结果：
   - `missing-test` / `weak-test` 的条目，在报告与 surface_map 里单列 `unverifiable` 清单并点名（这些是"声称 pytest 兜底但兜底不存在/不成立"，最该先补）；
   - 这一项本批**只点名、不自动删除豁免**（删除会改变分母/退出码，属口径动作，交人裁决）；但 `backed` 与 `unverifiable` 的计数必须出现在报告里。
5. surface_map（`build_surface_map`/`write_surface_map` 约 2160/2206 行）增补字段：`behavioral_covered`、`signed_exempt`、`legacy_exempt`、`unverifiable`（含 id 与桶别）、`honest_rule_coverage` 与 `apparent_rule_coverage` 两个率。旧字段能保留就保留，报告快照类测试（T2/syrupy）按实测更新并在 commit 说明"是口径新增不是凑数"。

**正反例回归锁**：
- 反例 1：追加一条 `date=2026-09-19`、无 redteam_seen 的新豁免 ⇒ 该规则仍在 uncovered、退出码不为 0；
- 反例 2：reason 写一个不存在的 `test_xxx` ⇒ 该条进 unverifiable 被点名；
- 正例：带合法 redteam_seen、且 reason 测试真实成立的新豁免 ⇒ 移出 uncovered；
- 锁：存量 27 条全部落 legacy、不被静默删除，且 honest/apparent 两个率都能算出并打印。

---

## 任务 3：重钉、测试、收工门禁

- `poison_drill.py` 在 CORE_TOOLS 内 ⇒ 改完**同一 commit** 跑 `.venv\Scripts\python.exe tools/tool_integrity.py --update` 重钉并带上 `tools/.tool_checksums`；若本批没动其它 4 个核心工具，只有它的 sha 变化。
- 新增/改动测试进 fast 还是 slow 要判断：纯函数/解析/集合计算进 fast（`-n auto` 安全）；任何触发真编译、真跑 replay、或比对真实 Examples 全树指纹的，**串行**（套 `conftest.replay_serial`，580 已为同类 xdist 假红立过规矩），别再制造 `-n auto` 假红。
- 护栏纪律：本批新增任何自检/校验函数**不许裸 `except Exception`**（570 教训：会把 NameError 吞掉导致自检永远假绿），异常类型收窄；且每个"绿"都要有一条能让它变红的反例测试。
- **收工门禁（fresh、串行、以退出码定论；`-m slow` 汇总行常被管道吞，别拿"没看到 failed"当绿）**：
  - `tool_integrity.py --check` exit 0；
  - gate 规则数/命中（block/warn/advice）与开工**逐字一致**（本批不改 gate 判决规则；warn=186 的 OBSERVATION-LIVENESS 待补锚是既有知识活，别碰）；
  - `python -m tools.poison_drill`：毒样例全过、零覆盖攻击面无，并打印新的 honest/apparent 两个覆盖率与 legacy/unverifiable 清单；
  - replay confirm=56/refute=0（本批不应碰 replay 判决；若没改 replay 可引用开工 fresh 数并说明）；
  - `pytest -m "not slow" -n auto` exit 0；`pytest -m slow -n0` 除**已知预期红** `test_golden_lock_json`（warn 136→186 待人审 accept，与本批无关）外全绿；
  - ruff（启用族 `["E4","E7","E9","F","I001","FURB167"]`）改动文件 All checks passed；
  - 受控目录 `git diff --quiet -- atoms/ evidence/ Examples/ Book/` exit 0；
  - 复跑 564 PoC-2 脚本：洞 A、洞 B 修后应**不再能注水**（注释文本不再增 covered、无签名新豁免不再移出分母），把修前/修后输出贴进 worklog。

## 交付与留痕

- 一任务一 commit（建议：任务1 行为级 covered 一个、任务2 豁免锁+legacy 一个、任务3 重钉/测试若与前两者强耦合可并入对应 commit）；commit message 里按任务分节，数字用实测值。
- `_worklog_581.md`：开工基线、第 0 步四张表（covered 对账/27 条三桶/PoC 修前修后）、改前改后 honest vs apparent 覆盖率、偏差表（"提示词/564 说 X、实测 Y"逐条）、复跑命令、交人项。
- **数字纪律（写死）**：行为级改造或 legacy 单列后覆盖率可能下降、unverifiable 可能非 0——**掉就如实掉，不许为维持"覆盖率 100%"而放水、补假载荷、替豁免签字**。发现器的价值在于数字诚实。
- 不 push、不 golden accept、不改卡、不碰 580 的 `--jobs` 路径与 mutation 判决。

## 明确不做（防止扩面）

- PoC-1 规则 `staging/registered` 双钥分离（564 建议 1，动规则生效语义，独立下一批）；
- PoC-3 `human_sign_events.jsonl` 人签事件流（564 建议 5，独立小任务）；
- gate 自启动完整性（建议 2）已在 567 的 `enforce()` 做了，不重复；
- 任何密码学签名/密钥/sigstore（战略冻结）；
- 替 27 条存量编 `redteam_seen`、自动删除 unverifiable 豁免、自动 accept golden；
- replay/golden 的 `--jobs`、M6 剩 8 条逃逸、560 B3/B4/B5（各有归属，不在本批）。

## 已知环境坑（省得重踩）

- replay/poison/mutation 全量**不可并发**（抢真实 `build/.replay_lock`），验收命令串行跑；
- 全量 pytest 收尾可能撞 `[safe-delete] SAFE_DELETE_BULK_CONFIRM_REQUIRED`（环境固有删除守卫，528/559 记录），复跑一次即可，非代码回归；但要在 worklog 区分"删除守卫假红"与真失败；
- `--cards all` 不解除 `--limit` 默认值；mutation 相关本批不跑全量（与主题无关）；
- 580 后 mutation 走 `--jobs`，本批不改它，别被并行 worker 的临时根干扰 poison 实跑（poison 走自己的 TEMP/monkeypatch 探针）。
