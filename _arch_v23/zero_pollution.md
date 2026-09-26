# zero_pollution.md — v23 深度调研零污染自证

> **自证范围**：2026-09-23 执行 `_arch_v23_brief.md`（攻击面×自身免疫率×Horizon 三靶深调）的全部写操作
> **自证时间**：2026-09-23 16:22（本机时间）
> **自证者**：MainAgent（Trae 会话）
> **目录状态**：`_arch_v23/` 开工前不存在（`Test-Path` 返回 NOT EXIST），本目录为本次调研新建，无命名冲突。

---

## 一、开工基线（2026-09-23 调研开始前 `git status --short`）

```text
 M _adv_v80/probes/p57.cpp
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
?? _arch_v21/（10 个 v21 调研文件）
?? _arch_v21_brief.md
?? _arch_v22/（8 个 v22 调研文件）
?? _arch_v22_brief.md
?? _arch_v23_brief.md
?? data/queyi_core_interface_design_625.md
?? data/queyi_core_trigger_check_625.md
?? tools/baseline_629.py
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```

（另有若干批次 626/628 的 data 未跟踪条目在会话窗口前后有进出；以本会话开工瞬间实测为准。）

## 二、本次写操作清单（共 6 个新文件，全部在 `_arch_v23/` 内）

| 文件 | 大小 | 内容 | 写入时间（本机） |
|---|---|---|---|
| 01_验证器攻击面分类学.md | 16,603 B | 靶 A：AISI/METR/spec gaming/ATLAS 三 taxonomy、V1-V7、L1-L8 对照与横切轴建议 | 16:09:03 |
| 02_自身免疫率度量框架.md | 15,300 B | 靶 B：免疫/flaky/SOC/支付/假设检验五域阈值与 B5 阈值建议 | 16:13:14 |
| 03_Verification_Horizon深化.md | 14,100 B | 靶 C：D1-D4/R1-R3、METR 双分位法、状态爆炸、CVSS/ATT&CK、C5 升级建议 | 16:17:19 |
| 04_跨靶位综合.md | 11,232 B | 三交叉点、对 629 A/B/D 三线建议、对 v21/v22 更新 | 16:19:47 |
| 00_总览.md | 6,531 B | 三靶核心结论、净新增（coverage）、数字速查、置信度 | 16:20:54 |
| zero_pollution.md | 本文件 | 零污染自证 | 16:22 |

会话级自证（工具调用事实）：
- 本会话全部 **Write 调用共 6 次，目标路径无一例外均为 `_arch_v23/`**；
- **Shell 命令全部只读**：`git status --short`、`Test-Path`、`Get-ChildItem`、`Get-Item`（取时间戳），无任何写盘/管道写文件操作；
- 未运行 git add/commit/push，未运行 Python/构建/测试/门禁；
- 网络操作为 WebSearch（约 14 次）与 WebFetch（2 次），不接触仓库；
- 未修改、删除、移动 `_arch_v23/` 外任何文件。

## 三、收工差异与归因（重要：存在并行会话产物）

收工 `git status --short` 相对开工基线，除 `?? _arch_v23/` 外，另有**非本会话产生**的差异，全部归因于**同期并行的批次 628/629 建设会话**（与 v21 调研日 628 并行会话同型）：

**新增已跟踪修改（10 个，开工基线中无 M 标记）**：
```
 M data/authority_v2_mode.json
 M data/human_review_dashboard_v2.html
 M data/learner_behavior_events.jsonl
 M data/learner_twin_gate_report_628.md
 M data/metrics_612.md
 M data/snapshot_integrity_626.json
 M data/snapshot_integrity_report_626.md
 M data/third_party_audit_demo_628.json
 M data/third_party_audit_demo_report_628.md
 M data/transparency_log.jsonl
```

**新增未跟踪文件（1 个）**：
```
?? data/vsa/attestation_20260923T081548Z.json
```

**归因证据链**：
1. **工具日志**：本会话无任何指向 data/ 的写操作（见第二节）；
2. **内容归属**：`data/vsa/attestation_*.json` 与 `data/transparency_log.jsonl` 是批次 628 他验线（VSA 凭证/透明日志）的运行时产物；`authority_v2_mode.json`、`human_review_dashboard_v2.html`、`learner_*`、`metrics_612.md` 属 628/629 人审/指标线；`tools/baseline_629.py` 与 `_arch_v23_brief.md` §五所述"629 正在落地"互为印证；
3. **时间戳（本机）**：并行会话在本调研窗口内持续活动——
   - `learner_behavior_events.jsonl` LastWrite 16:06:31、`metrics_612.md` 16:07:05、`human_review_dashboard_v2.html` 16:11:31、`transparency_log.jsonl` 16:15:48（VSA attestation 同时刻 16:15:48 生成）、`authority_v2_mode.json` 16:21:40；
   - 本会话文件写入区间为 16:09:03–16:20:54；
   - **`authority_v2_mode.json` 的最后修改 16:21:40 晚于本会话最后一次写入（16:20:54）**，直接证明收工瞬间另一会话仍在活动；
4. **模式先例**：与 2026-09-23 上午 v21 调研收工时 628 并行会话产生 `data/pck_backup_628/`、`tools/vsa_attestation_628.py`、transparency 三件的情形完全同型（见 `_arch_v21/zero_pollution_v21_scan.md` 第三节）。

## 四、对照 brief §零.2 的诚实声明

brief 要求"收工后比对，唯一差异必须是 `?? _arch_v23/`"。**本会话自身严格满足该约束**（本会话造成的差异恰好只有 `_arch_v23/` 6 个新文件）；但工作树在收工时客观上还存在并行 628/629 会话造成的 11 条差异。按既有零污染纪律（v21 先例），此处逐条归因、明示非本会话所为、不触碰这些文件，而不是将并行产物计入或隐去。

## 五、独立验证方法

```powershell
# 1. 本次产出全部在 _arch_v23/（应恰为 6 个文件）
Get-ChildItem _arch_v23

# 2. v23 之外的已跟踪修改均为并行批次（无 _arch_v23 路径）
git status --porcelain | Select-String -NotMatch "_arch_v2"

# 3. 本会话未触碰受控目录内容（_arch_v23 之外无本会话 16:09-16:21 的写入；
#    data/ 下该时段写入已归因为 628/629 会话）
```

---

**自证完成**：2026-09-23 16:22
**调研性质复核**：三靶深调按 A1-A5/B1-B5/C1-C5 全问题回答；所有外部事实三级标注；拿不到一手者（AISI 模型名单、MALT 细标签、R2 原文、部分二手数字）标【待验证】且未用于结论；未给工程实现方案；中文撰写；唯一新增判断（coverage 第三指标、双横切轴、双分位与先验阈值）均标【推断】与置信度。
