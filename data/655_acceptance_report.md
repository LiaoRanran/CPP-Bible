# 655 验收报告：开源准备 + 判决形式规格 v1 + 门禁三杠杆 + 前端深化

> 任务书：`_auto/inbox/655.md`　｜　批次：655　｜　状态：**awaiting_review**　｜　日期：2026-09-27
> 门禁：**run_655_gate PASS 13/13**（fast / full / ruff / mypy / 许可证头 / 前端产物 / 前端逻辑 /
> 前端 DOM 冒烟 / 三杠杆自检 / 缓存体检 / 保护器联调 / 受控零污染 / 信任根）

## 〇、开工快照与遗留现场（阶段 0）

| 项 | 值 |
|---|---|
| 开工 HEAD | `4f78e14b`（654 收工 + JSON 修复合） |
| 654 收工确认 | `status.json` 654 条目 + `outbox/654.md` + 范围只改前端 ⇒ **已收工** |
| 开工工作区 | 脏 **136**（内容差异 127：tests 62 / data 39 / tools 35）+ 未跟踪 **32** |
| 现场性质（取证） | 修改时间 **09-27 11:24–12:54**，早于 653/654 提交（21:41–22:43）⇒ 属 **650–652 区间遗留**：W2 重算 121→131、卡数 27→37 的写死数字同步；`data/grounded_labels_w2.json` 的 HEAD 版**带 UTF-8 BOM**（`git show` 解析失败），工作区版已去 BOM |
| 处置 | ① `b26ddd38` 基线快照（`data/655_baseline.md`）；② `09edc1d4` **遗留现场入册**（179 文件，独立 commit，标注"非本批产出、未逐条复核"）；③ `data/backup_652/` 与并行进程新产的 `_arch_v35..v38` **不入册**，保持未跟踪 |

## 一、A 开源准备（v34 地基 1）

**提交**：`19b797d9`（协作包）+ `5d3b375f`（许可证头工具与批量加头）

| 交付物 | 状态 | 说明 |
|---|---|---|
| `LICENSE` | ✅ | **MIT → Apache-2.0 全文**（附录版权人保持 `LiaoRanran (阿信)`）；**许可变更已登记为交人项** |
| `DCO.md` | ✅ | DCO 1.1 原文 + `git commit -s` 签署流程 + PR 勾选；**CI 未强制签名**（诚实登记） |
| `CONTRIBUTING.md` | ✅ | 重写：环境 / 两阶段测试约定 / 门禁命令 / PR 流程 / **good first issue 6 条** / 红线 |
| `CODE_OF_CONDUCT.md` | ✅ | Contributor Covenant v2.1 + 私密举报渠道（复用 SECURITY 通道） |
| `README.md` | ✅ | 重写：定位=**可执行知识的验证基础设施** + ASCII 架构图 + 快速开始 + 现状指标 + 路线图（保留 `gen_metrics --check` 锚定的 4 处数字，复核通过） |
| `.github/ISSUE_TEMPLATE/` | ✅ | 新增 **功能请求**、**提问** 两模板；保留既有 bug 报告与内容勘误（4 个模板） |
| `.github/PULL_REQUEST_TEMPLATE.md` | ✅ | 加 DCO 勾选块 + 换成真实命令（tool_integrity / cppbible / ruff / mypy / 许可证头 / 两阶段测试） |
| `tools/license_header_check_655.py` | ✅ | `--check/--report/--apply/--dry-run/--selftest/--json`；保留 CRLF·BOM·shebang·coding 行；幂等 |
| 批量加头 | ✅ | **active 口径 1107 个 `.py` 100% 带 SPDX 头**（`tools/ tests/ web/ Scripts/ conftest.py`） |

**诚实登记（A）**：
1. `all` 口径 = git 跟踪全部 `.py` **1422** 个，其中 **315 个**（`_archive/` 281 + `_adv_*`/`_arch_v*` 34）**未强制**，覆盖率 77.8%，报告 `data/655_license_header_report.{md,json}` 逐文件列出；
   **为何不强行全量**：`Examples/` 属**受控目录**且进 Merkle 根（`data/supply_chain/merkle_roots.json`，其 `.ots` 锚点已欠重锚）——动它会连带改根与锚，故红线优先。
2. 加头**触发 3 处本批引入的回归并已修**（见 §五）。

## 二、B 判决形式规格 v1（v34 地基 2）

**提交**：`5875dd9e`　**产出**：`docs/verdict_formal_spec_v1.md`（规格）+ `tests/test_verdict_spec_v1_655.py`（15 例回归锁）

