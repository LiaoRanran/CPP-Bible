# _worklog_472 · v5 渗透修复批执行记录（2026-09-14）

> 零上下文接手标准：每项含 ①当前代码状态 ②未完成原因 ③下一步精确命令。
> 输入：`_adv_v80/REPORT.md`（v5 独立对抗渗透，470 修复后复测）+ v5 的 7 条修复建议。
> 口径纪律：**可见化 ≠ 拦住**——v5 判定「严格拦截 = 卡无法直推 confirm/verified」。

## 0. 开工基线 vs 收工终值（全部实跑）

| 项 | 开工（470 收工态） | 收工（本轮终值） | 判读 |
|---|---|---|---|
| gate 规则数 | 48 | **50**（+ATOM-REL-UNKNOWN +EV-FIXTURE-NO-ECHO-DATA） | 472 P1-4/P1-2 |
| gate --check | block=0 warn=32 advice=5 | **block=0 warn=32 advice=5** | 零净增量（升格未误伤） |
| poison | 52/52 · RULE-COVERAGE 22/48+27 | **61/61 · 24/50+27 · 攻击面 11/11** | +9 载荷（P45–P57） |
| pytest | 153 例 | **272 点全绿** | +119 点（新测试文件 7 个） |
| replay --check | confirm=56 | **confirm=56 refute=0 infra_error=0** | 每卡含独立重编译 |
| writer_selfcheck | 56 卡 0 fail | **56 卡 0 fail** | 一致 |
| 424 攻击面台账 | 无 | **`tools/poison_surface_map.json`（11/11）** | 本轮新增产物 |

## 1. 待办状态（v5 建议 7 条 + 本轮收尾 3 项）

- [x] **P0-1 / N1 僵尸锁 DoS**（commit `4a93745`）
- [x] **P0-2 / N2 全局恒真断言盲区**（commit `ae39d0b`）
- [x] **P0-4 / N4 工件快照幂等还原**（commit `842c958`）
- [x] **P1-2 / E05 cat 式证据 exp→warn**（commit `d548b8d`，含 `test_p0b_echo` 锁同步见 §2.6）
- [x] **P1-3 / E16 闪卡过滤 draft 原子**（commit `152413f` + 锁同步 `28e4632`）
- [x] **P1-4 / N3 refutes 归一 + 未知关系类型可见**（commit `cebc1be` + `87d3ce3`）
- [x] **P1-1 / E10 零诊断规则升 block**（本轮补做，§2.5）
- [x] **424 武器面台账落盘 + `--by-type` 口径单点化**（本轮补做，§2.7）
- [ ] **P0-3 / E12 签收 git author 绑定**（未做，需人裁决范围 → §4.1）
- [x] 收工门禁 fresh run（§3）

## 2. 各子项摘要

### 2.1 N1 僵尸锁（commit 4a93745）
- **代码态**：`replay._acquire_replay_lock` 现写入 pid 并做存活检测（`os.kill(pid,0)` / Windows `OpenProcess`）；`stale_after=300s`（原 3600）；`atexit`/signal 释放。取锁参数 `wait_timeout` 与 `stale_after` 分离（470 教训）。
- **回归锁**：`tests/test_p0g_lock.py` + poison **P45**（pid 已死 → 立即接管，实测 0.0s）/ **P46**（活锁不得被抢，二次取锁须超时）。
- **未完成原因**：无。

### 2.2 N2 全局恒真断言（commit ae39d0b）
- **代码态**：判别力统计从「仅 contains_in 区间」扩到 `contains`/`contains_any` 全局断言（样板伪指令命中率 → 零信息即 refute）。
- **回归锁**：poison **P47**（`contains_any` 命中全为 `.file`/`.text` 样板 ⇒ 判无判别力）/ **P48-阴**（命中含 `ret` 非样板 ⇒ 按原语义放行）。
- **口径**：absent_in 不做频率统计（缺席是强断言）。

### 2.3 N4 工件事务化（commit 842c958）
- **代码态**：replay 生成工件前先落盘快照，还原走幂等路径（中断不丢工件）。
- **回归锁**：poison **P51**（快照幂等还原 = ORIGINAL-BYTES）/ **P52-阴**（正常路径不留 `.bak` 残留）。
- **注**：`Examples/atoms/_atom_alloc_arena.asm` 被清空是**本轮开工前既有事故**（v5 报告 N4），修复机制已落地；该工件本身由 replay 重生成即可恢复（本轮 replay 全量 56 confirm 已验证）。

