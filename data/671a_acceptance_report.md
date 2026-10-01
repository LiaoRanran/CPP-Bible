# 671a 批次验收报告

- **批次**：671a（B3 防复发 AST 语义哈希 + B4 漂移检测增强 + 数据扩样 reveal + 门禁完善）
- **分支**：master　**日期**：2026-10-01　**执行者**：LiaoRanran（DCO）
- **红线**：不碰 `research/paper_v0.8.md`、`research/latex/`、`atoms/`、`evidence/`、`Examples/`、`Book/`、
  `data/authority/`、452 账本、`gate_engine.py`、`counts_659.py`；不代 push。
- **并发批次**：671b（论文 v0.9 / ablation / B3 设计）、671c（调研，只读）——本批与其交叉处已在 §6 登记。

---

## 0. 一句话

> 670g 留下的两个最大缺口都补上了：**B3 防复发**（`guard_rerun_671a`：10 个检测器 / 17 个产物的
> 「判据指纹 × 产物指纹 × mtime 新鲜度」三重对账 + **产物↔论文↔前端三方数字一致**）与
> **B4 漂移增强**（`drift_watch_671a`：论文 / 前端 / baseline 三臂 / 门禁规则四组新判据）；
> 两轮扩样 reveal **真跑完成**（WSL 可用，连跑 3 次逐样本可复现）：holdout 可测 **16 → 21**、
> corpus 可测 **32 → 48**，新率与 CP 区间可复算；两者挂进主门禁（L0 20/20）。
> 新增测试 **134 条**全绿；三套既有门禁测试（670c 15 / 670g 27 / 论文管线 39）不回归。

---

## 1. 任务 A · guard_rerun_671a（B3 防复发 + 新鲜度 + 三方一致）

**产物**：`tools/guard_rerun_671a.py`、`data/guard_detector_files_671a.json`、
`data/guard_artifacts_671a.json`、`data/guard_rerun_baseline_671a.json`、`tests/test_guard_rerun_671a.py`

| 判据 | 实现 | 本仓现状 |
|---|---|---|
| 检测器代码变更 → 必须重跑产物 | 判据指纹 = AST + **局部变量名归一**，逐检测器比对基线；`src + deps` 一起进指纹 | 10/10 `OK` |
| 产物新鲜度 | `产物 mtime ≥ max(src,deps) mtime − 1s`；**基线新鲜→现在不新鲜 = block**；基线即不新鲜 = 存量 WARN | 10 个存量缺口登记（见下） |
| 三方数字一致 | 产物现算 k/n ↔ 论文正文 `pct%（k/n` ↔ 前端 JSON 指针；率 ±0.5pp，计数完全相等 | 4 指标：2 一致 + 2 待 671b |
| 产物自身自洽 | 产物里 `stored` 率 vs 现算 k/n | 一致 |
| 配置防腐烂 | 配置声明的论文 k/n 必须等于产物现算 k/n | 一致 |

* **三重指纹**：`raw_sha256`（诊断）/ `ast_sha256`（剥文档字符串）/ `judgment_sha256`（+局部重命名归一）。
  注释或局部变量改名**不**判红（否则门禁变狼来了）；函数名、模块常量、字符串、属性名仍进指纹（改了必须重跑）。
* **deps 进射程**：`holdout_reveal_665` 的判据来自 `holdout_reveal_661.detect` ⇒ 661 改动一样触发 STALE
  （只盯驱动脚本会漏掉"换判据"这种改动）。
* **存量新鲜度缺口**（基线时即早于判据代码，登记为 WARN 不判红）：
  `baseline_arms_670a`（4 产物）、`corpus_reveal_665`、`holdout_reveal_665`（2）、`mutation_656`（2）、
  `web_verdicts_667` —— 重跑对应产物后本项自动收紧。
* **三方数字**：`mutation_core_pct`（97.3451% = 110/113）、`rules_total`（67）与论文/前端一致；
  `holdout_rate_pct` / `corpus_rate_pct` 因本批扩样已变新值 ⇒ `PENDING_NEWER`（WARN，owner=**671b**），
  **不假装一致**。
* 复用而非复制：670c 的 5 个核心工具由本工具 import 其 `evaluate()` 一并覆盖（本仓 PASS）。

## 2. 任务 B · drift_watch_671a（B4 漂移增强）

**产物**：`tools/drift_watch_671a.py`、`data/drift_report_671a.json`、`tests/test_drift_watch_671a.py`

