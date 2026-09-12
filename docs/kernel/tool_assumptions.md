# 工具隐性假设台账（tool_assumptions）

> 来源：373 独立对抗渗透（TRAE / DeepSeek v4.1 flash 独立会话，异族执行）阶段一盲测 + 阶段二开卷校准。
> 收编：2026-09-12 由建设者（主 agent）从 `adversarial_373/工具假设台账草稿_15条.md` **正式化**；草稿原文保留在案，不改。
> 用法：本表回答一个门禁自查回答不了的问题——**「工具以为什么是真的？」**。每条假设被违反 = 一个逃逸。
> 规则数以 `tools/gate_engine.py --list` 为唯一口径（当前 **38 条**，勿写死）。

## 0. 与「工具能力清单」的区别

工具文档（`M4_gate_engine.md`）写的是**工具做了什么**；本表写的是**工具默默相信了什么**。
前者在写规则时会查，后者只在被攻击时才暴露——所以必须显式记账。

## 1. 假设台账（15 条）

状态列口径：
- **已修**：本批已落地实现，附实测证据；
- **待修**：逃逸已确认、规则未实现（见 `373_收编与修复记录.md` §4 的实测否决结论）；
- **承担转移**：机器层判定不可行，明确改由红队盲读/人审承担（**不假装工具已覆盖**）。

| ID | 假设内容（工具的隐性前提） | 违反者 | 逃逸前检查 | 现状 |
|---|---|---|---|---|
| T-A01 | `artifact_assert` 的断言语义由攻击者按「与 claim 相关的结构证据」填写 | B2-R1（`contains "main"`） | 无（只查断言命中，不查断言对象相关性） | **待修**：拟新增 `EV-ASSERT-DISCRIMINATOR`；按蓝图原文实现会误伤 29/56 张合法卡（§4 实测），须窄化 |
| T-A02 | `actual`/`.out` 中呈现的数字即「观测」，卡散文引用的读数即观测的子集 | B3-R2（未声明键 + 散文编造） | 部分（只扫声明键值域；run_match 只核声明键） | **待修**：拟新增 `EV-OBSERVATION-VISIBLE`；按原文实现误伤 32/56 张（§4），须窄化为「`.out` 未声明键」判据 |
| T-A03 | 「编译器零诊断/无警告」由 `compile_rc == 0` 即可证明 | B6-R3（`-Wall` 警告仍 rc=0） | 无（compile_rc 不看 stderr） | **已修**：`EV-ZERO-DIAG-WERROR`（371-W3 收口，含毒样例 P11） |
| T-A04 | `human:`/`machine:`/`redteam:` 前缀之后是「真实可信的署名者」 | B9-G2a/b/g（**空名 / 纯空格名**） | 无（仅 `startswith` 前缀） | **已修**：`principal_ok()` 单点（前缀 + 实名非空 + 人级在册），三处统一（S1 / status_history / DAL 豁免），另收 `debt_ledger.owner_ok()`；毒样例 P13 |
| T-A05 | `artifact` 与 `artifact_sha256` 描述的是「本卡命令亲自编译生成的那个产物」 | N4-R5（借他卡工件） | 弱（只要求命令行文本含 artifact 路径，任意 argv 均可） | **待修**：拟新增 `EV-ARTIFACT-GEN-TRACE`；按原文实现误伤 11/56 张（§4），须先修正「产出段归属」算法 |
| T-A06 | multi-TU 夹具的结论由「被锚的唯一 artifact + .out」完整承载 | B7（R2+R5 组合） | 无（单 artifact 字段） | **已修**：`artifacts[]` 多产物登记（371-W1），已用于 `EV-LANG-001/002` |
| T-A07 | `relations` 只有一种合法写法（dict 形态） | N1-G3（`- prerequisite: X` mapping-form 环静默） | 无（规则只读 `type`/`target` 键） | **待修**：解析器双写法归一后再跑 REL-DAG |
| T-A08 | EV id 全局唯一（与 ATOM 同级别身份） | N2-N1b（同 id 双卡遮蔽 verdict） | 无（EV 无唯一性规则） | **待修**：新增 `EV-ID-UNIQUE`（对齐 `ATOM-ID-UNIQUE`：stem == id + 全库唯一） |
| T-A09 | 行为不随环境（核数/用户名/日期/路径/CWD）漂移 | B5-R6（`nproc`/`__DATE__`/`USERNAME`） | 无（run_match 全等比较） | 部分已修（`d8ff94d` 已覆盖 `run_match_keys` 形态）；词根级检查（拟 `EV-NO-ENV-KEYS`）**待修** |
| T-A10 | `matrix.compiler` 声明的多编译器有真实双平台/CI 工件支撑 | N3-M11（P7 锚自满足） | 弱（锚正则含**命令自证项**） | **待修**：去掉命令自证锚，多编译器声明须附双份 `.out` 或 CI run 号 |
| T-A11 | P5 falsification「有量化值」即「可判别」 | B8-G5（同源自比含数字） | 部分（只查 `\d`） | **待修**：量化值须来自两个不同观察对象；同源自比 warn |
| T-A12 | pipeline 假定 `status_history`/`by` 是人真打的 | B9 / G2（前缀伪造） | 前缀级 | 见 T-A04（已修）。另：**按 git commit author 判身份**的 CI 侧白名单仍属 369 立项的第二批 M 项，与本条的**静态名册**互补（一个挡「空/冒名」，一个挡「本人账号代签」） |
| T-A13 | 卡的文件编码为 UTF-8 LF、无 BOM | M21/M22（CRLF/BOM 容忍） | 容忍（不报） | 非本洞新增（369-A1 行尾债）；**待裁决** |
| T-A14 | 折叠块 `\|`/`>-` 的内容会被解析为结构化字段 | N5-supp1（pedagogy 折叠 → 字符串） | 无（dict 检查静默跳过） | **待修**：解析器对折叠块仍做 dict 归一，或规则显式处理非 dict（P21） |
| T-A15 | replay `command` 只含编译器/构建类可执行程序 | N4-R5（`python`/`cp` 任意 argv） | 无（白名单不存在——353 §7.3 已如实记载） | **待修**：与 T-A05 合并解决（artifact 生成路径限制可执行程序） |

## 2. 三条「已修」的实证路径（可复现）

| 假设 | 规则/实现 | 毒样例 | 复现命令 |
|---|---|---|---|
| T-A03 | `EV-ZERO-DIAG-WERROR` | P11 | `python tools/poison_drill.py`（应全绿） |
| T-A04 | `principal_ok()` | P13 | 同上；另见 `tests/test_gate_engine.py::test_signoff_requires_real_name_not_just_prefix` |
| T-A06 | `artifacts[]` | — | `python tools/atom_evidence_replay.py --check`（EV-LANG-001/002） |

## 3. 台账维护约定

1. **新增门禁规则 ⟹ 回填本表**：若某条规则的动机正是补掉某条假设，把该行状态改为「已修」并填规则名；若规则只覆盖了假设的一部分，**必须在备注写清剩余部分**（半个覆盖比没覆盖更危险）。
2. **红队报告回国 ⟹ 先读本表**：新攻击若落在已有假设上，是「补漏」；若是新假设，追加一行（ID 续 T-A16…）。
3. **不得写「理论上已覆盖」**：状态只能是已修（附证据）/ 待修 / 承担转移（写清谁承担）。
