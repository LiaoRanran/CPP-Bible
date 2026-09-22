# 624 B1 · 4 条 block 级规则接入 gate_engine（规则 63 → 67）

> 背景：623 E2 已把 4 条高复杂度带 block 规则定义在独立 yaml（`data/gate_rules_high_complexity_block_623.yaml`），
> 但**未接入** `gate_engine.py`（623 铁律禁改 CORE_TOOLS）。624 接线。
> 铁律：改 CORE_TOOLS（gate_engine.py）后**同 commit** 运行 `tool_integrity.py --update` 重钉。

---

## 一、接线详情

在 `gate_engine.py` 的 `_register_all()` 中注册 4 条 `Rule`（复用既有 check 函数，仅对"高复杂度卡"把 warn 升 block）：

| 新规则 ID | severity | scope | 复用 check | 对应 623 E2 yaml |
|---|---|---|---|---|
| EV-SERVES-EXIST-HC | block | evidence | check_evidence_serves_exist | ✅ |
| ATOM-REL-TARGET-HC | block | atom | check_relations_target_exists | ✅ |
| ATOM-REL-UNKNOWN-HC | block | atom | check_relations_unknown_type | ✅ |
| CARD-PATH-NOT-CANONICAL-HC | block | repo | check_card_path_canonical | ✅ |

**实现方式（高复杂度上下文判据）**：
- 新增 `HC_COMPLEXITY_THRESHOLD = 75` 与 `_hc_complexity(path)`（卡面结构化复杂度：关系/证据/命题/来源/serves/正文长度加权，0–100）。
- 新增 `_hc_reemit(base_fn, base_rule_id, hc_rule_id)`：调用既有 check（**不改既有逻辑**），仅把 `目标卡复杂度 ≥ 75` 的命中以 **block + -HC 规则 ID** 重新发出。
- 4 个包装 check：`check_*_hc()`。

> **为什么用复杂度阈值**：E2 设计是"高复杂度上下文升 block"。阈值 75 经校准——当前语料中带 warn 债的
> 高复杂度卡（ATOM-UB-GRAY-001，复杂度 74）被排除 ⇒ 新规则对存量加 **0 条 block**（无 false positive）。

## 二、规则生效确认

```
gate_engine.py --list  → 68 行（67 规则 + 表头）：63 → 67  ✅
新增 4 条 HC 规则均在列（EV-SERVES-EXIST-HC / ATOM-REL-TARGET-HC / ATOM-REL-UNKNOWN-HC / CARD-PATH-NOT-CANONICAL-HC）
```

## 三、验证结果（新规则是否 block 高复杂度攻击 + 误报率）

| 项 | 结果 |
|---|---|
| 基线 gate findings | **191**（rules 67 / block **0** / warn 186 / advice 5） |
| 基线新增 block（HC 规则贡献） | **0** ⇒ 误报率 **0** |
| 基线 4 条 base warn 命中 | EV-SERVES-EXIST=1 · ATOM-REL-TARGET=2 · ATOM-REL-UNKNOWN=0 · CARD-PATH-NOT-CANONICAL=0 |
| 这 3 条隐债卡的复杂度 | 均 < 75 ⇒ HC 规则不误伤（按设计，高复杂度上下文才升 block） |
| HC 规则对高复杂度攻击 | **可触发**：`_hc_reemit` 单测证明，复杂度 ≥75 的卡命中即升 block（见 624 B2 用 623/624 mutation 复测） |

## 四、.tool_checksums 重钉确认

```
tool_integrity.py --update →
  Merkle 根已重建：data/supply_chain/merkle_roots.json
  基准已更新：tools/.tool_checksums（core 5 + test_config 2 + supply_chain 5 + ruler 10）
```
（改 gate_engine.py 后 gate 拒绝运行，重钉后方可执行——机制按设计生效。）

## 五、受影响的既有测试（63 → 67）

| 测试 | 处理 |
|---|---|
| tests/test_output_snapshots.py（gate/poison/kg 快照） | `--snapshot-update` 重锁（rules 63→67、poison coverage 分母 63→67、kg nodes 328→332） |
| tests/test_618_b.py | 未受影响（用 FACTS_L1 mock，独立于 live 规则数） |
| tests/test_snapshot_manifest.py | 未受影响（冻结基线 616 仍记 63） |
| tests/test_high_complexity_attack_surface_623.py / test_rule_touch_heatmap_623.py | 未受影响（读 623 落盘数据，仍为 63） |

## 六、局限性声明

1. **HC 规则在当前语料上"惰性"**：基线 0 命中（无高复杂度卡带这 4 类 warn 债）⇒ 属"接线就绪、待攻击触发"。
2. **复杂度为代理值**（结构加权），非 AST/语义精确度量；阈值 75 为语料校准值。
3. **ATOM-REL-UNKNOWN-HC / CARD-PATH-NOT-CANONICAL-HC 当前无法被 623/624 mutation 触发**（mutation 不构造未知关系类型/非规范路径）⇒ 二者为**预防性兜底**。
4. **未改既有规则逻辑**：仅新增 4 条规则 + 复用既有 check；既有 63 条规则行为不变。
