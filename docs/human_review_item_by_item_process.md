# 人审「逐条复核」流程（615 A2 · 交人执行）

> 本流程供**人**执行逐条复核；**苦力只生成决策清单，不执行复核、不改 annotations**。
> 决策清单：`data/human_review_item_by_item_30_615.md`。诚实背景：388 条为批量授权，逐条独立判断 0。

## 一、为什么需要逐条复核
`_arch_v19/05_人审即内容.md`：388 条"人审"= 1 名审阅者 × 5 模板，**0 条逐条独立判断**，
其中 194 条为镜像边（派生票）。⇒ 论证图的人类确认强度实为 **0**。逐条复核是把"计数资产"
（388 条）恢复为"信息资产"（边特定理由）的唯一路径。

## 二、逐条复核步骤（每条边 ~2–5 分钟）
1. **读目标卡 frontmatter**：`claim_type` / `status` / `dal` / `verified_by`。
2. **读目标卡正文**：命题（`claim_structured`）、证据、反例/边界。
3. **读源 MIS 的 refutations**：其文本是否**真的驳斥**目标命题的**某个具体断言**？
   （决策清单已给出目标断言文本，来自 `data/propositions.db`。）
4. **证据卡补做 replay 复核**：确认 `artifact_sha256`（人可在有编译环境时执行；本仓 replay 为监工职责）。
5. **observation 命题查活性锚**：`liveness={kind:fixture_symbol, symbol:…}` 是否指向真实夹具符号。
6. **查 MIS 关联**：`related_atoms` / `evidence` 是否一致。
7. **给出 verdict**（`approve` / `modify` / `reject`）+ **边特定理由**（禁止再用 5 模板）。

## 三、如何记录（需人授权）
- 追加写入 `data/human_attack_edge_annotations.jsonl`（**append-only**），每条：
  `{"edge_id": …, "action": "approve|modify|reject", "reason": "<边特定理由，独立判断>", "reviewer": "<实名>", "timestamp": …}`。
- **禁止模板化理由**：理由须含"驳斥了 prop-X 的断言 Y"级别的具体判断（≥50 字符、非镜像、非抽样）。
- 复核完成后，可用 `python tools/human_review_honesty_615.py --check` 复核标签（`item_by_item` 计数应上升）。
- 镜像边（反向 `ATOM::prop->MIS`）**不重复计入**独立确认（W2 中应标 `derived_from_reverse`）。

## 四、边界与纪律
- **苦力不执行任何复核**；本流程执行的更新动作需**人审授权**。
- 不修改卡（受控目录）；不批量代签；理由必须由复核人自己写。
- 单用户模型的上限仍在：即便逐条复核，仍是同一人 ⇒ 独立性弱于"第二人"，须在报告中诚实标注。
