# 671d · 前端重制验收报告（学术化 / 去 AI 味）

> 批次：671d（前端重制）　分支：master　日期：2026-10-01
> 接手说明：671d 前序已完成主体重制（未提交）；本报告为**接手后的核验 + 收口 + 修缺陷**验收。
> 红线遵守：未改 `research/paper_v*.md`、`research/latex/`、`tools/`、`tests/`、`data/` 原始数据、`atoms/`、`evidence/`；未引入外部依赖；未改设计令牌语义变量名（只改值）；未破坏 670c3/c4/c5 的 noscript / 键盘导航 / 焦点管理。

---

## 一、目标与验收结论

**目标**：把前端从"AI 生成感"改成"学术高级感"（参照 Distill.pub / Stripe 文档 / Linear / Vercel 文档的克制排版）；同步**全局改名** `祈易` → `阙疑`。

**结论**：**通过**。8 页排版统一、全站 0 AI 味词汇 / 0 AI 味视觉、设计系统 v2 全量应用、对比度与 a11y 全过、性能达标、889 断言全绿、dist 重建并验证。

| 验收项 | 标准 | 实测 | 结果 |
|---|---|---|---|
| 8 页重制 | 排版统一 | index / cards / card / learn / experiments / verdicts / starmap / verify 全部统一 | ✅ |
| 去 AI 味词汇 | 0 命中 | 禁词表全站 0 命中 | ✅ |
| 去 AI 味视觉 | 0 命中 | 渐变 / 毛玻璃 / 辉光 / 多阴影 / 大圆角 / count-up / hover 上浮 全站 0 命中 | ✅ |
| 设计系统 v2 | 全页 `var()` | 颜色/间距/圆角/动效一律 `var(--…)`，无写死 | ✅ |
| 对比度 | ≥4.5:1（正文） | 27 组 × 深浅 2 主题 = 54 项，failures=0 | ✅ |
| 响应式 | 4 断点无横向滚动 | 320/768/1024/1440 通过；0 critical / 0 moderate | ✅ |
| a11y | 8 页 0 问题 | 8 页 critical=0 moderate=0 minor=0 | ✅ |
| 性能 | 首页 gzip ≤120KB | 首页 gzip **35.1KB** | ✅ |
| 功能测试 | 888+ 断言全绿 | **889 断言 + 8 页 jsdom 冒烟** | ✅ |
| dist | 重建 + 验证 | `node web/build.mjs` 25 项；`dist_verify` PASS | ✅ |

---

## 二、设计系统前后对比（`web/css/design-tokens.css`）

| 维度 | 旧（666/667） | 新（671d v2） | 动机 |
|---|---|---|---|
| 底色 | 暖中性 `#1a1a1a` | 纯中性灰阶 `#0a0a0a` / `#fafafa` | 学术底色不该有温度偏好 |
| 强调色 | 暖橙 `#d97757` | 沉静蓝 `#5b8def`（浅 `#2563eb`） | 橙/紫/青被明令禁止；蓝更克制 |
| 主按钮填充 | 直接用强调色 | `--color-accent-strong`（`#2563eb`） | 白字压在 `#5b8def` 仅 3.23:1，压 `#2563eb` 才 5.17:1 |
| 圆角 | 含 `999px` pill | 收敛 4 / 6 / 8 三档 | 禁止全圆角滥用 |
| 动效 | 含 900ms 数字滚动 | 只剩 150 / 200ms 两档 | 数字滚动是典型"模板感" |
| 毛玻璃 | `backdrop-filter` | `--glass-blur: 0px` | 正文压在半透明噪音上 ⇒ 对比度不可算 |
| 辉光 / 渐变 | glow / grad-surface | 全部置空（保留变量名为别名） | 霓虹装饰属 AI 味 |
| 阴影 | 多层 | 默认无；仅弹窗/下拉/tooltip 一层 | 层级靠 1px 描边 + 底色差 |

---

## 三、排版变化（`style.css` + `css/669c.css`）

- 正文 `15px / 行高 1.7`（学术排版行高要大）；行宽 720px（65–75 字符）；section 之间 64–96px，用淡分隔线而非"卡片堆"。
- 标题不跳级：h1 32px / h2 24px / h3 18px，字重 ≤600，`letter-spacing: -.015em`。
- 数字一律 `font-variant-numeric: tabular-nums`（指标 / 表格 / 时间线 / 仪表盘）。
- 表格为**学术三线表**：表头底线 + 表尾线 + 淡行分隔，**无竖线**、无单元格底色。
- 实验页图表零依赖内联 SVG（不引 ECharts），每根柱带 Wilson 95% CI 与 k/n。
- 组件统一：`.card` / `.btn`（主/次/文字三态）/ `.table` / `qy-tag`（ok/warn/bad）/ `qy-nav`。

---

## 四、去 AI 味的具体措施

**文字**：全站禁词（赋能 / 打造 / 一站式 / 全方位 / 深度 / 极致 / 革命性 / 颠覆性 / 智能 / 自动化 / 高效 / 便捷 / 强大 / 完善 / "让我们一起" / "开启新篇章" / "引领未来"）经 `search_content` 全目录复查 **0 命中**。

