# 659 · 语料基数（唯一权威源：`tools/counts_659.py` 现算）

> 本文件由 `python tools/counts_659.py --md` 生成，**禁止手改**。
> 口径依据：`data/655_baseline.md`（47 = 37 实卡 + 10 draft650）、`README.md`。

| 量 | 值 | 事实源 |
|---|---:|---|
| 原子卡·实卡 | 37 | `atoms/*/ATOM-*.md`（不含 `draft650/`） |
| 原子卡·草稿 | 10 | `atoms/draft650/ATOM-*.md` |
| 原子卡·全量 | 47 | 实卡 + 草稿 |
| 证据卡 | 66 | `evidence/**/EV-*.md` |
| 卡·实卡口径 | 103 | 原子实卡 + 证据卡（历史写死 103 的口径） |
| 卡·全量口径 | 113 | 原子全量 + 证据卡（当前口径） |

## 去写死规则（659 A/B3）

1. 新写的断言**禁止**再裸写上述数字；一律 `import counts_659 as counts` 后
   用 `counts.ATOMS_TOTAL` / `counts.CARDS_TOTAL` 等常量。
2. 语义不同要选对常量：只遍历 5 个域目录（`conc/hist/lang/mem/ub`）的工具
   应取 `ATOMS_REAL`（`tools/evidence_base_644.py::list_atoms` 即此口径）；
   用 `atoms/**/ATOM-*.md` 通配符的工具应取 `ATOMS_TOTAL`。
3. 语料真扩容后，本文件随 `--md` 自动更新；测试无需再改数字。