- **三版本轴**：v0（二态，冻结）/ v0.5（四态+边界三元组，已实现）/ v1（+扩展轴，本规格）。
- **数据模型四域**：D 域内核 `Decision`（10 字段，`decision_id` 确定性）；L 域账本 `DecisionEvent v2`（实测 **452 条 × 25 字段**，`REQUIRED_FIELDS` 8 个）；C 域卡片记录 + **边界三元组**；X 域扩展字段（`conditions[]/partial_atoms[]/conflict_state/conflict_detail/unknown_reason`，全部可选）。
- **状态机**：6 条合法迁移（含冲突保护器 `C≥0.8 ⇒ fail`、人审 `supersedes` 回退）+ 3 类非法迁移（原地改、无新证据的回退、自动回滚）。
- **15 条不变量**，每条给**可测试形式**；已实现的 **11 条**落成单测（INV-1/2/3/5/6/7/8/9/10/13/14），未实现的 4 条明确登记（G-1…G-7 共 7 项缺口）。
- **关键澄清**：判决四态与**卡 status 轴**（`draft/…/verified/rejected`）**正交**（INV-13，实测 23 张 verified 卡全部 `unknown` = 边界缺失）。
- **Rust + Verus 衔接**：§8 给出类型即约束、纯函数契约（`ensures`）、链式归纳不变式与"域判定不进形式化范围"的边界。

## 三、C 门禁三杠杆（v34 地基 4）

**提交**：`93ec93ff`　**报告**：`data/655_gate_levers.md`（口径先定义、数字后给）

| 杠杆 | 实现 | 实测 |
|---|---|---|
| 1 增量选例 | `tools/test_selector_655.py`（git diff → 测试文件；高危面/未归类 **fail-safe 回退全量**） | 5 改动路径 ⇒ 选中 **1/545** 测试文件；跑选中 **15.65 s / 19 例** vs 子集 42.94 s ⇒ **−63.6%**；6 条 fail-safe 自检通过 |
| 2 结果缓存 | `tools/result_cache_655.py`（键 = 用例+**逐文件 sha256**+环境；条目自哈希） | record → **HIT**；改 1 字节 ⇒ MISS（列漂移文件）；手改条目 ⇒ **拒绝采信**；`--verify` 报篡改 |
| 3 分片 | `tools/pytest_shard_655.py`（LPT 按**整模块**）+ `tests/conftest.py` 新增 `--shard-id/--shard-count`（**默认 0 = 关闭**） | 3220 例四片精确划分 **780/809/818/813**、模块集合**零重叠**；LPT 不均衡 **1.0006** vs 轮转 1.1234 |

**诚实登记（C）**：
1. **未达成"全量 fast 砍 30-50%"**：全量 fast 实测 **3210 例 / 634.3 s**（junit）/ **636.7 s** 墙钟；三杠杆消除的是**重复劳动**，不是单次全量成本（详见报告 §五.2）。任务书所述"15.4 s"经复测对应**子集口径**（653 门禁口径实测 18.02 s）。
2. **发现 junit 时长口径缺陷**：`pytest-xdist` 的 `testcase@time` 是**累计失真**（3210 例求和 9196 s ≫ 套件自报 634 s，比值 14.5），计划表已内置 WARN + `caveat` 字段；正确口径为 `--durations=0 -n0`（`--durations-text` 已支持）。
3. 本批真实 diff（1107 个加头文件）下选择器**回退全量**——设计使然（用保守换正确）；提高命中率需 AST 级依赖图（列 656+）。

## 四、D 前端深化（v32 P1）

**提交**：`9cc5772c`　**门禁**：`web_assets` + `web_logic`（Node 真求值 22 断言）+ `web_smoke`（jsdom，缺则 SKIP）

