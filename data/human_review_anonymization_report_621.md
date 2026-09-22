# 621 D3 · 人审数据脱敏报告

> Authority 日志 388 条 + 历史标注 388 条 ⇒ 脱敏输出 **776** 条

## 一、脱敏方法

| # | 动作 | 说明 |
|---|---|---|
| 1 | reviewer → 稳定化名 | `R-<sha256前8>`，同人同码、不可逆推姓名 |
| 2 | 时间戳截断到日 | 去掉时刻，降低时序关联精度 |
| 3 | 用户目录名 → `<user>` | 清除 `C:\Users\<name>` / `/home/<name>` 等路径身份 |
| 4 | 哈希链字段 | **默认移除**（去关联） |

## 二、脱敏前后数据量对比

| 项 | 脱敏前 | 脱敏后 |
| 记录条数 | 776 | 776 |
| 含真实姓名的字段 | 776 条有 `reviewer` | **0**（改为 `reviewer_pseudo`） |
| 含时刻的时间戳 | 全部 | **0**（截断到日） |

## 三、残留身份扫描

- 已知真实姓名样本：2 个
- 脱敏结果中残留命中：**{}**
- 判定：**干净 ✅**

## 四、脱敏后样例（前 2 条）

```json
{"decided_at": "2026-09-19", "decision_id": "dec-000001", "power": "ACCEPT", "reason": "用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权", "review_method": "batch_authorization", "reviewer_pseudo": "R-24a61293", "source": "import:data/human_attack_edge_annotations.jsonl", "target": {"id": "ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3", "type": "attack_edge"}}
{"decided_at": "2026-09-19", "decision_id": "dec-000002", "power": "ACCEPT", "reason": "用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过", "review_method": "batch_authorization", "reviewer_pseudo": "R-24a61293", "source": "import:data/human_attack_edge_annotations.jsonl", "target": {"id": "ae-MIS-CONC-001->ATOM-UB-GRAY-001::prop-1", "type": "attack_edge"}}
```

