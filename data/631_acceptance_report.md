# 631 批次验收报告 · CI 根治 × 自身免疫率修复执行 × 污染根因 × coverage 补全 × 他验信任根 × Core 剥离

> 批次类型：巨大建设批（17 任务，全部完成）
> 前置：630 已收工并通过验收（PASS），HEAD=`53582fe2`，CI 四 job 全绿仅 pytest 红。
> 本批 HEAD=`29888f8f`（**未 push**，§零.2）。收工门禁 `run_631_gate.py` PASS。

## 一、六线交付一览

| 线 | 任务 | 交付物 | 结果 |
|---|---|---|---|
| 0 | 任务0 | `tools/baseline_631.py` + `data/631_baseline.md/json` | CI pytest 红项清单采集 ✓ |
| A | A1-A4 | `ci_pytest_triage_631.py` + 跨批脆弱 6 项修复 + 工具自检过期 3 项修复 + `ci_pytest_fix_*` 报告 + `ci_pytest_final_631.md` | 14→5 项：跨批脆弱 6 + 工具自检过期 3 清零，剩 5 = 环境依赖 4 + UTF-16 存疑 1，**无新增失败** |
| B | B1-B3 | `autoimmune_auto_fill_631.py`（auto 42 条落地）+ `autoimmune_human_queue_631.py`（human 90 清单）+ `autoimmune_post_fix_631.md` | auto 42 条 liveness 填充生效（23 卡 42 处）；复算 warn 134→92，但**率仍 100% 未改善** |
| C | C1-C2 | `pollution_bisect_631.py` + `pollution_prevention_design_631.md` | 逐组实跑**未复现**污染，未定位到函数；根因假设 + 三层防护设计交人 |
| D | D1-D2 | `coverage_gap_631.py` + `coverage_probe_l1_2_631.py` + `coverage_probe_l8_4_631.py` + `coverage_probe_result_631.md` | 19 向量→P0 2 / P1 16 / P2 1；建 2 个 P0 探针，coverage 口径 45.7%→51.4% |
| E | E1-E2 | `trust_root_upgrade_631.py` + `data/vsa/public_key_631.json` + `sample_signed_631.json` + `third_party_verify_guide_631.md` | 三路径评估推荐 C；导出 RSA-2048 公钥（私钥不落盘）+ 第三方验证指南 |
| F | F1 | `queyi_core_interface_v02_631.py` + `data/queyi_core_interface_v02_631.md/json` | 5 接口 25 方法只定义不实现；雷1 触发标准 3/5 |
| G | G1 | `run_631_gate.py` + 本报告 + `status.json` + `outbox/631.md` | 收工门禁 PASS |

## 二、关键实测数字（诚实）

- **CI pytest 红**：630 识别 14 项（跨批脆弱 6 + 工具自检过期 2 + UTF-16 1 + 环境依赖 5）。本批修复后 **14→5**，剩余 5 = 环境依赖 4 + UTF-16 存疑 1；**无新增失败**。
  - 注意：**全局** `pytest -m not slow` 仍有约 30 项失败，来自 625/627/629/591/601/611/613… 等**其他批次**的跨批脆弱测试（与 631 无关的存量债）。依 §零.11 不在本批范围，交对应批次回修补齐。
- **自身免疫率**：填充前 132 条 warn（auto 42 / human 90）→ 填充后 **warn 92 条**（auto 42 条 `OBSERVATION-LIVENESS` 全清零），但被 warn 的干净卡仍 **23/23** ⇒ **率仍 100%，未改善**（与 630 A3 严格情景预测完全一致）。
- **污染**：两次全量 + 4 组逐组实跑，受控目录 `atoms` 均**零污染**（`git diff --quiet` exit 0）；污染**未能复现**，故未定位到具体测试函数。
- **coverage**：630 工具口径 16/35 = 45.7%；本批补 2 个 P0 探针后，同分母扩展口径 **18/35 = 51.4%**（+5.7pp）。余 4 个无探针向量交人。
- **他验信任根**：RSA-2048 真非对称签名已具备（629 C1）；本批完成公钥导出 + 第三方验证指南 + 三路径升级评估（推荐 C）。算法独立 ≠ 信任根独立仍成立（C 路径未实施）。
- **受控目录零污染**：`git diff --quiet -- atoms evidence Examples Book` 全批保持 exit 0。
- **测试**：本批新增 10 个工具各带 `--check` + ≥5 例单测，共约 **60+ 例单测全绿**（`run_631_gate` 仅跑本批 10 测试文件，全部通过）。

