# 655 阶段 0 · 基线快照

> 任务书：`_auto/inbox/655.md`（开源准备 + 判决形式规格 v1 + 门禁三杠杆 + 前端深化 + 收工）。
> 本文件只记录**开工时刻的实测事实**，不做判断、不修数据。

## 一、开工快照

| 项 | 值 | 取证 |
|---|---|---|
| 仓库 | `C:\CodeLearnling\note\note\C++\CPP-Bible` | — |
| HEAD | `4f78e14b`（2026-09-27 22:43:08 +0800，"654 修 JSON：status.json 654 条目引号"） | `git log -1` |
| 未 push | `origin/master..HEAD` = **27** commit | `git rev-list --count` |
| 工作区 | **脏 136**（有内容差异 127；`tests/` 62 + `data/` 39 + `tools/` 35）+ **未跟踪 32**（`data/` 23 + `_arch_v31..v34` 目录与 brief 9） | `git status --porcelain`、`git diff --numstat` |
| 姊妹仓 | `C:\CodeLearnling\note\note\queyi-core`（保护器 5×647 + 4×649 均在此） | 逐文件 `Test-Path` |

## 二、654 收工确认

- `_auto/status.json`：`state=awaiting_review`、`active_batch=654`、`last_completed_batch=654`、`history` 末条为 654 ✅
- `_auto/outbox/654.md` 存在（收工报告，含"真浏览器控制台检查未做 + 人工 30 秒复核步骤"）✅
- 654 范围为**只改前端**（`web/`），未碰 `tools/`、`tests/`、后端 ✅
- 结论：**654 已收工**，655 可开工。

## 三、现状指标（本机实测，非引用）

| 指标 | 实测值 | 取证命令/文件 |
|---|---|---|
| 原子卡 | **47** 张 = 37 张实卡（`conc 3 / hist 1 / lang 8 / mem 23 / ub 2`）+ 10 张 `atoms/draft650/` | `atoms/**/ATOM-*.md` 计数 |
| 卡状态分布 | `verified 23 / red-team-verified 3 / draft 21` | 逐卡 frontmatter `status:` |
| 规则 | **67** 条（其中 `severity=block` 44 条） | `import gate_engine; len(gate_engine.RULES)` |
| 保护器 | **9** 个（`conflict_detector / anti_windup / blind_protocol / calibration_tracker / mdl_gate` = 647 真上岗 5 个；`tool_gate / shadow_mode / circuit_breaker / budget_guard` = 649 4 个） | `queyi-core/tools/*.py` 逐个存在 |
| 逃逸率 | **1 / 1406 = 0.0711%**（v7 基线；CS anytime 上界 0.9062%） | `data/616_baseline.md`、`data/629_acceptance_report.md` |
| W2 接地模型 | **131 节点**（IN 89 / OUT 42 / UNDEC 0）= 121 + 10 张 draft650 | `data/grounded_labels_w2.json`（工作区版） |
| 前端星图 | 178 节点（47 卡 + 89 命题 + 42 误解）/ 1093 边（attack 388 / defend 616 / asserts 89）/ 击败边 194 | `web/data/graph.json` `meta.counts` |
| 信任根闭包 | `.tool_checksums` 4 节 **34** 条（core 5 / test_config 2 / supply_chain 5 / ruler 22） | `tools/.tool_checksums` |
| pytest 基线（历史产物） | fast 2833 例 / 347.1 s；slow 1001.8 s（643 口径，`data/643_pytest_two_phase.json`） | 同上 |
| 663 批次规模 | `tools/` 556 `.py` + `tests/` 544 `.py`（tracked 合计 1423 `.py`，含 `_archive/` 281） | `git ls-files '*.py'` |

## 四、开工遗留现场（非本批产出）

**发现**：工作区有 136 个已跟踪文件被改动 + 32 项未跟踪，修改时间集中在 **2026-09-27 11:24–12:54**，
早于 653/654 的提交时间（21:41–22:43）⇒ 属 **650–652 区间的遗留现场**，651/652/653 三批报告均登记为
"未触碰、未提交"。

