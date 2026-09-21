# replay 报告 · 验证独立性等级（618 B4）

> 独立报告工具，不改 atom_evidence_replay.py；replay 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。

## 一、replay 统计（冻结基线）

- confirm（一致）：**56**
- refute（反驳）：**0**
- infra_error（基础设施错误）：**0**
- refute=0：atom↔evidence 重放零反驳，未观测逃逸（声称零逃逸 regime，见 617 A1 escaped 类型）。

## 二、验证独立性等级（617 B1）

- 离散等级：**L1**
- 连续性 scalar：**0.1532**
- 注解：verifier=1 ⇒ 基础在 Level 0；当前离散=1（第二实现存在，缺外部接口/第三方）；scalar 受 verifier 独立性=0 硬上限约束。

## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）

- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。replay 工件受 checksum 保护，但 external_verifiable=False（重放凭证未作为可第三方验证接口暴露）。
- **L2→L3 缺口**：需第三方审查 + 信任根真锚定；当前均为 False（partially_anchored）。
- **根因**：单一验证主体（verifier=1），scalar 受 0.2 硬上限 ⇒ 实测 0.1532。
- **升级路径（交人项 616 #9）**：重放凭证经 VSA/透明日志暴露给独立第三方重放 ⇒ 达 L2/L3。

## 四、对逃逸率口径的影响（呼应 617 A1 estimand）

- replay refute=0 即“声称零逃逸”，其 L2b 由 618 A3 的 e-process mixture 给出（≈0.6488%% 任何时刻上界），而非简单宣布 0；L3 外推（≈4.235%%）当前不成立（独立性 L1）。
