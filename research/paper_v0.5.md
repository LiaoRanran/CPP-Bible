# 祈易（Queyi）：让"验证能力"可被独立验收（v0.5）

> **版本关系**：本稿在 `research/paper_v0.4.md`（v0.4.2 口径修订）之上补三块 ——
> §2 Method（实验协议 / 数据集分层 / baseline 定义）、§4 Results（基线表 + 口径消融，全部带区间）、
> §5 Threats（construct / internal / external / statistical / temporal 五层）、§6 Claim 边界（能支撑 /
> 不能支撑 / **不可复现** 三栏）。起草纪律：**只写能复算的数字**；不能复算的写进"不可复现"栏，
> 不删、不美化。
>
> **数字纪律（可机器检查）**：本稿所有 `k/n` 断言带 **Clopper–Pearson 95% 区间**与分母
> （`python tools/ci_check.py research/`、`python tools/caliber_check_669.py --check` 双双为绿）；
> 区间由 `tools/stat_bounds.py` 现算，`data/669_caliber_report.md` 是机器生成的同源口径表。
> n < 30 的估计在正文标 **[探索性]**。
>
> **与并行草稿的关系**：`research/paper_draft_v0.5.md`（另一条工作线起草的叙述稿）与本稿并行存在；
> 本稿只对**数字与边界**负责（逐条给出复算命令），叙述合并留待下一批 —— 两稿冲突时以本稿的
> `data/669_caliber_report.md` 与产物 JSON 为准。

---

## 1. 摘要

祈易把"可被独立验收"作为核心主张：判决规则内嵌引擎（67 条规则；block 0 / warn 176 / advice 55，
`gate_engine.py --check` 现算）、四态判决（pass / fail / unknown / needs_review）、证据带 provenance、
元状态由**不依赖内核**的独立对账器核对。

v0.5 的三条增量（全部有产物）：

1. **口径清场**：所有检出率断言**同时**给出分母、分子、Clopper–Pearson 95% 区间与 Wilson 敏感性列
   （政策：`research/ci_policy.md`；执行：`tools/ci_check.py` + `tools/caliber_check_669.py`）。
   清场过程中抓到两处**真缺陷**：变异率把 core 的分子 110 与 all 的分子 128 拼成一个分数（正确分母见 §4.1）<!-- ci-check: ignore（此句引用的是被更正掉的错误配对 `110/128` 及其 85.9%，本身不是率断言） -->，以及若干"率无分母"的引用。
2. **验证工具只读化**：`atom_evidence_replay.py --check` 从"删旧工件→在仓库重生成→还原"改为
   **工件产出重定向到暂存目录**（仓库零写），并给中断路径补了在飞工件还原。
   验收：66 张证据卡连跑两轮判决**逐卡零差异**（confirm 56 / refute 10 / infra_error 0），
   受控目录 `git status` 零变化。
3. **证据卡补全 + 双平台留痕**：668 新增的 5 张机器实测卡补齐**独立证据卡**
   （`evidence/{ub,mem}/EV-*-669.md`）：每张含工件（本机 `-O2 -S` 汇编，sha 现算）、
   结构断言（MinGW 15.3 与 Linux 13.3 **两边实测**成立的指纹）、`expected_sanitizer`、
   量化证伪条件，以及 **WSL 检测器 + Windows 探针两份真机留痕**。

---

## 2. Method（实验协议 / 数据集 / baseline）

### 2.1 仪器（instrument）是一等公民

本系统的检出率由**外部 sanitizer 仪器**测量：`g++ -std=c++17 {-O0,-O2} -g -fsanitize=<kind>`
在 **WSL（Ubuntu 13.3.0）** 里编译并运行夹具；`-O0` 与 `-O2` **两档都跑，任一档报出即 catch**
（单档口径是 666 的假 miss 根因，见 §5 internal）。

