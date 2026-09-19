# 603 建设包：编译可复现性显性化 —— 把 replay 已有的隐式重编译验证升级为可证属性 + metrics 指标 + 回归测试

> 你是苦力建设者，不是调研者。任务是把 602 异族深度调研（_arch_v17/）发现的 replay 隐式能力显性化——`_recompile_invariant`（atom_evidence_replay.py 行 1409，P0-A/452 E01）已经在做独立重编译 + CCACHE_DISABLE=1 + 临时目录隔离 + 比 sha，但这个能力是"隐式"的（散落在代码里，没有作为独立属性暴露、没有 metrics、没有回归测试、没有跨时间窗口验证）。你的任务是把它显性化。
> 严格按本仓铁律：一任务一 commit + 正反毒样例 + 存量零误伤 + 新收紧 warn 起步 + 护栏不许裸 except Exception + 改 CORE 必须同 commit --update 带 .tool_checksums。
> 做不完停在任务边界，不留半成品。

---

## 前置依赖（必须先核实）

### 602 调研核心发现（开工先读 _arch_v17/，不要凭记忆）

- `_arch_v17/00_总览_TLA与翻译验证落地路径_replay状态机从启发式到可证.md`
- `_arch_v17/05_编译可复现性深度调研与本项目落地.md`
- `_arch_v17/02_翻译验证深度调研与本项目落地设计.md`
- `_arch_v17/probes/00_build_repro_probe.py`（手搓探针，可参考实现）

### 602 核心结论（先核实再用）

1. **replay 早已内置轻量翻译验证**：`atom_evidence_replay.py` 的 `_recompile_invariant`（行 1409，P0-A/452 E01）独立重编译 + CCACHE_DISABLE=1 + 临时目录隔离 + 比 sha。56 张 confirm 卡的"编译可复现"已被现有管线实证。
2. **但这个能力是隐式的**：没有作为独立属性暴露、没有 metrics 指标、没有回归测试、没有跨时间窗口验证（只在同一次跑批内重编译）、只比 sha（没有比符号表/段级别）。
3. **性价比最高 = 编译可复现性显性化**：纯标准库 + g++、零新工具、升级已有逻辑（不是从零建）。
4. **探针实证**：极小程序 + 3 个含 `__DATE__`/`__TIME__`/`__FILE__` 的夹具，两次编译 sha 均一致（短窗口内）。但未跨秒/跨天、未用真实卡命令、未用 diffoscope → 严格结论只是"短窗口确定"。

### 当前 replay 状态（开工先量，实跑确认）

- `atom_evidence_replay.py --check` → confirm=56 / refute=0 / infra_error=0
- `_recompile_invariant` 的当前实现：先读 atom_evidence_replay.py 行 1400-1450，确认它的输入/输出/调用方式
- 它在什么条件下被调用？（所有卡？只 confirm 卡？只在 P0-A 路径？）
- 它的失败处理是什么？（重编译 sha 不一致 → 怎么处理？infra_error？refute？警告？）
- 它有没有 metrics 输出？（当前应该没有）

---

## 任务 0：开工先量 + 编译可复现性基线（无 commit）

### 0.1 开工基线（实跑，记录数字）

1. `tool_integrity.py --check` → exit 0
2. `gate_engine.py --check` → 规则数 / 命中数 / block/warn/advice
3. `poison_drill.py` → 通过数 / RULE-COVERAGE / 表观/诚实覆盖率
4. `atom_evidence_replay.py --check` → confirm/refute/infra
5. `pytest -m "not slow" -n auto` → 记录通过数（预期全绿，601 后 fast 已全绿）

### 0.2 编译可复现性基线（实跑，在临时目录做，不碰正式 Examples/）

写一个临时探针脚本（放在 %TEMP%，不入库），做以下实验：

1. **短窗口可复现性**：从 Examples/ 中随机选 5 个夹具 .cpp 文件，用卡面的真实编译命令（从证据卡的 matrix 读取，如 `g++ -std=c++23 -O2`），在临时目录连续编译两次，比较：
   - 二进制 sha256 是否一致
   - 符号表（nm 输出）是否一致
   - 关键段（.text / .data / .rodata，用 objdump -h 或 readelf -S）大小是否一致
   - 记录：5 个文件中，几个 sha 一致 / 几个符号表一致 / 几个段一致

