# Architecture Decision Records

## ADR-001: 章节结构标准 (2026-07-07)
**决策**: 采用 20 圈码标题 + ≥30 cpp 块 + 立场标签体系
**依据**: 确保每章结构一致、内容可度量、门禁可自动化
**状态**: 已实施（CONVENTIONS.md v3）

## ADR-002: 增量演进策略 (2026-07-09)
**决策**: 所有操作仅做新增，禁止覆盖已有文件、重命名、删除 _legacy_
**依据**: 保护已有工程成果，避免破坏性重构导致的回归
**状态**: 已实施

## ADR-003: 项目参照级 (2026-07-09)
**决策**: 以 LLVM/Chromium/Qt 为工程参照，建立 Governance + Memory + Automation 三层体系
**依据**: 大型知识工程需要与大型软件工程同等级别的治理基础设施
**状态**: 已实施（GOVERNANCE.md + memory/）

## ADR-004: 知识图谱驱动关联 (2026-07-09)
**决策**: 章节间耦合由 knowledge_graph.json 表达，而非硬编码链接
**依据**: 机器可读的图谱可被工具链消费，生成自动交叉引用、依赖分析、学习路径
**状态**: 已建立基础版本，待工具链消费

## ADR-005: 双轨记忆 (2026-07-09)
**决策**: workbuddy memory/ 存会话级日志，项目 memory/ 存 checkpoint + 架构决策
**依据**: 两者受众不同（Hy3+user vs 全体贡献者），不应混用
**状态**: 已实施

---

## ADR-006: 三权分立 + 真机取证（G4/G5，2026-09）
**决策**: Writer（提议）/ 独立红队（独立上下文判语义盲区）/ 人审（human:liaoranran 唯一 verified 与 5 分授予）三权分立；每个 claim 必须有真机/标准原文/≥2 独立源客观锚，断言只锚常量+活性对照（不锚时序/倍数/地址）。
**依据**: LLM 不能当裁判（Self-Correction Blind Spot / Circular Trust / correlated error，见 References/275）；项目多次实证模型会把正确答案改错、自证断言、被内联否证。
**状态**: 已实施（gate_engine 33 规则、poison_drill 8 毒样例、golden_lock）。

## ADR-007: 阙疑 EPOCHE 认识论 + 单一六态状态机（2026-09）
**决策**: 悬置判断；探究网络为唯一内核；冲突不否决、先进溯因。状态机唯一六态 draft/anchored/open-inquiry/contending/cross-checked/published，信任度是字段不是状态，human-signed 是背书标记非状态；property-based 探索因 oracle 回魂退役。
**依据**: References/270、271（十问批判：判据密度不足，每机制必须可计算否则算隐喻；概念上限状态/机制各 ≤6）。
**状态**: 已实施（l2_state.py 为状态文件化范式）。

## ADR-008: GAUNTLET 压力测试 + FORGE 创造力（2026-09）
**决策**: GAUNTLET 五压力维（模型强度/上下文预算/任务难度/监督/环境）+ T1–T14 剧本，逃逸率 ≤20%、全监督档=0、检查点续作=100%、T14 污染零容忍；FORGE 四算子（变异/类比/反事实/组合）→ candidates/ 候选仓（发散不设防）→ 检验闸（收敛有判据），黄金 diff 只校 schema 形式不罚内容创新。
**依据**: References/273、274；目标是垃圾模型也能干活、无人自纠错到「可签悬置」。
**状态**: 协议已立；candidates/ 目录待建（见 ADR-010 I 项）。

## ADR-009: 架构宪法为最高架构事实源（2026-09-12）
**决策**: References/277 CONSTITUTION v1.0 是唯一当前生效架构，266–276 降级为只读演进档案；此后架构变更走修宪程序（证据→提案带判据→红队批判→版本号→GAUNTLET 复测），不再堆并列文档。
**依据**: 11 份演进文档导致「当前生效什么」不可知，本身违反环节减法。
**状态**: 已实施。

## ADR-010: 先复用后新建、先榨干后外求（2026-09-12）
**决策**: 任何新机制提案第一步必须 grep 现有工具并附「已存在/部分存在/不存在」判定，重复造轮子驳回（References/278 内部红利审计）。已查明：error budget 复用 debt_ledger.py；先决边复用 ATOM-REL-DAG/TARGET/PREREQ-READABLE + prereq_topo_check.py + learning_path.py（字段名以仓库为准 `prerequisite`，非 `prereq`）；价值函数覆盖维复用 atom_coverage_map.py。待办：建 candidates/；knowledge_graph.json（0 工具引用）限期激活或退役；~54 个非 CI 工具普查归档；P8–P11 新毒样例（编译期常量冒充活性/一 bit 两计/口径不统一反转/消除与失败不可区分）。
**依据**: 设计↔实现互相看不见是当前最大内部浪费；79 条误解、1528 夹具、49 卡的横向价值尚未二次提炼。
**状态**: 进行中。
