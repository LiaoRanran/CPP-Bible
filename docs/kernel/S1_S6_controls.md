# G3.2 自律制衡层 S1–S6（机制，非口号）

> 每套写明：**谁 / 在哪个环节 / 用什么手段 / 如何自动判定 / 违规处置**。
> S1/S2/S3 的机器判定在 `tools/gate_engine.py`；S4 = `tools/golden_lock.py`；S5 = `tools/debt_ledger.py`；S6 = `tools/poison_drill.py`。全部接入 `cppbible check --stage quality` 与 CI。

## S1 三权分立（Author 禁自证 / RedTeam 只证伪 / Gatekeeper 机器复算）

| 项 | 内容 |
|---|---|
| 谁 | **Author**（Agent/人）只产出原子卡与证据卡；**RedTeam** 只做证伪（KPI=挑出错，产出攻击工单）；**Gatekeeper** = `gate_engine` + `atom_evidence_replay` 机器复算；**人级认可权唯人**（`verified_by: human:*`）；机器级/红队级各自留痕（`machine:*`/`redteam:*`，G6 四级） |
| 环节 | 写入 → 机器复算 → 红队证伪 → 人审签收（**按 DAL 分级**：A/B 必到人审；C/D/E 红队通过即可，但豁免人审本身须人签 `dal_reviewed_by`）→ 入库（同一执行者不得跨越签收段） |
| 手段 | `S1-AUTHOR-SELF-VERIFY` 规则：`verified_by` 前缀必须与 `status` 级别匹配——人级 ⟹ `human:*`（Agent 写不出合法签收，写了也不被机器认）；`machine-verified` ⟹ `machine:*`；`red-team-verified` ⟹ `redteam:*`（见 `G6_status_levels.md`） |
| 自动判定 | 机器查字段前缀 + 级别匹配（gate_engine，block 级） |
| 处置 | **阻断**：无对应级签署人的已验证状态直接红 |
| 提示分离 | Author 提示（写卡模板/必填字段）与 RedTeam 提示（攻击清单：证伪/边界/反例）在流程上分离；执行 Agent 的提示模板在 G5 迁移时随卡模板固化 |

## S2 声明-证据绑定（作者自述无效）

| 项 | 内容 |
|---|---|
| 谁 | Author 声明（`claim` 字段）；Gatekeeper 复算 |
| 环节 | 声明入库 → Gatekeeper 干净环境重跑（`atom_evidence_replay`：编译→运行→工件哈希→sanitizer 四校验） |
| 手段 | 声明是结构化字段（`claim`/`claim_boundary`/`actual`），证据是可复算工件（`artifact` + `sha256`）；`S2-EVIDENCE-VERDICT`：verified 原子**只能绑 `verdict=confirm` 的证据卡** |
| 自动判定 | replay 四校验 + 规则查 verdict（block 级） |
| 处置 | **阻断**：证据 refute 时原子必须回 draft；引用不存在的证据卡 = 红 |

## S3 伪证据检测（空测试 / 恒真 / 硬编码 / 缩样本）

| 项 | 内容 |
|---|---|
| 谁 | Gatekeeper（机器）+ RedTeam（来源真实性核验） |
| 环节 | 证据卡入库与每次质量门禁 |
| 手段与自动判定 | ① **clean-room 重跑**：replay 每次真编译真运行（`compile_rc`/`run_match`）；② **工件同代**：`artifact_sha256_mismatch` 即拦（"旧工件 vs 旧记录"式假阳性机器化拦截）；③ **恒真测试**：`EV-FALSIFICATION` 缺证伪对照即拦；④ **硬编码期望**：`S3-EXPECTED-HARDCODED` 查期望片段是否出现在夹具字符串字面量里（打印常量冒充观测 = 作弊级阻断）；⑤ **缩样本**：`EV-MATRIX` 缺 compiler/std/opt 即拦 |
| 处置 | **阻断**（作弊级） |
| 设计占位 | 「为变绿删测」需 git 历史比对（删测试而门禁转绿），列为 warn 级设计占位（M5 实现口径） |

## S4 黄金非回归锁（`tools/golden_lock.py`）

