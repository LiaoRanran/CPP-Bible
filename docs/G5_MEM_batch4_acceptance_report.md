# G5 MEM 第四批 · 验收报告（PERF-003 原子化）

> 日期：2026-09-12 · 人审签署：`human:liaoranran` · 状态：**已原子化 + 已推送**

---

## 一、原子化结果

| 项 | 结果 |
|---|---|
| 原子 | `atoms/mem/ATOM-MEM-PERF-003.md` · `status: verified` · `verified_by: human:liaoranran` · `verified_at: 2026-09-12` |
| 编号确认 | `PERF-001`/`PERF-002` 已存在（第一/二批）⇒ 本颗为 **PERF-003** ✅ |
| 自评字段 | `rubric_self: 4/5` 已删除；改写入正文 **「5 分锚定依据（人审授予，2026-09-12）」** 节（三条） |
| 草稿目录 | `goldens/mem/` 已清空（草稿移出，gate 恢复全量扫描） |
| 误解 | `MIS-MEM-028`（内容类：布局不可移植）、`MIS-MEM-029`（**方法论类**：性能结论须标条件 + 基准须控制变量） |
| 证据 | `EV-MEM-038`（SSO 跨实现 + 同驱动对照）、`EV-MEM-039`（分配器基准，断言锚/留痕分层） |

## 二、人审三问裁决落地

| 裁决 | 落地内容 |
|---|---|
| **1 · 断言锚分层确认** | `actual` 锚**不扩大**（仍 4 行：`iters_per_round`/`rounds`/`block_bytes`/`sink_nonzero`）；新增卡内**「完整原始输出」节**：Windows 三资源 × 7 轮逐轮样本（771200…/154700…/253900…）+ 中位数/min/max + 比值，Linux 侧中位数与比值；**Linux 逐轮样本当时未采集，已如实标注"未采集、不编造"**（铁律 7）。完整数据同时落盘 `Examples/atoms/_atom_allocator_bench.out` |
| **2 · 误解编号处理** | `MIS-MEM-029` 由内容类**改写为方法论类**（触发词改为性能/基准/benchmark/平台相关/未标版本/控制变量）；三条反例：① 双平台排序相反实测；② 初版对照组三变量同变被红队拆掉；③ 顺序效应伪装成策略优势（global 首轮 771200 vs 后续 47–49 万）。`MIS-MEM-023` 未动 |
| **3 · libc++ 列处理** | matrix 如实改为「libc++-18 / WSL g++-14 驱动 / **现场复跑，待 CI 回填**」；`EV-MEM-038` 新增**「待办」节**：CI Cross-check 步补 Clang + libc++ `::notice::` 回填（仿 B/C 样板先例）；MSVC 列保持**未实测**、不写数字 |

## 三、门禁数据（原子化后复跑）

| 项 | 期望 | 实测 |
|---|---|---|
| `atom_evidence_replay` | 42/42 | ✅ **confirm=42 / refute=0**（40 旧 + 本批 2） |
| `gate_engine --check` | block=0（33 规则） | ✅ **block=0** · warn=8（`EV-SERVES-EXIST` ×2 随原子化自动清零） |
| `poison_drill` | 8/8 | ✅ 8/8 |
| `pytest tests/ -q` | 全过 | ✅ 88 passed |
| `golden_lock` | 恶化 0 | ✅ `--accept` 留痕后 sync：`{block:0, warn:10, evidence:42, verified_atoms:20, replay:42}` |
| WSL `ci_local_precheck` | 31 步 | ✅ 31 步 · 失败 0 |

## 四、提交与推送（工具/内容分离）

| 提交 | 内容 | 规模 |
|---|---|---|
| `9362130` | **提交 A**：S6 工具增强（`gate_engine.py` 29→33 规则、`poison_drill.py` P4–P7、`tests/test_s1_s6.py` 4 例、`docs/kernel/S1_S6_controls.md`、`docs/S6_tool_debt.md`） | 5 文件 +375/-3 |
| `cf59a2b` | **提交 B**：PERF-003 原子化（原子 + 2 证据卡 + 2 误解 + 3 夹具/工件 + 质检报告） | 11 文件 |
| `1dc29b9` | 黄金锁基线同步（`tools/golden_state.json`） | 1 文件 |

- 推送：`3c66c8a..1dc29b9  master -> master`（**pre-push 快校验全过**）
- 提交范围**不含** `References/`（铁律 3）；未提交任何非本批产物

## 五、P4–P7 盲区登记（本批只登记不改）

`docs/S6_tool_debt.md` 已登记四条规则在 PERF-003 上 **4/4 零命中**的原因与改进方向，
其中红队点名**`EV-MATRIX-UNBACKED` 豁免条件过宽**（"留痕"关键词自证式豁免）——
改进方向：豁免必须伴随**可核对锚**（`.out` 路径 / CI run 号 / `::notice::` 注解 / 现场复跑命令行），
仅有"外部留痕"四个字不算。四条改进均登记为下一批工具债，附带回归要求（42 卡全量重跑 + 新增 P8+ 毒样例）。

## 六、G5 MEM 域现状

- **verified 原子：20 颗**（G4 样板 3 + 第一批 8 + 第二批 4 + RVREF-001 + 第三批 3 + **PERF-003**）
- 证据卡 **42 张**、误解库 **29 条**、replay **42/42**
- 下一批方向待拍板：A 继续 MEM（ALLOC-002/LEAK-002/PERF-004）· B 转 CONC 域 · C 转 UB 域第二批
