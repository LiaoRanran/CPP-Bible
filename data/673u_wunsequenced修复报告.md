# 673u · wunsequenced 恒 catch 修复报告：修 detect 分支 bug + 重跑全部守护产物 + 历史数字如实重算

- **批次**：673u ｜**日期**：2026-10-03 ｜**执行人**：LiaoRanran（DCO 署名，**未 push**）
- **唯一代码改动**：`tools/holdout_reveal_661.py::detect` 的 `wunsequenced` 分支（其余分支一行未动）
- **产物**：本文 + 重算后的 reveal/attribution/guard 产物（清单见 §6）
- **红线遵守**：`detect()` 其余逻辑（-O0/-O2 双档、`setarch -R`、TSan 不可用判定、其他资产命中定义）未动；
  `detect_for_assets.py` / `run_a5_experiment_673p.py` / `verifier_pool_673p.py` / `selection_strategies_673p.py`
  一行未改（只重跑）；`research/`、`ci.yml`、`.tool_checksums` 未碰。

---

## 0. 结论速览

| 问题 | 答案 |
|---|---|
| bug 修了吗？ | ✅ `wunsequenced` 从**恒 catch**（41/41 与 64/64 全 catch 的常量资产）变为**恒 unknown**（检测器不可用，无支持无反驳） |
| FD 基线 82.9% / 62.5% 被污染了吗？ | **没有。** 重算后逐位不变：holdout **34/41 = 82.9%**、corpus **40/64 = 62.5%**（§3 给出为什么任务书里的担心不成立） |
| 那什么变了？ | **对照假阳性**：holdout control false_positive **2/11 (18.2%) → 0/11 (0.0%)**——两条假阳性全是这个 bug 造成的 |
| A5 变显著了吗？ | **主端点首次达标**：holdout k=4 Δ**+55.00pp** / p=**0.00098**、corpus Δ**+43.75pp** / p=**0.0391**（修复前两者都是 Δ=0.00 / p=1.0000）。**但 holdout 触发预注册 `uninterpretable` 条款，不得单独宣称 FD 优于 Random**（§5） |
| 其他守护产物？ | 变异测试 core **96.5%** / all **81.8%** **逐位复现**；quality **27/27**；guard **18/18 OK**；tool_integrity **exit 0**；fast_gate **overall=PASS** |
| tool_integrity 要重钉吗？ | **不需要。** `holdout_reveal_661.py` 不在四个哈希面（CORE_TOOLS / TEST_CONFIG / SUPPLY_CHAIN / RULER）里，Merkle 根也不覆盖它 —— `--check` 修复后实测 exit 0（§7） |

**一句话**：这个 bug 污染的是**对照假阳性**和 **A5 的可判定性**，不是 FD 的历史检出率；修掉它之后 A5 第一次能读，但读出来的 holdout Δ 是"避开零信息资产"的池构成效应，仍不能当"FD 选择策略更聪明"的证据。

---

## 1. bug 与根因

```bash
$ g++ -std=c++17 -Wall -Wextra -Wunsequenced -fsyntax-only x.cpp
g++.exe: error: unrecognized command-line option '-Wunsequenced'      # exit 1
```

本机 MinGW g++ 13.1（`C:/Qt/Tools/mingw1310_64`）**不认识** `-Wunsequenced`（那是 clang 的选项名）。
而 `detect()` 的命中判定是：

```python
# 修复前（holdout_reveal_661.py L167-170）
if kind == "wunsequenced":
    rc, out = _local(["g++", "-std=c++17", "-Wall", "-Wextra", "-Wunsequenced", "-fsyntax-only"] + copies)
    return ("catch", "g++ -Wunsequenced 告警") if "unsequenced" in out.lower() else ("miss", "无 unsequenced 告警")
```

`"unsequenced" in out.lower()` 命中的是**报错信息里的选项名** `-Wunsequenced` ⇒ **恒真** ⇒
该资产对**任何**输入（哪怕语法错误的空文件）都返回 `catch`。它是一个常量资产，不是检测器。