**视觉**（经 CSS 正则复查 0 命中）：
1. 删除全部渐变（尤其紫蓝渐变）与 `grad-surface`；
2. 删除毛玻璃 `backdrop-filter` → 顶栏/弹窗改不透明底 + 1px 线；
3. 删除辉光 `box-shadow glow`（pass/fail/unknown/accent 四档全置空）；
4. 圆角收敛（pill 999px → 6px；卡片 ≤8px）；
5. 卡片 hover 由"上浮 + 加阴影"改为**只变描边色**；
6. 删除卡片顶部/左侧彩色条（`.warn-line`、`.err-card` 左条改 1px 淡描边）；
7. 删除 `.eyebrow` 装饰小标签、删除 ✓/✗ 装饰符号、删除状态"彩色胶囊"→小圆点 + 文字；
8. 删除 900ms 数字滚动（count-up）。

**取代手法**：大量留白、1px 描边分层、90% 中性灰 + 10% 强调色、字体层次克制（不做 700 字重）。

---

## 五、改动文件清单

**前序已完成（本次核验确认）** — 18 个 web 文件：
`web/app.js`、`web/card.html`、`web/cards.html`、`web/components/qy-nav.js`、`web/components/qy-tag.js`、`web/css/669c.css`、`web/css/design-tokens.css`、`web/css/responsive.css`、`web/experiments.html`、`web/home.js`、`web/index.html`、`web/learn.html`、`web/starmap.html`、`web/starmap.js`、`web/style.css`、`web/tests/contrast.test.mjs`、`web/verdicts.html`、`web/verify.html`。

**本轮（接手）改动**：
1. `web/verify.html` — 补 `<h2>现场比对</h2>`，修 h1→h3 跳级（a11y moderate，8 页里唯一残留）。
2. `web/index.html` — 去 Hero 拼音副标题；入口文案对齐"查看卡库 / 查看实验"。
3. `docs/README_v2.md` — 设计准则行更新为"纯中性灰阶底 + 沉静蓝；无渐变/毛玻璃/辉光"（并收录 671d 全局改名 祈易→阙疑）。
4. `docs/670c_前端完成度.md` — 追加第七节（671d 重制记录）。
5. `web/dist/` — 重建（gitignored 本地产物）。

**命名**：全站品牌统一为 `阙疑 QueYi`（`qy-nav` 组件渲染）；`web/` 内 `祈易` 残留 **0**。

---

## 六、测试与审计结果（可复跑）

```bash
# 对比度（27 组 × 深浅 2 主题）
node web/js/contrast_check.js                     # → pairs=27 failures=0

# 功能测试（纯逻辑 + jsdom 冒烟）
cd web && npm test                                # → 889 断言全绿 + 8 页冒烟

# 静态审计（Python）
python3 tools/a11y_audit_670c4.py                 # → 8 页 0 问题
python3 tools/responsive_audit_670c5.py           # → 0 critical / 0 moderate
python3 tools/perf_audit_670c5.py                 # → 首页 gzip 35.1KB ≤ 120KB

# dist
node web/build.mjs                                # → 复制 25 项
python3 tools/dist_verify_670c2.py                # → PASS（8 HTML / 63 JS / 0 引用缺失）
```

| 测试 | 断言 / 页数 | 结果 |
|---|---|---|
| learn_engine.test | 106 | ✅ |
| charts.test | 162 | ✅ |
| cards.test | 100 | ✅ |
| verdicts.test | 126 | ✅ |
| starmap.test | 74 | ✅ |
| contrast.test | 32 | ✅ |
| robustness_670c3 | 70 | ✅ |
| a11y_670c4 | 122 | ✅ |
| keybind_670c5 | 24 | ✅ |
| perf_670c5 | 73 | ✅ |
| smoke（8 页结构 + 图表 DOM） | 8 页 | ✅ |

**累计 889 断言 + 8 页冒烟。**

---

## 七、诚实登记

1. **主体重制非本轮完成**：设计系统 v2、8 页排版、18 个 web 文件、全站改名、新增 `qy-tag` 组件，均由 671d **前序**完成。本轮工作为**核验 + 收口**：跑通全部审计、修 1 处 a11y moderate（verify.html 标题跳级）、对齐 1 处首页文案与 1 行文档、重建 dist。
2. **未做**：真实浏览器 / 读屏器实测（本机无 headless 环境，结论基于静态审计 + 单测 + jsdom 冒烟），与 670c 登记一致。
3. **响应式 1 minor**：媒体查询含 900/1080/1100 非统一断点，沿用 670c 登记，未强改（避免布局回归）。
4. **数字未改**：前端展示的指标一律来自 `web/data/*.json`，本轮**未改动任何数字**。
5. **dist 不入库**：`web/dist/` 已被 `.gitignore`（第 62 行 `dist/`）忽略，属本地发布/验证产物。

---

## 八、提交

- `git commit -s`（DCO 署名）；**不 push**。
- 提交范围：`web/` 重制源文件 + 本验收报告 + `docs/670c_前端完成度.md`（+ 671d 改名涉及的 `docs/README_v2.md`）。
- 不包含：`research/`、`tools/`、`tests/`、`data/` 原始数据、`atoms/`、`evidence/`、其他批次的未提交改动、`web/.playwright-cli/` 浏览器日志、`web/_671d_serve.mjs` 本地开发脚本。
