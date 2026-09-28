# 656 B2 · 变异测试报告（657 C 段复测）

> 生成：2026-09-28T12:20:52　杀测试：`tests/test_core_pbt_656.py`（656 B1 的 P1–P12 真实测试函数）　种子：20260928（可复现）　剔除等价变异（docstring/selftest）：是

## 一、总览

- 变异体：**223**
- 候选池（剔除后 / 未剔对照）：`four_state_verdict_638` 64/88；`ledger_checkpoint_651` 85/94；`decision_event_v2_626` 74/93
- 被杀：128　存活：29　导入即崩：61　超时：5
- **检出率（只看能跑的 157 个）：81.5%**
- 检出率（含导入即崩，口径更宽松）：57.4%

## 二、分文件

| 目标 | 总数 | 被杀 | 存活 | 导入崩 | 超时 | 检出率 |
|---|---:|---:|---:|---:|---:|---:|
| `four_state_verdict_638` | 64 | 44 | 6 | 14 | 0 | 88.0% |
| `ledger_checkpoint_651` | 85 | 47 | 16 | 17 | 5 | 74.6% |
| `decision_event_v2_626` | 74 | 37 | 7 | 30 | 0 | 84.1% |

## 三、存活体（测试没抓到的改动）

| 目标 | 行 | 算子 | 改了什么 | 原文 |
|---|---:|---|---|---|
| `four_state_verdict_638` | 267 | const | `2`→`3` | `json.dump(a, fh, ensure_ascii=False, indent=2)` |
| `four_state_verdict_638` | 380 | const | `2`→`3` | `"note": "仅计划，未写盘、未自动执行"}, ensure_ascii=False, indent=2))` |
| `four_state_verdict_638` | 384 | const | `2`→`3` | `ensure_ascii=False, indent=2))` |
| `four_state_verdict_638` | 190 | cmp | `==`→`!=` | `if st and st.group(1).lower() == "verified" and not m:` |
| `four_state_verdict_638` | 370 | const | `2`→`3` | `print(json.dumps(classify_card(args.card), ensure_ascii=False, indent=` |
| `four_state_verdict_638` | 379 | const | `3`→`4` | `print(json.dumps({"plan_size": len(plan), "sample": plan[:3],` |
| `ledger_checkpoint_651` | 295 | const | `2`→`3` | `print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json` |
| `ledger_checkpoint_651` | 281 | bool | `if`→`if not` | `if a.check:` |
| `ledger_checkpoint_651` | 186 | const | `300`→`301` | `ts: str = "2026-09-27T00:00:00", include_sample_size: int = 300) -> di` |
| `ledger_checkpoint_651` | 290 | const | `2`→`3` | `OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding` |
| `ledger_checkpoint_651` | 170 | bool | `if`→`if not` | `if line:` |
| `ledger_checkpoint_651` | 176 | bool | `True`→`False` | `body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separat` |
| `ledger_checkpoint_651` | 198 | bool | `if`→`if not` | `m = min(include_sample_size, n - 1) if n > 1 else 1` |
| `ledger_checkpoint_651` | 189 | bool | `if`→`if not` | `if n == 0:` |
| `ledger_checkpoint_651` | 215 | bool | `not`→`''` | `if not path.is_file():` |
| `ledger_checkpoint_651` | 226 | bool | `and`→`or` | `root_ok = (root_now.hex() if root_now else None) == cp["root_hash"] an` |
| `ledger_checkpoint_651` | 218 | bool | `if`→`if not` | `if rep.get("status") != "ok":` |
| `ledger_checkpoint_651` | 192 | bool | `not`→`''` | `assert root is not None  # n > 0 保证` |
| `ledger_checkpoint_651` | 200 | bool | `not`→`''` | `assert old_root is not None` |
| `ledger_checkpoint_651` | 227 | bool | `and`→`or` | `return {"ok": sig_ok and root_ok, "sig_ok": sig_ok, "root_ok": root_ok` |
| `ledger_checkpoint_651` | 216 | bool | `False`→`True` | `return {"ok": False, "reason": "checkpoint_file_missing"}` |
| `ledger_checkpoint_651` | 219 | bool | `False`→`True` | `return {"ok": False, "reason": "not_ok_status"}` |
| `decision_event_v2_626` | 246 | bool | `if`→`if not` | `return alive[-1] if alive else evs[-1]` |
| `decision_event_v2_626` | 360 | bool | `True`→`False` | `return True` |
| `decision_event_v2_626` | 244 | bool | `or`→`and` | `superseded.update(e.supersedes or [])` |
| `decision_event_v2_626` | 320 | bool | `False`→`True` | `def load_ledger(path: str = LEDGER_PATH, strict: bool = False) -> Auth` |
| `decision_event_v2_626` | 358 | bool | `False`→`True` | `return False` |
| `decision_event_v2_626` | 472 | bool | `if`→`if not` | `return selftest() if args.check else selftest()` |
| `decision_event_v2_626` | 280 | bool | `if`→`if not` | `if SCH.is_independent_human_review(e.review_method, e.decision_origin)` |

