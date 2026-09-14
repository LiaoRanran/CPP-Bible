# pytest 耗时分析报告（499 任务1）

> 数据源：`_pt499_dur.txt`（`pytest tests/ -q --durations=30`，2026-09-14 实跑，354 点）
> 另附实跑探针：全仓 walk 统计（见 §5）

## 0. 总耗时（口径说明，重要）

| 项 | 值 | 出处 |
|---|---|---|
| 测试总数 | **354** 点（进度点 5 行，无 `F`/`E`） | `_pt499_dur.txt` 首 5 行 |
| Top 30 合计 | **490.56s（8.18 min）** | `_pt499_dur.txt` 30 行求和（脚本精算） |
| 全量总耗时 | **≈ 642s（10.7 min）** ⇐ **未能从本次输出取得** | 提示词〇「开工基线」实测值 |

**为什么本次拿不到总耗时汇总行（如实记录，不编造）**：本批两次重跑（`Start-Process` 重定向、以及 `python -u` 无缓冲重定向）都在 pytest **session 收尾**被沙箱包装器阻断——stderr 出现
`[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] {"count":533,"threshold":500,...pytest-of-ASUS}`，
该包装器因批量删 tmp（>500 项）要求确认，session 以非零码结束且**汇总行 `354 passed in Xs` 未落盘**；stdout 只留下进度点（405 B）。测试本身**无失败**（全 `.`）。
→ 全量总耗时引用提示词〇的 498 收工实测基线 ≈642s；Top 30 占比按此计 ≈ **76.4%**。

## 1. 分类统计（Top 30 内）

| 类别 | 数量 | 合计耗时 | 占 Top30 | 判定依据 |
|---|---|---|---|---|
| **编译类**（实际调 g++/replay 真编译） | 16 | **299.64s** | **61.1%** | 测试体 `subprocess` 调 `golden_lock.py` / `atom_evidence_replay.py` / `poison_drill.py`，后两者源码明写「走真编译」 |
| **纯逻辑类**（字符串/规则判定，不编译） | 12 | **189.36s** | 38.6% | 只调 `gate_engine` 规则函数 / 读配置文件 |
| **IO 类**（读文件/进程协调，不编译） | 2 | **1.56s** | 0.3% | `test_lock_serializes_processes`(3.23)、`test_backfill_from_git`(0.26) |

> 分类依据：`tests/test_json_output.py`（`_run` 用 `subprocess.run([PY, tools/*.py...])`）、`tools/poison_drill.py` 第 21 行注释「P2 走真编译（与 replay 契约一致）」+ 第 116 行 `replay.replay_card(...)`、`tools/golden_lock.py` 第 111 行 `replay.replay_card(p, ...)`。

## 2. Top 10 最慢测试（按耗时降序）

| # | 测试名 | 文件 | 耗时(s) | 类别 |
|---|---|---|---|---|
| 1 | test_golden_lock_json | tests/test_json_output.py | **176.21** | 编译类 |
| 2 | test_contains_in_text_empty_or_cjk_blocked | tests/test_gate_engine.py | **79.73** | 纯逻辑类 ⚠️ |
| 3 | test_poison_drill_json | tests/test_json_output.py | **57.15** | 编译类 |
| 4 | test_contains_in_text_generic_mnemonic_advice | tests/test_gate_engine.py | **52.25** | 纯逻辑类 ⚠️ |
| 5 | test_poison_drill_all_caught_and_negative_passes | tests/test_s1_s6.py | **49.55** | 编译类 |
| 6 | test_contains_in_text_specific_passes | tests/test_gate_engine.py | **42.72** | 纯逻辑类 ⚠️ |
| 7 | test_replay_json | tests/test_json_output.py | 5.03 | 编译类 |
| 8 | test_gate_engine_json | tests/test_json_output.py | 4.24 | 纯逻辑类 |
| 9 | test_lock_serializes_processes | tests/test_p0g_lock.py | 3.23 | IO 类 |
| 10 | test_promoted_to_warn_rule | tests/test_p0b_echo.py | 2.15 | 纯逻辑类 |

