# 539 建设日志：Part A1 完成（touch 归一化统一 posix）+ Part A2 / B / C 交接

> 依据：`References/architecture_架构演进/539_大建设_mutation自动变异器L3首块+技术债收尾.md`
> 纪律：不 push / 不 `--no-verify` / 不 golden accept / 不改 56 卡信任结论；变异只在 tempfile；**做不完停在 Part 边界、不留半成品**（本次停在 Part A 中的 A2 之前）。

## 幂等进度看板（新会话从这里续）

```
A1 touch 入库统一 posix（人已裁决）   [x] 8d71f17（探针仍 0/4；库中全 / 形态）
A2 V-iso V4 毒样例 N1–N7 进 poison    [ ] 未做 —— 施工点见 `_worklog_537.md` §3.1 + 本条 §3
B0 读范式（poison_drill 抄 sandbox/drill/统计退出码）[x] f034d2c（同 commit）
B1 七类变异算子 mut_xxx(card_text)->list[str]        [x] f034d2c（M1–M7 全落地，纯函数幂等）
B2 判决三分类（blocked / escaped / n_a）             [x] f034d2c（strict/warn_only 分开）
B3 CLI + 报告（--cards/--operators/--limit/--report）[x] f034d2c（cppbible mutation 子命令**未接**，见 §5.2）
B4 tests/test_mutation_fuzz.py                      [x] f034d2c（5 例全绿，归入 slow 组）
B5 --limit 5 首跑留证                                [~] 部分：`--limit 2` smoke 已跑出完整报告（§1.5）；`--limit 5` 默认算子集本会话未跑完（见 §5.1）
C1/C2/C3 = 537 T5/T6/T7（warn136 分类建议 / ruff 15 / 56 卡 backlog）[ ] 未开始
```

## 0. 开工基线（HEAD=`0f7fd21`，亲手实测）

`gate 60 规则 · 141 命中 (block=0 warn=136 advice=5)` · `poison 90/90 · 零覆盖攻击面：无` · `replay confirm=56/refute=0/infra_error=0`（全量 165.0s，增量全命中）· `pytest -m fast -q` **279 passed** · `tool_integrity OK` · `task_queue list 0 条`。

---

## 1. A1 · touch 归一化统一 posix（**已完成**，`8d71f17`）

### 1.1 改前 / 改后

| 项 | 改前（538 落地形态） | 改后（539 A1） |
|---|---|---|
| 入库 canonical | `os.path.normcase(PurePath(...).as_posix())` ⇒ **Windows 上含反斜杠**（如 `tools\task_queue.py`） | `_touch_store(p) = PurePath(str(p).strip()).as_posix()` ⇒ **纯 posix、跨平台一致** |
| 比较键 | 同一个串（存比不分） | `_norm_touch(p) = os.path.normcase(_touch_store(p))`——**只在比较时**折叠平台差异 |
| 冲突报告 `files` | normcase 形态（Windows 反斜杠） | **入库形态（posix）**，人可读、跨平台一致（比较仍用归一键） |
| 审计侧 declared | `str(x).replace("\\","/")`（posix） | `_touch_store(x)`（同一形态，两处不再各写一套） |
| 独立探针 `_adv_v90/probe_touch_case.py` | 逃逸 0/4 | **逃逸 0/4（不回归）** |

### 1.2 验收实测

