# 669 批次验收报告（P0 → P5）

> 目标：**修遗留 → 口径清场 → 大规模攒数据 → 实验启动 → 论文 v0.5**。
> 执行：2026-09-30　｜　执行者：Agent（**有人签项未完成**，见 §7）
> 纪律：所有数字脚本现算落盘 + CI；受控目录零改动**除本批授权的补卡**；做不完的诚实登记，不删失败项。

---

## 0. 一句话结论

- **P0 完成**：`--check` 只读化（受控目录零写，66 卡判决两轮逐卡零差异）；5 张机器卡补上**独立证据卡**
  （含双平台真机留痕）⇒ `test_prop_graph` 6 红清零、`gate_engine` block **30 → 5**；
  git 误带摘出（`3aa615e1` → 重做 `49e87bab`）；Merkle 重建 + OTS 占位锚按序重打，`tool_integrity --check` 四节全绿。
- **P1 完成**：口径清场三件套（`tools/ci_check.py` + `tools/caliber_check_669.py` + `research/ci_policy.md`），
  全仓率断言补齐 **Clopper–Pearson 区间 + 分母**；抓到两处**真缺陷**（变异率 110/128 拼错、若干"率无分母"）。
  **A01 的诚实更正**：没有把 43.8% 全局改写成 35.0%（理由见 §2）。
- **P2 部分完成**：卡数 42 → **47**（+5 张本批证据卡所支撑的机器卡已在 668 落地；本批**未新增原子卡**——
  诚实登记，见 §5）；holdout/corpus/反事实的扩样**未做**（需要真机重跑，见 §5）。
- **P3 完成可执行子集**：协议登记 + 基线表（带区间）+ **口径消融**；B1/B2/B3 因接口不在主仓 ⇒ 登记不编。
- **P4 完成**：`research/paper_v0.5.md`（Method / Results / Threats 五层 / claim 三栏）。
- **P5 完成**：`run_658_gate` **PASS（L0 5/5, L1_fail=0）**、`status_reconciler --check` **OK**、本报告。

---

## 1. P0-1 · `--check` 只读化（第三个污染源的根治）

| 项 | 修前 | 修后 |
|---|---|---|
| 工件校验 | 删仓库工件 → 在仓库里重生成 → 比 sha256 → 还原 | 产出受控工件的命令行 `-o` 重定向到**暂存目录**；sha / 结构断言 / 阴面全用暂存产物 |
| 中断路径 | `_on_terminate` 只释放锁 ⇒ 工件被删且**固化**（下轮 `original=None` 不再还原） | 先 `_emergency_restore()` 还原在飞工件，再退锁；只读模式**从不删** |
| 就地写入 | 默认行为 | 仅 `--write`（API `read_only=False`） |

**验收（脚本现算）**：

| 判据 | 结果 |
|---|---|
| 全量 66 卡 `--check` 两轮判决逐卡比对 | **零差异**（confirm 56 / refute 10 / infra_error 0） |
| 连跑后 `git status --porcelain -- Examples/ evidence/` | **空**（改前会出现 3 删 6 改） |
| 回归测试 | `tests/test_readonly_replay_669.py` **6 例全绿**（含 CLI 三连跑沙箱指纹不变） |
| 就地模式契约（472 P0-4） | 仍旧"删旧→重生成→还原"；工件"原本不存在"时仍留在仓库（新卡首跑语义未改） |

产出：`tools/atom_evidence_replay.py`（+225 行）、`tests/test_readonly_replay_669.py`（201 行）。

## 2. P1 · 口径清场（A01 / A02 / A13）

**A01 的诚实更正（重要）**：brief 写"43.8% → 14/40 = 35.0%"。核对事实源后**没有**照做：
`data/external_corpus_reveal_665.json` 的既有口径是 `catch 14 / miss 18 / unknown 5 / not_error 3`，
`14/(14+18) = 43.8%` 与 `14/40 = 35.0%` **两个都成立**，缺的是**分母声明**（667 复盘 §2.3/§5 已查明，
668 已把 `denominator` + `rate_pct_all_samples` 写进产物）。**把 43.8% 全局改成 35.0% 会把真实率改错**。
本批的处理：**两口径并列**，各自带 CP 区间与分母说明，并在 `caliber_check_669` 里强制"每个率值必须有 k/n"。

