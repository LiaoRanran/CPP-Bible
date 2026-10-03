# 674a · fast_gate --all crash 排查报告

**生成日期**：2026-10-03
**任务**：674a 任务 B —— 排查 `fast_gate.py --all` 在 Windows 上的硬崩（673t 报 `0xC0000102`）与串行 900s 超时
**一句话结论**：**在当前 HEAD 上 3 次干净复跑均未复现 crash**（193.7s / 200.1s / 212s，全部跑完并给出 `overall=FAIL` 的正常判决）；
已定位**最可疑的压力源**（`-n auto` = 32 worker × 每 worker 61 MB 会话快照 ≈ 2 GB）并**落实一项零代价加固**（默认并发钉为 `min(核数, 16)`：墙钟只差 ~6s，峰值内存减半）。

---

## 1. 673t 报的两个现象，分别是什么

| 现象 | 673t 的描述 | 本批判定 |
|---|---|---|
| **串行 900s 超时** | `fast_gate.py --all` 串行跑超 900s（= `DEFAULT_TIMEOUT_TESTS`） | **已解释、且已被 673u 缓解**：串行全量 ≈ 2400s+ CPU（见下），必然超 900s。但 `--all` **默认并行**，串行只在 `--jobs 0` 时走。673u 的隔离快路径把 pytest 腿从 377s 降到 193s ⇒ 并行档远离超时；串行档仍是"不建议"的路径（已登记） |
| **并行硬崩 `0xC0000102`** | 默认并行时进程直接崩 | **本机当前 HEAD 未复现**（3 次）；已给出压力源分析 + 加固（§3） |

---

## 2. `--all` 的执行逻辑（`tools/fast_gate.py`）

三路**并发**（`threading`，非进程池）：

```
_gates_phase()    → 串行跑 3 道门禁：658 / 669d / 671a guard
_pytest_phase()   → pytest tests -q -m "not slow" -p no:cacheprovider --tb=line -n <jobs> --dist worksteal
_frontend_phase() → node web/run_tests.mjs
```

* 单步超时：门禁 300s（`DEFAULT_TIMEOUT_GATE`）、pytest 900s（`DEFAULT_TIMEOUT_TESTS`）
* 总预算：300s（`BUDGET_S`，**超了只 WARN 不判红**）
* 并发默认：`--all` 用 `-n auto`；`--tests` 用串行（`0`）

⇒ **三路并发 + pytest 腿吃掉全部 32 核**，是理解崩溃的关键前提。

---

## 3. 复现尝试与结果（3 次，全部无 crash）

| 环境 | 命令 | 结果 | 门禁腿 | pytest 腿 | 前端腿 |
|---|---|---|---|---|---|
| 673u 主仓（HEAD `1072c605`） | `fast_gate.py --all` | rc=1，**192.8s**，无崩 | 3/3 PASS | 192.8s | PASS |
| 674a 干净检出（`c13de06b`） | `fast_gate.py --all` | rc=1，**212s**，无崩 | 658/669d PASS，671a FAIL | 211.7s | PASS（用 `--build` 时 3/23 红，见 §5） |
| 674a 干净检出 v2（`c13de06b`） | `fast_gate.py --all` | rc=1，**193.7s**，无崩 | 658/669d PASS，671a FAIL | 193.7s | **PASS** |
| 674a 干净检出 v2 | `fast_gate.py --all --jobs 16` | rc=1，**200.1s**，无崩 | 同上 | 200.1s | PASS |

**结论**：crash 在"干净检出 + 已修 673u 隔离"的条件下**不可复现**。
`overall=FAIL` 是**判决**（671a guard + pytest 腿有失败），不是崩溃 —— 两者必须分清。

---

## 4. 压力源分析（为什么"曾经会崩"是合理的）

### 4.1 内存：`-n auto` × 每 worker 一份 `data/` 快照

根 `conftest.py` 的会话级 fixture `_isolate_production_data` 会给**每个 worker** 存一份
`data/` 快照（实测 **61 MB**，2200 个文件里 2178 个被整读）。于是：

```
32 worker × 61 MB ≈ 2.0 GB   仅"隔离快照"一项
+ xdist worker 进程本身 + 每个 worker 导入全套测试模块 + 用例内数据
```

