# 640 A4 · 老工具 --check 补齐 + 守卫劫持修复

> 扫描时间：2026-09-25。方法：全量扫描 tools/*.py（434 个）中的 `--check` 字样与 CLI 结构。

## 一、扫描结论（D12 的最终账）

| 项 | 数 |
|---|---|
| tools/*.py 总数 | 434 |
| 有 `--check` | 430 |
| 缺 `--check` | **4**（全部为无 CLI 入口的库/脚本模块，见下） |

**D12（633 登记 79 个）实际早已在 634 A2 批量补齐**——本次扫描是终验，剩余 4 个均属
"不适合 --check"类，逐一标注：

| 工具 | 处置 | 原因 |
|---|---|---|
| `_clean_junk.py` | 例外：纯库模块 | 只定义 `JUNK_RE` 常量供他具 import，无 CLI 入口、无业务可跳过 |
| `utf8_console.py` | 例外：纯库模块 | 只提供 `ensure_utf8()` 函数（toolchain 等导入使用），无入口 |
| `viso_diff.py` | 例外：纯库模块 | 只定义 `judge_delete_mechanism` 等判据函数，无入口 |
| `env_check.py` | 例外：脚本即体检 | 模块级直跑只读环境体检并 exit(1 if RED)；默认行为与 --check 语义等同，且模块级执行结构不适配守卫范式（见 §二） |

## 二、守卫劫持真 bug（634 A2 范式缺陷，本次修复）

**病**：634 A2 把 `if "--check" in sys.argv: print("OK..."); sys.exit(0)` 守卫插在
**模块级**。对被其他工具 import 的模块，import 时守卫读到的是**外层进程**的 argv ⇒
打印 OK 并 `sys.exit(0)`，**劫持调用方**。

**实证**：`replay_invariants.py --check` 从未真正运行过不变量——输出被导入链上的
`toolchain` 守卫劫持为 `OK: toolchain --check…`（5 项测试因此常红，且"绿灯"是假的）。

**修复**：
1. `toolchain.py`（被 atom_evidence_replay/cppbible/hy3_check 等导入）守卫移入 `__main__`；
2. 审计工具 `tools/guard_audit_640.py`（`--check` 语义：只读审计，可重复运行）：
   全库 79 个守卫工具中 **8 个有劫持风险**（被其他 tools/*.py import）：
   chapter_compile_check / compile_all / impact_analysis / mutation_fuzz /
   overturned_events / prop_closure / prop_graph / stat_bounds —— 守卫全部移入
   各自 `__main__`；
3. 回归锁 `tests/test_guard_hijack_640.py`（4 例）：带 `--check` argv 导入不被劫持、
   直跑 `--check` 仍 exit 0、replay_invariants 恢复真实不变量输出。

**验收**：`replay_invariants --check --no-heavy` 输出 5 项真实不变量全过 ✓；
430 个有 --check 的工具行为不变；4 个例外已注明理由。
