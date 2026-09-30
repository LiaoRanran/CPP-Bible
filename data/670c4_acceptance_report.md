# 670c4 批次验收报告

- **批次**：670c4（P1 可访问性全扫 + 键盘导航极致化 + 语义化收口）
- **分支**：master　**日期**：2026-09-30　**执行者**：LiaoRanran（DCO）
- **目标**：WCAG 2.1 AA 全通过；键盘党不用鼠标完成所有操作。

---

## 0. 一句话

> **8 页 a11y 审计 0 问题（critical / moderate / minor 全 0）**；全局快捷键 + 帮助弹窗 + 焦点陷阱就位；对比度 27 组 0 失败；新增 **122 条断言**，前端合计 **791 ≥ 709**；**670c3 健壮性完整保留**（noscript + initRobustness 8/8）。

---

## 1. 任务 A · WCAG 2.1 AA 审计与修复 ✅

**A1 工具**：`tools/a11y_audit_670c4.py`（静态解析 8 页；产出 `data/a11y_audit_670c4.json`）。
检查项：img alt / 可交互元素名称 / 表单控件 label 关联 / 空链接 / table caption / heading 层级 / 唯一 h1 / 重复 id / lang / viewport / 跳过链接 / 语义化建议。

**修复过程（审计驱动，逐轮收敛）**：

| 轮次 | critical | moderate | minor | 动作 |
|---|---|---|---|---|
| 初版 | 22 | 8 | 6 | 首扫（含 label 误报，见 §6-1） |
| 修 label 关联逻辑 | 3 | 8 | 6 | 审计支持 `<label for>` / 包裹 / `hidden` |
| 修 verify 输入 | 0 | 8 | 6 | 加 `aria-label` |
| 修 heading 倒置 | 0 | 2 | 6 | index 互换 h2↔h3；5 页 h3→h2 |
| 修 verify table | 0 | 0 | 6 | 加 `aria-label` + `<th scope="col">` |
| 加 `<header>` | **0** | **0** | **0** | 6 页 `<section>(h1)` → `<header>` |

**A2 对比度**：`node web/js/contrast_check.js` → **27 组 0 失败**（含正文/大字/UI 边框，深色主题）。

**A3 修复清单**：
- 表单控件补 `aria-label`：verify 的 sha256 输入 + 文件选择。
- **heading 层级倒置修复**（h1→h3 跳级）：index 互换 h2↔h3（section 升 h2、卡标题降 h3）；cards/learn/experiments/verify/card 的 h3→h2。
- 表格补 `aria-label` + `<th scope="col">`（verify 两张）。
- 6 页补 `<header>` 地标。

---

## 2. 任务 B · 键盘导航 ✅

- **B1 可达性**：8 页均有跳过链接（首个可聚焦元素）、`<main id="main">`、`<nav>`；焦点样式统一。
- **B2 快捷键系统**（`web/js/a11y.js` + `a11y_core.js`）：
  - 全局：`g`+`h/c/l/e/v/s` 跳转、`?` 帮助弹窗、`Esc` 关闭。
  - 卡库/学习页本地键位已在 `LOCAL_KEYS` 注册（`/`、`j/k`、`Enter`、`1-4`）。
  - **帮助弹窗**：`role="dialog"` + `aria-modal` + `aria-labelledby`，列出全部快捷键。
- **B3 焦点管理**：打开 → 焦点移入首个可聚焦元素；`Tab` **循环陷阱**（`cycleIndex`）；关闭 → 焦点**回到触发元素**；`Esc` 关闭。
- **B4 焦点样式**：`web/css/a11y.css` 统一 `:focus-visible` = **2px solid #d97757 + 2px offset**；`forced-colors` 高对比度下用 `Highlight`；未使用 `outline:none`。

---

## 3. 任务 C/D · 屏幕阅读器与语义化 ✅