| 要求 | 实现 | 验证 |
|---|---|---|
| 星图 hover 显示卡片标题/四态/credibility | `starmap.js` 卡片化 tooltip（+攻/防/被击败计数、`点击固定详情` 提示） | 语法 + 逻辑（`graph_core.statsOf` 对 178 节点逐节点暴力对账 **0 不一致**） |
| 点击节点**固定详情面板** | 新增 `<aside id="detail">`：id / 类型 / 四态 / credibility / domain / 卡状态 / 命题数 / **受攻击·发出攻击·防御清单**（含"被击败"标签）；再点空白取消 | `__starmap_hooks.select(i)` ⇒ 断言面板含 id/四态/credibility/攻防计数 |
| **边 hover** 显示攻击/击败关系 | 最近边拾取（点到线段距离 + 阈值 7px）+ 边缘高亮 + tooltip（kind/击败状态/两端类型与四态） | 几何 4 例解析断言 + 拾取 4 例（含 `passLink` 过滤） |
| landing 首屏会动 + **系统现状面板** | 数字**滚动动画**（尊重 `prefers-reduced-motion`）+ 现状面板：**37 卡（+10 draft）· 67 规则（block 44）· 9 保护器 · 逃逸 1/1406 = 0.0711%** | 数字全部来自 `web/data/status.json`（由 `tools/web_status_655.py` **现算**，缺项标 null + `unavailable`） |
| 验哈希**批量** + **CSV 导出** | 多文件拖入/多选 ⇒ 批量结果表 + 汇总（一致/不一致/无台账）+ 导出 CSV（BOM + RFC4180 转义） | CSV 表头/行数/引号转义/判定列 + 16 条台账哈希**现算复现** |
| 暗色克制、不加光斑粒子 | 只加面板/表格/标签样式，无渐变光斑/粒子 | 人工样式审查 |
| 用真实数据、不造演示数据 | 新增 `tools/web_status_655.py`（数字现算）+ 星图首屏描述改为**现算文案**（不再写死 178/388/194） | `status.json` 与 `graph.json` 对账断言（Node） |

**新增验证能力（本批附带）**：`tools/web_logic_check_655.mjs`（Node 18 可跑，**真求值**纯逻辑层
`web/verify_core.js`、`web/graph_core.js`）+ `tools/web_smoke_655.mjs`（jsdom **跑整页 DOM 交互**；
本机 Node 18 + 受管 jsdom 因 `@exodus/bytes` ESM 不兼容而 **SKIP**，非"假绿"——输出明确 SKIP 原因）。

**顺带修的真实漂移**：`.tool_checksums` 因 A/C 重钉后，`web/data/manifest.json` 里该文件的
sha256 陈旧 ⇒ **被前端逻辑检查当场抓出** ⇒ 重生成 graph/manifest（`web_data_653 --build`，自检 PASS，653 单测 5/5 过）。

## 五、E 收工与验证

### 5.1 门禁

`python tools/run_655_gate.py` ⇒ **PASS 13/13**：
fast / full / ruff / mypy（本批 6 工具）/ 许可证头（active 0 缺）/ 前端产物 / 前端逻辑 / 前端 DOM 冒烟 /
三杠杆自检 / 缓存体检 / 保护器联调（`mode_switch_effective` = 4 个，`not_effective` = 0）/
受控 atoms 指纹一致（`72b6eacef0112dd0`）/ 信任根 `--check` 4 节 OK。

### 5.2 两阶段 pytest（全量，实测）

| 阶段 | 例数 | 失败 | 跳过 | 时间 | 口径 |
|---|---|---|---|---|---|
| fast（`-m "not slow" -n auto`） | 3210 | 47 | 7 | junit 634.3 s / 墙钟 636.7 s | `data/655_junit_fast.xml`、`data/655_fast.txt` |
| slow（`-m slow -n0`，**按 4 片串行**） | 844 | 48 | 7 | junit 2381.6 s / 墙钟 2388.7 s | `data/655_slow_shard{0..3}.xml` |

**失败归因（逐条取证，结论：655 引入失败 = 0）**

| 类别 | 数量 | 取证方式 |
|---|---|---|
| 本批引入并**已修** | fast 3 例 → 0 | 基线工作树（`git worktree` @ `09edc1d4`）对照：3 例在基线**绿**、本批**红** ⇒ 定位并修复（见 §5.3） |
| 预存在（遗留数字漂移 / 陈旧门禁断言 / 环境） | fast **44** + slow **40** | 47 例中 44 例在基线工作树**同样红**；slow 侧失败消息直接指向 27↔37 卡、121↔131 节点、79↔89 命题、`断言 push 后 ahead=0`、`629 新增工具交叉核验`、路径过长 `WinError 206` 等**预存在**问题 |
| 本地陈旧 build 产物 | slow **7** | 605×4 + 606×2 + guard_hijack×1 全部指向 `build/replay_manifest.json`（**gitignored**）记录的卡指纹与现盘卡+夹具不符；**655 全程未改 `evidence/ atoms/ Examples/ Book/`**（`git diff 4f78e14b..HEAD -- evidence/ atoms/ Examples/ Book/` **为空** ⇒ 指纹输入未变）；移开该产物后 **7 例全绿**，检查走 "manifest not found, skipping" 中性分支 |
| 环境依赖（manifest 缺失时 608 断言 KeyError） | slow **1** | 同一用例在基线工作树**同样红**（`tests/test_replay_invariants_608.py:151 KeyError`） |

