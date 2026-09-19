# 588 建设包 · 变异「发现器」完备性：matrix 尾注释漏网收口 + 读取面诚实化 + 全算子卡面形态审计

> 角色：你是机械建设苦力。严格按本任务书执行，不自由发挥、不扩范围。
> 铁律不变：**先量后动、存量零误伤、一任务一 commit、正反例回归、改 CORE 必须同 commit `--update` 重钉、跑多少报多少、取证用 `$LASTEXITCODE`、poison/replay/工件指纹类串行勿并发。**
> 全程不 push、不 golden accept、不替人签。做不完停在任务边界，不留半成品。

## 本批定位（先读懂，决定了你什么能碰、什么不能碰）

这是**发现器/尺子侧**的一批，不是门禁硬化批。586→587 一路在堵「门禁漏判」，本批反过来查「**变异器有没有把该问的毒问题问出口**」——
即变异正则/解析对真实卡面的各种**合法书写形态**是否都能产生变体。一个该产生却没产生的变体，等于攻击集里少了一颗子弹，会让逃逸率被**低估得心安理得**。

**硬边界（违反即越界）：**

- 本批**原则上零判决规则改动**：不碰 `tools/gate_engine.py` 的任何 check、不碰 `atom_evidence_replay.py` 判决、不碰 `poison_drill.py`。
  主改文件预期只有 `tools/mutation_fuzz.py`、新增只读审计脚本/台账、`tests/`。
  `mutation_fuzz.py` **不在 CORE_TOOLS**（CORE 是 gate/replay/poison/toolchain/cppbible），故本批**预期无需 `tool_integrity --update` 重钉**；
  若你发现某处非改 gate 不可，**停下**，在 worklog 登记卡 id/算子/点/期望判决，交人，**不得擅自加规则**（加规则=另一个 warn 起步批）。
- 本批**不加 poison 毒载荷（P 编号）、不改 `tools/poison_surface_map.json`**。因此收工时 poison 台账与 syrupy 快照
  （`tests/__snapshots__/test_output_snapshots.ambr`）必须**逐字不变**；一旦它们变了，说明你越界碰到了呈现层，立即回滚并查原因。
  （这是 587 快照漏同步教训的反向利用：本批它们本就不该动。）
- 新补出来的变体若实跑**逃逸**：**只登记、不补规则、不洗成 equivalent**，逐条进 worklog 交人。
- **M1 那条 TCE 逃逸（当前全量唯一 escaped=1，删 negative_controls，需工件比对）继续冻结，本批严禁碰。**
- 尾注释/CRLF 等是**合法 YAML 形态**（仓内硬化 loader 与 replay 解析器本来就能读，见
  `tests/test_atom_evidence_replay.py:45`「flow 序列 + 尾注释剥离」、`tests/test_p0d_hardening.py:75` 的 `matrix:   # 注释行`）。
  所以本批定性是「**发现器正则没跟上合法语法**」，**不是卡写错了**——禁止去改任何卡面来迁就正则。

## 0. 背景与豆包已侦察的根因（已实测，直接用，不必重新定位）

### 0.1 必修漏点：`matrix:` 键行尾注释导致 M6 对该卡 0 变体

- 发现器 `tools/mutation_fuzz.py::_mut_matrix_values()`（当前约 432 行）用这条正则定位 matrix 块（约 441 行）：

  ```python
  m = re.search(r"(?m)^(matrix:)\s*\n((?:  [^\n]+\n)+)", text)
  ```

  它要求 `matrix:` 键行之后**只能是空白再换行**，且子行缩进**写死两个空格**。
- 真实卡 `evidence/mem/EV-MEM-004.md` 的 matrix 段是（逐字摘录）：

  ```yaml
  matrix:                          # ⚠️ 笛卡尔声明 ≠ 实测组数：GCC 13.1 只跑了 {c++17 × -O2} 一组
    compiler: [GCC 15.3.0, GCC 13.1.0]
    # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
    std: [c++11, c++14, c++17, c++20, c++23]
    opt: [-O0, -O2]
    arch: [x86-64]
  fixture: Examples/atoms/_atom_named_rvalue.cpp
  ```

  两处让正则失配/易错：
  1. **键行带尾注释** `matrix:   # ⚠️…`：`\s*` 匹配空格后撞上 `#`，随后要求 `\n` 失败 ⇒ **整块匹配不到**
     ⇒ M6 对 EV-MEM-004 **既不产删键、也不产非法值变体（0 个 matrix 变体）**。587 worklog 偏差#5 已记「55/56 卡有删键变体」，漏的就是这张。
  2. **块内插了注释行** `  # Clang 列待…`：即使修好键行，该行也会被 `(?:  [^\n]+\n)+` 吃进 block；
     遍历时靠 `":" not in s` 侥幸跳过（此行无英文冒号），但这是**脆弱巧合**——注释里一旦出现冒号就会被误当成键。