### 2.4 N3 关系键（commit cebc1be + 87d3ce3）
- **代码态**：`CONFLICT_SYNONYMS` 扩 `refutes`/`denies`；新增 `ATOM-REL-UNKNOWN`（warn）——表外关系类型**显形**，结束「枚举范式静默丢弃」。
- **回归锁**：poison **P55**（refutes 归一后检出矛盾）/ **P56**（未知类型可见）；pytest 同名测试组。

### 2.5 P1-1 零诊断升 block（本轮补做，v5 建议 5 剩余项）
- **背景**：v5 建议 5 原文「把 warn/experimental **升到 block**」；P1-2 只做了 E05 的 exp→warn，E10 仍停在 warn ⇒ 属「没跑完的这一轮」。
- **代码态**：`EV-ZERO-DIAG-WERROR` 两处 Finding 与注册表 sev 全部 warn→**block**（`check_evidence_zero_diag_werror`）。
- **升格依据（三条，全部实测）**：① warn 只可见化，卡照样 confirm 直推 verified（v5 E10a/b 实证）；② 措辞「零诊断」缺 `-Werror` ⇒ 判据**不可机器判定**（`compile_rc` 不看警告）⇒ 不可复算判据不得放行（与毒样例 P11 同义）；③ 存量 56 卡 **0 命中**（全库仅 EV-LANG-001 提及且已带 `-Werror`）⇒ 零误伤。
- **同步面**：`tests/test_p0f_zerodiag.py`（2 测试改名+断言）、`tests/test_gate_engine.py`（2 处）、`docs/kernel/M2_empirical.md`、poison **P11**（升为「须 block」双判据：命中 + 级别）。
- **回退（一行）**：`_register_all` 里 `"EV-ZERO-DIAG-WERROR": "block"` 及两处 Finding 改回 `"warn"`——无任何存量卡依赖。

### 2.6 test_p0b_echo 锁同步（本轮修）
- **问题**：`d548b8d`（P1-2 升 warn）后 `tests/test_p0b_echo.py::test_not_registered_in_gate_rules` 仍断言「不得注册」⇒ pytest 全套长红（升格遗漏同步）。
- **代码态**：改为 `test_promoted_to_warn_rule`——断言「已注册 + severity==warn + 命中产出 Finding 且不升 block」。

### 2.7 424 攻击面台账（本轮补做）
- **问题（双）**：① `--by-type` 用**静态前缀表**计数（46 条）与主流程实测（49 条）各说各话（同前缀多载荷被压成 1）；② A11 已入表，但文案/统计仍写 A1-A10，且 410 要求的产物 `tools/poison_surface_map.json` 从未落盘。
- **代码态**：新增 `ATTACK_TYPE_LABELS`（A1-A11 逐类标签，模块级 assert 与清单同源）、`unknown_attack_types()`（未登记前缀 `A?` **显形**，不再静默折算）、`build_surface_map()/write_surface_map()/load_surface_map()`；`--by-type` **改读台账**（口径单点化 = 实测 results），`--write-surface-map` 显式落盘（主流程/CI 不写，避免工作区变脏）；`--json` 增 `attack_surface` 段。
- **产物**：`tools/poison_surface_map.json`（61 载荷含 12 阴性对照 · 11/11 覆盖 · rule_coverage 24/50+27）。
- **回归锁**：`tests/test_poison_attack_type.py` +7 点（结构/防过期/往返/口径一致/未登记显形）。

### 2.8 分类学错位（**本轮新发现，待裁决**）
- **现象**：`ATTACK_TYPES` 的 A1-A10 与 `References/…/409_*.md` 原表**语义错位**——409 定义 `A4=注释伪造`、`A6=未声明键`、`A10=门禁假阳性`；代码实际 `A4=时序穿链`、`A6=解析走私`、`A10=供应链与工件完整性`。仅 A8（间接注入）/A9（规则逃逸）与 409 一致。A11 为新增（409 原文授权「全新攻击面则更新分类学 A11…」）。
- **性质**：非 bug（编号体系可演进），但**同名异义**会让跨文档引用失真（如 410 提示词按 409 口径写的 P→A 映射表）。
- **本轮处置**：不擅自回改（会砸掉自洽的测试断言与已入库映射），改为在代码注释、台账 `note` 字段、本文件**显式记录**。
- **裁决建议（二选一）**：① 保留代码口径 → 更新 409/410 文档的 A 表并标注版本；② 回改 409 原义 → 需同步 `ATTACK_TYPES`+7 处 pytest+台账，工作量约 1 小时。

## 3. 收工门禁 fresh run（2026-09-14，终态）

