# 666 B 段 · 前端改造：完成度登记（诚实版）

> 一句话结论：**B1/B2/B3/B4(部分)/B5/B6/B7(部分) 已落地并有可复算的检查**；
> 未达 666 目标的部分逐条写在 §3 —— 尤其"虚拟滚动"只做了**增量渲染**、WCAG 只做到**自动可验的部分**。

## 1. 交付物

| 产物 | 路径 | 说明 |
|---|---|---|
| 设计令牌（唯一变量源） | `web/css/design-tokens.css` | Claude 式暖中性底 + 单一橙强调 + 8px 基数 + 深/浅双主题 |
| 站点样式 | `web/style.css` | **只引用变量**；含指标卡/时间线/卡网格/进度条/焦点环/跳转链接 |
| 导航组件 | `web/components/qy-nav.js` | 五页共用；`aria-current` + 主题切换（localStorage `qy-theme`） |
| 首页逻辑 | `web/home.js` | 指标卡（滚动动画）/ 时间线 / 最新提交 / 现状面板 / hero 小图 |
| 卡库页 | `web/cards.html` + `web/cards.js` | 网格 + 筛选（状态/域/类型/范围）+ 搜索 + 展开 + 机器卡独立区 |
| 学习页 | `web/card.html` + `web/card.js` | 三段式（前置/学习/自测）+ **进度条**（`role="progressbar"`）+ 本机进度 |
| 指标数据 | `web/data/metrics_666.json` | 由 `tools/web_metrics_666.py` **现算**（卡数/规则数/检出率/账本/时间线/提交） |
| 数据流水线 | `tools/web_data_pipeline_656.py` | `--build` 重建 data+dist；`--check` 校验 schema/漂移/对比度/接线 |

## 2. 逐项对照 666 要求

### B1 设计系统重写 ✅
- 背景 `#1a1a1a`、主色 `#d97757`、圆角 8px 基数、间距 8px 基数、字体 Inter/system-ui、无阴影堆叠。
- CSS 变量化：颜色/间距/圆角/动效/层级/焦点全部在 tokens 里；`style.css` **零硬编码颜色**。
- **深/浅切换**：默认跟随系统，顶栏按钮显式覆盖（`localStorage.qy-theme`）。
- **对比度算出来**：`--check` 现算 8 组配对（深/浅两套都过 AA；实测值写在 tokens 的注释里）。

### B2 首页重做 ✅
- 顶部：项目名 + 一句话定位（"可被独立验收"）。
- 中部：**核心指标卡**（卡数 / 规则数 / holdout 检出率 / 账本事件）—— 数字全部来自
  `web/data/metrics_666.json`，滚动动画保留（`countUp`，尊重 `prefers-reduced-motion`）。
- 下方：**系统状态时间线**（6 个批次里程碑，带"这样做的理由"）。
- 底部：**最新提交**（git 现取）+ 链接区。
- 保留：真数据渲染的 hero 接地图、星图统计、三通道编码图例。

### B3 卡浏览页重做 ✅（新页 `cards.html`）
- 网格布局（`auto-fill, minmax(320px,1fr)`）+ hover（描边/底色，**不加阴影**）。
- 筛选：状态 / 域 / 类型 / 范围（实卡域 / 全部 / 只看草稿）；搜索 id 与标题。
- 点击展开：`<details>` 展示台账字段（命题/证据/先修 id 列表），并提供 `card.html?card=<id>` 深链。
- 机器卡独立区：16 张机器卡单独列出，显式标注 `needs_review`、**不进教学台账**。

### B4 学习页重做 ⚠️ 部分
- 三段式保留（前置 / 学习 / 自测）；自测题仍由台账字段机械生成（原有能力）。
- **新增**：进度条（视觉 + `role="progressbar"` + `aria-valuenow`），与"本机已学 x/y"同源。
- **未做**：自测题的交互重做（仍是"显示答案 + 记分"的朴素形态）、错题回顾、键盘快捷导航。