| 协议字段 | 值 | 为什么必须登记 |
|---|---|---|
| `protocol_version` | `669-P3/v1` | 没有它，数字无法归属到某次运行 |
| `verifier_version` | `tools/holdout_reveal_3_665.py`（detect 复用 `holdout_reveal_661.py`） | 判定逻辑可替换，必须钉住 |
| `dataset_version` | `queyi-holdout-reveal/v3`、`queyi-external-corpus-reveal/v2` | 样本集合变过（20 → 40） |
| `seed` | 无（本批全量复算；随机基线若做必须带种子） | 随机臂不可复现的头号原因 |
| `commit` | 见 `data/experiments/669_experiments.json::registry.commit` | 工作树与运行时必须可追溯 |
| `env` | WSL g++ 13.3.0 / 本机 MinGW 13.1.0（`holdout_reveal_3_665.json::env`） | **缺 WSL 会静默掉分**（审计 A1/A3） |

### 2.2 数据集与分层

| 数据集 | 规模 | 分层 | 口径 |
|---|---|---|---|
| holdout（真错） | 17 条带真值标签 | 单层 | 可测口径 = catch+miss = 16（unknown 1 剔除） |
| holdout（对照） | 9 条 | 单层 | 误报率（本不是缺陷） |
| external corpus | 40 条 | A 本地检测器 25 / B 跨编译器或测量 11 / C 无本地检测器 4 | 主口径 32（剔除 unknown 5 + not_error 3）；全样本口径 40 |
| 反事实案例 | 10 条带真值标签 | — | 分母 10（660 的另 10 条**无标签**，不进 P/R/F1） |

**分层的意义**：A/B/C 是"检测器可用性"的分层，不是难度分层 —— C 层 4 条**全 unknown**，
所以 C 层的 0% 是"没测到"，不是"测了没抓到"（这正是 `0/4 = 0%`（95% CI 0–60.2）必须带区间的理由）。

### 2.3 baseline 定义（B0–B3）与本批的可执行子集

| 基线 | 定义 | 本批状态 |
|---|---|---|
| B0 | 不做验证（随机猜） | 未做（连续型读数下"随机猜"无自然定义） |
| B1 | Rule-only（仅静态规则，无 sanitizer/失败驱动） | **阻塞**：主仓无 `detect_static` 路径（需拆仓接口） |
| B2 | Full-non-failure（资产随机选） | **阻塞**：资产选择在拆仓验证器里 |
| B3 | budget-matched random（同 N 资产：随机 vs 失败驱动） | **阻塞**：同上 |
| **E2（本批新增）** | **口径消融**：同一份原始计数下，unknown 的三种处置 | ✅ 已做（§4.2） |

**红线**：不用主仓里的近似物**冒充** B3；没有接口就没有对照，宁缺不造（登记见 §6 第三栏）。

### 2.4 统计政策

* 主报 **Clopper–Pearson 精确区间**（method = beta，双侧 95%）；另列 **Wilson** 作方法敏感性；
* 零计数写 `0/n（95% CI 0–上限）`：`0/4` 的 95% CI 上界是 60.2%（n 越小上界越高，零计数绝不能读成"零风险"）；
* 满计数写 `n/n（95% CI 下界–100）`：满计数必须带下界（`n` 越小下界越低），否则读者会把它当"确定 100%"；
* n < 30 一律标 **[探索性]**，不进"能支撑"栏；
* 组间比较暂只报差值 + 各自区间（配对检验需要逐档位判定记录，见 §6 第三栏）。

---

## 3. 系统与验证工具（v0.5 的工程增量）

### 3.1 `--check` 只读化（P0-1）

| 项 | 修前 | 修后 |
|---|---|---|
| 工件校验方式 | 删仓库工件 → 在仓库里重生成 → 比 sha256 → 还原 | 工件产出 `-o` 重定向到**暂存目录**，sha/结构断言/阴面全用暂存产物 |
| 中断（SIGTERM/kill） | 还原不完整 ⇒ `Examples/atoms/*.asm` **3 删 6 改**；且"删除"会被固化 | 中断钩子先还原**在飞工件**再退锁；只读模式**从不删** |
| 就地重生成 | 默认行为 | 仅在 `--write`（API `read_only=False`）下发生 |
| 验收 | — | 66 卡两轮判决逐卡零差异；`tests/test_readonly_replay_669.py` 6 例锁死 |