**处置**：陈旧 `build/replay_manifest.json` 已移档为 `build/replay_manifest.json.bak655`
（**gitignored 本地产物**，不入库；移档 = 恢复"干净克隆/CI"的中性状态，非隐藏问题）。
根治办法（交人）：`python tools/atom_evidence_replay.py --rebuild-manifest`（56 张卡真编译，耗时较长）。

### 5.3 本批自纠与自纠明细（全部已修）

| # | 问题 | 根因 | 修复 |
|---|---|---|---|
| 1 | `test_oracle_rotation_583` / `test_prop_asof_583` 源码只读断言变红 | 两例用 `raw.startswith('#!/usr/bin/env python3\n"""')` 判 docstring；**许可证头插在 docstring 之前** ⇒ 判定失效 ⇒ 把 **docstring 里描述禁令的词**（`gate_engine.run`、`open(`）当成代码扫到 | 两处改为"先剥 shebang + 前导注释行，再剥 docstring"（保持原意，只修脆弱假设） |
| 2 | `test_mypy_fix_625::test_mypy_tools_clean` 变红 | 新工具 `result_cache_655.py` 有 **9 处 mypy 错误**（`no-any-return` / 未注解 dict） | 修注解与 `json.loads` 的 `Any` 收口；`mypy tools/` ⇒ **Success: no issues found in 560 source files** |
| 3 | `web/data/manifest.json` 台账哈希陈旧 | A/C 两次 `tool_integrity --update` 改了 `tools/.tool_checksums` ⇒ 台账失配 | 重生成 `web/data/{graph,manifest}.json`（真数据），653 单测 5/5 复绿 |
| 4 | **HEAD 里的 `tools/.tool_checksums` 是旧值**（conftest 已改但基准未随之提交） | C 提交时只 `git add` 了指定路径，漏了 `.tool_checksums` ⇒ **干净克隆会被 `--check` 判红 / 测试拒跑** | 收工前审查 `git status` 发现 ⇒ 本批 E 提交补齐（这正是该机制要防的事） |

### 5.4 全新检出复核（本批新增的一道"外部视角"检查）

在 `git worktree` 里对**收工 HEAD（`a4308def`）做全新检出**，再跑门禁核心：

| 检查 | 结果 |
|---|---|
| 本批测试（`test_655_tools.py` + `test_verdict_spec_v1_655.py`，34 例） | ✅ 全绿（`pytest_configure` 的 `--check-test-config` 也通过） |
| `tool_integrity --check` | ⚠️ **红**：merkle 段（atoms / evidence / data/mutation 根不匹配）+ ruler 段（个别被钉工具"被改动"） |

**归因（预存在，非 655 引入）**：
- 根因是**工作区 CRLF ↔ 索引 LF 的历史漂移**（`.gitattributes` 的 `* text=auto eol=lf` + 2026-09-13 监工裁决"暂不 renormalize、碰到即转"）。
  本机工作区当前有 **1872 个文件是 CRLF**（`git ls-files --eol`：Examples 565 / data 682 / evidence 67 / atoms 23 / tools 27 / web 50 …），
  而 Merkle 根与被钉工具的 sha256 **都是对工作树字节算的** ⇒ 换成 LF 的全新检出必然对不上。
- **证据 1**：655 全程**未改** `data/supply_chain/merkle_roots.json`（git diff 为空）与 ruler 段；`--update` 两次重建后与 HEAD 逐字节一致。
- **证据 2**：把 655 **开工前**的提交 `09edc1d4` 也做全新检出并跑同一命令 ⇒ **同样红**（ruler 段 5 处 + merkle 段）⇒ 预存在。
- **证据 3**：本仓工作区（CRLF）跑同一命令 ⇒ **PASS**（这是 5.1 里 PASS 的原因，也是"本地绿、克隆红"的由来）。
- 影响面：CI 不跑 `tool_integrity --check` 全量（只跑 `--check-test-config`），故 CI 不受影响；**本地 clone 的维护者会看到红**。
- 本批新增文件（`DCO.md`、`docs/*`、`web/*.js` 等）也落在 CRLF 侧，但**不在被钉/被 Merkle 覆盖的范围**，无门禁影响。
- 处置：**不改**（一次性 renormalize 会淹没真实改动，且属 2026-09-13 已裁决事项）⇒ 登记为交人项 §六.9。

