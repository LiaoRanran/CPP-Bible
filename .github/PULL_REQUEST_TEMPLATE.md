---
name: 变更请求
about: 提交章节内容、工具或流程变更
title: "[type] 一句话描述"
labels: []
assignees: ''

---

## 变更类型（勾选）

- [ ] 内容（章节正文 / 示例代码 / 练习）
- [ ] 工具（tools/ 门禁、编译、发布脚本）
- [ ] 流程 / 文档（CI、治理、规范）
- [ ] 站点 / 界面（mkdocs 主题、CSS、导航）

## 摘要

<!-- 说明改了什么、为什么改；若与 Issue 相关请引用 #NN -->

## 本次涉及的章节 / 文件

<!-- 形如：Book/part07_stl/ch92_chrono.md；tools/compile_all.py -->

## 门禁自检（提交前必须全部执行）

- [ ] `python tools/cppbible.py check --stage quality`（16 项全绿）
- [ ] 若涉及内容：`python tools/cppbible.py check --stage compile`（5 项全绿）
- [ ] 若涉及 Python：`python -m py_compile` 全部改动文件
- [ ] 若涉及 Markdown：无 W1/W2/W3 空白缺陷；Mermaid 静态校验通过
- [ ] 若涉及 CI：`git diff --check` 无空白错误
- [ ] 未引入新的 `compile_exempt.json` 豁免（除非有明确理由并记录）

## 风险与回滚

<!-- 影响范围、兼容性、以及如何回滚（revert 是否安全） -->

## 测试证据

<!-- 附门禁输出片段 / 截图 / 链接；无证据视为未验证 -->