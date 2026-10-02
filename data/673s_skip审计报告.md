# 673s · skip 审计报告

**生成日期**：2026-10-02
**审计对象**：`tests/*.py` 下全部 `@pytest.mark.skip` / `skipif` / 运行期 `pytest.skip(...)` 站点
**方法**：静态枚举（脚本解析 75 个站点）+ 实跑取证（`CI=true pytest -n 16 -rs`，捕获**实际生效**的 84 条 SKIPPED）+ 逐条处置验证

> 结论：**真正能解除的只有 1 处（我自己在 673p 引入的回归）**；另有 4 处**看似可解除、实测不可解除**（解除后 4/4 全红），已把**真实阻塞原因**写回 reason。
> 其余 70 处属条件守卫 / 环境依赖 / 红线阻塞，按原设计保留。

---

## 1. 总量与分类

静态站点 **75** 个；实跑**实际生效**的跳过 **84 条**（含参数化展开）。

| 类别 | 站点数 | 实际生效 | 处置 |
|---|---|---|---|
| ① 条件守卫（`skipif`，条件当前**不成立** ⇒ 不跳过） | 20 | 0 | 保留（设计如此） |
| ② `_XDIST_PARALLEL` 并发守卫（673m 设计） | 7 | 7 | 保留（串行真跑、并发跳过） |
| ③ `CI=="true"` 平台守卫（MinGW / Windows 特有） | 9 | 0（本地） | 保留 |
| ④ 运行时条件（缺产物 / 锁被占 / 无 g++ / 人审通道不存在） | 12 | 少量 | 保留 |
| ⑤ 673h「内容同步」无条件 skip | 16 | 16 | 保留（红线：research/ + 并发 flip-flop） |
| ⑥ 陈旧守卫：`residue_present()` 型 | 4 | **4（含 CI）** | **不可解除（实测）**，已改写 reason |
| ⑦ 永久不可解除（探针/实证件未随仓保留） | 3 | 3 | 保留 |
| ⑧ **本批解除** | **1** | — | ✅ 已解除（见 §2） |

---

## 2. 已解除（1 处）：673p 引入的 seed-check 回归

**不是**已有的 skip 被摘掉，而是**我在 673p 新增的两个工具**让
`tests/test_seed_check_671i.py::test_real_repo_seed_state_is_locked` 变红
（该用例的设计就是"任何**新增**未固定种子的脚本都会改变集合 ⇒ 红"）。CI 会因此变红，
故属 673s"为 push 后 CI 准备"的范围内。

**根因（两类，分别处理）**：

| 文件 | 根因 | 处置 |
|---|---|---|
| `tools/verifier_pool_673p.py` | **真误报**：`random.sample` 字样只出现在**注释与报错文案**里，代码零随机性 | 改写文案（"随机抽样"），不再被扫中 |
| `tools/selection_strategies_673p.py` | 与既有 6 个文件**同一形态**：`random.Random(seed).sample(...)`（seed 由 CLI 传入、默认 `20260930`），而扫描器只认全局 `random.seed()` | 登记进 `KNOWN_LOCAL_RNG_WARNS`（该常量本就是为"口径限制"设的登记表） |

**验证**：
```
pytest tests/test_seed_check_671i.py -q -n 0            → 7 passed
pytest tests/test_verifier_pool_673p.py tests/test_selection_strategies_673p.py -q -n 0 → 57 passed
```

---

## 3. 看似可解除、实测**不可**解除（4 处）—— 本批最重要的审计发现

### 3.1 现象

4 个站点用同一个守卫：

```python
@pytest.mark.skipif(clr.residue_present(), reason="本地未跟踪残留(_arch_v2x/)干扰治理清单断言；CI 无残留应通过(631 A4)")
```

守卫语义是"**本地**有未跟踪残留 ⇒ 跳过；**CI 没有 ⇒ 应该真跑**"。

### 3.2 实测：守卫恒真，这 4 个用例在 CI 也**从未跑过**

`tools/ci_pytest_final_clear_632.py::residue_present()` 只判断目录**是否存在**，
而 `RESIDUE_DIRS` 里那 6 个目录**已全部入库**：

| 目录 | tracked 文件数 |
|---|---|
| `_arch_v19` | 39 |
| `_arch_v20` | 23 |
| `_arch_v21` | 15 |
| `_arch_v22` | 8 |
| `_arch_v23` | 6 |
| `_adv_v80` | 77 |
| **合计** | **168** |

⇒ `residue_present()` **恒为 True**（任何检出、包括 CI）⇒ 护栏语义**反转**：
本该在 CI 真跑的 4 个用例被永久跳过。

### 3.3 解除实验：摘掉守卫后 4/4 全红