### 5.5 红线守护（自我声明，均有器械证据）

- **未改** `CORE_TOOLS` 判决逻辑、**未改** 67 条规则、**未改**历史账本（`data/authority/*.jsonl`）、**未改**受控内容目录
  （`atoms/ evidence/ Examples/ Book/` 在 655 全程零 diff，含 5.2 的取证命令）；
- **未代签**、**未 golden accept**、**未 push**（`origin/master..HEAD` = 34 commit，含 655 的 7 个）；
- 受控 atoms 指纹门禁前后一致；保护器联调零漂移；信任根 `--check` 4/4 OK；
- 工作区非本批产物：`_arch_v35..v38`（并行进程调研）、`data/backup_652/`、`data/evidence_store/` 新分片 —— **未触碰、未入册**。

## 六、交人项

1. **MIT → Apache-2.0 是否最终确定**（涉及历史 release 的许可口径；本批按任务书执行）。
2. **DCO 是否上 CI 强制**（现状：文档 + PR 勾选；若强制需对历史 commit 批量 `--signoff`）。
3. **许可证头存量迁徙**：`all` 口径尚缺 315 个（`_archive/`、调研脚本）——是否补，或改用 `--scope all` 常驻门禁。
4. **`build/replay_manifest.json` 根治**：是否执行 `--rebuild-manifest`（56 卡真编译，耗时）。
5. **slow 相 40 个预存在失败**的处置：绝大多数是 650–652 遗留的**数字漂移**（27→37 卡 / 121→131 节点 / 79→89 命题）在各批门禁断言里的残留，建议独立批次统一"去写死"。
6. **门禁三杠杆接入 CI**：是否在 CI 用 `--shard-id/--shard-count` 矩阵、是否用 `result_cache` 短路未变更重跑。
7. **jsdom 环境**：本机 Node 18 + 受管 jsdom 的 `@exodus/bytes` ESM 不兼容 ⇒ `web_smoke_655.mjs` 只能 SKIP；CI 若用 Node ≥20 可开启真 DOM 冒烟（同因也使 `tools/mermaid_parse_check.mjs` 在本机不可跑——预存在问题）。
8. 是否 push（现状 ahead = 34）。
9. **CRLF 漂移的收口**（§5.4）：本机工作区 1872 个 CRLF 文件使"全新检出"下 `tool_integrity --check` 必红
   （merkle + ruler）；根治需一次性 `git add --renormalize` + 在 LF 工作副本上重钉 `.tool_checksums` + 重建 Merkle 根 + OTS 重锚 ——
   属 2026-09-13 已裁决"暂不 renormalize"的跨批事项，本批只登记不改。

## 七、产物清单

- 文档：`LICENSE`、`DCO.md`、`CODE_OF_CONDUCT.md`、`CONTRIBUTING.md`、`README.md`、`docs/verdict_formal_spec_v1.md`
- 模板：`.github/ISSUE_TEMPLATE/{feature_request,question}.md`、`.github/PULL_REQUEST_TEMPLATE.md`
- 工具：`tools/license_header_check_655.py`、`tools/test_selector_655.py`、`tools/result_cache_655.py`、
  `tools/pytest_shard_655.py`、`tools/web_status_655.py`、`tools/web_logic_check_655.mjs`、
  `tools/web_smoke_655.mjs`、`tools/run_655_gate.py`
- 前端：`web/{index,starmap,verify}.html`、`web/{starmap,verify}.js`、`web/{verify_core,graph_core}.js`、
  `web/style.css`、`web/package.json`、`web/data/status.json`（+ 重生成 graph/manifest）
- 测试：`tests/test_655_tools.py`（19 例）、`tests/test_verdict_spec_v1_655.py`（15 例）、`tests/conftest.py`（分片选项）
- 数据/报告：`data/655_baseline.md`、`655_license_header_report.{md,json}`、`655_gate_levers.md`、
  `655_test_selection.json`、`655_shard_plan.json`、`655_result_cache.json`、`655_junit_{fast,subset}.xml`、
  `655_slow_shard{0..3}.xml`、`655_{fast,durations_subset}.txt`、`655_{failed_ids,slow_failed_ids}.txt`、
  `655_base_failed_rerun.xml`、本报告

---
_655 收工：13/13 门禁 PASS；诚实登记 7 项交人 + 4 项自纠 + 两阶段 pytest 失败逐条归因（655 引入失败 0）。_
