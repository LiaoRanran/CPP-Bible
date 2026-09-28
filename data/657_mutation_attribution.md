# 657 C · 剩余存活体逐条归因

> 工具：`tools/mutation_attribution_657.py`（只读；数据源 `data/656_mutation_report_{core,all}.json`）。

## 一、达标对照

| 作用域 | 被杀/计分 | 检出率 | 目标 | 判定 | 导入崩 | 超时 | 剩余存活 |
|---|---|---:|---|---|---:|---:|---:|
| `core` | 110/113 | **97.3%** | ≥80% | 达标 | 30 | 4 | 3 |
| `all` | 128/157 | **81.5%** | ≥60% | 达标 | 61 | 5 | 29 |

> 口径：分母 = 被杀 + 存活（**导入即崩**与**超时**单独统计、不计入分母——前者不含信息量，后者是「跑飞」而非「没抓到」）。

## 二、core 存活体归因（3 条）

- 等价变异：**3**；CLI/IO 路径：**0**；现有杀测试未覆盖：**0**。

| 目标 | 行 | 算子 | 改了什么 | 落点函数 | 归因 |
|---|---:|---|---|---|---|
| `four_state_verdict_638` | 190 | cmp | `==`→`!=` | `classify_card` | equivalent |
| `decision_event_v2_626` | 244 | bool | `or`→`and` | `get_current` | equivalent |
| `decision_event_v2_626` | 246 | bool | `if`→`if not` | `get_current` | equivalent |

## 二、all 存活体归因（29 条）

- 等价变异：**3**；CLI/IO 路径：**25**；现有杀测试未覆盖：**1**。

| 目标 | 行 | 算子 | 改了什么 | 落点函数 | 归因 |
|---|---:|---|---|---|---|
| `four_state_verdict_638` | 267 | const | `2`→`3` | `write_report` | cli_io |
| `four_state_verdict_638` | 380 | const | `2`→`3` | `main` | cli_io |
| `four_state_verdict_638` | 384 | const | `2`→`3` | `main` | cli_io |
| `four_state_verdict_638` | 190 | cmp | `==`→`!=` | `classify_card` | equivalent |
| `four_state_verdict_638` | 370 | const | `2`→`3` | `main` | cli_io |
| `four_state_verdict_638` | 379 | const | `3`→`4` | `main` | cli_io |
| `ledger_checkpoint_651` | 295 | const | `2`→`3` | `main` | cli_io |
| `ledger_checkpoint_651` | 281 | bool | `if`→`if not` | `main` | cli_io |
| `ledger_checkpoint_651` | 186 | const | `300`→`301` | `build_checkpoint` | cli_io |
| `ledger_checkpoint_651` | 290 | const | `2`→`3` | `main` | cli_io |
| `ledger_checkpoint_651` | 170 | bool | `if`→`if not` | `_leaves_from_ledger` | cli_io |
| `ledger_checkpoint_651` | 176 | bool | `True`→`False` | `_sig` | cli_io |
| `ledger_checkpoint_651` | 198 | bool | `if`→`if not` | `build_checkpoint` | cli_io |
| `ledger_checkpoint_651` | 189 | bool | `if`→`if not` | `build_checkpoint` | cli_io |
| `ledger_checkpoint_651` | 215 | bool | `not`→`''` | `verify_checkpoint_file` | cli_io |
| `ledger_checkpoint_651` | 226 | bool | `and`→`or` | `verify_checkpoint_file` | cli_io |
| `ledger_checkpoint_651` | 218 | bool | `if`→`if not` | `verify_checkpoint_file` | cli_io |
| `ledger_checkpoint_651` | 192 | bool | `not`→`''` | `build_checkpoint` | cli_io |
| `ledger_checkpoint_651` | 200 | bool | `not`→`''` | `build_checkpoint` | cli_io |
| `ledger_checkpoint_651` | 227 | bool | `and`→`or` | `verify_checkpoint_file` | cli_io |
| `ledger_checkpoint_651` | 216 | bool | `False`→`True` | `verify_checkpoint_file` | cli_io |
| `ledger_checkpoint_651` | 219 | bool | `False`→`True` | `verify_checkpoint_file` | cli_io |
| `decision_event_v2_626` | 246 | bool | `if`→`if not` | `get_current` | equivalent |
| `decision_event_v2_626` | 360 | bool | `True`→`False` | `_raises` | cli_io |
| `decision_event_v2_626` | 244 | bool | `or`→`and` | `get_current` | equivalent |
| `decision_event_v2_626` | 320 | bool | `False`→`True` | `load_ledger` | cli_io |
| `decision_event_v2_626` | 358 | bool | `False`→`True` | `_raises` | cli_io |
| `decision_event_v2_626` | 472 | bool | `if`→`if not` | `main` | cli_io |
| `decision_event_v2_626` | 280 | bool | `if`→`if not` | `independent_human_review_count` | not_in_kill_scope |

## 三、等价变异的逐条理由（**只有核实过的才标 equivalent**）

- `decision_event_v2_626` L244：`e.supersedes or []` 改成 `and []`：**合法账本**里 `supersedes` 只指向更早的事件，因此最新一条必然不在 superseded 集合里 ⇒ `alive[-1] == evs[-1]`，两个写法同结果。（`supersedes` 若指向前方事件——本仓无此产生路径——才可能不同。）
- `decision_event_v2_626` L246：`alive[-1] if alive else evs[-1]` 改成 `if not alive`：同上，合法账本下 `alive[-1] == evs[-1]`，两分支等价。
- `four_state_verdict_638` L190：`status == "verified" and not m` 改成 `!=`：`_raw_state("")` 本身也判 `pass`，所以「改写 verdict」与「不改写」在 status=verified 且无显式 falsification 时结果相同；而一旦有显式 falsification，`not m` 为假使整条条件恒假 ⇒ 两者同样都不改写。

## 四、诚实边界

1. `equivalent` 只给**人工逐条核过**的 3 条；其余存活体一律按落点归类，**不为了把数字做好看而标等价**。
2. `cli_io` / `not_in_kill_scope` ≠ 不可测：它们是「本轮杀测试文件没覆盖到」，补测需另建夹具（CLI 断言 / HMAC checkpoint 文件），成本已如实登记。
3. `超时` 的变异体**是被发现**的（表达式跑飞），只是按工具口径不计入「被杀」，故不出现在本表。
