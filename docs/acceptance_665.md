# 665 批验收报告（0 § A § B § C § D § E § F § G § H）

> 纪律：**只登记实际跑了什么、读出什么**；没做的写"未做"；不把点估计说成结论。
> 数据截至 2026-09-29。所有命令均可在本仓复跑。

---

## 0 § 门基线（开工前）

| 命令 | 结果 |
|---|---|
| `python tools/run_658_gate.py --check` | 7/7 PASS（含 L0 红线 S1/S3/S6） |
| `python tools/status_reconciler.py --check` | **本仓无此工具**（它在 queyi-verifier 侧）⇒ 665 未在本仓复跑 |
| `python tools/ig_cards_665.py --check` | PASS 16/16 复现一致 |

**诚实更正**：0 段原计划里的 `status_reconciler --check` 在 CPP-Bible 侧**不存在**
（663/664 记录描述的是双仓语境），本报告不冒充跑过。

---

## A § 还债

### A1 语料缺口（**做了一半**）

- 症状：`C:\CodeLearnling\queyi-verifier` 全量 pytest **323 FAILED / 0 ERROR**。
- 定位：`atoms`、`data` 已是**联结**（junction）指向 CPP-Bible，但
  `Examples/atoms`、`evidence`、`misconceptions`、`.github`、`Book`、`research`、`docs`、`goldens` **缺失**。
- 处置：按**既有联结模式**补 8 个联接（`Examples/atoms` 原 30 个生成物改名保留，不删）。
- 结果：**fast 套件 红 323 → 125**（`uv run ... pytest -m "not slow" -n auto`；
  323 是**全量串行**数字，两次口径不完全可比，已在论文 §4 注明）。
- 残余 125 红：**39 条与 CPP-Bible 同源**（同一种"写死数字"病），86 条 verifier 独有
  （抽样看是 **tools 版本漂移**，例如 `test_kc_inventory_612` 期望 37 而本仓工具返回 47 ⇒ 工具副本旧）。
- **未做**：A2（写死数字去债，33 项）、A3（slow 基线）。

### A2/A3

**未做。** 只顺手修了 1 条**触发线**测试（`test_four_state_verdict_638.py::test_audit_real_corpus`）：
638 原本断言"卡无边界 ⇒ 全 unknown"（一条刻意触发线），665 回填边界后它**按设计亮了**
（23/23 有边界）。改为断言**关系**（有边界计数 == 逐卡 `boundary_ok` 之和；有边界不得停 unknown），
不再冻结数字。**其余 51 条同源红未碰。**

---

## B § 新增证据

### B1 664 独立生成 → 16 张机器卡

- `python tools/ig_cards_665.py --build` → 16 张（664 的 15 条 + 1 条修正探针 ig-16）。
- `python tools/ig_cards_665.py --check` → **16/16 复现一致**。
- 四态：pass 12 / unknown 4；verdict：catch 6 / miss 5 / unknown 1 / measure 4；与 664 记录 **16/16 一致**。
- **发现的真 bug**：664 的 ig-04 夹具有两处问题——①缺 `#include <utility>`（编译失败）；
  ②即便补上也**不会**推翻断言（该类型自带移动构造，只会打印 `move`）⇒ **664 的反例构造无效**。
  已登记在卡内 §六，并以 ig-16（类型无移动构造）重做该条。
- 机器卡一律 `signed_by: none` / `needs_review: true`；测试 `test_ig_cards_are_never_signed` 锁死红线。

### B2 Book 拆卡

**未做**（目标 83 张，实际新增 16 张机器卡）。

---

## C § 盲化与外部效度

### C1 holdout 20 → 30

- `python tools/holdout_extend_665.py --extend` → 30 样本，**真错 7 → 17**。
- **踩到并修掉的陷阱**：`holdout.json` 是 `holdout_658.py` 的**产物**，那个工具一跑就按内建 20 样本
  重写文件 ⇒ 665 的追加被**静默抹掉**（本批实测发现）。处置：另立 canonical
  `data/holdout/holdout_665.json` + 幂等 `merged()`，并加测试 `test_merge_view_survives_product_rewrite`。
- 诚实登记写进数据文件本体：新增 10 个样本**不具备盲态**（追加发生在 reveal 之后），
  只能用于增大样本量，**不得**据此 Claim 外部效度提升。

### C2 reveal_3

| 指标 | 值 |
|---|---|
| 真错子集 | 17（catch 10 / miss 5 / unknown 2）→ **检出率 66.7%** |
| 对照子集 | 9（误报 1） |
| 与 reveal_2 比 | 80.0%（4/5）→ 66.7%（10/15 可测）；**分母构成变了，不是验证器退步** |
| 优化档敏感性 | miss 的 5 个里 **3 个在 -O0 下 catch**（-O1 把内存操作优化掉了）；h29 位移两档都不报 ⇒ **真缺口** |