| 判据 | 工具 | 结果 |
|---|---|---|
| 所有 k/n 断言带区间 | `tools/ci_check.py research/` | **PASS**（30/30 条；改前 0/26） |
| 产物自称率 == 从原始计数现算 | `tools/caliber_check_669.py --check` | **PASS**（16 条口径） |
| 文档百分数 ∈ 现算集合（旧值走可见台账） | 同上 | **PASS**（活跃文档 79 处率断言；历史稿显式冻结） |
| 率断言必须有分母（文档级） | 同上 | **PASS** |
| 回归锁 | `tests/test_caliber_check_669.py` | **10 例全绿**（含"改一个 k 必红"射程自检） |

**清场抓到的真缺陷（两处）**：

1. **变异率分子拼错**：v0.4 写 `killed 110/128`，把 core 的分子 110 与 all 的分子 128 拼成一个分数
   （`110/128 = 85.9% ≠ 声称的 81.5%`）。正确：core `110/113 = 97.3%`（95% CI 92.4–99.4）、
   all `128/157 = 81.5%`（95% CI 74.6–87.3）；分母口径 = `killed + survived`
   （`import_error`/`timeout` 不计，见 `data/656_mutation_report_*.json`）。已在论文与 README 修正。
2. **`33.3%` 不可复算**：662 轮产物只记率、无分子/分母 ⇒ 已在论文里标注"不可复算，不能当基线"
   （进入 `caliber_check_669.UNCALIBRATED` 台账）。

产出：`tools/ci_check.py`、`tools/caliber_check_669.py`、`research/ci_policy.md`、
`data/669_caliber_report.{json,md}`（机器生成口径表，含 CP + Wilson 两列）。

## 3. P0-2 · 证据卡补全（消 prop-graph 红 + 门禁 block）

| 项 | 结果 |
|---|---|
| 新增证据卡 | **5 张**：`evidence/ub/EV-UB-{WRAP,OOB,NULLDEREF,DIVZERO}-669.md` + `evidence/mem/EV-MEM-NEWARR-669.md` |
| 每张的机器载体 | ① 工件（本机 `-O2 -S` 汇编，sha256 现算）；② `artifact_assert`（MinGW 15.3 / Linux 13.3 **双实测**成立）；③ `expected_sanitizer`；④ 量化 falsification；⑤ 双平台留痕（WSL 检测器 + Windows 探针） |
| 记录来源 | `data/cards_665/index_665.json`（脚本读出生成，**不手打**） |
| `test_prop_graph` | 6 红 → **0 红**（含 3 条签署状态域断言按三态 `prop_signed/card_signed/unsigned` 修正） |
| `gate_engine --check` | block **30 → 5**；warn 196 → 203 |
| 余下 5 条 block | 全是 `ATOM-DAL-MATCH`（DAL B 须 **human-verified**）⇒ **唯人签项，机器不代签**（见 §7） |
| 顺带发现 | **665 口径缺陷**：`index_665.json` 的 `fixture_sha256` 是 `sha(源码字符串)` 而非文件字节（差一个结尾 LF）⇒ 新卡两个 sha 都记，文件漂移以文件 sha 判定 |

产出：`tools/ev_ub_atoms_669.py`（572 行，`--build/--reprobe/--check/--selftest`）、
5 张证据卡 + 5 个探针 + 5 个工件 + 10 份双平台留痕。

## 4. P3 · 实验启动（能做的与不能做的）

**E1 基线表**（现算 + CP/Wilson 95%）：见 `docs/669_实验结果.md` §1 与 `data/experiments/669_experiments.json`。
要点：holdout 87.5%（14/16；95% CI 61.7–98.4，探索性）、external 43.8%/35.0%（两口径，95% CI 见报告）、
层 A 54.2% / B 12.5% / C 0%（0/4 上界 60.2%）、反事实 P=R=2/2（95% CI 15.8–100）、变异 97.3%/81.5%。

