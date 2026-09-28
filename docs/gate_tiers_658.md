# 658 B 段 · 门禁两层模型（L0 REDLINE / L1 ADVISORY）

> 配置：`tools/gate_tiers_658.json`（声明式）。本文件是架构说明。

## 设计动机

之前所有门禁混在一个红绿判定里，导致两个失真：

1. **把"测试充分度"当成了"正确性"**——变异得分 97% 被误读成"书几乎没错了"。
   实际上 97% 是对**自造变异分布**的漏检率，和外部世界真实错误率不是一回事（见 A5 / F）。
2. **把"建议"和"红线"混在一起**——clang-tidy 的一条建议和一个哈希校验失败有同样的阻断力，
   结果要么门禁噪到没人看，要么被悄悄关掉（"狼来了"）。

两层模型把"必须过"和"记录下来看"分开。

## B1 L0 REDLINE（不通过 = BLOCK）

| 门禁 | 工具 | 为什么是红线 |
|---|---|---|
| integrity | `tool_integrity.py` | 信任根：文件完整性 + Merkle 根 |
| correctness | `run_656_gate` 阶段 1-2 | 判决依赖的结构/符号/账本必须自洽 |
| provenance | `atom_evidence_replay.py` | 每条证据可溯源到 OTS 锚 |
| replayability | 证据 replay | 别人能重跑出同样结论 |
| state_consistency | `status_reconciler_658.py --check` | 文档状态 == git 实际状态（D 段） |
| known_critical_defect | A 段夹具 + holdout | 已知关键缺陷必须被抓 |
| dco | `dco_check_657.py` | 提交者纪律（658 E2 从报告态转硬） |

## B2 L1 ADVISORY（只出报告，不阻断）

mutation score（97.3%/81.5%）、asm coverage（203/513）、prose density、completeness、
performance、teaching quality、AddressSanitizer/UBSan、clang-tidy、AArch64+qemu-user 交叉编译、
内存序类测试。**全都不阻断 CI。**

## B3 架构

- advisory 层输出**报告**（不是红绿）。
- 引擎读 advisory 报告 → 决定是否把某个维度**升级为 L0 问题**（走 Authority Ledger 裁定，不擅自）。
- 这和"让引擎自己复现边界行为"是同一件事：引擎可以**诊断**、可以**提出**进化方案，
  但语义能力升级必须经过**独立验收边界**（658 宪法原则）。

## 不变式

- L1 在 CI 必须 `continue-on-error: true`，绝不阻断合并。
- mutation score 是 Test adequacy，禁止据此宣称外部效度。
- 升级 L1→L0 须经 Authority Ledger，不能工具自说自话。
