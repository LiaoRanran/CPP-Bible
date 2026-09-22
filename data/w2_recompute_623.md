# 623 D2 · W2 重算（通道打通后）

> 工具：`tools/w2_recompute_623.py`（聚合 annotations 原视图 / synced 视图为每原子判决，对比差异）
> 输入：`data/human_attack_edge_annotations.jsonl`（原） + `data/human_attack_edge_annotations.synced.jsonl`（D1 产出）

---

## 一、重算结果

| 视图 | 原子数 | IN | OUT | UNRESOLVED |
|---|---|---|---|---|
| 原 annotations | 67 | 59 | 0 | **8** |
| synced（D1 后） | 67 | **67** | 0 | 0 |

**原 → synced 判决变化原子数：8**（全部 `UNRESOLVED → IN`）：
`ATOM-LANG-INLINE-001 / MIS-LANG-001 / MIS-MEM-001 / MIS-MEM-003 / MIS-UB-001 / MIS-UB-004 / MIS-UB-008 / MIS-UB-014`

## 二、变化的真实来源（不是通道断，是通道打通的实效）

核对原始 annotations 动作分布：
- 原：`approve 354` + **`modify 34`**
- synced：`approve 388`

W2 聚合规则：`reject → OUT`；`approve → IN`；**其余（含 `modify`）→ UNRESOLVED**。
原 annotations 中 34 条边动作是 `modify`，不计入 `approve` ⇒ 含这些边的 8 个原子被判 `UNRESOLVED`。
D1 把 Authority 决策（ACCEPT→approve）合并进 synced 视图，34 条 `modify` 全部转为 `approve` ⇒ 8 原子翻转为 `IN`。

## 三、结论（诚实修订 622 D2 假设）

622 D2 报告 "W2 重算变化 0，非真无变化，而是通道断"。本批 D1 打通通道后重算，**实际变化 = 8 原子**
（UNRESOLVED→IN）——这**反向证实 622 D2 的"变化 0"确为通道断伪影**：
34 条 `modify` 边的 Authority 决策（approve）从未进入 annotations，W2 一直把它们当 UNRESOLVED 算，
故 622 看到的"稳定 0 变化"是假象。通道打通后，8 原子从"未决议"变为"准入"，W2 判决**真实变动**。

> 与提示词假设（"变化 0 不再因通道断，而是真无变化"）的差异：实测并非 0 变化，而是 8 变化。
> 这比假设更有价值——它坐实了 622 D2 的通道断诊断，并把 8 个原被漏判为 UNRESOLVED 的原子纠正为 IN。

## 四、下一步建议（留 624）

1. **`modify` 动作的语义**：当前 W2 把 `modify` 当 UNRESOLVED。建议明确 `modify` 在 W2 中的语义
   （视为 approve 的弱确认？还是需 re-review？），避免再次被漏判。
2. **写回真实 annotations**：D1 只产 synced 视图未覆盖受治理原文件；是否把 34 条 `modify→approve`
   写回 `human_attack_edge_annotations.jsonl` 由人审决定（铁律：不自动 push）。
3. **W2 solver 代码缺失**：仓库内无读取 annotations 的 W2 solver 代码（tools/ 无引用）。本工具用透明聚合规则
   重建 W2 判决；建议把真实 W2 solver 纳入 RULER_TOOLS 保护（见 C2）。

## 五、局限性声明

1. W2 聚合规则为本工具自定义的透明规则（reject→OUT / approve→IN / 其余→UNRESOLVED），非复刻某个缺失的 solver 代码。
2. 仅基于 annotations 两视图的 edge_id→action，不依赖任何 CORE_TOOLS。
3. 原子识别依赖 edge_id 格式 `ae-<src>-><ATOM>::prop-N`；格式异常边被安全跳过。