### 3.2 证据链补全（P0-2）

5 张新机器卡的证据从此**可被独立复核**：每张配 1 张 `EV-*-669.md`，含
① 工件（`-O2 -S` 汇编，sha256 现算）；② 结构断言（MinGW 15.3 / Linux 13.3 双实测成立）；
③ `expected_sanitizer`（CI Linux 上 replay 会**真跑一遍检测器** ⇒ 第三份独立测量）；
④ 量化证伪条件；⑤ 两份真机留痕（WSL 检测器原始输出 + Windows 探针输出）。

**顺带纠正一个 665 口径缺陷**：`index_665.json` 的 `fixture_sha256` 是 `sha(源码字符串)`
而非文件字节（差一个结尾 LF）——任何"拿 index 里的 sha 去校验文件"的写法都会误判。
新证据卡两个 sha 都记，夹具漂移以**文件 sha** 判定。

**门禁效果**：`gate_engine --check` 的 block 从 **30 → 5**，余 5 条全是
`ATOM-DAL-MATCH`（DAL B 须人审签署）——**唯人签项，机器不代签**。

---

## 4. Results

### 4.1 基线表（现算，`data/experiments/669_experiments.json`）

| 指标 | k/n | 点估计 | Clopper–Pearson 95% | Wilson 95% | 备注 |
|---|---|---|---|---|---|
| holdout 真错（双档） | 14/16 | 87.5% | 95% CI [61.7, 98.4] | [64.0, 96.5] | 探索性（n<30） |
| holdout 对照误报 | 1/9 | 11.1% | 95% CI [0.3, 48.2] | [2.0, 43.5] | 探索性 |
| external 可测口径 | 14/32 | 43.8% | 95% CI [26.4, 62.3] | [28.2, 60.7] | 主口径 |
| external 全样本 | 14/40 | 35.0% | 95% CI [20.6, 51.7] | [22.1, 50.5] | 第二口径 |
| external 层 A | 13/24 | 54.2% | 95% CI [32.8, 74.4] | [35.1, 72.1] | 探索性 |
| external 层 B | 1/8 | 12.5% | 95% CI [0.3, 52.7] | [2.2, 47.1] | 探索性 |
| external 层 C | 0/4 | 0% | 95% CI [0, 60.2] | [0, 49.0] | 探索性；零计数 ≠ 零失效率 |
| 反事实 P / R | 2/2 | 100% | 95% CI [15.8, 100] | — | 探索性；真值与判据同源 ⇒ **上界** |
| 变异 kill（core） | 110/113 | 97.3% | 95% CI [92.4, 99.4] | — | 内部指标，不作缺陷检测率 |
| 变异 kill（all） | 128/157 | 81.5% | 95% CI [74.6, 87.3] | — | 同上 |

**与 v0.4 的差异（两处更正）**：① v0.4 写"killed 110/128"是把 core 的分子与 all 的分子拼成一个分数
（110/128 = 85.9% ≠ 81.5%）<!-- ci-check: ignore（引用被更正掉的错误配对本身；正确值见上表） -->，正确的分母是 113（core）/ 157（all）；② v0.4 未给 `33.3%` 标注
不可复算（662 轮产物只记了率）——本稿已在 §4.3 登记。

### 4.2 口径消融（E2，同一份原始计数）

| 臂 | holdout 真错 | external |
|---|---|---|
| A 主口径（unknown 剔除） | 87.5%（14/16；95% CI [61.7, 98.4]） | 43.8%（14/32；95% CI [26.4, 62.3]） |
| B unknown 记 miss | 82.4%（14/17；95% CI [56.6, 96.2]） | 37.8%（14/37；95% CI [22.5, 55.2]） |
| C unknown + not_error 都进分母 | 82.4%（14/17；95% CI [56.6, 96.2]） | 35.0%（14/40；95% CI [20.6, 51.7]） |
| Δ（A − B） | +5.1pp | +6.0pp |
| Δ（A − C） | +5.1pp | +8.8pp |