2. **`_recompile_invariant` 覆盖范围**：读 atom_evidence_replay.py，确认 `_recompile_invariant` 在哪些路径被调用、覆盖多少张卡、失败时怎么处理。记录：
   - 调用点数量
   - 覆盖卡数（如果能从代码逻辑推断）
   - 失败处理方式（infra_error / refute / 警告 / 静默）

3. **跨时间窗口可复现性（可选，如果时间允许）**：编译一个含 `__DATE__` / `__TIME__` 的夹具，等待至少 1 秒后再次编译，比较 sha。如果不一致，记录差异来源（是 __DATE__ 还是 __TIME__ 还是其他）。

**产出**：编译可复现性基线报告（写进 _worklog_603.md §0.2），包含上述实验的真实数字。

**纪律**：
- 探针脚本放在 %TEMP%，不入库、不碰正式 Examples/
- 编译在临时目录做，不污染真实仓库
- 不许裸 except Exception
- 数字必须来自实跑，不编

---

## 任务 1：升级 `_recompile_invariant` 为独立可调用函数（commit 1）

### 1.1 重构为独立函数

当前 `_recompile_invariant` 可能是 replay 内部的一个私有函数，与 replay 的上下文（当前卡、当前夹具、沙箱路径）紧耦合。

**目标**：把它重构为一个独立的、可单独调用的函数，输入明确、输出明确，不依赖 replay 的全局状态。

**设计**（先核实当前实现，按实际情况调整）：

```python
def check_build_reproducibility(
    source_path: Path,           # 夹具 .cpp 文件路径
    compile_cmd: list[str],      # 编译命令（如 ["g++", "-std=c++23", "-O2", source, "-o", output]）
    work_dir: Path,              # 临时工作目录（调用方创建，函数不创建不删除）
    ccaches_disable: bool = True, # 是否禁用 ccache（默认 True，保证独立编译）
    check_level: str = "sha",    # 检查级别："sha"（只比二进制 sha）/ "symbols"（比符号表）/ "sections"（比关键段）/ "full"（全部）
) -> BuildReproResult:
    """
    验证编译可复现性：在临时目录独立编译两次，比较结果。
    
    返回 BuildReproResult（dataclass）：
    - success: bool（两次编译结果是否一致）
    - first_hash: str（第一次编译的二进制 sha256）
    - second_hash: str（第二次编译的二进制 sha256）
    - symbols_match: Optional[bool]（符号表是否一致，check_level >= "symbols" 时有效）
    - sections_match: Optional[bool]（关键段是否一致，check_level >= "sections" 时有效）
    - diff_detail: Optional[str]（如果不一致，差异详情）
    - compile_exit_code: int（编译 exit code，0=成功）
    - compile_stderr: str（编译 stderr，如果失败）
    - duration_ms: int（两次编译总耗时，毫秒）
    """
```

**实现要点**：
- 函数是纯函数（不修改全局状态、不依赖 replay 的上下文）
- 两次编译都在 work_dir 下的不同子目录（work_dir/run1 / work_dir/run2），保证隔离
- CCACHE_DISABLE=1 环境变量（如果 ccaches_disable=True），绕过编译缓存，保证独立编译
- 编译命令中的输出路径替换为临时目录下的路径（不要编译到真实 Examples/）
- sha 比较：hashlib.sha256(二进制文件内容)
- 符号表比较：调用 `nm <binary>`，比较输出（排序后比较，避免顺序差异）
- 关键段比较：调用 `objdump -h <binary>` 或 `readelf -S <binary>`，提取 .text / .data / .rodata 的大小，比较
- 如果编译失败（exit code != 0），success=False，compile_exit_code 记录失败码，compile_stderr 记录错误
- 不许裸 except Exception：编译失败是正常情况（夹具可能故意编译失败），不是异常，用返回值表示
- 超时保护：单次编译超时 30 秒（g++ 编译小文件应该几秒内完成，超时视为 infra_error）

### 1.2 接入 replay

把 replay 中原来调用 `_recompile_invariant` 的地方，改为调用新的 `check_build_reproducibility`。

