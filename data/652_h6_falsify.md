# 652 H6 · ESBMC falsification 试点

- esbmc 可用：**False**｜unwind=8｜探针 1

| 探针 | 状态 | 说明 |
|---|---|---|
| data/652_h5_probe.c | tool_unavailable | esbmc data/652_h5_probe.c --unwind 8 --no-div-by-zero-check |

> 语义：BMC 失败=硬结论(witness)；BMC 成功**仅** unknown(bounded)（有界通过≠全称）。