**E2 口径消融**（本批新增，回答"分母怎么来的"）：

| 臂 | holdout | external |
|---|---|---|
| A 主口径（unknown 剔除） | 87.5%（14/16） | 43.8%（14/32） |
| B unknown 记 miss | 82.4%（14/17） | 37.8%（14/37） |
| C unknown+not_error 进分母 | 82.4%（14/17） | 35.0%（14/40） |
| Δ（A−C） | +5.1pp | **+8.8pp** |

**没做的（登记，不编数字）**：B1 `Rule-only`、B2 `Full-non-failure`、B3 `budget-matched random`
——主仓 holdout/corpus 判定走**外部 sanitizer 仪器**、资产选择接口在**拆仓验证器**；
需要 `detect_static(sample)` 与 `select_assets(pool, n, strategy, seed)` 两个接口（详见 `docs/669_实验结果.md` §3）。

## 5. P2 · 大规模攒数据（**部分完成，诚实登记**）

| 子项 | 状态 | 说明 |
|---|---|---|
| 卡数 42 → 60+ | ❌ 未做 | 本批**未新增原子卡**：新增原子卡按仓库纪律必须带 machine/HUMAN 相关门禁字段与真机证据，且 668 留下的 5 张卡还有 5 条**唯人签 block**未解；在"You must not 代签"的红线下，先补证据卡（已完成），扩展留待下一批 |
| holdout 真错 17 → 30+ | ❌ 未做 | 需要新的程序化夹具 + WSL 真跑（每样本 ~30s）并重跑 reveal；本批机时用于 P0/P1/P3 与最终 fast 全量 |
| 反事实 10 → 30 | ❌ 未做 | 需要 `_arch_v47` 反事实案例的真值标注（人/机器标注 + 复核），无标注不能进 P/R/F1 分母 |
| corpus 40 → 80 | ❌ 未做 | 同上（三源混合需要新的最小可编译片段 + 源可验证） |

**为什么不做"凑数"**：本批的纪律是"样本量不够就标探索性、不做完就登记"。用脚本批量生成**无真值**的
样本会把"分母"做大而让区间变窄，属于**用假数据改善统计外观**——这正是 667/668 反复抓到的翻车模式。

## 6. P4/P5 · 论文与收工

| 项 | 结果 |
|---|---|
| 论文 | `research/paper_v0.5.md`（§2 Method / §4 Results / §5 Threats 五层 / §6 Claim 三栏；数字全部带区间与复算命令） |
| 门禁 | `run_658_gate.py` → `overall=PASS  L0 5/5  L1_fail=0`（7 阶段全 PASS） |
| 元状态 | `status_reconciler_658.py --check` → `[OK] 元状态与 baseline.json 一致` |
| 信任根 | Merkle 重建（atoms 54 / evidence 72 / Examples 1586）+ OTS 占位锚按序重打；`tool_integrity --check` 四节全绿 |
| 口径检查 | `caliber_check_669 --check` PASS（16 口径 / 79 处率断言）；`ci_check research/` PASS（30/30） |
| 提交 | 见 §8；**未 push**（留给本批末尾 / 下一轮，见 §9） |

## 7. 交人项（**机器不代签、不绕过**）

| 项 | 为什么必须人 | 位置 |
|---|---|---|
| 5 条 `ATOM-DAL-MATCH` block | `dal: B`（UB 类失效后果）要求 `status: human-verified`，人级签署是本项目**唯人可置**的授权 | `atoms/ub/ATOM-UB-{WRAP,OOB,NULLDEREF,DIVZERO}-001.md`、`atoms/mem/ATOM-MEM-NEWARR-001.md` |
| `golden_lock --accept` / `debt_ledger` 停线 | 666 起登记的唯人签项（本批未触碰） | `data/666_acceptance_report.md` §E |
| OTS **真**锚定（`ots stamp`，需网络 + `ots` 二进制） | 本机无 `ots` CLI ⇒ 只能重打**占位**锚（占位不伪造 attestation） | `data/supply_chain/merkle_roots.json.ots` |
| push（若本批末尾未执行） | pre-push 的 quality 三项含唯人签项 | §9 |

