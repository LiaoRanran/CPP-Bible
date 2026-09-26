# 637 任务0 · 开工快照 + 自我进化闭环设计

> 批次：637（自我进化闭环原型——让系统自己开口说话）。
> 时间：2026-09-25。性质：**影子闭环**（系统只看、只想、只说；人拍板）。
> 工具：`tools/self_observer_637.py`（只读）。

---

## 一、开工快照（实测，非抄表）

| 类别 | 指标 | 实测值 | 采集方式 |
|---|---|---|---|
| 规模 | 规则数 | **67** | `gate_engine.RULES` |
| 规模 | 工具数（`tools/*.py`） | **417** | `glob` |
| 规模 | 测试数（`tests/test_*.py`） | **416** | `glob` |
| 规模 | commits 数 | **1848** | `git rev-list --count HEAD` |
| 健康 | pytest 失败数 | 见 `637_observer_report.md`（闭环时实测） | `pytest -m "not slow"` |
| 健康 | ruff 错误数 | 见 `637_observer_report.md` | `ruff check --output-format=json` |
| 健康 | mypy 错误数 | 见 `637_observer_report.md` | `mypy tools/` |
| 知识 | 接地率 | **35.8%**（24/67 已接地） | `grounding_inventory_635.stats()` |
| 知识 | 击败器覆盖率 | **100.0%** | `defeater_ledger_635.stats()` |
| 知识 | taint=true 卡数 | **8** | `defeater_ledger_635.stats()` |
| 治理 | 例外条款条目数 | **227**（7 处来源） | `exception_review_635.stats()["total_entries"]` |
| 治理 | 观察态规则数 | **67 / 67 = 100%** | `verifier_admissibility_635.stats()` |
| 进度 | ahead 数 | **9** | `git rev-list --count origin/master..HEAD` |
| 进度 | 工作区状态行数 | **70** | `git status --short` |

> 与 635 冻结值一致：接地率 35.8、击败器覆盖 100、taint 8、观察态 67。
> 说明：观察态比例按「观察态规则数 ÷ 规则总数(67)」计，故为 100%（Daubert 表含 68 项 = 67 规则 + 1 mutation 生成器）。

---

## 二、闭环架构（文字版）

```
┌──────────────────────────────────────────────────────────────────────┐
│                    self_evolution_loop（影子，不自动执行）              │
└──────────────────────────────────────────────────────────────────────┘

  tools/self_observer_637.py        ← 眼睛：扫系统现状，采 14 项指标
            │  data/637_observer.json
            ▼
  tools/error_detector_637.py       ← 挑：8 条规则挑出 top 5 异常
            │  data/637_errors.json
            ▼
  tools/candidate_generator_637.py  ← 想：每异常 2-3 个候选方案（规则库）
            │  data/637_candidates.json
            ▼
  tools/cost_benefit_637.py         ← 算：score = 收益/成本 × 风险系数
            │  data/637_scored.json
            ▼
  tools/evolution_memo_637.py       ← 说：固定格式进化建议书
            │  data/637_evolution_memo.md
            ▼
       人审批（人决定做不做）——系统的建议只是「影子」
```

编排：`tools/run_637_gate.py --loop` 按序串起五段；`--check` 各自只读自检。

---

## 三、各环节输入 / 输出契约

| 环节 | 工具 | 输入 | 输出 | 关键约束 |
|---|---|---|---|---|
| 看 | `self_observer_637` | 仓库现状（git / glob / 635 只读依赖 / pytest·ruff·mypy） | `data/637_observer.json` + `637_observer_report.md` | `--check` 只读不写盘 exit0；`--report` 才落盘；≥5 单测 |
| 挑 | `error_detector_637` | observer JSON | `data/637_errors.json` + `637_errors.md` | 纯规则，无 LLM；top 5；每异常带 name/current/threshold/severity/why |
| 想 | `candidate_generator_637` | errors JSON | `data/637_candidates.json` + `637_candidates.md` | 规则库匹配；每异常 2-3 方案，带 action/cost/benefit/dependency/risk_class |
| 算 | `cost_benefit_637` | candidates JSON | `data/637_scored.json` + `637_scored.md` | `score = 收益/成本 × 风险系数`；输出全排序 + top3 |
| 说 | `evolution_memo_637` | scored JSON（+observer/errors） | `data/637_evolution_memo.md` | 固定格式；人 5 分钟读完；含「我觉得不靠谱的地方」 |
| 审 | 人 | 建议书 | 决定做不做 | **不自动执行、不代签、不 push** |
| 门 | `run_637_gate.py` | 全部产出 | `data/637_acceptance_report.md` | 零污染 + 6 工具 --check + ruff 全绿 + mypy 0 + 交付齐备 |

**风险系数口径**（供 cost_benefit 用）：只加报告/测量 → 0.5；加新工具 → 1.0；改 `CORE_TOOLS` 判决逻辑 → 1.5。

---

## 四、铁律遵守声明（对应 _auto/inbox/637.md §一）

1. **闭环是影子**：五段工具只产出报告，**不自动执行、不改系统**；建议只在 `637_evolution_memo.md` 里给人看。
2. **受控目录零污染**：受控目录 = `atoms/ evidence/ Examples/ Book/`；本批只写 `tools/*_637.py`、`tests/test_*_637.py`、`data/637_*`。
3. **新工具必有 `--check`**：6 个新工具全部实现只读 `--check`。
4. **不动 CORE_TOOLS**：不修改 `gate_engine.py` 任何规则与判决逻辑。
5. **乐观主义**：先跑起来；粗糙处后调（§五 偏差登记）。
6. **诚实登记**：`637_loop_quality_audit.md` 如实统计靠谱率，不打高分。

---

## 五、诚实登记（预先声明）

1. 本闭环的「智能」= **规则匹配 + 加权打分**，非 LLM/真 AI；
2. 阈值取 635/636 现状经验值（接地 <50%、观察态 >30%、taint >5、例外 >100、ahead >20），**未经校准**；
3. 「工具增长 vs 测试增长不匹配」缺历史序列，用**当前 tools/tests 比值**作代理，可能误判；
4. 首次跑靠谱率预计低（brief §五 预估 30% 量级），**低不代表方向错**，代表阈值待调；
5. 本批不 push、不自动执行任何建议。
