# REPLICATION.md · 复现指南（661 D2 · 670c B 段补齐）

> 目标：任何人（或未来的我）能按此把 queyi 验证器的关键结论**跑出来**。
> 配套：```run_reproduction.sh```（POSIX）、`data/dataset_hashes_661.json`（661 数据集哈希）、
> `data/dataset_hashes_670c.json`（670c 数据集哈希）、`tools/reproduce_all_670c.py`（一键编排器）、
> `data/croissant_670c.json`（数据集元数据 / Croissant 1.0）。
>
> **文档分区（重要）**
> * **§0–§5** = 661 D2 的**原文**，保留不改（历史留痕）。
> * **§6–§14** = 670c B 段补齐（2026-09-30），**权威口径**。两处冲突以 §6–§14 为准；
>   冲突本身逐条登记在 §14，不静默择一。
> * 本文每个**数字**都标了事实源（哪个文件的哪个字段）。核不到的写「**未核对**」，不编。

## 0. 前置（661 原文）

| 依赖 | 版本 | 用途 |
|---|---|---|
| Python | ≥3.11（本仓用 `uv` 管理） | 全部工具/测试 |
| [uv](https://docs.astral.sh/uv/) | ≥0.11 | `uv run` 一键环境 |
| Node.js | ≥20 | `web_logic_check_655.mjs`（前端台账哈希） |
| g++ / clang++ | g++≥13、clang≥15 | 缺陷注入的编译检测 |
| WSL（可选） | Ubuntu 22.04+ | TSan/ASan/UBSan 真机检测（holdout reveal） |

> ⚠ 上表是 661 当时的写法。**WSL 不是"可选"**，Node 也不是必须 ≥20 —— 见 §6。

## 1. 一键复现（推荐）

```bash
bash run_reproduction.sh
```

脚本依次跑：元状态对账 → 658 门禁 → 前端台账 → 缺陷注入 → holdout reveal（预期 REFUSED）→ 数据集哈希。

Windows（PowerShell 等价）：

```powershell
uv run python tools/status_reconciler_658.py --check
uv run python tools/run_658_gate.py
node tools/web_logic_check_655.mjs
uv run python tools/defect_injection_661.py
uv run python tools/holdout_reveal_661.py   # 已 reveal → REFUSED（铁律）
```

## 2. 期望输出（expected outputs）

| 步骤 | 期望 | 不通过的含义 |
|---|---|---|
| `status_reconciler_658.py --check` | `[OK] 元状态与 baseline.json 一致` | 文档/git 状态漂移 → 先修再跑实验 |
| `run_658_gate.py` | `overall=PASS  L0 5/5` | L0 红线被破，实验作废 |
| `web_logic_check_655.mjs` | `4/4 全绿` / `全部通过` | 前端台账哈希漂移（重跑 `tools/web_data_653.py --build`） |
| `defect_injection_661.py` | `重注入检出率 = 6/6 = 100%` | 门禁漏抓真实缺陷 |
| `holdout_reveal_661.py` | `[REFUSED] 已 reveal` | 若它跑起来 → **违反铁律**（已 reveal 不得回盲） |

## 3. 数据集哈希（frozen）

`data/dataset_hashes_661.json` 记录关键数据集的 sha256：

- `data/holdout/holdout.json`（D2 盲化，20 样本）
- `data/defect_fixtures/defects.json`（D1 历史，15 条真实缺陷）
- `data/_gate_rules.json`（规则清单，67 条，= 引擎）
- `web/data/graph.json`（星图，178 节点 / 1093 边）
- `data/holdout_reveal_1_661.json`（B1 reveal 报告）
- `data/defect_injection_661.json`（B2 注入报告）

> 注意：Windows 检出若发生 CRLF 转换，哈希会漂移；以 `.gitattributes` 为准，建议 `git config core.autocrlf false` 后重算。
> **670c 已把这件事做成工具**：见 §12。

## 4. 铁律（不可违反）

1. **holdout 不可回盲**：`data/holdout/.revealed` 一旦存在，任何"把盲态设回 true"的操作都被 `tools/holdout_658.py` 拒绝。
2. **受控目录零改**：`atoms/`（除 frontmatter 加字段）、`evidence/`、`Examples/`、`Book/` 不得改正文；`452` 账本零改。
3. **D2/D4 在 Phase 3/6 前不参与训练/调参**（违反即实验作废，见 `research/05`）。
4. **重注入只在临时副本**：`tools/defect_injection_661.py` 的 re-inject 绝不写仓库。

## 5. 跑单点实验

```bash
# 单条缺陷重注入
uv run python tools/defect_fixture_658.py --inject 657-manifest-drift

# holdout 状态（reveal 后）
uv run python tools/holdout_658.py --status

# 规则口径对账（engine vs 清单）
uv run python -c "import sys,json;sys.path.insert(0,'tools');import gate_engine;print(len(gate_engine.RULES), len(json.load(open('data/_gate_rules.json',encoding='utf-8'))))"
```

---

# 670c B 段补齐（2026-09-30）

## 6. 精确环境要求

版本值是 **2026-09-30 在本机（Windows 11 + PowerShell）实测**的，逐条给自检命令。

| 组件 | 要求 | 本机实测 | 自检命令 | 缺了会怎样 |
|---|---|---|---|---|
| Python | **3.13**（`.python-version` = `3.13`；`pyproject.toml` `requires-python = ">=3.11"`；CI 矩阵钉 3.11） | `Python 3.13.13` | `.\.venv\Scripts\python.exe --version` | <3.11 直接装不上；**3.11/3.12 在本批未复算 ⇒ 未核对** |
| pip 依赖 | `pip install -r requirements.lock.txt`（uv 导出、带 sha256 哈希校验） | 已装于 `.venv` | `.\.venv\Scripts\python.exe -m pytest --version` | 缺 `pyyaml` ⇒ `gate_engine` 起不来；缺 `pytest/pytest-xdist/hypothesis` ⇒ §9 第 8 条跑不了 |
| Node.js | CI `deploy.yml` 钉 **Node 20**；本机 **18.20.8** 也够用（根 `package.json` 的 note 说明把 jsdom 钉到 24 就是为了 Node 18 兼容） | `v18.20.8` | `node --version` | 缺 Node ⇒ `tools/web_logic_check_655.mjs` / `web_smoke_655.mjs` 无法真跑（前端台账哈希只能 SKIP） |
| g++（本机） | 能编 C++17 | `g++.exe (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0` | `g++ --version` | 缺 ⇒ `compiler-warn` / `wunsequenced` 类样本记 unknown |
| clang++ | ≥15 | `clang version 22.1.8` | `clang++ --version` | 缺 ⇒ `cross-compile` 差分检测退化为 unknown |
| **WSL + Ubuntu g++** | **必须有（硬依赖，不是可选）** | `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` | `wsl -e bash -lc "g++ --version \| head -1"` | 见 §6.1：**命令仍全绿，数字腰斩** |

其余运行时事实源：`data/holdout_reveal_3_665.json::env` 与 `data/experiments/669_experiments.json::registry.env`
（两者是同一份环境记录，互相印证）。

### 6.1 为什么 WSL 是硬依赖，以及不装会怎样

**为什么**：holdout 与 external corpus 里"sanitizer 类"样本的判定**不是静态规则**，
而是 `wsl -e bash -lc "g++ -std=c++17 -O0/-O2 -fsanitize=... 源码 -o /tmp/x && /tmp/x"`
——**在 WSL 里真编译、真运行**（实现见 `tools/holdout_reveal_661.py::detect`、
`tools/external_corpus_662.py::detect`，被 `holdout_reveal_3_665.py` /
`external_corpus_reveal_665.py` 复用）。Windows 原生 MinGW 上没有可用的 TSan 运行时，
ASan/UBSan 的行为也与 Linux 不同 ⇒ 这三族检测器**只能在 WSL 里跑**。

**不装会怎样（有实测数字，不是推测）**：`data/external_corpus/external_corpus_669d.json::env_dependency.note`
写明 —— WSL 缺位时这些样本降级为 `unknown`，外部语料检出率从 **35.0%（14/40）掉到 10.0%（4/40）**，
**而护栏仍然全绿**。这就是"静默掉分"：命令全部 exit 0，数字却腰斩。

因此 670c 的做法是：
1. 把 WSL 写进**硬依赖**（本节）；
2. `tools/reproduce_all_670c.py` 在 `env.wsl_gpp` 字段里记录它，报告与数字绑定；
3. `data/dataset_hashes_670c.json` 把 `data/cards_665/fixtures/*.cpp` 也钉住（夹具变了同样复算不出）。

## 7. 完整安装步骤

```powershell
git clone https://github.com/LiaoRanran/CPP-Bible.git
cd CPP-Bible

# 1) Python 环境
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe -m pytest --version        # 自检

# 2) Node 依赖（两份清单，作用域不同）
npm install                                           # 仓库根：jsdom@24.1.3（tools/*.mjs 用）
cd web; npm install; cd ..                            # web/：jsdom（前端纯逻辑测试用）

# 3) WSL（只需一次；重启后进 WSL 装 g++）
wsl --install -d Ubuntu
wsl -e bash -lc "sudo apt-get update && sudo apt-get install -y g++"
wsl -e bash -lc "g++ --version | head -1"             # 自检：应打印 Ubuntu 的 g++ 行
```

POSIX 等价：把 `.\.venv\Scripts\python.exe` 换成 `.venv/bin/python`，其余相同。

> `requirements.lock.txt` 是 `uv export --no-emit-project --extra dev --extra ci --extra pdf`
> 的产物（CI 的 MkDocs job 用的就是它），带哈希校验 ⇒ 装出来的版本与 CI 一致。
> 只想跑复现 kit 的最小集合是：`pyyaml pytest pytest-xdist hypothesis`
> （CI 的 pytest job 就是装这四个，见 `.github/workflows/ci.yml:429`）。

## 8. 数据集：真实路径与条数（**每个数字都写明"我是从哪个文件数出来的"**）

| 数据 | 条数 | 真实路径 | 我从哪数出来的 |
|---|---:|---|---|
| AtomCard（现算实卡） | **42** | 索引 `web/data/cards_index.json`；全文 `web/data/cards.json` | `web/data/verdicts_667.json::dashboard.cards_real = 42`（由 `tools/web_metrics_666.py` 现算）；`docs/669_独立审计.md` 第 36/221 行同写"实为 42" |
| AtomCard 草稿 / 合计 | 10 / **52** | 同上 | `web/data/verdicts_667.json::dashboard.cards_draft = 10`、`cards_total = 52` |
| 665 机器卡 | **16** | `data/cards_665/index_665.json` + `data/cards_665/fixtures/*.cpp` | `index_665.json::total = 16`（IG01–IG16；verdict 分布 catch 6 / miss 5 / unknown 1 / measure 4） |
| holdout 种子 | **30** | `data/holdout/holdout.json`（= `data/holdout/holdout_665.json`，同一 canonical 视图） | `holdout.json::count = 30`；逐条数 `planted` ⇒ true **17** / false **9** / unknown **4** |
| 669d 补充 holdout | 10 | `data/holdout/holdout_extension_669d.json` | `count = 10`（true 5 / false 2 / unknown 3；**未并入** holdout.json） |
| 外部 corpus | **40** | `data/external_corpus/external_corpus_662.json`（= `external_corpus_665.json`） | `count = 40`；按 `expected_detector` 数：ubsan 6 / asan 8 / tsan 1 / compiler-warn 6 / wunsequenced 4 / cross-compile 8 / measure 3 / unknown 4 |
| 669d 补充 corpus | 20 | `data/external_corpus/external_corpus_669d.json` | `count = 20` |
| 真实缺陷夹具 | **15** | `data/defect_fixtures/defects.json` | `stats.total = 15`（by_batch 656:6 / 657:3 / 652:1 / 历史章节:5；gate_caught yes 12 / partial 1 / unknown 2） |
| 缺陷重注入结果 | 6/6 = 100% | `data/defect_injection_661.json` | `reinjectable = 6`、`reinject_caught = 6`、`coverage_all_pct = 80.0` |
| 反事实案例（无真值） | 10 | `data/counterfactual_cases_660.json` | `cases` 长度 10；**没有 ground_truth 标签** ⇒ 不进 P/R/F1 分母 |
| 反事实案例（打分） | 10 | `data/counterfactual_cases_665.json` | `cases_total = 10`、`denominator.value = 10` |
| 669d 补充反事实 | 20 | `data/counterfactual_cases_669d.json` | `cases_total = 20` |
| 规则清单 | 67 | `data/_gate_rules.json` | `web/data/status.json::rules.rules_total = 67`（block 44） |

> 复核示例（每个数字都能这样现算，不靠文档转述）：
> ```powershell
> .\.venv\Scripts\python.exe -c "import json;d=json.load(open('web/data/verdicts_667.json',encoding='utf-8'));print(d['dashboard']['cards_real'])"
> .\.venv\Scripts\python.exe -c "import json,collections;d=json.load(open('data/holdout/holdout.json',encoding='utf-8'));print(len(d['seeds']), collections.Counter(str(s['planted']) for s in d['seeds']))"
> ```

## 9. 复现命令清单（命令 / 预期数字 + CI / 耗时 / 依赖）

**CI 一律 Clopper–Pearson 95%**，实现 `tools/stat_bounds.py`，数值取自 `docs/669_实验结果.md`
（该文件由 `tools/experiments_669.py --run` 现算落盘 `data/experiments/669_experiments.json`）。
n < 30 的行标 **[探索性]**，不得写进论文结论。

| # | 命令 | 预期结果（含 95% CI） | 耗时 | 依赖 |
|---|---|---|---|---|
| 1 | `python tools/run_658_gate.py` | `[658 gate] overall=PASS  L0 5/5  L1_fail=0`（exit 0） | 见 §9.1 | pyyaml、pytest（S6 阶段） |
| 2 | `python tools/run_669d_gate.py --no-write` | `[669d gate] overall=PASS  未登记BLOCK=0  已登记=4  WARN=13`（exit 0） | 见 §9.1 | pyyaml |
| 3 | `python tools/holdout_reveal_3_665.py` | 真错 **14/16 = 87.5%**（CP **[61.7, 98.4]**）；对照误报 1/9 = 11.1%（CP [0.3, 48.2]）；unknown 标签 4 | 见 §9.1 | **WSL + g++ + ASan/UBSan/TSan**、本机 g++/clang++ |
| 4 | `python tools/external_corpus_reveal_665.py` | 可测口径 **14/32 = 43.8%**（CP **[26.4, 62.3]**）；全样本 **14/40 = 35.0%**（CP [20.6, 51.7]）；A 层 13/24 = 54.2%（CP [32.8, 74.4]）、B 层 1/8 = 12.5%（CP [0.3, 52.7]）、C 层 0/4 = 0%（CP [0, 60.2]） | 见 §9.1 | 同 3 |
| 5 | `python tools/mutation_test_656.py --scope core --limit 450 --json` | **110/147 = 97.3%**（CP [92.4, 99.4]）；stdout JSON `mutants=147 killed=110` | 见 §9.1 | pytest、hypothesis |
| 6 | `python tools/mutation_test_656.py --scope all --limit 300 --json` | **128/223 = 81.5%**（CP [74.6, 87.3]） | 见 §9.1 | 同 5 |
| 7 | `python tools/counterfactual_extend_665.py` | P = R = F1 = **1.0**（tp 2 / fp 0 / tn 8 / fn 0）；分母 **10**；CP [15.8, 100] **[探索性]** | 见 §9.1 | 无第三方依赖 |
| 8 | `python -m pytest tests/ -m "not slow" -n0 -q` | 全绿（0 failed） | 见 §9.1 | pytest、pytest-xdist、hypothesis、pyyaml |

> **任务书里三条命令与仓库实际不符，如实登记（不改别人的工具）**：
> * `tools/holdout_reveal_665.py` **不存在** —— 真名是 `tools/holdout_reveal_3_665.py`（且**没有** `--run` 参数，跑就等于执行）。
> * `tools/external_corpus_662.py` **没有** `--run` 参数（该脚本无 argparse）；批量入口是 `tools/external_corpus_reveal_665.py`。
> * `tools/counterfactual_citation_658.py` **没有** `--eval` 参数（只有 `--assertion/--citation-id/--citation-text/--demo`）；
>   批量复算是 `tools/counterfactual_extend_665.py`，阈值扫描是 `tools/counterfactual_calibration_662.py`（无参数）。
> 以上都以 `argparse` 实测为准（`--help` / `grep add_argument`）。

### 9.1 耗时（本次实测）

跑 `python tools/reproduce_all_670c.py --mode run` 得到的逐步耗时见
`data/reproduction_report_670c.json::steps[].duration_s`（同一份报告里还有每步的退出码与
stdout/stderr 摘要）。参考区间（`pyproject.toml` 注释，589 批次 / 32 核 / Windows）：
fast 套件 `-n auto` ≈ **85–90s**、slow 套件 `-n0` ≈ **10–11 min**；
`-n0` 串行 fast 会明显更慢。**这些是参考值不是契约**（随机器负载与核数漂移）。

## 10. 一键编排器 `tools/reproduce_all_670c.py`

```powershell
.\.venv\Scripts\python.exe tools\reproduce_all_670c.py --list                       # 看 8 步与预期
.\.venv\Scripts\python.exe tools\reproduce_all_670c.py                              # 默认 verify（秒级）
.\.venv\Scripts\python.exe tools\reproduce_all_670c.py --mode run --skip-slow       # 真跑（跳过分钟级步骤）
.\.venv\Scripts\python.exe tools\reproduce_all_670c.py --mode run --only S3_holdout_reveal,S7_counterfactual
.\.venv\Scripts\python.exe tools\reproduce_all_670c.py --mode run --keep-outputs    # 复现者自己 clone：保留新产物
```

* 顺序：**门禁(S1,S2) → holdout(S3) → corpus(S4) → 变异(S5,S6) → 反事实(S7) → fast 测试(S8)**。
* **某步失败不中断**：一次跑完能看到 8 步的红绿，而不是修一步跑一次。
* **产物安全**：会写盘的步骤（S1/S3/S4/S7）的产物在跑之前**逐字节备份**，跑完在 `finally` 里**原样还原**；
  `--keep-outputs` 可关掉还原。报告 `artifacts[]` 给出每个产物的 `sha256_before/sha256_after/restored`，
  还原与否可复核，不靠口头保证。**本仓 670c 红线是"不碰 658/669d 的产物"**，所以：
  S1 默认只在 verify 下读 `data/658_gate_status.json`，真跑时也会还原；S2 一律加 `--no-write`。
* 报告：`data/reproduction_report_670c.json`（`steps[]` / `summary` / `overall` / `env` / `artifacts[]` / 时间戳）。
* 退出码：**0** = 跑到的步骤全匹配；**1** = 有步骤失败或不匹配；**2** = 参数错（未知 step id / 清单非法）。
* 诚实设计：`overall=PARTIAL` 表示**有步骤被跳过**（`--skip-slow` / `--only` / verify 模式无事实源的步骤），
  **不**把"没跑"写成"通过"。
* 已知限制：verify 模式下 `S8_fast_tests` 没有可判的落盘事实源 ⇒ 记 SKIP，`overall` 因此恒为 PARTIAL。
  要判它只能 `--mode run`。

## 11. 数据集元数据（Croissant 1.0）

`data/croissant_670c.json` 按 [Croissant 1.0](https://mlcommons.org/croissant/) 写：
`conformsTo = http://mlcommons.org/croissant/1.0`，含 `distribution[]`（`cr:FileObject`：
`contentUrl` / `encodingFormat` / `sha256` / `contentSize`）与 `recordSet[]`
（9 个记录集：holdout 种子 / 外部语料 / 缺陷夹具 / 反事实案例 / 665 机器卡 / AtomCard 台账 /
holdout reveal 逐样本 / corpus reveal 逐样本 / 变异测试汇总）。

* 全部 `sha256` 现取自 `data/dataset_hashes_670c.json`（不是手抄）。
* 每个 `field` 都来自**实际读到的 JSON 结构**（字段名、类型、说明），没有编字段。
* 两处诚实登记写进了文件里：`queyi:licenseNote`（LICENSE/SPDX = Apache-2.0，而 `pyproject.toml`
  的 `license` 字段写 MIT）、`queyi:citeAsNote`（论文未定稿，`citeAs` 只给仓库级引用）。

## 12. 数据完整性校验（复现者第一步）

```powershell
.\.venv\Scripts\python.exe tools\hash_datasets_670c.py            # 现算并刷新 data/dataset_hashes_670c.json
.\.venv\Scripts\python.exe tools\hash_datasets_670c.py --check    # 0=一致 / 1=冻结输入漂移 / 2=缺清单
.\.venv\Scripts\python.exe tools\hash_datasets_670c.py --list     # 只列射程（不读盘不写盘）
```

* 语义：`frozen=true` 是**输入**数据集（holdout / corpus / defects / counterfactual / cards_index / rules），
  漂移即 **ERROR**（exit 1）；`frozen=false` 是**产物**（reveal 报告 / 门禁状态 / 指标），漂移记 **WARN** 不阻断。
* 哈希的是**原始字节**，不做换行归一 ⇒ **CRLF 转换会显形**（§13.3）。
* 为什么先跑它：数字对不上只有两种原因 —— 数据漂了，或验证器变了。先跑 `--check` 才能把两者分开。
* 诚实边界：`--check` 只能证明"文件与某次落盘的清单一致"，**不能**证明清单自身可信（依赖 git 历史留痕）。

## 13. 常见问题（FAQ）

### 13.1 WSL 未安装 / `wsl` 命令没有输出
* 现象：第 3、4 条命令仍 **exit 0**，但 `unknown` 计数暴涨、检出率从 43.8% 掉到 10% 量级。
  **这不是**验证器变弱，而是**检测器不存在**（§6.1）。
* 先自检：`wsl -e bash -lc "g++ --version | head -1"`。打印不出 g++ 版本就是没装好。
* 装法：管理员 PowerShell 跑 `wsl --install -d Ubuntu` → 重启 → 进 Ubuntu
  `sudo apt-get update && sudo apt-get install -y g++`。
* 装不了 WSL 时怎么办：**不要**把 `unknown` 当 `miss` 统计 —— 那会把环境缺失伪装成能力下降。
  正确做法是只报"可测口径"并显式声明 `denominator.excluded`（产物里已经有这个字段）。
* 检查报告里 `env.wsl_gpp`（`tools/reproduce_all_670c.py` 的产物）是不是 `(不可用: ...)`。

### 13.2 sanitizer 相关失败
| 现象 | 含义 | 处理 |
|---|---|---|
| `unknown: 编译失败` | WSL 里 `g++` 编不过（缺 `-pthread` / 夹具语法错 / WSL 路径没转对） | 手工进 WSL 编一次看全量报错；检查 `/mnt/c/...` 路径转换（`_to_wsl` 在工具里） |
| `FATAL: ThreadSanitizer` / `TSan 无法初始化` | WSL 内核不支持（老内核 / 容器里 ASLR 配置不对） | 该样本记 `unknown`，**不计入分母**；或按 665 的做法做 `-O0` 敏感性复跑 |
| ASan 类样本在 `-O1/-O2` 下"报不出" | **不是** ASan 不会报，是优化把内存操作整段消掉了（无可观测副作用） | 666 起 pipeline 改为 **`-O0` + `-O2` 双档都跑**，任一档报出即 `catch`；历史 `-O0/-O1` 对照留在 `data/holdout_reveal_3_665.json::opt_sensitivity` |
| 检出率突然变高 | 先怀疑口径（分母/档位）而不是能力 | 对 `denominator` 与 `opt_levels` 两个字段，别只看率 |

### 13.3 CRLF / 换行导致哈希漂移
* 症状：`tools\hash_datasets_670c.py --check` 报一堆 ERROR，而 `git status` 干净。
* 处理：`git config core.autocrlf false`（Windows 检出）+ 重新 clone；仓库以 `.gitattributes` 的声明为准。
* 注意本工具的哈希面**故意是原始字节**：换行归一会让这类漂移**静默消失**，那正是要避免的。
* `data/657_crlf_convergence.json` / `.md` 是这条问题的历史记录。

### 13.4 其它
* **中文乱码**：工具都调 `tools/utf8_console.py::ensure_utf8()`；若还乱码，把终端切到 UTF-8
  （`chcp 65001` / `$OutputEncoding`）。
* **`pytest` 并行假红**：本仓 14+ 个模块共享 replay 全局锁与 `Examples/atoms` 工件，
  `-n auto` 会随机假红。**复现统一用 `-n0`**（§9 第 8 条）。
* **`uv` 还是 `.venv`**：§1/§5 的 `uv run` 是 661 的写法；670c 段一律用
  `.\.venv\Scripts\python.exe`（两者都指向同一个解释器口径）。**`uv` 未安装时 §1/§5 的命令会直接失败 —— 用 §7 的 venv 路径替代。**

## 14. 诚实登记（未核对 / 已知限制 / 与旧文冲突）

**已核对（有事实源）**：§8 的每个条数、§9 的每个率与 CI、§6 的每个版本、§12 的清单（54 个文件 / 838555 字节）。

**未核对 / 做不到的**：
1. **Python 3.11/3.12 的复算**：本机只有 3.13.13，CI 矩阵跑 3.11 但不跑本 kit ⇒ **未核对**。
2. **论文引用（`citeAs`）**：论文稿在 `research/`，670c 段按红线**不读**该目录 ⇒ 只给仓库级引用，**未核对**论文标题与作者列表。
3. **`--mode run` 的耗时数字**：随机器/负载/WSL 状态漂移，属**参考值非契约**；本次实测值见 §9.1。
4. **`data/holdout/holdout.json` 自带的 `audit_note` 已过期**：它写 662 当时的"真错 7 / 对照 8 / unknown 5"，
   而文件里 `planted` 字段实测是 **17 / 9 / 4**（665 追加 10 条真错后未同步该注释）。
   以 `planted` 字段与 `data/holdout_reveal_3_665.json::labels` 为准 —— 这条不改别人的产物，只登记。
5. **卡台账三处口径不一致（都真实存在，不静默择一）**：
   * `web/data/verdicts_667.json::dashboard.cards_real = 42`（**现算，采信**，与 `docs/669_独立审计.md` 一致）；
   * `web/data/status.json::cards.cards_real = 37`（陈旧）；`cards_index.json::count = 47`（37 实 + 10 草稿）。
   * `data/cards_665/index_665.json::total = 16` 是**机器卡**，与上面 42/47/52 **不是同一本账**，不可相加。
6. **§0 的"WSL（可选）"与"Node ≥20"已过时**：WSL 是硬依赖（§6.1）；Node 18 亦可（本机实测 + 根 `package.json` note）。
7. **任务书里的三条命令名与仓库不符**（§9 末尾已逐条列出真实入口）。
8. `data/dataset_hashes_661.json` 仍是 661 的 7 文件版本，**未**被本批替换（670c 另出 `…_670c.json`，不动旧产物）。

---

## 15. 前端复现（670c5 追加）

前端是**零构建静态站**（浏览器忽略 `web/package.json`），无需 `npm install` 即可打开；测试用纯 Node（jsdom 仅冒烟用，缺则跳过）。

```bash
# 1) 起本地静态服务器（不要用 file://，fetch 会被拦）
python -m http.server 8000 --directory web
#   打开 http://localhost:8000/index.html

# 2) 前端测试（888 断言，全绿）
cd web && npm test        # 或逐条：node tests/<name>.test.mjs

# 3) 重建 dist（可选；dist/ 被 .gitignore 忽略）
node web/build.mjs
python tools/dist_verify_670c2.py     # 8 HTML / 引用 0 缺失 / 首页 ≤200KB

# 4) 前端质量审计（静态，无需浏览器）
python tools/a11y_audit_670c4.py --write        # WCAG 2.1 AA：8 页 0 问题
python tools/responsive_audit_670c5.py --write  # 响应式：0 严重
python tools/perf_audit_670c5.py --write        # 性能：首页 gzip ≤120KB
```

**预期**：`npm test` 全绿（888 断言）；`a11y_audit` 输出 `critical=0`；`perf_audit` 首页 gzip ≈ 76KB。

**依赖说明**：上述 4 个前端命令**不需要 WSL / g++**（与 §6 的检测器复现不同）；只有 `holdout_reveal_*` / `external_corpus_reveal_*` 才需要 WSL。

**常见问题**：`file://` 打开时 `fetch` 被浏览器拦截 ⇒ 数据加载失败卡会提示改用 `python -m http.server`（这是 670c3 的预期行为，不是 bug）。

---

## 16. baseline 三臂 + 论文管线 + 门禁（670a / 670g 追加）

```bash
# 1) baseline 三臂（现算落盘 data/experiments/baseline_{static,random,fd}.json）
.\.venv\Scripts\python.exe tools\baseline_670a.py --run
.\.venv\Scripts\python.exe tools\baseline_670a.py --check     # 只读自检
#    预期：holdout FD 87.5%(14/16) vs Static 6.2%(1/16)；corpus FD 43.8%(14/32) vs Static 12.5%(4/32)

# 2) 论文管线五工具（全 PASS 才算过）
python tools/paper_sync_check_670c2.py       # md(v0.8) ↔ tex 数字一致性
python tools/bib_audit_670c2.py              # 48 条 BibTeX，0 error
python tools/figure_data_check_670c2.py      # Fig.3/4 数字可溯源
python tools/anonymity_check_670c2.py        # 主文 0 仓库路径
python tools/paper_quality_gate_670c2.py     # 主文 ≤9 页 / 0 未定义引用 / 摘要 ≤250 词

# 3) 670g 六条 P0 门禁（论文/baseline 维度）
python tools/gate_rules_670g.py --check      # 0 BLOCK

# 4) 主门禁（含 L1 的 670g/paper-* 五阶段）
.\.venv\Scripts\python.exe tools\run_master_gate_670c.py --check
```

**依赖**：上述命令**不需要 WSL / g++**（与 §6 的检测器复现不同）。
**注意**：主门禁的 `670c/controlled-dirs` 阶段在**有并行批次改仓库时可能偶发报 1 处写入**（快照期间文件被并发修改）；重跑即可确认（本仓实测：首跑 1 处、复跑 0 处）。

---

## 17. W3–W6 扩样 / 裁判臂 / 外部锚定 / 统计重做（672h–672k · 673b D2 补）

### 17.0 快速门禁与前端预览

```bash
# 批次回归默认（门禁三件套 + 本批测试，<5 分钟）
python tools/fast_gate.py --tests tests/test_<本批>.py
python tools/fast_gate.py --all                  # 全部非 slow 测试 + 前端（三路并发）

# 前端自测（23 个测试文件 / 1500+ 断言，~14s，无需浏览器）
node web/run_tests.mjs

# 前端预览（无构建步骤；file:// 会被 fetch 拦截，必须走 http）
python -m http.server 8099 --directory web       # http://127.0.0.1:8099/
```

### 17.1 W3 扩样（672h）：holdout 21→41、corpus 48→64

```bash
python tools/holdout_merge_672h.py --write       # h31–h60 幂等合并进 data/holdout/holdout.json
python tools/holdout_reveal_5_672h.py            # 逐样本 WSL 编译 ⇒ data/holdout_reveal_5_672h.json
python tools/external_corpus_reveal_672h.py      # d3e-* ⇒ data/external_corpus_reveal_672h.json
python tools/verify_expand_672h.py               # 双路径复算（<0.1pp），写 data/experiments/verify_expand_672h.json
#    预期：holdout 34/41=82.9%（unknown 1 不进分母）；corpus 40/64=62.5%（unknown 9 不进分母）
```

### 17.2 W4 LLM 裁判臂（672i）

```bash
python tools/llm_arm_672i.py                     # 预注册 H1–H4 ⇒ data/experiments/llm_arm_672i.json
#    结论（诚实登记）：H1–H4 全不成立——LLM 臂检出率低于 FD 且假阳性更高，见产物与 672i 验收报告
```

### 17.3 W5 外部锚定（672j）

```bash
python tools/external_anchor_fetch_672j.py       # 抓公开 C++ 题库 raw（URL+sha256 留痕）
python tools/external_anchor_672j.py             # 判决 ⇒ data/external_anchor_reveal_672j.json
#    预期：50 条样本（准则反例 35 + 重建 UB 15）
```

### 17.4 W6 统计重做（672k）

```bash
python tools/stats_672k.py                       # McNemar / Cohen h / CP / power / e-value ⇒ data/experiments/stats_672k.json
python tools/drift_watch_671a.py --selftest      # 三方数字 + 空值加固自检（673b A2 后 28 条断言）
python tools/guard_rerun_671a.py                 # 18 检测器全 OK（673b A4 扩容后）
```

### 17.5 环境常见问题（如实登记）

| 问题 | 现状 / 绕法 |
|---|---|
| Node 18 无法装 playwright | 永久边界：前端验证走 jsdom / 纯 Node 测试（run_tests.mjs）；真实浏览器需手动截图清单 |
| WSL 编译慢 | holdout/corpus reveal 逐样本 g++ 编译，全量约 1–5 分钟；只有 slow 档测试会触发 |
| tectonic 下载慢/失败 | PDF 构建依赖 tectonic；网络受限时配代理或用 `generate_pdf.sh` 的缓存路径 |
| Windows 控制台 UTF-8 | 工具已内置 `utf8_console` 兜底；PowerShell 建议 `chcp 65001` |
