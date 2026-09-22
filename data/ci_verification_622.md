# 622 B2 · CI 实跑结果验证（竞态修复是否有效）

> 查询方式：GitHub REST API（公开仓库，无鉴权）
> 目标 run：**#627 / id `35690665032`**，head `96fc0b8`（= 622 B1 的 push）
> 结论先行：**竞态修复已验证有效（gate 无 BLOCK 误报）；CI 整体仍红，但红因是两条与 622 无关的存量债。**

---

## 一、CI 4+1 个门禁 job 的结果（run #627）

| job | conclusion | started (UTC) | completed (UTC) | 耗时 |
|---|---|---|---|---|
| **concurrency-safety**（621 B3 新增） | ✅ **success** | 05:25:45 | 05:25:55 | 10 s |
| pytest | ❌ **failure** | 05:25:45 | 05:29:44 | 3 m 59 s |
| **replay** | ✅ **success** | 05:25:45 | **05:27:22** | 1 m 37 s |
| **gate** | ✅ **success** | **05:27:24** | 05:28:21 | 57 s |
| **quality (3.11)** | ❌ **failure** | **05:27:24** | 05:27:35 | 11 s |
| publish-check / Compile / epub / site / pdf / deploy | ⏭ skipped（上游失败阻断） | — | — | — |

**run 级**：`status=completed`，`conclusion=failure`，`run_started 05:25:42 → updated 05:29:45` = **243 s**。

## 二、🎯 核心验证：`needs: [replay]` 已生效，BLOCK 误报未复现

这是 B2 唯一要回答的问题，答案是**明确的"是"**：

| 证据 | 说明 |
|---|---|
| **`replay` 于 `05:27:22` 结束；`gate` 于 `05:27:24` 才启动** | 间隔 2 秒 ⇒ **gate 真实等待了 replay**，`needs` 被强制执行 |
| **修 needs 前** | `gate` 与 `replay` 同时启动（619 验收即此情形）⇒ gate 采样到 replay 重编译「删旧未写新」窗口 ⇒ **2 条假 BLOCK** |
| `gate` 结论 = **success** | ⇒ **gate 本次未报任何 block 级违规**，**619 的 2 条 BLOCK 误报未复现** |
| `quality` 同样于 `05:27:24` 启动 | ⇒ `quality` 的 `needs: [replay]`（621 B3 追加）也生效 |
| `concurrency-safety` = success | ⇒ 621 B3 新增的静态不变量检查（写者先、读者后）在 CI 通过 |

**⇒ 621 B1/B3 的竞态修复在真实 CI 环境中得到验证：有效。** ✅

### 2.1 运行时长对比

| run | head | 时长 |
|---|---|---|
| #623 | f2c3b33 | 209 s |
| #624 | cdd3b2d | 177 s |
| #625 | cbd0fbd（616） | 220 s |
| #626 | d2f412b（619） | **243 s** |
| **#627** | **96fc0b8（622）** | **243 s** |

修 needs 后（#627）与修之前（#626）**总时长相同（243 s）**。
⚠ **不可据此断言"加 needs 没有代价"**：两次 run 内容差异巨大（#627 含 620–622 全部新工具与单测），
**缺少对照**。可确定的是：`gate` 被推迟到 replay 之后，其自身耗时 57 s 属串行增量，
被 `pytest`（239 s）的并行窗口吸收。

## 三、❌ 两个失败 job 的根因（本地复现，**均非 622 引入**）

### 3.1 pytest 失败 → 治理 manifest 未同步（存量债）

- CI 失败步骤：`Pytest (xdist 并行 · 工具链回归测试)`。
- **本地复现**（同样命令）：`tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches`
  → `AssertionError: 15 项新增差异`。
- 差异来源：`References/architecture_架构演进/` 下出现 **15 个未签入 manifest 的新文件** ——
  `_arch_v21/00_总览.md`、`_arch_v21/01_第一波…`、`_arch_v21/02_第二波…`、`_arch_v21/03_产品经理…`、
  `_arch_v21/zero_pollution.md`、`_auto/inbox/616.md`、`_auto/inbox/617.md`、`_auto/inbox/618.md` …
