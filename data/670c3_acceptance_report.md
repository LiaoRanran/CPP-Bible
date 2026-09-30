# 670c3 批次验收报告

- **批次**：670c3（P0 前端健壮性收口：全局降级 + 入口页三态 + 全页面错误处理）
- **分支**：master　**日期**：2026-09-30　**执行者**：LiaoRanran（DCO）
- **目标**：**任何情况下用户都不会看到白屏**。

---

## 0. 一句话

> 8/8 页面有 `noscript` 纯 HTML 降级（全部 ≤500B）；`index` 三态（骨架屏 / 错误卡+重试 / 空状态）补齐；8/8 页面注入全局运行时兜底（`window.onerror` + `unhandledrejection` + 顶部横幅）；新增 **70 条断言**，前端断言总数 **669**（≥668），既有 599 条不回归。

---

## 1. 任务 A · 全局 noscript 降级 ✅

| 页面 | 降级内容 | 字节数 |
|---|---|---|
| index | 项目名 + 一句话定位 + 核心数字（67 规则 / 42 卡 / 452 账本 / 87.5% / 35.0%） | 474 |
| cards | 需 JS 才能浏览 + 返回首页链接 | 444 |
| learn | 需 JS + 学习路径文字版 | 466 |
| experiments | 核心结果纯文字（holdout/external/变异/反事实） | 471 |
| verdicts | 需 JS 查看四态判决历史 + 返回首页 | 434 |
| starmap | 需 JS（178 节点 / 1093 边） | 345 |
| verify | 需 JS（Web Crypto 重算 sha256，文件不出本机） | 378 |
| card | 需 JS + 示例卡断言/证据 | 477 |

- **8/8 覆盖**（`grep -c "<noscript>"` 逐页 = 1）。
- **样式内联**（不依赖 CSS 文件），深色兜底 `#1a1a1a` / 浅色文字 `#e8e6e3`、居中、`max-width:600px`。
- **全部 ≤500 字节/页**（E2 预算）✅。

---

## 2. 任务 B · index 三态 ✅

- **B1 loading**：`#metrics` 3 个骨架卡 + `#timeline` 2 条骨架线，**纯 CSS pulse 动画**（不依赖 JS），`data-qy-state="loading"` + `aria-busy="true"`；数据到达后 `setState('ready')` 切换，过渡 200ms。
- **B2 error**：`robustFetch()` 失败 → `renderErrorCard()`（⚠ 图标 + "数据加载失败" + 原因 + 重试按钮）；**重试最多 3 次、间隔 1s**；3 次后附"请检查本地服务器是否启动（python -m http.server）"。
- **B3 empty**：`classifyPayload` 判定空对象/缺字段 → `renderEmpty('no-data')`；提交列表为空 → `renderEmpty('no-commits')`；**指标为 0 或缺失显示 `--`**（`formatMetric`，避免把"无数据"误读成"确实是 0"）。
- **B4**：状态切换 200ms 过渡；error 态下导航链接不受影响（错误卡只替换数据容器）；`console.error` 输出细节，界面不暴露技术细节。

---

## 3. 任务 C · 全页面错误处理

- **C2 运行时兜底 ✅（8/8）**：`web/js/robustness.js::installGlobalErrorHandlers()` 注入 `window.onerror` + `unhandledrejection`，命中即在顶部显示红色横幅"页面初始化失败，请刷新重试"（`role="alert"` + `aria-live`）。8 个页面均含 `initRobustness` 调用。
- **C1 数据加载错误**：`index` 已接新统一错误卡（cards/status/metrics/commits/timeline 五处）；其余 6 个数据页面**保留其既有 per-page try/catch**（670c2 审计确认 cards/learn/experiments/verdicts/starmap/verify 均有 error 分支），并叠加**全局横幅兜底** ⇒ 满足"不白屏"，但**未统一到新错误卡**（诚实登记，见 §6）。
- **C3 空数据**：统一 `renderEmpty`（图标+文字+动作）；筛选无结果文案"无匹配项"+"清除筛选"已就位（`emptyModel('no-match')`）。

