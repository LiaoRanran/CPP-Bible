# 558 · 投喂词：固化 557 收尾基线 + V-iso 真编译毒载荷(N1–N7) + M3 区间收口 + impact 多跳闭包

> 你是「阙疑」元系统的建设者。仓库根 `C:\CodeLearnling\note\note\C++\CPP-Bible`，分支 master，Windows。
> 本批接续 557 的停点（B1/C/D 未做），并先把 557 的人审 accept 基线固化进版本。
>
> **铁律（违反即返工）**
> - 解释器只用 `.venv\Scripts\python.exe`（有 PyYAML 6.0.3）；workbuddy python 无 PyYAML，禁跑门禁。
> - 一 Part 一 commit；每个规则改动配正反例毒样例 + pytest，**positive 样例必须断言 severity 且载荷避开降级分支**（526 P65 教训）；poison 覆盖只认载荷里字面量 `"RULE-ID" in who`。
> - 改 gate_engine.py / poison_drill.py / viso 等核心工具后 `tool_integrity.py --update` 重钉；改核心工具后跑**全量** pytest 不只单文件。
> - **存量零误伤硬约束**：任何规则改动先全量实测，block 不得新增、warn 不得新增存量命中（毒样例沙箱除外）；不达标立即回退、停在该 Part 边界，不留半成品规则。
> - 不 push、不 --no-verify；golden accept 已由监工完成（本批只复用，不再 accept）。
> - 不编数字：跑多少报多少，覆盖分子不变就如实写"不变"，不许凑覆盖率。
> - 做不完按 Part 边界停（A > B > C），不留半成品；worklog 写明停点与复跑命令。

---

