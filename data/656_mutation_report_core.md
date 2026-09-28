# 656 B2 · 变异测试报告

> 生成：2026-09-28T10:20:40　杀测试：`tests/test_core_pbt_656.py`（656 B1 的 P1–P12 真实测试函数）　种子：20260928（可复现）

## 一、总览

- 变异体：**60**
- 被杀：30　存活：18　导入即崩：10　超时：2
- **检出率（只看能跑的 48 个）：62.5%**
- 检出率（含导入即崩，口径更宽松）：50.0%

## 二、分文件

| 目标 | 总数 | 被杀 | 存活 | 导入崩 | 超时 | 检出率 |
|---|---:|---:|---:|---:|---:|---:|
| `four_state_verdict_638` | 20 | 8 | 11 | 1 | 0 | 42.1% |
| `ledger_checkpoint_651` | 20 | 12 | 2 | 4 | 2 | 85.7% |
| `decision_event_v2_626` | 20 | 10 | 5 | 5 | 0 | 66.7% |

## 三、存活体（测试没抓到的改动）

| 目标 | 行 | 算子 | 改了什么 | 原文 |
|---|---:|---|---|---|
| `four_state_verdict_638` | 142 | bool | `not`→`''` | `missing = [k for k in BOUNDARY_FIELDS if not rec.get(k)]` |
| `four_state_verdict_638` | 181 | bool | `True`→`False` | `return {"file": path, "state": "unknown", "downgraded": True, "boundar` |
| `four_state_verdict_638` | 90 | bool | `False`→`True` | `656 B3：入参不是 dict ⇒ **显式**返回 False（原来会 `AttributeError` 炸出去，` |
| `four_state_verdict_638` | 160 | bool | `or`→`and` | `"boundary_ok": True, "reasons": reasons or ["有边界，按原始判决定态"]}` |
| `four_state_verdict_638` | 119 | bool | `or`→`and` | `return "pass_with_exception" if (exc or explanation) else "pass"` |
| `four_state_verdict_638` | 156 | bool | `True`→`False` | `"boundary_ok": True, "reasons": reasons}` |
| `four_state_verdict_638` | 190 | cmp | `==`→`!=` | `if st and st.group(1).lower() == "verified" and not m:` |
| `four_state_verdict_638` | 190 | bool | `and`→`or` | `if st and st.group(1).lower() == "verified" and not m:` |
| `four_state_verdict_638` | 187 | bool | `if`→`if not` | `"explanation": (ex.group(1) if ex else ""),` |
| `four_state_verdict_638` | 149 | bool | `False`→`True` | `"boundary_ok": False, "reasons": reasons}` |
| `four_state_verdict_638` | 114 | bool | `or`→`and` | `exc = rec.get("exception") or rec.get("has_exception") or rec.get("exc` |
| `ledger_checkpoint_651` | 104 | bool | `False`→`True` | `return False` |
| `ledger_checkpoint_651` | 162 | bool | `and`→`or` | `return fr == old_root and sr == new_root` |
| `decision_event_v2_626` | 258 | bool | `False`→`True` | `return False` |
| `decision_event_v2_626` | 245 | bool | `not`→`''` | `alive = [e for e in evs if e.event_id not in superseded]` |
| `decision_event_v2_626` | 244 | bool | `or`→`and` | `superseded.update(e.supersedes or [])` |
| `decision_event_v2_626` | 246 | bool | `if`→`if not` | `return alive[-1] if alive else evs[-1]` |
| `decision_event_v2_626` | 240 | bool | `not`→`''` | `if not evs:` |

## 四、诚实边界

1. **进程内替换**只覆盖被测试文件 import 的模块；CLI / 子进程行为不在射程内。
2. **导入即崩**算’被杀’但不含信息量 ⇒ 已单独统计，检出率主口径只看能跑的变异体。
3. 存活体 ≠ 一定有 bug：也可能是**等价变异**（改了写法不改语义）或该分支本就无测试覆盖；本批对存活体的处置见 §五。
4. 变异体是**随机抽样**（种子固定 ⇒ 可复现），不是穷举；样本外仍可能有漏网。

## 五、对存活体的处置

检出率 62.5% < 80% ⇒ **未达标**；存活体已列在 §三，按任务书要求应补测试（见收工报告的诚实登记）。
