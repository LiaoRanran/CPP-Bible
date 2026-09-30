# 670d · Baseline 实验脚本设计（命令级）

> **性质**：设计规格（**不实现、不跑**；红线 1 禁止碰 `tools/`、`data/experiments/`）。
> **前置接口**：B1 的 `detect_static` 与 B3 的 `select_assets` **主仓没有**，须由拆仓验证器 `queyi-verifier`（670c）暴露——本文件把接口契约写死，供实现方对齐。

---

## 0. 三类 baseline（对应 §5.2）

| ID | 名称 | 定义 | 关键对齐条件 |
|---|---|---|---|
| **B1** | 静态门禁（rule-only） | 只跑静态规则，**不获取运行时证据** | 同语料、同判定粒度 |
| **B2** | 静态 + 变异 | B1 + 变异测试（L1 自证层全开） | 同上 + 同变异预算 |
| **B3** | budget-matched random | **同等预算下随机**扩充证据（不按失败驱动选） | 同预算（时间/调用次数）、同语料、同档位 |
| **Full** | 失败驱动（现状系统） | 按 miss/unknown 归因新增证据能力 | 与 B1/B3 同语料同口径 |

---

## 1. B1 · 静态门禁（rule-only）

### 1.1 实现步骤（命令级）

```bash
# 前提：queyi-verifier 暴露 detect_static(sample) -> verdict
# 1) 导出被测样本集（D2 + D3 的 canonical 视图，只读）
python -c "import json; d=json.load(open('data/holdout/holdout.json')); print(len(d['seeds']))"   # D2: 30
# 2) 逐样本跑静态判定（不编译、不运行）
python -m queyi_verifier.detect_static --samples data/holdout/holdout.json \
    --rules gate_engine.RULES --out <TMP>/b1_holdout.json
python -m queyi_verifier.detect_static --samples data/external_corpus/external_corpus_665.json \
    --rules gate_engine.RULES --out <TMP>/b1_corpus.json
# 3) 汇总（现算率 + CP CI）
python -m queyi_verifier.summarize --in <TMP>/b1_holdout.json --caliber planted_true --cp-ci
```

> **`<TMP>` 必须是仓库外临时目录**（红线 1：不写 `data/experiments/`）。

### 1.2 输入 / 输出格式

**输入**：`data/holdout/holdout.json`（`seeds[]`：`id/planted/atom_ref/detector`）、`data/external_corpus/external_corpus_665.json`（`samples[]`：`id/expected_detector`）。

**输出 schema**（`b1_*.json`）：
```json
{
  "schema": "queyi-baseline/v1",
  "baseline": "B1-static",
  "caliber": {"denominator": "planted_true_measurable", "opt_levels": null},
  "budget": {"wall_sec": 0.0, "detector_calls": 0, "note": "静态：无运行时调用"},
  "env": {"wsl": false, "gpp": null},
  "per_sample": [{"id": "h1", "verdict": "catch|miss|unknown|not_error", "evidence": "rule_id"}],
  "summary": {"k": 0, "n": 0, "rate_pct": 0.0, "cp95": [0.0, 0.0]}
}
```

### 1.3 budget-matched 保证

- **B1 天然是"零运行时预算"** ⇒ 对齐点是"**同语料 + 同判定粒度**"，不是时间。
- 产物必须记 `budget.detector_calls = 0`，作为 B3/Full 的预算下界参照。

### 1.4 统计检验（McNemar 配对表）

B1 vs Full 是**同批样本配对**。建表（仅"可测真错"子集）：

| | Full catch | Full miss |
|---|---|---|
| **B1 catch** | a | b |
| **B1 miss** | c | d |

- **精确 McNemar**：`p = 2 * Σ_{i=0}^{min(b,c)} C(b+c,i) 0.5^{b+c}`（二项精确）。
- **效应量**：Cohen's h（比例差）。
- **命令级**：`python -m queyi_verifier.mcnemar --pair <TMP>/b1_holdout.json <TMP>/full_holdout.json`

