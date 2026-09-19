# 557 · 投喂词：人审解锁（L4 校准引擎第一块）+ L1 验证网补密 + 影响闭包

> 你是「阙疑」元系统的**建设者**。仓库根 `C:\CodeLearnling\note\note\C++\CPP-Bible`，分支 master，Windows。
> 本批主线：当前系统最痛的不是缺功能，是 **136 条 warn 压着 golden_lock 红、人无法快速裁决**，以及几条"判决已实现但毒样例/收口没补齐"的 L1 尾巴。本批把人审从"逐条读 136 条"变成"只看约 15 条真信号"，这是 L4 进化层（自我校准引擎）的第一块落地实体（见 References/architecture_架构演进/555）。
>
> **铁律（违反即返工）**
> - 解释器只用 `.venv\Scripts\python.exe`（有 PyYAML 6.0.3）；workbuddy python 无 PyYAML，禁跑门禁。
> - 一 Part 一 commit（Part A 内 A1/A2/A3 可分 commit）；每个规则改动必须配正反例毒样例 + pytest，**positive 毒样例必须断言 `severity=="block"/"warn"` 且载荷避开降级分支**（526 P65 假通过教训），不能只断言 "RULE-ID" in who。
> - 改 gate_engine.py / poison_drill.py 后必须 `tool_integrity.py --update` 重钉；改任何核心工具后跑**全量** pytest，不只跑单文件（528 教训）。
> - **存量零误伤是硬约束**：任何规则改动先全量实测 83 卡，block 不得新增（除毒样例沙箱）；不达标立即回退、停在该 Part 边界，宁可只交侦察结论，不留半成品规则。
> - 不 push、不 --no-verify、**绝不 `golden_lock --accept`**（accept 权唯人）；本批只产"建议人审的清单"，不替人签。
> - 不编数字：跑多少报多少；提示词与磁盘不符时以磁盘为准并记偏差表。
> - 做不完按 Part 边界停（A > B > C > D），不留半成品；worklog 写明停点与复跑命令。

---

## Part 0 · 开工侦察（先实测，约 10 分钟，结果写进 worklog §0）
1. `.venv\Scripts\python.exe tools\gate_engine.py --check` 核对基线：规则 61 · 命中 141（block=0 warn=136 advice=5）。
2. `tools\poison_drill.py` 核对 96/96、RULE-COVERAGE 36/61+27 豁免；`atom_evidence_replay.py --check` 核对 confirm=56/refute=0/infra=0。
3. `pytest -m "not slow" -n auto -q` 记录 fast 点数与全绿（556 后应全绿，含 1 skip）。
4. 复核 warn 按规则 id 的分布（监工已实测，供你对账，须自己重跑确认）：
   `ATOM-CLAIM-CONCEPT-NORMALIZED 77 · INFERENCE-NOT-MACHINE-VERIFIED 28 · EV-MATRIX-UNBACKED 16 · EV-OUT-UNDECLARED-KEY 6 · EV-FALSIFICATION-QUANT 4 · EV-ASSERT-SYMBOL-MAPPED 3 · ATOM-REL-TARGET 2 · EV-ENV-DEPENDENT-KEY 2 · EV-OUT-STALE-MTIME 2 · EV-SERVES-EXIST 1`（另有 5 条 advice）。
5. `git status` 记录开工现场（EV-CONC-001.md 的 M、tools/env_check.py 是 pre-existing，非你所改，勿纳入提交）。

## Part A ·（P0 主线）golden_lock 人审经济学：分桶 + 排序 + 建议清单（纯读，零规则改动）
目标：把 136 条 warn 自动结构化，让人 5 分钟裁决，而不是逐条读。**只新增工具/报告，不改任何 severity、不降级真问题、不自动 accept。**

