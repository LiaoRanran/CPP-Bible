# 656 基线快照（阶段 0）

> 生成：2026-09-28　｜　任务书：`_auto/inbox/656.md`　｜　类型：夜间大包（G9 总闸门 + 内核极致 + 前端工程 + 教学 MVP 骨架）

## 一、开工现场

| 项 | 值 |
|---|---|
| HEAD | `f75f157c`（655 收尾：status 收工态） |
| `origin/master..HEAD` | **37** commit（未 push） |
| 受控改动（tracked） | **无**（`git status --porcelain` 只剩未跟踪项） |
| 未跟踪 | `_arch_v35/` `_arch_v36_brief.md` `_arch_v37/` `_arch_v37_brief.md` `_arch_v38/` `_arch_v38_brief.md`（并行调研进程产出）、`data/backup_652/` |
| 655 是否收工 | ✅ 已收工：`_auto/status.json` state=awaiting_review / last_completed_batch=655 / next_batch=656；`run_655_gate` 13/13 PASS；`data/655_acceptance_report.md` + `_auto/outbox/655.md` 齐备 |

## 二、现状指标（现算，非记忆值）

| 指标 | 值 | 来源 |
|---|---|---|
| 知识卡 | **37** 张实卡 + **10** 张 draft650 = 47 | `tools/web_status_655.py` 扫 `atoms/**` |
| 判决规则 | **67**（`severity=block` **44**） | 现 import `tools/gate_engine.py` |
| 保护器 | **9/9** 就位（5×647 真上岗 + 4×649） | 现扫 `queyi-core/tools/` |
| 逃逸率 | **1 / 1406 = 0.0711%**（v7 基线，与 616 冻结口径交叉核对一致） | `data/mutation/full_baseline_v7.json` |
| W2 接地 | **131** 节点：IN **89** / OUT **42** | `data/grounded_labels_w2.json` |
| 星图 | 178 节点 / 1093 边（攻击 388，其中被击败 194）/ 防御 616 | `tools/web_data_653.py` 生成的 `web/data/graph.json` |
| 信任根 | `--check` **4/4 OK**（core 5 / supply_chain 5 / merkle / ruler 22） | `tools/tool_integrity.py --check` |

## 三、655 交人 9 项在本批的分派（诚实先说"不做什么"）

| # | 655 交人项 | 656 处置 |
|---|---|---|
| 1 | MIT→Apache-2.0 是否最终确定 | **不动**（保持 Apache-2.0；许可变更属权利人决策，非技术批次该动） |
| 2 | DCO 是否上 CI 强制 | **不做**（需改 workflow 与历史 commit 批量 signoff，超本批容量；仍交人） |
| 3 | 315 个存量文件是否补许可证头 | **不做**（`_archive/`+调研脚本；保持 active=100% / all=77.8% 现口径） |
| 4 | `build/replay_manifest.json` 根治（`--rebuild-manifest`） | **不做**（56 张卡真编译耗时；仍交人并给命令） |
| 5 | slow 相 40 个预存在失败（27↔37 卡等数字漂移） | **不做**（独立批次去写死；本批只做落户的对账与归因） |
| 6 | 门禁三杠杆是否接入 CI | **部分做**：C3/C4 里接 web 数据管线自校验（`--check`），不改造 CI 的 pytest 矩阵 |
| 7 | jsdom / Node 版本（CI 若 ≥20 可开真 DOM 冒烟） | **部分做**：C4 的 Pages workflow 里跑 Node **20**（由 CI 提供）+ `web_logic_check`；本机 Node 18 仍 SKIP，不改本机环境 |
| 8 | 是否 push（ahead 37） | **不 push**（红线；等用户指令） |
| 9 | CRLF 漂移收口（`git add --renormalize` + 重钉 + 重锚） | **不做**（2026-09-13 已裁决"暂不 renormalize"；本批会在 A 阶段**顺手不动** `.ots` 之外的行尾） |

## 四、本批可执行性取证（先探再做的三项）

| 能力 | 探测结果 | 对 A 阶段的影响 |
|---|---|---|
| `ots` CLI | ❌ 未安装（`CommandNotFoundException`） | 走库路径或降级 |
| Python `opentimestamps` 库 | ✅ 已装进 `.venv`（`ensurepip` + `pip install opentimestamps-client`，`opentimestamps 0.4.5`） | 可**用官方实现真解析/真 stamp 真提交** |
| OTS 日历（HTTPS） | ✅ `alice/bob.btc.calendar.opentimestamps.org`、`finney.calendar.eternitywall.com`、`a.pool.opentimestamps.org` 均可达 | 可真实提交 digest；Bitcoin 确认需等挖矿（pending → confirmed） |

> ⚠️ **`.venv` 现在多了 opentimestamps 系列依赖**（python-bitcoinlib / pycryptodomex / GitPython 等）。
> 这是 **G9 的必要代价**（没有官方实现就等于自己编造 OTS 文件 ⇒ 不允许）。本批会在报告里登记这个环境变化，
> 并在 tool 里对"库不可用"保留降级路径（CI/他机无该库时仍可跑 `--check`）。

---
_本文件为 656 阶段 0 产物；后续阶段（A/B/C/D/E）的实测数据另见各自的 `data/656_*` 报告。_
