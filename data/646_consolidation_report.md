# 646 工具合并分析报告（B4）

- 645 核心工具数：15
- 合并后可达：**10**（目标 ≤12）
- 是否已执行合并：**False**（本工具只分析，执行留 647）

## 合并方案

### 耦合编排 + 反馈 + 效果评估
- 成员：three_layer_orchestrator_645, coupling_feedback_645, coupling_effect_645
- 目标：three_layer_orchestrator_645（子模块 feedback/effect）
- 理由：三者都消费同一份 chain 数据，feedback/effect 都是 chain 上的纯函数

### 证据等级 + 充分性
- 成员：evidence_grading_645, evidence_sufficiency_645
- 目标：evidence_grading_645（充分性作 judge 子模块）
- 理由：充分性判定直接消费等级结果，同属头部层证据判定

### R5 闭环 + 规则 error/老化
- 成员：loop_r5_runner_645, rule_error_tracker_645, rule_aging_detector_645
- 目标：loop_r5_runner_645（error/aging 作子模块）
- 理由：三者都读同一份账本历史，闭环以 error/aging 为输入

## 诚实登记

- **未执行合并**：15 个工具各自被 `tests/test_*_645.py` import，删除会导致 645 测试套件整体红，违反「功能不丢失 / 单测全绿」。执行合并需同步改测试，留 647。
- 合并方案已给出（3 组，15 → 9），可执行、可验证。
