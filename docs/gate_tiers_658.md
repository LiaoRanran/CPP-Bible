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

---

## 666 批补：两层各自的**可执行口径**（B 段落地版）

> 666 的活是把上表的"是什么"落到"**跑什么命令、阻断谁、看哪个数字**"。

### L0 REDLINE —— 跑法 / 阻断 / 现场

| 门禁 | 命令（主仓） | 阻断谁 | 失败时的现场 |
|---|---|---|---|
| integrity | `python tools/tool_integrity.py --check` | 发布 + CI 合并 | `tools/.tool_checksums` + `data/supply_chain/merkle_roots.json` |
| correctness | `python tools/run_656_gate.py --check` | 同上 | `data/656_*` 报告 |
| provenance | `python tools/atom_evidence_replay.py --check` | 同上 | `data/evidence_store/`（内容寻址） |
| replayability | `pytest -n0 -q tests/test_ledger_* tests/test_*replay*` | 同上 | 逐条复算命令在测试里 |
| state consistency | `python tools/status_reconciler_658.py --check` | 同上 | `data/baseline.json`（口径见 `caliber_convergence_658.md`） |
| known critical defect | `python tools/holdout_reveal_*` + `poison_drill` | 同上 | `data/holdout_reveal_*.json` |
| dco | `python tools/dco_check_657.py --check` | 同上 | 提交者纪律 |

**L0 的判定标准**：失败 = **不许发布**，且**不许**用"改断言/改阈值/加 ignore"绕过；
绕过必须走 ADR 并人签（见 `docs/adr/`）。

### L1 ADVISORY —— 跑法 / 谁看 / 升级路径

| 维度 | 命令 | 现场 | 升级为 L0 的条件（须人签） |
|---|---|---|---|
| mutation score | `python tools/mutation_fuzz.py --report` | core 97.3% / all 81.5%（666 时点） | **永不**（内部指标，最多进威胁清单） |
| 双档编译证据 | `python tools/compiler_probe_645.py` | 28 卡 / 147 次编译 / 28 双编译器确认 | 出现与卡面断言矛盾的实测 ⇒ 升级 |
| sanitizer 分层 | `python tools/external_corpus_reveal_665.py` | A 54.2% / B 12.5% / C 0%（全 unknown） | C 层出现"有仪表却全 miss" ⇒ 升级 |
| 前端质量 | `python tools/web_*` + 手工检查 | 见 `docs/666_frontend.md` | 无障碍/性能**实测**不达标且影响可用性 ⇒ 升级 |
| 文档一致性 | `python tools/docstring_quality_646.py` / `chapter_lint.py` | 报告 | 影响可复算入口的文档错误 ⇒ 升级 |

**L1 的判定标准**：只出**报告**，CI `continue-on-error: true`；但**报告缺失必须在验收报告里显形**
（"没跑"≠"没问题"，见 `docs/discipline/error_handling.md` §1）。

### 665/666 的两条经验（写进本层的理由）

1. **"低分"要在 L1 里先怀疑配置**：666 A5 的 5 个 miss 里 3 个换 `-O0` 就被抓 ——
   若当时把检出率当 L0 闸门，就会得出"验证器不行"的错误结论。
2. **口径变更必须在 L0/L1 边界上说清**：66.7% → 81.2% 是**口径变更**，不是能力提升；
   升级/降级判据都要写"换口径"这一行（见 `docs/discipline/release.md` §5）。
