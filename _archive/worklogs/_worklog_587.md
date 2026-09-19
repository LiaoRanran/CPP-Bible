# _worklog_587 · M6 矩阵「非法值替换」逃逸收口（matrix 值校验硬化，warn 起步）

> 过程文档，**按惯例不入库**（未 commit、未 push、未 golden accept、未替人签）。
> 解释器 `.venv\Scripts\python.exe`；串行取证；`$LASTEXITCODE` 定论。

## 任务 0 · 先量（只出事实，不落规则）—— commit `ae0aa02`

全量扫描 56 张证据卡 frontmatter 的 `matrix`，逐元素去重落
`data/matrix_value_inventory.md`（机器生成、只读台账）。

| 键 | 去重值 | 真实分布 |
|---|---|---|
| compiler | 8 | `GCC 15.3.0`(40 卡)、`GCC 15.3.0 (MinGW-w64)`(16)、`GCC 14.2.0 (WSL)`(9)、`GCC 13.3.0 (WSL)`(8)、`GCC 13.1.0`(3)、`GCC 8.1.0`(2)、`GCC 14.2.0 (WSL —— 同驱动跑 libstdc++ 与 libc++ 各一次)`(1)、**`Clang (ubuntu-latest runner 默认)`(1，EV-UB-001)** |
| std | 5 | c++11(2) / c++14(4) / c++17(6) / c++20(2) / c++23(54) |
| opt | 5 | `-O2`(54)、`-O0`(22)、**`-O1（sanitizer 观测档）`**、**`-O2（零依赖判据档）`**、**`-O2（本卡）/ -O1（同夹具…）`** |
| arch | 1 | `x86-64`（56 卡全有） |
| stdlib | 6 | 可选键，**本批不校验** |

**0.2 终稿口径**（由真实分布反推，非拍脑袋）：先剥**半角/全角**括号注释、再按 `/` 拆段逐段校验——
- `std` `^(gnu|c)\+\+(98|03|11|14|17|20|23|26)$`
- `opt` `^-O([0-3sgz]|fast)$`
- `arch` 限存量真实出现集合（仅 `x86-64`）
- `compiler` 带括号注释 ⇒ 只要求注释外的核心含族名关键词（gcc/g++/clang/clang++/msvc，大小写不敏感）；
  不带注释 ⇒ 族名关键词 **且** 至少一段版本数字
- `stdlib` / `sanitizer` / `sanitizer_note` 不校验

**0.3 零误伤前置自证**：该口径对存量 56 卡空跑 **0 命中**（草稿口径曾 4 命中，已按真实分布修正）。

## 任务 1 · 发现器：补「非法值替换」变异点（先量逃逸）—— commit `01122e3`

`_mut_matrix_values()` 保留 586 的删键变异，新增四键非法值替换（只换 flow 列表**首元素**，
键与列表结构不变、正文逐字不动）：std→`c++99`、opt→`-O9`、arch→`z80-nonexistent`、
compiler→`totally-not-a-compiler xyz`。切分逗号时跳过半角/全角括号内的逗号（防切坏 `Clang (ubuntu-latest runner 默认)`）。

**修前实测**（`--cards all --limit 999 --operators M6 --jobs 4`，717 变体）：

| 键 | 变体 | 逃逸 | 说明 |
|---|---|---|---|
| compiler | 55 | **39** | 另 16 个被既有 `EV-MATRIX-UNBACKED`（warn）处置，非本次新增规则之功 |
| std | 55 | **55** | |
| opt | 55 | **55** | |
| arch | 55 | **55** | |
| **合计** | **220** | **204** | 586 估约 165，**实跑 204** |

## 任务 2 · 门禁：matrix 值校验（warn 起步，逐元素）—— commit `ad4de8c`

`check_evidence_matrix()`：缺键 **block**（语义不变）之后新增**值校验 warn**（`EV-MATRIX` rule_id，
文案 `matrix.<键> 含非法值: <值>（疑似被弱化/伪造）`）；键存在但非列表 ⇒ 也 warn。
**缺键 block 与值非法 warn 不混淆。**

- 存量零误伤（硬门）：真实 56 卡 `gate --check` = **63 条 / 191 命中 (block=0 warn=186 advice=5) 逐字不变**，新校验存量 **0 命中**。
- **修后实测**（同参数）：

| 键 | 变体 | 修前逃逸 | 修后逃逸 |
|---|---|---|---|
| compiler | 55 | 39 | **0** |
| std | 55 | 55 | **0** |
| opt | 55 | 55 | **0** |
| arch | 55 | 55 | **0** |
| **合计** | **220** | **204** | **0** |

M6 整体 `escaped 204 → 0`、`blocked 505 → 709`、`treated_rate 0.7123 → 1.0`；等价变异体 8 仍单列不进分母。
观察期保持 **warn，不升 block**（升级交监工裁决）。

## 任务 3 · 毒样例 + 回归锁 + 基线重冻结 + 收工 —— commit `6ff2e1e`

- 毒样例 **3 阳 + 3 阴**：P77（std `c++99`）、P78（opt `-O9`）、P79（compiler `totally-not-a-compiler xyz`）
  各须命中 EV-MATRIX **warn 不 block**；P77-阴 / P78-阴 / P79-阴 为同构且取值全合法（取自台账真实分布）的卡，须放行。
  登记 ATTACK_TYPES：P77/P78/P79 → **A2**（声明的编译环境与任何真实可跑环境脱钩）。