## 三、§十二 偏差与诚实登记

| # | 偏差 | 处理 |
|---|---|---|
| 1 | **B1 自身免疫率未改善**（仍 100%） | 如实记录；warn 条数 134→92 但被 warn 卡不变 ⇒ 率不变。与 630 严格情景预测一致。 |
| 2 | **C1 污染未定位到具体测试函数** | 逐组实跑未复现；交付最小范围（22 个静态候选）+ 根因假设（沙箱 apply 后 restore 前失败，有 3 条证据，未证实）；防护设计交人（C2）。 |
| 3 | **D2 coverage 提升有限**（+5.7pp，余 4 个无探针向量） | 只补 2 个 P0；余 L2.3/L4.2/L4.4/L7.5（难度中/高）交人。630 工具口径仍 45.7%，本批仅扩展标注、未改该工具（§零.11 越界）。 |
| 4 | **A 线剩 5 项 pytest 红**（环境依赖 4 + UTF-16 1） | 不修复，标注交人；非 631 引入，系其他批次跨批脆弱存量债。 |
| 5 | **§零.13 与 F1 提交冲突** | §零.13 列 `tools/queyi_core_*` / `data/queyi_core_*` 为"工作区残留不要提交"，但其模式也匹配本批 F1 交付物 `queyi_core_interface_v02_631.*`。**按 F1（§十 明确要求创建并提交）提交了 v02_631 文件，未提交 625 残留**（`queyi_core_interface_design_625.*`、`queyi_core_trigger_check_625.*`）。特此登记偏差。 |
| 6 | **630 已有工具未改**（§零.11） | `coverage_metric_630.py` 口径仍是 16/35=45.7%；本批 51.4% 为同分母扩展标注。A 线 4 项修复均只改**测试断言**，未改被测工具生产逻辑。 |
| 7 | **未 push**（§零.2） | `status.json` next_batch=632，留待 632 或用户授权。 |
| 8 | **E1 路径 C 未实施** | 仅完成评估 + 公钥导出 + 验证指南；信任根真正外移（OTS/Sigstore）需后续批次。 |

## 四、交人项预告（§十三，延续）

1. human 90 条字段填充（B2 清单，signed_by 机器永不代签）；
2. C2 污染防护机制是否实施（推荐先做 L1 会话级受控目录快照守卫）；
3. E1 信任根升级路径选择（评估推荐 C，但 A 与 C 并存：A 供离线验证、C 供外部锚）；
4. F1 Core 接口 v0.2 是否进入实施（抽象已就绪，待各工具适配）；
5. D2 余 4 个无探针向量（L2.3 证据漂移 / L4.2 规则绕过 / L4.4 判据冲突 / L7.5 时序）；
6. A 线剩 5 项 pytest 红（其他批次跨批脆弱存量债）；
7. 629 交人项剩余（V2 flag / Blind Review / PCK / 镜像边 / 学习者开门）。

## 五、硬边界遵守自检

- ✅ 未跑监工四门禁 `--check` 全量（仅新工具 `--check` + 本批测试）
- ✅ 未 push、未代签人审、未 golden accept
- ✅ 新工具均有 `--check` + ≥5 例单测
- ✅ 一任务一 commit（共 17 commit）
- ✅ 受控目录零污染
- ✅ 纯标准库（无 pip install）
- ✅ 未删改任何 JSONL 账本（append-only）
- ✅ 未动两条 CRLF 假脏文件、未提交 §零.13 所列残留
- ✅ 630/629/628 等已有工具生产逻辑未改（仅改测试断言，授权范围内）
