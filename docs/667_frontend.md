# 667 B 段 · 前端深化：完成度登记（诚实版）

> 一句话结论：**琉璃质感 / 表格 / 星图加强 / 层级留白 / 仪表盘 / 动效 / 对比度现算 七项都落地了，
> 且每一项都有可复算的检查**；没做到的写在 §5 —— 尤其**屏幕阅读器实测与真浏览器控制台仍未做**，
> 以及 `dist/` 因新增两页两模块**超过了 666 定下的 100 KB 预算**。

## 1. 交付物

| 产物 | 路径 | 说明 |
|---|---|---|
| 判决页（新） | `web/verdicts.html` + `web/verdicts.js` | 仪表盘 + 判决历史表（时间倒序/色标/筛选/排序/空状态）+ 数据对比表 + 漂移登记 |
| 判决页纯逻辑 | `web/verdicts_core.js` | 筛选/排序/取值抽成纯函数 ⇒ **可被 Node 真求值**（照 `graph_core.js` 先例） |
| 数据（现算） | `web/data/verdicts_667.json` | 由 `tools/web_verdicts_667.py` 现算（仪表盘 / 31 条判决 / 对比表 / 漂移 / excluded） |
| 数据工具 | `tools/web_verdicts_667.py` | `--selftest` / `--check` / `--write` / `--json`；**只读**，只写那一个文件 |
| 星图加强 | `web/starmap.html` + `web/starmap.js` | 聚类分色 + 聚类展开 + 搜索 + 聚类筛选 + 缩放按钮 + 线宽按权重 + hover 微发光 |
| 设计令牌 | `web/css/design-tokens.css` | 新增**琉璃组**（毛玻璃/回退底/辉光/渐变）与 `--touch-min`，深浅两套各有值 |
| 站点样式 | `web/style.css` | 新增 667 段：琉璃/表格/空状态/仪表盘/聚类面板/留白/44px 触控；**仍只引用变量** |
| 导航 | `web/components/qy-nav.js` | 新增"判决与数字"入口（六页共用同一实现） |
| 管线 | `tools/web_data_pipeline_656.py` | ① 对比度改为**分主题**解析（修了一个真缺陷，见 §4）；② 新增 5 组文字对比规则；③ `verdicts_667.json` 进 schema；④ 新页进 `PAGES`/`ASSETS` |
| 检查脚本 | `tools/web_logic_check_667.mjs`（Node 真求值）、`tools/web_smoke_667.mjs`（jsdom 真跑 DOM） | 28 + 23 条断言 |
| 回归锁 | `tests/test_web_verdicts_667.py` | 11 例，锁的是**不变量**不是数字 |

## 2. 逐项对照 667 要求

### ① 琉璃质感 ✅
- 卡片毛玻璃：`.glass` = `backdrop-filter: blur(14px) saturate(115%)` + 半透明底 + `--glass-line` 描边 + `--grad-surface` 微妙渐变。
- **必须有的回退**：`@supports` 不成立时用 `--glass-bg-fallback` **不透明底** ——
  否则正文会压在半透明噪音上，对比度直接失控（这是"好看但不可用"的典型）。
- 节点辉光：pass 绿 / fail 红 / unknown 灰，各带对应 `box-shadow`；**只给小语义元素**
  （状态点、星图 hover 节点），不给整块面板。
- 尊重 `prefers-reduced-motion`：辉光与过渡在 reduce 下一律关闭（不是"变快"，是**关掉**）。

### ② 表格美化 ✅
- **判决历史表**：时间倒序（默认）+ 四态色标（`.state-pill[data-state]`，色点 + 文字，**不只靠颜色**）
  + 搜索（id/说明/检测器）+ 状态筛选 + 来源筛选 + 6 种排序 + **点击表头切换升降序**。
- 表头是真 `<button>`（键盘可达），带 `aria-sort`；因为用了 `all: unset`，
  焦点环在 CSS 里**显式补回**（否则 Tab 过去看不见焦点）。
- **数据对比表**：同一量的两种算法**两个都列**（如外部语料 43.8% vs 35.0%），
  并用 `drift / caliber / frozen / ok` 四类标签标明性质。
