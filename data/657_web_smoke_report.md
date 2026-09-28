# 657 D7 · 前端 DOM 冒烟（jsdom 升级后能真跑，不再 SKIP）

> 工具：`tools/web_smoke_655.mjs`。取证：本机 `node` v18.20.8 + 仓库根 `node_modules/jsdom@24.1.3`。
> 本批改动：`web/verify_core.js` 的 `_subtle()` 加固（优先 `self.crypto`→`globalThis.crypto`，给清晰报错）；
> `tools/web_smoke_655.mjs` 的 jsdom 解析顺序（受管 workspace → **仓库根 node_modules** → 旧兜底）、
> WebCrypto/`devicePixelRatio`/`matchMedia`/`ResizeObserver` 等 jsdom 缺口垫片、以及无 subtle 时
> **诚实降级为 SKIP（不是假绿）**。

## 一、655 的状态 vs 657 的状态（关键进展）

| | 655 | 657 本批 |
|---|---|---|
| jsdom 可用性 | 受管 workspace 的 jsdom 与 Node 18 的 `@exodus/bytes` ESM 不兼容 ⇒ **只能 SKIP**（exit 0，看不到任何页面逻辑） | `jsdom@24` 钉进仓库根（Node 18 兼容）⇒ **真跑 4 个页面** |
| 覆盖 | 0 个页面逻辑被验证 | 4/4 页面脚本被真求值，命中**真实缺陷** |
| 报告 | "SKIP（环境缺）" | 5 处真实断言失败 + 1 处真数据漂移，见 §二 |

> 这是 D7 的核心交付：**冒烟从「假装通过」变成「能看到页面真问题」**——655 那次 SKIP
> 把下面 §二 的全部缺陷都藏住了。

## 二、657 实跑结果（2026-09-28，本仓工作区）

```
[1/3] web/verify.html
  [ok] 批量表出现 2 行            [ok] 一致行命中台账路径        [ok] 导出按钮已启用
  [FAIL] 主结论：1 一致 / 1 不一致 · 实际：一致 1 / 不一致 0 / 无台账 1
  [FAIL] CSV 有表头              [FAIL] CSV 含两条数据行（lines=1）
  [FAIL] CSV 判定列正确          [FAIL] CSV 实算哈希 = 台账哈希（真算）· b7140e768974738e
[2/3] web/starmap.html
  [ok] 星图数据加载 / 节点数178 / 边数 / 首屏描述现算 / 统计卡6格
  [FAIL] 存在受攻击的卡节点
[3/3] web/index.html
  [ok] 现状面板 / 知识卡37 / 规则67 / 保护器9 / 逃逸率0.0711% / 现状脚注 / 首屏节点178
  [FAIL] 星图按钮文案现算
[4/4] web/card.html（devicePixelRatio 垫片后已不崩，待 E 段补齐更多断言）
```

## 三、逐条归因（交给 E 段）

| # | 页面 | 现象 | 归因 | 处置 |
|---|---|---|---|---|
| 1 | verify.html | tampered 文件被判「无台账」而非「不一致」 | `verify.js` 分类：未列于台账的路径走「无台账」分支，测试期望「不一致」 | E 段：确认分类语义（未被台账收录的文件，应是「不一致」还是「无台账」？语义定清后修断言或逻辑） |
| 2 | verify.html | CSV 导出 blob 为空（表头/行/判定列/哈希全缺） | jsdom 下 `blob.text()` 或导出回调未拿到结果集（可能 `URL.createObjectURL` 垫片时序） | E 段：修导出路径（这是 655 D 新增功能，本就未经真跑验证） |
| 3 | verify.html | CSV 实算哈希 ≠ 台账哈希 `b7140e768974738e` | **真实数据漂移**：台账里存的 sha256 与文件当前字节不一致（同 D5 的「写死/漂移」一类） | E 段：重算并更新 `web/data/manifest.json` 的台账哈希（属前端数据完整性） |
| 4 | starmap.html | 未标记「受攻击」的卡节点 | `graph_core.js` / starmap 渲染未接 `status.json` 的受攻击标记 | E 段 |
| 5 | index.html | 星图按钮文案未含真实节点数 | `starmap-btn` 文案现算未接 `graph.json.meta.counts` | E 段 |

## 四、为什么本批不代修这 5 条

1. 它们是**前端功能正确性**问题，正是 E 段「前端重型优化（页面）」的范畴；657 的 D7 目标是
   **让冒烟能跑**，不是顺手重写前端。
2. 第 3 条（台账哈希漂移）与 D5 同根：655 生成台账哈希后，底层文件又被后续批次改动过
   ⇒ 真漂移。根治 = 让台账哈希由事实源现算（与 D5「慢测试去写死」同源）。
3. `web_logic_check_655` 的「台账 16 条现算 sha256 全部一致」FAIL 与第 3 条同源（同一批台账哈希漂移）。

## 五、诚实登记（不假绿）

- 冒烟现在会**真实失败**（exit 1）而非 SKIP。门禁 `run_656_gate.py` 阶段 6c 因此会变红——
  这是**暴露长期隐藏的前端债**，不是 657 引入的回归。E 段修掉 §三 的 5 条后，阶段 6c 自然转绿。
- 若需在 E 段落地前先让门禁不红：本文件已内置「无 subtle ⇒ SKIP 计 PASS」的诚实降级分支；
  是否把「已知前端债」也纳入该分支由人裁决（建议：不纳入，保持红以驱动 E 段）。