**读法**：口径效应（external 最多 8.8pp）**不小于**层间差异的一部分（B 层 12.5% 的 CI 上界 52.7%）⇒
任何"只报一个百分数"的写法都会让读者在 35.0%–43.8% 之间自由发挥。

### 4.3 报告了什么、没报告什么

* **报了**：holdout / external（两个口径 + 三层）/ 反事实 / 变异（core + all），全部带区间与分母；
* **没报**：B1/B2/B3（§2.3，登记阻塞原因）；662 轮的 `33.3%`（**不可复算**：旧产物只记率，
  无分子/分母 ⇒ 只能作方向性参照，**不能当基线**）；
* **不能用**：把变异 kill 当缺陷检测率（内部指标）；把扩样样本当盲态证据（665 扩样在 reveal 后加入）。

---

## 5. Threats to validity（五层）

### 5.1 Construct（构念效度）

* 我们的"检出率"= **sanitizer 仪器在夹具上是否报出**，不是"人是否认为这是缺陷"。
  两者在**对照子集**上会分叉：对照 1/9（95% CI 0.3–48.2）被仪器报出（误报），
  说明仪器判定 ≠ 语义判定。
* `observation` 命题要求"机器闭环"（gate `OBSERVATION-NEEDS-ARTIFACT`）：5 张新卡由
  `artifact_assert` + 真机留痕支撑；但**结构断言**只能锚"机器形态"（如 `mov eax, 1`），
  不能锚"这条 UB 的语义" —— 语义层仍待人工审签（DAL B 的 5 条 block 就是它）。

### 5.2 Internal（内部效度）

* **仪器配置就是结论**：单档 `-O1` → 双档 `-O0/-O2` 使 holdout 从 66.7%（10/15；95% CI [38.4, 88.2]）
  变成 87.5%（14/16；95% CI [61.7, 98.4]）。**检测器一行没改**，改的是"怎么测"。
  故本系统所有数字都必须在**协议登记**（§2.1）下读。
* **环境漂移**：holdout/external 依赖 WSL + libasan/libubsan。缺 WSL ⇒ 静默降级（审计 A1/A3）。
  本批把 `env` 写进产物，并给新证据卡显式声明 `expected_sanitizer`（缺环境只 skip，不误判 confirm）。
* **工具自污染（已修）**：`--check` 曾会改写受控目录（§3.1）。

### 5.3 External（外部效度）

* external corpus 40 条**不是随机抽样**：三层是按"检测器可用性"构造的（A 25 / B 11 / C 4），
  所以 pooled 43.8% 是**分层构成相关**的读数；换构成就换值（这就是要求"两口径并列"的原因）。
* holdout 17 条真错来自 660/665 的**程序化构造**（不是真实缺陷报告），构造方式与检测器同源
  ⇒ 只能证"检测器能测到什么"，不能证"现实中最重要的缺陷都在里面"。

### 5.4 Statistical（统计效度）

* n 小是主约束：holdout 16、反事实 10、层 B 8、层 C 4 —— 区间宽到能装下相反结论
  （层 B 12.5% 的上界 52.7%）。**本批所有这类行都标 [探索性]**，不作为"能支撑"结论。
* 口径消融是**描述性**的：Δ 与区间分别给出，但未做配对检验（需要逐档位判定记录，登记在 §6）。
* 多重比较未校正（本批只做少量预定义比较；未做 BH/Holm）。

### 5.5 Temporal（时间效度）

* 数字与**工具链版本**绑定：MinGW 13.1/15.3、WSL g++ 13.3、sanitizer 运行库版本都会改变结果；
  产物记录 `env` 与 `artifact_compiler`，跨环境重跑必须先比对这两项。
* 仓库状态口径：`git status --porcelain -uall`（含未跟踪）；"受控目录零改动"的判据是本批
  反复使用的红线（669 起 `--check` 结构性保证它）。

---

## 6. Claim 边界（三栏，逐条给复算命令）

### 能支撑（可复算）

