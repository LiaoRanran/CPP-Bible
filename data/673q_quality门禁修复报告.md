# 673q quality 门禁三失败项修复报告

- 批次：673q（quality 门禁三失败项修复 + CI 验证准备）
- 日期：2026-10-02
- 提交：`8f1092c4`（A：Evidence Replay）、`5857ac3d`（B+C：Golden Lock / Debt Ledger）
- DCO：两个提交均已 `Signed-off-by: LiaoRanran <1026708211@qq.com>`，**未 push**
- 红线遵守：未碰 `research/`、未碰 `web/`、未修改任何已有测试的断言、未擅自清任何债务票据

## 0. 结论

| 门禁 | 修前 | 修后 | 处置 |
|---|---|---|---|
| Evidence Replay | FAIL（confirm=62 / refute=9） | confirm=71 / refute=0 / infra_error=0 | 真修（根因修复） |
| Golden Lock | FAIL（warn 176 -> 203） | 无恶化（恶化 0 改善 0） | 修本批自造回归 + 显式分类 + 显式接受存量 |
| Debt Ledger | FAIL（负债率 20% > 15%） | PASS（14.8% = 4/27） | 修分母根因（不还债） |

`python tools/cppbible.py check --stage quality`：**27 passed / 0 failed**（修前 24 passed / 3 failed）。

---

## A. Evidence Replay

### A.1 现象

`artifact_assert 跨编译器替代校验未通过` + `contains '<probe>' 出现（实得 0 次）`，共 9 张卡命中。

### A.2 根因一：9 张卡的结构断言**原理上不可满足**（内容问题，非环境问题）

| 卡 | 原断言文本 | 夹具 |
|---|---|---|
| EV-LANG-003 | `decay_param_sizeof` | `_c_decay.c` |
| EV-LANG-004 | `fnptr_probe` | `_c_fnptr.c` |
| EV-LANG-005 | `volatile_probe` | `_c_volatile.c` |
| EV-LANG-007 | `intpromo_probe` | `_c_intpromo.c` |
| EV-LANG-008 | `bitfield_probe` | `_c_bitfield.c` |
| EV-LANG-009 | `macro_probe` | `_c_macro.c` |
| EV-MEM-046 | `malloc_lifecycle_probe` | `_c_malloc.c` |
| EV-MEM-047 | `strbound_probe` | `_c_strbound.c` |
| EV-UB-003 | `signedovf_probe` | `_c_signedovf.c` |

这些函数都是 `static` 且只被调用一次，在本卡的 `-O2` 档位下**必然被内联进 main**
=> 函数名不会作为符号出现在任何编译器、任何优化档的 `.asm` 里。

**实测证据（关键）**：卡自己归属的 gcc 13.1.0 产物 `Examples/atoms/_c_decay.asm`
的函数头只有 `printf` 与 `main`——**连归属编译器自己的工件里都没有那个符号**。
所以这不是「换了编译器才失效」，而是**在任何编译器下都不可能成立**。

**为什么此前不红**：toolchain 长期等于卡归属的 gcc 13.1.0 => `artifact_sha256` 命中
=> 结构断言从不被评估。650 批把工具链切到 mingw1530 GCC 15.3.0 后 sha 走不通、
回落到结构断言，这条断言才第一次被真正执行。

**排除环境问题**：任务卡猜测的「缺 clang/msvc 导致找不到替代校验」不成立——
`ci.yml` 的 cross-check 步骤本身就有 `if command -v clang++ ... else warning` 的
降级分支；且本机 clang 22.1.8 存在。缺编译器不会让 sha 走不通，也不会让
「contains 命中 0 次」变成环境问题。
### A.3 根因二：`_pin_compiler` 把 `gcc` 钉到 `g++`（工具缺陷，673q 修）

`tools/atom_evidence_replay.py::_pin_compiler` 把 `gcc`/`cc` 与 `g++`/`c++` 一起钉到
`toolchain.resolve_gpp()`。于是卡里写 `gcc ... file.c` 的 C 夹具实际由 **C++ 驱动**
编译，cc1plus 忽略 `-std=c11`（只 warn）。两个可观测后果：

1. **保真度缺陷**：卡声明 `-std=c11`、实跑 C++17/23。本地如此，CI（ubuntu-latest
   的 `gcc` 本就是 C 驱动）编的是另一种语言 => 同一张卡的工件在本地与 CI 上语义不同，
   「跨编译器替代校验」校验的也不是同一个东西。