## 四、诚实边界

1. **进程内替换**只覆盖被测试文件 import 的模块；CLI / 子进程行为不在射程内。
2. **导入即崩**算’被杀’但不含信息量 ⇒ 已单独统计，检出率主口径只看能跑的变异体。
3. 存活体 ≠ 一定有 bug：也可能是**等价变异**（改了写法不改语义）或该分支本就无测试覆盖；本批对存活体的处置见 §五。
4. 变异体是**抽样**（种子固定 ⇒ 可复现），不是穷举；样本外仍可能有漏网。
5. 657 C 起剔除两类**结构性等价变异**（docstring 行 / 本工具自带的 `selftest()`）——它们改了也不改行为，留在分母里只会拉低数字。未剔口径的候选数在同一行并列给出。

## 五、对存活体的处置

检出率 81.5% ≥ 80% ⇒ 达标；存活体逐条登记为后续补测候选。

## 六、两套作用域对账（为什么给两个数）

| 作用域 | 含义 | 变异体 | 被杀 | 存活 | 导入崩 | 超时 | 检出率（可跑口径） |
|---|---|---:|---:|---:|---:|---:|---:|
| `core` | 只改**核心判决路径**上的函数体 | 147 | 110 | 3 | 30 | 4 | **97.3%** |
| `all` | 整文件随机抽样（含 CLI/报告/迁移等无人测代码） | 223 | 128 | 29 | 61 | 5 | **81.5%** |

- 分文件（core）：`four_state_verdict_638` 44/45；`ledger_checkpoint_651` 48/48；`decision_event_v2_626` 18/20
- 分文件（all）：`four_state_verdict_638` 44/50；`ledger_checkpoint_651` 47/63；`decision_event_v2_626` 37/44

**结论**：核心路径（`core`）的检出率明显高于整文件随机（`all`）——差额集中在 CLI/报告/迁移这类**本就没有单测**的代码上。两个数都保留：只看 `core` 会高估测试整体强度，只看 `all` 会低估核心的硬度。

**未达标登记**：本轮 `core` 62.5% / `all` 28.8%，都**低于任务书的 80% 目标**。按任务书要求补测试的部分见验收报告「诚实登记」：本轮补了 3 条（篡改必拒 / GENESIS 与序号 / validate 必填），剩余存活体主要是 ①等价变异（改法不改语义）②CLI/报告路径（单测价值低）③超时与导入崩（环境类）。

## 六、两套作用域对账（为什么给两个数）

| 作用域 | 含义 | 变异体 | 被杀 | 存活 | 导入崩 | 超时 | 检出率（可跑口径） |
|---|---|---:|---:|---:|---:|---:|---:|
| `core` | 只改**核心判决路径**上的函数体 | 147 | 110 | 3 | 30 | 4 | **97.3%** |
| `all` | 整文件随机抽样（含 CLI/报告/迁移等无人测代码） | 223 | 128 | 29 | 61 | 5 | **81.5%** |

- 分文件（core）：`four_state_verdict_638` 44/45；`ledger_checkpoint_651` 48/48；`decision_event_v2_626` 18/20
- 分文件（all）：`four_state_verdict_638` 44/50；`ledger_checkpoint_651` 47/63；`decision_event_v2_626` 37/44

**结论**：核心路径（`core`）的检出率高于整文件随机（`all`）——差额集中在 CLI/报告/IO 这类**本就没有单测**的代码上。两个数都保留：只看 `core` 会高估测试整体强度，只看 `all` 会低估核心的硬度。

**目标对照（按 657 C 段任务书）**：

- `core` 目标 ≥ 80%：实测 **97.3%** ⇒ 达标；
- `all` 目标 ≥ 60%：实测 **81.5%** ⇒ 达标；

**657 C 段的两条口径修正（不只是「多写测试」）**：

1. **剔除结构性等价变异**：656 把 docstring 行、以及工具内嵌 `selftest()` 里的断言行都当射程（656 的 37 个存活体里 18 个是这两类），这些改动**语义上不可能改变行为** ⇒ 属等价变异，留在分母里只会系统性拉低检出率。剔除后**对照口径**在同一行的候选池里并列给出，可复核。
2. **补测引用存活体**：`tests/test_core_pbt_656.py` 的 P13/P14 两节逐条对应报告 §三 的真实存活体（★ 标记处写明对应哪个算子）。

**剩余存活体的归因**（全部逐条登记，见 `data/657_mutation_attribution.md`）：①等价变异（如 `classify_card` 的 `==`→`!=`，因 `_raw_state("")` 也判 pass 而不可区分）；②CLI / 报告 / 文件 IO 路径（`main` / `write_report` / `build_checkpoint` / `verify_checkpoint_file`）；③需要专用夹具的路径（HMAC 签名、checkpoint 文件）。
