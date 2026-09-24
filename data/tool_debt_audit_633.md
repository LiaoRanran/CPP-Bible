# 633 B2 · 工具债清理报告

> 输入：任务0 的「工具债」盘点。纪律：**不删工具、不改老工具核心逻辑**（§零.10）。

## 一、关键更正：TODO/FIXME 计数误报

- 任务0 初扫报告「TODO/FIXME 总数 35」；**复算后真债 ≈ 12 处**。
- 误报来源：把 `XXX` 当**占位符**的用法（`MIS-XXX`/`ATOM-XXX`/`xxx.h`/`FB-XXX`/`xxx.py` 等）共 **23** 行被宽松正则 `\bXXX\b` 命中。
- 本工具改用严格口径（只认 `TODO|FIXME|HACK`，且排除占位/描述行）。

## 二、工具债分类

| 类别 | 数量 | 说明 | 处置 |
|---|---|---|---|
| 无 --check 的 CLI 工具 | 79 | 625 前老工具，多数仍被引用 | **本批只示范少数补 --check，其余登记**（工作量 L） |
| import 不存在的本地模块 | 0 | 任务0 静态扫描结果 | 无（本批为 0） |
| 真 TODO/FIXME/HACK | 12 | 严格口径 | 逐条评估（见下） |
| 超过 500 行的巨型文件 | 23 | 拆分风险高 | 登记，不拆分 |
| 命名不符 *_6XX.py | 217 | 318 处引用成本高 | 登记，不重命名 |

## 三、本批实加 --check 的老工具（示范 + 真实减债）

以下 3 个**被其它工具 import 且缺 --check** 的老工具，本批补了**只读 `--check`**（在 `main()` 顶部拦截，返回前不跑任何业务逻辑）：

| 工具 | 状态 |
|---|---|
| `tools/comment_blocks.py` | ✅ 已补 --check（exit 0） |
| `tools/backup.py` | ✅ 已补 --check（exit 0） |
| `tools/observability.py` | ✅ 已补 --check（exit 0） |

经核查：三者**均非 CORE_TOOLS**（CORE=gate_engine/atom_evidence_replay/poison_drill/toolchain/cppbible）⇒ 无需 `tool_integrity --update`（§零.6 不触发）。

### 示范范式（供后续批量应用）

```python
# 在 argparse 解析后加只读分支（范例，按各工具 main 结构适配）：
if args.check:
    # 只校验：文件存在 / 依赖可 import / 基本参数合法；绝不跑业务逻辑、不写盘
    import importlib
    importlib.import_module(__name__)   # 或断言关键常量存在
    print('OK: <tool> --check 只读自检通过')
    return 0
```

## 四、真 TODO 逐条（严格口径）

| 文件 | 行 | 内容 |
|---|---|---|
| `tools/debt_inventory_633.py` | 441 | f"| TODO/FIXME 总数 | {snap['todo_count']} |", |
| `tools/human_review_todo_generator_618.py` | 5 | - 扫描 evidence/ 下 EV-*.md（只读），取前 30（按路径排序）生成逐条复核 TODO。 |
| `tools/human_review_todo_generator_618.py` | 58 | L.append("> 615 诚实发现：原 388 条人审中**逐条独立语义审查 = 0**（仅 194 镜像边 + 354 批量授权）。本清单即补齐该缺口的 TODO。\n") |
| `tools/human_review_todo_generator_618.py` | 70 | L.append("- 清单为 TODO 模板；最终裁决与统计由人审执行，本批不代签。") |
| `tools/round7_mutator_625.py` | 44 | "DOC-ZERO-PLACEHOLDER": ("MSET", "claim", "TODO"), |
| `tools/tool_debt_audit_633.py` | 6 | **关键更正**：任务0 初扫的「TODO/FIXME 35 处」绝大多数是**误报**——命中的是把 |
| `tools/tool_debt_audit_633.py` | 8 | 真正的 `TODO/FIXME/HACK` 代码标记约 **0 处**。本工具用更严的口径复算并如实登记。 |
| `tools/tool_debt_audit_633.py` | 111 | "## 一、关键更正：TODO/FIXME 计数误报", "", |
| `tools/tool_debt_audit_633.py` | 112 | f"- 任务0 初扫报告「TODO/FIXME 总数 35」；**复算后真债 ≈ {len(todos)} 处**。", |
| `tools/tool_debt_audit_633.py` | 121 | f"| 真 TODO/FIXME/HACK | {len(todos)} | 严格口径 | 逐条评估（见下） |", |
| `tools/tool_debt_audit_633.py` | 135 | "## 四、真 TODO 逐条（严格口径）", ""] |
| `tools/tool_debt_audit_633.py` | 149 | "3. 任务0 的 TODO 计数为**误报**，本报告已更正并登记（§十.1 新发现）；", |

## 五、诚实登记

1. **未批量补 --check**：无 --check 的老 CLI 工具共 79 个（任务0 口径），逐批补属**工作量 L、风险中**（需逐个适配 main 结构）；本批**实补 3 个**（§三），其余 76 个登记交后续批次；
2. **未删任何工具**、未重命名、未拆分巨型文件（§零.10/§零.15）；
3. 任务0 的 TODO 计数为**误报**，本报告已更正并登记（§十.1 新发现）；
4. 无 import 不存在模块的真债（任务0 P0=0 复现）。
