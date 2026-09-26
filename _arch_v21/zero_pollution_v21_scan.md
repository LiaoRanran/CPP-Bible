# zero_pollution_v21_scan.md — v21 宽泛调研零污染自证

> **自证范围**：2026-09-23 执行 `_arch_v21_brief.md`（前期宽泛方向调研）的全部写操作
> **自证时间**：2026-09-23
> **自证者**：MainAgent（Trae 会话）
> **文件名说明**：brief 第三节要求文件名为 `zero_pollution.md`，但该文件名已被本目录 2026-09-21 外部评审存档工作流占用（git 已跟踪）。经用户授权（2026-09-23，AskUserQuestion 裁决"改用新文件名"），本次自证写入本文件，旧 `zero_pollution.md` 保持不动。

---

## 一、开工基线（2026-09-23 调研开始前，`git status --short` 原文）

```text
 M _adv_v80/probes/p57.cpp
 M data/adversarial_loop_round3_623.md
 M data/authority_v2_mode.json
 M data/metrics_612.md
 M tools/authority_v2_switch_627.py
 M tools/pre_push_checklist_627.py
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
?? _arch_v21_brief.md
?? data/.622_apply.lock
?? data/queyi_core_interface_design_625.md
?? data/queyi_core_trigger_check_625.md
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```

说明：`_arch_v21/` 目录下 5 个旧文件（00_总览/01_第一波/02_第二波/03_产品经理内化/zero_pollution，均 2026-09-21）已被 git 跟踪，基线中不出现。

## 二、本次写操作清单（共 10 个新文件，全部在 `_arch_v21/` 内）

| 文件 | 内容 |
|---|---|
| 00_方向地图.md | 总览：22 方向清单表+统计图描述+Top5+不推荐+对 v20 更新 |
| 01_验证层.md | D1-D6 六个验证方向明细 |
| 02_治理层.md | D7-D11 五个治理方向明细 |
| 03_学习层.md | D12 学习者建模（含"不凑数"诚实声明） |
| 04_生成层.md | D13-D14 APR 闭环/可扩展监督 |
| 05_基础设施层.md | D15-D20 形式化/供应链/复现构建/知识表示/密码学/溯源 |
| 06_跨层新兴方向.md | D21-D22 基准退役/可靠性分位（清单外发现） |
| 07_统计分析.md | 分层/成熟度/相关性/红海蓝海/死路/被忽略方向 |
| 08_推荐深挖Top5.md | 正式 v21 深调选靶建议（不含实现方案） |
| zero_pollution_v21_scan.md | 本文件 |

未覆盖、未删除、未修改 `_arch_v21/` 内 5 个旧文件；未修改仓库其他任何文件。未运行 git add/commit/push，未运行任何 Python/构建/写盘脚本；Shell 命令全部只读（git status/ls-files/check-ignore、Get-ChildItem、Select-String），网络操作仅 WebSearch 检索公开网页。

## 三、收工比对（写完 9 个交付文件后、写本文件前的 `git status --short` 差异）

相对开工基线，差异共两类：

### 3.1 本次产出（全部位于 `_arch_v21/`，符合零污染约束）

```text
?? _arch_v21/00_方向地图.md
?? _arch_v21/01_验证层.md
?? _arch_v21/02_治理层.md
?? _arch_v21/03_学习层.md
?? _arch_v21/04_生成层.md
?? _arch_v21/05_基础设施层.md
?? _arch_v21/06_跨层新兴方向.md
?? _arch_v21/07_统计分析.md
?? _arch_v21/08_推荐深挖Top5.md
```

（写本文件后将再增加一条 `?? _arch_v21/zero_pollution_v21_scan.md`。）

### 3.2 `_arch_v21/` 外的两个新增条目——逐条归因：**非本次会话所为**

```text
?? data/pck_backup_628/
?? tools/vsa_attestation_628.py
```

归因证据链：

1. **时间戳**：`data/pck_backup_628/` 目录创建于 2026-09-23 10:35:36（内部文件保留 2026-09-21 23:19 的旧 LastWriteTime，符合"备份"特征）；`tools/vsa_attestation_628.py` 创建于 10:52:54。二者均出现在开工基线之后、本次调研会话窗口之内。
2. **命名归属**：两者带批次号 `628`，按项目命名惯例属于批次 628 工作流；vsa_attestation（VSA 凭证）属他验三件套建设线，与本次只读调研无任务交集。
3. **会话自证**：本次会话的写盘工具调用恰为 9 次 Write，目标路径全部在 `_arch_v21/`（见第二节清单）；从未向 `data/`、`tools/` 发起任何写操作；`pck_backup_628/` 内含上百个备份文件，非本次会话可能产生。
4. **结论**：两个条目为**并行的批次 628 他验建设会话**在同一仓库并发工作所致（与项目记忆中"顺序接力、避免并行"的约定出现并发，但不影响本次零污染成立）。本次会话未触碰、未移动、未删除它们，仅在此如实登记。

除上述两条外，开工基线中的全部预存条目（6 个已跟踪修改 + _arch_v19/_arch_v20 等其他会话产物）在收工时状态原样未变。

## 四、独立验证方法

```powershell
# 1. 本次新增仅限 _arch_v21/ 下 10 个新文件（含本文件）
git status --porcelain

# 2. 确认 2026-09-21 旧文件零改动（应无输出）
git diff -- _arch_v21/00_总览.md _arch_v21/zero_pollution.md

# 3. 确认受控目录无本次改动（data/ 下仅有的新增为 628 并发会话，归因见 3.2）
git status --porcelain atoms/ evidence/ Book/ Examples/ tools/ tests/
```

---

**自证完成**：2026-09-23
**调研性质复核**：未读论文全文、未写代码、未复现实验、未给工程实现建议；22 方向均按六字段记录；外部事实三级标注齐全（已查证附 URL / 一方称 / 推断 / 待验证）。
