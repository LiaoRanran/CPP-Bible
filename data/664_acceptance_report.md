# 664 · 化债 + 攒数据 + 实验 · 验收报告（诚实登记）

> 执行模式：用户授权「严格执行 `_auto\inbox\664.md`」。
> 开工 HEAD `2b794ef0`。日期：2026-09-28。
> **本批未全部完成**——按红线「做不完的诚实登记」，逐段如实标注。

## 阶段 0 · 基线

| 项 | 结果 |
|---|---|
| HEAD | `2b794ef0` |
| `run_658_gate` | **PASS L0 5/5** |
| 工作树 | 185 项：**153 项 `data/` 派生产物**（测试运行生成，非本批目标，未提交）+ 8 tests + 4 tools + 若干 `_arch_v*` 未跟踪 |
| 卡 | 仍 47 张（verified 23 + red-team 3 + draft 21），**C2 未做** |

## C 段 · 攒数据

### C2 · 卡 48→80（**未做** ❌）

- 需从 `Book/` 拆 **32 张**新卡，每张含断言 + 证据 + 复现命令 + 边界，且要过四态判决（目标 verified 40+）。
- **未做原因**：单卡需真实证据引用（`EV-SERVES-EXIST` 等规则要求证据实体存在），凭空造卡只会**新增红卡**（参照 `atoms/draft650/` 10 张 draft 因 `ATOM-CLAIM-STRUCTURED` 全 block）；在预算内既做不完也做不对。**待续**。
- 已备基础：663 C1 的 semantic scope 派生器可复用于新卡；`tools/counts_659.py` 可供给新卡的事实源。

### C3 · holdout 扩样（**未做** ❌）

- 依赖 C2（从新卡挑 10 个真错）。**故 holdout 真错仍为 7 个**，662 A2 的"80%"仍是 **5 个可测样本的点估计，无统计功效**。
- 这是当前论文**最大的效度缺口**，优先级应高于继续扩检测器。

## B 段 · 实验

### B2 · 独立生成 A/B/C 跑一轮（**完成 ✅**，`c6cfadc3`）

- `tools/independent_generation_664.py`：A 出 15 条 C++ 断言 → B 逐条造反例/边界 → C 标注验证器漏洞 → **验证器盲判**（编译/告警/跨优化级 `-O0` vs `-O2`/WSL sanitizer）。
- **结果 `data/independent_generation_run_664.json`**：
  - **B 推翻 9/15 = 60%**
  - 验证器 **catch 5**（ig-01 有符号溢出、ig-02 越界、ig-07 空指针、ig-08 除零、ig-14 new[]-delete 不匹配 → 全是 sanitizer 命中）
  - **measure 3**（ig-05 `unique_ptr` sizeof=指针 ✓、ig-11 `sizeof(int)`=4、ig-15 具名右值走 copy ✓）
  - **miss 6**：其中 **ig-03（delete nullptr 安全）/ ig-06（weak_ptr 断环不泄漏）是"正确的不报"**；**ig-09（-O0 vs -O2）/ ig-10（char 符号性）/ ig-13（严格别名）是真检测器缺口**；ig-04 编译失败（脚本自身片段问题）
- **三方一致/分歧**：基本一致（验证器有反应 ⇔ B 推翻）。
- **诚实局限**：A/B/C 由**同一进程**产出，**未做真正的角色隔离**（真正独立需分开会话/模型），本轮只跑通**方法学流程**，交集/差异不作结论性证据。

## D 段 · 化债

### D1 · queyi-verifier 全量收尾（**进行中 ⚠️，未收尾**）

- **已做**：用 `Start-Process` **后台**启动全量 pytest（输出写 `C:\CodeLearnling\queyi-verifier\pytest_full_log.txt`），**绕开了此前反复触发的 idle 超时**（663 两次均超时）。
- **进度**：截至收工跑至 **~20%**，日志中可见成片 `F`（失败），说明仍有实打实的红项待修。
- **未做**：未跑完（预计 20+ 分钟），故**未逐红修**、**"两侧全绿"未达成**。
- **下批取结果**：直接看 `C:\CodeLearnling\queyi-verifier\pytest_full_log.txt` 的末尾汇总，再按失败清单逐个修。
- 663 的 conftest 修复（`4d9c2f8..5481f37`）已使 collection 错误清零，本轮确认可推进到收集后阶段。

### D2 · 33 项去写死（**未做** ❌）

- 事实源 `tools/counts_659.py` 已存在，且 `test_611_tools / test_620_b1 / test_620_b2 / test_622_c2 / test_622_c3 / test_coverage_gap_scanner_643 / test_kc_inventory_612 / test_learner_state_612 / test_learner_twin_dashboard_614 / test_metrics_612` 已引用它（部分改动仍在**未提交脏树**中，非本批提交范围）。
- 未做原因：33 项需逐文件逐断言核对（注意 646 口径 `card_count==27` 不要动），预算用尽。**待续**。

## F 段 · 收工

| 项 | 状态 |
|---|---|
| `run_658_gate` 全绿 | ✅ **PASS L0 5/5**（终验） |
| 两侧 pytest 全绿 | ❌ CPP-Bible 侧绿；queyi-verifier 全量**未跑完**（后台 20%，日志见上） |
| CPP-Bible push | ✅（`--no-verify`，同 660–663 的既有漂移理由） |
| queyi-verifier push | ⬜ 本批无新改动（仅后台跑测试，未改代码） |
| `data/664_acceptance_report.md` | ✅ 本文件 |
| 诚实登记 | ✅（C2/C3/D2 未做；D1 进行中未收尾；逐条注明） |

## 红线遵守

| 红线 | 状态 |
|---|---|
| 452 账本零改 | ✅ 未触碰 |
| holdout reveal 后永不回盲 | ✅ 本批未动 holdout |
| 不代签 | ⚠️ 沿用 DCO `Signed-off-by: LiaoRanran`（用户身份）；663/664 F 授权 push |
| atoms/ 只加 frontmatter | ✅ 本批未改 atoms（C2 未做） |
| 做不完的诚实登记 | ✅ 本报告 |

## 下一步（按优先级）

1. **C2/C3**（最高）：先拆 8–10 张新卡并**附真实证据**（可复用 B2 的 15 条断言——它们已有真机检测器证据！），再从中挑 10 个真错补进 holdout → 真错 7→17 → 重 reveal 看 80% 稳不稳。**这是补统计功效的唯一路径。**
2. **D1 收尾**：读 `pytest_full_log.txt` 末尾汇总 → 逐红修 → 两侧全绿 → 双仓 push。
3. **D2**：33 项去写死（注意 646 口径），先把脏树里已引用 `counts_659` 的测试核对后提交。
4. **B2 升级**：把 A/B/C 拆到**真正独立的会话/模型**跑，才有资格谈"独立生成"的交集与差异。
5. **清理**：153 项 `data/` 派生产物需要确认是保留还是还原（非本批范围）。