| 组 | 判据 | 本仓现状 |
|---|---|---|
| 论文数字漂移 | 扫当前稿的 `pct%（k/n`，与**声明的产物**（三方配置 + 三臂 + corpus 分层）现算比对 | 匹配 25、未匹配 9（外部文献等，登记不判红）、**drift 0** |
| 前端数字漂移 | ① 声明指针 ↔ 产物；② 扫 `web/data/**.json` 的 `*rate_pct/*pct`（74 个）与上期报告比 | 声明 7 条全一致、扫描 74 个 **0 漂移** |
| baseline 三臂一致 | 三臂样本数必须相同 + 率必须能从 k/n 复算 + 分母 = catch+miss | holdout 17/17/17、corpus 40/40/40，**PASS** |
| 门禁规则漂移 | `gate_engine.RULES` ↔ `_gate_rules.json` ↔ 前端/文档声明（数量 + severity 分布） | 67 = 67 = 67；`{block: 44, warn: 16, advice: 7}` 与声明一致 |
| 跨时间（670c 协议） | ±10% 阈值 + `data/experiments/` 有新记录才 justified | 6 个核心数字 `ok=6` |

* **确定式不一致不接受实验记录豁免**：论文↔产物、前端↔产物、三臂样本数、规则数是"同一时刻两处矛盾"，
  有实验记录也不能变绿（与跨时间漂移分开处理）。
* 论文**只判当前稿**（v0.9）；v0.1–v0.8 是冻结留痕，只列出不判红（`--all-papers` 可全扫）。

## 3. 任务 C · 数据扩样 reveal（**真跑完成**，WSL 可用）

**产物**：`tools/holdout_reveal_4_671a.py`、`tools/external_corpus_reveal_671a.py`、
`tools/reveal_update_671a.py`、`data/holdout_reveal_4_671a.json`、`data/holdout/reveal_3_detail_671a.json`、
`data/external_corpus_reveal_671a.json`、`data/external_corpus/reveal_detail_671a.json`、
`data/experiments/reveal_update_671a.json`、`tests/test_reveal_671a.py`

环境：WSL Ubuntu 24.04 + g++ 13.3.0；`setarch -R` 可用（关 ASLR）；连跑 **3 次**逐样本一致
（`all_reproducible=true`，`unstable_samples=[]`）。

### C1 holdout h31–h40（第 4 轮 reveal，判据复用 `rv661.detect`）

| | 真错标签 | catch | miss | unknown | 可测分母 | 检出率 |
|---|---|---|---|---|---|---|
| 本轮（h31–h40） | 5 | 3（h31/h32/h40） | 2（h33 严格别名、h34 fence-mixed） | 0 | 5 | **60.0%** |
| 累计（h1–h40） | 22 | 17 | 4 | 1 | **21** | **81.0%**（CP95 [58.1, 94.5]） |

对照（planted=false）累计 `fp=2/11`（**h35** -Wunsequenced 命中、**h38** auto_ptr 命中 ⇒ 需 671b 裁定口径）。

### C2 corpus d3e-01..d3e-20（分层报告，禁止合并成一个数）

| 层 | 累计可测 | 检出率 |
|---|---|---|
| sanitizer | 19/24 | 79.2% |
| compiler-warn | 6/14 | 42.9% |
| cross-compile | 1/10 | 10.0% |
| perf / compile-time / other | 0/2 · 0/2 · 0/7 | **拒绝给率**（本机无检测器） |

本轮 12/16 = 75.0%；累计 **26/48 = 54.2%**。**口径变更已声明**：665 的 sanitizer 是单档 `-O1` 且未关 ASLR，
本轮新样本改为 `-O0`/`-O2` 双档 + `setarch -R` ⇒ 与 665 的数字**不可直接比大小**。

### C3 检出率更新（只算，不改论文）

| 指标 | 旧（论文/前端引用） | 新 | Δ | CP95 宽度 |
|---|---|---|---|---|
| holdout（可测） | 87.5%（14/16） | **81.0%（17/21）** | −6.5pp | 36.8 → 36.5pp |
| corpus（可测） | 43.8%（14/32） | **54.2%（26/48）** | +10.4pp | 36.0 → 29.5pp |
| 对照假阳性 | 11.1%（1/9） | **18.2%（2/11）** | — | — |

`pending_for_671b` 3 条（holdout / corpus / 假阳性），每条都写明"从哪变成哪、哪些文件/表格要跟着改"。
**未修改** `research/paper_v0.8.md`、`research/paper_v0.9.md`、`research/latex/`、`web/data/*.json`。

