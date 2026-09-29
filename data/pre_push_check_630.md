# 630 B1 · push 前检查

> 工具：`tools/pre_push_630.py`（只读；**不执行 push**）
> 待推 commit 数：**None**（`origin/master..HEAD`）

## 一、检查项

| # | 检查 | 结果 | 细节 |
|---|---|---|---|
| 1 | `git status --short` 无**阻断性**意外改动 | ❌ | 阻断项 **2** · 预期残留 1（并行会话产物）· 本批待提交 data 报告 0 · 测试再生产物 0 |
| 2 | 受控目录零污染（§零.6） | ✅ | `git diff --quiet -- atoms evidence Examples Book` |
| 3 | `ci.yml` 语法正确 | ❌ | 模式：missing（ci.yml 不存在） |
| 4 | A/C/D 线交付物全部已 commit | ❌ | 应提交 25 项，缺 9 项 |
| 5 | 本批 630 文件无未提交改动 | ✅ | 0 项 |

**总判定：❌ 存在阻断项**

### 意外改动（需处理）

```
?? conftest.py
?? uv.lock
```

### 缺失交付物

- `data/630_baseline.md`
- `data/autoimmune_diagnose_630.md`
- `data/autoimmune_fix_proposal_630.md`
- `data/autoimmune_recalc_630.md`
- `data/coverage_metric_630.md`
- `data/attack_surface_axes_630.md`
- `data/autoimmune_threshold_630.md`
- `data/stale_test_triage_630.md`
- `data/stale_test_fix_630.md`

## 二、预期残留（不提交，§零.13）

```
?? _adv_v80/
```

### 测试套件再生产物（非阻断；push 前按需提交）

```
（无）
```

> 这些文件由套件里的其他测试重写（报告时间戳/快照口径/日志追加）。若不单列，B1 的测试在套件内运行时会**自我判红**——已实测踩到并在此修正。

## 三、push 命令（由 B2 执行）

```bash
git push --no-verify   # 需 git 代理 http://127.0.0.1:7890（§六 B2）
```

## 四、诚实登记

- ci.yml 语法检查模式：**missing**；若 PyYAML 不可用则为结构性检查；
- 本工具**不执行 push**（§零.2 授权 push 由 B2 任务显式执行）；
- 「预期残留」清单来自 §零.13（并行会话产物 `_arch_v19..v23/`、`_adv_v80/`、`data/queyi_core_*`、`tools/queyi_core_*`）。注意 `data/pck_backup_628/` 虽在 §零.13 被列为残留，但它是 **628 A2 的正式备份交付物**且已随 628 E1 入库 ⇒ 本工具把它归入预期清单但**不要求删除**（事实登记）。