- 尾注释是合法 YAML（解析器读得到、门禁判得了），所以这是纯粹的发现器盲区。

### 0.2 读取面诚实化：`GATE_READ_KEYS` 漏了 `matrix`

- `tools/mutation_fuzz.py:154` 的 `GATE_READ_KEYS` 元组列了门禁真读的顶层键（571 已补过同款漏网的 `actual`），
  但**不含 `matrix`**；而 `gate_engine.py::check_evidence_matrix()`（约 2901 行，`:2911 _meta(p).get("matrix")`）确实真读 matrix。
- 后果：`_gate_read_spans()`（约 165 行）不把 matrix 块划进门禁读取面，任何依赖「读取面内可弱化点」的判定
  都可能把 matrix 区域当成「门禁不读」，与 571 的 actual 是同一类「把没问记成不适用」的尺子不诚实。
- matrix 取值（编译器名/标准/优化级/arch）里没有文件路径后缀、也没有 contains_in/-Werror/count 等 M2/M3 目标，
  **预估补了对分类计数 0 影响**——但「预估」不算数，必须实跑逐变体 diff 证实（见任务 2）。

### 0.3 开工基线（先 fresh 复跑核对，再动手；数字以你实跑为准）

- gate：63 规则 / 191 命中（block=0 warn=186 advice=5）；poison 124/124、RULE-COVERAGE 39/63、表观 100% / 诚实 95.2%（60/63）；
  replay confirm=56/refute=0/infra=0；tool_integrity exit 0；fast 全绿（5 snapshots）。
- mutation 权威基线：先 `git ls-files "data/mutation/full_baseline_*.json"` 找到最新权威文件（587 重冻结后约为
  **1568 变体 / blocked 1374 / escaped 1 / n_a 185 / strict 784 / 可判分母 1375**；文件名与数字以磁盘实测为准，不许凭记忆）。
  读它的逐算子计数（M1..M7 的 blocked/escaped/n_a）作为修前对照锚点。
- 工作树有两条开工前即存在的 CRLF 假脏（`data/mutation/full_baseline_v4.json`、`evidence/conc/EV-CONC-001.md`，内容 diff 为空），
  **不要提交、不要还原、不要碰**。

---

## 任务 0 · 先量（只读，不落任何规则/不改发现器）

### 0a 坐实尾注释漏网（修前证据）

1. 全量扫 `evidence/**/EV-*.md` 与 `atoms/**/*.md` 的 frontmatter，统计：
   - 有多少张卡含 `matrix:` 块；其中 **matrix 键行带尾注释**（`matrix:` 与换行之间有 `#…`）的卡，逐张列 id；
   - matrix **块内出现注释行**（缩进行以 `#` 开头）的卡，逐张列 id；
   - 对每张含 matrix 的卡，调用当前未修改的 `_mut_matrix_values()`，记录产出的变体数。
     预期：干净键行卡产出「删键 3 + 非法值 4」量级，尾注释卡（已知 EV-MEM-004）产出 **0**。
   - 给出「能产 matrix 变体的卡 / 含 matrix 的卡」比值（修前预期 55/56，以你实测的卡总数为准）。
2. 这一步只读数、打印/落台账，不改任何代码。

### 0b 全算子 × 卡面形态覆盖审计（本批「大」的主体，只读）

1. 新增**只读、幂等、纯标准库**脚本 `tools/mutation_shape_audit.py`（不 import scipy/numpy/pandas，仓内没装）：
   遍历真实卡 frontmatter，对 M1–M7 每个变异点，核对它的正则/解析能否覆盖下列**合法书写形态**（按实际遇到的增补，不要硬凑）：
   - 键行/值行**尾注释**（`key: … # 注`）、块内**整行注释**；
   - **flow 序列** `[a, b]` vs **块式序列**（`- item`）、flow 映射 `{k: v}`；
   - **全角括号/符号** `（）：，`、行内并列 `/`、单/双引号包裹的列表项；
   - **嵌套块**（如 `claim_structured:` 列表内的字段，M5 已处理过一类）、折叠标量 `>` / `|` / `>-`；
   - **缩进深度不一致 / Tab 与空格混用**、键行前后多余空格；
   - **CRLF（`\r\n`）vs LF（`\n`）行尾**（单列，见 0c）；
   - 空值 / 缺失可选键（如 `stdlib` 可选）。
