# 验证独立性 4 级（617 B1）

> 背景（外部评审 #2 / #5）：当前验证者数量 = **1**（`gate_engine.py`），生成者 = 判断者 = 同一主体，独立票结构性缺失。须定义独立性分级，量化当前等级与缺口，为 A1 的 L3 外推 shrinkage 提供 `independence_level` 依据。
> 工具：`tools/verify_independence_level.py`（按事实计算离散等级 0–3 与连续 scalar）。

## 一、四级定义
| 等级 | 名称 | 含义 | 关键判据 |
|---|---|---|---|
| **Level 0** | 自证 self-attestation | 生成者自证，无独立票 | verifier_count = 1（基础在此级）|
| **Level 1** | 内部第二实现 internal cross-check | 项目内独立第二实现 ≥1 规则 | second_implementation_rules > 0 |
| **Level 2** | 外部可验证 externally verifiable | checksum + 独立验证接口（VSA 凭证 / 透明日志），外人不依赖项目即可验证 | checksum_protected AND external_verifiable_interface |
| **Level 3** | 独立第三方 independent third-party | 独立于项目的验证者 + 透明日志 + 第三方复核 + 信任根锚定（OTS 真上链 / in-toto 真签名）| Level 2 AND third_party_review AND trust_root_anchored |

## 二、当前判定（取自 616 D 他验基线）
- verifier_count = **1** ⇒ 基础在 **Level 0**。
- second_implementation = **1/63**（仅 `ev_matrix_unbacked_v2`）⇒ **Level 1 部分达到**。
- checksum_protected = **22 项**（core5+test_config2+supply_chain5+ruler10）⇒ 满足。
- external_verifiable_interface = **False**（无 VSA 凭证 / 无透明日志）⇒ **Level 2 未达**。
- third_party_review = **False**、trust_root_anchored = **False**（OTS pending、in-toto `hmac` 非标准）⇒ **Level 3 未达**。

**结论**：
- 离散等级 = **1**（第二实现存在，但 verifier 仍为 1、无外部可验证接口、无第三方）。
- 连续 scalar（L3 shrinkage 用）≈ **0.153**（verifier 独立性 = 0 为硬上限，仅内部缓解 + checksum 积分；封顶 0.2）。

## 三、治理结论
1. A1 的 L3 外推必须以独立性为支撑；当前 scalar 低 ⇒ 部署逃逸率**不能**用 L1/L2 直接外推，须 shrinkage 向先验 0.05。
2. 提升路径：
   - 到 Level 2：加 VSA 凭证 / 透明日志接口（他验架构阶段 2）。
   - 到 Level 3：引入独立第三方验证者 + 信任根真锚（OTS 真上链 / in-toto 真签名）。
3. 本等级为**客观事实判定**，不代签任何裁决；是否投入 Level 2/3 见交人项（616 #9）。
