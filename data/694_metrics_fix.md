# 694-C · metrics 修复记录（`gen_metrics.py --check` 3 处不一致 → 0）

批次：694 · 起点 HEAD `acc9cf9b`（693-G） · 日期 2026-10-08

---

## 1. 现象（修复前）

```
python tools/gen_metrics.py --check
✗ 3 处数字与事实源不一致：
  - README.md:141: 写死 515，事实源 cpp_blocks=7515
  - README.md: 未匹配到 '(\d+)\s*章，(\d+)\s*章自包含通过'——文档结构变了
  - README.md: 未匹配到 '(\d+)/(\d+)\s*章（(\d+)%'——文档结构变了
```

事实源（`metrics.schema.json` → 实时扫描 `Book/` + `tools/compile_report.json` + git，
**非** `build/metrics.json` 快照）：

| 字段 | 值 |
|---|---|
| chapters | 147 |
| md_total | 151 |
| lines | 255897 |
| **cpp_blocks** | **7515** |
| d5_coverage | 127 |
| exercise_total | 700 |
| verified | 165 |
| compile_total_chapters | 147 |
| compile_passed_chapters | 115 |
| d5_pct | 86（= round(127/147×100)） |
| commit | acc9cf9b |

---

## 2. 三处问题的性质（**与任务卡预判不同，实测为准**）

### 2.1 `README.md:141` 写死 515 —— **不是数字错，是千分位逗号导致正则截断**

原文：`> **147 章 · 16 part · 约 25.6 万行 · 7,515 个 cpp 代码块**`

值 **7,515 是对的**（= 事实源 7515）。问题是 schema 正则
`(\d+)\s*个 cpp 代码块`（`metrics.schema.json:37`）里的 `\d+` **不匹配逗号**，
`re.search` 于是从 `7,515` 的 `515` 处起匹配 ⇒ 抓到 `515` ≠ `7515`。

处置（按任务卡"修法1：改 README 比改检查逻辑更安全"）：去掉千分位逗号 → `7515`。
**数值信息零变更**，只去掉分隔符；未动 `metrics.schema.json`、未动 `gen_metrics.py`
（后者若改正则还需同步做逗号归一，改动面更大，且会稀释"散文文档只校验"的分工）。

### 2.2 / 2.3 两条"文档结构变了" —— **693 统一 README 时删掉了这两行，锚点丢失**

比对 `git show 1f34ca9f~1:README.md`（693-C 之前的 README），原表里有两行：

```
| 全量编译 | `python tools/compile_all.py --main-only` | 147 章，115 章自包含通过 |
| D5 性能附录 | `python tools/d5_gap_scanner.py` | 127/147 章（86%，口径已统一），结构 ERROR=0 / WARN=3（措辞建议，不阻断） |
```

693-C（"unified README"）重写了 §7 的门禁表，只保留 5 行，这两行被删 ⇒
`metrics.schema.json:38-39` 的两条正则在 README 里再也匹配不到 ⇒ 门禁报"文档结构变了"。

处置（同样选**修法1**）：把这两行**按原措辞补回** §7 门禁表（现 README:161-162），
数值全部取自事实源，未沿用旧文本里未经本批复核的部分——
`结构 ERROR=0 / WARN=3` 是本批**未实测**的数字，按"禁止预写未核实数字"纪律**不写入**。

---

## 3. 改动清单（README.md，共 3 行）

| 行号 | 改前 | 改后 | 事实源字段 |
|---|---|---|---|
| 141 | `· 7,515 个 cpp 代码块` | `· 7515 个 cpp 代码块` | `cpp_blocks=7515` |
| 161 | （无此行） | `\| 全量编译 \| \`python tools/compile_all.py --main-only\` \| 147 章，115 章自包含通过 \|` | `compile_total_chapters=147`、`compile_passed_chapters=115` |
| 162 | （无此行） | `\| D5 性能附录 \| \`python tools/d5_gap_scanner.py\` \| 127/147 章（86%，口径已统一） \|` | `d5_coverage=127`、`chapters=147`、`d5_pct=86` |

`git diff -- README.md` 实测：1 处替换 + 1 处 2 行插入，**无其它改动，无整文件伪 diff**（行尾原样）。

---

## 4. 正则匹配验证（修复后）

```
python tools/gen_metrics.py --check
[gen-metrics] ✅ 全部文档数字与事实源一致        （exit 0）
```

五条 checks 逐条对账（`metrics.schema.json:35-41`）：

| 正则 | 匹配到的文本 | 抓取值 vs 事实源 |
|---|---|---|
| `(\d+)\s*章 ·` | `147 章 ·` | 147 = chapters ✅ |
| `(\d+)\s*个 cpp 代码块` | `7515 个 cpp 代码块` | 7515 = cpp_blocks ✅ |
| `(\d+)\s*章，(\d+)\s*章自包含通过` | `147 章，115 章自包含通过` | 147/115 = compile_total/passed ✅ |
| `(\d+)/(\d+)\s*章（(\d+)%` | `127/147 章（86%` | 127/147/86 = d5_coverage/chapters/d5_pct ✅ |
| `(\d+)\s*章 C\+\+ 技术书`（NEXT_LLM.md） | — | 147 = chapters ✅ |

---

## 5. 诚实边界

- 未用 `gen_metrics.py --fix` / `--sync` 自动回填（`--fix` 只替换正则锚定的数字位，
  对"正则失配"这 2 条**无能为力**，必须人工补文档）；`STATE.json` 亦未回写（本批未涉及）。
- 未改 `metrics.schema.json` 的任何正则 —— 保持"文档跟着事实源走"，而不是"让检查器迁就文档"。
- 补回的两行只写已核实数字；旧 README 里的 `结构 ERROR=0 / WARN=3` **未复写**（本批未实测，不预写）。