| 项 | 命令 | 结果 |
|---|---|---|
| gate | `.venv\Scripts\python.exe tools/gate_engine.py --check` | **BLOCK=0 WARN=32 ADVICE=5** · 规则 50 · exit 0 |
| poison | `… tools/poison_drill.py --write-surface-map` | **61/61** · RULE-COVERAGE 24/50+豁免 27 · 攻击面 11/11 · exit 0 |
| pytest | `… -m pytest tests -q` | **272 点全绿**（后台跑，约 8 分钟；`-u` 直出可避免管道缓冲假超时） |
| replay | `… tools/atom_evidence_replay.py --check` | **confirm=56 refute=0 infra_error=0** |
| selfcheck | `… tools/writer_selfcheck.py --all` | **56 卡 fail=0** |

## 4. 未完成项（零上下文可继续）

### 4.1 P0-3 / E12 签收 git author 绑定（未做，需人裁决范围）
- **当前代码态**：`gate_engine.principal_ok()` 只校验「前缀 + 实名非空 + 在册名册 `HUMAN_PRINCIPALS=("liaoranran",)`」；`.github/CODEOWNERS` 不存在；无 git author 白名单。v5 实测 `human:liaoranran` 自签 ⇒ **0 block 0 warn**（链根未闭环）。
- **未完成原因**：改动面涉及 signoff 语义（历史 51 处 `human:liaoranran` 全部会命中）+ 需要人裁定「是否要求 author ∈ 历史作者集合 / 是否引入 CODEOWNERS」，非苦力可自决。
- **下一步（建议范围）**：① 新规则 `S1-GIT-AUTHOR-BINDING`（先 warn，从 `git log -1 --format=%an` 取 HEAD 作者，比对签收名）；② 判定单点仍在 `principal_ok`（勿三处各写）；③ CI 侧 CODEOWNERS + 分支保护。
- **精确命令**：`git log --format=%an | Sort-Object -Unique`（看作者集合）；`.venv\Scripts\python.exe tools/gate_engine.py --list | Select-String S1`（看签收规则现状）。

### 4.2 E05 是否再升 block（留人裁决）
- **现状**：`EV-FIXTURE-NO-ECHO-DATA` 已升 warn（P1-2），存量 0 命中。
- **未升 block 的原因**：该规则是**启发式正则**（读仓库内文件 + 8 行窗口原样打印 ⇒「疑似」），误伤面高于 E10（E10 是结构性判据：措辞 vs `-Werror` 的存在性）。升 block 需再跑一轮更大的阴性面（更多"合法读基线数据"夹具形态）。

### 4.3 其他（470 已明确留后续）
419（攻击用例回归库）、426（InvariantChecker 框架）、428（freshness 字段）、429（错误模式库）。

## 5. 临时文件（untracked，**不入库**；删除需用户批准，本环境未删）
```
Remove-Item _po.txt,_po3.txt,_po3e.txt,_po_err.txt,_rp.txt,_rp2.txt,_rp2e.txt,_rp3.log,_rp3.err,_pt.log,_pt.err,_ci_probe.py
```
`_adv_v80/`（v5 探针目录 + REPORT.md）与 `_worklog_403.md`/`_worklog_470.md` 同 403/470 惯例保留（untracked，作为证据留档）。

## 6. 提交清单（本轮，**均未 push**）

| commit | 主题 |
|---|---|
| `4a93745` | P0-1 / N1 僵尸锁 pid 存活检测 + stale 300s + atexit |
| `842c958` | P0-4 / N4 工件快照落盘 + 幂等还原 |
| `cebc1be` | P1-4 / N3 refutes·denies 归一 + 未知关系类型可见 |
| `87d3ce3` | P56 变量名修正（补 cebc1be 的 RULE-COVERAGE 识别） |
| `152413f` | P1-3 / E16 闪卡默认过滤 draft 原子 |
| `28e4632` | 测试同步：test_all_atoms_exported → draft 语义 |
| `d548b8d` | P1-2 / E05 cat 式证据 experimental → warn |
| `ae39d0b` | P0-2 / N2 恒真断言扩展到 contains/contains_any |
| `4428a2f` | 同步 P1-2 升格后的 p0b 锁（experimental→warn） |
| `dbdc85d` | 424 攻击面台账落盘 + `--by-type` 口径单点化（A1-A11） |
| `45926d6` | P1-1 零诊断规则升 block（472 P1-1/452 E10） |

**合计 11 提交，全部未 push**（本地 ahead 138；用户既定指令：本环境不重试 push，待可连通 SSH 网络手动推）。

