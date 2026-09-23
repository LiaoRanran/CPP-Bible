# 628 B4 · 他验端到端演示报告（独立验证 → VSA 凭证 → 透明日志）

- 运行时刻：2026-09-23T04:52:01Z
- 独立验证者：`independent_verifier_628`（脚本 sha256 `a85cad4faa914506…`）

## 一、链路步骤与结果

| 步骤 | 组件 | 结果 |
|---|---|---|
| 1 独立重算关键数字 | B1 独立验证者（零 import） | W2 {'IN': 114, 'OUT': 7, 'UNDEC': 0}／PCK authorized 27／ledger 链 valid（452 条）／unique 93 |
| 2 与系统 V2 投影对比 | 626 编译器（flag=1） | 系统 {'IN': 114, 'OUT': 7, 'UNDEC': 0} ↔ 独立 {'IN': 114, 'OUT': 7, 'UNDEC': 0} ⇒ 一致 |
| 3 生成 VSA 凭证 | B2（HMAC-SHA256） | `data\vsa\attestation_20260923T045200Z.json` |
| 4 追加透明日志 | B3（append-only） | index=24（entry_hash a83b206864f7b826…） |
| 5 日志完整性 | B3（线性哈希链） | 完整（25 条） |
| 6 凭证存在性 | B3（inclusion） | 在册 index=24 |
| 7 日志/凭证一致性 | B3（漂移检测） | 引用文件完整 True（25 条）· 未入册凭证 0 张 |

## 二、独立验证 vs 系统输出

| 项目 | 独立重算 | 系统口径 | 一致 |
|---|---|---|---|
| W2 IN/OUT/UNDEC | {'IN': 114, 'OUT': 7, 'UNDEC': 0} | {'IN': 114, 'OUT': 7, 'UNDEC': 0} | True |
| W2 逐节点 vs 冻结 label | 121 节点 | 121 节点 | True |
| PCK authorized | 27 | 27 | True |
| ledger 哈希链 | valid | 452 条 valid | True |
| unique 审查项 | 93 | 93 | True |

## 三、审计声明

> 在 2026-09-23T04:52:01Z，独立验证者 independent_verifier_628（脚本 sha256 a85cad4faa914506…）对输入 ledger=452 条 / PCK=83 张 / 节点 grounded_labels 独立重算得 W2 IN/OUT/UNDEC=114/7/0，与系统 V2 投影 IN/OUT/UNDEC=114/7/0 一致；凭证 data\vsa\attestation_20260923T045200Z.json 已存入透明日志 index=24（entry_hash=a83b206864f7b826…），日志链完整（25 条）。

## 四、他验意义

- 这是系统第一次有「**不依赖本项目代码**、可验证、可追溯的第三方复核闭环」：
  独立验证者零 import 本项目工具、纯标准库、朴素算法；凭证锚定输入哈希；
  日志 append-only 且任何历史改动都会断链。
- 与 v20 调研结论对应：独立复核 ✅ / VSA 验证凭证 ✅ / 透明日志 ✅（三件套全部落地**原型**）。
- **诚实局限**：① 验证者仍由本项目作者编写（缺真正的外部验证者）；
  ② VSA 用 HMAC 而非非对称签名（无独立密钥托管）；
  ③ 日志存本地、无外部见证者。三条都需后续批次（外部主体 / 密钥托管 / 公开 Rekor）。

- **总判定**：端到端全绿 ✅