- **空状态**：不是空白表格 —— 写清"为什么空"+"下一步（重置 / 生成命令）"。
- 表格有 `<caption>`（屏幕阅读器），结果计数用 `role="status" aria-live="polite"`。

### ③ 星图加强 ✅
- 节点按状态着色（既有三通道保留：色=四态 / 形=类型 / 光=credibility）。
- **连线按权重粗细**：数据里没有 `weight` 字段 ⇒ 用"两端节点度数之和的对数压缩"作**派生权重**，
  并在页面图例与本文档明确标注它是派生的（不许让人误以为数据自带权重）；可一键切回等宽。
- **聚类分色**：聚类键 = `domain` **展示层小写归一**（数据里 `mem 65 + MEM 23`、`lang 10 + LANG 8` 大小写两态，
  不归一会把一个域拆成两簇）；**只归一显示，不改数据文件**。
- **搜索 / 筛选 / 缩放**：搜索命中压暗（不是隐藏）+ 命中数播报；聚类下拉可只看该簇；放大/缩小按钮 + 滚轮；缩放到 `[0.25, 6]`。
- **cluster 展开**：点聚类 chip ⇒ 展开成员列表（前 60 个），可"只看这个聚类"或"定位"到某节点。

### ④ 层级与留白 ✅
- 标题大而松（`h1` 34/27px、`line-height 1.25`）、正文小而密（13px、`max-width 68ch`）、注释更淡（`--color-text-mute`）。
- 桌面端 `section` 上下留白 48→64px；新增 `.section-head` / `.eyebrow` / `.prose` / `.note-faint` 分层类。

### ⑤ 状态仪表盘 ✅（脚本现算，不写死）
- 8 个大数字：卡数 / 规则 / 判决历史条数 / holdout 检出率 / 外部语料检出率 / 逃逸率 / 账本事件 / 保护器。
- **数字全部来自 `web/data/verdicts_667.json`**，由 `tools/web_verdicts_667.py` 现算。
- 漂移项**自己标红**：holdout 的 `bad=1` + 一行"落盘 X 无现算来源，现算 Y，需人裁决前不得引用"。

### ⑥ 动效 ✅
- 数字滚动（`requestAnimationFrame` + 三次缓出）、hover 微发光、卡片 hover 描边/辉光。
- `prefers-reduced-motion: reduce` ⇒ 数字**直接写终值**、辉光关闭、过渡关闭（冒烟测试里专门验了这一条）。

### ⑦ WCAG 2.2 AA 对比度**现算** ✅（并修了一个真缺陷）
- `tools/web_data_pipeline_656.py --check` 现算 **13 组 × 2 主题 = 26 对**，深浅两套全过。
- 新增 5 组**文字**规则（四态色在 667 起也当文字用 ⇒ 阈值从 3.0 提到 4.5，且压在 `surface` 上而非 `bg` 上）。
- **修掉的真缺陷**：旧 `parse_tokens` 对同名变量**取最后一次出现**，而浅色块写在文件后面
  ⇒ `--check` 实际**只验了浅色主题**，深色从未被算过（666 B1 却声称"深浅两套都过"）。
  667 改为**分主题解析**（`parse_token_blocks`），两套都算。
- 移动端 44px 触控（按钮/输入/下拉/表头/导航链接），WCAG 2.5.8 只要求 24px，本项目按 44 做。

## 3. 数据与验收：怎么复算

```powershell
# ① 数据现算 + 自检 + 漂移比对
.venv\Scripts\python.exe tools\web_verdicts_667.py --selftest
.venv\Scripts\python.exe tools\web_verdicts_667.py --write
.venv\Scripts\python.exe tools\web_verdicts_667.py --check

# ② Python 回归锁（11 例）
.venv\Scripts\python.exe -m pytest tests/test_web_verdicts_667.py -q -p no:cacheprovider

# ③ 前端纯逻辑 Node 真求值（28 条断言）
node tools\web_logic_check_667.mjs

# ④ jsdom 真跑 DOM（23 条断言；本机 Node 18 + jsdom 实测可跑，未 SKIP）
node tools\web_smoke_667.mjs

# ⑤ 管线（schema / 漂移 / 对比度 26 对 / 接线 / 卡片契约）
.venv\Scripts\python.exe tools\web_data_pipeline_656.py --check

# ⑥ 静态检查
.venv\Scripts\python.exe -m ruff check tools\web_verdicts_667.py tools\web_data_pipeline_656.py tests\test_web_verdicts_667.py
.venv\Scripts\python.exe -m mypy tools\web_verdicts_667.py tools\web_data_pipeline_656.py
node --check web\verdicts.js ; node --check web\verdicts_core.js ; node --check web\starmap.js

# ⑦ 本地预览（必须经 HTTP）
.venv\Scripts\python.exe -m http.server 8765 --directory web
```

