# 603 建设包：编译可复现性显性化 —— worklog（按惯例不入库）

## §0 开工基线（任务 0，无 commit）

### 0.1 工具链与既有基线（实跑，2026-09-19）
- 编译器：`C:\Qt\Tools\mingw1530_64\bin\g++.exe`（GCC 15.3.0 MinGW-w64）。
- 同目录可用：`nm.exe` / `objdump.exe` / `readelf.exe` / `strip.exe` ⇒ `check_level="full"`（符号表 + 关键段）可行。
- `tool_integrity --check` → 0（601 后基线）。
- `gate_engine --check` → 63 规则 / 191 命中（block=0 warn=186 advice=5）。
- `atom_evidence_replay --check` → confirm=56 / refute=0 / infra_error=0。
- `pytest -m "not slow" -n auto` → 0（601 验收已录）。

### 0.2 编译可复现性探针（%TEMP%，不碰正式 Examples/）
脚本：`C:\Users\ASUS\AppData\Local\Temp\c603_probe.py`（未入库）。
- 随机 5 个 Examples/*.cpp 夹具，用裸 `-std=c++23 -O2` 独立编译两次（临时目录）：
  - 4/5 **编译失败**（缺 `.h` 依赖 / 多 TU / 需要卡 `command` 的 include 路径）——**预期**：裸命令无法独立编多数夹具。
  - 1/5（`_asm_rtti.cpp`）编译成功且 **sha 一致 + `nm` 符号表一致**（短窗口确定）。
- 段级（`.text`/`.data`/`.rodata` via `readelf -S`）：失败夹具不适用；成功夹具因编译失败未取段。
- **诚实结论**：短窗口内、可独立编译的夹具确定；多数夹具需卡的真实 `command`（含 include/链接）才能编译——该"真实命令可复现性"由 **任务 2 的 `collect_build_reproducibility`（N=10，用卡真实 command）** 给出，不在此重复编。
- 与 602 探针（`_arch_v17/probes/00_build_repro_probe.py`）结论互相印证：本机短窗口内同命令同编译器确定。

### §0 偏差预案（D-主动）
- **D-A（架构级，已决）**：任务书 1.2 写"replay 改调 `check_build_reproducibility`"。但原 `_recompile_invariant` 的语义是
  **"独立重编译一次 vs 卡值 want_sha（防篡改）"**，新引擎语义是 **"重编译两次互相比对（证确定）"**——二者不是同一件事。
  为保证 replay 判决 **逐字不变（存量零误伤）**，决策：保留 `_recompile_invariant` 的 want_sha 比对原路径，
  让它**委托**新引擎取 `first_hash`（引擎多编一次 run2 仅用于 metrics/测试，不影响 replay 判决）；
  新引擎（run1 vs run2 + symbols/sections）**只**进入 metrics（任务 2）与回归测试（任务 1.3 / 3.2），**不**进入 replay 判决路径。
  代价：replay 的 recompile 段耗时约翻倍（56 卡各多编一次），可接受。
- **D-B**：任务书 1.1 签名是 `(source_path, compile_cmd:list, work_dir, ...)`。本项目 replay 命令是
  **多行 shell 字符串**，硬拆 list 会改行为。故引擎接受 `compile_cmd: str | list[str]`（list 免 shell、
  str 走 `shell=True`），`source_path` 用于存在性校验 + 默认输出名；replay 用 str 形态、tests 用 list 形态。
- **D-C**：`check_level="full"` 的 symbols/sections 比对若 `nm`/`readelf` 不可用 → 该字段返回 `None`（不 crash、
  不误判），并在 note 说明；本机四件齐备故全可测。

---

## §1 任务 1（commit `1c9e5b4`）：引擎 `check_build_reproducibility` 显性化

- `tools/atom_evidence_replay.py` 新增 `@dataclass BuildReproResult` + `check_build_reproducibility()`：
  两次独立编译落 `work_dir/run1`、`work_dir/run2`，比 sha（`check_level="sha"`）/ 符号表（`nm`）/ 关键段（PE 走 `objdump -h`，**Size 在 `parts[2]`**）。
- **绝不抛**：只捕 `TimeoutExpired` / `OSError`，其余失败一律经返回值表达（exit：`0`=ok / `-1`=源缺失或起不来 / `-2`=超时）。
- `_recompile_invariant` 改为**委托**新引擎取 `first_hash` 再比 want_sha ⇒ replay 判决**逐字不变**。
- 测试 `tests/test_build_reproducibility_603.py`：9 例（sha/full/`__DATE__`/语法错/篡改 run2/源缺失/编译器缺失/幂等/隔离）全过。
- CORE 改动 ⇒ **同 commit `tool_integrity.py --update` 重钉**（core 节）。

## §2 任务 2（commit `d54c65a`）：metrics 新增编译可复现率

- `tools/metrics_collector.py`（**非 CORE，不重钉**）新增 `collect_build_reproducibility(sample=10, seed=603, ...)`：
  `random.Random(seed).sample` 确定性抽样 → 取每卡 `lines[-1]`（同 `_recompile_invariant` 语义）→ 注入
  `-Wl,--no-insert-timestamp`（**度量口径**，不进 replay 判决）→ 调引擎 `check_level="sha"`。
- 接入 `collect()` **仅 heavy 分支**（`--no-heavy` 跳过）。
- 测试 `tests/test_build_reproducibility_metrics_603.py`：2 例过。
- **关键工程结论**：MinGW ld 默认插 PE 时间戳（随墙钟秒变）⇒ 须 `-Wl,--no-insert-timestamp` 才能确定化；
  **原则：引擎保持纯粹，确定性由调用方决定**（replay 走 want_sha 匹配不受影响）。

## §3 任务 3（commit `ae5f903`）：replay 不变量回归锁 + 毒样例 P80–P83

### 3.1 `tests/test_replay_invariants_603.py`（新，6 例）

把 602 `_arch_v17/08_不变量清单与优先级.md` 的清单显性化为可证断言：

| ID | 不变量 | 落点 | 覆盖方式 |
|---|---|---|---|
| I1 | 仓库一致性 | confirm / refute 两路径结束后工件须**逐字节**回到运行前 | 用**哨兵字节**覆盖工件（校验中途会删旧+重生成为"真实 asm"）⇒ 能区分"真·还原"与"恰好重生成" |
| I2 | 判定一致性 | confirm 卡→`confirm`；错 sha 卡→`refute:sha256_mismatch` | 合成卡（范式对齐 `tests/test_recompile_invariant.py`） |
| I3 | 还原幂等 | `_restore_artifact` 有效不动 / 缺失或空才重建 / 重复调用无漂移 | 直接单测（返回 `False/True/False`） |
| I4 | 错误处理 | `compiler_missing`、`msvc_unavailable` → `infra_error`，**绝不退化成 refute**；内容缺失仍 `refute:missing_field` | `monkeypatch toolchain.resolve_gpp` |
| I5 | 并发隔离 | — | **不复测**：已由 `tests/test_replay_lock_serial.py` 覆盖（避免重复） |
| I6 | manifest 一致性 | — | 不复测：既有 `test_replay_manifest*` 覆盖 |

沙箱：`monkeypatch replay.ROOT = tmp_path` + `chdir`（复现"ROOT==进程 cwd"语义；Windows 相对可执行名按父进程 cwd 解析）。

### 3.2 毒样例 P80–P83（并入 `tests/test_build_reproducibility_603.py`）

- **D5 核实**：`poison_drill.py` 的 `ATTACK_TYPES` 是"**gate 规则是否拦截**"模型（每条挂 `rule=`/`check=`），
  "两次编译互校"不是 gate 规则 ⇒ **架构不支持**，按任务书预案放独立测试文件。
- P80 正例：`-S` 汇编两次 ⇒ sha 一致。
- P81 正例：`__DATE__`（精度=天）+ `full` 级 ⇒ 一致。
- P82 反例：`__TIME__`（精度=秒）⇒ 在 `run2` 前**注入 >1s 延迟**确定性命中跨秒边界 ⇒ 判不可复现
  （不依赖"恰好慢到跨秒"，避免随机跳红）。
- P83 反例（**边界，如实记录**）：引擎两次编译**共用同一 cwd** ⇒ 同 cwd 的 `-g` 判可复现；
  而"不同 cwd + `-g`"（DWARF `DW_AT_comp_dir` 路径绑定）确实 sha 不同，但**不在本引擎判别范围**（非缺陷）——
  测试同时验证了这半句现象为真，避免把边界写成"已覆盖"。

---

## §6 偏差表（对任务书模板）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | `_recompile_invariant` 在行 1409 | 行号已偏移（593 行段），调用点唯一（`replay_card` recompile 路径） | 按实测定位，语义未变 |
| D2 | 覆盖所有 confirm 卡 | 56 张卡全部走 recompile 路径 | 按实测；`--check` 56/0/0 逐字不变 |
| D3 | 短窗口 5 夹具全 sha 一致 | 裸命令 4/5 **编不过**（缺头文件 / 多 TU）；可独立编译者 sha+符号一致 | 真命令口径交任务 2（10 卡 10/10 reproducible） |
| D4 | metrics 10 卡约 30–60s | heavy 全量采集（poison+replay+build_repro）整体约 2–3 min；其中 10 卡 10/10 reproducible、0 compile_failed | 保留 `sample=10` |
| D5 | poison_drill 支持新增此类毒样例 | **不支持**（模型是"gate 规则拦截"） | P80–P83 放独立测试文件 |
| D6 | replay 不变量全部可测 | I1–I4 可测；I5/I6 已有既有测试覆盖 | 测试文件头写明"不复测原因"，不强行造测试 |
| D7 | 1.2 要求 replay 改调新引擎 | 语义冲突：`want_sha` 比对 ≠ 两次互校 | replay 仅**委托**取 `first_hash`；互校只进 metrics/测试（见 §0 D-A） |
| D8 | 验收 15 项预期"两条 CRLF 假脏" | 实测**仅 1 条**（`data/mutation/full_baseline_v4.json`，`git diff` 内容零差异） | 按实测记录 |
| D9 | 验收第 7 项预期 `governance verify`=0 | 开工即红：**2 处**（新增 603 投喂词 + `PM_六维度…20260919更新.md` 内容变更） | 按 592/601 先例做 **chore**：`update --force`(2 处) + `scan` 刷新 + 重钉(supply_chain 仅 1 行) |
| D10 | 计划 3 commit | 因 D9 多 1 个 chore commit ⇒ **603 实际 4 commit** | 见 §7 |

---

## §7 收工总验收（全部以 `$LASTEXITCODE` 定论；HEAD=`1eaba2c`）

| # | 项 | 结果 |
|---|---|---|
| 1 | `tool_integrity.py --check` | **0**（core 5 一致） |
| 2 | `tool_integrity.py --check-test-config` | **0**（2 个测试器配置一致） |
| 3 | `tool_integrity.py --check-merkle` | **0**（目录级 Merkle 一致，警告 0） |
| 4 | `gate_engine.py --check` | **0** · 规则 63 · 命中 191 (block=0 warn=186 advice=5) ＝任务 0 基线逐字相同 |
| 5 | `poison_drill.py` | **0** · 124/124 · 表观 100.0%(63/63) · 诚实 95.2%(60/63) ＝基线逐字相同 |
| 6 | `atom_evidence_replay.py --check` | **0** · confirm=56 refute=0 infra_error=0 ＝基线逐字相同（**重构未改判决**） |
| 7 | `governance_doc_guard.py verify` | **0**（经 chore 后；开工时 1，见 D9） |
| 8 | `merkle_integrity.py --check` | **0**（5 个目录根一致，警告 0） |
| 9 | `supply_chain.py layout verify` | **0**（7 步 · 3 检查点） |
| 10 | `metrics_collector.py collect`（全量） | **0** · 27/27 项落盘；新行 `build_reproducibility` = total 10 / reproducible 10 / compile_failed 0 / not_reproducible 0 / unavailable 0 / rate 100.0 |
| 11 | `pytest -m "not slow" -n auto` | **0**（5 snapshots passed；修 D9 前为 1 failed，红因治理台账，非本批代码） |
| 12 | `pytest -m slow -n0` | **1**，唯一红 = `test_json_output.py::test_golden_lock_json`（预期红） |
| 13 | `ruff check`（本批 6 个 .py） | **0** · All checks passed |
| 14 | `git diff --quiet -- atoms evidence Examples Book` | **0**（受控目录零污染） |
| 15 | `git status --short` | 仅 ` M data/mutation/full_baseline_v4.json`（内容零差异，CRLF/stat 假脏）＋未跟踪 `_worklog_603.md` 与 603 投喂词（按惯例不入库） |

### 本批 commit（4 个，不 push、不 golden accept）
1. `1c9e5b4` 任务1：引擎 `check_build_reproducibility`（CORE ⇒ 同 commit 重钉）
2. `d54c65a` 任务2：metrics `build_reproducibility` 指标 + 测试
3. `ae5f903` 任务3：replay 不变量回归锁 + 毒样例 P80–P83 + conftest SLOW_MODULES + test_config 重钉
4. `1eaba2c` chore：治理台账纳入 603 投喂词 + PM 文档（2 处）+ scan 刷新 + supply_chain 重钉

---

## §8 交人项 / 残余边界

1. **治理台账 `update` 的语义边界**：本批 `update --force` 只是把"文档变了（2 处）"**机械重录**进台账，
   **不构成任何语义认可**。scan 出的 **high=55** 仍需人读 diff（模式匹配≠语义理解）。
2. **P83 边界**：引擎两次编译共用同一 cwd ⇒ "不同 cwd + `-g`"的调试路径绑定**不在判别范围**。
   当前各卡命令均为同 cwd 复算，不影响 replay / metrics 口径；若要覆盖需引擎按 run 切 cwd（另议）。
3. **metrics 采样口径**：`sample=10`、`seed=603`（`random.Random(603).sample`）⇒ 抽样清单随卡池变化而变；
   长期趋势比较须同时看 `sampled_cards`（已落盘）。
4. **并发会话**：本批执行期间另有 **604 会话在同仓并行提交**（HEAD 由 `ae5f903` → `7fe40cb` → `e9744bb`）。
   本批 4 个 commit 均在 `ae5f903` 之上线性落地，§7 全部数字在**本批 HEAD `1eaba2c`** 上复跑取得。
   提醒：多会话并行时提交前先看 `git log -1`，验收须在自己 HEAD 上复跑。
5. **未做（任务书边界）**：跨时间窗口（跨天/跨版本）验证、GIMPLE/IR 或 SMT 级翻译验证、TLA+ 模型检查，
   均按任务书留给未来建设包。
