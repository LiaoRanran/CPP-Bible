# 机械变异对抗测试报告（499 任务 7）

> 对象：5 张源卡 × 8 变异 = **40 个变异**，逐卡用 gate 实测是否触发对应 BLOCK。
> 源卡：EV-MEM-040 / EV-CONC-001 / EV-LANG-001 / EV-UB-001（证据卡，覆盖 mem/conc/lang/ub）
>       + ATOM-MEM-RAII-001（原子卡，测原子规则）。
> 变异：M1 删 artifact_sha256 · M2 verdict→confirm · M3 删 fixture · M4 artifact_version→99
>       · M5 run_match_keys 加 FAKE_KEY · M6 删 claim · M7 缩进走私 verdict · M8 artifact→不存在文件。
> **方法学（关键）**：早期版本给变异卡起唯一 id 会导致 `EV-ID-UNIQUE`（重复 id）、
> `ATOM-ID-FORMAT`（id 格式）、`EV-ARTIFACT-PRODUCER`（新卡缺 producer 字段）**全部误报**，
> 掩盖真实信号。修正为：**保留原 id + 测试时把原卡暂移走**，只留变异副本（原 id）在
> `evidence/_mut_tmp` 或 `atoms/_mut_tmp` 跑 gate，抓取该文件命中后立即恢复。这样命中的
> BLOCK 才是变异本身引起的。40 份变异卡归档于 `_mutation_test/`，`git status evidence/ atoms/`
> 跑完为 **0 改动**（铁律 #3：未改正式文件）。驱动脚本 `_mut_test.py`。

## 一、40 行实测结果

| # | 源卡 | 变异 | gate 反应 | 判定 |
|---|---|---|---|---|
| 1 | MEM-040 | M1 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 2 | MEM-040 | M2 | 仅基线 WARN（MATRIX-UNBACKED） | 放行（verdict 无影响，原卡 confirm） |
| 3 | MEM-040 | M3 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 4 | MEM-040 | M4 | BLOCK `EV-ARTIFACT-VERSION-MATCH` | 真拦 |
| 5 | MEM-040 | M5 | 仅基线 WARN | **放行（FAKE_KEY 未校验）** |
| 6 | MEM-040 | M6 | 仅基线 WARN | 放行（证据卡无 claim 字段，N/A） |
| 7 | MEM-040 | M7 | BLOCK `EV-FM-YAML-HARDENING` | 真拦 |
| 8 | MEM-040 | M8 | WARN（未登记路径）+基线 | **放行（工件不存在未 block）** |
| 9 | CONC-001 | M1 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 10 | CONC-001 | M2 | 仅基线 WARN | 放行（verdict 无影响） |
| 11 | CONC-001 | M3 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 12 | CONC-001 | M4 | BLOCK `EV-ARTIFACT-VERSION-MATCH` | 真拦 |
| 13 | CONC-001 | M5 | BLOCK `EV-FM-YAML-HARDENING`（**偶发**：插入破坏 YAML） | 真拦（非 FAKE_KEY 校验） |
| 14 | CONC-001 | M6 | 仅基线 WARN | 放行（无 claim 字段，N/A） |
| 15 | CONC-001 | M7 | BLOCK `EV-FM-YAML-HARDENING` | 真拦 |
| 16 | CONC-001 | M8 | WARN×3（未登记/符号映射/MATRIX） | **放行（工件不存在未 block）** |
| 17 | LANG-001 | M1 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 18 | LANG-001 | M2 | 仅基线 WARN | 放行（verdict 无影响） |
| 19 | LANG-001 | M3 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 20 | LANG-001 | M4 | BLOCK `EV-ARTIFACT-VERSION-MATCH` | 真拦 |
| 21 | LANG-001 | M5 | BLOCK `EV-FM-YAML-HARDENING`（**偶发**） | 真拦（非 FAKE_KEY 校验） |
| 22 | LANG-001 | M6 | 仅基线 WARN | 放行（无 claim 字段，N/A） |
| 23 | LANG-001 | M7 | BLOCK `EV-FM-YAML-HARDENING` | 真拦 |
| 24 | LANG-001 | M8 | WARN×2（未登记/MATRIX） | **放行（工件不存在未 block）** |
| 25 | UB-001 | M1 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 26 | UB-001 | M2 | 0 命中 | 放行（verdict 无影响） |
| 27 | UB-001 | M3 | BLOCK `EV-FM-REQUIRED` | 真拦 |
| 28 | UB-001 | M4 | BLOCK `EV-ARTIFACT-VERSION-MATCH` | 真拦 |
| 29 | UB-001 | M5 | 0 命中 | **放行（FAKE_KEY 未校验）** |
| 30 | UB-001 | M6 | 0 命中 | 放行（无 claim 字段，N/A） |
| 31 | UB-001 | M7 | BLOCK `EV-FM-YAML-HARDENING` | 真拦 |
| 32 | UB-001 | M8 | WARN×2（未登记/符号映射） | **放行（工件不存在未 block）** |
| 33 | RAII-001(atom) | M1 | 0 命中 | 放行（原子无 artifact_sha256，N/A） |
| 34 | RAII-001(atom) | M2 | 0 命中 | 放行（原子无 verdict，N/A） |
| 35 | RAII-001(atom) | M3 | 0 命中 | 放行（原子无 fixture，N/A） |
| 36 | RAII-001(atom) | M4 | 0 命中 | 放行（原子无 artifact/版本规则，N/A） |
| 37 | RAII-001(atom) | M5 | 0 命中 | **放行（FAKE_KEY 未校验）** |
| 38 | RAII-001(atom) | M6 | BLOCK `ATOM-FM-REQUIRED` | 真拦 |
| 39 | RAII-001(atom) | M7 | 0 命中 | 放行（原子无 verdict，N/A） |
| 40 | RAII-001(atom) | M8 | 0 命中 | 放行（原子无 artifact，N/A） |

