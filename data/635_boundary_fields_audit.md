# 635 1.1 · 边界字段回填审计

- `data/*baseline*` 文件：**34** 个
- 5 字段：`mutation_set_hash` / `mutation_count` / `generator_version` / `evidence_channel` / `materiality_flag`

| 文件 | mutation_count | generator_version | evidence_channel | materiality |
|---|---|---|---|---|
| `609_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `611_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `612_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | false |
| `613_baseline_argumentation.md` | 1593 | mutation_fuzz@v7 | human_review | false |
| `613_baseline_ci.md` | 1593 | mutation_fuzz@v7 | direct_experiment | false |
| `613_baseline_d5_debt.md` | 1593 | mutation_fuzz@v7 | direct_experiment | false |
| `613_baseline_learner_twin.md` | 1593 | mutation_fuzz@v7 | direct_experiment | false |
| `614_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `615_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `616_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `617_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `618_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `619_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `620_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `621_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `622_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `623_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `624_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `625_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `626_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `627_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `628_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `629_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `630_baseline.json` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `630_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `631_baseline.json` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `631_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `632_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `634_baseline.md` | 1593 | mutation_fuzz@v7 | human_review | true |
| `634_soft_baseline.json` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `635_baseline.json` | 1593 | mutation_fuzz@v7 | direct_experiment | true |
| `635_baseline.md` | 1593 | mutation_fuzz@v7 | human_review | true |
| `autoimmune_rate_baseline.md` | 1593 | mutation_fuzz@v7 | standard_textbook | true |
| `ev_matrix_dual_impl_baseline_616.json` | 1593 | mutation_fuzz@v7 | direct_experiment | true |

- `mutation_set_hash`（统一，当前规范 mutation 集）：`d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`

## 诚实登记

1. `evidence_channel` / `materiality_flag` 为**内容关键词启发式**推断（非人工逐份标注）；
2. `mutation_set_hash` 取**当前规范** mutation 集（历史 baseline 未各自绑定专属集，统一引用 v7）——如实说明该简化；
3. 回填**只追加小节/加键**，不改任何既有内容与判决。
