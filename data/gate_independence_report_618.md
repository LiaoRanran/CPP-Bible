# gate 报告 · 验证独立性等级（618 B2）

> 独立报告工具，不改 gate_engine.py；gate 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。

## 一、gate 统计（冻结基线）

- 规则数：**63**
- 命中数：**191**（block=0 / warn=186 / advice=5）
- block=0：当前 63 条规则零 block 命中（含学习者镜像门 closed 等），非真逃逸。

## 二、验证独立性等级（617 B1）

- 离散等级：**L1**
- 连续性 scalar：**0.1532**
- 因子：verifier_independence=0.0, second_implementation=0.0159, checksum=1.0, external_verifiable=0.0, third_party=0.0
- 注解：verifier=1 ⇒ 基础在 Level 0；当前离散=1（第二实现存在，缺外部接口/第三方）；scalar 受 verifier 独立性=0 硬上限约束。

## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）

- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。当前 checksum=True 但 external_verifiable=False（无 VSA 凭证/透明日志生产接口；616 D 原型未接线）。
- **L2→L3 缺口**：需 `third_party_review=True` 且 `trust_root_anchored=True`。当前第三方审查=False、信任根未真锚定（OTS 未真上链 / in-toto 真签名未做 ⇒ partially_anchored）。
- **根因**：verifier_count=1（单一验证主体），独立性基础在 Level 0；第二实现（1/63）仅内部缓解，scalar 受 0.2 硬上限约束 ⇒ 实测 0.1532。
- **升级路径（交人项 616 #9）**：① 接线 VSA 凭证/透明日志 ⇒ 达 L2；② 引入独立第三方审查 + OTS 真上链/in-toto 真签名 ⇒ 达 L3。

## 四、对逃逸率口径的影响（呼应 617 A1 estimand）

- 因独立性=L1，blocked 类型的 L2 任何时刻上界取置信序列 CS=0.9062%%（A1），而非更松的 L3 外推；L3（≈4.25%%）仅在显式标注"部署外推、独立性支撑"时使用，当前不成立。