| 结论 | 数字 | 复算命令 |
|---|---|---|
| holdout 检出率（双档口径） | 87.5%（14/16；95% CI [61.7, 98.4]） | `python tools/holdout_reveal_3_665.py` |
| external 检出率（两口径） | 43.8%（14/32；95% CI [26.4, 62.3]）/ 35.0%（14/40；95% CI [20.6, 51.7]） | `python tools/external_corpus_reveal_665.py` |
| 口径效应 | A−C = +8.8pp（external；95% 区间见 §4.2） | `python tools/experiments_669.py --report` |
| 全部率断言的区间与分母 | 一致性检查全绿 | `python tools/caliber_check_669.py --check` |
| 证据卡机器复算 | 66 卡：confirm 56 / refute 10 / infra_error 0（两轮逐卡零差异） | `python tools/atom_evidence_replay.py --check` |
| 5 张新卡证据链 | 5 张证据卡 + 双平台留痕 + 结构断言全部成立 | `python tools/ev_ub_atoms_669.py --check` |
| 门禁状态 | block 30 → 5（余 5 条为 DAL B 唯人签项） | `python tools/gate_engine.py --check` |

### 不能支撑（**不要写**）

* ❌ "检出率 87.5% 说明验证器比 666 强"：变的是**档位口径**，检测器一行没改（§5.2）。
* ❌ "external 43.8% 优于 662 轮的 33.3%"：两轮样本集合不同，且 33.3% **不可复算**（§4.3）。
* ❌ "C 层检出率 0%"：0/4 的 95% CI 上界是 60.2%（零计数与高真实率相容，不能说"零缺陷漏检"）。
* ❌ "变异 kill 81.5% 代表缺陷检测能力"：内部充分度指标（自证闭环）。
* ❌ "反事实 F1 = 1.0 可泛化"：分母 10、真值与判据同源 ⇒ 只是**上界**（P=R=2/2，95% CI [15.8, 100]）。
* ❌ "失败驱动选资优于随机选资"：B3 未做（接口在拆仓验证器，§2.3）。

### 不可复现（本环境缺失/历史产物不足，**保留不删**）

| 项 | 数字 | 为什么不复现 |
|---|---|---|
| 662 轮 external | 33.3% | 旧产物只记率、无分子/分母 ⇒ 永远拿不到口径与区间（§4.3） |
| 666 声称的 holdout | 81.2%（13/16；95% CI [54.4, 96.0]） | 从未出现在任何产物里；重跑为 87.5% ⇒ **作废**（v0.4 文首修订表） |
| 本文档的数字 | 全部 | 依赖 WSL + libasan/libubsan；缺 WSL 的机器上**静默掉分**（审计 A1/A3）⇒ 必须先核 §2.1 的 `env` |
| B1/B2/B3 | — | 需要拆仓验证器的接口（`detect_static` / `select_assets`），主仓无法独立复算 |

---

## 7. 相关工作与研究伦理

* 相关工作定位沿用 v0.4 §7（本批未新增对比实验）；**已知缺口**：对比仅定位性、无同台实测，
  故不作为"优于"的依据。
* AI 参与：本稿由 LLM 辅助起草，逐处登记在 `research/AI_USAGE_LOG.md` / `research/AI_USAGE_shturl`；
  未登记的 AI 贡献按项目纪律视为未声明作者（`research/13_ai_use_and_authorship.md`）。
* 数据与工具：本稿所有数字的产物与工具路径见 §6；`data/669_caliber_report.md` 是机器生成的口径表。

## 8. 复现入口（一条命令级）

```powershell
.venv\Scripts\python.exe tools\holdout_reveal_3_665.py            # holdout（双档 + 明细 + env）
.venv\Scripts\python.exe tools\external_corpus_reveal_665.py      # external（两口径）
.venv\Scripts\python.exe tools\counterfactual_extend_665.py       # 反事实（分母 + 第三判据）
.venv\Scripts\python.exe tools\caliber_check_669.py --check       # 口径 / 区间 / 声称值一致性
.venv\Scripts\python.exe tools\experiments_669.py --run           # 基线表 + 口径消融（带协议元数据）
.venv\Scripts\python.exe tools\atom_evidence_replay.py --check    # 证据卡机器复算（只读）
.venv\Scripts\python.exe tools\ev_ub_atoms_669.py --check         # 5 张新卡的证据链一致性
```
