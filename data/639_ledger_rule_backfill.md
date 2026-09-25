# 639 D2 · ledger 规则归属回填报告

> 生成：2026-09-25T10:30:05。append-only：**不改写**历史事件，结论落 overlay。

## 一、schema 上线（链兼容实证）

- `DecisionEvent` 新增 `rule_id` / `rule_version`（空值不参与哈希）；
- 历史事件重放：**452/452** 自哈希吻合；
- prev_hash 链条完整：**True**。

## 二、历史 452 条事件归属判定

- `attributed`（精确命中唯一规则）：**0** 条；
- `ambiguous`（命中多条）：**0** 条；
- `undetermined`（无命中）：**452** 条。

> **诚实结论**：事件中的 `ATOM-*` 串是**原子卡 id**（edge 的端点），与规则 id 同前缀但不同物；历史判决证据链（basis_refs → authority_log）实测**不含规则引用** ⇒ 全部标 `undetermined`，**不编造归属**。

## 三、known_error_rate 重跑

- rule 级样本仍为 0 ⇒ 67 条规则维持「无数据」（诚实，不给估算值）；
- **路径已通**：新判决事件自本批起携带 rule_id，error_rate_collector 的 `RULE_FIELD_CANDIDATES` 将自动生效，rule 级样本从此累积。

## 四、交人项

- 判决事件是否应强制携带 rule_id（涉及监工流程改造，非本批范围）；
- 如需历史归属，只能靠人工回看 452 条判决对应的门禁运行记录（大工程）。