- **A1 分桶器**（新增 `tools/review_triage.py`，纯读 gate Finding 集，不跑编译、不写受控目录）：把每条 warn 按规则 id + 是否有清零路径分四桶——
  - **桶① 迁移过程债（预期，随回填清零）**：`ATOM-CLAIM-CONCEPT-NORMALIZED`、`INFERENCE-NOT-MACHINE-VERIFIED`。每条附"清零动作"（概念归一/命题回填或人签，指向 526/528 的 STAGING 名单与 backlog），并标注这是新规则上线后的存量迁移信号、非内容退化。
  - **桶② 规则设计待甄别**：`EV-MATRIX-UNBACKED` 16 条。逐条读 `gate_engine.py` 中该规则实现（约 :1000-1002 的 A3①"刻意排除 actual"）与卡内容，区分 (a) 落在刻意设计排除区间=规则预期（建议登记豁免或细化规则措辞）vs (b) 真缺矩阵支撑=真信号转桶③。给出每条判定与证据行号。
  - **桶③ 真信号（人必须逐条看，排最前）**：EV-OUT-UNDECLARED-KEY / EV-FALSIFICATION-QUANT / EV-ASSERT-SYMBOL-MAPPED / ATOM-REL-TARGET / EV-ENV-DEPENDENT-KEY / EV-OUT-STALE-MTIME / EV-SERVES-EXIST。每条给 卡 id + 一句话为何是真信号 + 建议动作。
  - **桶④ 已登记豁免/重复**。
  - 输出机器可读 JSON（data/review/triage_<gitshort>.json，大 JSON 不入 git，加 .gitignore）+ 终端摘要（每桶计数 + 桶③清单）。
- **A2 人审排序 `--review-order`**：桶③优先；桶③内部按"知识完整性等级 KIL 高 × 是否首次出现 × 可证伪性/不确定性"排序（555 批次 U：人是校准 judge，把人有限的注意力放到最可能错、影响最大的卡上）。排序必须确定性（同输入同输出），无 KIL 数据时用规则权重 + 卡 id 兜底，并在报告注明"KIL 数据缺失，当前为兜底排序"。
- **A3 建议清单（不代签）**：在 `_worklog_557.md` 产出：四桶计数对账表 + 桶②逐条定性 + 桶③逐条建议 + 一段**供人复制的 `golden_lock.py check --accept "<理由>"` 命令**（理由里的数字用你实测的终值，不许照抄本提示词）。明确写：accept 执行权在监工，本工具任何情况下不得自行调用 accept。
- **pytest**（tests/test_review_triage.py，fast）：构造含各桶代表的 Finding 集合，断言分桶正确、桶②刻意设计样本被识别、排序确定性（跑两次结果逐字一致）、空 Finding 集不崩。
- 红线：A 全程**不得**修改 gate_engine 规则、不得改卡、不得 accept；若你认为桶①应降级为 advice，只作为"给人的选项"写进 A3 建议，**不在代码里执行**。

## Part B ·（P1，便宜收尾）V-iso 毒样例补齐 + parser 跨键陷阱定性
- **B1 V-iso N1–N7 进 poison（535 V4 遗留）**：判决函数 `check_negative_controls` 已在 replay 路径（535 V3），只补载荷。N1–N7 的七类"阴面造假/走形式"定义读 `_arch_v2_round2/533_V-iso施工规格.md` 与 `tools/viso_diff.py` 判据（单 hunk/纯删除/删 1–3 行/token≤40/改动率≤2%/anchor 内/retain 逐字/符号同源/实测翻转）。每条载荷断言**期望判决与 severity**，走真实 sandbox；注意 poison 覆盖判定只认载荷里字面量 `"RULE-ID" in who`（变量名须恰为 who，参数化比较会"载荷过但规则算未覆盖"，500 教训）。poison 全过且覆盖分子同步增加。
- **B2 parser 跨键 YAML 陷阱定性（556 留下的 xfail）**：把前导零与 YAML 1.1 陷阱词（`00000000`、`yes/no/on/off/null/~`、裸 `=`、超长数字等）在**门禁真正关心的键**（id/serves/verdict/command/negative_controls/relations 等）上逐一实测：自定义解析器 vs PyYAML safe_load 是否产生**语义分歧且硬化层放行**。产生真实放行分歧的 ⇒ 补硬化（白名单形态/类型校验，配毒样例，存量零误伤）；实测不造成分歧（两解析器一致或已被既有规则拦）的 ⇒ 把 xfail 转成**确定性通过测试**并注释"已证安全"，不留永久 xfail 黑洞。产出一张陷阱词×键的实测矩阵。