**注意**：
- 保持 replay 的原有行为不变（confirm/refute/infra_error 判定逻辑不变）
- 新函数的返回值可以被 replay 使用（如记录编译可复现性结果），但不改变 replay 的判定
- 如果原来的 `_recompile_invariant` 失败时是静默处理，接入后仍然静默处理（不改变行为）
- 存量零误伤：接入后 `atom_evidence_replay.py --check` 的 confirm/refute/infra 数字必须与任务 0 基线逐字相同

### 1.3 保留旧函数（可选）

如果 `_recompile_invariant` 被其他地方引用（如测试），保留旧函数作为 wrapper（内部调用新函数），标记 `@deprecated`，不删除。这样不破坏现有测试。

### 测试（tests/test_build_reproducibility_603.py）

- 正例：一个可正常编译的简单 .cpp（int main(){return 0;}），check_level="sha" → success=True，两次 hash 一致
- 正例：check_level="full" → success=True，symbols_match=True，sections_match=True
- 正例：含 `__DATE__` 的 .cpp，短窗口内（同一秒）编译两次 → success=True（__DATE__ 精确到天，同一天内一致）
- 反例：故意写一个编译失败的 .cpp（语法错误）→ success=False，compile_exit_code != 0，compile_stderr 非空
- 反例：篡改第一次编译的二进制（手动改一个字节）→ success=False，diff_detail 非空
- 反例：传入不存在的 source_path → 函数不崩溃，返回 compile_exit_code != 0（或明确的错误返回）
- 幂等：同一输入连续调用两次，返回值（除 duration_ms 外）逐字一致
- 隔离：函数不修改 work_dir 外的任何文件（验证：调用前后 work_dir 外的文件状态不变）
- 可证伪性：不许裸 except Exception

---

## 任务 2：新增"编译可复现率"metrics 指标（commit 2）

### 2.1 metrics_collector.py 新增指标

在 `tools/metrics_collector.py` 中新增"编译可复现率"指标的采集逻辑。

**设计**（先核实 metrics_collector.py 的现有结构，按实际情况调整）：

- 新增函数 `collect_build_reproducibility()` → 采样 N 张卡（默认 10 张，从 56 张证据卡中随机或按顺序选），对每张卡调用 `check_build_reproducibility`，统计：
  - total: int（采样总数）
  - reproducible: int（可复现数，success=True 且 compile_exit_code=0）
  - compile_failed: int（编译失败数，compile_exit_code != 0）
  - not_reproducible: int（编译成功但不可复现数，success=False 且 compile_exit_code=0）
  - rate: float（可复现率 = reproducible / total，如果 total=0 则为 None）
  - avg_duration_ms: float（平均编译耗时）
  - sampled_cards: list[str]（采样的卡 ID 列表，用于复现）
- 采集结果写入 metrics.jsonl 的新行，包含 `build_reproducibility` 字段
- 与现有 metrics 采集逻辑集成（`collect_all()` 调用 `collect_build_reproducibility()`）

**注意**：
- 采样是只读的（在临时目录编译，不碰正式 Examples/）
- 采样卡数不要太多（默认 10 张），避免 metrics 采集太慢（每张卡编译两次，10 张约 30-60 秒）
- 采样卡列表写入结果，保证可复现（下次用同样的卡列表能得到同样的结果）
- 编译失败的卡不算"不可复现"（单独统计 compile_failed），因为编译失败可能是夹具故意设计的（如 UB 卡）
- 不许裸 except Exception

### 2.2 metrics 输出格式

metrics.jsonl 新行的 `build_reproducibility` 字段格式：

```json
{
  "build_reproducibility": {
    "total": 10,
    "reproducible": 9,
    "compile_failed": 1,
    "not_reproducible": 0,
    "rate": 0.9,
    "avg_duration_ms": 1234.5,
    "sampled_cards": ["EV-MEM-001", "EV-UB-001", "..."],
    "check_level": "sha",
    "collected_at": "2026-09-19T23:00:00"
  }
}
```

### 测试（tests/test_metrics_build_repro_603.py）

- 正例：`collect_build_reproducibility()` 返回格式正确，total=10（默认采样数），rate 在 [0, 1] 范围内
- 正例：采样卡列表非空，且长度=total
- 正例：reproducible + compile_failed + not_reproducible == total（三分类互斥且穷尽）
- 反例：如果所有采样卡都编译失败（极端情况），rate=0（不是 None，因为 total>0）
- 反例：如果 total=0（采样卡列表为空），rate=None
- 幂等：用同样的 sampled_cards 连续采集两次，结果（除 collected_at / avg_duration_ms 外）逐字一致
- 可证伪性：不许裸 except Exception

