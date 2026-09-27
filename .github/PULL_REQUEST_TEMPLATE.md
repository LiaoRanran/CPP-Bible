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
- [ ] 流程 / 文档（CI、治理、规范、许可证与协作文件）
- [ ] 站点 / 界面（web/ 或 mkdocs 主题、CSS、导航）

## 摘要

<!-- 说明改了什么、为什么改；若与 Issue 相关请引用 #NN -->

## 本次涉及的章节 / 文件

<!-- 形如：Book/part07_stl/ch92_chrono.md；tools/compile_all.py -->

## DCO 签名（必须）

- [ ] 本 PR 的**所有** commit 均已签署 `Signed-off-by:`（`git commit -s`，见 [`DCO.md`](../DCO.md)）
- [ ] 我确认贡献内容为我原创，或来自允许再分发的来源（并在描述中注明出处）
- [ ] 我同意以本仓库许可证（Apache-2.0）分发该贡献

## 门禁自检（提交前必须全部执行）

- [ ] `python tools/tool_integrity.py --check`（信任根哈希面 34 条；若改动被钉文件，已 `--update` 重钉并在描述中说明）
- [ ] `python tools/cppbible.py check --stage quality`（16 项全绿）
- [ ] 若涉及内容：`python tools/cppbible.py check --stage compile`（5 项全绿）
- [ ] 若涉及 Python：`python -m ruff check tools/ tests/` 与 `python -m mypy --ignore-missing-imports tools/` 全绿
- [ ] 若新增/修改 `.py`：`python tools/license_header_check_655.py`（新增文件须带 Apache-2.0 SPDX 头）
- [ ] 若涉及测试：两阶段已跑（`-m "not slow" -n auto` 与 `-m slow -n0`），并在描述中附**计数（以 junit XML 为准）**
- [ ] 若涉及 Markdown：无 W1/W2/W3 空白缺陷；Mermaid 静态校验通过
- [ ] 若涉及 CI：`git diff --check` 无空白错误
- [ ] 未引入新的 `compile_exempt.json` 豁免（除非有明确理由并记录）

## 风险与回滚

<!-- 影响范围、兼容性、以及如何回滚（revert 是否安全） -->

## 测试证据

<!-- 附门禁输出片段 / 截图 / 链接；无证据视为未验证 -->

## 诚实登记（本项目强制）

<!-- 未做的、只做了一半的、口径有争议的、依赖外部条件的 —— 写在这里。
     "没做到"不会被打回，但"假装做到"一定会。 -->