- 回归锁：`test_matrix_illegal_values_warn_per_key`（四键非法值各命中一次且为 warn + 合法值放行）、
  `test_matrix_stock_real_values_all_pass`（台账**全部**存量真实取值含全角注释/`并列`/CI runner 默认 ⇒ 0 命中）、
  `test_matrix_non_list_value_warns`。顺带修 `re.I` → `re.IGNORECASE`（ruff FURB167）。
- **基线重冻结（非回归，新增变异点 + 值校验收口）**：全量 all 算子 jobs4
  `variants=1568 blocked=1374 escaped=1 n_a=185 strict=784 equivalent_invalid=8`
  ⇒ 可判分母 **1155 → 1375**，逃逸率契约 `1/1155 → 1/1375`（escaped 仍 1 = M1 那条 TCE，本批不做）。
  同步 `full_baseline_v5.json`（note 增补第 (3) 条）、`test_metrics_collector_curves.py`、
  `test_poison_exemptions_581.py`（行为覆盖 38→39）、`test_output_snapshots.ambr`（RULE-COVERAGE 38→39）、
  重跑 `--write-surface-map`。

## 任务 4 · `.gitignore` 独立 commit —— `8e6bf24`

`git check-ignore .env` → 输出 `.env`（exit 0）；`git ls-files | grep '^\.env$'` → 无输出；
`git add .gitignore`（仅此 1 文件 3 行），message `chore: gitignore .env 本地密钥`。`.env` 本身永不提交。

## 收工总验收（fresh，串行，退出码定论）

| 项 | 结果 |
|---|---|
| `tool_integrity.py --check` | **exit 0**（已 `--update` 重钉，同 commit 带 `.tool_checksums`） |
| `gate_engine.py --check` | **exit 0** · 63 条规则 / **191 命中 (block=0 warn=186 advice=5) 逐字不变** |
| `poison_drill.py` | **exit 0** · **124/124**（118+6）· V-iso 双指标 **100%/100%**（6/6、2/2）· RULE-COVERAGE **39/63** · 表观 100.0% · 诚实 **95.2%（60/63）未下降** · 零覆盖攻击面 无 |
| `atom_evidence_replay.py --check` | **exit 0** · confirm=56 refute=0 infra_error=0 |
| `pytest -m "not slow" -n auto` | **exit 0**（1 skip、5 snapshots） |
| `pytest -m slow -n0` | **exit 1，唯一失败 = 已知预期红 `test_golden_lock_json`**（golden 待人审 accept，苦力不自签） |
| `git diff --quiet -- atoms evidence Examples` | **exit 0** |
| ruff（改动文件，族 E4,E7,E9,F,I001,FURB167） | **新增告警 0**（余 3 条为 `poison_drill.py` 存量：I001、E702×2） |

## 偏差表（提示词假设 X / 实测 Y）

| # | 提示词假设 | 实测 | 处理 |
|---|---|---|---|
| 1 | 非法值逃逸"预估约 165" | **204**（变体 220） | 以实跑为准，逐键列出 |
| 2 | compiler 口径"须含族名 **且** 版本数字" | EV-UB-001 `Clang (ubuntu-latest runner 默认)`（全库唯一）有族名无版本 | 按任务书 0.2「括号注释一律放行」取「带注释 ⇒ 只要求族名」⇒ 存量 0 命中；**收紧则 +1 warn 违反 191**，交人裁决 |
| 3 | opt 口径 `^-O[0-3sgz]$\|-Ofast` | 存量 3 个值带**全角**括号注释、1 个值含 `/` 并列 | 扩展为"剥半角/全角括号 + 按 `/` 拆段"，`-O9` 照样拦 |
| 4 | 任务 1.3"若基线/冻结结论变化就重冻结" | 修前 204 逃逸属**过渡态** | 不在任务 1 冻中间态，任务 3 一次性重冻结并注明「非回归，新增变异点 + 值校验收口」 |
| 5 | （未预想）M6 删键正则覆盖 56 卡 | **55/56**：EV-MEM-004 的 `matrix:` 行带尾注释 ⇒ 正则匹配不到 ⇒ 该卡无 matrix 变异体 | 本批**未改**（改它会新增变体、动基线）；报告交人 |
| 6 | （未预想）compiler 非法值应全逃逸 | 55 中 **16 个**被既有 `EV-MATRIX-UNBACKED`（warn）处置，真逃逸 39 | 如实分列，不把既有规则之功算到新规则头上 |
| 7 | 快照/契约数字保持不变 | 新增毒载荷 ⇒ 行为覆盖 38→39、可判分母 1155→1375 | 同步更新四处并注明"非回归" |
| 8 | ruff 新增告警 0 | 自查发现 `re.I` 触发 **FURB167** | 已改 `re.IGNORECASE`，收工复跑新增告警 0 |

## 交人（未自作主张）

1. **compiler 版本数字要不要强制**：EV-UB-001 的 `Clang (ubuntu-latest runner 默认)` 是唯一反例；
   强制版本数字 ⇒ 存量 +1 warn ⇒ 破坏 191 零误伤 ⇒ 须监工裁决（或改卡补版本号，那是人审动作）。
2. **值校验 warn → block 升级**：本批观察期 warn，升级交人。
3. **EV-MEM-004 的 `matrix:` 尾注释导致 M6 无变异体**（既有 586 正则的漏网点）：建议下批修正则并同批重冻结。
4. **M1 那条 TCE 逃逸（escaped=1）** 本批不做。
5. 未做：PoC#1/#3、585 冻结项（仓内第二锚、人签通道）、ruff 余族大清扫。