---

## D § 外部 corpus

### D1 20 → 40（**刻意分层**）

A 层（本机可跑）16 条 / B 层（跨编译器·测量）2 条 / C 层（本机无检测器）2 条。
同样立 canonical `data/external_corpus/external_corpus_665.json`（理由同 C1）。

### D2 检出率

总 40：catch 14 / miss 18 / unknown 5 / not_error 3 → **43.8%**（662 为 33.3%）。

| 层 | 可测 | 检出率 |
|---|---|---|
| A 本机可跑 | 24/25 | **54.2%** |
| B 跨编译器·测量 | 8/11 | **12.5%** |
| C 本机无检测器 | 0/4（4/4 unknown） | 0%（无可测样本） |

**这就是把 662 的"低分大概因缺检测器"变成对照证据的地方。**

---

## E § 表达层

- **E1**：`docs/trace_layer_665.md` —— 轨迹 5 → 10 条（T6–T10，逐条接地 665 真机卡，可复算）；
  仍是手写 + 机器留痕，**未**自动采集。
- **E2**：`data/counterfactual_cases_665.json` —— 反事实 10 → 20 条，**首次带真值标签**
  （外部锚：standard ⇒ independent / measurement ⇒ dependent）。算子（复用 658 版）
  在 10 条新样本上全判 independent ⇒ **P=R=F1=0（漏判 2）**。
  这把 662 的"校准不充分"从一个形容词变成三个数。

---

## F § 论文

- **F1**：`research/paper_v0.3.md`（§4 全表更新；§5 claim 边界**第三次收紧**：7 条能支撑 / 7 条不能支撑）。
- **F2**：`docs/figure1_665.md`（ASCII + Mermaid 双版闭环图，**每个数字标注出处**）。

---

## G § 前端

- **G1**：`python tools/web_status_655.py` 现算 → 卡 37(+10 draft)、规则 67（block 44）、
  逃逸 1/1406；再由 `tools/web_ig_cards_665.py` **追加** `ig_cards_665`（16 张，机器卡）。
- **G2**：`web/data/ig_cards_665.json` + `web/card.html` 一行说明；
  **明确不进** `cards.json` 教学台账（红线：verified 唯人签），并有测试锁
  （`test_web_ig_cards_are_labelled_machine_derived`）。
  目标"83 张卡全进前端"**未达**（只 16 张机器卡）。

---

## H § 交付

| 项 | 状态 |
|---|---|
| 门禁 7/7 | PASS（665 未动门规则） |
| 新增测试 | `tests/test_ig_cards_665.py`（10 条，全绿，不编译属 fast 套件） |
| 修改测试 | `tests/test_external_validity_658.py`（**只放宽下界**，不撤一致性锁）；`tests/test_four_state_verdict_638.py`（触发线改关系断言） |
| 复算入口 | 见 `research/paper_v0.3.md` §8 表（7 条命令） |
| 两侧全绿 | **未达**（CPP-Bible fast 52 红；verifier fast 125 红） |

### 665 批新增文件（可点验）

```
tools/ig_cards_665.py                16 张机器卡（--build/--check/--selftest）
tools/holdout_extend_665.py          holdout 20→30（canonical + 幂等合并）
tools/holdout_reveal_3_665.py        reveal_3 + -O0/-O1 敏感性
tools/external_corpus_extend_665.py  corpus 20→40（分三层）
tools/external_corpus_reveal_665.py  40 条检出率 + 分层
tools/counterfactual_extend_665.py   反事实 20 条 + 算子打分
tools/web_ig_cards_665.py            机器卡进前端（不混入台账）
data/cards_665/                      16 张卡 + 16 个夹具
data/holdout/holdout_665.json        canonical 30 样本（真错 17）
data/external_corpus/external_corpus_665.json  canonical 40 条
data/holdout_reveal_3_665.json       第三次 reveal 报告
data/external_corpus_reveal_665.json 40 条 reveal 报告
data/counterfactual_cases_665.json   20 条（带真值标签）
docs/trace_layer_665.md              轨迹 T6–T10
docs/figure1_665.md                  闭环图
research/paper_v0.3.md               论文 v0.3
tests/test_ig_cards_665.py           665 回归测试
```

---

## 一句话总结

665 没把验证器"变得更强"，而是**把三个测量陷阱变成了数字**：
标签（分母 7→17 ⇒ 80%→66.7%）、检测器可用性（A 54.2% vs C 0% 可测）、
编译档（3/5 miss 是假 miss）。
**"不能支撑"清单比"能支撑"清单更值钱**，这就是本批的产出。