### B5 星图页保留 ✅
- 星图不重构；配色改为**与设计令牌同值**（`app.js` 的 `STATE_COLORS`/`LINK_STYLE` 镜像 tokens，
  理由是 canvas 拿不到 CSS 变量）。
- 新增：跳转链接、canvas `role="img"` + `aria-label`。

### B6 性能 ⚠️ 部分
- 懒加载：星图依赖走**动态 import**（`await import('./vendor/cosmos.js')`），只在星图页加载；
  vendor 1.4MB 与手写资源彻底分离。
- 增量渲染：卡库每批 24 张 + `IntersectionObserver` 哨兵自动续批（**不是**完整虚拟滚动）。
- 体积实测（未压缩、含共享资源）：

| 页面 | 首屏 html+css+js |
|---|---|
| index.html | 59.4 KB |
| cards.html | 51.7 KB |
| card.html | 59.6 KB |
| verify.html | 54.9 KB |
| starmap.html | 66.8 KB |

`web/dist/` 压缩产物合计 **92.8 KB < 100 KB**（不含 `web/vendor/` 第三方库）。
- **未做**：图片懒加载（本站基本无图片）、按路由代码分割、真实大列表（>1000 项）压测。

### B7 WCAG 2.2 AA ⚠️ 部分（自动可验的部分已过）
- 已做：跳转链接（每页）；统一 `:focus-visible` 焦点环（含 offset）；主题切换按钮有 `aria-label`；
  导航 `<nav aria-label>` + `aria-current="page"`；结果计数 `role="status" aria-live="polite"`；
  进度 `role="progressbar"`；canvas 有 `role="img"` + 描述；表单控件均有 `<label for>`；
  `prefers-reduced-motion` 关动效。
- 对比度：由 `--check` **现算**（8 组配对，深浅两套均过）。
- **未做**：屏幕阅读器（NVDA/VoiceOver）实测、全站键盘走查（Tab 顺序逐页记录）、
  缩放 200%/400% 重排实测、自动化 axe 扫描。**这些需要人**（见 §3）。

## 3. 诚实登记：没做到的部分（不许算"已完成"）

1. **虚拟滚动**：只做了增量渲染（每批 24）。若卡数涨到几千，需要真正的窗口化
   （或服务端分页 + 索引分片）。
2. **无障碍**：只做到"能自动验的"（对比度 + 语义属性 + 焦点样式）。
   屏幕阅读器实测/键盘走查/缩放重排**未做**，不能声称"WCAG 2.2 AA 通过"。
3. **学习页交互**：自测仍是朴素形态；没有错题本、没有间隔重复（spaced repetition）。
4. **主题切换**：只切颜色令牌；canvas 里的颜色在 JS 侧镜像，切换主题时**需要刷新**
   （未做运行期重读 CSS 变量的重绘）。
5. **构建**：仍然无打包框架（刻意的）；`dist/` 只是保守压缩（删注释/空行），不做 tree-shaking。
6. **i18n**：全中文；无多语言。

## 4. 怎么复算

```powershell
# ① 数据与令牌校验（schema / index 漂移 / WCAG 对比度 / 组件接线 / 卡片契约）
.venv\Scripts\python.exe tools\web_data_pipeline_656.py --check

# ② 重建前端数据与 dist（会重跑各生成器）
.venv\Scripts\python.exe tools\web_data_pipeline_656.py --build

# ③ 首页指标现算（卡数/规则数/检出率/账本/时间线/提交）
.venv\Scripts\python.exe tools\web_metrics_666.py --selftest
.venv\Scripts\python.exe tools\web_metrics_666.py --check

# ④ 本地预览（静态站，必须经 HTTP 打开：file:// 下 fetch 受限）
.venv\Scripts\python.exe -m http.server 8765 --directory web
```