2. 产出台账 `data/mutation_shape_coverage.md`（机器生成、只读），每行一个「算子 × 变异点 × 形态」格子，字段：
   `算子 | 变异点 | 目标字段 | 卡面形态 | 真实卡例(id，至少1个) | 现正则能否变异(能/漏) | 漏网证据(卡id+行号+为什么正则没中)`。
   **漏网格子必须给可复核的卡 id 与行证据**，找不到真实卡例的形态标「库内未出现」，不许编。
3. 给脚本配最小 pytest（新文件 `tests/test_mutation_shape_588.py`）：脚本对固定夹具卡幂等（连跑两次输出逐字相同）、
   纯只读（跑前后 `git diff --quiet -- evidence atoms Examples` exit 0）。

### 0c CRLF 子审计（可复现性，与 579 非确定性同源）

1. 统计 `evidence/`、`atoms/` 下卡文件的行尾分布（LF / CRLF / 混合），给数量。
2. 若存在 CRLF 卡：构造/选取「LF 版与 CRLF 版同内容」的一对卡，分别跑各 MUTATORS，比对**变体集合是否逐字相同**
   （注意现有正则大量用 `\n` 与 `ln + "\n"` 做切片/替换，CRLF 下行尾带 `\r`，可能静默少产或产错）。
3. 只记录结论：哪些算子在 CRLF 下变体集与 LF 不一致；一致则明确写「CRLF 无影响」并给证据。修放在任务 3。

> 任务 0 独立 commit（审计脚本 + 台账 + 0a/0c 读数写进台账或 worklog）。此 commit 不改判决、不改发现器行为，门禁数字应逐字不变。

---

## 任务 1 · 修 M6：matrix 键行尾注释 + 块内注释行（发现器补全，核心）

1.1 改 `_mut_matrix_values()` 的块定位与遍历，要求：

- **键行允许尾注释与行尾空白**：把 `^(matrix:)\s*\n` 放宽为能匹配 `matrix:`、`matrix:   `、`matrix:   # 任意注释` 三种形态后再换行
  （形如 `^matrix:[ \t]*(?:#[^\n]*)?\n`，以你实测能覆盖三种形态且不误伤正文同名行为准）。
- **子行缩进不要写死两空格**：块体改为「连续的、缩进深于顶格（行首至少一个空格/Tab）的行」，遇到下一个**顶格键**
  （如 `fixture:`/`command:`/`verdict:`）或 `---` 自然终止（形如 `(?:[ \t]+[^\n]*\n)+`，但务必验证不会多吃到后续顶格键）。
- **遍历时先剥尾注释再解析键**：对每条子行先按 `#` 拆出注释（`s.split("#", 1)[0]`），剥后为空（纯注释行）则跳过，
  再做 `partition(":")`；避免注释里的冒号被当成 matrix 键。matrix 真实取值（编译器名/标准/优化级/arch）不含 `#`，
  但你必须加测试证明剥注释对**正常无注释行、值内含括号/斜杠的行**逐字无副作用。
- 删键仍只对 compiler/std/opt（arch 缺键门禁不拦，删它只造无意义变体，维持现状）；非法值替换四键逻辑与 `_illegal_value_line()` 不变。

1.2 **零误伤/无副作用是硬门**，用回归锁死：

- 对修前能产变体的那 55 张（或你实测数）干净卡：修后产出的 matrix 变体**数量与文本逐字不变**（不多不少）；
- 对尾注释卡（EV-MEM-004 及 0a 扫出的同类）：修后**从 0 变为正常产出**删键/非法值变体；
- 在 `tests/test_mutation_shape_588.py` 至少加：
  - ① 合成卡 `matrix:   # 尾注释\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]\n` ⇒ 断言传 compiler/std/opt 三个删键变体都生成；
  - ② 同卡块内插一行 `  # 注释：含冒号也不怕` ⇒ 断言该注释行**不**被当成键、不产伪变体，且 std/opt 变体仍在；
  - ③ 干净键行卡修前/修后变体集逐字相等（防「修尾注释顺手改了正常路径」）；
  - ④ CRLF 版与 LF 版同内容卡的变体集相等（若 0c 发现 M6 受 CRLF 影响，在此一并锁；不受影响也加一条记录无影响）。

