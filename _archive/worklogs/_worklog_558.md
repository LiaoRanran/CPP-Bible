# _worklog_558 · 557 收尾基线固化 + V-iso 真编译毒载荷(N1–N7) + M3 区间收口 + M2 诚实化 + impact 多跳闭包

> 提示词：`References/architecture_架构演进/558_投喂词_557收尾基线_Viso真编译毒载荷N1N7_M3区间_impact闭包.md`
> 分支 master（本地，未 push）｜解释器只用 `.venv\Scripts\python.exe`｜本文件按惯例**不入库**。

## 0 · 停点

**全部 Part 已做完（0 / A / B / C），无停在 Part 边界。** 每条 commit：

| commit | Part | 内容 |
|---|---|---|
| `9092f82` | 0 | 557 人审 accept 基线固化（golden_state warn 59→136 + 四桶）+ 化债总账入库 |
| `7597e86` | A | V-iso N1–N7 真编译毒载荷进 poison + trap_block_rate/clean_pass_rate 双指标 |
| `56796c8` | B | M3 区间锚定丢失收口（warn）+ M2/M3 逃逸诚实化（门禁读取面 / out_of_scope） |
| `428f4dd` | C | impact_analysis 多跳传递闭包 + 环检测 |

复跑命令（照抄可用）：

```
.venv\Scripts\python.exe tools/gate_engine.py --check
.venv\Scripts\python.exe tools/atom_evidence_replay.py --check
.venv\Scripts\python.exe tools/golden_lock.py buckets
.venv\Scripts\python.exe tools/poison_drill.py                 # 含 N1–N7 与双指标
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards all --operators M2,M3,M4 --limit 5
.venv\Scripts\python.exe -m pytest -m "not slow" -n auto -q
.venv\Scripts\python.exe -m pytest -m slow -n0 -q tests/test_json_output.py tests/test_writer_selfcheck.py tests/test_patch_blocks.py
.venv\Scripts\python.exe -m pytest -m slow -n auto -q tests/test_poison_attack_type.py
```

---

## 1 · Part 0 开工对账 + 基线固化（`9092f82`）

提示词状态与磁盘**逐项相符**（无偏差）：gate `规则 61 · 命中 141 (block=0 warn=136 advice=5)`、
poison `97/97 · 覆盖 11/11 · 零未覆盖`、replay `confirm=56 refute=0 infra_error=0`、
golden buckets `real 12 / false_positive 0 / legacy 108 / accepted 16 / 未分类 0`、
`pytest tests/test_json_output.py -k golden_lock_json` 绿。

固化内容：`tools/golden_state.json`（M）+ `docs/kernel/system_debt_ledger.md`（新入库，监工化债总账）。
`evidence/conc/EV-CONC-001.md` 的 pre-existing M **未**纳入本批（非本批产物）。

**顺手发现（已在本批内修）**：固化基线后 `tests/test_review_triage.py::test_triage_reconciles_and_is_deterministic`
变红——`review_triage` 会读 `golden_state.warn_classify` 判"已登记豁免"，人审 accept 把
`ATOM-CLAIM-CONCEPT-NORMALIZED` / `INFERENCE-NOT-MACHINE-VERIFIED` 落 legacy ⇒ 它们归桶④、B1 归零。
按"对着口径复核"处理（B1 本身仍由**空 exempt 集**的单元用例守着），**不是**改测试凑数。

---

## 2 · Part A V-iso N1–N7 真编译毒载荷（`7597e86`）

位置：`tools/poison_drill.py::drill()`，P43f 之后**内联**（磁盘无 `tests/poison/`，沿用 P43b/c/f 先例）；
复用现有 `sandbox()` + 临时重定向 `atom_evidence_replay.ROOT` ⇒ 夹具与阴面编译全在 tempdir；
阴面走**真实 g++**（同一次 replay 里阳面 rc=0 ⇒ 编译器健康是实测证据，不解析 stderr 文本）。

实测判决（**逐条跑出来的**，非照抄 533 期望）：

| 载荷 | 实测 verdict |
|---|---|
| N1 阳过阴也过（逐字复制+加注释） | `refute:negative_control_diff`（零语义 diff） |
| N2 冒名阴面（整个换成别的程序） | `refute:negative_control_diff` |
| N3 阴面写坏（anchor 内删声明行 ⇒ 真编译 rc=1） | `refute:negative_control_broken` |
| N4 形式阴面（删 anchor 外的行） | `refute:negative_control_diff` |
| N5 阴面缺失（阴夹具不存在） | `refute:negative_control_missing` |
| N6 连主体删除（机制+返回 ⇒ retain 缺） | `refute:negative_control_diff` |
| N7a 干净卡（无 `negative_controls` 字段）/ N7b 合规 nc1（flip verified） | 放行（verdict 空） |

