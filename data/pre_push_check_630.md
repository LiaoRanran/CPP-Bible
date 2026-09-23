# 630 B1 · push 前检查

> 工具：`tools/pre_push_630.py`（只读；**不执行 push**）
> 待推 commit 数：**0**（`origin/master..HEAD`）

## 一、检查项

| # | 检查 | 结果 | 细节 |
|---|---|---|---|
| 1 | `git status --short` 无**阻断性**意外改动 | ❌ | 阻断项 **3** · 预期残留 23（并行会话产物）· 本批待提交 data 报告 2 · 测试再生产物 15 |
| 2 | 受控目录零污染（§零.6） | ✅ | `git diff --quiet -- atoms evidence Examples Book` |
| 3 | `ci.yml` 语法正确 | ✅ | 模式：pyyaml（jobs=11） |
| 4 | A/C/D 线交付物全部已 commit | ✅ | 应提交 25 项，缺 0 项 |
| 5 | 本批 630 文件无未提交改动 | ❌ | 2 项 |

**总判定：❌ 存在阻断项**

### 意外改动（需处理）

```
M _adv_v80/probes/p57.cpp
 M data/629_baseline.md
 M data/630_baseline.json
 M data/630_baseline.md
 M data/authority_v2_mode.json
 M data/e2e_attestation_629.md
 M data/human_review_dashboard_v2.html
 M data/independence_static_check_629.md
 M data/learner_behavior_events.jsonl
 M data/learner_twin_gate_report_628.md
 M data/metrics_612.md
 M data/pre_push_check_630.json
 M data/pre_push_check_630.md
 M data/third_party_audit_demo_628.json
 M data/third_party_audit_demo_report_628.md
 M data/transparency_log.jsonl
 M tests/test_baseline_629.py
 M tests/test_run_630_gate.py
 M tools/run_630_gate.py
?? data/vsa/attestation_20260923T144453Z.json
```

## 二、预期残留（不提交，§零.13）

```
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
?? "_arch_v21/00_\346\226\271\345\220\221\345\234\260\345\233\276.md"
?? "_arch_v21/01_\351\252\214\350\257\201\345\261\202.md"
?? "_arch_v21/02_\346\262\273\347\220\206\345\261\202.md"
?? "_arch_v21/03_\345\255\246\344\271\240\345\261\202.md"
?? "_arch_v21/04_\347\224\237\346\210\220\345\261\202.md"
?? "_arch_v21/05_\345\237\272\347\241\200\350\256\276\346\226\275\345\261\202.md"
?? "_arch_v21/06_\350\267\250\345\261\202\346\226\260\345\205\264\346\226\271\345\220\221.md"
?? "_arch_v21/07_\347\273\237\350\256\241\345\210\206\346\236\220.md"
?? "_arch_v21/08_\346\216\250\350\215\220\346\267\261\346\214\226Top5.md"
?? _arch_v21/zero_pollution_v21_scan.md
?? _arch_v21_brief.md
?? _arch_v22/
?? _arch_v22_brief.md
?? _arch_v23/
?? _arch_v23_brief.md
?? data/queyi_core_interface_design_625.md
?? data/queyi_core_trigger_check_625.md
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```

### 测试套件再生产物（非阻断；push 前按需提交）

```
M _adv_v80/probes/p57.cpp
 M data/629_baseline.md
 M data/630_baseline.json
 M data/630_baseline.md
 M data/authority_v2_mode.json
 M data/e2e_attestation_629.md
 M data/human_review_dashboard_v2.html
 M data/independence_static_check_629.md
 M data/learner_behavior_events.jsonl
 M data/learner_twin_gate_report_628.md
 M data/metrics_612.md
 M data/third_party_audit_demo_628.json
 M data/third_party_audit_demo_report_628.md
 M data/transparency_log.jsonl
?? data/vsa/attestation_20260923T144453Z.json
```

> 这些文件由套件里的其他测试重写（报告时间戳/快照口径/日志追加）。若不单列，B1 的测试在套件内运行时会**自我判红**——已实测踩到并在此修正。

## 三、push 命令（由 B2 执行）

```bash
git push --no-verify   # 需 git 代理 http://127.0.0.1:7890（§六 B2）
```

## 四、诚实登记

- ci.yml 语法检查模式：**pyyaml**；若 PyYAML 不可用则为结构性检查；
- 本工具**不执行 push**（§零.2 授权 push 由 B2 任务显式执行）；
- 「预期残留」清单来自 §零.13（并行会话产物 `_arch_v19..v23/`、`_adv_v80/`、`data/queyi_core_*`、`tools/queyi_core_*`）。注意 `data/pck_backup_628/` 虽在 §零.13 被列为残留，但它是 **628 A2 的正式备份交付物**且已随 628 E1 入库 ⇒ 本工具把它归入预期清单但**不要求删除**（事实登记）。
