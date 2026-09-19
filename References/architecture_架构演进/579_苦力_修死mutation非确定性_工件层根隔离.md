# 579 · 建设任务书：修死 mutation 跑批非确定性——根因是"工件层没进沙箱"，不只是 manifest

> 基线：HEAD 为 578 收尾后；v5 清态权威值 **989/9/185（严格 619）、M5 29/0/56、M6 324/8/0**，
> 已由 `_rep578.log` 两次清态逐算子一致证实，**数字不改**。本批只修"尺子会抖"，不改任何判定规则。

## 监工独立复核结论（比 578b 自查更深一层，先读这段再动手）
578b 已证：清空 `build/replay_manifest.json` 后两次全量逐字一致；脏 manifest 跑出 991/7 离群。
但 578b 的 M1 规格（只把 manifest 指到 tmp）**必要不充分**。监工读码钉死了它标【未实证】的机制：

**`mutation_fuzz.sandbox()` 只重定向了卡文本目录（`ge.ATOMS/ge.EVIDENCE → tmp`），所有工件层读写仍打在真实仓库：**
- `gate_engine.py:38` `ROOT` 是模块级常量，sandbox 不换它；
- EV-ARTIFACT-FILE-EXISTS 约 `:2627` 用 `(ROOT / r).is_file()` 查**真实工件存在性**；
- EV-ASSERT-SYMBOL-MAPPED 约 `:1742` 用 `f = ROOT / rel; f.read_text()` 读**真实工件内容**；
- replay：`art_path = ROOT / art_rel`（约 1420）、extra_arts 同样 `ROOT/...`、`(ROOT/"build").mkdir`（1487）、
  `run_commands(..., ROOT, ...)`（cwd=ROOT）、`MANIFEST = ROOT/"build"/"replay_manifest.json"`（1745）。

⇒ 跑批期间 M1/M7 变体的 replay 在**真实工件**上 unlink→重编译→备份还原、写真实 `build/`、读真实 manifest；
后续 M6 变体的 gate 全库扫描又用 ROOT 查这些真实工件。034 的 finding 抖，是因为它的**真实工件**在某次
M1/M7 replay 的删-建窗口 / build 残留 / manifest 复用决策下处于非常态，被 028/029 的 M6 gate 读到——
**不是 034 的 .md 卡文本变异**（finally 已还原）。578b 三次探针在沙箱卡文本里找，所以复现不到。

架构已预留一半：`card_fingerprint(card, calc_root=None)`（1755–1760 `root = calc_root or ROOT`）支持重定向根，
但 replay_card 的 art_path/build/manifest 与 gate 两条工件规则还没接通。**这套根重定向同时就是 560 B2
"卡间隔离并行"要的同一机制**（replay 注释 1865：每 worker 独立 `build_<pid>`）——一次施工两处收益。

---

## 任务 1（根因修复）：工件层根隔离，让跑批对真实 ROOT 零副作用

**做法（推荐方案 A，彻底）**：
1. 引入显式"跑批根"（优先 contextvar 或函数参数，**不要**全局 monkeypatch），默认值 = 真实 ROOT，
   保证所有现存 CLI / 测试行为逐字不变（存量零误伤的硬前提）。
2. 把根重定向从 `card_fingerprint` 贯通到：
   - replay：`art_path`、`extra_arts`、`build/`、`MANIFEST`、`run_commands` 的 cwd；
   - gate：EV-ARTIFACT-FILE-EXISTS、EV-ASSERT-SYMBOL-MAPPED（审计其余所有 `ROOT/...` 用法，
     区分"该跟随跑批根的工件路径"与"必须留真实 ROOT 的工具自身配置"，列清单写进 worklog）。
3. `mutation_fuzz.sandbox()` 进沙箱时：把真实 `evidence/`（**含 actual 工件**）整树复制进 tmp，
   激活跑批根 = tmp，给一个**空的 tmp/build**；M1/M7 replay 的编译/manifest/工件全部落在 tmp，跑完 rmtree。
   卡文本与工件在同一个 tmp 根内自洽，gate 任何规则都读不到真实仓库的瞬态。

**不接受方案 B（仅 manifest 指 tmp + 备份还原真实工件）作为收尾**：它仍在真实工件上删建，时序窗口不消除。
若方案 A 改动面经审计确实过大，可先交 A 的最小子集（manifest+build 进 tmp）并在 worklog 明确残留窗口，
但必须标注"非确定性未根除、--selfcheck 仍可能红"，由监工裁决是否接受。

## 任务 2（验收闸门，把 578b 的②反向因果融进测试）
- 新增 `mutation_fuzz --selfcheck-determinism`：跑完对关键子集（至少含 M6 全卡 + 每张有 M1/M7 的卡）
  立即重跑一次，逐变体比对 `(verdict, new_block, new_warn)`，不一致 **fail-loud** 并打印"哪张卡哪条 finding 抖了"。
- 正反例 pytest：
  - **反例（锁旧病，旧代码必红）**：预先把 manifest 填脏（塞异源/真卡条目）并在 build 留残留产物，
    连续两次跑同一子集，断言逐字段一致——旧代码会因继承状态抖而红。
  - **正例（新代码必绿）**：方案 A 隔离后，同样"脏 manifest + build 残留"预置下两次逐字一致；
    且断言跑批前后真实 `evidence/**/actual`、`build/replay_manifest.json` 字节不变（真实 ROOT 零副作用）。
- 修完重跑全量：清态与预置脏态都必须 = 989/9/185 逐算子一致（数字不因修复而变，只消除抖动）。

## 任务 3（报告诚实性，便宜）
- `metrics_collector` / 基线 README 给全量逃逸率加 tag：**"点估计含运行间方差（实测 ≥2/998）；
  C-P 区间只覆盖抽样误差，不覆盖跑批非确定性"**。确定性修好、--selfcheck 稳定 N 轮后再撤该 tag。

## 任务 4（M2，独立小项，可同批可另开）
- `_META_CACHE/_FM_CACHE` 注释收紧（gate_engine.py:198 那句"不存在窗口"过强，实测同尺寸改写 0ms 间隔 9/12 相撞）；
- 加 O(1) `invalidate(path)`，规定进程内改盘必须调用，配"写同尺寸→invalidate→读到新值"正反例。
- gate 属 CORE_TOOLS：本任务同 commit `tool_integrity.py --update` 重钉，带 .tool_checksums，复跑 gate/poison/replay/fast/slow。

## 收工门禁（fresh）
- `pytest -m "not slow" -n auto` exit 0；`pytest -m slow -n0` exit 0（仅 golden_lock 那 1 个待人 accept 的预期红除外）；
- gate 仍 63/191 block=0 warn=186（命中数不变）；poison 118/118；replay confirm=56；
- tool_integrity --check exit 0；受控目录 + **真实 build/manifest** 跑批前后零差异；
- 一任务一 commit；不编数字，跑多少报多少；做不完停任务边界、施工点写 `_worklog_579.md`。