---

## 任务 3：replay 不变量回归测试 + 编译可复现性正反例（commit 3）

### 3.1 replay 不变量回归测试

基于 602 调研方向 4（replay 不变量与活性属性），为 replay 的关键不变量写回归测试。

**先核实 602 的不变量清单**（读 _arch_v17/08_不变量清单与优先级.md），选择 3-5 个最关键、最容易测试的不变量：

候选不变量（从 602 清单中选，按优先级）：
1. **仓库一致性不变量**：replay 完成后，真实仓库的状态与跑批前完全一致（所有临时文件被删除、所有被修改的文件被还原）
2. **判定一致性不变量**：replay 的 confirm/refute 判定与证据卡的 artifact_assert 一致
3. **还原幂等不变量**：replay 的"还原真实仓库"操作是幂等的（连续还原两次，仓库状态相同）
4. **错误处理不变量**：replay 遇到 infra_error 时，不会误判为 refute
5. **并发隔离不变量**：并发跑批时，每个 worker 的沙箱互不干扰（这个可能难测，留到未来）

**测试设计**（tests/test_replay_invariants_603.py）：

- **仓库一致性测试**：
  - 记录跑批前的 git status 和关键文件 hash
  - 运行 replay --check（或 replay 单张卡）
  - 记录跑批后的 git status 和关键文件 hash
  - 断言：跑批前后 git status 一致、关键文件 hash 一致
  - 注意：replay --check 可能不修改仓库（只读验证），如果是这样，这个测试 trivially 通过。需要找一个会修改仓库的 replay 路径（如完整 replay 单张卡，包含编译和还原），或者测试 replay 的"还原"函数单独调用

- **判定一致性测试**：
  - 选一张已知 confirm 的卡（如 EV-MEM-001），手动运行 replay，断言判定=confirm
  - 选一张已知 refute 的卡（如果有），断言判定=refute
  - 注意：当前 refute=0，可能没有 refute 卡。如果没有，只测 confirm 卡，并在测试注释中说明"当前无 refute 卡，refute 路径待未来有 refute 卡时补充"

- **还原幂等测试**：
  - 调用 replay 的还原函数（如果是公开的）两次
  - 断言：两次还原后仓库状态相同
  - 如果还原函数是私有的，通过 replay 完整流程间接测试

- **错误处理测试**：
  - 模拟 infra_error（如编译环境不可用、g++ 不存在）
  - 断言：replay 判定=infra_error，不是 refute
  - 注意：模拟 g++ 不存在可能需要 monkeypatch，测试后恢复

**纪律**：
- 测试必须是幂等的（跑多次结果相同）
- 测试不修改正式仓库（在临时目录或用 monkeypatch）
- 不许裸 except Exception
- 如果某个不变量当前无法测试（如 replay 函数是私有的），在测试文件中写明原因，不强行测试

### 3.2 编译可复现性正反例（毒样例风格）

在 poison_drill.py 中新增编译可复现性的正反例（如果 poison_drill 的架构支持新增攻击类型；如果不支持，放在独立测试文件中）。

**先核实 poison_drill.py 的架构**（读 poison_drill.py，确认如何新增毒样例）。

**正例（应该通过可复现性检查）**：
- P80：一个简单的 .cpp，不含 __DATE__/__TIME__，编译命令固定 → 两次编译 sha 一致
- P81：含 __DATE__ 的 .cpp，同一天内编译 → 两次编译 sha 一致（__DATE__ 精确到天）

**反例（应该不通过可复现性检查，如果跨时间窗口）**：
- P82：含 __TIME__ 的 .cpp，跨秒编译 → 两次编译 sha 不一致（__TIME__ 精确到秒）
  - 注意：这个反例需要等待至少 1 秒，测试可能慢。可以用 monkeypatch 时间，或者在测试注释中说明"这个反例需要跨秒，CI 中可能跳过"
- P83：编译命令中包含绝对路径（调试信息中包含绝对路径），不同工作目录编译 → 调试信息中的路径不同 → sha 不一致
  - 注意：这个反例需要 -g 编译选项，且工作目录不同

