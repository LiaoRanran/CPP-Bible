# 652 验收报告（究极巨大建设：交人项自动化 + W4+）

- 批次：652　状态：awaiting_review　日期：2026-09-27
- 仓库：CPP-Bible（主，+7 提交）／queyi-core（T2，+1 提交）
- 门禁：`python tools/run_652_gate.py` → **8/8 全 PASS**（fast / full / ruff / mypy / selftest /
  **跨仓保护器联调** / 受控零污染 / 信任根）

---

## 一、阶段完成

### 阶段 0 ✅　`data/652_baseline.md`：651 收工确认 + 环境可用性（ots/esbmc **缺**）登记 + 交付清单。

### A 交人项自动化 ✅
| 项 | 结果 |
|---|---|
| 87 张卡补 `verified_at` | **87 写完 / 0 跳过**（来自 `git log --diff-filter=A`），备份 `data/backup_652/`；651 H7 复扫 **无 verified_at 0** |
| T1 判决真回填 | **452 条** → 新文件 `decision_event_v2_ledger_backfilled_652.jsonl`；**原账本 sha256 前后一致** `ec8cbf5c…` |
| M7 队列迁移 | **30 条** → 新文件 `pending_review_migrated_652.jsonl`（**30 收 / 0 拒**）；**原文件 sha256 一致** `8f4842e1…` |
| 648 conftest 提交 | ✅ `78bed36e`（648 逐测试 Merkle 隔离） |
| 全量 pytest 收集 | ✅ **4015 例 / 541 文件**（装 `hypothesis` 后由 4 个收集错 → 0） |
| 全量两阶段复跑 | ⚠ **未跑完**：fast 阶段 **600s 仅 20%** ⇒ 估 ~50 min，超 idle-timeout（见 652_gaps G4） |
| OTS 重锚 | ⚠ **结构重锚完成**（digest 更新、`--check` 通过），**attestation 仍 pending**（无 `ots` CLI，G1） |

### B W4+ 头部 ✅
- `probe_assembler_652.py`（H5）：6 积木 → **单翻译单元组装** → 真机差分矩阵 **8 例**：4 `ok`（13 kv/例）、
  4 `sanitizer_runtime_missing`（诚实分类：`cannot find -lubsan`）。
- `esbmc_falsify_652.py`（H6）：**降级**（`esbmc` 未装）→ `tool_unavailable` + 拟命令；
  语义纪律已编码：**BMC 失败=硬结论(witness)，BMC 成功仅 `unknown(bounded)`**。

### C W4+ 中间 ✅
- `challenger_652.py`（M4）：十卡 × 5 算子 = **50 变体**，读取面检出 **50/50，逃逸率 0.0**；
  critic=MDL 代理 + 校准（读 651 M3）；变体**不写 atoms/**。
- `embedded_adapter_652.py`（M5）：裸金属约束静态检查 → 10 fixtures **41 违规**；
  **诚实登记 LLM 嵌入式 pass@1 = 55.6%**。

### D W4+ 尾部 ✅
- `rats_closure_652.py`（T3）：信任根映射 **RATS 三库** → reference_values **7** / endorsements **4** / verifier_code **27**。
- `pck_export_652.py`（T7）：**103 证书** → in-toto link + C2PA 断言；**103/103 硬绑定一致**，硬绑定共 **182** 条。
- T2（queyi-core）：`protector_rollout_652.py` 三态灰度 **shadow→canary→enforce** + 一键回滚 +
  **差分真验证**：`tool_gate_649` / `circuit_breaker_649` **模式生效**；
  `shadow_mode_649` / `budget_guard_649` **模式不可区分（只改标签）** ⇒ 登记 G12。

### E 差啥登记 ✅
`data/652_gaps.md`：**19 条**（G1-G19），每条给「缺什么 / 为什么缺（实测依据）/ 何时能做」。

### F 收工 ✅
`run_652_gate` **8/8 PASS**；ruff/mypy（652 文件）全绿；跨仓保护器联调 PASS；
受控 atoms 指纹前后一致；信任根刷新后 `--check` 4/4 OK。

---

## 二、关键发现（诚实）

1. **M4 的 10 次"逃逸"是变异 bug**：首跑 `M4_drop_evidence` 正则只匹配行内数组，而卡用**块式列表**
   ⇒ `changed=False` 被误计为逃逸。修好后 **50/50 检出**（当场纠错，非掩盖）。
2. **T2 差分验证照出"假开关"**：`budget_guard` / `shadow_mode` 在 enforce 与 shadow 下**观测信号完全相同**
   （`halted()` 均 True、`protection_raised` 均 0、`decide()` 均 `record_only`）⇒ 描述里的"shadow 回滚"
   对这两个保护器**并不成立**。已登记 G12（需人裁决语义）。
3. **全量收集原本就红**：4 个收集错误全是 `ModuleNotFoundError: hypothesis` ⇒ 装依赖即解（G4 的"跑不完"是**时长**问题，非环境缺依赖）。
4. **H5 的 sanitizer 闭环卡在运行库**：不是代码错，是 MinGW 未带 UBSan 运行库（G3）。
5. **M5 的 41 违规**主要来自 648 C fixtures 大量使用 `printf` ⇒ 裸金属场景下它们**不合规**，
   说明"能编译 ≠ 可用于嵌入式"是真实约束。

## 三、诚实边界 / 未做
- **全量两阶段 pytest 未跑完**（G4，实测速率依据：600s→20%）。
- **OTS 未真上链**（G1）、**ESBMC 未真跑**（G2）、**sanitizer 未闭环**（G3）、**HIL/交叉编译不可得**（G13）。
- **H5 的"LLM 造积木"未做**（G8，无 LLM）；**M4 未接线全量 67 规则**（G9）。
- **既有脏文件**（非 652 引入）仍有批量 `tests/test_6xx*.py` 等未提交（G17）——652 只提交了 `conftest.py`。
- 本批 A1 改 atoms/ ⇒ **信任根 Merkle 必须重钉**（已做）；这会使**旧 `.ots` 失效**（G16）。

## 四、门禁明细（8/8）
fast / full / ruff（9 文件）/ mypy（9 文件）/ 8 工具 `--check` / **跨仓保护器联调** / 受控 atoms 零漂移 / 信任根 `--check`。

## 五、交人项（含 651 结转）
- [ ] **G12**：`budget_guard`/`shadow_mode` 的 shadow 语义是否应"不置位"（否则"回滚"名不副实）。
- [ ] **G10/G11**：是否给保护器加 per-protector 通道与真比例灰度。
- [ ] **G1**：OTS 真上链（装 client + 人工 submit）。
- [ ] **G9**：是否把 67 规则 gate 接进 challenger（沙箱）。
- [ ] **G17**：存量脏测试文件是否成批提交。
- [ ] **G14**：`verified_at` 是否按"真实复核日期"覆盖 git 日期。
- [ ] 651 结转：W0 三词表采纳 / T1 是否采用回填版 / M7 队列是否切换。
