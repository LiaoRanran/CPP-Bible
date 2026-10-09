# 706 Task D — 投稿前终检报告

- 日期：2026-10-09
- 论文：`research/latex/queyi_neurips2027_v1.1.tex`（全稿 36 页 / 正文 9 页）

## 1. 匿名化终检 —— PASS

| 扫描 | 结果 |
|------|------|
| 论文 tex：`LiaoRanran` / `Liao, Ran` / `Ran Liao` / `1026708211` / `@qq.com` / `github.com/LiaoRanran` / `合肥` / `Hefei` / `Fuzhou` / `University` | **0 命中** |
| `tools/anonymity_check_670c2.py` | `STRICT 命中 0，MAIN 命中 0` → **PASS** |

- Cover letter 亦不含作者姓名（正文以 “The Authors” 落款），符合匿名审稿。
- （说明：`CITATION.cff` 含作者信息且题名陈旧，但那是仓库元数据、非投稿论文，**不在匿名范围内**；其题名问题另见 §7。）

## 2. 数字一致性终检 —— PASS（0 missing）

- `tools/verify_paper_numbers.py`：**检察 130 条；missing 0；consistent 116**；692 批次自洽 **35/35 PASS**。

### 2.1 五处手工复算（从冻结产物独立重算）

| 论文数字 | 权威源 | 复算 | 一致 |
|----------|--------|------|------|
| OR 检出 61.6% / 盲区 38.4% | `data/blindspot_676g_stats.json` | 707/1147 = 0.6164；440/1147 = 0.3836 | ✅ |
| 真实靶场 59.09% | `data/683_real_world_detection_matrix.json` | 65/110 = 0.590909（字段 `or_catch_rate_pct=59.0909`） | ✅ |
| A5 $k{=}4$ $\Delta$(FD−Random) $+24.03$pp | `data/a5_676f_results.json::primary_main_8candidates` | 54.5936 − 30.5654 = 24.0282 | ✅ |
| 环境 E1 60.07% / E2 24.74% | 566 分母 | 340/566 = 0.6007；140/566 = 0.2473 | ✅ |
| 盲区 >50% 的类型 13/34 | `data/681_type_stats_normalized.json` | `n_types=34`，`types_gt50_blind=13` | ✅ |

### 2.2 关于 `verify_paper_numbers.py` 的一处必要修改（诚实披露）

706 减页把 4 个附录节移入 `supplementary/paper_appendix_extras.tex`，导致其中 **5 条** 数字（`F08x.legacy`、`F08x.concurrency`、`F10x.planted_false`、`F10x.planted_true`、`D14`）在主稿中“消失”，被工具判为 `missing`。

**处理**：为工具新增 `--tex-extra`（默认 `supplementary/paper_appendix_extras.tex`），把 Supplementary 文本**并入同一扫描域**（页数仍取主稿 log）。
- **这不是放宽检查**：数字仍必须存在于“主稿 ∪ Supplementary”（本文的完整投稿件）中，只是扫描范围与 706 后的结构对齐。
- 修改后：**missing 0**（consistent 116），与 706 前基线一致。
- 影响：`unclassified token` 由 113 → 156（因并入 Supplementary 的全文 token）；不影响任何 claim 判定。
- 修改文件：`tools/verify_paper_numbers.py`（+12 行，纯新增参数与并入逻辑）。

## 3. TODO 清零 —— PASS

- 论文 tex `TODO|FIXME|XXX`：**0 命中**。
- `paper_quality_gate`：`仅已登记占位（TODO{670a} 宏 + 0 个 ablation 占位）` → 通过。

## 4. 引用完整性 —— PASS

- `tools/bib_audit_670c2.py` → **PASS**（所有 `\cite` 均有 bib 条目）。
- 反向提示（非错误，信息级）：4 个 bib 条目从未被 `\cite`（`sadasivan2023canai`、`shadish2002experimental`、`shankar2025leaderboard`、`skalse2022rewardhacking`）——保留备选，未清理。

## 5. 编译终检 —— PASS

| 项 | 结果 |
|----|------|
| tectonic 编译错误 | **0** |
| 全稿页数 | **36**（≤36 ✅） |
| 正文页数（page:endmain） | **9**（≤9 ✅） |
| 未定义引用 | **0** |
| 摘要词数 | **229**（≤250 ✅） |

## 6. paper_gate —— 6/6 PASS

```
[OK] 主文页数≤9        page:endmain -> 9 页
[OK] 0 未定义引用      undefined 条目 0
[OK] 所有 \section 有 \label   8/8
[OK] 所有 \ref 有 \label       31/31
[OK] 摘要≤250词        229
[OK] 无 TODO/FIXME     仅已登记占位
[paper-gate] PASS
```

## 7. 两个**预先存在**的检查失败（诚实披露，非 706 引入）

`build.ps1` 还跑另两项检查，它们**失败，但在 706 之前（HEAD）就已失败**，与减页无关——已核验：

| 检查 | 现象 | 是否 706 引入 | 证据 |
|------|------|---------------|------|
| `paper_sync_check_670c2.py` | `e-value 量级`：tex 缺 `2.5\times10^8` | **否** | 该字面量在 `git HEAD` 原稿中出现 **0 次**（706 前后均为 0） |
| `figure_data_check_670c2.py` | 缺 Fig.3（holdout）/ Fig.4（批次）坐标块 | **否** | `coordinates` 在 `git HEAD` 原稿中 **0 次**（论文从未含 pgfplots 坐标块） |

- 这两项**不属于** “paper_gate”（= `paper_quality_gate`，已 6/6 PASS）。
- 交叉验证减页未破坏它们：`holdout` 词频 HEAD=44 = 工作树 41 + extras 3（移出恰 3 处，无额外丢失）。
- **建议**：paper_sync/figure_data 属 707 待办（补 e-value 量级表述 / 恢复或重构 Fig.3-4 坐标块），本批不动（超 706 范围）。

## 8. 遗留（写入验收报告）

1. **人类 IAA = 0**（最大未解决项）。
2. `CITATION.cff` 仍含旧题名（超出 README-only 范围）。
3. `paper_sync` / `figure_data` 两项预存失败（非本批引入）。
