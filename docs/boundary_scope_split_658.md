# 658 C 段 · boundary 概念拆分（provenance vs semantic scope）

> 现状：657 补了 26 卡边界，但 "boundary" 一个词指两种不同的东西。本段明确拆分。

## C1 问题

"Borders of what?" 混问了两类问题：
- **你凭什么信这条结论？**（实验范围）→ provenance
- **这条结论在哪种条件下成立？**（适用条件）→ semantic scope

不拆清，就会把"在我这套实验里得到"误读成"在所有情况下都成立"。

## C2 Provenance（验证来源边界）

回答："你在什么实验范围内得到这个结论？"
- `mutation_set_hash` — 用了哪版变异集
- `mutation_count` — 变异数量
- `generator_version` — 生成器版本
- 证据 `SHA256` — 每条证据的内容指纹
- 证据条数 — 引用了几条证据
- 编译器版本 — gcc 13.1.0 / clang 22.1.8

## C3 Semantic Scope（知识语义边界）

回答："这个结论在什么条件下成立？"
- C++ 标准版本（C++11/14/17/20/23/26）
- 编译器 / 优化级别
- 平台（x86_64 / AArch64 / Windows / Linux）
- 输入域假设
- 前置条件

## C4 实现（本批边界）

- provenance：由 `tools/boundary_scope_658.py` 只读提取到 `data/boundary_provenance_658.json`（**不碰 atoms**）。
- semantic scope：**卡的 frontmatter 拆两组字段** 这一动作本批**不执行** ——
  atoms/ 是 658 红线"受控目录零改动"之一。C4 的 frontmatter 编辑须留待
  显式获得 Authority Ledger 批准备份后再做。
- 判决逻辑：用 provenance 算"证据够不够"（provenance 不全 → 该结论不可用于红绿判决）；
  semantic scope 用于"这个结论在什么条件下成立"的标注（不影响判决，只影响引用时的适用声明）。

## 不变式

- provenance 与 semantic scope **不混在一个 `boundary` 字段里**。
- provenance 缺失的边界结论，只能当 unknown，不能当 pass。
