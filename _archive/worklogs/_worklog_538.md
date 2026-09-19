# 538 建设日志：T0 修 E1 touch 归一化 P0（完成）+ 537 剩余机械活（未做）

> 依据：`References/architecture_架构演进/538_建设批_修E1-touch归一化P0+537收尾.md`
> 纪律：不 push / 不 `--no-verify` / 不 golden accept / 不改 56 卡信任结论；做不完停在 T 边界、不留半成品。

## 幂等进度看板

```
T0 修 E1 touch 路径归一化逃逸（P0）  [x] 0f7fd21（探针 4/4 逃逸 → 0/4 全 blocked）
T1 V4 毒样例 N1–N7 进 poison        [ ] 未做 —— 施工点见 `_worklog_537.md` §3.1
T5 warn 136 四桶分类建议文档         [ ] 未做 —— 施工点见 `_worklog_537.md` §3.2
T6 CI ruff 存量 15 项               [ ] 未做 —— 施工点见 `_worklog_537.md` §3.3
T7 V-iso 56 卡迁移 backlog 文档      [ ] 未做 —— 施工点见 `_worklog_537.md` §3.4
```

## 0. 开工基线（HEAD=`a804ef0`，亲手实测）

`gate 60 规则 · 141 命中 (block=0 warn=136 advice=5)` · `poison 90/90 · RULE-COVERAGE 35/60 · 零覆盖攻击面：无` · `replay confirm=56 / refute=0 / infra_error=0`（全量 173.4s）· `pytest -m fast -q` **275 passed** · `tool_integrity OK`。

---

## 1. T0 · E1 touch 路径归一化逃逸修复（**已完成**，`0f7fd21`）

### 1.1 问题复现（修前）

`_adv_v90/probe_touch_case.py`（建设方独立探针，非本批自造）修前实测 **逃逸 4/4**：
wA 领任务声明 `touch=tools/task_queue.py` 在飞，wB 用 `TOOLS/TASK_QUEUE.PY` / `Tools/Task_Queue.py` /
`./tools/task_queue.py` / `tools/./task_queue.py` 声明**同一物理文件**，只做 `replace("\\","/")` 的
集合比较全部不等 ⇒ wB 照样领到 ⇒ 两个 worker 并发改同一文件（55b53ae/527 类事故的复发路径）。

### 1.2 修法（照 538 处方，未另起炉灶）

```python
def _norm_touch(p) -> str:
    return os.path.normcase(PurePath(str(p).strip()).as_posix())
```
- `enqueue` 入库：`touch_set = sorted({_norm_touch(t) for t in (touch or []) if str(t).strip()})`
- `_conflicts` 比较：`want = {_norm_touch(t) for t in touch}`
- `_claimed_touch` 读回：`{_norm_touch(x) for x in _jload(...)}`（**双保险**：历史库里可能已存未归一键）
- 注释写死纪律：**不许写死 `.lower()`**——`os.path.normcase` 平台相关（Windows 小写化 / Linux 原样），
  否则会在 Linux 上把两个真实不同的文件错误合并成一把锁（假冲突）。

### 1.3 验收实测（改后）

| 项 | 修前 | 修后 |
|---|---|---|
| `_adv_v90/probe_touch_case.py` 4 变体 | **逃逸 4/4** | **逃逸 0/4**（4/4 全 `blocked`，`blocked_by_touch` 点名 wA 与文件） |
| `pytest tests/test_task_queue.py -q` | 46 passed | **49 passed + 1 skipped**（skip = 仅 posix 的用例，Windows 上按设计跳过） |
| `pytest -m fast -q` | 275 passed | **279 passed**（+4 T0 用例） |
| ruff 0.6.9（改动文件） | — | `All checks passed!` |

