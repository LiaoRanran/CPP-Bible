# _worklog_568 · 一大批：日常门禁瘦身 + golden/replay 去重 + 卫生债

> 任务书：`References/architecture_架构演进/568_一大批_日常门禁瘦身_golden去重_卫生债.md`
> 承接：`34e7d9f`（567 完整性自检）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付（一任务一 commit）

| 任务 | 内容 | commit |
|---|---|---|
| 1 | stateful fuzz 归 nightly | `1734f0c` |
| 2 | golden 复用 replay 增量结论（T2a→T2b） | `8eceb08` |
| 3 | `run_fuzz` 写-跑-还原加 try/finally | `0ed9fde` |
| 4 | ruff 存量债清零 + CORE_TOOLS 重钉 | `12d484d` |

## 1 · 任务 1：fast 串行 106s → **42s**（实测）

* 现状：`tests/test_task_queue_stateful.py`（554 T1）文件头写的是"标 fast"（理由：临时库/无共享状态），
  但 `TestTQ::runTest` 一个用例 **65.69s**（hypothesis stateful 要 shrink/枚举）——本该 nightly。
* 做法：**文件级** `pytestmark = pytest.mark.slow`（不是 `skip`，不删用例）。
* 实测：
  * `pytest -m "not slow" -n0`（串行）**42s**（监工改前实测 106s；本机 42s 与"去掉 65.69s"吻合）；
  * `pytest -m slow --collect-only -q` ⇒ `tests/test_task_queue_stateful.py: 7`（**slow 照收**）；
  * `pytest -m "not slow" --collect-only -q` ⇒ 该文件 **0 例**（fast 已排掉）。

## 2 · 任务 2：golden 去重（T2a 侦察 → T2b 实现）

### T2a 侦察结论（先量后改）
* **改前真实耗时**（动 golden 之前后台量，见 `_t2a568.out`）：**178s**；改后等价"旧行为"路径
  （`--no-reuse`）在 A/B 里同轮实测 **249.2s**（机器负载不同；监工机上 ~131s）。三个数都贴出来，
  不挑好看的用。
* **它怎么调 replay**：`measure()` 里 `for p in evids: replay.replay_card(p, do_sanitizer=False)` ——
  **逐卡直调**，绕过了 replay **自己**的增量机制。
* **replay 侧已有的机制**（498 任务 5）：`build/replay_manifest.json`，指纹 =
  `sha256(卡 ‖ 夹具 ‖ 工件)`；`select_incremental()` 的规则逐条写死：无记录/指纹变了/
  上次非 confirm/指纹 `MISSING` ⇒ **跑**；指纹同且上次 `confirm` ⇒ **skip**。
* **判断：可以复用，且不该自造规则** ⇒ 把"该跑/该复用"判定**原样交给 replay 的纯函数**。

### T2b 实现（`tools/golden_lock.py`）
* `_select_replay(cards, replay_mod)`：`--no-reuse` ⇒ 全量真编译；否则
  `replay.load_manifest()`（缺失/损坏 ⇒ `{}`）+ `replay.select_incremental(...)`；
  任何异常 ⇒ 回退全量真编译（**fail-closed**）。
* `measure()`：只对 `to_run` 逐卡真编译；复用项**按定义只能是 confirm**（同一条规则）⇒ 计入 confirm；
  stderr 打一行"复用 N/M 卡"（诊断，不进 metrics，避免动 `golden_state.json` 的键集）。
* 新增 `check --no-reuse`：审计/对照开关（强制逐卡真编译）。

### 实测（机器判据，不是估计）
```
REUSE    : {"confirm": 56, "refute": 0, "infra": 0, "cards": 56, "sec": 11.2}
RECOMPILE: {"confirm": 56, "refute": 0, "infra": 0, "cards": 56, "sec": 249.2}
THREE-NUMBERS-IDENTICAL = True
```
⇒ **249.2s → 11.2s（≈22×）**，三数**逐字一致**。
**真实 fail-closed 案例（意外收获）**：本轮把 `EV-CONC-001.md` 的 M4 残留恢复成原文后，指纹变了 ⇒
golden 自动只对**那 1 卡**回退真编译（stderr 实测："复用 55/56 卡…其余 1 卡真编译"）——
"输入一变就回真编译"在真实数据上被撞到并验证。

### 独立性边界（诚实声明）
复用后，golden 对**内容未变**的卡不再独立重编译——这与 498 给 replay CLI 的既有语义一致
（replay 自己也会 skip）；**判定规则、锁与三分类语义都没动**（不削弱 Oracle）。代价：manifest 位于
`build/`（gitignore）⇒ 与 replay 一样，**篡改 manifest 可伪造 confirm**（这是既有的信任边界，
对应 PoC#3"无认证自签"，等 564 规格）。要审计时用 `--no-reuse` 拿真编译数对账。

## 3 · 任务 3：`run_fuzz` 还原进 finally

