# 621 验收报告 · 17 任务（新 mutation 生成 + CI 竞态根治 + 雷6 弃权三态 + 30 条逐条人审落地）

> 批次：621 · 起始 `d5edb14`（620 收工）· 收工 HEAD 见文末
> 本批 commit：**16 个任务 commit**（任务0 + A1-A4 + B1-B3 + C1-C3 + D1-D3 + E1-E2）
> + 若干补正 commit；区间内另含 **1 条并行 PM 会话**插入的 commit（见 §七.7）
> 状态：**awaiting_review**（不 push、不 golden accept、不打开 delegation、不代签人审）
> 解释器：`.venv\Scripts\python.exe`（本批修复，见 §六）

---

## 一、任务完成度：17/17

| # | 任务 | 交付 | Commit | 状态 |
|---|---|---|---|---|
| 0 | 开工基线 | `data/621_baseline.md` | `ed84ad7` | ✅ |
| A1 | mutation 生成器框架 | `tools/mutation_generator_621.py` + 15 例单测 | `763d6f7` | ✅ |
| A2 | 第一轮生成 + 判决 | `data/mutation/new_mutations_621_round1.jsonl`(50) + `data/mutation_generation_round1_621.md` + 9 例 | `ce0f449` | ✅ |
| A3 | 质量评估 + 去重 | `tools/mutation_quality_621.py` + `data/mutation_quality_report_621.md` + `high_value_621.json` + 12 例 | `f9d1a50` | ✅ |
| A4 | 闭环第二轮 | `data/adversarial_loop_round2_621.md` + 7 例 | `f072c27` | ✅ |
| B1 | ci.yml gate+replay 加 needs | `.github/workflows/ci.yml` + `data/ci_race_fix_621.md` + 6 例 | `4eee9d0` | ✅ |
| B2 | 本地并发竞态复现工具 | `tools/ci_race_reproducer_621.py` + `data/ci_race_reproduction_621.md` + 9 例 | `01c1de9` | ✅ |
| B3 | CI 并发安全检查 | `tools/ci_concurrency_check_621.py` + ci.yml 新 job + 10 例 | `829b384` | ✅ |
| C1 | ABSTAIN 状态定义 + 分类器 | `data/abstain_state_definition_621.md` + `tools/abstain_classifier_621.py` + 14 例 | `381726c` | ✅ |
| C2 | 全量 83 张 ABSTAIN 分类 | `data/abstain_classification_621.jsonl` + `data/abstain_classification_report_621.md` + 8 例 | `0060c06` | ✅ |
| C3 | ABSTAIN 与 PCK 集成 | `tools/pck_abstain_sync_621.py` + `data/pck_abstain_sync_report_621.md` + 8 例 | `acf14c5` | ✅ |
| D1 | 30 条复核 → Authority 待审条目 | `tools/authority_pending_621.py` + `data/authority/pending_review_621.jsonl`(30) + `data/authority_pending_30_621.md` + 9 例 | `a6fc405` | ✅ |
| D2 | 人审质量评估 | `tools/human_review_quality_compare_621.py` + `data/human_review_quality_compare_621.md` + 10 例 | `6dc37c9` | ✅ |
| D3 | 人审数据脱敏 + 导出 | `tools/human_review_anonymize_621.py` + `data/human_review_anonymized_621.jsonl`(776) + 报告 + 10 例 | `938635b` | ✅ |
| E1 | 620 交人项 + 化债 | `data/621_debt_clearance.md` | `15e73d4` | ✅ |
| E2 | 收工门禁 + 验收报告 | `tools/run_621_gate.py` + `tests/test_621_gate.py` + 本文件 + status/outbox | 见文末 | ✅ |

---

## 二、收工门禁（E2）复跑结果