---

## 2. B2 · 静态 + 变异

### 2.1 实现步骤

```bash
# 在 B1 基础上追加变异测试（L1 自证层）
python -m queyi_verifier.detect_static --samples data/holdout/holdout.json \
    --rules gate_engine.RULES --mutation data/656_mutation_report_core.json \
    --out <TMP>/b2_holdout.json
```

### 2.2 与 B1 的差异

- 额外记录 `mutation.kill_rate`（**内部指标**，不得当检测率）。
- **预写假设（§5.3 组 B）**：加变异**不改变外部召回**——若 B2 外部召回显著高于 B1，则假设被推翻，**原样报告**。

### 2.3 统计检验

- B1 vs B2：配对 McNemar（同批）。
- 若外部召回差值 CI **跨 0** ⇒ "变异提升外部检测"不成立。

---

## 3. B3 · budget-matched random

### 3.1 实现步骤

```bash
# 需要 queyi-verifier 暴露 select_assets(pool, n, strategy, seed)
# 1) 记录 Full 的预算（时间/调用次数），作为对齐目标
python -m queyi_verifier.budget --run full --out <TMP>/full_budget.json
# 2) 随机选同数量资产（固定种子 + 分配表）
python -m queyi_verifier.select_assets --pool data/holdout/holdout.json \
    --n $(jq '.assets_selected' <TMP>/full_budget.json) --strategy random --seed 20260930 \
    --out <TMP>/b3_alloc.json
# 3) 用随机选中的资产扩充能力，再测同一批 X
python -m queyi_verifier.run_pipeline --alloc <TMP>/b3_alloc.json \
    --samples data/holdout/holdout.json --out <TMP>/b3_holdout.json
```

### 3.2 budget-matched 保证（**最关键**）

必须同时对齐三项，并**写进产物**：
- **资产数量**：`assets_selected` 相同；
- **检测器调用次数**：`detector_calls` 相同（±0）；
- **墙钟时间**：`wall_sec` 在 ±10% 内。

**随机臂必须带种子 + 分配表**（`seed` + `alloc.json`），否则不可复算。

### 3.3 统计检验

- **Full − B3**：配对 McNemar（同批 X）。
- **判读规则（预写，§6.2）**：若差值 CI **跨 0** ⇒ "失败驱动优于随机预算"**不成立**，必须原样报告。

---

## 4. 统一产物 schema 与检验矩阵

| 字段 | 说明 |
|---|---|
| `schema` | `queyi-baseline/v1` |
| `baseline` | `B1-static` / `B2-static+mutation` / `B3-random` / `full` |
| `caliber` | `denominator` + `opt_levels`（必须显式，防 §7.4 第 2 点的口径漂移） |
| `budget` | `wall_sec` / `detector_calls` / `assets_selected` |
| `env` | `wsl` / `gpp`（缺 WSL 时判 `UNVERIFIED`，不得判 `unknown`） |
| `per_sample[]` | `id → verdict`（供 McNemar 配对） |
| `summary` | `k/n/rate_pct/cp95`（CP 单一来源 `tools/stat_bounds.py`） |

**检验矩阵**：

| 对比 | 检验 | 效应量 | 多重比较 |
|---|---|---|---|
| B1 vs B2 | 精确 McNemar | Cohen's h | 3 baseline → Holm |
| B1 vs Full | 精确 McNemar | Cohen's h | Holm |
| B2 vs Full | 精确 McNemar | Cohen's h | Holm |
| **B3 vs Full** | 精确 McNemar | Cohen's h | **Holm（最关键）** |

---

## 5. 一句话

> baseline 的难点**不是算法**，而是**对齐**：B1 对齐"同粒度"、B2 对齐"同变异预算"、**B3 对齐"同预算"**。**B3 是唯一能证伪"失败驱动"的对照**——没有它，"失败驱动更有效"就只是"投入更多所以看起来好"（T8）。