* 567 的发现坐实：还原写在**循环尾**（原 line 444），异常/中断/提前 return 都会把变异留在副本里。
* 改法：`for op in ops` 整段包进 `try:`，还原移到 `finally:`（沙箱副本还原成原卡文本）。
* 回归锁（`tests/test_mutation_fuzz.py::test_568_run_fuzz_restores_card_on_exception`）：
  替身 `sandbox()` 指向已知目录 + 替身 `classify` 先污染副本再抛错 ⇒ `run_fuzz` 必抛 ⇒
  断言 ①副本已还原成原卡文本 ②**真实卡零改动**。
* 另：`classify` 里原有一个 `finally: pass` 死代码，随本批的 ruff 清理一并去掉。

## 4 · 任务 4：ruff 存量债

* **实测与提示词不符（重要）**：`pyproject.toml` 的 `[tool.ruff]` **只配了** `line-length=120` /
  `target-version=py311`，**没有 `select`** ⇒ 规则集随 ruff 版本漂移：
  * 本机 `ruff==0.16.5`（`requirements` 钉的版本；提示词说的 0.6.9 已过时）**无 select** 时
    报 **914 项**（`I001`/`PLW1510`/`FURB167`/`UP009`/`SIM115`/`RUF100`/`ISC004`/`BLE001`…）；
  * 显式用**经典默认集** `E4,E7,E9,F` ⇒ **22 项**（与提示词"约 4–15 项"同量级）。
* 按经典默认集**清零**（只改风格不改逻辑）：
  * 13 项自动修（`F401` 未用导入 / `F541` 无占位符 f-string / `E401` 一行多导入）；
  * 9 项人工：`E741` 变量名 `l`→`ln`（`test_observability` / `test_p02_discriminative` ×3 /
    `env_check` ×2 / `gate_engine` / `poison_drill`）、`F841` 去未用赋值（`test_trace_logger`，
    保留有副作用的调用本身）。
* 结果：`ruff check tools/ tests/ --select E4,E7,E9,F` ⇒ **All checks passed!**
* `gate_engine.py` / `poison_drill.py` 属 **CORE_TOOLS** ⇒ **同 commit 重钉** `tools/.tool_checksums`；
  重钉后 `tool_integrity.py --check` ⇒ **exit 0**。

## 5 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **ruff 版本与规模**：提示词说"仓库钉的 0.6.9、约 4–15 项"；实测 `requirements` 钉的是
   **0.16.5**，且 pyproject **没有 `select`** ⇒ 无 select 时报 **914 项**。本批按**经典默认集**
   （E4,E7,E9,F，22 项）清零并在交人项建议**显式钉 select**——否则"存量债"这个数字会随
   ruff 升级自己变化（不可复现的债务口径）。
2. **任务 2 没有走"不能省"分支**：侦察确认 replay 已有落盘增量机制（`select_incremental` +
   manifest 指纹），复用的判定**可以完全交回给 replay 自己**（不自造规则），故实现了 T2b；
   三数逐字一致的机器判据已达成（见 §2）。
3. **`tests/test_mutation_fuzz.py` 同时含任务 3 与任务 4 的改动**（同一文件、无法拆 hunk，
   本环境无交互式 `git add -p`）⇒ 其 ruff 风格修随任务 3 的 commit 一起进来，已在 commit message 注明。
4. **任务 1 的"改前 106s"**取自监工实测（我未复跑改前基线，只复跑了改后 42s）——如实标注来源。

## 6 · 收工验收（fresh）

见 `_acc568.log`（后台 fresh 跑，含 slow）。要点：
`tool_integrity.py --check` exit 0 · 篡改拦截（567 已锁）· gate 61/141（block=0 warn=136）·
poison 107/107（双指标 100%）· replay confirm=56 · pytest fast `-n auto` 全绿 · pytest **slow `-n0`** 全绿
（**含** stateful 7 例）· 受控目录 `git diff --quiet -- evidence/ atoms/` exit 0。

## 7 · 交人项

1. **给 ruff 显式钉规则集**（`[tool.ruff.lint] select = ["E4","E7","E9","F", ...]`）：
   现在"存量债数量"是版本相关的，不可复现；钉了之后跑 `ruff check` 才有稳定口径。
   若要清 914 项那套（0.16.5 全规则），建议单开一批、按规则分批 `--fix` + 人审，不要混进功能批。
2. **manifest 的信任边界**（PoC#3）：`build/replay_manifest.json` 可被本地改写以伪造 `confirm`，
   golden/replay 都会采信 ⇒ 等 564 规格加签名/认证。要立刻拿真编译数可用
   `golden_lock.py check --no-reuse`。
3. **`EV-CONC-001.md` 的 M4 残留**（567 发现）：本批已恢复原文并加 `try/finally`；
   但残留的**原始来源未被完全确证**（当时的运行可能被中断）——建议后续给 `mutation_fuzz`
   加"退出即校验受控目录零差异"的自检（或在 CI 里跑 `git diff --quiet -- evidence/ atoms/`）。
4. 仓库根还有 4 个**既有**未跟踪目录 `_adv_critique/ _adv_v80/ _adv_v90/ _adv_v95/`（红队工作区，
   非本批产生）；`.pytest_tmp/`、`data/logs/` 的清理仍需非 agent 终端。