**双指标（首跑实值）**：`trap_block_rate = 100%（6/6）` · `clean_pass_rate = 100%（2/2）`。
**覆盖率诚实口径**：nc 判决是 replay 路径字符串、不是 gate 规则 ⇒ **RULE-COVERAGE 分子仍 36/61（不变）**，
未覆盖仍为空；poison 通过数 97 → **105**（N1–N6 六毒 + N7a/N7b 两对照）。

---

## 3 · Part B M3 区间降级收口 + M2/M3 诚实化（`56796c8`）

### B1 · M3 区间降级真洞（543 P3 形状）

真洞：`contains_in{symbol:区间, text}` 被降级成 `contains{text}` 后区间锚定丢失、主路径放行。
**先量后落码**（2026-09-16，56 卡 118 条断言）：

| 候选信号 | 存量命中 |
|---|---|
| **全文 kind 残留 `symbol`**（= 降级指纹，本批采用） | **0** |
| 全文 kind + 空 text（541 试验 1 说放开 block 0→38 的那族） | 39 |
| `_in` + 空/纯中文 text（既有 block 分支） | 0 |

落码：只对"全文 kind 残留 symbol"出 **warn**（`EV-ASSERT-SYMBOL-MAPPED`）：
空/纯中文 block **仍只对** `*_in`；已被 block 路径命中则**抑制**该 warn（单点互斥，防 541 试验 2）。

**复跑实测**：gate **完全不变** `规则 61 · 命中 141 (block=0 warn=136 advice=5)`；
`EV-CONC-001` 的 M3 两条变体 `escaped 2 → blocked 2`（warn_only）。

### B2 · M2/M3 逃逸诚实化（548 建议，落到两个算子）

病：M2 取全文第一个带 `/` 的路径、M3 取全文第一个 `contains_in` ⇒ 变异点常落在门禁**从不读**的
注释/正文，产出的"逃逸"里混着**无效提问**。
治：新增 `GATE_READ_KEYS` + `_gate_read_spans()`（只认 frontmatter 顶格门禁键
`command/artifact/artifact_producer/fixture/fixtures/run_match_file/artifacts/negative_controls/artifact_assert`）；
M2/M3 只在读取面内选点；面内找不到 ⇒ 算子返回 out_of_scope 单例（`None`）⇒ 报告记 **`n_a(out_of_scope)`**
（与 malformed 并列单列）。

**修前/修后对照**（同一批 `--cards all --operators M2,M3,M4 --limit 5`；修前用 `git show HEAD:` 还原的
旧 gate_engine+mutation_fuzz 副本实跑）：

| 指标 | 修前 | 修后 |
|---|---|---|
| escaped | **13** | **0** |
| 严格拦截（block 级） | 20 | 20（不变） |
| 含 warn 处置率 | 69.0% | **100.0%** |
| n_a(out_of_scope) | — | 3 |

**口径变化声明（不与旧数字直接比大小）**：M2 的"逃逸→拦下"来自变异点**从正文改到门禁真读字段**
（路径转大写/加 `./`/换反斜杠落到真字段后被既有 `CARD-PATH-NOT-CANONICAL` 等规则接住）；
M3 的 3 条"逃逸→n_a"来自变异点本就不在读取面（CONC-003/004/005 的首个 `contains_in` 落在
`expected:` 正文，其 `artifact_assert` 实为 `kind: contains`）——修前的 3 条**全是假逃逸**。

毒样例：P70（`contains` 残留 symbol ⇒ 须 warn **且不 block**）+ P70-阴（合法全文散文 contains 无 symbol
⇒ 零 Finding）。poison 105 → **107** 全过，双指标仍 100%/100%。

---

## 4 · Part C impact_analysis 多跳闭包（`428f4dd`）

数据源纪律：仍读 atom frontmatter 的 `relations` dict（**不是 SQLite ⇒ 不用 recursive CTE**）。
`--depth`：默认 1 = **425 原口径**（直接邻居，输出逐字不变）；N>1 = 闭包；0 = 不限。
BFS 最短跳数去重（菱形汇点只算一次，结果确定性）；环检测用**沿路径回边**（菱形依赖不算环）、
迭代 DFS（不撞递归上限）⇒ `CycleError` fail-loud（`main` 打环路并 exit 1）。

存量实跑（27 颗原子全量）：上游闭包非空 **10** · 下游闭包非空 **21** · 出现 >1 跳的原子 **18** · **环 0**。
pytest +7（链式多跳不重复 / 菱形汇点只算一次 / depth 封顶 / 自环 / 成环带环路 / 缺目标 fail-loud /
`depth=1` schema 向后兼容）。

---

## 5 · 收工总验收（fresh run，逐项实测）

