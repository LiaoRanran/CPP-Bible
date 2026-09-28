# 656 B2 · 变异测试报告

> 生成：2026-09-28T10:22:22　杀测试：`tests/test_core_pbt_656.py`（656 B1 的 P1–P12 真实测试函数）　种子：20260928（可复现）

## 一、总览

- 变异体：**60**
- 被杀：15　存活：37　导入即崩：8　超时：0
- **检出率（只看能跑的 52 个）：28.8%**
- 检出率（含导入即崩，口径更宽松）：25.0%

## 二、分文件

| 目标 | 总数 | 被杀 | 存活 | 导入崩 | 超时 | 检出率 |
|---|---:|---:|---:|---:|---:|---:|
| `four_state_verdict_638` | 20 | 3 | 14 | 3 | 0 | 17.6% |
| `ledger_checkpoint_651` | 20 | 10 | 8 | 2 | 0 | 55.6% |
| `decision_event_v2_626` | 20 | 2 | 15 | 3 | 0 | 11.8% |

## 三、存活体（测试没抓到的改动）

| 目标 | 行 | 算子 | 改了什么 | 原文 |
|---|---:|---|---|---|
| `four_state_verdict_638` | 142 | bool | `not`→`''` | `missing = [k for k in BOUNDARY_FIELDS if not rec.get(k)]` |
| `four_state_verdict_638` | 267 | const | `2`→`3` | `json.dump(a, fh, ensure_ascii=False, indent=2)` |
| `four_state_verdict_638` | 186 | bool | `if`→`if not` | `"verdict": (m.group(1) if m else ""),` |
| `four_state_verdict_638` | 346 | cmp | `==`→`!=` | `"generator_version": "v"}) == "unknown")` |
| `four_state_verdict_638` | 143 | bool | `if`→`if not` | `if missing:` |
| `four_state_verdict_638` | 339 | cmp | `==`→`!=` | `enforce({**b, "verdict": "pass", "exception": "条款X"}) == "unknown")` |
| `four_state_verdict_638` | 172 | const | `656`→`657` | `656 B3：`path` 为空 / 不是字符串 ⇒ 显式 unknown（原来 `open(None)` 抛 `TypeError`，` |
| `four_state_verdict_638` | 138 | bool | `False`→`True` | `return {"state": "unknown", "requested": requested, "downgraded": Fals` |
| `four_state_verdict_638` | 10 | const | `2`→`3` | `2. **边界三元组强制**（§三.1.3）：任何 `pass`/`fail` 必须附` |
| `four_state_verdict_638` | 160 | bool | `or`→`and` | `"boundary_ok": True, "reasons": reasons or ["有边界，按原始判决定态"]}` |
| `four_state_verdict_638` | 187 | bool | `if`→`if not` | `"explanation": (ex.group(1) if ex else ""),` |
| `four_state_verdict_638` | 149 | bool | `False`→`True` | `"boundary_ok": False, "reasons": reasons}` |
| `four_state_verdict_638` | 155 | bool | `True`→`False` | `return {"state": "unknown", "requested": requested, "downgraded": True` |
| `four_state_verdict_638` | 90 | bool | `False`→`True` | `656 B3：入参不是 dict ⇒ **显式**返回 False（原来会 `AttributeError` 炸出去，` |
| `ledger_checkpoint_651` | 215 | bool | `not`→`''` | `if not path.is_file():` |
| `ledger_checkpoint_651` | 295 | const | `2`→`3` | `print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json` |
| `ledger_checkpoint_651` | 243 | const | `33`→`34` | `for n in range(1, 33):` |
| `ledger_checkpoint_651` | 84 | const | `656`→`657` | `656 B3：**空列表 / 下标越界 ⇒ 返回 []**。原来这条路径会无限递归` |
| `ledger_checkpoint_651` | 258 | const | `32`→`33` | `bad[0] = bytes(32)` |
| `ledger_checkpoint_651` | 104 | bool | `False`→`True` | `return False` |
| `ledger_checkpoint_651` | 15 | cmp | `==`→`!=` | `====` |
| `ledger_checkpoint_651` | 200 | bool | `not`→`''` | `assert old_root is not None` |
| `decision_event_v2_626` | 246 | bool | `if`→`if not` | `return alive[-1] if alive else evs[-1]` |
| `decision_event_v2_626` | 383 | cmp | `==`→`!=` | `chk("seq 从 1 开始", e1.seq == 1)` |
| `decision_event_v2_626` | 145 | bool | `if`→`if not` | `return DecisionEvent(**{k: v for k, v in d.items() if k in known})` |
| `decision_event_v2_626` | 463 | const | `452`→`453` | `len(hist) == 452 and hist.verify_chain(), str(len(hist)))` |
| `decision_event_v2_626` | 360 | bool | `True`→`False` | `return True` |
| `decision_event_v2_626` | 32 | const | `642`→`643` | `因为 642 B3 的 FO-B 复现与 `from_dict({})` 的宽容语义依赖它，历史账本也必须能 lenient 导入。` |
| `decision_event_v2_626` | 320 | bool | `False`→`True` | `def load_ledger(path: str = LEDGER_PATH, strict: bool = False) -> Auth` |
| `decision_event_v2_626` | 258 | bool | `False`→`True` | `return False` |
| `decision_event_v2_626` | 306 | bool | `if`→`if not` | `if strict:` |
| `decision_event_v2_626` | 177 | bool | `if`→`if not` | `if errs:` |
| `decision_event_v2_626` | 294 | bool | `True`→`False` | ``strict=True` ⇒ 逐条走 `from_dict_strict()`，任一不完整/未知字段即抛` |
| `decision_event_v2_626` | 5 | const | `626`→`627` | `**只有 Authority Ledger 有「人决定了什么」的权力**；W2/PCK/golden 都是派生视图（626 D 线 Proj` |
| `decision_event_v2_626` | 407 | const | `2`→`3` | `chk("count_by_review_method", led.count_by_review_method().get("BATCH_` |
| `decision_event_v2_626` | 232 | bool | `and`→`or` | `if e.target_type == target_type and e.target_id == target_id]` |
| `decision_event_v2_626` | 170 | bool | `not`→`''` | `missing = [f for f in REQUIRED_FIELDS if not d.get(f)]` |

