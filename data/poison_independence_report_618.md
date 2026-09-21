# poison 报告 · 验证独立性等级（618 B3）

> 独立报告工具，不改 poison_drill.py；poison 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。

## 一、poison 统计（冻结基线）

- 触发/总数：**124 / 124**（通过率 100%）
- 覆盖率：表观 **63/63** · 诚实 **60/63**（诚实口径剔除 machine-untriggerable 3 条）
- 诚实覆盖率 = 60/63 = 95.2%%，如实反映 3 条机器不可触发规则不计覆盖。

## 二、验证独立性等级（617 B1）

- 离散等级：**L1**
- 连续性 scalar：**0.1532**
- 注解：verifier=1 ⇒ 基础在 Level 0；当前离散=1（第二实现存在，缺外部接口/第三方）；scalar 受 verifier 独立性=0 硬上限约束。

## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）

- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。poison_drill 工具在 checksum 保护集内（22 项），但 external_verifiable=False。
- **L2→L3 缺口**：需第三方审查 + 信任根真锚定；当前均为 False（partially_anchored）。
- **根因**：单一验证主体（verifier=1），scalar 受 0.2 硬上限 ⇒ 实测 0.1532；poison 覆盖率诚实口径的"可信度"受独立性 L1 限制，不能宣称独立第三方背书。
- **升级路径（交人项 616 #9）**：接线 VSA 凭证/透明日志 + 独立第三方重跑 poison ⇒ 达 L2/L3。

## 四、对逃逸率口径的影响（呼应 617 A1 estimand）

- poison 覆盖率诚实 95.2%% 是样本内描述（L1）；若做 L3 部署外推，需叠加独立性 scalar 收缩（≈4.25%% 量级），当前不成立。
