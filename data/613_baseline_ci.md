# 613 基线 0.1 · CI 四 job 现状台账

> 生成：`python tools/613_baseline.py` ｜ 时间：2026-09-20T23:26:23
> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。

仓库 `LiaoRanran/CPP-Bible` ｜ API 总运行数=605

## Run #605（queued / **None**）

- head_sha：`f78c4f7f54c8` ｜ 事件=push ｜ 分支=master ｜ 创建=2026-09-20T15:26:08Z
| job | conclusion | 失败步骤 |
|---|---|---|
| quality (3.11) | None | — |
| replay | None | — |
| gate | None | — |
| pytest | None | — |

## Run #604（completed / **failure**）

- head_sha：`d365be6b9cae` ｜ 事件=push ｜ 分支=master ｜ 创建=2026-09-20T15:13:10Z
| job | conclusion | 失败步骤 |
|---|---|---|
| quality (3.11) | failure | D5 Appendix Structure Audit (性能附录格式合规门禁) |
| gate | failure | S1-S6 Controls (黄金锁 / 债务台账 / 毒样例演练) |
| pytest | failure | Pytest (xdist 并行 · 工具链回归测试) |
| replay | success | — |
| publish-check | skipped | — |
| pdf | skipped | — |
| Compile (${{ matrix.name }}) | skipped | — |
| deploy | skipped | — |
| epub | skipped | — |
| site | skipped | — |

## Run #603（completed / **cancelled**）

- head_sha：`fbe1c684542e` ｜ 事件=push ｜ 分支=master ｜ 创建=2026-09-20T15:12:42Z
| job | conclusion | 失败步骤 |
|---|---|---|
| quality (3.11) | cancelled | — |
| replay | cancelled | — |
| pytest | cancelled | — |
| gate | cancelled | — |
| publish-check | cancelled | — |
| Compile (${{ matrix.name }}) | cancelled | — |
| pdf | cancelled | — |
| epub | cancelled | — |
| site | cancelled | — |
| deploy | cancelled | — |

> 判定口径：CI 结论以 API 为准（外部视角，最权威）。本批不本地复跑监工工具。