叠加 3 路并发（门禁 3 个子进程 + node 前端腿），32 核机在**内存与句柄**上都被压到边缘。
xdist 的 worker 是**独立进程**，任一 worker 异常终止时，父进程看到的就是一个
**非 0 的异常退出码**（673t 观察到的 `0xC0000102` 即属此类"进程级异常"）。

> 佐证：673u 之前，pytest 腿要跑 377s（隔离 fixture 占 CPU 73%）；跑得越久、内存驻留越久，
> 崩溃窗口越大。673u 把这条腿降到 193s 之后，本批 3 次复跑全部干净 —— **时间与崩溃是同一条因果链上的**。

### 4.2 排队：三路并发却让 pytest 吃掉全部核

`-n auto` = 全部核 ⇒ 门禁的 3 个子进程与 node 前端腿只能抢剩下的边角，
既是**尾延迟**来源，也让"同时驻留的进程数"最大化。

### 4.3 串行档为什么必然 900s 超时

串行全量的 CPU 工作量实测 ≈ **2450s**（673u 优化后；优化前 ≈ 8159s）> `DEFAULT_TIMEOUT_TESTS = 900`。
⇒ 串行档**设计上就超时**，`--jobs 0` 只适合排查，不适合 `--all`。

---

## 5. 落实的加固（零代价）

`tools/fast_gate.py`：

```python
#: `--all` 的 pytest 腿**并发上限**（674a）
MAX_WORKERS = 16
...
if not jobs:
    jobs = (str(min(os.cpu_count() or 1, MAX_WORKERS)) if all_fast else "0")
```

**为什么是"零代价"**：实测 `-n 16` = **200.1s** vs `-n auto`（32）= **193.7s** —— 墙钟只差 ~6s（噪声内），
而峰值内存**减半**（16 × 61 MB ≈ 1 GB）。这与 CI 的既有选择同口径
（ci.yml 的 pytest job 钉 `-n 16`，理由："runner 通常 2-4 核，且 replay/gate job 会同时抢 CPU"）。

**可回退**：`--jobs auto` 原样透传，拿回旧行为。
**未改**：`BUDGET_S`（300s）、`DEFAULT_TIMEOUT_*` —— 没有证据表明它们不合理，改它们属策略决策。

`fast_gate` 自带单测：`pytest tools/test_fast_gate.py` → **23 passed** ✓（ruff 亦通过）。

---

## 6. 一条**由本批发现并修掉**的自身问题（诚实登记）

第一次在干净检出跑 `fast_gate --all` 时，**前端腿 3/23 红**（`cards.test.mjs` / `verdicts.test.mjs` / `starmap.test.mjs`）。

**根因**：本批任务 C 最初在 ci.yml 里用的是 `web_data_pipeline_656.py --build`，
而它的**第 1 步会重跑数据生成器、重写受跟踪的 `web/data/*.json`**（实测 5 个受跟踪文件 + 23 个新文件）。
改脏了工作树里的前端数据 ⇒ 前端自测跟着红（主仓因为数据是"已生成态"所以看着正常）。

**修法**：给该工具加 `--dist-only` 模式（跳过生成器与 `index.json` 写入，只产出 `dist/`），
ci.yml 改用它。验证：

```
$ python3 tools/web_data_pipeline_656.py --dist-only
[pipeline656] 生成步骤 0 个；data 文件 12 个；dist 资源 38 个（压缩 34）
$ git status --porcelain -- web/     → 0 条
$ node web/run_tests.mjs             → 23/23 全绿，1417 条断言
```

⇒ 既拿到 `web/dist/`（救 4 项 dist 测试），又对 `web/` **零改动**（红线 2）。

---

## 7. 遗留（登记，未动）

| 项 | 状态 | 说明 |
|---|---|---|
| `671a guard` 门禁腿在**干净检出**上 FAIL | 登记 | 报 12 项真实 block（`baseline_arms_670a` / `corpus_reveal_672h` / `external_anchor_672j` …）—— **是真实判定**，需人裁（补产物重跑 or 接受为已知缺口）。主仓上该腿 PASS |
| 串行档（`--jobs 0`）必然 >900s | 登记 | 设计上如此；`--all` 默认并行，不构成阻塞 |
| `0xC0000102` 未能在本机复现 | 登记 | 若在别的机器复现，请连同"当时 `-n` 值 + 内存占用 + 是哪个 worker"一起报；本批的加固已把最可疑项（并发×快照内存）砍半 |