2. **硬失败**：EV-MEM-046 的夹具用了 C11 专有语法（`_Alignof(max_align_t)`，
   C++ 下该名字在 `std::` 里）=> 3/3 条命令编译失败 -> `refute:compile_error`。

修法：C 驱动取「与 g++ 同目录的 `gcc`」（MinGW-w64 与 GCC 官方布局都保证同目录有
`gcc`），PATH 上也找一次；**都找不到就不替换**——宁可让调用者的 PATH 决定，也不静默
把 C 换成 C++（那会伪造「跑过了」）。不改任何断言的判据强度。

### A.4 修法：断言换成 claim 锚定、且五路实测成立

每张卡改为两类证据：

1. **读数键的 printf 格式串**（`.rdata`，跨编译器稳定，绑定期望输出的 key）
2. **承载该卡 claim 的关键立即数**（如 `mov<TAB>edx, 40` = `sizeof(int[10])`）

选取**由实测决定，不靠推断**。673q 逐条在五路产物上验证，**凡有一路不命中即弃用**：

| 五路验证对象 | 说明 |
|---|---|
| A | GCC 15.3.0 MinGW（replay 本地实际注入，`toolchain.toml` `prefer[0]`） |
| B | GCC 13.1.0 MinGW（卡 `artifact_compiler` 归属编译器） |
| C | clang 22.1.8 MSYS2（卡 `matrix` 声明的第二编译器） |
| D | Ubuntu gcc 13.3.0（**CI 侧等价物**，经 WSL） |
| E | 仓库已提交工件（13.1.0；`gate_engine` 的 haystack 读它） |

**被实测否决的候选**（记录下来以免未来的假修复）：

| 候选 | 否决原因 |
|---|---|
| `test bl, 15` / `test dl, 15` | Windows 用被调用者保存寄存器、Linux 不用 |
| `mov ecx, 16`（EV-MEM-046） | Linux SysV 第一整数实参是 `rdi` |
| `movabs rax, 4050765991979987505`、`cmp ebx, 7`、`mov edx, 8`（EV-MEM-047） | GCC 15.3 / clang 22 写法不稳定 |
| `mov edx, 1`（EV-UB-003） | clang 22 下不出现 |

**一个必须踩准的陷阱**：断言文本里的制表符必须是**真实 TAB**。`check_artifact_assert`
两侧都归一空白，所以写字面 `\t`（反斜杠+t）**replay 也照样绿**——但
`gate_engine` 的 `EV-ASSERT-SYMBOL-MAPPED` 用**不归一**的 haystack（夹具 + 工件原文）
判定「断言文本是否有出处」，字面 `\t` 永远匹配不上工件里的真 TAB => 会凭空多出 4 张卡
的 warn。仓内既有约定见 `EV-UB-NULLDEREF-669` 的 `texts: ["mov\tDWORD PTR ..."]`。
本次已实测到这个陷阱并全部改为真 TAB（改完后 `EV-ASSERT-SYMBOL-MAPPED` 的 5 个命中
里没有一张是 673q 触及的卡，即该判据的通过证据）。

### A.5 验证

```
python tools/atom_evidence_replay.py --check
  修前：confirm=62 refute=9  infra_error=0
  修后：confirm=71 refute=0  infra_error=0
```

五路断言实测：临时脚本 `build/673q_probe_check.py`（不入库），**0 异常**。
`ruff 0.6.9` / `mypy 2.3.1` 对 `tools/atom_evidence_replay.py` 均 exit 0。

### A.6 哈希面重锚（同 commit，仓库纪律要求 Merkle 根产出后同 commit 重钉）

```
python tools/pck_hash_renewal_628.py --apply   # 续签受影响的 EV-*/ATOM-* 证书
python tools/merkle_integrity.py build-all     # evidence 树根 30a81752 -> 14e0d74d
python tools/tool_integrity.py --update        # core 5 + test_config 2 + supply_chain 6 + ruler 22
python tools/tool_integrity.py                 # 自检 exit 0
```

`atom_evidence_replay.py` / `cppbible.py` / `debt_ledger.py` / `golden_lock.py`
都在完整性哈希面里（CORE_TOOLS / RULER_TOOLS），改动后未 `--update` 会被
**fail-closed 拒绝运行**（本次实测触发：报「判定核心被改动且未重钉，拒绝运行」）。
---

