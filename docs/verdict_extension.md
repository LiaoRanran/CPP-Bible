# 判决扩展词表（T1：只加字段，不改语义）

> 651 W0 产出（纯文档，零代码）。约束（651 任务书）：**只加字段不改语义**、历史证书**向后兼容**。
> 落地实现见 `tools/verdict_extension_651.py`（schema + 校验 + 历史回填 dry-run）。

## 一、现状与目标

现有判决（四态 `pass / pass_with_exception / fail / unknown`，见 638）已能表达主结论，
但表达不了四类**边界事实**：
1. 结论**在什么条件下**成立（conditions）；
2. 结论只覆盖了**部分原子命题**（partial atoms）；
3. 同一条出现**显式冲突**（两侧都有证据但结论互斥）；
4. `unknown` **为什么** unknown（reason 枚举，而非一个黑箱 unknown）。

本扩展**只新增可选字段**；旧字段一字不改，旧证书缺新字段 ⇒ 视为「未声明」（不判错）。

## 二、新增字段（全部可选，`schema_version: 2`）

| 字段 | 类型 | 含义 | 缺省语义 |
|---|---|---|---|
| `schema_version` | int | 判决结构版本；旧证书=1 | 1 = 无扩展 |
| `conditions[]` | array<object> | 结论成立的前提；每项 `{kind, expr, evidence_ref}` | 空 = 无条件 |
| `partial_atoms[]` | array<object> | 只覆盖到的原子命题子集；每项 `{atom_id, covered: bool, note}` | 空 = 覆盖全命题 |
| `conflict_state` | enum | `none / detected / resolved` | `none` |
| `conflict_detail` | object\|null | 冲突双方 `{left, right, c_value, evidence_both_sides: bool}` | null |
| `unknown_reason` | enum\|null | unknown 的原因（见下枚举） | null |

### 2.1 `conditions[].kind` 枚举
`platform` / `compiler_version` / `std_version` / `optimization` / `input_domain` / `assumption` / `other`

### 2.2 `conflict_state` 枚举
- `none`：无冲突。
- `detected`：检出冲突但**未裁定**（应转人审，见 M7 队列）。
- `resolved`：已裁定（`conflict_detail` 必填，且需 `resolution` 理由）。

### 2.3 `unknown_reason` 枚举（**封闭枚举**，白名单）
| 值 | 含义 |
|---|---|
| `no_evidence` | 无任何证据 |
| `evidence_conflict` | 证据互相冲突 |
| `out_of_scope` | 断言超出当前域/Domain Pack 范围 |
| `implementation_defined` | 落在实现定义/未规定处（对应双轴 D2） |
| `insufficient_samples` | 样本不足 |
| `tool_unavailable` | 所需工具/编译器不可用 |
| `not_applicable` | 该规则对该卡不适用 |
| `other` | 其他（必须附 `unknown_note`） |

**fail-closed 纪律**（对应 M7「封 647 A2 默认值洞」）：若某字段值**不在**上述枚举内，
校验器必须**拒绝**（而非默认放行）。旧证书缺 `unknown_reason` 不拒绝（兼容），但**新写入**必须合法。

## 三、最小示例

```json
{
  "decision_id": "DE-000123",
  "state": "pass_with_exception",
  "schema_version": 2,
  "conditions": [
    {"kind": "compiler_version", "expr": "gcc==13.1.0", "evidence_ref": "EV-648-decay"},
    {"kind": "optimization", "expr": "-O2", "evidence_ref": "EV-648-decay"}
  ],
  "partial_atoms": [
    {"atom_id": "ATOM-C-DECAY-001", "covered": true, "note": "数组退化面已覆盖"},
    {"atom_id": "ATOM-C-DECAY-002", "covered": false, "note": "变长数组面未测"}
  ],
  "conflict_state": "none",
  "unknown_reason": null
}
```

## 四、向后兼容判据（回填脚本必须满足）
1. 旧证书（无新字段）经本 schema 校验 ⇒ **PASS**（视为 v1）。
2. 回填**只加字段**，不动 `state`/`decision_id`/哈希链字段。
3. 回填默认 `conflicts_state=none`、`unknown_reason=null`、`schema_version=2`；
   `unknown` 态旧证书回填 `unknown_reason` 时**只能填 `other` 且附 note**（不臆测根因）。
4. 回填 dry-run 必须报告「将改条数 / 每条 diff / 原文件 sha256 不变」。
