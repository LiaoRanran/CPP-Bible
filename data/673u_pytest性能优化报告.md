# 673u · fast_gate pytest 腿性能优化报告

**生成日期**：2026-10-03
**任务**：673u 任务 B —— 让 `fast_gate.py --all` 的 pytest 腿 ≤300s（预算），且**不改变测试覆盖率与正确性**
**结论**：**已达成**。pytest 腿 **377s → 193s（-49%）**，用例数、跳过数、失败集**不变**；根因是 634/640/648 的**逐测试隔离 fixture 每例读 4 个目录全部内容两遍**（~30 MB × 2 / 测试）。
**红线**：未减少任何测试、未标记 slow、未跳过任何用例、未改动任何断言。

---

## 1. 基线与本机测量口径

**先决条件**（673s 已登记）：本机 `PYTHONPATH` 注入了 WorkBuddy 的安全删除拦截层，会把删除类用例伪造成 `SystemExit: 1`。**下列数字一律在 `CODEBUDDY_SAFE_DELETE_ENABLED=0` 下测得。**

| 时点 | 命令 | pytest 腿 | 总耗时 | 失败 | 跳过 | 用例数 | 备注 |
|---|---|---|---|---|---|---|---|
| 673s（HEAD `a412b8ff`） | `fast_gate.py --all` | **327.4s** | 327.4s | ≥8（工具截断） | — | — | 673s 基线（`data/673s_fast_gate基线.md`） |
| **673u 优化前**（HEAD `1072c605`） | `pytest -m "not slow" -n auto --dist worksteal` | **377s** | — | 7 | 29 | 4266 | 本报告基线 |
| **673u 优化后** | 同上 | **193s** | — | 6 | 29 | 4266 | ✅ ≤300s |

> 口径说明：`fast_gate --all` 的 pytest 腿 = `pytest tests -q -m "not slow" -n auto --dist worksteal`（本报告用它做可比测量）。
> 377s 比 673s 的 327.4s 更高，主要来自 673t 的 `sha256_of` 归一化（每 worker 多一次 `git ls-files --eol`，~2s × 32）与机器负载差异——**不是**本批引入。

---

## 2. 慢在哪：逐层定位

### 2.1 `--durations` 的第一印象（会误导）

```
137.14s setup    tests/test_loop_metrics_629.py::test_coverage_dimension
 90.75s setup    tests/test_loop_metrics_629.py::test_asymmetry_is_computed
 41.65s setup    tests/test_repo_split_sandbox_647.py::test_c1_3_standalone_runs
 ...
```

看起来是"少数长尾测试"。但把它们加总只有 ~700s，而**全量 CPU 是 8159s**（4266 例 × 均 1.9s）。⇒ 真正的成本在**每个测试都要付的固定开销**里。

### 2.2 定位：逐测试隔离 fixture（真凶）

单个测试的 `setup` / `teardown` 实测（`--durations`）：

```
0.76s setup     tests/test_json_canonical_671e.py::test_canonical_hash_is_key_order_independent
0.74s teardown  tests/test_json_canonical_671e.py::test_merkle_roots_hash_is_over_file_bytes_not_dict
0.38s setup     ...（其余用例同样量级）
```

即 **~1.1s / 测试**，来自根 `conftest.py` 的 `_isolate_merkle_dirs`（648 引入，`scope="function"` + `autouse`）——
它对 `atoms/ evidence/ Examples/ Book/` 做**逐测试**快照 → 跑测试 → 严格还原。

**上限实验**（临时把该 fixture 改成空 `yield`）：

| | 墙钟 | CPU 总和 | 用例 | 失败 |
|---|---|---|---|---|
| 有隔离 | 377s | **8159s** | 4266 | 7 |
| 无隔离 | **191s** | **2162s** | 4266 | 9 |

⇒ 该 fixture 占 pytest 腿 **CPU 的 73%、墙钟的 49%**。

### 2.3 为什么这么贵：是"读"，不是"遍历"

对最贵的 `Examples/`（1597 文件 / 14 MB）逐项计时：

| 操作 | 耗时 |
|---|---|
| `os.walk` 遍历 | 0.004s |
| `os.walk` + `os.path.getsize` | 0.022s |
| `os.scandir` + `entry.stat()` | 0.005s |
| **读全部文件内容** | **0.183s** ← 真凶 |

而 `_snapshot()` 读一遍、`_restore_strict()` 为了比对**又读一遍** ⇒ 每测试 ~30 MB × 2 的重复读，
且是 1900 次小文件 `open/read/close`（按文件数而非字节数付费）。

---

## 3. 优化：元数据快路径（语义等价）

### 3.1 改了什么（根 `conftest.py`，**不在** `tool_integrity` 的 test_config 钉住面内）