## 3. 最大瓶颈（一句话）

**Top 1 单测 `test_golden_lock_json`（176.21s，占全量 ≈27%）**：它通过 `tools/golden_lock.py check` 对**全库证据卡**逐卡 `replay.replay_card()` 真编译复算以比对 golden 基线，是全量最重的单点；紧随其后的第 3/5 名（`test_poison_drill_*`，共 106.7s）也是真编译。

## 4. 更值得修的第二瓶颈：3 个"纯逻辑"测试白烧 174.7s（根因已实测）

第 2/4/6 名合计 **174.70s（占 Top30 的 35.6%、全量 ≈27%）**，却**不编译任何东西**。根因已实跑确认：

1. 测试用 `sandbox` fixture（`tests/test_gate_engine.py:43`）只 monkeypatch 了 `ge.ATOMS/EVIDENCE/MISCONCEPTIONS` 到 `tmp_path`，**未 patch `ge.ROOT`**。
2. 测试卡由 `_write_card`（同文件 :872）生成，默认字段**不含 `fixture`/`artifact`**。
3. `gate_engine._assert_haystack`（`tools/gate_engine.py:1422`）用 `f = ROOT / str(rel or "")` 解析路径；`rel` 为空 ⇒ `ROOT / ""` = **仓库根目录**，`is_dir()` 为真 ⇒ 走 `f.rglob("*")` 分支，把**整仓每个文件全文读入**当"出处空间"。

实测（探针）：

```
ROOT/ -> 'C:\\CodeLearnling\\note\\note\\C++\\CPP-Bible'   is_dir True
files_under_root 28588    walk_sec 1.97
```

即每次调用要遍历并**全文读取 28588 个文件**（含 `.git/objects`、`.venv/`、`Examples/`、`_adv_v80/`），单测 42–80s 由此而来。

**附带正确性隐患（推断，建议好模型复核）**：同一分支意味着**任何缺 `fixture`/`artifact` 字段、却带 `artifact_assert` 的真实卡**，其"出处空间"会静默退化为**整个仓库**，于是 `EV-ASSERT-SYMBOL-MAPPED` 对这类卡恒不命中（任何符号都能在仓库里"找到"）。这与既有教训「缺字段静默降级 = 绕过面」同源，属潜在门禁盲区。

## 5. 建议（含估算，均已标注）

| # | 建议 | 预计收益 | 性质 |
|---|---|---|---|
| 1 | `_assert_haystack` 对空/缺失路径**直接 return**（不解析为 ROOT）；或 `sandbox` fixture 一并 `monkeypatch.setattr(ge, "ROOT", sandbox)` | 3 个 contains_in 测试 174.7s → **亚秒级**，全量 ≈642s → **≈468s（-27%）** | **估算**（依据：单次全仓 walk 实测仅 1.97s，耗时全在读取 28588 文件全文；隔离后无文件可读） |
| 2 | `test_golden_lock_json` 的编译借 ccache（replay 已接，热缓存实测 1.22×） | 编译类 Top30 299.64s → ≈245s，全量 ≈642s → **≈587s（-9%）** | **估算**（1.22× 来自 479 批 ccache 实测；golden_lock 是"锁基准"须跑全管线，收益有限） |
| 3 | 若要把全量压到分钟级以下 | 需拆分 golden_lock（JSON 结构锁 ≠ 全库复算）或把全库复算移到夜间/预提交 | 方向性建议 |

**优先级**：建议 1 明显优于建议 2——它同时修掉一个潜在门禁盲区，且收益（-27%）更大、改动更小（属"修正路径解析"而非"性能调优"）。

> 说明：本批铁律#3 禁止改 `tools/*.py` 与 `tests/`，故上述仅为建议，未实施。
