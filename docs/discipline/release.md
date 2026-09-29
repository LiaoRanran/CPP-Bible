# C6 · 版本与发布规范（666 批）

> **一句话**：发布不是"打标签"，而是**声明这批证据覆盖到什么**。
> 尤其当**口径变了**（分母、档位、样本集），release notes 必须把**旧数字作废**写清楚 ——
> 否则后人会把两组不可比的数字当成"进步"。

## 1. tag 规范

```
v<论文主版本>.<批次号>       例：v0.4.666
v<论文主版本>.<批次号>-rc<N>  例：v0.4.666-rc1
```

- 主版本跟论文（`research/paper_v0.4.md` ⇒ `v0.4`），批次号跟 `_auto/inbox/<批次>.md`。
- **不打** `latest`/`stable` 之类会漂的标签（无法复算）。

## 2. CHANGELOG 条目模板（追加到根 `CHANGELOG.md` 顶部）

```markdown
## [666] 2026-09-29 · 究极收尾大包

### 口径变更（**旧数字作废**）
- 检出率口径：单 `-O1` → **双档 `-O0`/`-O2`**。旧值 **66.7% 作废**，新值 **81.2%**（同批样本）。
- 反事实算子新增"断言自报机器/平台实测"判据：旧 F1 **0 作废**，新 F1 **1.0（上界）**。

### 修复
- 主仓/拆仓测试套件：fast 全绿；slow 见 §验收。
- 拆仓 wrapper 的静态分析（PEP 562）与三处诊断工具的"追 canonical"。

### 证据
- `data/holdout_reveal_3_665.json`、`data/645_compiler_probe_report.json`、
  `data/counterfactual_cases_665.json`、`data/666_acceptance_report.md`。

### 红线
- `data/646_authority_rule_annotation.jsonl` **452 事件零改**。
```

## 3. release notes 模板

```markdown
# <批次> 发布说明

1. **这批改了什么**（一句话）
2. **口径有没有变**（有 ⇒ 列出旧值/新值/为什么不可比）
3. **证据在哪**（可复算命令 + 落盘文件）
4. **哪些没做**（诚实登记，不许省）
5. **红线核对**（452 账本 / 受控目录 / 供应链重钉）
6. **人签**（谁看过；AI 参与见 `research/AI_USAGE_LOG.md`）
```

## 4. 发布前检查清单（逐条必须过）

| # | 检查 | 命令 | 不过怎么办 |
|---|---|---|---|
| 1 | 信任根 | `python tools/tool_integrity.py --check` | 重钉 `--update` **并说明为什么变更** |
| 2 | 元状态对账 | `python tools/status_reconciler_658.py --check` | 先修口径差，别改对账器 |
| 3 | 主仓 fast | `pytest -m "not slow" -n auto` | 全绿才发 |
| 4 | 主仓 slow | `pytest -m slow -n0` | 红必须逐条登记（不许"默默跳过"） |
| 5 | 拆仓 fast/slow | 同 3/4（在 `queyi-verifier`） | 同上 |
| 6 | 静态 | `ruff check tools/ tests/` + `mypy tools/` | 全绿 |
| 7 | 452 账本 | `git status -- data/646_authority_rule_annotation.jsonl` | 有改动 ⇒ **停发** |
| 8 | 受控目录 | `git status -- atoms evidence Examples Book` | 有改动 ⇒ 重钉 Merkle + 写占位/归档说明 |
| 9 | 供应链 | `data/supply_chain/merkle_roots.json` 已重钉；`.ots` 状态与占位登记一致 | 见 `docs/discipline/provenance.md` §5 |
| 10 | AI 日志 | `research/AI_USAGE_LOG.md` 有本批条目 | 补 |

## 5. 口径变更的处理流程（本批新增，最易被忽视）

1. **判定**：这是"同口径的新测量"还是"换了口径"？
   - 同口径 ⇒ 更新数字即可。
   - 换口径 ⇒ 走 2–4。
2. **作废旧值**：在论文、报告、CHANGELOG 里标明旧值与作废原因（**不许静默替换**）。
3. **给可比性说明**：新旧数字能否同图？不能就分开列（本批 66.7% / 81.2% 即分开）。
4. **在工具里留痕**：口径写在代码常量/docstring（如 `rv661.detect` 的档位循环注释），
   不写在"口头约定"里。

## 6. 回滚

- 数据类：`git revert <commit>`；受控目录回滚后**必须重钉 Merkle** 并重跑 `tool_integrity --update`。
- 口径类：**不许**用 revert 掩盖（旧值已被引用）；改为"新批次再改一次并写清"。
- 规则类：见 C7 §回滚。