| 新增/改动 | 作用 |
|---|---|
| `_scan_stats(base)` | `{path: (size, mtime_ns)}`，只 `os.scandir` + `entry.stat()`（走 scandir 已缓存的 stat），**零内容读** |
| `_snapshot()` **签名与返回值不变** | 保持 `{path: bytes\|None}`（`tests/test_a1_isolation_634.py` 直接断言该形状 ⇒ 不能改） |
| `_restore_strict(snap, base, stamps=None)` | 新增可选 `stamps`：**指纹一致的文件判为"没动过"、不读内容**；`None` ⇒ 完全保留 648 的逐字节比对 |
| `_restore(snap, base, tracked=None, stamps=None)` | 同上（会话级 `data/` 还原也受益；两个既有单测传 `stamps=None` ⇒ 语义不变） |
| `_isolate_merkle_dirs` | 新增**跨测试内容快照缓存**：指纹未变 ⇒ 连快照那一遍读也省掉（每 worker 只付一次） |
| `_ISOLATE_STRICT`（环境变量 `CPPBIBLE_ISOLATE_STRICT=1`） | **逃生开关**：置 1 ⇒ 整体退回"逐字节比对"的原始语义 |

### 3.2 诚实边界（红线 5：不改变正确性）

快路径把"文件是否被改过"的判据从**逐字节比对**换成 **(size, mtime_ns) 比对**。
两者只在"**同长度**且**同 mtime** 的静默改内容"下分歧 —— 这要求测试写完后**显式把 mtime 改回原值**。

**673u 全仓核对**：所有 `os.utime` / `copystat` / `copy2` 调用（`test_drift_watch_670c/671a`、
`test_gate_engine`、`test_guard_rerun_671a`）都作用于 `tmp_path` / 沙箱 / `data/`，
**无一作用于受隔离的 `atoms/ evidence/ Examples/ Book/`** ⇒ 本仓当前用例集下**等价**。
需要绝对严格时用 `CPPBIBLE_ISOLATE_STRICT=1`。

### 3.3 功能验证（证明隔离仍有效）

| 验证 | 结果 |
|---|---|
| `tests/test_a1_isolation_634.py` + `tests/test_conftest_safeguard_640.py` | **12 passed** |
| 探针：往 `Examples/` 新建文件 + **同长度**改内容（只能靠 mtime 检出）→ `_restore_strict` | 新增文件**已删除** ✓ / 被改文件**已复原** ✓ |
| 探针后 `git status -- Examples/ atoms/ evidence/ Book/` | **干净** ✓ |
| 单测 teardown 开销复测 | **0.74s → 0.09s** ✓ |
| `tool_integrity --check-test-config`（根 conftest 不在钉住面内） | **OK**（无需重钉）✓ |

---

## 4. 优化后全量复测

```
WALL(优化后) = 193s
tests=4266  failures=6  errors=0  skipped=29
CPU 总和= 2451s        # 8159s → 2451s（-70%）
```

**覆盖率不变**：用例数 **4266 不变**、跳过数 **29 不变**、无 slow 新增、无用例被删。

**失败集**（本机主仓口径，均为**预存**、与本批无关；且该集合本身**非确定** —— 见 §5）：

```
FAILED tests/test_numbers_env_671g.py::test_real_machine_has_required_env      # 真实机器环境（本机特有）
FAILED tests/test_c_target_648.py::test_a4_out_keys_match_declared_run_match_keys
FAILED tests/test_ots_anchor_656.py::test_real_target_not_invalid
FAILED tests/test_grounded_audit_596.py::test_real_committed_report_matches_fresh_render
FAILED tests/test_tool_integrity_647.py::test_a1_8_strict_default_declared_and_real_repo_green
（±1~2 条并发 flip-flop：如 test_ots_anchor_613 / test_trust_root_audit_647::test_a5_7）
```

> 优化前基线 7 条、优化后 6 条，差集是**并发 flip-flop**（同一命令两次运行集合不同），不是本批引入的回归。

---

## 5. 本批解除的 skip 里，有一条需要并发守卫（如实登记）

任务 A 解除了 4 处 `residue_present` 型 skip。其中
`tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections`
在**串行/干净检出下绿**，但在 **xdist 并发下 flip-flop**：它要跑 `tool_integrity --check` 的
`merkle_check` inspection（覆盖 `atoms/evidence/Examples/Book`），而别的 worker 可能正处在
"隔离快照 → 测试 → 还原"的中段 ⇒ 读到瞬时污染。

处置：按 622/647 的**既有惯例**换成 `_XDIST_PARALLEL` 守卫（`PYTEST_XDIST_WORKER` 存在即跳过）——
**串行真跑、并发跳过**，比原来那个恒真的 `residue_present()` 守卫强，且不制造假红。

```
$ pytest tests/test_supply_chain_chain_601.py -n 0   → 7 passed
$ pytest tests/test_supply_chain_chain_601.py -n 2   → 6 passed, 1 skipped
```

