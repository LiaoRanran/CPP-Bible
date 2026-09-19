# _worklog_574 · 续包：修 M5 尺子 + v3 基线 / 放权门接口

> 任务书：`References/architecture_架构演进/574_续包_修M5尺子_v3基线_放权门接口_阴面样板.md`
> 承接：`d79a4a7`（573）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。
> **停在任务边界**：**E、D 完成并提交**；**C（V-iso 阴面 3 张）未开工**（见 §6）。

## 0 · 任务 0（开工先量）

改动前 fresh：gate `63 条·141 (block=0 warn=136 advice=5)` · replay `confirm=56` ·
`tool_integrity --check` exit 0 · 验收脚本跑完 ⇒ 基线干净。（`_acc574.log`）

## 1 · 任务 E：M5 尺子 bug（根因、修法、修前修后）

**根因（与提示词判断一致，实测确认）**：`mut_m5` 用 `re.search(r"(?m)^(\s*)claim_type:\s*(\w+)\s*$", text)`
只取**全文第一个** `claim_type:`；原子卡的命题写在 `claim_structured:` 列表里，且 **prop-1 多为
observation** ⇒ 第一个命中就是 observation ⇒ `!= "observation"` 不成立 ⇒ **永远返回空** ⇒
29 条 inference 命题一条都改不到。**v2 实测 M5 = 0 blocked / 0 escaped / 83 n_a（全 n_a）**。

**修法**：
* 先定位 `claim_structured:` 块（`_claim_structured_span`，按缩进判块结束）⇒ **只改块内**，
  卡面顶层的 `claim_type` 不动（有锁）；
* 块内**每一行** `claim_type: inference` 各出一个**独立变体**，只改该行的值、其余逐字不动；
  变体描述带命题 id（回溯最近的 `- prop-id:` / `- id:`）；
* 纯函数、幂等、不改原卡（沿用其他算子范式）；块内无 inference ⇒ out_of_scope 单例（**不假装可判**）。

**修前 → 修后（实跑）**：

| | 修前（v2） | 修后（v3 全量） |
|---|---|---|
| M5 | blocked 0 / escaped 0 / **n_a 83** | blocked 0 / **escaped 29** / n_a 56（判了 29） |

**29 条全部逃逸 = 真洞，只登记不补规则（按硬纪律）**：inference 命题被自标成 observation 后，
530 T3 的 **OBSERVATION-LIVENESS 闸完全没有反应** ⇒ "改个标签就能把推断类命题伪装成观测类命题"。
工具自身已把它标成 `rate_flags: M5：**活雷** —— 逃逸 29/29（区间 [88.06%, 100.00%]）`。
**本批不替它补规则**，逐条登记，交下一批（见 §7）。

## 2 · 任务 E：v3 全量基线 + metrics 时点

`data/mutation/full_baseline_v3.json`（966s / 1183 变体 / 83 卡，全 7 算子）：

| 算子 | v2 (b/e/n_a) | v3 (b/e/n_a) | 可判 | 逃逸率 95% C-P |
|---|---|---|---|---|
| M1 | 64/1/27 | 64/1/27 | 65 | 1/65 = 1.5% [0.04%, 8.3%] |
| M2 | 168/0/27 | 168/0/27 | 168 | 0% [0, 2.2%] |
| **M3** | 13/**52**/42 | **65/0**/42 | 65 | **0% [0, 5.5%]**（572 收口生效） |
| M4 | 200/0/33 | 200/0/33 | 200 | 0% [0, 1.8%] |
| **M5** | **0/0/83** | **0/29/56** | 29 | **29/29 = 100% [88.1%, 100%]（活雷）** |
| M6 | 324/8/0 | 324/8/0 | 332 | 8/332 = 2.4% [1.0%, 4.7%] |
| M7 | 139/0/0 | 138/0/1 | 138 | 0% [0, 2.6%] |

**总体逃逸率（metrics 时点升 v3）**：**38/997 = 0.038114**，C-P95 **[0.027111, 0.051942]**
（v2 是 61/969 = 6.3%，v1 是 227/956 = 23.7%）；**v1 / v2 保留为历史时点，不覆盖**。

回归锁 5 例（`tests/test_m5_operator.py`）：每 inference 命题一变体 / 只改那一行 / 不动顶层
claim_type / 纯 observation ⇒ out_of_scope / 纯函数且无块返回空。