> **与受理单预期的差异（诚实登记）**：受理单写"holdout 16→26 可测、corpus 32→52"，
> 实际是 **16→21** 与 **32→48**。原因：新增样本里只有 `planted=true` 的进真错分母
> （h35/h36 是对照、h37–h39 标签 unknown），corpus 的 `perf`/`compile-time` 两层本机无检测器记 unknown。
> 数字按现算登记，未按预期凑。

## 4. 任务 D · 门禁完善

**产物**：`tools/run_master_gate_670c.py`（新增 3 个阶段组）、`tests/test_master_gate_671a.py`

* **D1 670g 纪律规则挂进主门禁**：新增 `gates_discipline_670g()`，**逐条**成阶段
  （条数从规则表现读，不写死"六条"）。分层：能吐 block 的 4 条 = L0，只吐 warn 的 2 条 = L1，
  **未分层的新规则默认 L0（fail-closed）**；且 670g 的 BLOCK 会并进 `unregistered_blocks` 分母 ⇒ overall FAIL。
* **D2 671a 两阶段**：`671a/guard`（L0）+ `671a/guard-armed`（L1）、`671a/drift`（L0）+ `671a/drift-armed`（L1）。
  未配置 / 未标定**只亮 L1**，不假装覆盖；真红进 L0 阻断。
* 主门禁实测：`overall=PASS  L0 20/20  L1 15/15  未登记BLOCK=0`（`--check`：受控目录 1910 文件快照、
  `write_detected=0`）。状态 JSON 新增 `guard_671a` / `drift_671a` / `discipline_670g` 三块。

## 5. 任务 E · 验收

| 检查 | 命令 | 结果 |
|---|---|---|
| 前端 888 断言 + 8 页冒烟 | `cd web && npm test` | ✅ 106+162+100+126+74+31+70+122+24+73 = **888**，SMOKE 8 页 ✅ |
| 论文管线 39 条 | `pytest tests/test_paper_sync_670c2.py tests/test_dist_perf_670c2.py` | ✅ 39 |
| 670g 门禁测试 | `pytest tests/test_gate_rules_670g.py` | ✅ **27**（22 + 671b 新增规则的 5 条） |
| 671a 新增测试 | 4 个文件 | ✅ **134**（guard 56 / drift 37 / master_gate 18 / reveal 23） |
| 门禁相关全量 | 11 个文件 | ✅ **264 passed**（连跑 2 轮稳定） |
| 658 门禁 | `python tools/run_658_gate.py` | ✅ PASS L0 5/5 |
| 主门禁 | `python tools/run_master_gate_670c.py --check` | ✅ PASS L0 20/20 L1 15/15 |
| guard_rerun_671a | `python tools/guard_rerun_671a.py` | ✅ PASS（exit 0，10 检测器 / 三方 4 指标） |
| drift_watch_671a | `python tools/drift_watch_671a.py` | ✅ PASS（0 漂移） |
| a11y / responsive / perf | 三个审计工具 | ✅ PASS（critical 0） |
| 测试总数 | 888 + 39 + 27 + 134 | **1088 ≥ 1014** ✅ |

## 6. 诚实登记

1. **并发批次交叉（3 处，均已处置或登记）**
   * **671b 新增第 7 条规则 `G-ABLATION-CONSISTENCY`**：本批的 670g 阶段是"逐条挂 + 未分层默认 L0"，
     所以新规则**自动**进了主门禁（无需改本批代码）。主门禁 selftest 也改成"已分层规则必须存在"
     而不是死等 6 条。
   * **两处测试夹具/断言随 671b 迁移修复**（不碰其语义）：
     `tests/test_gate_rules_670g.py` 的论文文件名改为**从被测模块读** `g.PAPER`
     （原写死 `paper_v0.8.md`，v0.9 迁移后 13 条用例集体变"论文不存在"）；
     `tests/test_paper_sync_670c2.py` 的 `FACTS` 解包宽度改为按第 0 位取。
     `test_real_repo_has_six_rules` → `test_real_repo_p0_rules_present`（断言六条 P0 都在 + 追加规则具名）。
   * **并发写入者（非本批）**：`atoms/conc/ATOM-CONC-FENCE-001.md`（8:49 丢 `id:` 行）、
     `ATOM-CONC-LOCK-001.md`（9:15）、`data/coverage_*_630/631`、`data/647_*`、`data/defense_chain_report.md`、
     `data/evidence_store/**` 在会话期间被非本批命令改写。**本批未执行任何写 `atoms/`/`evidence/` 的命令**，
     主门禁 `--check` 实测 `write_detected=0`。**未回滚他人文件**（避免踩并发批次的手）。
