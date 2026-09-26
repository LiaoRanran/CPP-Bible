# 645 开工基线（阶段 0.1）

> 自动生成于 2026-09-26 执行 `inbox/645.md` 之前。所有数字均来自真实仓库状态，非估算。
> 本文件为 645 轮次的开工快照，用于对比收工时的增量。

## 一、版本与提交

| 项 | 值 | 来源 |
|---|---|---|
| HEAD | `0c99920f` | `git rev-parse --short HEAD` |
| ahead（相对 origin/master） | `80` | `git rev-list --count origin/master..HEAD` |
| git_status | 本地未 push（符合铁律：本轮不 push） | `git status` |
| 643/644 状态 | 均收工（outbox 已写），但均**未 push** | `status/643_acceptance_report.md` `status/644_acceptance_report.md` |

## 二、工程量

| 项 | 值 | 计算方式 |
|---|---|---|
| 工具总数（tools/*.py） | `493` | `dir tools\*.py` |
| 测试文件（tests/test_*.py） | 见 pytest（643/644 新测试 59 个含 64x 前缀） | `dir tests\test_*.py` |
| 规则数（gate_engine.RULES） | `67` | `len(ge.RULES)` |
| 原子卡（atoms/**/ATOM-*.md） | `27` | `dir /s ATOM-*.md` |
| 现有证据卡（evidence/**/EV-*.md） | `56` | `dir /s EV-*.md` |
| 内容寻址证据库（data/evidence_store） | `1` 条（真实 g++ L1 实测） | `dir /s` 64 位 hash 文件 |
| Authority 判决账本 | `452` 条（append-only 哈希链） | `data/authority/decision_event_v2_ledger.jsonl` 非空行 |

## 三、645 轮次前的关键指标（来自 STATE.json / 644 报告）

| 指标 | 值 | 口径 |
|---|---|---|
| 一致性门禁 | 100/100（147 章 ERROR=0 WARN=0） | `consistency_check.py` |
| 644 头部层证据库 | 1 条真实 L1（g++ 实测） | `data/evidence_store/` |
| 644 证据索引 | 58 条卡-证据关联 | `data/evidence_index.json` |
| 643 智能层 | 19 工具（18 个 643 + 门禁），144 测试 | `status/643_acceptance_report.md` |
| 644 头部层 | 20 工具（19 + 门禁），88 测试 | `status/644_acceptance_report.md` |
| R5 校准度（643 E3） | `0.1`（10%，未达 60% 门槛） | `data/642_loop_calibration.json` 口径 |

## 四、环境（真实探测）

| 项 | 值 |
|---|---|
| Python | 3.14.5 |
| g++ | `C:\Qt\Tools\mingw1310_64\bin\g++.exe`（GCC 13.1）；另有 `mingw1530_64`（GCC 15.3） |
| clang++ | `C:\msys64\mingw64\bin\clang++.exe`（存在 ⇒ B3 双编译器**可行**） |
| 网络 | 待 B1 实测（eel.is/cppreference 可能受限，按诚实降级） |

## 五、本轮目标（对照 645 §十一）

- 阶段 A：智能层补强（问题发现/攻击/提案/闭环/错误追踪/老化/整合）
- 阶段 B：头部层补强（标准获取/编译器实测/双编译器/反例/分级/充分性/整合）
- 阶段 C：三层耦合（数据模型/编排/评估/反馈）
- 阶段 D：接口统一（审计/规范/迁移）
- 阶段 E：性能（pytest 两阶段/工具提速/证据检索）
- 阶段 F：优雅代码（注释/去冗余/风格）
- 阶段 G：收工（门禁/两阶段终验/验收报告+status+outbox）

## 六、铁律确认

1. 不 push（ahead 保持或增加，收工后统一 push 留交人）。
2. 5 个 CORE_TOOLS 判决逻辑零改动。
3. 受控目录（atoms/evidence/Examples/Book）零污染。
4. 不代签人审、不 golden accept。
5. 建设优先，A/B 阶段建实，不用代理实现/优雅降级糊弄。
6. 每个工具 `--check` 只读幂等、单测覆盖。
7. 做不到的诚实登记，不编造、不"改到绿"。
8. 全程中文。
9. 注释充分（模块/类/关键函数 docstring + 行内注释）。