---

## 4. 任务 D · 测试

- **D1 新增** `web/tests/robustness_670c3.test.mjs`：**70 条断言**（noscript 覆盖 8 + 体积 8 + CSS 链接 8 + 兜底注入 8 + 骨架 2 + 纯逻辑 36）。
  - **纯 Node、无 jsdom 依赖** ⇒ **始终可跑**（不依赖 `npm i jsdom`）。
  - 覆盖：noscript 存在/体积、CSS 关键类、index 骨架与 loading 态、`shouldRetry/retryDelayMs/classifyPayload/friendlyError/classifyFetchError/emptyModel/formatMetric/exhaustedHint/noscriptHtml`。
- **D2 不回归**：既有 **599** 条全绿（learn_engine 106 / charts 162 / cards 100 / verdicts 126 / starmap 74 / contrast 31）+ `smoke` exit 0 + 670c2 的 **39** 条 Python 测试全绿。
- **合计前端断言 669 ≥ 668** ✅（106+162+100+126+74+31+70）。
- `web/package.json` 的 `test` 脚本已加入新测试。

---

## 5. 任务 E · 验证

| 项 | 结果 |
|---|---|
| 8/8 noscript（grep） | ✅ |
| index 三态齐全 | ✅ |
| 全局运行时兜底 8/8 | ✅ |
| JS 语法（`node --check`） | ✅ robustness_core / robustness / home 全 OK |
| 骨架 CSS ≤2KB | ✅ **665B** |
| noscript ≤500B/页 | ✅ 最大 477B |
| 错误处理 JS ≤3KB | ⚠ **偏差**：raw 9.7KB / **gzip 3.9KB**（见 §6-1） |
| 首屏 +100ms 内 | ⚠ 未用浏览器实测；模块为 `type="module"`（延迟执行），gzip 3.9KB 增量极小 |

---

## 6. 诚实登记（未达标 / 偏差）

1. **错误处理 JS 超预算**：E2 要求 ≤3KB，实测 **raw 9730B / gzip 3925B**。原因：实现的是**完整模块**（重试状态机 + 全局横幅 + 错误卡 + 空状态 + 骨架切换），而非最小内联片段。**权衡**：功能更完整、可单测；若要压到 3KB，可去掉注释并把 core 内联进 `qy-*.js`。**未做**。
2. **C1 未统一**：仅 `index` 用新错误卡；其余 6 页沿用既有 per-page 错误处理 + 全局横幅，**未逐页替换为新组件**。
3. **未做浏览器实测**：E1 的手动清单（禁用 JS / 断网）是**设计保证 + 静态/单测覆盖**，**未在真实浏览器中逐条目视**（无 headless 浏览器环境）。
4. **`web/dist/` 未重建**：dist 为 `.gitignore` 忽略的构建产物；本批改了 `web/*.html` 与 `web/home.js`，**dist 已过期**（下次构建刷新）。
5. **`formatMetric` 把 0 显示为 `--`**：这是 B3 的**明确要求**，但会掩盖"真实为 0"的情况——已在函数注释标注。

---

## 7. 新增/变更文件

**新增**：`web/js/robustness_core.js`、`web/js/robustness.js`、`web/css/robustness.css`、`web/tests/robustness_670c3.test.mjs`、`data/670c3_acceptance_report.md`
**修改**：`web/index.html`、`cards.html`、`learn.html`、`experiments.html`、`verdicts.html`、`starmap.html`、`verify.html`、`card.html`（noscript + robustness.css + init 注入）、`web/home.js`（三态接线）、`web/package.json`（test 脚本）

> 未碰 `tests/`、`data/experiments/`、受控目录、`gate_engine.py`/`counts_659.py`、`research/latex/*.pdf`。
