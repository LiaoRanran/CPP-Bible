# 669 口径报告（现算 + CI）

> 由 `tools/caliber_check_669.py --write` 生成；数字全部现算，不手打。
> 区间口径：Clopper–Pearson 精确（实现单一来源 `tools/stat_bounds.py`），Wilson 作敏感性列。

| 口径 id | 说明 | k/n | 点估计 | Clopper–Pearson 95% | Wilson 95% | 事实源 |
|---|---|---|---|---|---|---|
| `external.valid` | 外部 corpus（可测口径） | 14/32 | 43.8% | [26.4, 62.3] | [28.2, 60.7] | `data/external_corpus_reveal_665.json` |
| `external.all` | 外部 corpus（全样本口径） | 14/40 | 35.0% | [20.6, 51.7] | [22.1, 50.5] | `data/external_corpus_reveal_665.json` |
| `external.a` | 外部 corpus 分层 A | 13/24 | 54.2% | [32.8, 74.4] | [35.1, 72.1] | `data/external_corpus_reveal_665.json` |
| `external.a.total` | 外部 corpus 分层 A（含 unknown 的全层） | 13/25 | 52.0% | [31.3, 72.2] | [33.5, 70.0] | `data/external_corpus_reveal_665.json` |
| `external.b` | 外部 corpus 分层 B | 1/8 | 12.5% | [0.3, 52.7] | [2.2, 47.1] | `data/external_corpus_reveal_665.json` |
| `external.b.total` | 外部 corpus 分层 B（含 unknown 的全层） | 1/11 | 9.1% | [0.2, 41.3] | [1.6, 37.7] | `data/external_corpus_reveal_665.json` |
| `external.c` | 外部 corpus 分层 C | 0/0 | 0.0% | [0.0, 100.0] | [0.0, 100.0] | `data/external_corpus_reveal_665.json` |
| `external.c.total` | 外部 corpus 分层 C（含 unknown 的全层） | 0/4 | 0.0% | [0.0, 60.2] | [0.0, 49.0] | `data/external_corpus_reveal_665.json` |
| `holdout.valid` | holdout 真错（双档口径） | 14/16 | 87.5% | [61.7, 98.4] | [64.0, 96.5] | `data/holdout_reveal_3_665.json` |
| `holdout.control_fp` | holdout 对照（误报） | 1/9 | 11.1% | [0.3, 48.2] | [2.0, 43.5] | `data/holdout_reveal_3_665.json` |
| `counterfactual.p` | 反事实算子 P | 2/2 | 100.0% | [15.8, 100.0] | [34.2, 100.0] | `data/counterfactual_cases_665.json` |
| `counterfactual.r` | 反事实算子 R | 2/2 | 100.0% | [15.8, 100.0] | [34.2, 100.0] | `data/counterfactual_cases_665.json` |
| `external.unknown_as_miss` | external（unknown 记 miss） | 14/37 | 37.8% | [22.5, 55.2] | [24.1, 53.9] | `data/external_corpus_reveal_665.json` |
| `holdout.unknown_as_miss` | holdout 真错（unknown 记 miss） | 14/17 | 82.4% | [56.6, 96.2] | [59.0, 93.8] | `data/holdout_reveal_3_665.json` |
| `mutation.core` | 内部变异 core | 110/113 | 97.3% | [92.4, 99.4] | [92.5, 99.1] | `data/656_mutation_report_core.json` |
| `mutation.all` | 内部变异 all | 128/157 | 81.5% | [74.6, 87.3] | [74.7, 86.8] | `data/656_mutation_report_all.json` |
