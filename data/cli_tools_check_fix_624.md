# 624 D1 · 3 个 CLI 工具补 `--check`

> 背景：623 的 3 个 CLI 工具缺 `--check`（违"新工具必有 --check"铁律）：
> `authority_to_annotations_sync_623.py`、`w2_recompute_623.py`、`run_623_gate.py`。
> 本任务补 `--check`（**只读**，不写盘）。

---

## 一、补 `--check` 详情

| 工具 | `--check` 检查项 | 结果 |
|---|---|---|
| **authority_to_annotations_sync_623.py** | authority 日志存在 / annotations 存在 / 两 JSONL 可解析 / power 映射（不匹配仅 info）/ `sync()` 可计算 | ✅ exit 0 |
| **w2_recompute_623.py** | annotations 存在 / synced 存在 / 两 JSONL 可解析 / `verdicts([]) == {}` | ✅ exit 0 |
| **run_623_gate.py** | 目标目录存在 / 枚举到 .py / ruff 可用（探针） | ✅ exit 0 |

## 二、`--check` 验证结果

```
authority_to_annotations_sync_623.py --check  → D1 check: PASS  exit=0
w2_recompute_623.py --check                   → D2 check: PASS  exit=0
run_623_gate.py --check                       → gate check: PASS  exit=0
```
**3/3 exit 0。**

> 附注：`authority` 日志出现 `power=OVERRIDE` 不在 `POWER_MAP`（`ACCEPT/REJECT/MODIFY/ESCALATE/DEFER`）——
> 按现有逻辑回落默认 `approve`；`--check` 将其列为 **info**（不 fail），与既有行为一致。

## 三、铁律遵守

- `--check` **只读**，不写盘（3 个工具的 check() 均无写操作）。
- 未改工具判决逻辑，仅新增只读检查分支与参数。
- 修改工具后同 commit 运行 `tool_integrity.py --update` 重钉（若在保护清单内）。

## 四、局限性声明

1. `--check` 只做**输入/可运行性**检查，不校验业务正确性（那由 pytest 覆盖）。
2. `power=OVERRIDE` 的语义未在 `POWER_MAP` 显式建模（沿用默认 approve），留 625 澄清。
