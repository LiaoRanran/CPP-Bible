# 区间与口径政策（CI policy）

> 669 P1（A02/A13）落地的**可执行**口径：所有检出率类断言必须带**区间**、带**分母**、并与**现算值**一致。
> 强制检查：`tools/ci_check.py`（区间存在性）+ `tools/caliber_check_669.py`（口径/现算一致性）。
> 区间实现单一来源：`tools/stat_bounds.py::cp_interval`（Clopper–Pearson 精确）与 `::wilson`（敏感性列）。

## 1. 三条硬规则

| 规则 id | 判据 | 谁在查 | 失败后果 |
|---|---|---|---|
| `G-CI-REQUIRED` | 每个 k/n 检出率断言必须带区间标记（`95% CI` / `CI [` / `Clopper` / `置信区间` / `[lo, hi]`） | `tools/ci_check.py research/` | exit 1 |
| `G-CALIBER-DECLARED` | 每个百分数必须**在该文档内**至少有一处写出 `k/n`（否则读者无法复算分母） | `tools/caliber_check_669.py --check` | exit 1 |
| `G-RATE-CONSISTENCY` | 文档里的百分数必须属于"从事实源现算出的值集合"；产物自称的率必须等于从原始计数现算的值 | `tools/caliber_check_669.py --check` | exit 1 |

补充（同一批）：`web_metrics_666 --check`（三个率 + 分母的漂移护栏，668 已建）在 `caliber_check_669 --check`
里作为**前置阶段**被调用 —— 射程不重复实现。

## 2. 报法（论文表）

- **主报 Clopper–Pearson 精确区间**（method = beta，双侧 95%）；
- **另列 Wilson** 作方法敏感性（结论跨方法不变时才写"稳健"）；
- 零计数（`0/n`）**不许**写成"零失效率"：一律写 `0/n（95% CI 0–上限）`——
  `0/4` 的上界是 **60.2%**，`0/8` 是 **36.9%**；
- 满计数（`n/n`）**必须带下界**：`6/6 = 100%`（95% CI 54.1–100）；
- 任何百分比都必须能在同一文档里找到 `k/n` 与事实源产物路径。

## 3. 冻结与豁免（可见台账，不静默）

* **冻结历史稿**：`research/paper_v0.1.md`–`v0.3.md` —— 各自时点的口径快照，追改等于改写历史记录。
  口径演进以 `research/paper_v0.4.md` 文首修订表为准。
* **并行草稿**：`research/paper_draft_v0.5.md` —— 由 669 P4 终稿 `research/paper_v0.5.md` 承接并统一补 CI。
* **不可复算值**：`33.3%`（662 轮产物只记率、未记分子/分母）—— 允许无 k/n，但文档必须**在同一处**标注
  「不可复算」（`caliber_check_669.py::UNCALIBRATED`）。
* **行级豁免**：`<!-- ci-check: ignore（理由） -->` —— 理由必须写在括号里（可审计）；用于"引用被否定的
  错误数字"这类场景，**不**用于放过自己的断言。
* 台账都在工具源码里（`ci_check.EXEMPT` / `caliber_check_669.HISTORICAL` / `UNCALIBRATED`），
  要收窄射程就删对应行 —— 迁移积压是**可见的**。

## 4. 复算入口

```powershell
.venv\Scripts\python.exe tools\ci_check.py research/                 # G-CI-REQUIRED
.venv\Scripts\python.exe tools\caliber_check_669.py --report          # 口径表（现算 + CP/Wilson）
.venv\Scripts\python.exe tools\caliber_check_669.py --check            # 三类判据 + ci_check + web_metrics
.venv\Scripts\python.exe tools\caliber_check_669.py --write            # 落盘 data/669_caliber_report.{json,md}
```

`data/669_caliber_report.md` 是**机器现算**的口径表（论文引用前先跑 `--write`，不许手抄）。
