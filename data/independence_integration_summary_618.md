# 独立性等级接入汇总（618 B4 · 收尾 doc）

> 三份报告（gate/poison/replay）均由独立报告工具生成（不改受控工具），调用 617 B1 `verify_independence_level.compute_level`（只读事实）。
> 所有独立性数字取自 `data/SNAPSHOT_MANIFEST_617.json`（冻结基线）。

## 一、三份报告的独立性等级汇总
| 报告 | gate | poison | replay |
|---|---|---|---|
| 离散等级 | **L1** | **L1** | **L1** |
| 连续性 scalar | 0.1532 | 0.1532 | 0.1532 |
| 数字源 | manifest.gate（63/191, block0/warn186/advice5）| manifest.poison（124/124, 63/63, 60/63）| manifest.replay（56/0/0）|
| 独立性结论 | 同左 | 同左 | 同左 |

三份报告的一致性：独立性等级由**同一个验证主体事实**决定（verifier=1），与具体门禁无关 —— 这正是"独立性是系统级属性，不是单门禁属性"的体现。

## 二、当前 L1 的完整定义与限制
- **定义（617 B1）**：离散 L1 = 存在内部第二实现（second_implementation_rules>0）但缺外部可验证接口 / 第三方审查。
  - 当前：第二实现 1/63（ev_matrix 双实现锁），checksum 保护 22/22，但 `external_verifiable_interface=False`、`third_party_review=False`、`trust_root_anchored=False`。
- **连续 scalar = 0.1532**：加权合成，受 `verifier_independence=0`（verifier_count=1）硬上限 0.2 约束。
- **限制**：
  1. 所有"验证正确性"声明仅代表**自证/内证**，不能宣称独立第三方背书。
  2. 逃逸率 L2 任何时刻上界取置信序列 CS=0.9062%（A1），**不能**用更松的 L3 外推（≈4.25%）对外。
  3. 信任根仅 partially_anchored（OTS 未真上链 / in-toto 真签名未做）。

## 三、升级到 L2 的前提条件
- `checksum_protected=True`（已满足：22 项尺子已钉）+ `external_verifiable_interface=True`（**待做**）。
- **待做项**：将 616 D 的 VSA 凭证 / 透明日志原型接线为**生产级可验证接口**（attestation 可作为第三方输入重放/复算）；公开见证端点。
- 完成后离散等级 ⇒ L2，scalar 上限放开（仍受 verifier=1 约束，但 external_verifiable 权重 0.1 计入）。

## 四、升级到 L3 的前提条件
- 在 L2 基础上需 `third_party_review=True` + `trust_root_anchored=True`（**均待做**）。
- **待做项**：① 引入独立第三方审查（多主体 verifier_count>1，打破 verifier=1 硬上限）；② OTS 真上链 / in-toto 真签名（信任根从 partially_anchored ⇒ anchored）。
- 完成后离散等级 ⇒ L3，scalar 可达 ≥0.5，逃逸率方可做 L3 部署外推（呼应 617 A1 estimand 第三层）。

## 五、交人项（616 #9 继承）
- 是否投入 L2/L3 工程（接线 VSA/透明日志、引入第三方、OTS 上链）属人审裁决，本批不代签、不实施。
- 本批仅把"独立性等级"显式接入三份报告，使缺口**可量化、可复算**，为后续升级提供基线。
