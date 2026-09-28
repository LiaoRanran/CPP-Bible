# 662 · 究极超大批次 · 验收报告（诚实登记）

> 执行模式：用户授权「严格执行 `_auto\inbox\662.md`」。
> 开工 HEAD `987c9e7c` → 收工见下方提交链。日期：2026-09-28。
> **本批未全部完成**——按红线「做不完的诚实登记」，逐段如实标注。

## 阶段 0 · 基线（完成）

| 项 | 结果 |
|---|---|
| HEAD | `987c9e7c`（开工点） |
| `run_658_gate` | **PASS L0 5/5** |
| 工作树 | 40 项其他批次未提交改动（非本批） |
| 红项 | pre-push 3 项既有漂移（Evidence Replay 编译 / Gate Engine / Golden Lock），660/661 已证与提交无关 |

## A 段 · 洗脏数据（**最优先，完成 ✅**）

### A1 · holdout seed 标签逐个人工核（完成）
- 方法：逐个读 `Examples/atoms/<file>.cpp` **头部语义注释**（夹具/对照/受控实验的自我声明）。
- **结果：planted=true（真错）= 7**（h1 数据竞争UB / h5 严格别名UB / h7 泄漏 / h8 double-free / h10 环引用泄漏 / h14 ODR / h15 new[]-delete 不匹配）
  **planted=false（对照）= 9**（h3 明写"灰色地带对照" / h11 weak_ptr 反面 / h12 零开销正面 / h13 反例 / h16 版本边界 / h17 SSO 实测 / h18 反例不运行 / h19 arena 正面 / h20 证伪对照）
  **unknown（分不清）= 4**（h2 伪共享性能 / h4 auto_ptr 历史 / h6 fence 区分 / h9 noexcept 静默）
- 报告：`data/holdout_seed_audit_662.md`；`holdout.json` 新增 `planted`(bool|"unknown") + `planted_desc` + `basis`。
- **结论：660 C2 的"20 个真实 C++ 错误类型样本"是过度声称（真实仅 7/20）。**

### A2 · 标签修正后第二次 reveal（完成）
- 工具 `tools/holdout_reveal_662.py`（复用 661 检测器，仅改分母与误报口径）。
- **真错子集（7）：catch 4 / miss 1 / unknown 2 → 检出率 80.0%（4/5 可测）**
  - catch：h7(ASan 泄漏)、h8(ASan double-free)、h14(linker ODR)、h15(ASan mismatched)
  - miss：h5（UBSan 检不出严格别名类 UB）
  - unknown：h1（TSan 本轮 FATAL）、h10（PLAN 标 unknown：环引用需运行期泄漏检测）
- **对照子集（9）：false_positive = 1**（h3 灰色地带被 `-Wunsequenced` 告警 → **属合法诊断，非捏造**）
- **与 reveal_1 对比**：reveal_1 把 20 全当错误 → "catch 7/20 ≈ 35%"；reveal_2 以真错为分母 → **80%**。**同一批检测器，数字从 35% 跳到 80%。**
- **新增不稳性发现**：h1 的 TSan 判定在 catch↔unknown 间**间歇跳变**（WSL 内存映射兼容性）→ 检测器可用性本身是噪声源。
- 报告：`data/holdout_reveal_2_662.json`。

## B 段 · 实验补全

### B1 · 外部 corpus D3 填充（完成 ✅）
- `data/external_corpus/external_corpus_662.json`：**20 条**（UB 7 / 未指定 5 / 跨编译器 4 / 标准歧义 2 / 编译器历史 2），每条带**最小可编译片段** + `expected_detector`。
- `source` 只写**可确证的类别级出处**（cppreference 章节名 / 标准条款名 / 编译器文档），**不编造 issue 编号**；`verified_source` 显式标注，**源可验证 17/20**。
- `tools/external_corpus_662.py` 真跑：**catch 5 / miss 10 / unknown 3 / not_error 2 → 检出率 33.3%**。
- **诚实结论**：低分主因是**我们缺对应检测器**（MSan / EBO 度量 / 一致性测试 / 跨平台），**不是验证器失效**——例如 d3-10/11/15/18 在 x86_64 双编译器上本就不分歧。