## 3 · 任务 D：信任放权门（只写不读、默认不放权）

* `data/oracle_registry.json`：当前认可的 oracle 版本（gcc 15.3.0 / gate_engine / atom_evidence_replay）+ delegation 开关。
* 卡/命题 frontmatter 可选 `verified_by_oracle:`（oracle / version / verified_at / scope）——纯记录。
* **只写不读硬不变量**：`oracle_report()` 只在**报告层**做统计与 stale 标记；
  **gate/replay/poison 的判决逻辑一律不读该字段**。
* 回归锁 4 例（`tests/test_oracle_gate.py`）：
  ① **填了 `verified_by_oracle`（含"没人认可的 99.0.0"）⇒ gate 命中集合逐字不变**；
  ② 复算 verdict 不变（EV-CONC-001 confirm→confirm）；
  ③ 报告层 stale：版本对上不 stale、对不上/不在册 ⇒ stale、没填 ⇒ 记 missing_field；
  ④ 放权开关（G-iso / oracle_auto_accept / llm_as_judge）代码与 registry **双处全 OFF**。

## 4 · 收工验收（fresh）

| 项 | 实测 |
|---|---|
| gate | `63 条 · 141 (block=0 warn=136 advice=5)` —— 与基线**逐字相同**（存量零误伤） |
| poison | `114/114` |
| replay | `confirm=56 refute=0 infra_error=0` |
| `tool_integrity --check` | exit 0 |
| ruff（启用族） | **All checks passed!** |
| pytest fast `-n auto` | **exit 0** |
| 受控目录 | `git diff --quiet -- evidence/ atoms/` exit 0 |
| E | M5 修前 0/0/83 → 修后 0/29/56；v3 落盘；metrics 时点 = 38/997 |
| D | 只写不读锁绿（gate 集合 + replay verdict 逐字不变）、stale 仅报告层、开关全 OFF |

（本批**未**复跑 slow 组；改动涉及的 targeted 用例（M5 / 曲线 / overturned / oracle）与 fast 全绿。）

## 5 · 偏差表

1. **我误把 ruff 的退出码当成 pytest 的**：一次提交时 `$LASTEXITCODE` 已被 ruff 覆盖（=0），
   于是**带着一条红测提交**（`de68119`），随后查清并补提交修正（`81d6d3b`）。已如实留痕。
2. **我新用例里两处低级错误**：① 断言"变体里不该再有 inference"——但**别的** inference 命题本就该保留
   ⇒ 改为"比原卡少一个 inference / 多一个 observation"；② 测试里误用 ASCII 引号导致语法错 ⇒ 修。
3. **M5 单算子跑与全量跑的严格数不同**（单算 3 blocked / 全量 0 blocked、29 escaped）：
   以**全量 v3 为准**（单算子那次是过程测量，未采信）。
4. **任务 E 拆成两个 commit**（实现 + 曲线用例数字更新）+ **D 拆两个**（实现 + 新代码告警清理）：
   均为同一任务的收尾，分开便于 review。
5. **C 未开工**（见 §6）。

## 6 · 停在任务边界：C（V-iso 阴面 3 张）未开工

本批预算被 **E 的 v3 全量（966s，含两次等待）+ D 的接口与锁 + 若干测试修正** 消耗殆尽，
按任务书"做不完停任务边界、不留半成品"，**C 一行未动**：没有挑卡、没有造阴面、没有提交。

## 7 · 交下一批

* **最高优先**：M5 的 29 条"活雷"（inference 自标成 observation 无人察觉）⇒ 设计
  **OBSERVATION-LIVENESS 的补强**（先量后动、warn 起步、不硬凑）。登记条目见
  `data/mutation/full_baseline_v3.json` 的 M5 escaped 列表（29 条，带命题 id）。
* **C**：57 卡只有 EV-CONC-001 有真阴面；19 张 run_match 卡是候选池，只挑 3 张、判据一条不降，
  每张独立 commit + replay 翻转留证；结构性做不出单变量运行级阴面的卡（如纯存在性卡）登记。
* 其余冻结项：自动 KG / LLM-as-judge / 自动 LLM 推翻 / PoC#3/#4/#5 / golden fork / 测试按卡裁剪
  / 给全 56 卡硬塞阴面 / ruff 其余噪声族。