2. **修了一个真缺陷（跨测试 import 污染）**：`drift_watch_670c.metric_rules()` 按名字
   `import gate_engine`；测试里 tmp 仓库的假引擎（2 条规则）一旦被缓存，真实仓库的 `rules_total`
   会读成 **2**（67 → −97%）⇒ 假漂移、真实仓库用例随机红。已加 `unpoison_engine_cache()` 护栏
   （按 `__file__` 校验缓存来源，清掉后写进指标明细）+ 用例侧 autouse 清理 + 2 条回归用例。
   修复后该文件连跑 3 次全绿（此前约 50% 概率红）。
3. **口径 vs 受理单预期不一致**（见 §3 末尾）：holdout 16→**21**、corpus 32→**48**，
   原因写清、数字按现算，未凑预期值。
4. **本批未跑全量 `pytest tests/`**（670a 实测 ≈55 min）：改跑**门禁相关 264 条** +
   前端 888 + 审计三件套。全量命令与已知"并发瞬时污染"现象见 `REPLICATION.md`。
5. **`PENDING_NEWER` 的两项不判红**：holdout/corpus 的新率与论文/前端不一致（owner=671b）。
   这是**有意**的：本批不越界改论文，但也不许它静默落后 —— 门禁报告与
   `data/experiments/reveal_update_671a.json` 里都写了待办。
6. **`perf` / `compile-time` 两层"拒绝给率"**：本机无检测器 ⇒ `unknown`，不是 miss。
   要与"检测器报不出"区分开，这正是 662 那条猜测需要的对照。
7. **未做**：dist 未重建（本批未改 `web/`，`test_dist_perf_670c2.py` 通过）；未 push。

## 7. 新增 / 变更文件

**新增（本批）**
`tools/guard_rerun_671a.py`、`tools/drift_watch_671a.py`、`tools/holdout_reveal_4_671a.py`、
`tools/external_corpus_reveal_671a.py`、`tools/reveal_update_671a.py`、
`data/guard_detector_files_671a.json`、`data/guard_artifacts_671a.json`、`data/guard_rerun_baseline_671a.json`、
`data/drift_report_671a.json`、`data/holdout_reveal_4_671a.json`、`data/holdout/reveal_3_detail_671a.json`、
`data/external_corpus_reveal_671a.json`、`data/external_corpus/reveal_detail_671a.json`、
`data/experiments/reveal_update_671a.json`、
`tests/test_guard_rerun_671a.py`、`tests/test_drift_watch_671a.py`、`tests/test_master_gate_671a.py`、
`tests/test_reveal_671a.py`、`data/671a_acceptance_report.md`

**修改**
`tools/run_master_gate_670c.py`（670g 纪律阶段 + 671a 两阶段 + BLOCK 合并分母 + selftest）、
`tests/test_gate_rules_670g.py`（夹具随模块常量）、`tests/test_paper_sync_670c2.py`（解包宽度）

> 未碰：`research/paper_v0.8.md`、`research/paper_v0.9.md`、`research/latex/`、`atoms/`、`evidence/`、
> `Examples/`、`Book/`、`data/authority/`、452 账本、`gate_engine.py`、`counts_659.py`。

## 8. 复现命令

```bash
# A 防复发 + 三方一致（只读）
python tools/guard_rerun_671a.py --verify-config
python tools/guard_rerun_671a.py                # exit 0 = PASS
python tools/guard_rerun_671a.py --init         # 唯一写盘：刷新基线（确认产物已重跑后）

# B 漂移监控
python tools/drift_watch_671a.py                # exit 0 = 无漂移

# C 扩样 reveal（需 WSL；连跑 3 次逐样本对比）
python tools/holdout_reveal_4_671a.py --runs 3
python tools/external_corpus_reveal_671a.py --runs 3
python tools/reveal_update_671a.py

# D 主门禁（含 670g 纪律 + 671a 两阶段）
python tools/run_master_gate_670c.py --check --out build/master_gate_671a.json

# E 测试
python -m pytest tests/test_guard_rerun_671a.py tests/test_drift_watch_671a.py \
                tests/test_master_gate_671a.py tests/test_reveal_671a.py -q
python -m pytest tests/test_gate_rules_670g.py tests/test_master_gate_670c.py \
                tests/test_paper_sync_670c2.py tests/test_dist_perf_670c2.py -q
cd web && npm test                              # 888 断言 + 8 页冒烟
```