## Part 0 · 开工对账 + 固化 557 收尾基线（第一个 commit）
1. 监工已完成 557 人审 accept：`golden_state.json` 现为 M（基线 warn 59→136，四桶 real12/legacy108/accepted16）。**本 Part 把它固化**：连同 `docs/kernel/system_debt_ledger.md`（监工化债总账，正式台账）一起提交，commit message 写清"557 人审 accept 基线固化 + 化债总账"。`_worklog_*.md` 按惯例不入库。
2. 实测对账基线：`gate_engine.py --check` 应得 **规则 61 · 命中 141（block=0 warn=136 advice=5）**；`poison_drill.py` **97/97、RULE-COVERAGE 36/61+27、零覆盖攻击面无**；`atom_evidence_replay.py --check` **confirm=56/refute=0/infra=0**；`golden_lock.py buckets` 应得 real12/legacy108/accepted16/**未分类 0**；`pytest tests/test_json_output.py -k golden_lock_json -n0` 应绿。任何一项不符，先停下报监工，别在脏基线上施工。
3. 提示词与磁盘不符以磁盘为准，记偏差表。

## Part A ·（P1）V-iso N1–N7 真编译毒载荷进 poison（557 B1 停点）
- 背景：N1–N7 的**判决分支**已由 `tests/test_negative_controls.py`（10 例，替身编译器）全覆盖；缺的是**真实 sandbox + 真编译**载荷化（533 §2.5）。
- 位置：`tools/poison_drill.py::drill()`，在 P43f 之后**内联**新增（磁盘无 tests/poison/ 目录，毒样例内联是 P43b/c/f 先例）。用现有 `sandbox()`。
- 七类"阴面造假/走形式"定义读 `_arch_v2_round2/533_V-iso施工规格.md` 与 `tools/viso_diff.py` 判据（单 hunk/纯删除/删1–3行/token≤40/改动率≤2%/anchor 函数体内/retain 逐字/Itanium 符号同源/实测翻转）。
- **关键陷阱（557 D6，别谎报）**：nc 判决是 replay 路径字符串、**不是 gate 规则**，故 N1–N7 **不会**增加 RULE-COVERAGE 分子。你要如实报"poison 全过、覆盖分子仍 36/61"；N1–N7 的拦截效果由**双指标**另立计数器——`trap_block_rate`（七类假阴面被拦的比例）与 `clean_pass_rate`（合法真阴面不误伤的比例），首跑报这两个数。
- 验收：poison 97→（97+N7 条，但全过）；trap_block_rate 应=100%（七类假阴面全被拦）；clean_pass_rate 应=100%（NC1 合法真阴面不误伤）；任一 <100% 如实报、别硬凑。

## Part B ·（P1，真洞收口，零误伤不达标即回退）M3 区间降级 + M2 诚实化（557 C 停点）
照 541 已验证安全形状，**不许自由发挥**：
- **B1 M3 区间锚定丢失**：把 `contains_in→contains`、`absent_in→absent`（区间锚定退化为全文存在性）与去 `-Werror` 的变异收口。
  - 单点互斥：同一条 artifact_assert 已被更高 severity 路径 block 时，不再重复出 Finding（避免 541 试验 2 的 block+warn 并发打散既有测试）；
  - **空/纯中文 text 的 block 仍只对 `contains_in/absent_in`**（541 试验 1 证明放开会 block 0→38 误伤）；新纳入的 contains/contains_any 等 kind 只出 **warn**；
  - 先全量实测 83 卡 0 新增命中再落码；配正反例毒样例（区间降级须 warn / 合法 contains 散文不误伤）；重钉 tool_integrity；全量 pytest。
- **B2 M2 逃逸诚实化（548 建议）**：mutation M2 路径变形目前取全文第一个路径，变异点落在门禁从不读的注释/正文，逃逸数混着无效提问。改为只在**门禁真读字段**（command/artifact/run_match_file/fixture 等）内挑路径；变异点不在门禁读取面的计 n_a(out_of_scope) 而非 escaped。重算 `mutation_fuzz.py --operators M2,M3,M4` 拦截率，修前/修后对照（口径变化写明，不与旧数字直接比大小）。
- 若 B1 任何一步存量误伤无法消除 ⇒ 回退 B1 代码、只交侦察与精确施工点，不许带红收工。

## Part C ·（P2，小而确定，可停）impact_analysis 多跳闭包（557 D 停点）
- `tools/impact_analysis.py` 目前一跳、数据源是 frontmatter dict（**不是 SQLite，禁止 recursive CTE**；recursive CTE 只属于本就是 SQLite 的 knowledge_graph.py）。
- 纯 Python 补：传递闭包（多跳上游/下游影响）+ 环检测（环要显式报错，不无限递归）。
- pytest 覆盖：链式 A→B→C 多跳不重复、菱形依赖计数正确、自环/成环报错、缺目标节点 fail-loud。

---

## 收工总验收（fresh run，逐项实测写进 _worklog_558.md）
1. Part 0：收尾基线已 commit；golden buckets 未分类=0；golden_lock_json 测试绿。
2. Part A：poison 全过且**如实报覆盖分子是否变化**；trap_block_rate / clean_pass_rate 两个新计数器报实值；NC1 合法真阴面不误伤。
3. Part B：若落地，gate 仍 block=0、warn 不新增存量命中；M3/M2 修前修后拦截率对照；全量 pytest 绿、tool_integrity 重钉；若回退写明原因与后续施工点。
4. Part C：impact 多跳/环 pytest 绿。
5. 总门禁：gate 规则数/命中（报实测）、replay confirm=56/refute=0、`pytest -m "not slow" -n auto` 连续 2 轮全绿、slow 套件含 golden_lock_json 全绿、受控目录零污染。
6. 偏差表：所有"提示词假设 X / 磁盘实测 Y"逐条记录。

## 明确本批不做
- 不重新 accept / 不改已落桶的四桶分类（real12/legacy108/accepted16 是监工人审结果）；不做 26 张卡命题回填；不做概念自动合并；不做 model canary；不做 golden_lock 并行化；不开 G-supervisor；不让 LLM 进闸。