## Part C ·（P1，真洞收口，零误伤不达标即回退）M3 区间降级 + M2 诚实化
- **C1 M3 区间锚定丢失**：mutation 全量基线（data/mutation/full_baseline_v1.json）中 M3 把 `contains_in→contains`、`absent_in→absent`，区间锚定语义退化为全文存在性却放行（11 条逃逸含去 -Werror）。按 541 已验证的安全形状落地（541 两次撞存量，**严格照做**）：
  - 单点互斥判定：同一条 artifact_assert 已被更高 severity 路径 block 时，不再重复出 Finding（合并为单点，避免 541 试验 2 的"同条目 block+warn 并发打散既有测试"）；
  - **空/纯中文 text 的 block 仍只对 `contains_in/absent_in`**（541 试验 1 证明放开会 block 0→38 误伤）；新纳入的 contains/contains_any 等 kind 只出 **warn**；
  - 先全量实测 83 卡 0 新增命中再落码，配正反例毒样例（区间被降级须 warn / 合法 contains 散文不误伤），重钉 tool_integrity，全量 pytest。
- **C2 M2 逃逸诚实化（548 建议）**：mutation M2 路径变形目前取全文第一个路径，22 张卡变异点落在门禁从不读的注释/正文，逃逸数里混着无效提问。改为只在**门禁真读字段**（command/artifact/run_match_file/fixture 等）内挑路径变形；变异点不在门禁读取面的计 n_a(out_of_scope) 而非 escaped。重算 `--operators M2,M3,M4` 拦截率，给修前/修后对照（口径变化要写明，不与旧数字直接比大小）。
- 若 C1 任何一步存量误伤无法消除 ⇒ 回退 C1 代码、只交侦察与精确施工点，不许带红收工。

## Part D ·（P2，小而确定，可停）impact_analysis 多跳闭包
- `tools/impact_analysis.py` 目前只有一跳、数据源是 frontmatter dict（**不是 SQLite，勿用 recursive CTE**；recursive CTE 只属于本就是 SQLite 的 knowledge_graph.py）。纯 Python 补：传递闭包（多跳上游/下游影响）+ 环检测（环要显式报错而非无限递归）。pytest 覆盖：链式 A→B→C 多跳、菱形依赖不重复计数、自环/成环报错、缺目标节点 fail-loud。

---

## 收工总验收（fresh run，逐项实测写进 _worklog_557.md）
1. Part A：`review_triage.py` 四桶计数之和 == warn 总数（对账闭合，不漏不重）；桶②每条有行号证据；桶③排序确定；`pytest tests/test_review_triage.py` 绿；**确认全程无 accept、无 severity 改动、无卡改动**（git diff 受控目录为证）。
2. Part B：poison 全过（报新数字）、RULE-COVERAGE 分子同步；陷阱词×键矩阵落盘，xfail 要么转硬化要么转确定性通过测试。
3. Part C：若落地，gate 仍 block=0、warn 不新增误伤；M3/M2 修前修后拦截率对照；全量 pytest 绿、tool_integrity 重钉；若回退，写明回退原因与后续施工点。
4. Part D：impact 多跳/环 pytest 绿。
5. 总门禁：gate 规则数/命中（报实测）、replay confirm=56/refute=0、`pytest -m "not slow" -n auto` 全绿（连续 2 轮）、`-m slow -n0` 仅 pre-existing 的 test_golden_lock_json（golden 基线落后，等人 accept，与本批无关）、受控目录零污染。
6. 偏差表：所有"提示词假设 X / 磁盘实测 Y"逐条记录。

## 明确本批不做（防止越界/过载）
- 不做 golden accept、不做 26 张卡的命题回填（V5 backlog 另开）、不做概念自动合并（555 批次 V 只产候选）、不做 model canary（批次 W）、不做 golden_lock 自身并行化（125s 硬下限，涉 replay 全局锁，单开一批）、不做 G-supervisor（系统不自起 worker）、不让 LLM 进闸（L3 门未开）。
