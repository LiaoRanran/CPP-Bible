# 625 C2 · QueYi Core 核心接口抽象设计（v0.1 · 设计版）

> 接口版本 **v0.1**（设计版）；626 为实现版。**只设计不实现**。

## 一、核心接口

### Claim —— 知识命题（原子卡的可验证主张）

- 属性：`id` / `statement` / `domain` / `difficulty` / `prerequisites` / `evidence_refs`
- 方法：`validate()` / `get_evidence()` / `get_prerequisites()`

### Evidence —— 证据（可复算工件/观测）

- 属性：`id` / `type` / `source` / `content` / `hash` / `verifier_refs` / `provenance`
- 方法：`validate()` / `get_verifiers()` / `get_provenance()` / `verify_hash()`

### Attack —— 攻击/mutation（对命题或证据的扰动）

- 属性：`id` / `type` / `target` / `strategy` / `complexity` / `expected_result`
- 方法：`apply()` / `revert()` / `get_result()` / `get_complexity()`

### Verify —— 验证器（规则/复算/毒样例）

- 属性：`id` / `type` / `version` / `rules` / `config`
- 方法：`verify(claim)` / `verify(evidence)` / `verify(attack)` / `get_rules()`

### Authority —— 人审权威（第一原则：生成者不得兼任判断者）

- 属性：`id` / `type` / `permissions` / `audit_log`
- 方法：`authorize(claim)` / `reject(claim)` / `abstain(claim)` / `get_audit_log()`

## 二、接口关系图

```
Claim --> Evidence   // claim 引用 evidence_refs
Attack --> Claim   // attack 扰动 claim
Attack --> Evidence   // attack 扰动 evidence
Verify --> Claim   // verify 判定 claim
Verify --> Evidence   // verify 判定 evidence
Verify --> Attack   // verify 判定 attack 是否被挡
Authority --> Claim   // authorize/reject/abstain claim
```

## 三、与现有工具的映射

| 现有工具 | QueYi Core 接口 |
|---|---|
| `gate_engine` | Verify（规则层验证器） |
| `atom_evidence_replay` | Evidence（证据复算/复现） |
| `poison_drill` | Attack（毒样例攻击面 + 回归） |
| `tool_integrity` | Verify（信任根/尺子完整性） |
| `weighted_af_solver` | Claim（论证图判决：IN/OUT/UNRESOLVED） |
| `human_review_queue` | Authority（人审队列） |
| `authority_log_620` | Authority（决策审计日志） |
| `pck_certificate_verifier_619` | Evidence（PCK 证书验证） |

## 四、626 实现计划

| 顺序 | 接口 | 理由 |
|---|---|---|
| 1 | Evidence | 先实现（replay/PCK 已近接口） |
| 2 | Verify | 其次（gate/integrity 已具备） |
| 3 | Claim | 再次（论证图/原子卡已有数据） |
| 4 | Attack | 随后（沙箱 apply API 已具备） |
| 5 | Authority | 最后（涉及人审治理） |

## 五、局限性声明

1. v0.1 为**设计草案**，未落地为 Python `Protocol`/抽象基类。
2. 映射为**语义映射**，现有实现未必严格满足接口契约（626 逐项对齐）。
3. 未定义跨靶场（C++/数学/嵌入式）的差异化实现细节。