**性质（抽样取证）**：
- `data/grounded_labels_w2.json`：HEAD 版**带 UTF-8 BOM**（`git show HEAD:… | python -m json` 解析失败），
  工作区版无 BOM 且已含 draft650 的 10 个节点（121 → 131）；`data/*baseline*`、`data/646_rule_card_mapping.*` 等
  报告同步为 37 卡口径。
- `tools/`（35 个）、`tests/`（62 个）：把写死的 W2 数字（121 / 27 卡 / 195-1175-270 强度分布）
  同步为现值（131 / 37 卡 / 206-1575-370）。样例：`tools/defense_chain.py` 文档串 121→131、
  `tests/test_w2_authority_640b.py` 断言 121→131。
- `data/640_auto_executor_log.jsonl`：追加的是**测试夹具**记录（`auto_exec_fixture_*` 临时目录），非生产修复。

**处置（655 阶段 0）**：以**独立 commit** 入册（沿用 641 "遗留现场 116 项入册" 的既有做法），
使 655 后续提交（尤其 A 的批量许可证头）**不与遗留改动混提交**，并在收工报告登记为**非本批产出、未逐条复核**。

不计入入册范围（保持未跟踪并登记）：`data/backup_652/`（652 的原子/证据卡备份副本，92 文件）。

## 五、655 任务书对照（开工时的可行性与风险）

| 阶段 | 交付物 | 开工风险 |
|---|---|---|
| A 开源准备 | `LICENSE`(Apache-2.0) / DCO / `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` / `README.md` 重写 / `.github/ISSUE_TEMPLATE` 3 模板 + PR 模板 / `tools/license_header_check_655.py` | ① 现状 `LICENSE` 是 **MIT**，改为 Apache-2.0 属**许可变更**（须登记）；② 许可证头需覆盖 `tools/`+`tests/` 约 1100 个 `.py` ⇒ 会变更 `tools/.tool_checksums`（34 条）与哈希面，须 `tool_integrity --update` 重钉 |
| B 判决形式规格 v1 | `docs/verdict_formal_spec_v1.md` | 四态**已实现**（`tools/queyi_core_v10_641.py:42` + `tools/four_state_verdict_638.py`）；扩展轴（`conditions/partial_atoms/conflict_state/unknown_reason`）**只有 schema 与校验**（`tools/verdict_extension_651.py`），**卡级无真实数据** ⇒ 规格须区分"已实现/仅 schema/未实现"三档 |
| C 门禁三杠杆 | `tools/test_selector_655.py` / `tools/result_cache_655.py` / conftest 分片 | 现状**无**增量选例、**无**结果缓存；`pyproject.toml` 明令不把 `-n auto` 写进 addopts、`--dist loadgroup` 实测无效 ⇒ 三杠杆必须是**可选层**，不得改变默认两阶段口径（否则等于改门禁契约） |
| D 前端深化 | `web/starmap.*` / `web/index.html` / `web/verify.*` | 现状：hover 卡片**已有**、点击详情面板**无**、边 hover **无**；landing 已有 canvas 动画但**无计数动画/系统现状面板**；验哈希仅**单文件**、无 CSV 导出 ⇒ 全部为增量改造，数据仍走 `web/data/*.json` |
| E 收工 | 两阶段 pytest / ruff / mypy / 保护器联调 / 信任根刷新 / 许可证头检查 / 报告 | 全量 pytest（fast+slow）历史实测约 23 分钟以上，需分批跑并保留现场；本批 pytest 引入失败须为 0 |

## 六、红线与纪律（本批自我约束）

1. 不动 `CORE_TOOLS` 判决逻辑、不改 67 条规则、不改历史账本（`data/authority/*.jsonl`）与 `atoms/`、`evidence/`；
2. 不代签、不 golden accept、不 push（除非任务书明示）；
3. 每条"已完成"必须有可复跑命令或产物文件；做不到的写进验收报告 §诚实登记；
4. 每阶段一次 commit，小步快跑。

---
_生成：655 阶段 0（开工快照）_