在干净 worktree 里把 `_adv_v80` 从 `RESIDUE_DIRS` 摘掉后复跑：

```
FAILED tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified
FAILED tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches
FAILED tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash
FAILED tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections
```

统一根因：`[gov] manifest 不一致（634 处）` —— `data/governance_docs_manifest.json`
与真实文档树漂移 **634 处**（这些 `_arch_*` 目录入库时**没有同步治理清单**）。

### 3.4 处置：**不解除**，改写 reason 写清真实阻塞

- 我确实改了 `residue_present()` 的实现（改成"存在 **且** 未跟踪"，语义上更正确），
  但实测它会把 4 个用例由绿转红 ⇒ **已 `git checkout` 回退**，不制造新的红源。
- 按任务书"对不能解除的：在 skip reason 里写清楚阻塞原因和解除条件"，
  把 4 处 reason 改写为真实原因（保留原装饰器，语义等价，不影响任何断言）：

> 673s 实测修正：阻塞原因**不是**未跟踪残留 —— `_arch_v19..v23/_adv_v80` 已全部入库
> （168 文件 tracked）⇒ 守卫恒真、本用例在 CI 也从未跑过。真阻塞是
> `data/governance_docs_manifest.json` 与真实文档树**漂移 634 处**。
> 解除条件：owner 重生成/重钉治理清单（治理动作，673s 红线 4 不擅自清票）。

**验证**：改后 4 个文件仍正常收集、该 4 用例仍跳过、其余用例不受影响（`s...s......s...............s.`）。

---

## 4. 不可解除的 16 处「673h 内容同步」（红线）

全部为**无条件** `@pytest.mark.skip`，两类根因：

| 根因 | 站点 | 为什么不能在本批解除 |
|---|---|---|
| 读 `research/` 论文正文或 `web/data/*` | `test_baseline_672f`、`test_caliber_check_669`×2、`test_number_consistency_671g`、`test_paper_sync_670c2`×2 | **红线 1 / 2**：不碰 research/、web/。数字同步归论文线与前端线 owner |
| 真实仓门禁并发 flip-flop | `test_master_gate_671a`×6、`test_gates_redpath_671g`、`test_terminology_671g`、`test_ig_cards_665`、`test_e_671g` | 并发批次持续改写共享产物；非本批可单独稳定修复 |
| 复制层漂移 | `test_split_670c` | 需 656 批次重跑 |
| `tests/` 的 ruff I001 整理 | `test_mypy_fix_625` | CI 只对 `tools/` 做 ruff，`tests/` 不入门禁；属独立批次 |

---

## 5. 保留但已带明确 reason 的其它类别

- **② `_XDIST_PARALLEL`（7 处，673m 设计）**：`skipif(_XDIST_PARALLEL)` ——
  串行**真跑且全过**，仅 xdist 并发下因 622 沙箱锁 / 647 信任根读写争用跳过。
  **这是"条件跳过"而非"永久跳过"**，语义正确，保留。
- **③ `CI=="true"`（9 处）**：依赖本地 MinGW 编译产物 sha（`build_reproducibility_603/608`、
  `ccache_prefix`×2、`recompile_extended_610`、`replay_invariants_605`、`pe_timestamp_caliber_611`、
  `task_queue`）。CI 是 ubuntu，产物 sha 必然不同 ⇒ 保留。
- **④ 运行时条件（12 处）**：`无 g++` / `锁被占` / `人审通道不存在` / `no confirm card` 等，
  都是**当时状态**判定，非永久阻塞。
- **⑦ 永久（3 处）**：`test_stat_bounds`（`_arch_v6/probe_bounds.py` 未随仓保留）、
  `test_viso_diff`×2（沙箱实证件已清理）。**解除条件：把对应探针/实证件重新入库**，
  否则永久保留。
- **`test_run_630_gate.py:66`**：`skipif(_ahead_of_remote() > 0)` ——
  当前 ahead=18 ⇒ 跳过；**push 后自动恢复真跑**。属正确设计，无需动。

---

## 6. 本批未做（明确交 owner）

1. **`residue_present()` 的语义修正**（存在 → 存在且未跟踪）：方向正确，但会连带 4 个用例变红。
   建议与"重钉治理清单"**同批**做（先补清单，再改守卫），否则按下葫芦浮起瓢。
2. **4 处 `residue_present` 型 skip 的解除**：等治理清单同步（634 处）后自动可解。
3. **16 处 673h 内容同步 skip**：需论文线 / 前端线 owner 同步后解锁（见 `data/673h_内容同步报告.md`）。
4. **`_arch_v19..v23` + `_adv_v80` 是否该继续留在仓库**：168 个 tracked 文件属历史归档，
   是否归档/移出仓库是 owner 的取舍（本批不动）。