```
run_621_gate → 验收门: PASS (EXIT=0)
解释器：.venv\Scripts\python.exe
[1/6] 受控目录零污染            ✅ 干净（atoms/ evidence/ Examples/ Book/）
[2/6] 621 新工具 --check        ✅ 9/9 通过（run_621_gate 自身不参与，避免自指）
[3/6] 620 工具 --check 回归      ✅ 7/7 通过
[4/6] ci.yml 语法 + 并发安全     ✅ YAML OK + 并发安全检查通过
[5/6] ruff 静态检查              ✅ 23 个文件通过
[6/6] pytest（621 新增单测）      ✅ 127 passed
刻意不跑（621 §六.3）：tool_integrity --check, gate_engine --check, poison_drill, atom_evidence_replay --check
```

- 门禁自身单测 `tests/test_621_gate.py`（11 例）**单独跑全绿**；
  未纳入 `NEW_TESTS_621` 是刻意的（否则「门禁 → 自己的单测 → 门禁」自指递归）。
- **621 新增单测合计 138 例**（127 + 门禁自身 11）。

---

## 三、实测数字

### 3.1 A2 新 mutation 生成（50 条）

| 项 | 值 |
|---|---|
| 生成总数 | **50**（覆盖 50/83 张卡） |
| 策略分布 | rule_blind_spot **17** · evidence_ambiguity **17** · provenance_inconsistency **16** |
| 判决（**预测**） | blocked **36** · n_a **14** · escaped **0** |
| **新逃逸发现** | **0** |
| 判决依据 | 50/50 命中 v7「同卡同算子」实测记录（confidence=high） |

⚠ **判决是预测，不是真实 gate 运行**（621 §六.3 不跑门禁 + 无沙箱施加 API）。详见 §四.3。

### 3.2 A3 质量评估

| 维度 | 均值 |
|---|---|
| novelty（新颖性） | **0.50**（50/50 落在「(卡,算子) 已存在但变异点新」档） |
| attack_strength | 0.14（blocked 计 0、n_a 计 0.5） |
| semantic_validity | 1.00 |
| reproducibility | 1.00 |
| composite | 0.506（Top1 = 0.65） |

**关键诚实发现**：50 条新 mutation 的**（卡,算子）组合 100% 已存在于 v7** ⇒
**候选空间并未真正被打散**，只有"变异点"是新的。

### 3.3 A4 闭环第二轮（W2，3 轮，Top10）

| 项 | 值 |
|---|---|
| 候选 / 可判 | 50 / **36** |
| 每轮 blocked | 10 / 10 / 10 |
| 每轮 escaped | **0 / 0 / 0** |
| 新逃逸 | **0** |
| VFDR 累计 | **0.0**（序列 [0.0, 0.0, 0.0] → flat-zero） |
| 收敛 | 是 |

**与 620 第一轮的差异**：621 第二轮**首次用上非 v7 的新 mutation**（620 想做而做不到），
但逃逸仍为 0 —— 因为判决是预测、且新颖性不足（§3.2）。

### 3.4 B1/B3 CI 竞态修复

| 项 | 内容 |
|---|---|
| 修复 1 | `gate` 加 `needs: [replay]`（写者先、读者后） |
| 修复 2 | **B3 追加发现**：`quality` 的 Worktree-Cleanliness 步骤同样读 `Examples/atoms/` 且与 replay 并行 ⇒ 一并加 `needs: [replay]` |
| 固化 | 新增 `concurrency-safety` job（跑 `ci_concurrency_check_621.py`） |
| 验证 | ci.yml YAML 语法 OK；并发安全检查 **通过**（`REAL_EXIT:0`） |
| 未验证 | CI 实际运行（621 不 push） |

### 3.5 C2 ABSTAIN 分类（83 张）

| 状态 | 张数 | 占比 |
|---|---|---|
| SUPPORTED | **56** | 67.5% |
| UNDECIDED | **27** | 32.5% |
| REFUTED / INSUFFICIENT_EVIDENCE / CONFLICTED / STALE | 0 | 0% |