**实测结果（本批）**：pytest 11 passed · web-logic 28 passed/0 failed · web-smoke 23 passed/0 failed ·
ruff 0 · mypy 0 · `pipeline --check` PASS · `node --check` 全过。

## 4. 判决页**只有 31 条**，这是故意的

判决历史表只收**真正落了逐条 verdict** 的产物：

| 来源 | 条数 |
|---|---:|
| `data/cards_665/index_665.json`（665 B1 机器卡） | 16 |
| `data/defect_injection_661.json`（661 缺陷夹具） | 15 |

**不进表**的（登记在页面「为什么只有这些条目」里，也在 JSON 的 `excluded` 字段里）：

- holdout 30 条、external corpus 40 条：**产物只有聚合计数，没有逐条结果** ⇒ 编不出来，也不编；
- 反事实 10 条：有逐条预测，但**算子已改、产物未重跑**（F1=0.0）⇒ 重跑前不进表。

> 这两条同时是 `docs/667_全量复盘.md` §4.5 的 N1/N6 缺陷。**页面把缺陷显示出来，而不是替它遮掩。**

## 5. 诚实登记：没做到的部分（不许算"已完成"）

1. **屏幕阅读器实测（NVDA/VoiceOver）未做**；全站键盘 Tab 顺序走查未做；200%/400% 缩放重排实测未做；
   axe 自动扫描未做。⇒ **不能声称"WCAG 2.2 AA 通过"**，只能说"能自动验的部分现算通过"。
2. **真浏览器控制台未看**：本机 Node 18，Playwright 要求 ≥20 ⇒ 星图页的 GPU/2D 渲染与新建控件
   **只过了 `node --check` 与 jsdom（判决页）**，星图交互需人工 30 秒复核（见下）。
3. **星图未在 jsdom 里验**：canvas `getContext` 在 jsdom 返回 `null`，starmap.js 会直接崩。
   它的纯逻辑（`graph_core.js`）仍被 655 的检查覆盖；新增的聚类/权重函数**只被 `node --check` 与人工复核覆盖**。
4. **`dist/` 超预算**：666 定的是 <100 KB（13 个资源 92.8 KB）；本批加了两页两模块 ⇒
   **24 个资源 158,305 B → 136,986 B**。未做体积优化（冻结区：不引入打包框架）。
5. **主题切换仍需刷新**：canvas 的颜色在 JS 侧镜像（canvas 读不到 CSS 变量），切换主题后星图要重绘/刷新。
6. **学习页（B4）未继续深化**：自测仍是朴素形态，无错题本 / 间隔重复。
7. **i18n**：仍全中文。

## 6. 人工 30 秒复核步骤（给维护者）

```
1) .venv\Scripts\python.exe -m http.server 8765 --directory web
2) http://127.0.0.1:8765/verdicts.html
   · 大数字是否滚到终值；holdout 那格是否**标红**并带"漂移"提示
   · 点表头"时间"是否切换升降序；搜索 ubsan 是否只剩几行；搜一个不存在的词是否出现**空状态**
   · 切到浅色主题（顶栏"主题"）再看一遍对比度
3) http://127.0.0.1:8765/starmap.html
   · 左下角"渲染："是否 GPU（降级为 2D 也会显式标注）
   · 点一个聚类 chip ⇒ 是否展开成员；勾"连线粗细按权重"再取消 ⇒ 粗细是否变化
   · 搜索 "ATOM-MEM-LEAK" ⇒ 未命中节点是否压暗、命中数是否播报
   · 放大/缩小按钮是否生效
```