**影响面（修复前实测，673r 的 840 次真实矩阵）**：

| | 修复前 | 修复后 |
|---|---|---|
| holdout 41 样本 × wunsequenced | **41/41 catch** | **41/41 unknown** |
| corpus 64 样本 × wunsequenced | **64/64 catch** | **64/64 unknown** |
| 全池 OR 判定（8 资产） | holdout 41/41 = 100%、corpus 64/64 = 100% | holdout **35/41 = 85.4%**、corpus **54/64 = 84.4%** |

（OR 掉到 35/41 与 54/64，与 673r 报告 §4.2 的预测"仅被 wunsequenced 抓到的样本 holdout 6 条、corpus 10 条"**逐位一致**。）

---

## 2. 修复（方案 1：识别 "unrecognized option" ⇒ unknown）

```python
# 修复后
if kind == "wunsequenced":
    rc, out = _local(["g++", "-std=c++17", "-Wall", "-Wextra", "-Wunsequenced", "-fsyntax-only"] + copies)
    low = out.lower()
    # 673u 修复：编译器不认 -Wunsequenced ⇒ 检测器不可用 ⇒ unknown（不是 catch，也不许当 miss）
    if "unrecognized command-line option" in low or "unrecognized option" in low:
        return ("unknown",
                "检测器不可用(wunsequenced)：编译器不认 -Wunsequenced"
                "（detector unavailable: compiler does not recognize -Wunsequenced）")
    return ("catch", "g++ -Wunsequenced 告警") if "unsequenced" in low else ("miss", "无 unsequenced 告警")
```

* **为什么是 unknown 而不是 miss**：四态逻辑里 unknown = "无支持、无反驳"，不进检出率分母。
  检测器在当前工具链下根本没跑起来，把它记成 miss 等于声称"测过且没报"——那是编造。
* **两个变体都认**：gcc 的完整报错是 `unrecognized command-line option`，缩写形态是
  `unrecognized option`；只认其一会在别的工具链上漏判（已用测试锁住，见 §8）。
* **原命中判定原样保留**：unknown 拦截是**前置**的一道闸，`"unsequenced" in low` 一字未动——
  在认得 `-Wunsequenced` 的编译器（clang++ / gcc≥14）上行为不变。
* 模块 docstring 增加了 673u 说明与 pre-673u / post-673u 版本标记（注释，不影响判据指纹）。

---

## 3. FD 基线重算：82.9% / 62.5% **不变**，对照假阳性 2 → 0

重跑链：`holdout_reveal_3_665.py` → `holdout_reveal_4_671a.py` → `holdout_reveal_5_672h.py`（各 3 回合）。

| 指标 | 修复前（pre-673u） | 修复后（post-673u） | 变化 |
|---|---|---|---|
| holdout 检出率 | 34/41 = **82.9%**（CP95 [67.9, 92.8]） | 34/41 = **82.9%**（CP95 [67.9, 92.8]） | **无变化** |
| corpus 检出率 | 40/64 = **62.5%**（CP95 [49.5, 74.3]） | 40/64 = **62.5%**（CP95 [49.5, 74.3]） | **无变化** |
| holdout 对照假阳性 | **2/11 = 18.2%** | **0/11 = 0.0%** | **−2** |
| reveal_3（665）对照假阳性 | 1/9 | 0/9 | −1 |
| reveal_4（671a）对照假阳性 | round4 1/2、cumulative 2/11 | round4 0/2、cumulative 0/11 | −1 / −2 |

**为什么任务书担心的"82.9%/62.5% 偏高"不成立（重要，如实登记）：**

1. **holdout**：被指派 `wunsequenced` 的只有 **h3 与 h35 两条，而它们都是 `planted=false` 的对照样本**
   （不是真错）。检出率的分母是 `planted=true 且 verdict∈{catch,miss}` ⇒ 这两条**从来不在分母里**。
   它们造成的污染在**对照假阳性**那一栏（control false_positive 2/11），不在 82.9% 里。
