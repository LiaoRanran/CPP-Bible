# _worklog_565 · 可计算质量内核第一批（统计原语 / 报告说真话 / 命题状态图 / 可观测性）

> 提示词：`References/architecture_架构演进/565_苦力建设批_可计算质量内核_统计原语_报告区间_命题状态图.md`
> 分支 master（本地，未 push）｜解释器只用 `.venv\Scripts\python.exe`｜本文件按惯例**不入库**。

## 0 · 停点（重要）

**Part 1 完成并单独 commit（`cad77da`）；Part 2 / 3 / 4 未开工——按提示词"做不完停在 Part 边界，
不留半成品"停在 Part 1 边界。** 本批总时长用在 T0 + Part 1 的四重锚点自证与口径核查上
（期间查出 563 探针一处**真实口径缺陷**，见 §2.3）。Part 2/3/4 的精确施工点见 §5 交人清单。

| commit | Part | 状态 |
|---|---|---|
| `cad77da` | 1 | ✅ 完成：`tools/stat_bounds.py` + `tests/test_stat_bounds.py`（23 例全绿） |
| — | 2 | ⬜ 未开工 |
| — | 3 | ⬜ 未开工 |
| — | 4a/4b | ⬜ 未开工 |
| — | 4c | ⬜ 未开工（但 559 遗留物的清单已在 §5 列明） |

复跑命令：

```
.venv\Scripts\python.exe -m pytest tests/test_stat_bounds.py -n0 -q
.venv\Scripts\python.exe tools/stat_bounds.py cp --k 0 --n 56
.venv\Scripts\python.exe tools/stat_bounds.py n-needed --eps 0.05
```

---

## 1 · T0 开工侦察（实测，逐条对账）

| 项 | 提示词假设 | 磁盘实测 | 判定 |
|---|---|---|---|
| 带 `claim_structured` 的卡 | 27 | **27** | ✅ |
| 命题总数 | 79（obs 50 / inf 29） | **79（observation 50 / inference 29）** | ✅ |
| `scipy` / `numpy` | 未安装 | **均未安装** | ✅ |
| metrics 断流 | 最新 2026-09-14 | `data/metrics.jsonl` 最后写入 **2026-09-14 21:30:35**（内容也停在当日口径：rule 55 / warn 31 / poison 72/72） | ✅（口径澄清见下） |
| `full_baseline_v1.json` | variants 1188 / blocked 729 / escaped 227 / n_a 232 / strict_blocked 615 / strict_rate 0.6433 / treated_rate 0.7626 | **逐值一致** | ✅ |

**口径澄清（非偏差，但会影响 Part 4a 施工）**：提示词写"`data/logs` 下 metrics 产物最新为
2026-09-14"，而 `data/logs/` 里其实有 09-15/09-16/09-17 的 `*.jsonl`（那是**观测日志**
CPPBIBLE_OBS 产物，今天还有写入）；**真正断流的是 `data/metrics.jsonl`**（metrics_collector 的
产物，停在 09-14 21:30）。Part 4a 要修的是后者。

