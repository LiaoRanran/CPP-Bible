# REPLICATION.md · 复现指南（661 D2）

> 目标：任何人（或未来的我）能按此把 queyi 验证器的关键结论**跑出来**。
> 配套：`run_reproduction.sh`（POSIX）、`data/dataset_hashes_661.json`（数据集哈希）。

## 0. 前置

| 依赖 | 版本 | 用途 |
|---|---|---|
| Python | ≥3.11（本仓用 `uv` 管理） | 全部工具/测试 |
| [uv](https://docs.astral.sh/uv/) | ≥0.11 | `uv run` 一键环境 |
| Node.js | ≥20 | `web_logic_check_655.mjs`（前端台账哈希） |
| g++ / clang++ | g++≥13、clang≥15 | 缺陷注入的编译检测 |
| WSL（可选） | Ubuntu 22.04+ | TSan/ASan/UBSan 真机检测（holdout reveal） |

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