2. **corpus**：`expected_detector=wunsequenced` 的 4 条（d3-08/09/29/30）走的**不是** `rv661.detect`，
   而是 `external_corpus_662.detect` —— 那条路径的命中判定是 `"warning:" in ln`（只认真正的告警行），
   编译器报的 `error: unrecognized ...` 不含 `warning:` ⇒ 这 4 条一直是 **miss**，从未被 bug 抬高。

**逐样本回归核对（可复现性）**：三份 holdout 明细（30 + 40 + 60 = 130 行）修复前后逐位对比，
**verdict 变化只有 h3、h35 两条（catch → unknown），其余 128 行逐位一致**。
也就是说：sanitizer / tsan / ubsan / cross-compile / linker 的全部历史判决在今天的机器上原样复现。

---

## 4. 840 次真实矩阵重跑（`detect_for_assets.py --dataset both`）

| 资产 | holdout 旧 catch | holdout 新 catch | corpus 旧 catch | corpus 新 catch |
|---|---:|---:|---:|---:|
| asan | 26 | 26 | 25 | 25 |
| tsan | 13 | 13 | 18 | 18 |
| ubsan | 11 | 11 | 23 | 23 |
| compiler-warn | 4 | 4 | 17 | 17 |
| cross-compile | 2 | 2 | 8 | **7** ⚠ |
| linker | 1 | 1 | 1 | 1 |
| compile-time | 0（恒 unknown） | 0 | 0 | 0 |
| **wunsequenced** | **41** | **0**（恒 unknown） | **64** | **0**（恒 unknown） |

* **其余 7 资产 × 105 样本 = 735 个判定中，只有 1 个变化**：`d3f-10 × cross-compile` catch → miss。
  这**不是**本修复造成的——673r 报告 §4.8 已登记"同一批样本两次全量实测，唯一差异是 d3f-10 的
  cross-compile"，本次重跑再次踩中同一个已知不稳定点（g++/clang++ 运行输出差分的环境敏感）。
* **保真率**（本批单回合一轮 vs 672h 三回合冻结记录）：holdout **41/41 = 100%**；corpus **57/64 = 89.06%**。
  corpus 的 7 条不一致 = 4 条 wunsequenced（冻结 miss → 现在的 **unknown**，这是修复的**正确**结果）
  + 3 条 asan（d3-21/22/25，冻结 miss → 本批 catch，673r 已登记为"1 回合 vs 3 回合口径差异"）。
* **耗时**：wunsequenced holdout 41 次 1.56s（0.038s/次；修复前 1.3s，0.032s/次）——
  多的那一次子串检查没有可测影响。全量 holdout 413s / corpus 600s（673r 为 266s / 397s，
  差异来自本批与其他批次并发抢 CPU，与修复无关）。

---

## 5. A5 重跑：主端点首次显著，但 holdout 触发 `uninterpretable` 条款

重跑 `tools/run_a5_experiment_673p.py`（真实段；replay 段逐位同口径未动）。
口径：派生集估 fail_hits（不含评估集信息）→ 评估集（holdout n=20 / corpus n=16）上比三臂，主预算 k=4。

### 5.1 主分析（预注册 8 项候选，不剔除任何资产，k=4）

