# 634 B1 · coverage 矩阵（35 向量）

- 基线（630）：ran 16/35 = 45.7%
- 631 加 L1.2/L8.4、632 加 L2.3/L4.2/L4.4 ⇒ 21/35
- **634 加 14 向量 ⇒ ran 35/35 = 100.0%**

## 一、本批新建的 14 个探针（结构性覆盖）

| 向量 | 名称 | risk | 防御载体 | 机制存在 |
|---|---|---|---|---|
| `L1.1` | 命题等价改写 | high | `tools/mutation_fuzz.py` | ✅ |
| `L1.3` | 命题范围偷换 | high | `tools/atom_evidence_replay.py` | ✅ |
| `L1.4` | 命题-证据错配 | high | `tools/gate_engine.py` | ✅ |
| `L2.4` | 证据凭空伪造 | high | `tools/poison_drill.py` | ✅ |
| `L3.1` | 解析歧义 | high | `tests` | ❌ 缺口 |
| `L3.3` | 字段注入 | high | `tools/gate_engine.py` | ✅ |
| `L3.4` | 解析器特性绕过 | medium | `tools/gate_engine.py` | ✅ |
| `L4.3` | regex heuristic 绕过 | high | `tools/gate_engine.py` | ✅ |
| `L5.3` | 验证者自身被投毒 | high | `tools/independent_verifier_628.py` | ✅ |
| `L7.2` | 模板化人审 | high | `tools/human_review_executor_625.py` | ✅ |
| `L7.4` | rubber-stamp | high | `tools/weighted_af_human_review_609.py` | ❌ 缺口 |
| `L7.5` | 人审覆盖不足 | medium | `tools/autoimmune_human_queue_631.py` | ✅ |
| `L8.2` | 签名投毒 | high | `tools/vsa_verify_628.py` | ✅ |
| `L8.3` | append-only 链断裂 | high | `tools/transparency_verify_632.py` | ✅ |

- 机制存在：**12/14**

## 二、覆盖状态总表（ran 集合）

- ran（35）：`L1.1`, `L1.2`, `L1.3`, `L1.4`, `L2.1`, `L2.2`, `L2.3`, `L2.4`, `L3.1`, `L3.2`, `L3.3`, `L3.4`, `L4.1`, `L4.2`, `L4.3`, `L4.4`, `L4.5`, `L5.1`, `L5.2`, `L5.3`, `L5.4`, `L6.1`, `L6.2`, `L6.3`, `L6.4`, `L7.1`, `L7.2`, `L7.3`, `L7.4`, `L7.5`, `L8.1`, `L8.2`, `L8.3`, `L8.4`, `L8.5`

## 三、诚实登记

1. 本批探针为**结构性覆盖探针**（测防御机制是否存在），**非**动态攻击复现（这些向量在 630 口径下无独立运行时探针）；
2. 与 632/633 同口径：coverage 的「ran」= 该向量**已有一次覆盖测量**；本批把 14 个从未测量的向量纳入 ⇒ 35/35；**不等价于**「14 个动态攻击都被拦」；
3. 机制缺失的向量**如实标 ❌ 缺口**，不粉饰。
