# 629 E1 · push 裁决材料（**不执行 push**，交人裁决）

> 生成：2026-09-23 · 工具：`git log`（只读）· 结论：**建议推送，但先接受 pytest job 必红的现实**
> **本文件只整理清单与风险，不执行任何 push**（§零.2）。

## 一、push 清单（本地领先远程 **85 commit**）

| 批次 | commit 数 | 主题 | 备注 |
|---|---|---|---|
| 625 | 16 | mypy 67→0 / OTS re-anchor / 雷2 稳定 / 路径解耦 / 尺子 22→34 | 已在本机验收（run_625_gate PASS） |
| 626 | 16 | Authority 语义收口（DecisionEvent v2 / 唯一审查账本 / 投影编译 / PCK 四层） | 15 工具 + 143 例单测 |
| 627 | 12 | 固本批（W2 归一化 519→121 / supersedes 重映射 / V2 端到端 / Blind Review 工具链） | run_627_gate PASS |
| 628 | 18 | 修债 + 他验三件套原型 + 人审仪表盘 v2 + 镜像门监控 | run_628_gate PASS |
| 629 | 23 | 自身免疫率 × 验证器攻击面 × 他验深化 × 闭环第八轮 | **run_629_gate PASS** |

远程 HEAD：`793b5c45`（624）；本地 HEAD：`c1d88d77`（629 F 线收工后）。

## 二、CI 风险评估（逐 job）

| job | 预期结果 | 风险 | 依据 |
|---|---|---|---|
| `replay` | ✅ 绿 | 低 | 629 全程未改受控目录（D2 沙箱跑批后 `git status -- atoms evidence` 为空）；manifest 无需 rebuild |
| `concurrency-safety` | ✅ 绿 | 低 | 未改 ci.yml 与并发相关工具 |
| `gate`（needs replay） | ⚠️ 未知 | 中 | gate 属**监工域**，629 本地禁跑（§零.1）；628 收工时监工跑过 67/191/block=0。629 未改原子/证据 ⇒ 推断不劣化，但**未经本地验证** |
| `quality`（needs replay） | ⚠️ 中风险 | 中 | 本地 `ruff tools/ tests/` 全绿、`mypy tools/` 0 errors ✅；但该 job 还有约 35 步历史治理/metrics/清单类检查，**629 未逐项本地复现**（823 基线冻结口径不变） |
| `pytest` | ❌ **必红** | 高 | 629 任务0 实测：`pytest -m "not slow"` 有 **19 项既有失败**（状态快照型断言被 628 的 A2/A3 数据处置打破）；另 `-m slow` 段未测 |
| `compile`/`publish-check`（needs quality,pytest,replay,gate） | 预计 **skipped** | — | 依赖 job 红 ⇒ 下游不跑 |
| `site`/`pdf`/`epub`/`deploy` | 预计 **skipped** | — | 依赖链同上 |

**关键结论**：push 后 CI **不会全绿**，但红因**不是 629 引入**——19 项失败在 629 开工前就存在
（`data/629_baseline.md` §六 已冻结清单）。这一点必须在推送说明里写明，否则会被误读为 629 回归。

## 三、建议策略（三条，供人裁决）

1. **方案 A（推荐）：一次性 push 全部 85 commit**，随 push 附一句说明「pytest 仍红为
   **11 项他批既有失败**（628 数据处置使 627 断言过期 5 / 本地未跟踪 `_arch_v2x/` 4（CI 检出无此文件）/
   625 阈值 1 / 611 快照 1），非 629 引入，清单见 629 基线台账 §六」。理由：628/629 的地基是
   626/627（DecisionEvent v2、投影编译），**区间不可拆分**（拆开推会让中间态 CI 更红）；
   且区间 push 的价值主要是「定位红因」，而红因已提前定位。
2. **方案 B：先推 625-627（44 commit），观察 CI，再推 628-629（33 commit）**。理由：能验证
   「625-627 段是否引入 quality/gate 红」。代价：两轮 CI、中间态 CI 红（628 的数据处置尚未推）。
3. **方案 C：先修 19 项过期断言再推**。理由：让 pytest job 绿。代价：那 19 项属
   **他批资产**（625/627/624 的测试），修它们需要确认「原断言意图 vs 现状」，
   **越权风险高**（629 无权改他批判决口径）⇒ 建议**交人决定**（见 E3 第 12 项）。

**机器不代做**：push 动作、CI 红因的最终判定、19 项测试的处置口径。

## 四、push 前自查（本批已做）

- 受控目录零污染：`git status -- atoms evidence Examples Book` = 空 ✅
- 新增工具 `--check` 全绿（F1 门禁覆盖）✅
- ruff 整目录 + mypy tools/ 全绿 ✅
- 密钥/私钥零落盘（C1 全仓扫描 `[]`）✅
- 未 push、未 golden accept、未开 delegation、未代签 ✅