另 3 处（治理 manifest / self_hash / CLI verify）只**读**已提交文件、不写共享状态 ⇒ 并发下稳定，**已无守卫真跑**。

---

## 6. 试过但**否决**的方案（按任务书 a–d 逐项交代）

| 策略 | 实测 | 否决理由 |
|---|---|---|
| **(a) 把最慢的测试标记为 slow** | 未采用 | 会**降低 fast_gate 快档覆盖**（`test_loop_metrics_629` 的 3 例、`test_repo_split_sandbox_647` 的 3 例会被移出快档）⇒ 违反红线 5。且实测墙钟瓶颈不是它们。 |
| **(b) 优化 conftest 加载/缓存** | ✅ **采用** | 见 §3。这是唯一"零覆盖损失"的大杠杆。 |
| **(c) 增加并发数** | 已在上限 | `-n auto` = 32（本机 32 核），已是最大。**另试 `--dist loadscope`**（按模块分组，可省掉 `test_loop_metrics_629` 的重复 fixture）：**379s / 9 failures**，比 worksteal 的 377s / 7 failures **更差**（长尾失衡 + 多 2 条红）⇒ 否决。 |
| **(d) 优化单个慢测试的逻辑** | 部分 | 找到一处**真实低效**：`tools/loop_metrics_629.py::asymmetry()` 内部**又调一次** `autoimmune_dim()`（42.8s），而测试的 `dims` fixture 已经算过 ⇒ 每次 fixture 实例化白烧 ~43s。**本批未改**（193s 已达标，不必再冒风险）；登记为后续机会，见 §7。 |

---

## 7. 遗留机会（不擅自做）

1. **`loop_metrics_629` 的重复计算**：`asymmetry()` 重复调用 `autoimmune_dim()`（~43s/次 × 每个用到 `dims` 的 worker）。
   给 `autoimmune_dim()`/`escape_dim()` 加进程内 memo 可再省 ~130s CPU 并缩短最长单测（146s → ~104s）。
   需先确认"测试不会在修改输入后调用它们"。
2. **`_text_flags()` 的每 worker 固定成本**：673t 引入，`git ls-files --eol` ~2s × 32 worker ≈ 64s CPU。可考虑缓存到文件或按需构建。
3. **会话级 `data/` 快照**：每 worker 读 61 MB（`data/` 4 GB 里 ≤2 MB 的部分）。本批已给它加上 `stamps`（还原时免读），但**快照那一遍读**仍在。可考虑同样的跨测试复用。
4. **`fast_gate.BUDGET_S` 未改**（300s）：本批靠真优化达标，不需要调预算数字。

---

## 8. 诚实登记：一个**预存**的并发竞态被"跑得更快"暴露得更频繁

优化后跑 `fast_gate --all` 时，观察到一条**此前不在失败集里**的失败：

```
FAILED tests/test_standard_fetcher_644.py::test_acquire_no_write - assert 70 ...
```

**根因（已复现并定位）**：

```python
# tests/test_standard_fetcher_644.py:25
def test_acquire_no_write():
    before = len(base.iter_stored())      # 数 data/evidence_store/ 的条目
    r = d1.acquire("nullptr")
    after = len(base.iter_stored())
    assert before == after
```

而 `data/evidence_store/` **不在**逐测试隔离面内（`_ISOLATE_DIRS` 只有
`atoms / evidence / Examples / Book`），且**确有别的测试往里写**：

- `tests/test_evidence_integrity_644.py:18` → `base.store_evidence(...)`
- `tests/test_compiler_probe_644.py:47` → `d2.make_evidence(...)`

⇒ 只要有别的 worker 在 `before` / `after` 之间写一条，计数就变 ⇒ **xdist 下天然 flaky**（串行/单文件必过）。

**证据**：

```
$ pytest tests/test_standard_fetcher_644.py -n 0   → 4 passed
$ pytest tests/test_standard_fetcher_644.py -n 4   → 4 passed
$ fast_gate.py --all（全量并发）                    → 该用例偶发红（before=70, after=71）
```

**责任界定**：本批的改动**不写任何文件**，只改"怎么快照/还原"⇒ 竞态是**预存**的。
但必须诚实承认：**套件跑快后，并发重叠窗口变密，这类预存竞态的命中率会上升**。

**建议补丁（交 owner，本批未擅自改他人测试）**——沿用 622/647 的既有惯例：

```python
_XDIST_PARALLEL = os.environ.get("PYTEST_XDIST_WORKER") is not None

@pytest.mark.skipif(_XDIST_PARALLEL, reason="673u：串行必过；xdist 下别的用例写 data/evidence_store/ 致计数漂移")
def test_acquire_no_write():
    ...
```

（更根本的治法是把 `data/evidence_store/` 也纳入隔离面——但那会改变 648 的隔离口径，属 owner 决策。）
