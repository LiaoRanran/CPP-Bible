# G3.3 质量度量 M5（北极星指标 + 三级 DoD）

> 工具：`tools/m5_dashboard.py`（聚合**既有事实源**，不重复实现口径；命名避开 `tools/legacy/quality_dashboard.py`）
> 阈值校准：**先标 golden 再反推**——G4 三样板达标后取其得分作基线；改口径必须过黄金锁（S4 `--accept` 留痕）

## 1. 北极星指标（口径与当前值，2026-09-10 实测）

| 指标 | 口径 | 当前值 | 来源 |
|---|---|---|---|
| 证据完备度（原子） | `evidence[]` 非空的原子占比 | n/a（原子库空，G4 锻造后起算） | atoms/ |
| 一手实证覆盖（原子） | `first_hand: true` 占比 | n/a | atoms/ |
| 原创占比（原子） | `superiority` 非空且不含禁词占比 | n/a | atoms/ + M3 §4 禁词 |
| 教学达标（原子） | `pedagogy` 四字段齐占比 | n/a | atoms/ |
| **纵深锚定率（Book）** | ASM 符号锚定 / 总锚定对象 | **203/512 = 39.6%** | `metrics.json:asm` |
| **Book 验证标记** | `[VERIFIED]` / `[UNVERIFIED]` | **165 / 298**（存量债按 DRQ-4 单列） | `metrics.json:verification` |
| 冲突清零 | `contradicts` 未仲裁边数 | **0** | atoms/ 关系 |
| 活体漂移 | 黄金锁恶化数 | **0** | `golden_state.json` |
| 规则命中 | gate_engine block/warn | **block=0 · warn=1**（EV-SERVES-EXIST，G4 后清零） | `gate_engine --run` |
| 债务负债率 | 票据数 / 质量门禁项数 | **1/23 = 5%**（合规 ≤15%） | `debt_ledger.json` |

口径纪律：**任何"当前值"必须能被 `quality_dashboard.py` 现场复算**；引用数字必须注明来源事实源。

## 2. 三级 DoD

| 级 | 定义 | 判定（当前） |
|---|---|---|
| **原子级** | 五剖面全绿：多源 ≥1（①）· 证据非空 + 一手实证（②）· superiority 非空非禁词（③）· `depth.layer` 标注（④）· 教学 4 字段（⑤） | 0/0（G4 锻造后起算） |
| **章级** | 该章全部原子达原子级 DoD + 章门禁全绿 | 0/147（**G5 绞杀者迁移逐步达成**） |
| **全书级** | 全部章级 + 冲突清零 + 黄金锁零恶化 + 负债率合规 | 未达成（依赖章级） |

## 3. 仪表盘与留痕

- `python tools/quality_dashboard.py [--json build/dashboard.json]`——JSON 落盘进 CI artifact，即 S6 的黑匣子留痕之一。
- 指标只增不删：新增指标必须写明口径与来源事实源；**删除指标 = 改口径**，须过 S4 黄金锁并写理由。
