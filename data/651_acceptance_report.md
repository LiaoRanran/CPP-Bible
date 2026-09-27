# 651 验收报告（整体建设 W0-W3）

- 批次：651　状态：awaiting_review　日期：2026-09-27
- 仓库：CPP-Bible（知识库，主）
- 门禁：`python tools/run_651_gate.py` → **fast / full / ruff / mypy / selftest / 保护器联调 / 零污染 / 信任根 全 PASS（8/8）**

---

## 一、四阶段完成情况

### 阶段 0 · 开工 ✅
`data/651_baseline.md`：确认 650 已收工；资产定位（452 账本 / 648 十卡 / 信任根 / 两阶段纪律）；**受控写保护 + 全量 pytest 限界**登记。

### A · W0 词表（纯文档，零代码）✅
- `docs/evidence_dual_axis.md`：L1-L5 获取级 × GRADE 式把握度（高/中/低/极低）+ 5 升级/5 降级因子 + 合成规则。
- `docs/verdict_extension.md`：`conditions[] / partial_atoms[] / conflict_state / unknown_reason` 扩展词表（只加字段）+ 封闭枚举 + 向后兼容判据。
- `docs/pck_c2pa_mapping.md`：PCK ↔ C2PA（claim/assertion/**硬绑定** c2pa.hash.data）/ in-toto（layout/link）字段映射 + 诚实缺口。

### B · W1 头部（只读/旁路）✅
| 交付 | 结果 |
|---|---|
| `tools/evidence_aging_651.py`（H7） | 扫 **113 卡**，过期 **0**、**无 verified_at 87**；出陈旧队列 + **frontmatter dry-run 计划**（不写卡）+ 订阅清单 |
| `tools/seeker_replay_651.py`（H1） | 648 十卡回放：evidence 引用 **10**、解析失败 **0**（无疑似误引）；出人工评召回/误引留痕表 |
| `data/651_h2_dual_axis_review.md`（H2） | 十卡双轴手标；**关键结论：第二轴须按「命题级」而非「卡级」**（一张卡内同时有高/低把握度面） |

### C · W2 尾部（信任资产）✅
| 交付 | 结果 |
|---|---|
| `tools/ledger_checkpoint_651.py`（T4） | RFC6962 Merkle 签名 checkpoint + **inclusion/consistency 双证明**；**自检穷举 n=1..32 全通 + 篡改被拒**；真账本 452 叶子 root=`38b62c76…`，`--verify` OK |
| `tools/verdict_extension_651.py`（T1） | 只加字段 + **fail-closed 枚举校验**；452 账本回填 **dry-run**：would_change=452，**原文件 sha256 不变** |
| `tools/replay_probe_651.py`（T5） | 648 十卡 reproduce manifest + **单命令验收**：真编译+真运行 **10/10 ACCEPT** |
| `tests/test_core_pbt_651.py`（T6） | 核心状态 PBT 骨架：P1 半格、P2 worst-wins、P3 账本前缀保持、P4 Merkle 追加一致性、P5 保护器置换不变（7 例全绿） |

### D · W3 中间（先 shadow，不上岗）✅
| 交付 | 结果 |
|---|---|
| `tools/shadow_rotator_651.py`（M2） | 新变异器/规则/模型先 shadow N 轮（只记账）；实测 3 轮后 2 个 eligible、model（5 轮）仍 shadow |
| `tools/calibration_upgrade_651.py`（M3） | 分层 α 预算 + 双跑（计数/置信加权）；不一致或超 α ⇒ **强制重校准**；真账本 strata=1、forced=[] |
| `tools/human_review_queue_651.py`（M7） | 缺字段 **fail-closed** + reason 白名单 + **显式适配器** + 优先级 + 三率看板 |

### E · 收工 ✅
`tools/run_651_gate.py`（8 项全 PASS）；ruff/mypy 修 651 文件至全绿；保护器联调 + 受控 atoms 指纹不变（`0404fbdd…`）；**信任根闭包刷新**。

---

## 二、关键发现（诚实登记）

1. **M7 坐实 647 A2 洞（真数据）**：真队列 `pending_review_621.jsonl` 30 条，
   - **raw 严格**：收 0 / **拒 30**（`fail_closed_reject_rate=1.0`）——字段名不符（`proposal_id` vs `item_id`）、`suggested_reason` 是**自由文本**（非枚举）、**无 `created_at`**；
   - **显式适配器后**：收 30 / 拒 0。
   ⇒ 证明"缺字段被默认放行"的洞在真数据上确实存在；修复路径 = 显式别名 + 自由文本规范化（逐条留痕），**非**静默填默认值。
2. **信任根漂移根因**：650 加 10 张 draft 卡 ⇒ `atoms` Merkle **39→49** 不匹配（**非 651 引入**）。E 阶段 `tool_integrity --update` 重钉 ⇒ `--check` 4/4 OK。
3. **H7**：87/113 卡无 `verified_at` ⇒ 时效治理的真实缺口是"没记录"，非"过期"；卡为内容寻址（PCK hash），**写 frontmatter 会致 hash 漂移**，故只出 dry-run 计划。
4. **M3 分层退化**：452 账本事件**无 `source` 字段**（实测全 MISSING）⇒ 分层退化为 1 层，`forced=[]`（rate 0.1881 < α=0.2）。诚实登记：分层需账本先补 `source`。

---

## 三、诚实边界 / 未做

- **全量 pytest 未跑**：642 实测整仓 ~36 分钟，超本工具 idle-timeout。本批跑 **651 新测试（两阶段）+ 门禁 8 项**；全量以登记（不虚报）。
- **既有脏文件 175 个未触碰**：CPP-Bible 工作区存在**大量非 651 改动**（含 648 未提交的 `tests/conftest.py` 逐测试隔离改动、及若干 `tests/test_6xx*.py`）。651 **只提交自身产物**；这些脏文件**非本批引入、未改**。
- **信任根重钉的副作用**：`tool_integrity --update` 会把 `tests/conftest.py`（TEST_CONFIG 面，正是 648 那处未提交改动）一并重钉 ⇒ 等于**追认**了该改动。**需人确认**该 648 conftest 改动是否应正式提交。
- **OTS 未重锚**：重建 `merkle_roots.json` 使其旧 `.ots`（OpenTimestamps）失效 ⇒ 需重锚（同 625/631，**交人**）。
- **demo 见证密钥**：T4 默认 `--witness-key local-witness-demo`（可复现、非机密）；真用须换外部密钥。

## 四、门禁明细（8/8 PASS）
fast pytest / full pytest / ruff(651 文件) / mypy(651 文件) / 8 工具 --check / 保护器联调 / 受控 atoms 指纹零漂移 / 信任根 `tool_integrity --check`。

## 五、交人项
- [ ] W0 三词表是否采纳（尤其 `unknown_reason` 封闭枚举的 8 个值）。
- [ ] H7 是否**批量给 87 张卡补 `verified_at`**（本批只出计划，未写卡）。
- [ ] H2 结论——第二轴是否**按命题级**落地（若是，落地到 `partial_atoms[]`）。
- [ ] T1 452 账本**是否真回填**（本批仅 dry-run）。
- [ ] M7 真队列是否**按适配器迁移**（含补 `created_at`）。
- [ ] 648 的 `tests/conftest.py` 改动是否正式提交（本批 `--update` 已追认其哈希）。
- [ ] `merkle_roots.json` 的 **OTS 重锚**。
- [ ] 全量 pytest（两阶段）整仓复跑（超时留人/CI）。