| | pre-673u（673r） | **post-673u（本批）** |
|---|---|---|
| holdout FD | 100.0% (20/20) | **90.0% (18/20)** |
| holdout Random（seed 20260930） | 100.0% (20/20) | **35.0% (7/20)** |
| holdout Static | 100.0% | **10.0% (2/20)** |
| **holdout Δ(FD−Random)** | +0.00pp，CI [0,0]，**p=1.0000**（b=0,c=0） | **+55.00pp**，CI [+33.20, +76.80]，**p=0.00098**（b=11,c=0），h=1.232 |
| **holdout Δ(FD−Static)** | +0.00pp，p=1.0000 | **+80.00pp**，CI [+62.47, +97.53]，**p=3.05e−05**（b=16,c=0） |
| corpus FD | 100.0% (16/16) | **81.25% (13/16)** |
| corpus Random | 100.0% (16/16) | **37.5% (6/16)** |
| corpus Static | 100.0% | **37.5% (6/16)** |
| **corpus Δ(FD−Random)** | +0.00pp，**p=1.0000** | **+43.75pp**，CI [+13.90, +73.60]，**p=0.0391**（b=8,c=1），h=0.928 |
| Random 2000 次分布（holdout） | 均值 79.62%，FD 严格更优 **52.1%** | 均值 **55.04%**，FD 严格更优 **93.75%** |
| Random 2000 次分布（corpus） | 均值 79.17%，FD 严格更优 **52.1%** | 均值 **53.73%**，FD 严格更优 **95.8%** |

k 扫描（主分析，探索性）：holdout 在 k=1..5 全部 p≤0.00098、k=6/7 p=0.0156、k=8 退化（Δ≡0）；
corpus 在 k=4 p=0.0391、k=2 p=0.0703、k=5 p=0.0625。

### 5.2 预注册判定表（照抄 673r 条款逐条对）

| 条款 | 结果 |
|---|---|
| `primary_pass`：holdout p<0.05 且 Δ>0 | ✅ p=0.00098，Δ=+55.00pp（**673r 时为 ❌**） |
| `secondary_pass`：corpus p<0.05 且 Δ>0 | ✅ p=0.0391，Δ=+43.75pp（673r 时为 ❌） |
| `uninterpretable`：主分析 Δ 完全由退化资产驱动（并列分析中消失或反号） | ⚠ **holdout 触发**：并列分析里 Δ=**0.00**（消失）。corpus 不触发（并列分析 Δ=+31.25pp，同号） |
| `not_significant` / 扩样 | 不适用（显著了），但 n=20/16 ≪ 138 的功效缺口**依旧存在** |

**⚠ 必须并报的读法（不许只报显著）**：

主分析里 Random 的 k=4 子集是 `{wunsequenced, cross-compile, tsan, compile-time}` —— 其中
wunsequenced（现在恒 unknown）与 compile-time（恒 unknown）是**零信息资产**，Random 抽到它们
等于白扔一半预算；FD 靠派生集 fail_hits（wunsequenced=0、compile-time=0）天然避开。
**所以 holdout 的 +55pp 主要来自"FD 不浪费预算"，是池构成效应，不是"FD 在有用资产里挑得更准"。**
证据：剔除退化资产后的并列分析（5 候选）里，Random 也拿到 90.0%，Δ 掉到 **0.00**（p=1）。
按 673r 预注册 `decision_thresholds.uninterpretable`，**不得据此单独宣称 FD 优于 Random**。

corpus 的信号更干净一点：并列分析（6 候选）Δ=+31.25pp（CI [+2.69, +59.81]）与主分析同号、
未消失，但 p=0.125 不显著。

### 5.3 并列分析与敏感性视角

| 口径 | pre-673u | post-673u |
|---|---|---|
| holdout 并列（5 候选，k=4） | FD 90.0% / Random 90.0%，Δ=0.00，p=1.0000 | **逐位相同**（候选集未变：`{asan,compiler-warn,linker,tsan,ubsan}`） |
| corpus 并列（6 候选，k=4） | FD 81.25% / Random 56.25%，Δ=+25.00，p=0.2188 | FD 81.25% / **Random 50.0%**，Δ=**+31.25**，p=0.125（Random 的变化来自 d3f-10 cross-compile 的已知不稳定，见 §4） |
| holdout 敏感性（只剔恒 catch，7 候选） | FD 90.0% / Random 30.0%，Δ=+60.00，p=0.0005 | **skip**（已无恒 catch 资产 ⇒ 该视角前提不再成立） |
| 退化资产标记 | holdout：wunsequenced(100%)、compile-time(0%)、cross-compile(0%)；corpus：wunsequenced(100%)、compile-time(0%) | **同一组集合**；wunsequenced 从 100% 形态变 0% 形态（仍按预注册规则标记） |