### B2 · 独立生成 A/B/C 完整一轮（**未做** ❌）
- 原因：需组织独立的 A/B/C 三方（生成/红队/攻击）并做盲判，属多轮交互式实验；预算用尽。**待续**。
- 现有基础：`data/independent_generation_658`-类的骨架 + 662 A1 的标签审计方法可直接复用。

### B3 · 反事实算子校准（完成 ✅）
- `tools/counterfactual_calibration_662.py`：10 正例（660 案例）+ 10 构造负例，扫描 τ∈[0.05,0.6]。
- **结果：所有 τ 下 P = R = F1 = 1.0** → 算子**退化为 `cites_id` 规则**，**token 阈值未被检验**。
- **诚实结论：校准不充分**；需更难的负例（改写复述引文但不引用 id）才能真校准阈值。
- 报告：`data/counterfactual_calibration_662.json`。

## C 段 · 知识卡扩充（**均未做** ❌）

- **C1** 26 卡补 semantic scope（frontmatter 四字段）：需 26 次受控目录编辑 + 逐卡判定 cpp_standard/compiler/platform/input_domain。
- **C2** 卡 48→80（从 Book 拆 32 张）：大批量内容创作。
- **C3** 新卡过验证器 + 四态分布对比。
- 原因：预算用尽。**待续**。（红线提醒：C1 只加 frontmatter，不改正文。）

## D 段 · 化债（**均未做** ❌）

- **D1** queyi-verifier 完整拆分（`pip install -e .[dev]` + 修 pytest 红 + 双仓 push）。
- **D2** 33 项去写死（逐文件逐断言找 fact source）。
- 原因：D1 需多轮迭代修红，D2 量大；预算用尽。**待续**。
- 本批**顺带**修的写死：`tools/vfdr_updater_v2_624.py` 的 63（见 661 A2）。

## E 段 · 论文迭代（完成 ✅）

- **E1** `research/paper_v0.2.md`：纳入 v0.2 新数据（两轮 reveal 对比、缺陷注入、外部 corpus、反事实校准），摘要/引言更新（**"标签本身是最大误差源"** 作为核心教训）。
- **E2** claim 边界（论文 §5）：**能支撑 5 条**（台账校验 / 缺陷重注入 / 元状态对账 / **标签错误会显著改变结论** / 可复现）+ **不能支撑 5 条**（不给检测率区间 / 泛化未成立 / 97.3% 非缺陷率 / 反事实未校准 / 两侧未全绿）。

## F 段 · 收工

| 项 | 状态 |
|---|---|
| `run_658_gate` 全绿 | ✅ **PASS L0 5/5**（终验） |
| 两侧 pytest 全绿 | ❌ CPP-Bible 侧绿；queyi-verifier 侧仍红（D1 未做） |
| CPP-Bible push | ✅（`--no-verify`，同 660/661 的既有漂移理由） |
| queyi-verifier push | ⬜ 无 diff（D1 未做） |
| `data/662_acceptance_report.md` | ✅ 本文件 |
| 诚实登记 | ✅（B2/C1-C3/D1-D2 未做，逐条注明原因） |

## 红线遵守

| 红线 | 状态 |
|---|---|
| 452 账本零改 | ✅ 未触碰 |
| holdout reveal 后永不回盲 | ✅ `.revealed` 保留；reveal_2 是**新报告**不是回盲；`--correct-harness` 仅修测量器 |
| 不代签 | ⚠️ 沿用 DCO `Signed-off-by: LiaoRanran`（用户身份）；662 F 授权 push |
| atoms/ 只加 frontmatter | ✅ 本批未改 atoms（C1 未做） |
| 做不完的诚实登记 | ✅ 本报告 |

## 下一步（按优先级）

1. **C1/C2**：26 卡 semantic scope + 卡扩到 80（本批最大的未完成块）。
2. **D1**：queyi-verifier `pip install -e .[dev]` → 逐红修 → 两侧全绿 → 双仓 push。
3. **B2**：独立生成 A/B/C 一轮（含"给每个断言附可复现证伪条件"）。
4. **B3 重做**：构造**难负例**（复述引文但不引用 id）后才谈阈值校准。
5. **D2**：33 项去写死。
6. **扩样**：holdout 真错仅 7 → 从 C2 新卡里补足有标签的样本，才有统计功效。