| 项 | 实测 |
|---|---|
| Part 0 基线已 commit | `9092f82` ✔ |
| golden buckets | `real 12 / false_positive 0 / legacy 108 / accepted 16 / 未分类 0` ✔ |
| gate | `规则 61 条 · 命中 141 (block=0 warn=136 advice=5)` ✔ |
| replay | `confirm=56 refute=0 infra_error=0` ✔ |
| poison | `107/107`（全过）· 覆盖 11/11 · 零未覆盖 · trap_block_rate 100%(6/6) · clean_pass_rate 100%(2/2) · **RULE-COVERAGE 分子仍 36/61（不变）** ✔ |
| mutation | M2/M3/M4 5 卡：escaped 13→0（严格 20 不变）；口径变化已写明 ✔ |
| fast 套件 ×2 | 两轮全绿（81s / 71s，含 5 个 syrupy 快照）✔ |
| slow 套件 | 105 例全绿（分三批：json_output+writer_selfcheck+patch_blocks = 20 例 181s 串行；poison = 16 例 10s；其余 7 文件 = 69 例 18s）。**含 `test_golden_lock_json` 绿** ✔ |
| tool_integrity | 已重钉（`gate_engine.py` + `poison_drill.py`；5 文件基准）✔ |
| 受控目录零污染 | 无新增未跟踪产物（`_adv_*` / `References` / `_worklog_*` 属既有惯例）✔ |
| push / --no-verify / 代签 accept | 均**未**发生 ✔ |

⚠️ **slow 套件用 `-n auto` 全跑时** `test_golden_lock_json` 与 `test_stock_zero_false_positive` 会红，
**串行或分批后全绿**（已单独串行复跑验证）——属 xdist 并发抢占共享状态（gate/golden/writer 自检都
读同一批卡与 golden_state），**非本批引入的回归**；本批只改 gate 的**新增 warn 分支**（存量 0 命中）
与 mutation 算子，逐条复跑均绿。

---

## 6 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **N1 期望判决**：533 写 `refute:negative_control_passed`，实测先被 viso 形态判据以"零语义 diff"拒
   ⇒ 落 `refute:negative_control_diff`（两者同属"零判别力"refute 家族，拦截不放水）。
2. **N3 构造**：按字面"未闭合括号"构造会先被形态判据拒（新增行=1 不符 v1 纯删除形态），改为
   "anchor 内删声明行"——通过形态判据后真编译 rc=1 ⇒ 才真正命中 `_broken`（验到"写坏 ≠ 环境故障"分界）。
3. **载荷条数**：558 写"97+N7 条"，而 N7 明列**两类干净卡** ⇒ 实际 +8（N1–N6 六毒 + N7a/N7b）= 105。
4. **B2 范围**：提示词点名 M2，实测 **M3 有同款病**（CONC-003/004/005 首个 `contains_in` 在正文）
   ⇒ 同一套"门禁读取面"纪律同时落到 M2 与 M3（否则 M3 拦截率无法诚实复算）。
5. **"83 卡"**：提示词写"全量实测 83 卡"，磁盘实为 **56 张证据卡 / 118 条断言**（原子卡另有 27 颗，
   本批按证据卡口径量）；数字以实测为准。
6. **slow 套件并行**：`-n auto` 全跑有 2 例并发干扰红（串行/分批全绿），见 §5 说明。
7. **`depth=0`**：初版 `depth=0` 在闭包函数内被当成"封顶 0 跳"（返回空），已归一为"不限跳数"（与 CLI 同口径）。

## 7 · 交人项（本批未做，不擅自扩面）

1. **工作树根目录残留** `UsersASUSAppDataLocalTempreplay_…nc_nc1.s`：`replay_card` 的
   `mkdtemp(prefix="replay_")` 沙箱里，阴面编译的 `-o` 目标在 `run_commands`（shlex 规则）下
   丢了分隔符 ⇒ 写出 CWD 相对名（`_nc_path` 的 docstring 已记过同类现象）。**已手动删除**；
   用 `replay --check`、`tests/test_negative_controls.py`、poison drill 三条命令**均未复现**，
   怀疑由某次全量 fast 套件触发。**建议**：给 `_nc_rewrite` 的 `-o` 目标加引号（`"{new_out}"`），
   或让 `run_commands` 统一用 `shlex.split(posix=False)`。**未在本批顺手改核心工具**（超出 Part 边界）。
2. **N1–N6 的攻击面归类**：本批把 N1/N3/N4/N6 记 A1（记录层伪造：宣称有判别力却零判别力）、
   N2/N5 记 A2（声明-实现脱钩），N7 两类干净卡按阴性对照不计入。**归类属我的判断**，若监工
   认为该另立 V-iso 专属攻击面（如 A12），改 `ATTACK_TYPES` 一处即可。
3. **slow 套件并发红**：如上，建议后续给 golden/writer 自检类用例加 xdist 分组或资源锁，或把它们
   在 CI 里固定串行。
4. **`depth=0` 语义**：本批定为"不限跳数"（`--depth` 文档已写）。若监工更希望 0 = 直接邻居、
   用负一/`all` 表示不限，改一处判断即可。
