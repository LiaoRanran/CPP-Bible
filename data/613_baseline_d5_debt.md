# 613 基线 0.4 · D5 基准文件债务台账

> 生成：`python tools/613_baseline.py` ｜ 时间：2026-09-20T23:54:27
> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。

## 计数

| 项 | 数 |
|---|---|
| Book 中声明的基准源（去重） | 123 |
| 仓库根 `_bench_d5_*.cpp` | 0 |
| `_archive/benchmarks/` 中 | 126 |
| 磁盘合计（根 ∪ archive） | 126 |
| 声明但两处都缺失 | 0 |
| 孤儿（存在但未被 Book 引用） | 3 |

## 真·缺失（声明但磁盘不存在）

- 共 **0** 个（无）

## 孤儿文件（磁盘存在但 Book 未引用）

- 共 **3** 个：_bench_d5_ch37_demo.cpp、_bench_d5_ch38_demo.cpp、_bench_d5_ch50_demo.cpp

## 根因

- `tools/d5_source_integrity.py` 的契约是「每条声明对应**仓库根**一个真实存在且 git 跟踪的 `_bench_d5_X.cpp`」；而基准源实际已迁至 `_archive/benchmarks/`（未 ignore，git 已跟踪）。
- ⇒ 门禁判「声明但磁盘缺失/未跟踪」，**并非文件内容真的丢失**。

> 与任务书假设的偏差：任务书写「8 章引用缺失 + 22 孤儿文件」，实测见上表（以实测为准）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `direct_experiment`
- `materiality_flag`: false