- **来源批次**：`_arch_v21/` 由**并行 PM 会话** commit **`0b9683f`**（"PM：_arch_v21 外部独立预审查v1存档"）引入，
  且**已存在于 `d2f412b`（619 收工）** ⇒ **先于 620/621/622**。
- ⇒ **与 622 无关**；这解释了为何 #623–#626 **全部 failure**（CI 已红多批）。
- 修复路径（留 623）：`python tools/governance_doc_guard.py update --force` 重签 manifest。
  ⚠ 本批**未执行**：该 manifest 是**防篡改基线**，重签属治理动作，宜由人确认后再做。

### 3.2 quality 失败 → Ruff 存量 lint 债

- CI 失败步骤：`Ruff (tools/ 静态检查硬门禁)`（该 job 后续 31 个步骤全部 skipped）。
- **本地复现**（`ruff check tools/`）：**6 项存量错误**，**全部在 618/619 的旧文件**：

| 文件 | 规则 |
|---|---|
| `tools/pck_certificate_verifier_619.py:14` | F401 `os` 未使用 |
| `tools/pck_renderer_619.py:138` | E702 ×2（一行多语句） |
| `tools/run_619_gate.py:11` | F401 `json` 未使用 |
| `tools/test_classifier_618.py:97` | F841 `primary` 赋值未用 |
| `tools/vfdr_619.py:18` | F401 `json` 未使用 |

- **没有任何 621/622 新文件出现在该清单中** ⇒ 622 的新工具 ruff 干净。
- ⚠ **口径告警（重要发现）**：CI 钉 `ruff==0.6.9`，本机为 **0.16.5**，规则集存在版本差异
  ⇒ 上表是**近似复现**，CI 实际报错集合可能不同。
- **深层原因（值得记入 623）**：618–622 各批都只对**本批新文件**跑 ruff，
  而 CI 跑的是 `ruff check tools/`（**整目录**）⇒ 存量债从未被这些批次发现，CI 因而长期红。
- 修复路径（留 623）：修掉上述 6 处（均为安全修改），或按 CI 钉的 0.6.9 重跑确认精确集合。

### 3.3 无法取得 CI 日志的说明

- `check-runs/{job}/annotations` 仅返回通用 `Process completed with exit code 1`（无 ruff 细节）。
- 完整 job 日志端点需**鉴权**（本批无 token）⇒ 故采用**本地复现**作为证据，并已标注其局限。

## 四、结论

| 问题 | 结论 |
|---|---|
| **gate ∥ replay 竞态是否根治？** | ✅ **是**（gate 在 replay 结束后 2 s 才启动；gate success，无 BLOCK 误报） |
| `quality` 竞态修复是否生效？ | ✅ 是（同样等待 replay） |
| 新增的并发安全检查是否可用？ | ✅ 是（`concurrency-safety` job success） |
| CI 整体为何仍红？ | ❌ 两条**存量债**：治理 manifest 未同步（pytest）+ tools/ 存量 ruff 债（quality） |
| 这两条是否 622 引入？ | ❌ **不是**（manifest 债源自并行 PM 的 `0b9683f`，且在 `d2f412b` 即存在；ruff 债在 618/619 文件） |

## 五、局限性声明

1. **单次 run（#627）**：一次通过不能完全排除竞态（理论上仍存在概率性窗口，
   但 `needs` 是**调度级**保证，非概率手段）；建议后续 2–3 次 run 持续观察。
2. **无法读取 job 日志**（无鉴权）⇒ 失败根因靠**本地复现**推断，非 CI 原始报错。
3. **ruff 版本不一致**（本地 0.16.5 vs CI 0.6.9）⇒ 错误集合为近似。
4. **push 后 B1 的文档 commit 使本地领先远程** ⇒ #627 对应的是 `96fc0b8`，
   **不含** B2 本身及其后的提交；这些提交的 CI 结果需下一批观察。
5. **时长对比缺对照**（内容差异大）⇒ 未能量化 `needs` 的 wall time 代价。