---

## 6. 其他守护产物重跑结果（逐项）

| 产物 | 命令 | 结果 | 变化 |
|---|---|---|---|
| 变异测试 core | `python tools/mutation_test_656.py --scope core --limit 300` | **96.5%**（147 变异体，杀 110 / 存活 4 / 导入崩 29 / 超时 4） | **逐位一致** |
| 变异测试 all | `python tools/mutation_test_656.py --scope all --limit 300` | **81.8%**（223 变异体，杀 130 / 存活 29 / 导入崩 61 / 超时 3） | **逐位一致** |
| E9 外部工具对比（FD 侧） | 现算复算（生成器是 673e 的临时脚本，不在 `tools/`） | FD holdout 34/41=82.9%、corpus 40/64=62.5%，六层分解与 `data/673e_comparison_stats.json` 的 `layers` **逐项一致** | 无需重算 |
| llm_arm_672i | `python tools/llm_arm_672i.py --run`（20/20 全缓存命中，0 次 API 调用） | LLM 12/12=100%、FD 6/12=50%、Δ=−50pp、FP 4/8、McNemar b=0 c=6 p=0.0312 | **指标逐位一致**；仅 `generated_at` 与逐条 `note: api→cache` 变化 |
| guard_rerun_671a | `python tools/guard_rerun_671a.py` | **overall=PASS，18/18 OK**（block=0，warn=0），三方数字一致 4/4（82.9% / 62.5% / 96.5% / 67 条） | 重跑后 4 个检测器为 RERUN（改了也重跑了）⇒ `--init` 重标定 |
| quality 门禁 | `python tools/cppbible.py check --stage quality` | **27 passed / 0 failed**，exit 0 | 无 |
| tool_integrity | `python tools/tool_integrity.py --check` | **exit 0**（5 核心工具 + 6 信任根数据 + Merkle 根 + 22 尺子全一致） | **无需重钉**（§7） |
| fast_gate 默认档 | `python tools/fast_gate.py --tests tests/test_wunsequenced_fix_673u.py tests/test_detect_for_assets_673r.py --skip-frontend` | **overall=PASS**（pytest 7.8s + 658 + 669d + 671a guard） | 无 |

**三方一致性**（产物 ↔ 论文 ↔ 前端）修复后仍是 4/4 CONSISTENT——因为 82.9% / 62.5% / 96.5% / 67 条
这四个数**一个都没变**。control_false_positive 不在三方对账清单里（`data/guard_artifacts_671a.json` 只绑
holdout rate / corpus rate / mutation core / rules_total 四项）。

---

## 7. tool_integrity：**无需重钉**（与任务书假设不同，如实登记）

任务书预期"detect() 改了 ⇒ `tools/.tool_checksums` 里 holdout_reveal_661.py 的哈希会变"。
实测：**`holdout_reveal_661.py` 根本不在完整性校验面里**——

* `CORE_TOOLS` = gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible（5 个，无 661）；
* `TEST_CONFIG_TOOLS` = tests/conftest.py + pyproject.toml；
* `SUPPLY_CHAIN_FILES` = 毒样例台账 / 治理 manifest / Merkle 根 / layout / OTS（6 个）；
* `RULER_TOOLS` = 22 个判决尺子（`mutation_fuzz.py`、`golden_lock.py`…，无 661）；
* 目录级 Merkle 根的 COVERED_DIRS 也不含 `tools/` 下的这个文件。

⇒ `grep -c holdout_reveal_661 tools/.tool_checksums` = **0**；修复后 `--check` 实测 **exit 0**。
**处置：不重钉、不改 `.tool_checksums`。**（若未来要把检测器判据纳入哈希面，属独立批次——
那会改变"改判据必须显式留痕"的覆盖范围，不该顺手在本批做。）

