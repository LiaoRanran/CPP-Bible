# ADR-0004：G3 Rule 引擎挂接点 = 复用 `cppbible.py` 执行器，收敛双清单

- 状态：**已接受**（2026-09-10，G1 附加调研，用户 G0 答复第 1 条附加指令）
- 决策人：架构师提议，随 G1 交付报人确认

## 背景（已查证事实）

用户附加指令要求：G3 的 Rule 引擎**直接对接现有 quality 执行器，不另起独立 CI 系统**。调研 `tools/cppbible.py` 得：

1. `cmd_check()` 的门禁清单是**硬编码元组列表**：`(name, [python, tools/xxx.py, args...])`，逐项 `subprocess` 执行、退出码即判定、非 0 即整条红。
2. `pyproject.toml:quality_gates`（17 条）是**另一份独立清单**——与 `cmd_check` 内容重叠但各自维护，属于双事实源。

## 决策

G3 的 Rule 引擎产出**编译为现有元组结构**注入 `cmd_check`：

- `Rule` 接口（`selector → check → severity → message → fix_hint`）在注册器内登记；
- 注册器提供 `compile_to_gates() -> list[tuple[str, list[str]]]`，把可程序化规则编译成 `(name, [cmd...])` 元组；
- `cmd_check` 增加一个来源：内置元组 ∪ 注册器产出，**合并后仍是同一执行循环**（退出码语义、报告格式不变）；
- `pyproject:quality_gates` 在 G3 收敛时降级为**生成物或废弃**，杜绝双清单漂移。

## 候选与否决

**候选 B：另起独立 gate runner（新 CLI）。**
否决：形成第二套 CI 入口——新旧两份门禁清单会各自漂移（今天 `cmd_check` 与 `pyproject` 的重叠已是证据）；且丢失现有退出码约定、pre-push 复用链（`prepush_check.py` 直接调工具脚本）与 CI quality job 的既有接线。

## 后果

- 正面：现有 CI/pre-push/报告格式零改动；规则注册器与执行器解耦，规则可单测（tests/ 已有先例）。
- 负面：Rule 引擎的表达力受限于"退出码即判定"——LLM 语义类规则本就按 DRQ-5 不做阻断判定，故无损失；`severity` 分级需在报告文本层表达而非退出码层。
- 约束：G3 落地时必须先给 `cmd_check` 的清单加**来源标注**（内置/注册器），否则收敛无法验证。
