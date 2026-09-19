# 539 · 大建设批：mutation_fuzz 自动变异器（L3 第一块）+ 技术债收尾

> 你是建设苦力。本批主线：把这几轮**手工对抗**（536/521/500/529 积累的变异模式）沉淀成一个**零 LLM、可重复跑的自动变异器** `tools/mutation_fuzz.py`——这是 L3「系统检验系统」的第一块，也是把"人手工造探针找逃逸"升级成"机器批量找逃逸"。Part A 先清两笔快债，Part B 是核心，Part C 收尾。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`0f7fd21`。门禁用 `.venv\Scripts\python.exe`。**动手前先 Read 目标源码（行号会漂移），规格与磁盘冲突以磁盘为准并记 worklog。做不完停在 Part 边界，不留半成品。**

## 开工基线（亲手量，收工对比零回归）
gate（60 规则 / block=0 / warn=136）、poison（90/90）、replay（confirm=56）、`pytest -m fast -q`（约 279）。

---

# Part A · 两笔快债（先做，各独立 commit）

## A1 · touch 归一化统一 posix 入库（538 交人裁决项，已裁决：统一 posix）
- 现状：`_norm_touch` 直接返回 `os.path.normcase(...)`，Windows 上 canonical 形态含反斜杠；而 `_touch_audit` 的 declared 用 `replace("\\","/")` 是 posix——两套形态。
- 改法：拆两步——**入库存 posix**：`PurePath(str(p).strip()).as_posix()`；**比较时折叠大小写**：比较两侧各套一层 `os.path.normcase()`。即"存的是纯斜杠，比的时候才平台相关"。
- 验收：`_adv_v90/probe_touch_case.py` 仍 0/4 逃逸；库中 touch_set 全部是 `/` 形态；49+1 pytest 不回归。独立 commit。

## A2 · V-iso V4 毒样例 N1–N7 进 poison（537 T1）
- 照 `_worklog_537.md §3` 施工点 + `_arch_v2_round2/probe_fence_iso/`：为 viso_diff 判据每条违反造应 block/refute 的毒样例（冒名程序/42→43 替换/删错位置/注释走私/连循环带 fence 删/retain 被注释/符号换 static）。判决实现已在 535 V3 `check_negative_controls`，只补载荷。
- 注意 poison 覆盖正则只认字面量 `"RULE-ID" in who`。验收：poison 全过、RULE-COVERAGE 无新增 uncovered。独立 commit。

---

# Part B · 核心：tools/mutation_fuzz.py（L3 自动变异器 v0）

## B0 · 先读两个范式，别重造
- `tools/poison_drill.py`：抄它的 `sandbox()`（临时目录隔离）、`drill()` 主循环、`ATTACK_TYPES`/`attack_type_stats`/`rule_coverage` 的统计与退出码范式。
- **边界写清（注释里）**：poison_drill = 人工写死的固定载荷，测"规则有没有覆盖已知攻击"（回归锁）；mutation_fuzz = 对**真实证据卡自动批量变异**，找"毒样例没覆盖的新逃逸"。两者互补，不合并。

## B1 · 七类变异算子（每类一个纯函数 `mut_xxx(card_text) -> list[str]`，返回多个变异后卡文本）
全部来自历史手工对抗，不发明新理论：
- **M1 字段删除**：删 `artifact_sha256` / `run_match_file` / `negative_controls` / `signed_by`（逐个删，各产一个变体）。
- **M2 路径变形**：卡内路径做大小写翻转 / 加 `./` / 正反斜杠互换（复用 A1 的归一化思路反向构造）。
- **M3 断言弱化**：`contains_in`→`contains`、删断言里的 `-Werror`、量化断言（min/max/计数）改成纯存在性。
- **M4 恒真注入**：注入通用符号（main/call/ret）、ABI 帧符号（.p2align/.seh_endproc/.cfi_startproc）、`contains_any: ['.file']`。
- **M5 claim 自标**：`claim_type: inference`→`observation`（测 OBSERVATION-LIVENESS/NEEDS-ARTIFACT 是否拦）。
- **M6 YAML 变形**：重复键、缩进提升一个键、全角键名、flow 写法（复刻 E07 缩进走私族）。
- **M7 数值/哈希篡改**：计数 ±1、sha256 改一位 hex。
> 算子必须**幂等、不改原卡**：输入卡文本，输出变异副本字符串；原卡只读。