**弃权合计 27/83（32.5%）**。
- 原子卡 27 张 **全部 UNDECIDED**（原子卡**没有 `verdict` 字段**）；
- 证据卡 56 张 **全部 SUPPORTED**（有 `verdict: confirm` + `artifact_sha256`）。

**⚠ 关键交叉发现（与 PCK）**：

| ABSTAIN × human_authority | 张数 |
|---|---|
| SUPPORTED × pending | **56** |
| UNDECIDED × approved | **27** |

**完全反相关**：机器说"支持"的 56 张人全部未批准；机器说"不知道"的 27 张人全部已批准。
⇒ 机器判据与人的授权**基于不同信号**，暴露"机器说知道、人没认"与"人认了、机器不知道"
**两个方向的缺口同时存在**。

### 3.6 C3 ABSTAIN ↔ PCK 同步

| 项 | 值 |
|---|---|
| 同步成功 | **83 / 83** |
| `uncertainty.abstain_state` | SUPPORTED 56 / UNDECIDED 27 |
| **`human_authority`** | **改动 0**（approved 27 / pending 56 前后完全一致）⇒ 不代签 |
| 同步后 B2 验证 | **83 / 83** |

### 3.7 D1 30 条待审条目

| 项 | 值 |
|---|---|
| 待审条目 | **30**（建议 MODIFY 17 + ACCEPT 13） |
| `status` | 全部 `pending` |
| `review_method` | 全部 `item_by_item_proposed` |
| **Authority 决策日志** | **388 → 388（零改动）** ⇒ 不代签（机制化证明） |

### 3.8 D2 人审质量对比

| 维度 | 批量（388） | 逐条（30） |
|---|---|---|
| 理由长度均值 | 69.2 | **21.9**（更短） |
| 理由去重数 | 5 | **2** |
| 一致性（字面 / 语义族） | — | 43.3% / **100%** |
| 真语义分歧 | — | **0** |

**诚实结论**：逐条建议**理由是模板化的、决策是从批量派生的** ⇒
当前"逐条"只是**形式上的逐条**，其价值尚未兑现（价值在于把 17 条可疑边挑出来供人审）。

### 3.9 D3 脱敏

| 项 | 值 |
|---|---|
| 输出条数 | **776**（388 Authority + 388 历史标注） |
| 真实姓名残留 | **0**（2 个已知姓名扫描 clean） |
| 时间戳 | 全部截断到日 |

---

## 四、偏差表（自报 vs 实际）

| 项 | 提示词/计划 | 实际 | 偏差说明 |
|---|---|---|---|
| 新建工具数 | 9 个 | **10 个** | D1 需可测试代码 ⇒ 新增 `authority_pending_621.py`（提示词任务表未列） |
| C1 状态数 | 提示词写"5 态"却列 6 个名字 | 按 **6 态**实现 | 提示词内部不一致，已在 C1 文档登记 |
| C1 路线图来源 | "读 37 号路线图雷6节" | **仓库内检索不到** | 与 620（雷5）同况，按提示词规格 + 现有系统推导并如实登记 |
| B2 竞态实跑 | "修复前应能复现，修复后应为 0" | **未实跑（dry-run）** | 621 §六.3 不跑门禁；且 replay 会写受控目录。改为引用 620 历史实测 |
| A2/A4 判决 | "运行 gate_engine 做判决" | **改为 v7 先验预测** | 621 §六.3 不跑 gate（620 曾开口子，621 收回）；无沙箱施加 API |
| 单测例数 | A1≥8 / A2≥4 / A3≥5 / A4≥3 / B2≥3 / B3≥4 / C1≥6 / C2≥3 / C3≥4 / D1≥3 / D2≥4 / D3≥3 | 15/9/12/7/9/10/14/8/8/9/10/10 + gate 11 | **全部超额达标** ✅ |
| 本批 commit 数 | 17 任务 | **16 个任务 commit** + 补正（+1 并行 PM commit） | 见 §七.7 |

---