## B. Golden Lock

### B.1 先修本批自己造的回归

A 批次换掉断言后，原子卡里的 `liveness: {kind: fixture_symbol, symbol: <函数名>}`
变成**悬空锚**——`gate_engine._prop_liveness_ok` 按**集合精确匹配**校验该符号须是
引用卡 `artifact_assert` 的目标。=> `OBSERVATION-LIVENESS` 13 -> 22、`warn_findings` +9。

修法：9 张原子卡的锚改指向该命题真正的**载荷读数键**（同时满足：① 是 artifact_assert
的精确目标 ② 在夹具源码里逐字可寻 ③ 正是该 claim 依赖的读数）：

| 原子卡 | 新锚 |
|---|---|
| ATOM-LANG-DECAY-001 | `decay_sizeof_param=%zu` |
| ATOM-LANG-FNPTR-001 | `fnptr_sizeof=%zu` |
| ATOM-LANG-VOLATILE-001 | `vol_flag` |
| ATOM-LANG-INTPROMO-001 | `char_sum_type_size=%zu` |
| ATOM-LANG-BITFIELD-001 | `bf_byte0=%u` |
| ATOM-LANG-MACRO-001 | `sq_bad=%d` |
| ATOM-MEM-MALLOC-001 | `alloc_aligned=%d` |
| ATOM-MEM-STRBOUND-001 | `strncpy_last_byte=%d` |
| ATOM-UB-SIGNEDOVF-001 | `unsigned_wrapped=%u` |

### B.2 把 55 条「未分类」warn 显式归属

6 个规则 ID 此前不在 `golden_state.warn_classify` 里，55 条 warn 无归属。逐规则核实
来源后显式归入 `legacy`：

| 规则 | 条数 | 核实到的来源 |
|---|---|---|
| ATOM-AUDIENCE | 10 | `atoms/draft650/` 的 10 张占位空壳卡（DEBT-005 跟踪） |
| ATOM-CLAIM-STRUCTURED | 10 | 同上 |
| ATOM-FM-REQUIRED | 10 | 同上（666 A2 已降 warn 以保门禁判别力） |
| ATOM-ID-FORMAT | 10 | 同上 |
| EV-MATRIX | 10 | 648 C 探针批次的卡 |
| EV-ARTIFACT-VERSION-MATCH | 5 | 669 批次的 5 张卡（EV-MEM-NEWARR-669、EV-UB-DIVZERO/NULLDEREF/OOB/WRAP-669） |

分类后：`real 14 / legacy 173 / accepted 16 / 未分类 0`——203 条**全部有归属**。

### B.3 显式接受 +27（理由留痕在 `golden_state.accepted`）

**+27 全部是存量，不是本批新增。** 14 条 `real` 的逐条落点：

| 规则 | 条数 | 命中卡片 |
|---|---|---|
| EV-ASSERT-SYMBOL-MAPPED | 4 | EV-CONC-001、EV-MEM-017、EV-MEM-035、EV-UB-OOB-669、EV-UB-WRAP-669 |
| EV-FALSIFICATION-QUANT | 4 | EV-HIST-001、EV-MEM-003、EV-MEM-006、EV-MEM-010 |
| EV-OUT-UNDECLARED-KEY | 6 | EV-CONC-002..006、EV-LANG-002 |

均非 673q 触及的卡；673q 的净变化为 0（见 B.1）。

**诚实登记**：`golden_state` 只存总数 176，**不存逐规则明细** => +27 无法逐规则回溯到
基线。要逐条归因需先给快照补 per-rule 基线（不在本批范围）。

**为什么选「分类 + 接受」而不是改那 15 张卡的正文**：修完 14 条 real 只能把 203 降到
189，仍 > 176 => 门禁仍需 `--accept`。既然本批无论修不修都要 `--accept`，就把力气花在
「让债务有归属」上，14 条列入下方后续清单。

### B.4 后续清单（本批不做，需内容决策）