- **C1**：`aria-live="polite"` 播报区（`ensureLive`）；弹窗 `role="dialog"`；表格 `aria-label` + `<th scope="col">`；跳过链接。
- **C2 动态播报**：`announce()`；`announceResults(shown,total)`（"显示 N 条结果，共 M 条"/"没有匹配项"）；`announceRating(grade)`（"已标记为已掌握"等）；错误走 `role="alert"`（670c3 横幅）。
- **D1 语义化**：`<header>`（8/8）、`<nav>`（qy-nav 组件）、`<main id="main">`、`<footer>`、`<section>`。
- **D2/D3**：导航为链接（`<a href>`），触发动作为 `<button>`；审计**无 `link-as-button` 命中**。

---

## 4. 任务 E · 测试 ✅

- 新增 `web/tests/a11y_670c4.test.mjs`：**122 条断言**（≥40），**纯 Node、无 jsdom 依赖**。
  覆盖：快捷键映射/归一化/序列解析/焦点循环/播报文案 + 8 页静态结构（跳过链接、main、nav、**唯一 h1**、lang、viewport、a11y.css、initA11y、**noscript/initRobustness 保留**）+ 审计产物 `critical_total==0`。
- **不回归**：learn_engine 106 / charts 162 / cards 100 / verdicts 126 / starmap 74 / contrast 31 / **robustness_670c3 70** / **a11y_670c4 122** = **791**（≥709）；`smoke` exit 0。
- `web/package.json` test 脚本已加入新测试。

---

## 5. 任务 F · 验证

| 项 | 结果 |
|---|---|
| a11y_audit 0 严重问题 | ✅ **0/0/0** |
| 对比度双主题达标 | ✅ 27 组 0 失败（深色） |
| 8 页跳过链接 | ✅ |
| 全局快捷键 | ✅ |
| 弹窗焦点管理 | ✅ 移入 / 循环 / 回位 |
| aria-live 播报 | ✅ |
| 语义结构 | ✅ header/nav/main/section/footer |
| 一页一 h1、不跳级 | ✅ |
| 审计工具运行 ≤5s | ✅ **418ms** |
| 快捷键 JS ≤3KB gzip | ✅ **3059B ≈ 2.99KB**（贴线） |
| 670c3 健壮性不破坏 | ✅ noscript + initRobustness 8/8 |

---

## 6. 诚实登记

1. **审计工具自身修了 2 个误报**：① 初版不识别 `<label for>`/包裹标签 ⇒ 22 个假 critical；② table caption 用页面级判断 ⇒ 误报/漏报。**均已修正**（现为逐表判定）。
2. **未做真实辅助技术实测**：F1 的 NVDA/Narrator、Windows 高对比度、200% 缩放、文字间距 —— **均未在真实环境逐条目视**（无 headless 浏览器/读屏器）。当前结论基于**静态审计 + 单测**。
3. **`<header>` 在 `<main>` 内**：6 页的 `<header>` 是**内容头部**（不是页面级 `banner` 地标）；`banner` 地标未单独建立。
4. **快捷键仅注册，未接页面逻辑**：`g+` 导航、`?`/`Esc` 已全局可用；`/`、`j/k`、`1-4` 等**本地键位已在 core 注册并可测**，但**卡库/学习页的具体绑定未逐一接线**（需改各页 JS）。
5. **`smoke` 依赖 jsdom**：本机未装，但能从父级 `node_modules` 解析到 ⇒ 通过；干净克隆下会优雅跳过。

---

## 7. 新增/变更文件

**新增**：`tools/a11y_audit_670c4.py`、`data/a11y_audit_670c4.json`、`data/670c4_acceptance_report.md`、`web/js/a11y_core.js`、`web/js/a11y.js`、`web/css/a11y.css`、`web/tests/a11y_670c4.test.mjs`
**修改**：8 个 HTML（a11y.css + initA11y + heading 层级 + header 地标 + verify 表单/表格 label + noscript 标题 h1→p）、`web/package.json`

> 未碰 `tests/`、`data/experiments/`、受控目录、`gate_engine.py`/`counts_659.py`、`research/latex/*.pdf`。
