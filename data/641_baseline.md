# 641 · 开工快照（任务 0.0）

> 采集时间 2026-09-26。数字**全部实测**，不抄历史快照。
> 采集脚本只读（git status / 目录计数 / `gate_engine.RULES` / `w2_derived_640c.pinned()` / ruff / tool_integrity / control_char 扫描）。

## 一、仓库状态

| 项 | 实测 |
|---|---|
| HEAD | `83f72122` 640b [E1] 总收尾报告 |
| `origin/master..HEAD` | **38**（未 push，640b/640c 全区间） |
| `git status` 总条目 | **139**（staged 1 / unstaged 49 / untracked 89） |
| 受控目录污染（atoms/evidence/Examples/Book） | **0**（`git status` 无一条命中） |
| 规模 | 工具 **439** · 测试 **440** · 规则 **67** |
| ruff（tools/ + tests/） | All checks passed |
| `tool_integrity --check` | 4/4 全绿（core 5 / 信任根 5 / Merkle / 尺子 22） |
| `control_char_cleaner --check`（data/） | **0** 文件含控制字符 |

## 二、139 项的构成（按 640c 交接单核对）

| 组 | 说明 |
|---|---|
| 640c 本轮改动（工具 5 + 测试 7 + 新增 2） | `tools/w2_derived_640c.py`(新)、`tools/defense_chain.py`、`tools/argument_audit.py`、`tools/defense_chain_deepen.py`、`tools/metrics_611.py`、`tools/.tool_checksums`；`tests/` 7 个（含新增 `test_w2_derived_640c.py`） |
| 640c 重生成的入库产物 | `data/argument_audit_report.md`、`data/defense_chain.html`、`data/defense_chain_report.md`、`data/defense_chain_deepen_611.md`、`data/out_mis_review_support_611.md` |
| 640c 证据产物 | `data/640c_baseline.md`、`data/640c_task0_subset.txt`、`data/640c_pytest_final.txt`、`data/640c_b20_recheck.txt`、`_auto/outbox/640c.md`、`_auto/status.json` |
| 640/640b 遗留未提交 | 批次产物（`data/640_*.md`、`data/640b_*.md` 等） |
| 更早批次未跟踪资产 | `data/637_*`、`tools/*_637.py`、`tests/test_*_637.py`、`tools/queyi_core_*_625.py`、`data/_archive_633/` 等 |
| 非本工程资产 | `_arch_v19`…`_arch_v28*`（调研快照，`??`） |

**结论**：与 640c 交接单一致，无新增未知项；`_auto/status.json` 为唯一 staged 项（640b 遗留，随 0.5 统一 commit）。

## 三、W2 权威现值（`tools/w2_derived_640c.py`）

```
节点 121（命题 79 + 误解 42）· 边 388（击败 194）
IN 79 / OUT 42 / UNDEC 0
可信度 high 79 / medium 35 / low 7
OUT MIS 42 · 无辩护者节点 46
两路交叉校验 consistent = True（现算 == 入库产物）
```

与 §一"现状基线"给出的一致 ✓，与 640c 交接单一致 ✓。

## 四、Core 雏形（本轮要收敛的对象）

| 文件 | 现状 |
|---|---|
| `tools/queyi_core_interface_design_625.py` | 625 期接口设计（非运行时） |
| `tools/queyi_core_interface_v02_631.py` | 5 接口 25 方法，**抽象** |
| `tools/queyi_core_interface_v03_632.py` | 仅 Evidence 接口真实适配，其余 4 个空定义 |
| `tools/queyi_core_trigger_check_625.py` | 剥离触发标准自检（3/5） |

## 五、已知残留

1. **偶发测试**：`tests/test_poison_coverage_581.py::test_injected_ghost_comment_does_not_inflate_coverage`
   —— 640c 两次全量：第 1 次 3 红（均为本机 PowerShell 重定向写出 UTF-16 产物的控制字符副作用，已修）；
   第 2 次 **1 红**即此项。单跑 ✅、`-k poison` 组 ✅、`-k test_p` 组 ✅ ⇒ 顺序/负载敏感，未定位。
   线索：`poison_drill.behavioral_covered()` 用模块级 `_LAST_BEHAVIORAL_COVERED` 缓存；测试对
   **同一实现的两个模块副本**各跑一次完整 `drill()` 并断言集合相等；`drill()` 内含
   `replay._acquire_replay_lock(wait_timeout=5, stale_after=300)` 等重活（已标记工具内部行号）。
   本轮任务 0.1/0.2 处置。
2. 640 验收报告 §七 引用"见 §八"，但报告**无 §八**（640b 遗留）⇒ 任务 0.4 一并处理。
3. 交人裁决（不代决）：approve 的 MIS 是否抬到 high（命题人签 high ⇒ OUT MIS 1→42、无辩护者 7→46）。

## 六、本轮硬边界（开工前确认）

- 5 个 CORE_TOOLS 判决逻辑**零改动**；Core 为新增并行层
- 受控目录零污染；不代签、不 golden accept、不 push
- 落盘一律 `encoding="utf-8", newline="\n"`（§四.7）
