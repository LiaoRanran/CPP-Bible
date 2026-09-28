# 13 · AI 使用与署名（AI_USAGE_LOG）

> NeurIPS 等政策要求披露 LLM 用途。本仓库所有 AI 贡献自此登记。

## 本仓库 AI 使用概况
- **用途**：架构设计、边界概念拆分（provenance/semantic scope）、外部效度方案、文档起草、
  工具脚手架（status_reconciler / defect_fixture / holdout / boundary_scope）。
- **人不做**：最终判决（pass/fail/unknown）由 four_state_verdict 与账本裁定；
  红线（受控目录零改动、账本零改）由人类维护的 Authority Ledger 锁定。
- **人工审**：每个 658 提交带 `git commit -s`（DCO），且门禁 L0 红线由人类可复核的工具执行。

## 登记规则
- 任何 LLM 生成的内容/代码，若影响验证器语义能力，必须经独立验收边界（658 宪法）。
- 新 AI 贡献追加到本文件 + `AI_USAGE_LOG.md`（若存在）。

## 责任
AI 生成内容不替代人类作者署名；错误责任归仓库维护者（人类），不归工具。