## B2 · 判决三分类（核心逻辑，定义写死）
对每个 (卡, 算子, 变体)：把变异副本写进 sandbox 临时目录，跑 gate（M7 涉及工件的额外跑 replay），与**原卡 verdict（confirm）**对比：
- `blocked`：变异后被 block/refute，或产生新的命中 warn —— **守住（✓）**。
- `escaped`：变异后**仍 confirm 且无任何新 warn/block** —— **逃逸（✗，最高优先输出）**。
- `n_a`：变异导致 YAML 解析失败 / infra_error / 该卡本就没有被变异的字段 —— 不适用，**不算守住也不算逃逸**（不许把 n_a 当 blocked 凑拦截率）。
> 拦截率口径同 v80：warn 只算"可见化"单列，严格拦截只认 block/refute；报告同时给"严格拦截率"和"含 warn 处置率"两个数。

## B3 · CLI 与报告
- `python tools/mutation_fuzz.py --cards <glob或all> --operators M1,M2.. --limit N --report data/mutation/last.json`
- 默认 `--limit 5` 小批先跑通；`all` 才全量（56×7 约 392 变体，注意耗时：非 M7 只跑 gate 不跑 replay 以控时长）。
- 输出：控制台汇总（变体总数 / blocked / escaped / n_a / 严格拦截率）+ JSON 报告（每个 escaped 逐条挂：卡 id、算子、变异点、复现命令、原 verdict vs 变异 verdict）。
- 接入 `tools/cppbible.py` 统一入口（`mutation` 子命令），风格对齐既有子命令。

## B4 · pytest（tests/test_mutation_fuzz.py）
小而确定，不跑全量：
1. M1 删 `artifact_sha256` 的变体必被判 blocked（用 1 张真实小卡）。
2. 不变异的对照卡仍 confirm（证明工具不会把好卡误报成逃逸）。
3. 判决分类单测：构造"仍 confirm 无 warn"的假结果必落 escaped；构造解析失败必落 n_a（防把 n_a 当 blocked）。
4. 算子纯函数性：连跑两次输出一致、原卡文本字节不变。
验收：新 pytest 全绿 + 既有 fast 套件零回归。

## B5 · 首跑留证
`--limit 5` 真跑一次，把结果写进 worklog：**有 escaped 就如实逐条列出（这正是工具价值，不许为"好看"把 escaped 判成 blocked）**；全 blocked 也如实报。独立 commit（B1-B4 一个 commit、B5 报告若落 data/ 单独评估是否 gitignore）。

---

# Part C · 技术债收尾（时间够再做，各独立 commit）
- **C1（=537 T5）** warn 136 四桶分类建议文档 `docs/kernel/warn_136_分类建议.md`，只记录不 --accept。
- **C2（=537 T6）** CI ruff 15 项，逐个最小修、会动行为的跳过交人（会动 8 个文件，逐个判语义）。
- **C3（=537 T7）** V-iso 56 卡 backlog `docs/kernel/viso_migration_backlog.md`，只排队不改卡。
施工点细节都在 `_worklog_537.md §3`。

---

## 收工
fresh 全量门禁报实测终值；写 `_worklog_539.md`（A1 改前改后探针、B5 首跑 escaped 清单、每条 commit、规格偏差表、交人项）。
**不 push、不 --no-verify、不 golden accept、不改 56 卡信任结论；mutation 所有变异只在 tempfile，atoms/evidence 原卡零改动（收工 git status 自证）。**