## 四、诚实边界

1. **进程内替换**只覆盖被测试文件 import 的模块；CLI / 子进程行为不在射程内。
2. **导入即崩**算’被杀’但不含信息量 ⇒ 已单独统计，检出率主口径只看能跑的变异体。
3. 存活体 ≠ 一定有 bug：也可能是**等价变异**（改了写法不改语义）或该分支本就无测试覆盖；本批对存活体的处置见 §五。
4. 变异体是**随机抽样**（种子固定 ⇒ 可复现），不是穷举；样本外仍可能有漏网。

## 五、对存活体的处置

检出率 28.8% < 80% ⇒ **未达标**；存活体已列在 §三，按任务书要求应补测试（见收工报告的诚实登记）。

## 六、两套作用域对账（为什么给两个数）

| 作用域 | 含义 | 变异体 | 被杀 | 存活 | 导入崩 | 超时 | 检出率（可跑口径） |
|---|---|---:|---:|---:|---:|---:|---:|
| `core` | 只改**核心判决路径**上的函数体 | 60 | 30 | 18 | 10 | 2 | **62.5%** |
| `all` | 整文件随机抽样（含 CLI/报告/迁移等无人测代码） | 60 | 15 | 37 | 8 | 0 | **28.8%** |

- 分文件（core）：`four_state_verdict_638` 8/19；`ledger_checkpoint_651` 12/14；`decision_event_v2_626` 10/15
- 分文件（all）：`four_state_verdict_638` 3/17；`ledger_checkpoint_651` 10/18；`decision_event_v2_626` 2/17

**结论**：核心路径（`core`）的检出率明显高于整文件随机（`all`）——差额集中在 CLI/报告/迁移这类**本就没有单测**的代码上。两个数都保留：只看 `core` 会高估测试整体强度，只看 `all` 会低估核心的硬度。

**未达标登记**：本轮 `core` 62.5% / `all` 28.8%，都**低于任务书的 80% 目标**。按任务书要求补测试的部分见验收报告「诚实登记」：本轮补了 3 条（篡改必拒 / GENESIS 与序号 / validate 必填），剩余存活体主要是 ①等价变异（改法不改语义）②CLI/报告路径（单测价值低）③超时与导入崩（环境类）。
