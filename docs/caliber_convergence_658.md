# 658 E1 · 口径收敛

> 目标：文档/README/baseline.json 数字对齐；差异登记并由 status_reconciler（D 段）对账。

## 已对齐（verified，入 baseline.json）

| 项 | 值 | 来源 |
|---|---|---|
| HEAD | eb700aec（657 收工，未含 658 提交） | `git rev-parse` |
| cards(atoms) | 48 | glob atoms |
| mutation | core 97.3% / all 81.5% | data/656_mutation_report_* |
| graph | 178 节点 / 1093 边 | web/data/graph.json |
| boundary | 26 卡有边界（23 verified + 3 red-team） | data/657_boundary_backfill.json |

status_reconciler_658.py 已對这五项与 git/fs 实际值对账（HEAD 漂移会在每次提交后刷新 baseline）。

## 已收敛（**666 A6 定位完成**，两处"权威源不明"都不是冲突）

> 666 A6 的活就是"把不能机器复算的数字变成能复算的"，或**证明它根本不该对齐**。
> 两条都做完了，结论如下（证据可当场复算，命令见各条）。

### 规则数：67 —— 63 是**历史快照**，不是另一个口径
- **活口径 67**：两个独立来源一致 ——
  `tools/gate_engine.py::RULES`（67 个 `Rule` 对象）与 `data/_gate_rules.json`（67 条）。
  复算：`python -c "import sys;sys.path.insert(0,'tools');import gate_engine as g;print(len(g.RULES))"` → 67。
- **63 的出处已定位**：`_arch_v19_brief.md:92` —— "gate_engine 的 63 条规则本身是否正确？"
  那是 **v19 架构简报里的历史值**（引擎随后长到 67）。
- 处置：**文档口径统一为 67**；`_arch_v19_brief.md` **不改**（版本化简报是历史快照，
  改它等于篡改历史）。reconciler 对 rules 键以 `gate_engine.RULES` 实测为准。
- 663/665 复盘：658 当时"仓库根无 `_gate_rules.json`、gate_engine 未找到 RULES 注册表"
  是**搜索不完整**（文件在 `data/` 不在仓库根；`RULES` 是模块级 list 而非"注册表"）。
  **教训：找不到 ≠ 不存在；先换搜索口径再下"权威源不明"。**

### 节点数：178 vs 121 —— **量纲错误**，两者不是同一量
- **178 节点 / 1093 边**：`web/data/graph.json` 实测（reconciler 每次对账）。
- **121 的出处已定位**：`docs/migration_647.md:87` ——
  "拆分带入 **118** 个 core 文件；加 README/conftest/.gitignore 后 tracked = **121**"
  ⇒ 121 是 **647 拆分仓的 tracked 文件数**，与图节点**无关**。
- 该数字**不可复算于当前仓**（拆分仓 666 时点 tracked = 1242，已远离 121），
  所以它连"另一个时刻的文件数"都算不上当前口径 —— 是一条**跨批次串了行的数字**。
- 处置：`graph_nodes` 以 `graph.json` 为准（178），**121 不作任何口径**；
  本条从"待确认"改判为**已定位的量纲错误**（证据：唯一可复算出处 + 与节点指标无函数关系）。

## 不变式
- 任何"文档数字"若能被 git/fs 机器复算，必须进 baseline.json 并由 reconciler 对账；
- **666 A6 追加**：口径差的收敛标准不是"两边改成一样"，而是**先定位权威源**——
  定位不到时只有三种结论：① 历史快照（改文档口径、留历史）② 量纲错误（作废该数字）
  ③ 真的冲突（才需要人裁决）。**禁止**为了"对齐"把不可复算的数字改成另一个不可复算的数字。
