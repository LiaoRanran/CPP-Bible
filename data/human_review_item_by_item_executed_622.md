# 622 D1 · 30 条逐条人审执行（按用户授权）

> # 🔴 口径警示（2026-09-22 补，外部大模型审阅发现 + 626 A3 落地）
>
> **本批 30 条为「按用户授权执行」，未新增独立人类语义判断。**
>
> - `review_method = USER_AUTHORIZED_EXECUTION`（v2 规范名：`ITEM_OPEN`）
> - `decision_origin = user_authorized_execution`
> - **独立人类确认强度仍为 `0` 条** —— 这 30 条**不得**计入独立人审证据
>
> 事实依据：第一批 17 条是 OVERRIDE，理由直接沿用清单模板；第二批 13 条是 ACCEPT，
> 理由同样是模板化的「复核 approve」。文档自己即承认「本批未新增任何人工判断，只做了把授权落到日志」。
> 「30 条日志已执行」与「30 条新的独立人类语义审查」必须彻底区分（判据 1）。
>
> 详细口径见：本文档 A3 标注 · `data/human_review_honesty_615.md` 第六节 · `tools/authority_schema_v2_626.py`。

> ⚠ **这是按用户授权执行 615 决策清单，不是系统自动决策。**
> 每条决策均标注 `source=615_decision_list` 与 `authorized_by=user_authorization_2026-09-21`。

## 一、执行统计

| 项 | 值 |
|---|---|
| 执行条数 | **30** |
| Authority 决策日志 | **388 → 418**（+30） |
| 哈希链校验 | **通过 ✅** |
| power 分布 | {"OVERRIDE": 17, "ACCEPT": 13} |
| `review_method` | `item_by_item_executed` |
| `authorized_by` | `user_authorization_2026-09-21` |
| `source` | `615_decision_list` |
| 全部带 overrides 指名的条数 | 17 |

## 二、与 615 决策清单的对应关系（proposal_id 序号 = 615 #）

| 615 # | proposal_id | 边 ID | 置信度 | power | overrides |
|---|---|---|---|---|---|
| 001 | `prop-621-001` | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1` | low | OVERRIDE | `dec-000178` |
| 002 | `prop-621-002` | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-2` | low | OVERRIDE | `dec-000179` |
| 003 | `prop-621-003` | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-3` | low | OVERRIDE | `dec-000180` |
| 004 | `prop-621-004` | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1` | low | OVERRIDE | `dec-000181` |
| 005 | `prop-621-005` | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-2` | low | OVERRIDE | `dec-000182` |
| 006 | `prop-621-006` | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-3` | low | OVERRIDE | `dec-000183` |
| 007 | `prop-621-007` | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-1` | low | OVERRIDE | `dec-000184` |
| 008 | `prop-621-008` | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-2` | low | OVERRIDE | `dec-000185` |
| 009 | `prop-621-009` | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-3` | low | OVERRIDE | `dec-000186` |
| 010 | `prop-621-010` | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-1` | low | OVERRIDE | `dec-000187` |
| 011 | `prop-621-011` | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2` | low | OVERRIDE | `dec-000188` |
| 012 | `prop-621-012` | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-1` | low | OVERRIDE | `dec-000189` |
| 013 | `prop-621-013` | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-2` | low | OVERRIDE | `dec-000190` |
| 014 | `prop-621-014` | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-1` | low | OVERRIDE | `dec-000191` |
| 015 | `prop-621-015` | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-2` | low | OVERRIDE | `dec-000192` |
| 016 | `prop-621-016` | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-1` | low | OVERRIDE | `dec-000193` |
| 017 | `prop-621-017` | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-2` | low | OVERRIDE | `dec-000194` |
| 018 | `prop-621-018` | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-1` | medium | ACCEPT | — |
| 019 | `prop-621-019` | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-2` | medium | ACCEPT | — |
| 020 | `prop-621-020` | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-3` | medium | ACCEPT | — |
| 021 | `prop-621-021` | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-1` | medium | ACCEPT | — |
| 022 | `prop-621-022` | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-2` | medium | ACCEPT | — |
| 023 | `prop-621-023` | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-3` | medium | ACCEPT | — |
| 024 | `prop-621-024` | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-1` | medium | ACCEPT | — |
| 025 | `prop-621-025` | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-2` | medium | ACCEPT | — |
| 026 | `prop-621-026` | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-3` | medium | ACCEPT | — |
| 027 | `prop-621-027` | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-1` | medium | ACCEPT | — |
| 028 | `prop-621-028` | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-2` | medium | ACCEPT | — |
| 029 | `prop-621-029` | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-3` | medium | ACCEPT | — |
| 030 | `prop-621-030` | `ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-1` | medium | ACCEPT | — |

## 三、声明

1. **按用户授权执行**：来源 = 615 决策清单（`data/human_review_item_by_item_30_615.md`），
   授权 = `user_authorization_2026-09-21`。**非系统自动决策。**
2. **append-only**：只追加 30 条，未修改/删除任何历史条目（哈希链校验通过）。
3. **未修改任何原始卡**：决策只落入 Authority 日志。
4. 是否**最终认可**这 30 条执行结果 = 622 §八.4 **人拍板项**。

## 四、局限性声明

1. **30 条样本量小**，不代表全量人审质量（全库 388 条仍为批量授权）。
2. **理由是 615 的模板化建议文本**（如"需独立判断（原为镜像/短理由…）"），
   不是逐条写下的实质判断 ⇒ 这是「形式上的逐条」（622 D2 已量化）。
3. **`reviewer` 记为 `human:LiaoRanran`**：执行的是该人的既有授权，
   本批**未新增**任何人工判断，只做了"把授权落到日志"这一步。
4. **未改 annotations 源文件**：决策落在 Authority 日志，
   `data/human_attack_edge_annotations.jsonl` 未动 ⇒ 两处仍可能不同步。