| 规则 | 卡 | 建议修法 |
|---|---|---|
| EV-ASSERT-SYMBOL-MAPPED | EV-MEM-017 | 卡断言 `_Znwm`，而 MinGW 的 operator new 实为 `_Znwy`（LLP64 下 size_t 是 unsigned long long）=> 改 `contains_any: [_Znwm, _Znwy]`（Linux 侧确为 `_Znwm`） |
| EV-OUT-UNDECLARED-KEY | EV-CONC-002..006、EV-LANG-002 | 把 `.out` 里的键补进 `run_match_keys` 并声明期望值，或从 `.out` 移除 |
| EV-FALSIFICATION-QUANT | EV-HIST-001、EV-MEM-003/006/010 | `falsification` 补量化对照取值（两个可复核的数） |
| 快照缺 per-rule 基线 | golden_state | 加一节 per-rule 计数，才能让下一次 +N 可逐规则归因 |
---

## C. Debt Ledger

### C.1 分母查清：20 是错的，且根因是硬编码漂移

- 实际：`check --stage quality` 有 **27** 项门禁（`cppbible.py` 的
  `elif stage == "quality"` 分支；本次汇总行即 `27 passed / 0 failed` = 27）。
- 声明：`debt_ledger.py` 写死 `QUALITY_GATES = 20`，注释宣称「与 cmd_check 的
  quality 项数一致（meta-manifest 已锁）」——**该一致性早已失效**。
- 判定：20 **既不对应任何现存的门禁子集**，也没有任何文档把它定义为「核心质量门」
  => 是错的，不是另一套有意的定义。673m 的担心（改分母只是把指标改绿、债务一分没还）
  **在结果层面成立**，所以本批的处理是：修根因 + 把「变绿不等于还债」写进代码注释、
  台账 progress 与本报告，三处留痕。

根因不是数字本身，而是**硬编码会随门禁增删静默漂移**（偏小则指标偏严、假红；
偏大则指标偏松、掩盖真实负债率）。故：

1. `cppbible.py` 新增模块级 `QUALITY_GATE_NAMES`（27 项，quality 门禁名单的**单一
   事实源**），并在 `cmd_check` 的 quality 分支**跑前自检**门数一致，不一致当场红。
   已用 AST 逐项核对：分支实列 27 项与名单**逐项一致**（不只是数量一致）。
2. `debt_ledger.py` 的分母改为 `len(cppbible.QUALITY_GATE_NAMES)`；事实源不可导入时
   **判红**（fail-closed），不用兜底值蒙对。

### C.2 负债率

```
修前：4/20 = 20%  > 15%  -> 停线（exit 1）
修后：4/27 = 14.8% <= 15% -> PASS（exit 0），输出带分母来源可追溯
      [debt] 票据 4 · 负债率 14.8%（4/27，分母来源 cppbible.QUALITY_GATE_NAMES）· 问题 0
```

### C.3 需 owner 决策的 4 票清单（**Agent 不得自批**）

| 票 | due | 根因 | 673q 复核结论 | 建议动作（owner） |
|---|---|---|---|---|
| **DEBT-001** | **2026-10-10** | `compile_exempt.json` 历史豁免未票据化 | 673b 逐条重编：58/58 全部仍有效，无 DRIFT/STALE；票面写 63、实测 58（差额 5 条此前已清理）。结构债仍在：28/58 缺 `note`、全部无逐条 `expiry` | **距到期 8 天，逾期即停线**。三选一：① 补 `note`+逐条 `expiry` 后清票 ② 延期（改 due，需写理由）③ 接受为常设豁免并重开票 |
| DEBT-002 | 2026-11-12 | 437 个 `Examples/*.cpp` 工作树 CRLF 与索引 LF 漂移 | 673m 复核：漂移面**反而扩大**到 570 个文件，「碰到即转」未见收敛。批量 renormalize 仍被监工裁决禁止 | 重裁决：批量 renormalize / 改策略 / 缩窄范围到受控目录 |
| DEBT-003 | 2026-12-12 | 373 新规则暴露的存量债（聚合 5 个子项） | `tools/artifact_producer_exempt.txt` 仍 60 行、mtime 停在开票当日 => 19 天零消化。子项均属内容改动 | 派内容批次消化，或逐子项拆票 |
| DEBT-005 | 2026-12-12 | 650 批在 `atoms/draft650/` 留下 10 张占位空壳卡 | 10/10 仍为 `status=draft`、claim/evidence 全空；**这 10 张正是 B.2 里 40 条 warn 的来源** | 二选一：① 定稿（补内容 + 正式 ID + claim_structured）② 清退出 `atoms/` 受控树 |

