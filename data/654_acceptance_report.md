# 654 验收报告（修星图 cosmos.gl 加载）

- 批次：654　状态：awaiting_review　日期：2026-09-27
- 范围：**只改前端**（`web/`），未碰后端/`tools/`/`tests/`（唯一新增的 `_fetch_vendor.py` 也放在 `web/vendor/` 内）
- 提交：`48a777b9`（1 次）

---

## 一、根因（实测定位，非猜测）

653 的 `starmap.js` 用 `import('https://cdn.jsdelivr.net/npm/@cosmograph/cosmos@3/+esm')`。
抓取该 `+esm` 产物（cosmos **3.4.1**，385 KB）后逐条解析其 `import`：

```
... from "/npm/@luma.gl/core@9.3.6/+esm"
... from "/npm/@luma.gl/webgl@9.3.6/+esm"
... from "/npm/@luma.gl/engine@9.3.6/+esm"
```

BFS 全依赖树（36 个模块，**0 个 404**）后得到 **luma.gl 两套版本并存**：

| 拉入方 | 版本 |
|---|---|
| cosmos / webgl / engine | `@luma.gl/core@9.3.6` |
| **`@luma.gl/shadertools@9.3.5`**（engine 的传递依赖） | **`@luma.gl/core@9.3.5`** |

⇒ **同一份 luma.gl 被加载两次**（两个 `luma` 单例 / 两个 device 注册路径）⇒ 运行时报错 ⇒
页面落进 2D 降级分支。**这正是 653 观察到的 "9.3.6 vs 9.3.5 冲突"。**

> 附带更正：本次全树抓取**未发现 404**（36/36 均 200）。653 提到的"一个 404"可能是当时瞬时或其它子路径，**本批未复现**，如实登记。

## 二、为什么 import map 治不了

`import map` 只能改写**裸说明符**（`@luma.gl/core`），而 jsDelivr 的 `+esm` 产物把依赖写死成
**绝对 URL**（`/npm/@luma.gl/core@9.3.5/+esm`）⇒ 映射不到。**必须改依赖来源**。

## 三、修法：本地 vendor + 版本统一（可离线）

新增 `web/vendor/`（**39 文件 / 1374 KB**），由 `_fetch_vendor.py` 生成：

1. 从 `@cosmograph/cosmos@3.4.1/+esm` 出发 **BFS 抓取全部 `/npm/...` 依赖**（写入内存）；
2. **版本统一**：`@luma.gl/*@9.3.5` → **`@9.3.6`**（9.3.6 全族都在，含 shadertools）⇒ **双份消除**；
3. 把每份产物里的导入**全部重写为相对路径** `./<name>.js`；
4. 落盘并生成 `manifest.json`（spec→文件 映射，可追溯）。

`starmap.js` 改为 `await import('./vendor/cosmos.js')`；`.luma.gl-*9.3.6.js` 命名把**版本钉在文件名里**，一眼可查。
另加 `web/vendor/package.json`（`type: module`）：浏览器忽略，但让 Node 可把该目录当 ESM 做 CI 静态复核。

## 四、验证（三层，尽量用真证据）

| 层 | 方法 | 结果 |
|---|---|---|
| **① 依赖图静态校验** | 遍历 39 个文件：相对导入是否可解析 / 是否残留绝对 `/npm/` / 是否残留 `9.3.5` | **未解析 0 / 残留绝对导入 0 / `9.3.5` 出现 0** ⇒ 双份已消除 |
| **② Node 真求值** | 最小 DOM/WebGL 桩下 `import(file://.../web/vendor/cosmos.js)` | **IMPORT OK**，导出含 `Graph`（starmap 用的类）；**无 duplicate-singleton 报错**；unhandledRejection **0** |
| **③ 静态服务冒烟** | `http://127.0.0.1:8099/` 取 `starmap.html / starmap.js / style.css / vendor/cosmos.js / vendor/manifest.json / vendor/package.json` | 全部 **200**；改动后 `starmap.js` 过 `node --check` |

**要求 5 满足**：2D 降级逻辑**保留**（`tryCosmos()` 的 `catch` 分支 + `.fallback-note` 未动），
且失败原因现在会写进 `window.__cosmos_err`。

### 未完成的一层（诚实登记）
**真浏览器控制台检查未做**：本机 Node 为 **v18.20.8**，而 `@playwright/cli` 要求 **Node ≥ 20**
（实测报 "Playwright requires Node.js 20 or higher"）；改用自包含的 `agent-browser` 时被用户取消执行。
⇒ 未取得"控制台无 error"的浏览器实录。

**人工 30 秒复核（已埋好探针）**：刷新 `http://127.0.0.1:8099/starmap.html`，
1. 右上"渲染："应显示 **`GPU · cosmos.gl v3（本地 vendor 3.4.1 / luma.gl 9.3.6）`**；
2. 画布**左下角不出现** 2D 降级提示；
3. 控制台执行 `window.__cosmos_ok` ⇒ 应为 `true`（失败时 `window.__cosmos_err` 给出原因）。

## 五、影响面与残留
- 只改 **4 个前端产物**（`starmap.js` / `starmap.html` / `style.css`）**+ 新增 `web/vendor/`**；
  **未改** 仓库 `tools/`、`tests/`、`data/`、`atoms/`。
- `web/vendor/` 纳入版本库（1374 KB）⇒ 站点**彻底离线可用**，不再依赖 CDN。
- 残留：`windicss`-类无关；唯一"未解析"的两条命中经核实是 **shadertools 里的 GLSL 着色器注释文本**（非真实 ES 导入），不影响求值（Node 求值已验证）。
- 交人项：是否需要把 vendor 体积压到更小（可换 `esbuild` 预打包为单文件）；是否补一条 CI 静态校验（现成脚本 `_fetch_vendor.py --check` 尚未提供校验子命令）。