## 五、交人项（不可代决）

### 5.1 621 提示词 §八 的 5 条

1. **新 mutation 是否纳入 v8 基线**（50 条）；需人审。
2. **ABSTAIN 是否对外展示**（是否写入 `data/pck/rendered/`）；本批未重渲染。
3. **30 条逐条人审是否执行**（D1 只建待审条目）；执行结论由人给。
4. **CI 竞态修复是否 push**（改了 ci.yml，远程验证需 push）。
5. **人审脱敏数据是否开源**（776 条已就绪）。

### 5.2 621 新增（须人知悉）

6. **schema 文档升级**：C3 新增了 `uncertainty.abstain_state` 等字段，
   但 619 B1 schema（`data/pck_certificate_schema_619.md`）**未同步** —— 冻结件，改它需人审。
7. **原子卡缺 `verdict` 字段**：导致 27 张原子卡机器侧恒为 UNDECIDED。
   是否给原子卡补 `verdict`（改受控目录）由人定。
8. **`quality` 也需 `needs: [replay]`** 已由 B3 实施 —— 这会**增加 CI wall time**
   （quality 不再与 replay 并行），是否接受由人定。

### 5.3 620 遗留仍留人（5 条，未变）

权重拍板 · Authority 是否启用替换现有人审通道 · PCK 是否成权威源 ·
是否 push · **沙箱 apply API**（本批**仍未解除**，是 VFDR 恒 0 的根本瓶颈）。

---

## 六、环境修复（本批）

`.venv\Scripts\python.exe`（uv trampoline）在 D1 期间损坏
（`uv trampoline failed to spawn / os error 2`），根因是 uv 的
`cpython-3.13-windows-x86_64-none` **junction 不可遍历**（Windows `error 448`）。

**修复**：用 base 解释器（`3.13.13`）的 `python.exe`/`pythonw.exe`/4 个 DLL 恢复
`.venv\Scripts\`，原 trampoline 备份为 `python.exe.uv-trampoline.bak`。
**结果**：`.venv\Scripts\python.exe -c "import yaml, pytest"` → OK（3.13.13 / pytest 9.1.1）。
`.venv` 不在版本控制内 ⇒ **不影响仓库交付物**。详见 `data/621_debt_clearance.md` §四。

---

## 七、未做项 / 诚实登记

1. **A 线未产生任何新的机器验证事实**：判决全为预测（§四 偏差表）。
   ⇒ 621 仍**没有真正打破**"只考旧题"的困境；真正打破需要沙箱 apply API。
2. **候选空间未真正打散**：50 条的（卡,算子）组合与 v7 100% 重合（A3 实测）。
3. **B2 未实跑竞态复现**：dry-run，引用 620 历史实测（2 BLOCK 并发 / 0 串行）。
4. **CI 修复未经 CI 实跑**：621 不 push。
5. **`CONFLICTED` / `STALE` / `INSUFFICIENT_EVIDENCE` 恒为 0**：是元数据缺失
   （`relations` 普遍为空、`verified_at` 缺失）的**判不出来**，不是"没有问题"。
6. **`quality` 竞态**：B1 报告曾把它列为"留 622"，B3 的静态检查当场抓到并已修，
   属**提前化债**（已在上表登记）。
7. **并行会话插入**：`d5edb14..HEAD` 区间含 1 条**非本批苦力产出**的 commit
   `db6b06c PM：38号产品经理报告（620后）+ 导航索引更新`（由并行 PM 会话提交）。
   本批**未修改**其内容；受控目录清洁检查通过说明它未污染 `atoms/evidence/Examples/Book`。
8. **工作树遗留**（CRLF 假脏 `p57.cpp`、`metrics_612.md`、未跟踪 `_arch_v19/20/`）
   保持原状，不清理、不提交（沿用 619/620 处置）。
9. **621 仍未做**：雷1 / 雷7 / 雷8（提示词 §六.9 明确留 622+）。