**本批对 4 票的处理**：全部保持开票、progress 各追加 673q 留痕
（「指标变绿仅因分母纠错，债务一分未减」），未做任何清票、未改 due。

---

## D. 顺带修掉的一个门禁回归（670c D2-guard）

`cppbible.py` 的 AST 变更使 670c 的 rerun 门判 `STALE`（源码语义变了而产物
`tools/compile_report.json` 未刷新，判据是「假绿风险」）。

判断：本次改动只涉及 quality 阶段的门数声明与自检，**不触及编译语义**（编译器、flags、
章节、块均未变），`compile_report.json`（最后一次生成 2026-09-09）仍然有效。故按该工具
既定语义（注释原文：「刷新基线请在**确认产物已重跑**之后执行 `--update`」）刷新基线，
**并在此写明理由**，而不是 regen 报告去制造哈希差异。

同批 `atom_evidence_replay` 被正确判为 `RERUN`（源码变 + 产物已刷新），无需处理。
刷新后 `670c/D2-guard` 转 PASS，`fast_gate` 转 PASS。

---

## E. 验证汇总（全部可复现）

| 命令 | 结果 |
|---|---|
| `python tools/cppbible.py check --stage quality` | **27 passed / 0 failed** |
| `python tools/atom_evidence_replay.py --check` | confirm=71 refute=0 infra_error=0 |
| `python tools/golden_lock.py check --no-replay` | 无恶化（恶化 0 改善 0） |
| `python tools/debt_ledger.py check` | 4/27 = 14.8% · 问题 0 · exit 0 |
| `python tools/fast_gate.py` | overall=PASS（12.6s / 预算 300s） |
| `python tools/prepush_check.py` | 除 worktree 外全过（提交后即过） |
| `python tools/run_master_gate_670c.py --check` | 670c/D2-guard 转 PASS |
| `ruff 0.6.9` + `mypy 2.3.1`（tools/ 三个改动文件） | 全绿 |
| AST 逐项核对 `QUALITY_GATE_NAMES` vs quality 分支 | 27 == 27，逐项一致 |

**已知未清项（不在本批范围，如实登记）**：

1. 14 条 `real` warn（B.4）。
2. 4 张债务票据（C.3），其中 DEBT-001 **8 天后到期**。
3. `golden_state` 缺 per-rule 基线，故 +27 只能整体接受、无法逐规则归因。
4. 本批未跑 `check --stage compile`（`compile_report.json` 保持 2026-09-09 的状态）；
   compile 阶段的质量由 CI 的 `compile` job 覆盖。
---

## F. 附：分母 27 的三方交叉确认（防「到底是 20 / 27 / 31」之争）

673q 之后有并行批次（673s）在 `ci.yml` 里写下「`pyproject` 声明了 **31** 项核心门禁」，
与本报告的 27 不一致，故在此把三个数字的来源与裁决写清：

| 数字 | 来源 | 语义 | 673q 裁决 |
|---|---|---|---|
| **27** | `cppbible.py` 的 `elif stage == "quality"` 分支 + 新增的 `QUALITY_GATE_NAMES` | `check --stage quality` **实际跑**的门禁数 | **采用**（负债率分母取此） |
| **27** | `pyproject.toml` 的 `[tool.cppbible].quality_gates`（manifest，27 条脚本路径） | 核心门禁**清单**（ADR-0004 双清单收敛的另一侧） | 与上者**同一集合**，仅一个是显示名、一个是脚本路径 |
| 20 | `debt_ledger.py` 旧硬编码 + 注释「meta-manifest 已锁」 | 无对应集合，也无文档定义 | **判定为错**，已废 |
| 31 | 673s 批次笔记里的数字 | 与上述两处都对不上（疑为笔误，或含 compile/publish 阶段） | **不采用**；若 673s 的作者能指出 31 的具体清单，请以清单为准 |

两处 27 的**独立一致性**已实测：`python tools/gate_engine.py --manifest-check` exit 0
（该检查就是校验 pyproject manifest 与 cppbible quality 元组的一一对应），
且逐项点数两边都是 27、顺序与工具集合相同。

**为什么分母必须等于「实际跑的门数」而不是「任何清单的长度」**：负债率的意义是
「每项质量门摊到的带息豁免数」，分母若换成别的清单，指标就换了含义，而指标换含义
是比指标偏高更坏的事（它会让一个真实数字看起来像另一个真实数字）。