1.3 全量量修后效果（`--cards all --limit 999 --operators M6 --jobs 4 --progress`，`--cards all` 不解除默认 limit，571 教训）：

- 逐卡确认现在「能产 matrix 变体的卡 / 含 matrix 的卡」应为 **N/N（不再漏尾注释卡）**；
- 新增的变体（EV-MEM-004 等）逐条看判决：**删键**应被 EV-MATRIX 以 block「缺键」拦、**非法值**应被 587 的值校验以 warn 拦
  ⇒ 预期**全部 blocked、0 新增逃逸**；
- 这些变体改变了解析后的 matrix 内容（少键 / 值变垃圾），**不是 583 的等价变异体**，绝不能被标进 equivalent；若被判 equivalent 是判据被绕过，停下报。
- 若出现任何**新增 escaped**：按硬边界只登记（卡/点/why）交人，不补规则。

1.4 独立 commit（发现器侧）。`mutation_fuzz.py` 非 CORE，不重钉；提交前确认 `gate_engine.py`/`poison_drill.py`/`atom_evidence_replay.py` 零 diff。

---

## 任务 2 · 读取面诚实化：`GATE_READ_KEYS` 补 `matrix`（先量 diff，再决定）

2.1 在 `GATE_READ_KEYS` 元组补 `"matrix"`，并在旁边加注释说明「check_evidence_matrix 真读此键」，口径与 571 补 actual 的注释一致。

2.2 **先量后动的硬要求**：分别在补前/补后各跑一次全量（同 `--cards all --limit 999 --jobs 4`，报告落不同临时文件），
  对结果做**逐变体 diff**（归一化沙箱临时路径后比对 verdict/kind/why/new_block/new_warn）：

- 若**零差异**（预估情形：matrix 里无 M2 路径、无 M3 弱化目标）：把「补 matrix 前后逐变体一致」写成一条回归锁
  （可对固定卡集断言 `_gate_read_spans` 现在包含 matrix 区间，但全量分类计数不变），注明这是**纯诚实化、零判决影响**；
- 若有变体从 `n_a(out_of_scope)` 变为可判（blocked/escaped）：**逐条**列出卡 id/算子/点/前后判决，
  变 blocked 的是修正漏判（注明「尺子修正，非回归」），**变 escaped 的只登记交人、不补规则**。
  不允许出现「总数对不上但说不清哪条变了」。

2.3 独立 commit（读取面清单 + 注释 + 回归）。同样不碰 CORE。

---

## 任务 3 · CRLF 健壮性 + 审计发现的其余漏网（封顶，做不完停边界）

3.1 **CRLF（若 0c 实测有影响才做）**：修对应 MUTATORS 的切片/替换正则，使 CRLF 与 LF 同内容卡产出**相同变体集**
（思路：行遍历对 `\r` 免疫，或统一在变异前按行处理、替换时保留原行尾；不要把整库文件改行尾）。配 LF/CRLF 同构对拍测试。
若 0c 证明无影响，本步跳过并在 worklog 写明「实测无影响」，不得为凑改动而改。

3.2 **0b 审计台账里的其余漏网格子**：只处理同时满足以下三条的，**最多 3 处**（按「影响可判样本数」从大到小取）：

  1. 形状明确、是合法 YAML（解析器读得到、门禁理论上判得到）；
  2. 补出变体后该变体被**既有规则**拦（blocked）——即纯发现器补全，不需要新规则；
  3. 能写出正反例回归。
  不满足②（补出会逃逸）的漏网，**一律只登记进 worklog「交人：潜在新逃逸」**，不在本批补规则、不改门禁。
  每条独立或合并 commit，commit message 写清补的是哪个算子的哪种形态、补出多少变体、判决分布。

3.3 超出 3 处或预算不足：剩余漏网格子保留在 `data/mutation_shape_coverage.md` 台账里（它本身就是交付），停在任务边界，不留半成品代码。

---

## 任务 4 · 收工总验收（fresh，串行，全部用退出码定论并贴出）

