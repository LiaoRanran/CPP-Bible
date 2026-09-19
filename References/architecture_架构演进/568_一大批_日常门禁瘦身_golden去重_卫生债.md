# 568 · 一大批：日常门禁瘦身 + golden/replay 去重 + 卫生债

承接 `34e7d9f`（567 完整性自检，监工已亲验篡改拦截）。解释器只用 `.venv\Scripts\python.exe`；一任务一 commit；不 push、不 golden accept。**核心目标：让日常 fast 从 ~106s 串行降到 <60s，golden 不再重放 replay 已做过的真编译；全程不许削弱 Oracle 独立性。**

## 任务 1（实锤、零风险）：把 65s 的 stateful fuzz 用例挪出 fast
监工刚量到：`pytest -m "not slow" -n0` 串行 106s，其中
`tests/test_task_queue_stateful.py::TestTQ::runTest` 一个用例 = **65.69s**（hypothesis stateful fuzz）。它本该 nightly 跑，误挂在 fast。
**做法**：把 `test_task_queue_stateful.py` 整个文件（或该类）打上 `@pytest.mark.slow`，让它只在 `pytest -m slow -n0` 跑。
**验收**：
- `pytest -m "not slow" -n0` 串行总时长应 <60s（原来 106s，去掉 65s）；
- `pytest -m slow -n0` 仍包含该 stateful 测试且全绿（**不许删测试、不许 skip**）；
- 全量 `-m "not slow" -n auto` 仍全绿。

## 任务 2（先侦察再改，可回退）：golden / replay 去重
监工确认 `golden_lock.py:158 import atom_evidence_replay as replay`。560 实测：replay 全量 126.9s 后，golden --check 又把 56 卡整权重放约 131s——**纯重复真编译**。
**T2a 先侦察（不许直接改）**：
- 量 `golden_lock.py check` 当前真实耗时；
- 读它怎么调 replay——是重新真编译每卡，还是读 replay 的增量 manifest / 结果缓存；
- 判断：在"输入冻结、replay 刚跑过且 confirm=56"的前提下，golden 能否**复用 replay 已落盘的结果**（manifest / 缓存 / 上一次 confirm 数）而不是重新编译。
**T2b 若安全则实现**（前提：不削弱独立性）：
- golden 复用 replay 结果后，confirm/refute/infra_error 三个数必须与"重新真编译"**逐字一致**（这是机器判据，不是估计）；
- 若 replay 结果缺失/过期（输入变了），golden 必须**回退到真编译**，不许拿过期结果当新基线——这是 fail-closed；
- 若侦察发现 golden 的"独立复算"本质上就要求重新编译（不是读缓存），**就不改、如实写 worklog 说明为什么不能省**，别为了加速牺牲 Oracle。
**验收**：golden check 耗时对比（改前→改后贴数）；复用态与重编译态的 confirm/refute/infra **逐字一致**；输入改动后能正确回退真编译（回归锁）。

## 任务 3（567 抓到的小修）：run_fuzz 写卡-还原加 try/finally
567 发现：`mutation_fuzz.py` 的 run_fuzz"写卡→跑门禁→还原"段缺异常安全兜底——进程被打断时，变异写的卡残留（EV-CONC-001.md 的 M4 注入残留就是这么来的）。
**做法**：把"写变体→跑→还原原卡"包进 try/finally，保证**任何异常/中断都还原原卡**。
**验收**：人为注入异常（monkeypatch 让门禁步骤抛错）→ 受控卡片仍被还原（git status evidence/ 零残留）；正常路径行为不变。

## 任务 4（机械活）：ruff 存量债
`ruff check tools/ tests/ --output-format concise`（用仓库钉的 0.6.9 版本），逐个修存量告警（此前约 4–15 项），**只改风格不改逻辑**。改完 ruff 全过、相关测试全绿。

---
## 收工验收（fresh）
- 任务 1：`pytest -m "not slow" -n0` 串行 <60s 实测贴数 + slow 组含 stateful 全绿；
- 任务 2：golden 改前/后耗时对比 + 复用态与重编译态三数逐字一致（若 T2a 判定不能省，如实记录不改）；
- gate 61/141（block=0 warn=136）· poison 107/107（双指标 100%）· replay confirm=56 · 完整性 `tool_integrity.py --check` exit 0 · pytest fast/slow 全绿；
- 受控目录 evidence/atoms 零残留；改了 CORE_TOOLS（gate/replay/poison/toolchain/cppbible）就 `--update` 重钉并同 commit 带上；
- 写 `_worklog_568.md`：每个任务改前/改后实测耗时、T2 侦察结论、偏差表。做不完停在任务边界。

## 本批不做
PoC#3/#4/#5（等 trae 564 规格）、M3 单点互斥、命题级 signed_by、B2 golden 多 worker fork 并行（本批只做"结果复用"，不做进程并行——那是更高风险的下一步）。