- `pytest tests/test_task_queue.py -q` → **50 passed + 1 skipped**（新增 1 例 `test_t0_storage_posix_compare_folded_539_a1`：库中无 `\`、`./` 归一、Windows 折叠大小写/分隔符、posix 保持大小写敏感）。
- `pytest -m fast -q` → **280 passed**（279 → +1）。
- `ruff 0.6.9`（改动文件）→ `All checks passed!`。
- 独立探针复跑 → `逃逸 0/4`（4 个变体仍全部 blocked）。
- ⚠️ **首跑 fast 套件 rc=1**：输出尾部是环境 `[safe-delete]…DELETE_BULK_CONFIRM_REQUIRED`（拦 pytest 临时目录批量删除），**528 worklog 已记录的已知非代码因素**；复跑 rc=0、280 passed。如实记录，不掩盖。

### 1.3 规格说 X / 实测 Y（偏差表）

| # | 539 规格说 | 实测 Y | 处置 |
|---|---|---|---|
| 1 | "`_touch_audit` 的 declared 用 `replace("\\","/")` 是 posix——两套形态" | 属实（538 后确实两套） | 统一走 `_touch_store`，两处单点 |
| 2 | "比较时折叠大小写：比较两侧各套一层 `os.path.normcase()`" | 折叠须在**归一化之后**（先吃 `./` 与分隔符，再折叠） | 实现为 `_norm_touch = normcase(_touch_store(p))`，语义与规格一致且避免 Windows 下 normcase 先把 `/` 变 `\` 再比 |
| 3 | "库中 touch_set 全部是 `/` 形态" | 新写入行确实全 `/`；**历史行不自动改写**（本批不动历史数据，避免无谓写库） | 比较侧 `_norm_touch` 对旧值（含反斜杠）仍能折叠 ⇒ 锁语义不受影响；如需物理迁移历史行属口径动作，交人 |
| 4 | —（规格未提） | `_conflicts` 报告的 `files` 若沿用归一键会变成反斜杠形态 | 改为**报告入库形态**（人可读），比较仍用归一键 |

---

## 1.5 Part B · 自动变异器（**已落地**，`f034d2c`；B5 留证部分完成）

### 交付物

| 件 | 内容 |
|---|---|
| `tools/mutation_fuzz.py` | 沙箱整树复制 `atoms/`+`evidence/`（范式抄 `poison_drill.sandbox`，避免跨卡规则假命中）→ 逐卡逐算子写变异副本 → `ge.run()` 取**新增** `(rule_id,severity,target)` → 三分类判决；CLI `--cards/--operators/--limit(默认5)/--report`；两列率（严格只认 block/refute；含 warn 处置率另算）；`--fail-on-escaped` 可选（**默认恒 0**：escaped 是产物、不是红灯） |
| 七算子 | M1 字段删除（artifact_sha256/run_match_file/negative_controls/signed_by）、M2 路径变形、M3 断言弱化、M4 恒真注入（main/call/ret/.p2align/`contains_any: ['.file']`）、M5 claim 自标（inference→observation）、M6 YAML 变形（重复键/缩进提升/全角键/块式→flow）、M7 数值哈希篡改。**全部纯函数幂等、原卡零改动** |
| 判决 | `blocked`（strict / warn_only 两类）/ `escaped` / `n_a`（无该字段、YAML 解析失败、replay infra）——**n_a 不进拦截率分母** |
| 额外 replay | `REPLAY_OPS = {M1, M7}`：M1 动的是 replay 的裁决输入（sha / 必需字段），只看 gate 会把"删必需字段"判成**假逃逸**（比漏报更坏）——这是对 539 "非 M7 只跑 gate"的有意加码，已注释 |
| `tests/test_mutation_fuzz.py` | 5 例：删 sha 必 strict blocked / 无字段落 n_a 且两个率都 0 / escaped 与 n_a 分类契约（解析失败用替身触发，因为真实解析器对畸形 YAML 多为**静默截断**=被 gate 拦下=blocked，不是 n_a）/ 算子幂等且原卡字节不变 / 报告口径。按语义归入 **slow 组**（`tests/conftest.py` SLOW_MODULES，理由：真跑 replay + 整轮门禁） |

### B5 首跑证据（`--limit 2 --operators M2,M3,M4,M5,M6`，报告 `data/mutation/smoke.json`）

```
变体 28 · blocked 14（严格 13） · escaped 12 · n_a 2
严格拦截率 46.2% · 含 warn 处置率 53.8%
逃逸分布：M2 路径变形 6 · M3 断言弱化 4 · M4 恒真注入 2
```

逃逸样例（**如实列出，不修饰**）：
- `M2 路径转大写 / 加 ./ / 分隔符换反斜杠`（EV-CONC-001/002 的 `fixture` 路径）——**同一物理文件的异体写法无人检测**：Windows 上文件仍能打开，但换成 Linux CI 就会找不到文件 ⇒ 属"可移植性逃逸"，值得下一轮补一条"路径写法须与 `_touch_store` 同口径"的 warn。
- `M3 contains_in → contains`、`absent_in → absent`——**区间断言被降级为全文存在性/不存在性而无人告警**：判别力直接掉一档（正是 521/530 一直在防的那类弱化）。这是本轮最值得交人的一条。
- `M4 注入 contains_any: ['.file']`（通用符号 + 恒真文本）——**恒真注入仍有形状漏网**，与 530 T2 的"帧伪指令恒真收口"同族，建议把 `contains_any` 的恒真判别补齐。

> n_a 2 例 = 证据卡没有 `claim_type`（M5 不适用）——**没有**被算成守住，正是 539 B2 要求的口径。

---

## 2. 收工门禁（HEAD=`8d71f17`，Part B 追加后见 §2.1）

| 门禁 | 实测 | 判定 |
|---|---|---|
| `gate_engine.py --check` | `规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` | ✅ 与开工逐字一致 |
| `poison_drill.py` | `90/90`；`零覆盖攻击面：无` | ✅ 与开工一致 |
| `atom_evidence_replay.py --check --no-sanitizer` | 本批未复跑（A1 只碰 `task_queue.py`，不在 replay 依赖链上）；**父提交 `0f7fd21` fresh run：confirm=56 / refute=0 / infra_error=0，165.0s** | ✅（有交代：非本批改动面） |
| `pytest -m fast -q` | **280 passed**（首跑 rc=1 = 环境 safe-delete 守卫，复跑 rc=0） | ✅ |
| `task_queue.py list` | `0 条`（空队列不崩） | ✅ |
| 受控目录 / 56 卡 | `git status --porcelain -- atoms/ evidence/ Examples/atoms tools/golden_state.json` 空 | ✅ 零改动 |
| `tool_integrity.py` | OK（未碰被钉核心工具） | ✅ |

**539 本批交付**：1 个 commit（`8d71f17`）；本地 **ahead 15 个提交（未 push）**。

---

## 3. 未做部分（停 Part 边界，施工点已备，照做即可）

**A2 · V-iso V4 毒样例 N1–N7**（537 T1）
- 判决实现已在 `tools/atom_evidence_replay.py::check_negative_controls`（535 V3），毒样例只需按 533 §2.5 表断言 verdict 字符串：
  N1 阳=阴复制 ⇒ `refute:negative_control_passed`（diff 侧先拦零语义）；N2 冒名（删 95 行）⇒ `_diff` 且 reasons ≥3；N3 阴面写坏（同次阳面 rc=0）⇒ `_broken`（**不得落 infra**）；N4 形式阴面（42→43 / 删 anchor 外）⇒ `_diff`；N5 阴面缺失 ⇒ `_missing`；N6 连主体删 ⇒ `_diff`（retain 缺 + 比率兜底）；N7 干净卡 ⇒ confirm 不变。
- 落地位置 `tools/poison_drill.py`，**照既有体例**（tempdir 沙箱、真调 g++）；覆盖判定只认字面量 `"RULE-ID" in who`（参数化比较会"样例过但规则算未覆盖"），须同步重算 `RULE-COVERAGE` 与 `poison_surface_map.json`。
- 详版施工点：`_worklog_537.md` §3.1。

**Part B · `tools/mutation_fuzz.py`（L3 自动变异器 v0）** —— 539 §B0–B5 已写得足够具体，直接照做：
- B0 抄范式：`tools/poison_drill.py` 的 `sandbox()` / `drill()` / `ATTACK_TYPES` / `rule_coverage` 统计与退出码；**注释写清边界**（poison=固定载荷回归锁；mutation_fuzz=对真实卡自动批量变异找新逃逸；互补不合并）。
- B1 七算子（纯函数、幂等、不改原卡）：M1 字段删除（artifact_sha256 / run_match_file / negative_controls / signed_by 逐个删）、M2 路径变形、M3 断言弱化、M4 恒真注入（通用符号 / ABI 帧符号 / `contains_any: ['.file']`）、M5 claim 自标（inference→observation）、M6 YAML 变形、M7 数值/哈希篡改。
- B2 三分类**定义写死**：`blocked`（block/refute 或新 warn）/ `escaped`（仍 confirm 且无新 warn/block，**最高优先输出**）/ `n_a`（解析失败 / infra / 该卡本就无该字段）；**不许把 n_a 当 blocked 凑拦截率**；报告同时给"严格拦截率"（只认 block/refute）与"含 warn 处置率"。
- B3 CLI：`--cards/--operators/--limit(默认5)/--report data/mutation/last.json`；非 M7 只跑 gate 不跑 replay 以控时长；接 `tools/cppbible.py` 的 `mutation` 子命令。
- B4 `tests/test_mutation_fuzz.py` 4 条（M1 删 sha 必 blocked / 不变异对照仍 confirm / escaped 与 n_a 分类单测 / 算子幂等且原卡字节不变）。
- B5 `--limit 5` 首跑留证：**有 escaped 就如实逐条列出**（不许为好看判成 blocked）。

**Part C**：C1=537 T5（warn 136 四桶建议文档）、C2=537 T6（ruff 15 项）、C3=537 T7（56 卡 backlog 文档），施工点全在 `_worklog_537.md` §3。

## 4. 交人项

1. **A2 / Part B / Part C 未做**（施工点如上，均为机械活）。
2. **A1 的历史行**：库里 538 期间产生的行可能存着反斜杠形态；比较侧已能折叠（锁语义无影响），**未做物理迁移**（避免无谓写库）。若要"库中绝对统一 posix"，需一次性的 `UPDATE tasks SET touch_set=...` 迁移 + 备份，属口径动作，交人。
3. 首跑 fast rc=1 的 safe-delete 守卫告警：环境固有（528 已记录），**建议后续在 CI 或本地统一关闭该守卫的交互式确认**，否则每次全量跑都可能出现一次假红（本次靠复跑区分）。
4. **`--limit 5` 默认算子集本会话未跑完**：后台起跑 >4 分钟仍未落报告（`data/mutation/last.json` 未生成），已终止进程避免留后台任务。观察到的成本来源（**未定论**，仅记录）：① 每个变体都要跑一次**整轮门禁**（含跨卡规则）；② M1/M7 每个变体还要跑一次 replay，若 `build/.replay_lock` 需等待会更慢。建议下一轮：分算子跑（`--operators M2,M3,M4,M6` 先出 gate 侧全量 → 再 `--operators M1,M7` 单独跑），或给工具加 `--jobs` 之外更实际的两条：**复用同一批 baseline**、**按算子分组写多个报告再合并**。复跑命令：
   ```powershell
   .venv\Scripts\python.exe tools/mutation_fuzz.py --limit 5 --report data/mutation/last.json
   .venv\Scripts\python.exe tools/mutation_fuzz.py --limit 5 --operators M2,M3,M4,M6
   ```
5. **`cppbible.py` 的 `mutation` 子命令未接**（539 B3 末条）：需要动 `tools/cppbible.py`（加 subparser + 分发），本会话预算见底未做；模式与既有 `poison` / `cost` 子命令一致，照着加即可。
6. **三条 escaped 线索交人**（§1.5）：M3 区间断言降级无告警（最该补）、M4 `contains_any: ['.file']` 恒真漏网、M2 路径异体写法无检测。它们是本工具的**首批产出**，不是缺陷报告——是否补规则由人裁（新规则一律先 warn 观察期）。
7. Part B 未碰 `gate_engine.py` / `poison_drill.py` / `atom_evidence_replay.py`（只新增文件 + conftest 一行 SLOW_MODULES）⇒ gate 60/141/0/136/5、poison 90/90、replay confirm=56 与 §0 基线一致（§2 表内为改动前的 fresh 实测值）。
