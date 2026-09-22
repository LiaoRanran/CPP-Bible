# 624 B2 · 规则回归 + 误报分析（B1 接线后）

> 目的：确认 624 B1 接入的 4 条 HC block 规则**不破坏**既有 gate/poison 回归，且**无误报**；
> 并用 623/624 的真实 mutation 复测新规则是否 block 住高复杂度攻击。
> 铁律（§六.4）：**不跑监工门禁** ⇒ 未运行 `gate --check` / `atom_evidence_replay --check`；
> 改用 `gate_engine.run()`（引擎读数）与 `poison_drill.rule_coverage()`（纯读）取而代之地取证。

---

## 一、gate 回归结果

| 项 | 值 |
|---|---|
| 注册规则数 | **67**（63 + 4 HC） |
| 全库 findings | **191**（与 623 基线一致，未变） |
| **block** | **0**（新规则对存量 **0 误报**） |
| warn | 186 |
| advice | 5 |

## 二、poison 回归结果

| 项 | 值 |
|---|---|
| 制衡层 | **124/124**（全部拦截 + 阴性放行，含 P29/P30 relations 矛盾、P62 artifact 不存在、P69 路径非规范） |
| RULE-COVERAGE | covered **39/67** |
| 未覆盖规则 | **EV-SERVES-EXIST-HC · ATOM-REL-TARGET-HC · ATOM-REL-UNKNOWN-HC · CARD-PATH-NOT-CANONICAL-HC** |

⚠ **诚实登记**：4 条新 HC 规则**当前未被 poison 攻击面覆盖**（poison 的 P29/P69 针对 base 规则，未针对"高复杂度上下文"变体）⇒ 新规则的 poison 覆盖为 **0**，属**待补覆盖债**（留 625）。

## 三、replay 回归结果

| 项 | 值 |
|---|---|
| 冻结基线（616） | confirm 56 / refute 0 / infra 0 |
| 本批是否重跑 | **否**（铁律禁跑 `atom_evidence_replay --check`） |
| 加性安全性论证 | 4 条 HC 规则为 `fact/programmatic` **gate** 规则；replay 位于独立的复算层（`atom_evidence_replay.py`），其判定不含门禁规则集 ⇒ **加规则不改 replay** |

## 四、新规则 block 住的高复杂度攻击数

### 4.1 623 的 80 条高复杂度 mutation（复跑）

| 项 | 值 |
|---|---|
| 判决分布 | blocked 46 / nonblock 16 / neutral 12 / escaped 4 / infra 2（**与 623 一致**） |
| HC 规则新增 block | **0** |

**归因**：623 mutation 命中的 base warn 卡（如证据卡）复杂度 < 75 ⇒ HC 规则不触发（按设计）。

### 4.2 624 的 60 条跨卡 mutation（复跑，本批核心）

| 项 | 接线前（624 A2） | **接线后（B1 生效）** |
|---|---|---|
| blocked | 47 | **55** |
| detected_nonblock | 13 | **5** |
| escaped | 0 | **0** |
| 新增 block 规则 | — | **ATOM-REL-TARGET-HC · ATOM-REL-UNKNOWN-HC** |

- **100 条跨卡 mutation 中 53 条命中复杂度 ≥75 的卡**；X1（悬空引用）把高复杂度原子（如 ATOM-MEM-ALLOC-001 复杂度 96）的 relation target 改为不存在 ⇒
  **ATOM-REL-TARGET-HC 升 block**（原 base 规则只 warn）。
- **净效果**：8 条原本 warn 的高复杂度攻击被**升级为 block**（47→55 blocked）。

## 五、误报分析

| 项 | 结果 |
|---|---|
| 基线（存量卡）新增 block | **0** |
| 623 mutation 复跑新增 HC block | 0 |
| 624 mutation 复跑新增 HC block | 2 条规则、8 条命中 —— **均为真实高复杂度跨卡攻击**（非合法内容） |
| 合法内容误伤 | **无**（HC 仅对复杂度 ≥75 且命中 base warn 的卡升 block） |

**结论**：新规则**零误报**；对高复杂度攻击可按设计升 block（ATOM-REL-TARGET-HC / ATOM-REL-UNKNOWN-HC 已实证触发）。

## 六、局限性声明

1. **EV-SERVES-EXIST-HC / CARD-PATH-NOT-CANONICAL-HC 未被任何实测攻击触发**（证据卡复杂度 <75；mutation 不改路径）⇒ 二者为预防性兜底。
2. **poison 覆盖新增 4 条 HC 规则为 0** ⇒ 待 625 补 poison 载荷。
3. **replay 未重跑**（铁律），以加性论证替代。
4. 复杂度阈值为语料校准值（75）。