4.1 落修后全量基线 `data/mutation/full_baseline_v6.json`（`--cards all --limit 999 --jobs 4 --progress
  --selfcheck-determinism --selfcheck-equivalent`）：

- 与开工基线（0.3 的权威文件）逐算子对照，给出 M1..M7 的 blocked/escaped/n_a 修前→修后，**每一处数字变化都要能指到具体任务**
  （任务1 尾注释补 N 变体、任务2 读取面修正 M 条、任务3 …）；
- **escaped 总数必须仍为 1（M1 TCE，冻结）**；若 >1，新增项逐条是已登记交人的逃逸，不得隐瞒、不得洗成 equivalent/n_a；
- `--selfcheck-determinism` exit 0（同输入两次跑逐变体一致，579）；`--selfcheck-equivalent` exit 0（583 保守性自证）；
- root_fingerprint_ok=true、真实仓 `Examples/` 与 build 锁无副作用。

4.2 门禁与呈现层（证明本批没污染判决）：

- `tool_integrity.py --check` exit 0（本批没动 CORE，应直接过；若提示基准不一致，说明你误改了 CORE，回滚）；
- `gate_engine.py --check`：仍 **63 规则 / 191 命中（block=0 warn=186 advice=5）逐字不变**；
- `poison_drill.py`：仍 **124/124**、39/63、双指标 100%/100%；
- **`git diff --quiet -- tools/poison_surface_map.json tests/__snapshots__/` exit 0（本批特色反向锁：台账与快照必须零变化）**；
- `atom_evidence_replay.py --check`：confirm=56 refute=0 infra_error=0。

4.3 测试与卫生：

- `pytest -m "not slow" -n auto` exit 0（含新 `test_mutation_shape_588.py`；若新用例比对真实 Examples 指纹/跑 replay，
  按 580/583 教训归 conftest 的 SERIAL_EXTRA/replay_serial，别在 -n auto 下裸奔）；
- `pytest -m slow -n0` 除已知 `test_golden_lock_json`（golden warn 136→186 待人审 accept 的预期红）外全绿；
- 改动文件过 `ruff check`（启用族 E4,E7,E9,F,I001,FURB167）新增告警为 0；护栏/自检不许裸 `except Exception`（570 教训）；
- 受控目录 `git diff --quiet -- atoms evidence Examples` exit 0；
- 若 4.1 重冻结改变了冻结结论类测试（如 test_metrics_collector_curves / 某 FROZEN_CONCLUSIONS），按实测更新并在 commit
  注明「非回归：发现器补全新增可判变体」，**但要能逐变体解释，不许改测试凑绿**。

4.4 独立 commit（v6 基线 + 必要的冻结结论同步 + worklog）。

## 交人（不要自作主张）

- 任务 1/2/3 补出的任何**新增逃逸**：只登记卡 id/算子/变异点/why，不补规则、不改卡、不洗口径。
- 任何需要改 gate/replay/poison 才能收口的问题：停，登记，另开 warn 起步批。
- M1 TCE escaped=1：继续冻结，禁止碰。
- 不做：PoC#1/#3、585 冻结项（仓内第二锚、人签通道）、ruff 余族大清扫、golden accept、push、替人签 liveness/oracle。
- 两条开工前 CRLF 假脏（full_baseline_v4.json、EV-CONC-001.md）维持现状，不提交不还原。

## 交付汇报格式

逐任务给：commit 短 hash 与每 commit 改了哪些文件；
任务 0：含 matrix 卡总数 / 尾注释卡 id 清单 / 修前「能产变体卡/含 matrix 卡」比值、形态审计台账漏网格子数、CRLF 分布与结论；
任务 1：修前/修后 EV-MEM-004 等卡变体数（0→?）、新增变体判决分布（应全 blocked）、干净卡变体逐字不变的证据；
任务 2：补 matrix 前后全量逐变体 diff 结论（零差异 / 变化清单）；
任务 3：CRLF 是否改动、其余补了哪几处漏网（≤3）及各自变体判决，未处理漏网如何在台账留口；
任务 4：v6 逐算子计数与每处变化归因、escaped 是否仍=1、两个 selfcheck 退出码、门禁全套退出码与数字、
**poison 台账与快照零 diff 的证据**、fast/slow/ruff/受控目录结果；
偏差表（提示词假设 X / 实测 Y 逐条）。worklog 落 `_worklog_588.md`（不入库惯例）。