---

## 8. 新增测试

`tests/test_wunsequenced_fix_673u.py`（8 条，全绿，秒级，不碰 WSL）：

1. `test_wunsequenced_is_unknown_not_catch` —— 修复后必须是 unknown；
2. `test_wunsequenced_note_names_the_root_cause` —— note 必须写明"不可用"与 `-Wunsequenced`（不许静默）；
3. `test_wunsequenced_unknown_is_not_counted_as_miss_or_catch` —— 四态互斥；
4. `test_source_keeps_both_unrecognized_variants` —— 两个报错变体都要认；
5. `test_source_keeps_original_hit_predicate_after_the_guard` —— **红线**：原命中判定必须原样保留；
6. `test_source_keeps_two_tier_opt_levels_and_setarch` —— 双档 / setarch -R / TSan 判定未动；
7. `test_other_local_assets_verdicts_unchanged` —— compiler-warn / linker 行为级不变；
8. `test_detect_signature_unchanged` —— 与 673r 守卫同款（2 元签名）。

连同受影响测试一起跑：`tests/test_wunsequenced_fix_673u.py + test_detect_for_assets_673r.py +
test_expand_672h.py + test_reveal_671a.py + test_drift_guard_668.py` = **93 条全绿**。

---

## 9. 环境陷阱（本批踩到并绕过，下次直接照做）

1. **WSL 横幅（必须设 `WSL_UTF8=1` + `WSLENV=WSL_UTF8/u`）**：本机 WSL 2.7.10 在 Windows 系统代理
   开启时，每次 `wsl.exe` 都向 stderr 写一条 UTF-16LE 横幅 ⇒ `subprocess.run(text=True)` 解码抛
   `UnicodeDecodeError` ⇒ sanitizer 报告（走 stderr）全丢 ⇒ **系统性假 miss**。实测（修复前 12:46 一次
   未设 env 的重跑）：h41 asan 判 **miss**（应为 catch）⇒ 那次运行在写任何产物前已中止作废。
   `reveal_3_665 / reveal_4_671a / reveal_5_672h` 三个工具都**没有** 673r 那套适配层，所以重跑它们
   **必须**先设 env（`detect_for_assets.py` 自带适配层，无所谓）。
2. **note 字段出现 WSL 横幅**（外观差异，如实登记）：672h 时代的落盘 note 不含横幅（当时无代理或
   WSL 版本不同）；本次重跑的 note 前缀多了
   `wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。`。
   **verdict 不受影响**（横幅不含任何命中关键字），已逐样本核对；但产物 note 与历史不再逐字节可比。
   治本（把 673r 的 L3 横幅剥离下沉成共享模块）属独立批次，本批不动 `detect()` 其他逻辑。
3. **`detect_for_assets.py --check` 在 ambient `WSL_UTF8=1` 下会红**：它的
   `[FAIL] 适配层卸载后 env 已还原` 断言假设 `WSL_UTF8` 初始未设。跑测试时**不要**带
   `WSL_UTF8=1`（本批 pytest 首跑就是这么红的，去掉后 93 条全绿）。该断言的环境敏感性属 673r
   代码，本批不改。

---

## 10. 局限性（诚实边界）

1. **n=20 / n=16 仍远低于 138 对的功效门槛**（`sample_size_reality_check`）。CI 很宽
   （holdout [+33.20, +76.80]），显著性不能当确认性点估计读；扩样到 n≥138 是唯一出路，属独立批次。
2. **holdout 主分析的 Δ 主要是池构成效应**（避开零信息资产），并列分析中消失 ⇒ 按预注册仍须报
   "不可解释"风险。**本批不宣称 FD 优于 Random。**