## 二、汇总

- **真拦（变异本身触发的 BLOCK）：19 处**（含 CONC/LANG 的 M5 因插入破坏 YAML 偶发拦 2 处；
  若仅计"变异目标被精准拦截"则为 17 处：M1×4、M3×4、M4×4、M7×4、M6(atom)×1）。
- **放行：21 处**，拆为：
  - **真实门禁盲区：6 处** —— M5 假键（MEM-040 #5、UB-001 #29，纯逃逸；CONC/LANG 因偶发 YAML 拦
    不计入）+ M8 工件不存在（#8/#16/#24/#32，仅 WARN 未登记路径，未 BLOCK）。
  - **N/A（原子卡无对应字段）：7 处** —— #33/#34/#35/#36/#37/#39/#40（原子卡本无 artifact_sha256/
    verdict/fixture/artifact，M1/M2/M3/M4/M5/M7/M8 对其天然不适用）。
  - **N/A（证据卡无 claim 字段）：4 处** —— #6/#14/#22/#30（证据卡用 `hypothesis` 非 `claim`，
    M6 删 claim 对证据卡无效）。
  - **测试覆盖局限（M2）：4 处** —— #2/#10/#18/#26（5 张源卡 verdict 均为 confirm 或无 verdict 字段，
    `verdict→confirm` 是 no-op，无法验证"与 actual 矛盾的 refute 是否被拦"）。

## 三、真实门禁盲区（建议新增规则，超苦力权限）

1. **M5：run_match_keys 含不存在的键（如 FAKE_KEY）未校验**
   当前 `EV-OUT-UNDECLARED-KEY` 只查"`.out` 出现的键不在 `run_match_keys`"（反向）；
   `run_match_keys` 里声明了但 `.out`/工件根本不存在的键 **无人查**。攻击者可在 `run_match_keys`
   塞任意假键而不被拦（#5/#29 纯逃逸；#13/#21 仅因插入碰巧破坏 YAML 才被 `EV-FM-YAML-HARDENING`
   拦，与 FAKE_KEY 无关）。
   **建议规则**：`run_match_keys` 的每个键必须出现在对应 `.out` 的发射键中（反向校验），否则 block。

2. **M8：artifact 指向不存在的文件未校验**
   改 `artifact:` 为不存在路径，gate 只 WARN"台账未登记"（因路径不在 `artifact_versions.json`），
   **不 BLOCK**。工件缺失的真实拦截靠 replay 的 `artifact_absent`——但日常 gate 不跑 replay，
   故恶意/损坏卡指向缺失工件时 gate 放行（#8/#16/#24/#32 全放行）。
   **建议规则**：`EV-ARTIFACT-EXISTS`——`artifact` 字段指向的文件必须存在，否则 block（与 replay
   的 artifact_absent 形成双重保险）。

> ⚠️ 铁律 #3 禁止苦力改 `tools/*.py` / 增规则。以上两条为**建议**，交好模型裁决与实现。

## 四、N/A 与覆盖局限（非门禁缺陷，记录备查）

- **原子卡字段差异**：8 个变异中有 7 个对原子卡 N/A（原子卡无 artifact/fixture/verdict）。说明这 8 个
  变异本质是**证据卡**导向；原子卡仅 M6（删 claim）有意义。若后续要测原子卡变异，应另选针对原子的
  变异集（如改 `relations` 目标、改 `prerequisites` 等）。
- **M2 无 refute 源卡**：5 张源卡 verdict 均为 confirm（原子卡无 verdict）。`verdict→confirm` 对它们
  是 no-op，无法验证"把 refute 卡改成 confirm 是否触发矛盾 block"。建议后续补 1–2 张 refute 源卡
  重测 M2。
- **基线 WARN 干扰**：MEM-040/CONC-001/LANG-001 副本仍触发 `EV-MATRIX-UNBACKED`（基线 warn，见任务 2
  报告——规则 `_raw_without_actual` 误报），非变异引入，已在判定中剔除。

## 五、结论

40 变异中门禁对**结构/字段缺失类**变异（缺 sha、缺 fixture、版本漂移、YAML 走私、原子缺 claim）
拦截扎实（17–19 处真拦）；但对**语义一致性类**变异存在 2 个真实盲区：
① `run_match_keys` 假键未反向校验；② 工件文件缺失 gate 不拦（依赖 replay）。
另 11 处放行为"原子卡无对应字段 / 证据卡无 claim / 无 refute 源卡"的测试覆盖局限，非门禁缺陷。
`git status evidence/ atoms/` 跑完为 0 改动，符合铁律 #3。