**注意**：
- 毒样例的目的是验证 `check_build_reproducibility` 函数的判别力（正例应该判 success=True，反例应该判 success=False）
- 不是验证 replay 的行为（replay 的行为不变）
- 如果 poison_drill.py 的架构不支持新增这种类型的毒样例，放在 tests/test_build_reproducibility_603.py 中作为独立测试

---

## 任务 4：收工总验收（无 commit，纯验收）

按以下清单逐项验收，全部用退出码定论（$LASTEXITCODE）：

1. `tool_integrity.py --check` → exit 0（改了 atom_evidence_replay.py 和 metrics_collector.py，必须同 commit --update 带新的 .tool_checksums）
2. `tool_integrity.py --check-test-config` → exit 0
3. `tool_integrity.py --check-merkle` → exit 0（601 新增，确认未受影响）
4. `gate_engine.py --check` → exit 0，规则数/命中数/block/warn/advice 与任务 0 基线逐字相同
5. `poison_drill.py` → exit 0，通过数/RULE-COVERAGE/表观/诚实覆盖率与基线逐字相同
6. `atom_evidence_replay.py --check` → exit 0，confirm/refute/infra 与基线逐字相同（**关键：重构后 replay 行为不变**）
7. `governance_doc_guard.py verify` → exit 0（601 已修复，确认未受影响）
8. `merkle_integrity.py --check` → exit 0（601 新增，确认未受影响）
9. `supply_chain.py layout verify` → exit 0（601 新增，确认未受影响）
10. `metrics_collector.py`（全量）→ exit 0，新行包含 build_reproducibility 字段
11. `pytest -m "not slow" -n auto` → exit 0（含本批新增测试）
12. `pytest -m slow -n0` → exit 1，唯一红 = test_golden_lock_json（预期红）
13. `ruff check`（本批全部新增/改动 .py）→ All checks passed
14. `git diff --quiet -- atoms evidence Examples Book` → exit 0（受控目录零污染）
15. `git status --short` → 仅本批文件（+ 两条 CRLF 假脏）

---

## 明确不做（任务书边界）

- **不改变 replay 的判定逻辑**：confirm/refute/infra_error 判定逻辑不变，只是把 `_recompile_invariant` 重构为独立函数
- **不做跨时间窗口验证**：602 探针只验证了短窗口可复现性，跨天/跨版本验证留到未来（需要长时间运行，不适合本包）
- **不做中量级/重量级翻译验证**：GIMPLE IR 比对、SMT 求解器验证留到未来（602 方向 2 的阶段 4/5）
- **不做 TLA+ 模型检查**：602 方向 1/4 的 TLA+ 规格和模型检查留到未来建设包（需要学习 TLA+ 工具链）
- **不修改 gate_engine.py / poison_drill.py / toolchain.py / cppbible.py 的核心逻辑**
- **不 push / 不 golden accept / 不替人签**

---

## 偏差表模板（写进 _worklog_603.md §6）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | `_recompile_invariant` 在行 1409 | （实跑结果，可能行号有偏移） | 按实测行号 |
| D2 | `_recompile_invariant` 覆盖所有 confirm 卡 | （实跑结果，可能只覆盖部分路径） | 按实测覆盖范围 |
| D3 | 短窗口内 5 个夹具全部 sha 一致 | （实跑结果，可能有不一致） | 按实测记录，不一致的分析原因 |
| D4 | metrics 采集 10 张卡约 30-60 秒 | （实跑结果） | 按实测调整默认采样数 |
| D5 | poison_drill 支持新增编译可复现性毒样例 | （实跑结果，可能架构不支持） | 不支持则放独立测试文件 |
| D6 | replay 不变量全部可测试 | （实跑结果，某些可能因函数私有而无法测试） | 无法测试的写明原因 |
| ... | ... | ... | ... |

---

## 过程文档

- `_worklog_603.md`：按惯例不入库，含任务 0 基线 / 编译可复现性基线实验 / 各任务实跑数字 / §6 偏差表 / §7 收工验收 / 交人项
- 每个任务一个 commit，message 里写明任务编号和一句话结果
- 改了 atom_evidence_replay.py / metrics_collector.py 必须同 commit `tool_integrity.py --update` 带新的 .tool_checksums
- 编译可复现性基线实验的真实数字写进 _worklog_603.md §0.2，不编