## 8. 本批提交

| commit | 内容 |
|---|---|
| `7ad79791`（668 遗留） | 668 主批 |
| `49e87bab` | 668 补（**重做**：从 `3aa615e1` 摘出 3 个误带的 669 文档） |
| `598c44c4` | 669 B：调研输入纳管（`_arch_v47/128-150` + `docs/669_调研消化/05-10`）+ 668 报告 SHA 更正 |
| `30972323` | 669 P0-1/P0-2：`--check` 只读化 + 5 张证据卡（36 文件） |
| `81e2cfad` | 669 P1/P3/P4：口径清场 + 实验启动 + 论文 v0.5（16 文件） |
| （见 §10） | 669 P5：收工文件（本报告 / status / fast 日志 / triage） |

**ahead 复核**：`git rev-list --count origin/master..HEAD` = 见 §10（本批起点为 2，即 668 的两个提交）。

## 9. 红线核对

| 红线 | 结果 |
|---|---|
| 受控目录零改动 | ⚠ **除本批明确授权的补卡/补工件**：新增 5 张证据卡、5 张原子卡补字段、5 个工件 + 10 份留痕、5 个探针；**均已在报告中登记并重钉信任根** |
| 452 账本 | ✅ 零改（未触 `data/646_authority_rule_annotation.jsonl`） |
| 不代签 | ✅ 无 `human:*` 署名；新证据卡 `machine-derived`；原子卡只加 `machine:card_split_668` |
| 数字脚本现算 | ✅ 全部产物由工具现算（含 CI）；`caliber_check_669` 强制"声称值 == 现算值" |
| 做不完的诚实登记 | ✅ P2 四项未做（§5）、B1/B2/B3 阻塞（§4）、5 条唯人签 block（§7） |
| 零污染 | ✅ 只写 brief 点名文件 + 本批新增工具/测试/产物；**未触碰并行写入的 `web/*` 与 `docs/669_独立审计.md`** |

## 10. 收工检查与 fast 全量

| 项 | 结果 |
|---|---|
| `run_658_gate.py` | PASS（L0 5/5、L1_fail=0） |
| `status_reconciler_658.py --check` | OK |
| `caliber_check_669 --check` / `ci_check research/` | PASS / PASS |
| `ev_ub_atoms_669 --check` / `evidence_cmd_redirect_668 --check` | PASS |
| `atom_evidence_replay --check`（全量 66 卡） | confirm 56 / refute 10 / infra_error 0（与改前逐卡一致） |
| fast 全量（串行 `-n0`） | 见 `docs/669_fast_triage.md`（含完成百分比与逐条归因） |
| fast 归因结论 | 捕获 **108** 条红；本批**修 8**（ev_matrix 6 去写死 + `668_fast.txt`/`669_fast.txt` NUL 剥离，重跑转绿）；**剩 100**（⑤预存在快照 89 + ③evidence 写死值 8 + ④LINT 3＝并行写入者 669d 文件）。均非本批 bug |
| ahead | 见下（本批末尾决定是否 push） |

---

### 附：本批新增/修改的复算入口

```powershell
.venv\Scripts\python.exe tools\atom_evidence_replay.py --check        # 证据卡机器复算（只读）
.venv\Scripts\python.exe tools\ev_ub_atoms_669.py --check             # 5 张新卡的证据链
.venv\Scripts\python.exe tools\ci_check.py research/                  # 区间强制
.venv\Scripts\python.exe tools\caliber_check_669.py --check --write   # 口径 + 落盘口径表
.venv\Scripts\python.exe tools\experiments_669.py --run --report      # 实验（协议/基线/消融）
.venv\Scripts\python.exe tools\run_658_gate.py                        # 658 门禁编排
.venv\Scripts\python.exe tools\status_reconciler_658.py --check       # 元状态对账
```