| 项 | 内容 |
|---|---|
| 谁 | Gatekeeper 自动固化与比对 |
| 环节 | 达标时 `sync` 固化快照 → 每次 CI/prepush `check` |
| 手段 | 指标全部机器复算：block_findings / warn_findings / atoms_total / evidence_total / verified_atoms / replay_confirm（ADR-0005 快照-漂移底座）+ **G6 四级分列** human_verified / red_team_verified / machine_verified / dal_gap |
| 自动判定 | block/warn/dal_gap 上升、原子/证据/各级 verified/复算通过数下降 → **恶化即红**（只盯总数会被"人级掉 1 / 红队级涨 1"置换掩盖）；改善提示 `sync` 把进步锁进快照 |
| 处置 | **阻断**；口径/阈值变更不得静默——`check --accept "理由"` 显式接受并写入快照 `accepted[]` 审计字段 |

## S5 豁免 = 带息债务（`tools/debt_ledger.py`）

| 项 | 内容 |
|---|---|
| 谁 | **人**开票（`owner: human:*`，Agent 不得自批——机器校验）；Gatekeeper 核销 |
| 环节 | 豁免发生时开票（cause/risk/compensation/owner/opened/due）→ 每次质量门禁核验 → 到期清票（写 reason，清票也留痕） |
| 手段 | `debt_ledger.json` 台账 + 四类机器判定：**字段缺失** / **owner 非人工** / **到期未清（due < today）** / **无永久豁免（due − opened > 90 天）** / **负债率 > 15%**（票据数/质量门禁项数） |
| 自动判定 | 全部 block 级 |
| 处置 | **停线**（exit 1） |
| 首张票 | `DEBT-001`：`compile_exempt.json` 的 63 条历史豁免未票据化（显性化既有债，due 2026-10-10，G5 迁移波次逐条转正） |

## S6 审计黑匣子 + 变异测试（`tools/poison_drill.py`）

| 项 | 内容 |
|---|---|
| 谁 | Gatekeeper 对制衡层自身发起攻击（自我红队） |
| 环节 | 每次质量门禁跑 `poison_drill`（定期注入 = 每次注入）；工单/快照/台账全部落盘（git + state 文件 = 黑匣子） |
| 手段 | 注入**七类**毒样例 + 一个阴性对照：**P1 假论断**（verified 无证据无签收 → S1+S2+VERIFIED-BOUND 必须拦）、**P2 过期工件**（sha256 不符 → replay 必须拦）、**P3 缺反例**（→ EV-FALSIFICATION 必须拦）、**P4 自证断言**（夹具自定义 `operator new/delete`，而断言只做存在性匹配——命中**定义处**即通过、零调用点也恒真 → `EV-SELF-SATISFIED-ASSERT`）、**P5 伪证伪**（`falsification` 只有"若…则应…"的假设句、无量化对照值 → `EV-FALSIFICATION-QUANT`）、**P6 恒真观测**（`actual` 只有存在性判断，如 `observer != nullptr`，对 claim 的关键变量零响应 → `EV-TRIVIAL-OBSERVATION`）、**P7 无留痕矩阵**（`matrix.compiler` 声明多个编译器却只有一个工件、卡内无"外部留痕"说明 → `EV-MATRIX-UNBACKED`）、**阴性**（干净卡必须放行，防恒红） |
| 由来（P4–P7） | 2026-09-11 第四批：把**第三批红队抓到的真实漏网**变成机器可判的结构性质疑——P4 对应 `EV-MEM-032` 初版的自证断言（`_ZdaPvy` 被夹具自身定义满足）、P6 对应 `EV-MEM-034/035` 初版的 `use_count after join=1`（join 后任何实现都读到 1）。四规则均 `warn` 级：指向**判别力**问题而非形式缺失，且对"卡内已注明调用点口径"（P4）与"跨类型比对值"（P6）自动豁免，避免误伤 |
| 自动判定 | 任一毒样例漏网或阴性误杀 → exit 1 |
| 处置 | **先修制衡，再修内容**（抓不出毒 = 制衡失效，比内容错误更严重） |
| 「连续零质疑视为可疑」 | poison_drill 每次必跑 = 结构性质疑；warn 债务在工单中持续可见（S5 台账），不存在"静默全绿" |

## 与 G3 验收门的对应

验收门要求「3 个毒样例现场攻击制衡层，必须全部拦截并报对原因；任一门禁能给出正例触发与反例不触发」：
- 毒样例 = `poison_drill.py` 的 **P1–P7**（**机器化，每次 CI 现场攻击**；验收门原要求的 3 个已由 P1/P2/P3 满足，P4–P7 是 2026-09-11 按第三批红队漏网追加）；
- 正例触发 + 反例不触发 = `tests/test_gate_engine.py`（每条规则成对）+ `poison_drill` 的阴性对照 + `tests/test_s1_s6.py`（S4/S5 的红绿对）。