Part 1 顺带记录的两个可用基线（供 Part 2 勾稽）：
- 可判分母 = 1188 − 232(n_a) − 0(malformed) = **956**；strict = 615/956 = **64.33%**；treated = 729/956 = **76.26%**；
- by_operator：M1 64/1/27 · M2 **0/207/14**（可判 207，逃逸 207 ⇒ 100%）· M3 2/11/75（**仅 13 可判**）·
  M4 200/0/33 · M5 0/0/**83**（可判 0）· M6 324/8/0 · M7 139/0/0。

---

## 2 · Part 1 · `tools/stat_bounds.py`（完成）

### 2.1 交付

正规化自 `_arch_v6/probe_bounds.py`（函数名/算法不变），新增：`cp_upper` / `cp_upper_one_sided` /
`cp_interval` / `wilson` / `normal_quantile` / `n_for_upper_bound_zero` / `n_for_proportion` /
`beta_quantile` / `proportion`（报告块）+ CLI（`cp` / `wilson` / `n-needed`，均可 `--json`）。
边界 fail-loud：n=0 / k>n / k<0 / conf∉(0,1) / eps∉(0,1) ⇒ `ValueError`（CLI rc=2 + stderr）。

### 2.2 四重锚点（`tests/test_stat_bounds.py`，23 例全绿）

① 解析解与对称性（k=0 闭式、双侧闭式、`lo(k)==1-hi(n-k)` 全 k 遍历）；
② **独立第二实现**：二项尾和直接求和 + 二分，与不完全 Beta 连分式在随机网格×40 上偏差 <1e-7
（**单侧对单侧、双侧对双侧**）；③ 公开锚点（0.05209 且紧于 3/56；n=100 ⇒ 0.0295）；
④ 样本量（59 / 149，并验 n=59 上界 ≤5%、n=58 >5% 的互逆）；另与 563 探针**逐值一致**（<1e-12）。

### 2.3 实测查出的口径缺陷（**须记档**）

563 探针的 `cp_upper` **两侧混用**：`k==0` 分支是**单侧**（`1-(1-conf)^(1/n)` = 0.05209），
`k>0` 分支走 `beta_quantile(1-alpha/2, …)` 是**双侧**。两者相差约 22%（0.05209 vs 0.06375 在
n=56,k=0 处），**口径切换发生在 k=0↔k>0 之间且无任何提示**——正是提示词说的"同名不同义的率"
会误导决策的形态。
处理（不破坏"与探针逐值一致"）：保留 `cp_upper` 原样 + docstring 写死警告，
**另立 `cp_upper_one_sided()`** 作口径统一版；CLI 的 `cp` 两条都打并显式标注：
`0/56 = 0.0000 · C-P 95% 区间 [0.0000, 0.0638]` / `单侧上界 95%：0.05209`。
**Part 2 施工时按此口径取数**：区间用 `cp_interval`，单侧上界用 `cp_upper_one_sided`。

### 2.4 其它修正（越界但必要）

`wilson()` 在探针里 z 只对 `conf==0.95` 有值（其它 conf 直接 TypeError）；`n_for_proportion`
硬编码 z=1.96。本版都按 conf 实算 z（`normal_quantile`，二分反解 erf ~1e-12）——语义不变、边界不再炸。

---

## 3 · Part 2 / 3 / 4 未开工的理由与施工点

- 未开工是**时间边界**，不是遇到阻碍：Part 1 的锚点自证 + 口径核查（含 §2.3 的缺陷定位）已用满
  本批预算。按提示词"做不完停在 Part 边界，不留半成品"，不擅自起 Part 2 的半截报告层。
- 每个 Part 的**精确施工点**见 §5（含已实测好的分母/分子与数据源），可直接接续。

---

## 4 · 收工红线自查（只对已完成部分）

- gate / poison / replay / pytest 两阶段：**本批未改任何判定核心**（新增的 `tools/stat_bounds.py`
  与 `tests/test_stat_bounds.py` 都是纯新增文件，不在 `.tool_checksums` 的 5 个 CORE_TOOLS 内
  ⇒ 无需重钉）。但按红线要求，收工仍应跑一遍全量两阶段（**留给接续批或人工**：见 §5 第 1 条）。
- 受控目录：仅新增 2 个文件；`evidence/` `atoms/` `tools(判定核心)` `tests` 语义零改动
  （`tests/test_stat_bounds.py` 是新增文件，未动既有测试）。
- 不 push / 不 --no-verify / 不 golden accept ✓。

---

## 5 · 交人清单（含接续批的施工点）

1. **收工总验收未跑**（本批停在 Part 1）：请接续批或人工补跑 `pytest -m "not slow" -n auto` 与
   `pytest -m slow -n0`，以及 gate 61/141 · poison 107/107 · replay confirm=56 的 fresh 复核。
2. **Part 2 施工点**（口径已备好）：
   - `data/mutation/README_v1.md` 写死四口径：可判分母 956；严格 615/956=64.33%（warn_only 114
     永不计入严格分子）；含 warn 729/956=76.26%；**全分母率正名为 treated_all=729/1188，不得叫 strict**；
   - `tools/mutation_fuzz.py` **只改报告呈现层**（不动判决/分类）：统一走 `stat_bounds.proportion()`
     出"分子/分母 + 点估计 + C-P95 区间"；分算子 M1–M7 各给率+区间+可判样本数；
     **M2 逃逸 207/207 标"活雷，区间 cp_interval(207,207) = [98.24%, 100%]"**；**M5 可判 n=0 标
     `insufficient evidence`（不算率、不填 0）**；**M3 仅 13 可判 ⇒ 标样本不足 + 给 n≥59 的补样目标**；
     n_a/malformed 单列、永不进分母；
   - 复跑 `tests/test_mutation_fuzz.py`（判决断言逐字不变）——注意 559 已给它挂了 `replay_serial`。
3. **Part 3 施工点**：`tools/prop_graph.py` + `data/propositions.db`（**与 knowledge_graph.db 的
   concepts 表分离**）；`build` 幂等；查询按 id/卡/claim_type/机验/签署；`tests/test_prop_graph.py`
   断言总数 79、obs 50/inf 29、重建不修改任何卡（前后 git status 零差异）。
   实测底座：命题级 `signed_by` 目前 **0 条**（全靠卡级人签兜底），79 条全部有 `evidence` 字段。
4. **Part 4a 施工点**：修 `data/metrics.jsonl` 断流（最后写入 2026-09-14 21:30:35）；注意
   `data/logs/*.jsonl` 是观测日志、**不是** metrics 产物（别修错对象）；加"采集确实落盘"回归锁。
5. **Part 4b**：三曲线字段（mutation 逃逸率带区间 / `overturned_by_stronger_verifier`（当前预期 0）/
   逃逸生存时间），**只有 1 个时点 ⇒ 文档必须注明"单调收敛尚不可声称"**。
6. **Part 4c 卫生清理清单**（模板：用 `.venv` python 的 `os.remove`/`shutil.rmtree` 通道，
   shell 删除会被本环境 safe-delete 拦）：
   - `.pytest_tmp/run-*`（559 起按运行次数堆积，实测已 34+ 个）；
   - 559 遗留：`_probe559.py` / `_probe559b.py`（**建议留档**：它是 Part B 的复现探针）/
     `_probe559c.py` / `_probe559d.py` / `_commit_msg_559*.txt` / `_t559*`（log/err/ps1/raw）；
   - 仓库根 `_probe_ch132_blk*.exe`（9/9 老残留）；
   - 本批新增：`_probe565t0.py` / `_commit_msg_565p1.txt`；
   - **只删上述明确 pattern，删前后 `git status` 核对，任何不确定的文件留清单交人**。

## 6 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **口径澄清（非偏差）**：提示词说 "`data/logs` 下 metrics 产物最新 2026-09-14"；实测 `data/logs/`
   有 09-17 的**观测日志**，真正停在 09-14 的是 `data/metrics.jsonl`。Part 4a 修后者。
2. **提示词锚点公式笔误**：① 写"k=0 解析解 == `1 - conf**(1/n)`"；实测该式在 conf=0.95,n=56 时
   为 0.000916，而锚点值 0.05209 对应的是 **`1 - (1-conf)**(1/n)`**（探针与锚点值自洽）。按**锚点值**
   实现，并在测试里锁死。
3. **563 探针真缺陷（本批新发现）**：`cp_upper` 的 k=0 分支是单侧、k>0 是双侧（差 ~22%）。
   本批保留原值 + 另立 `cp_upper_one_sided` + CLI 双标口径。**Part 2 取数务必按 §2.3 口径。**
4. **`wilson` 的 z 硬编码**：探针只在 conf==0.95 有值（其它 conf TypeError）；本版按 conf 实算 z。
5. **本批未做完 Part 2/3/4**：按边界停；施工点与已实测数据见 §5（不留半成品代码）。