新增用例（`tests/test_task_queue.py`）：
1. `test_t0_dot_variants_collide_on_all_platforms`：`./x`、`a/./x` 两个变体在**任何平台**都撞锁（PurePath 平台无关）；
2. `test_t0_case_and_backslash_variants_blocked_on_windows`：Windows 上大小写变体 + `\` 变体全部撞锁 + 入库即归一；
3. `test_t0_case_sensitive_semantics_preserved_on_posix`：**Linux 大小写敏感语义不被破坏**（两个仅大小写不同的真实文件不许合并成一把锁；Windows 上 skip）；
4. `test_t0_regression_existing_touch_lock_still_works`：既有 touch 锁行为回归（同写法挡、不相交不挡）。

### 1.4 规格说 X / 实测 Y（偏差表）

| # | 538 规格说 | 实测 Y | 处置 |
|---|---|---|---|
| 1 | 三处改点（enqueue / `_conflicts` / 读回） | 磁盘一致，行号已漂移（enqueue 约 666→现 60x；`_conflicts` 约 377→现 37x） | 以磁盘为准改三处 + 新增 `_norm_touch` |
| 2 | 处方函数返回 `os.path.normcase(PurePath(...).as_posix())` | Windows 上 `ntpath.normcase` **会把 `/` 换回 `\`** ⇒ 入库 canonical 形态含反斜杠（如 `tools\task_queue.py`），不再是纯 posix | **照处方执行**（比较两侧同归一 ⇒ 锁语义正确，探针 0/4 证明）；同步把 4 处既有断言改成"归一形态"（`tq._norm_touch(...)`）而不是写死分隔符方向 |
| 3 | "跨平台：Linux 大小写敏感不被破坏" | 需要一条 Windows 上会 skip 的用例才能真正证明 | 已加（`skipif not _WIN` / `skipif _WIN` 两条，当前环境 1 skipped 属预期） |

---

## 2. T1 / T5 / T6 / T7 · 未做（停在 T 边界）

本会话上下文预算见底，按 538/537 的"做不完停在 T 边界、不留半成品"停在此处。
**施工点（含现成资产、注意坑、验收判据）已逐条写在 `_worklog_537.md` §3**，照做即可：

- **T1 V4 毒样例 N1–N7**：`_worklog_537.md` §3.1；判决实现已在 `tools/atom_evidence_replay.py::check_negative_controls`（535 V3 落地），毒样例只需按 533 §2.5 表断言 verdict；注意 poison 覆盖正则只认字面量 `"RULE-ID" in who`。
- **T5 warn 136 四桶分类建议文档**：§3.2（`.venv\Scripts\python.exe tools/golden_lock.py buckets`，只出建议**不 accept**）。
- **T6 CI ruff 15 项**：§3.3（钉 0.6.9 口径；9 项可 `--fix`、6 项需判语义；会动 8 个此前未改文件 ⇒ 建议独立小任务）。
- **T7 V-iso 56 卡 backlog 文档**：§3.4（数据源 `_arch_v2_round2/survey_cards.py` + 533 §2.4 分批结论；只排队不改卡）。

---

## 3. 收工门禁（fresh run，HEAD=`0f7fd21`，串行）

| 门禁 | 实测 | 判定 |
|---|---|---|
| `gate_engine.py --check` | `规则 60 条 · 命中 141 (block=0 warn=136 advice=5)` | ✅ 与开工逐字一致 |
| `poison_drill.py` | `90/90`；`RULE-COVERAGE 35/60`（豁免 27）；`零覆盖攻击面：无` | ✅ |
| `atom_evidence_replay.py --check --no-sanitizer` | `confirm=56 / refute=0 / infra_error=0`，全量 **165.0s** | ✅ |
| replay `--incremental` | 56 张全部命中缓存（无变化，未跑编译） | ✅ |
| `pytest -m fast -q` | **279 passed**（275 → +4 = T0 用例） | ✅ |
| `tool_integrity.py` | `OK：5 个核心工具与基准一致`（T0 未碰被钉核心工具） | ✅ |
| ruff 0.6.9（改动文件） | `tools/task_queue.py` + `tests/test_task_queue.py` → `All checks passed!` | ✅ |
| 受控目录 / 56 卡 | 未动任何卡、未动 `golden_state.json` | ✅ |

**538 交付**：1 个 commit（`0f7fd21`，P0 修复 + 4 例回归锁）；本地 **ahead 14 个提交（未 push）**。

## 4. 交人项

1. **T1/T5/T6/T7 未做**（同上，施工点已备）。
2. **T0 的 canonical 形态选择**：处方落地后 Windows 入库值含反斜杠（`normcase` 平台行为）。锁语义已验证正确；若人希望库里统一存 posix 形态（便于跨平台读库/人读），需把 `_norm_touch` 改为
   `os.path.normcase(PurePath(...).as_posix()).replace("\\\\", "/")` 并重归一历史行——**属口径变更，交人裁决**（本批按 538 处方不动）。
3. 沙箱未跟踪目录（`_arch_*`/`_adv_*`/`_worklog_*`/`_t*`）不入库；`_adv_v90/probe_touch_case.py` 是本批 P0 的**独立探针证据**，保留供复跑。

## 5. 证据复跑命令

```powershell
# P0 探针（修后应 逃逸 0/4）
.venv\Scripts\python.exe _adv_v90\probe_touch_case.py
# T0 回归锁
.venv\Scripts\python.exe -m pytest tests/test_task_queue.py -q -k t0
```