3. **单回合**：A5 真实段仍是 1 回合口径，与 672h 三回合冻结记录不可相减（673r 已登记）。
4. **`wunsequenced` 在本工具链下依然是"不可用"**：修复只是把"假装抓到"改成"诚实说不可用"。
   要让它真正工作，需要换 clang++ 判 `-Wunsequenced`，或升级 MinGW 到 ≥ gcc 14 —— 属独立批次。
5. **版本标记**：673u 之前的 reveal 记录为 **pre-673u**（wunsequenced 判决含恒 catch 污染），
   之后为 **post-673u**。跨版本比较 wunsequenced / control FP / A5 主分析时必须注明口径。
6. **d3f-10（cross-compile）** 的不稳定是既有问题，本批第三次复现，未修（不属本批射程）。

---

## 11. 论文待更新项（**本批不碰 research/**，等用户确认后由论文批次做）

| 位置 | 现状（pre-673u） | 需改成（post-673u） |
|---|---|---|
| control false positive（§6.4/§7 一带） | 2/11 = 18.2% | **0/11 = 0.0%**（并说明原因是检测器缺陷已修） |
| A5 主端点（§7/§10） | Δ=0.00pp、p=1.0000、判"不可解释" | Δ=+55.00pp / p=0.00098（holdout）、Δ=+43.75pp / p=0.0391（corpus）；**必须并报** holdout 并列分析 Δ=0 ⇒ `uninterpretable` 条款仍触发 |
| A5 随机分布位置 | FD 严格更优 52.1% / 52.1% | **93.75% / 95.8%** |
| 全池 OR 检出 | 41/41、64/64（100%） | 35/41（85.4%）、54/64（84.4%） |
| 逐资产命中表（§4.2/§7） | wunsequenced 21/21、48/48、41/41、64/64 | 全部 0（恒 unknown，检测器不可用） |
| `673r_a5_preregistration.json` | — | 已追加 `post_hoc_amendments[0]`（未动任何锁定字段） |

---

## 12. 复算命令

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible

# 0) bug 本体（本地 g++ 不认 -Wunsequenced）
g++ -std=c++17 -Wall -Wextra -Wunsequenced -fsyntax-only Examples/atoms/_atom_eval_order.cpp
python -c "import importlib.util as u; s=u.spec_from_file_location('r','tools/holdout_reveal_661.py');\
m=u.module_from_spec(s); s.loader.exec_module(m); print(m.detect('wunsequenced',['_atom_eval_order.cpp']))"
#   => ('unknown', '检测器不可用(wunsequenced)：编译器不认 -Wunsequenced（detector unavailable: ...)')

# 1) FD 基线重算（holdout 链，须先 export WSL_UTF8=1 WSLENV=WSL_UTF8/u）
python tools/holdout_reveal_3_665.py && python tools/holdout_reveal_4_671a.py && python tools/holdout_reveal_5_672h.py
python -c "import json;d=json.load(open('data/holdout_reveal_5_672h.json',encoding='utf-8'))['cumulative'];\
print(d['error_subset'], d['control_subset'])"
#   => error_subset {'catch': 34, 'miss': 7, ... 'detect_rate_pct': 82.9} | control_subset {'total': 11, 'false_positive': 0}

# 2) 840 次真实矩阵（自带适配层，无需 env）
python tools/detect_for_assets.py --dataset both

# 3) A5 三臂对照
python tools/run_a5_experiment_673p.py

# 4) 守护产物
python tools/mutation_test_656.py --scope core --limit 300     # 96.5%
python tools/mutation_test_656.py --scope all  --limit 300     # 81.8%
python tools/llm_arm_672i.py --run                             # 全缓存命中
python tools/guard_rerun_671a.py                               # 18/18 OK
python tools/cppbible.py check --stage quality                 # 27/27
python tools/tool_integrity.py --check                         # exit 0
python tools/fast_gate.py --tests tests/test_wunsequenced_fix_673u.py tests/test_detect_for_assets_673r.py --skip-frontend
```
