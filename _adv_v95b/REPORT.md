# 547 · 第五轮独立对抗（续打）REPORT

> 独立对抗者：与建设者不同模型族、零上下文。本轮只打 **B/C/D 面**（V-iso 阴阳同构 / 新旧接缝 / mutation_fuzz 判决诚实性），A 面（L2 task_queue）已由 545 打完（见 `_adv_v95/REPORT.md`），**本轮不重复 A 面**。
> 纪律：全部探针落 `_adv_v95b/`，只读正式文件、不 commit、不 push、不 accept；零污染自证见 `zero_pollution.md`。
> 复跑：`.venv\Scripts\python.exe _adv_v95b\probes/run_all.py`

## 一句话：这批系统最脆的一环

**V-iso 阴阳同构的 `negative_controls` 准入缺两道硬闸——阴面 fixture 不锚定到本卡阳夹具（B3）、且门禁 YAML 硬化层对 `negative_controls` 沉默接受 flow 式写法（B5）；相比之下 mutation_fuzz 判决诚实性（D）与新旧接缝（C）本轮全绿。**

## 严格拦截率（warn 不算拦截；INCONCLUSIVE 不进分母）

| 面 | 有效探针（BLOCKED+ESCAPE） | ESCAPE | INCONCLUSIVE（未测/需真编译） | 仅 warn 可见 |
|---|---|---|---|---|
| B · V-iso | 4 | **2**（B3、B5） | 2（B1、B6） | 1（B3 为 naming warn） |
| C · 接缝 | 2 | 0 | 1（C2） | 0 |
| D · mutation_fuzz | 7 | 0 | 0 | 0 |
| **合计** | **13** | **2（15.4%）** | 3 | 1 |

- **严格诚实率** = (13 − 2) / 13 ≈ **84.6%**
- **逃逸率** = 2 / 13 ≈ **15.4%**（均落在 B 面，且均属"准入层"而非"判决层"）
- 两处 ESCAPE 都不是"直接把错误状态推成 verified/done"：B5 是门禁层**沉默接受**（无 block 无 warn），B3 至少是 schema **naming warning 可见**但未升 block。后果是 V-iso 的"阴性证据"可被冒名/走私，削弱 533 阴阳同构的判据完整性，但**不会**把坏卡当 verified 放行。

## 发现（含可复现证据）

### B3 · 阴面 fixture 不锚定到本卡阳夹具 — 严重度 **中**（ESCAPE）

- **构造**：取一张与阳夹具 `Examples/atoms/_atom_fence_vs_atomic.nc1.cpp` 不同的真实 `.cpp`（`Examples/atoms/_atom_align_ctrl.cpp`，同优化级/同仓别卡产物）当作某 `nc9` 的 `fixture`，`anchor=spin_plain`、`probe.symbol=_Z10spin_plainv`。
- **实测**（`probes/probe_viso_negative.py::t_b3_yin_not_bound_to_card`）：
  ```
  [ESCAPE] t_b3_yin_not_bound_to_card: ESCAPE (借来 fixture=Examples/atoms/_atom_align_ctrl.cpp；
  schema 仅告警 naming=[...命名规约建议...]，未绑到本卡阳夹具)
  ```
- **击穿点**：`tools/viso_diff.py::validate_nc_schema`（L308–407）只校验 fixture *存在*（L339）、fixture *不是阳夹具自身*（L337）、以及命名规约——后者在 L345–347 仅是 `warns.append(...)`，**不是 errors**；全程**没有"该 fixture 必须与本卡阳夹具同源/同卡"的约束**。于是阴面可以借别卡/别优化级的产物冒充自己的"翻转"证据，schema 仅以 naming warning 放过去。
- **后果**：533 §2.1 阴阳同构的"阴面翻转必须真由删机制引起"判据被冒名削弱——阴性控制读到的可能是别的编译产物。
- **建议修**：在 `validate_nc_schema` 里加 `yang_fixture` 同源锚定校验（阴面 fixture 主干名必须 == 阳夹具主干名 + `.nc<id>`，否则 `errs.append` 升 block）；命名规约 warning 同步升 block。

### B5 · 门禁硬化层沉默接受 flow 式 `negative_controls` — 严重度 **中高**（ESCAPE）

- **构造**：把 `negative_controls` 写成 flow 列表塞进 frontmatter（`negative_controls: [{id: nc1, variant: delete, ...}]`）。
- **实测**（`probes/probe_viso_negative.py::t_b5_flow_style_nc_parsed`）：
  ```
  [ESCAPE] t_b5_flow_style_nc_parsed: ESCAPE (flow 式 negative_controls 被收下：[{...}]);
  门禁硬化只查 block 式，flow 漏网
  ```
- **击穿点**：
  - `tools/atom_evidence_replay.py::parse_frontmatter`（L275）用自定义解析器，**flow 式 list 被正常收下**（返回 `negative_controls` 为 list）。
  - 门禁硬化 `EV-FM-YAML-HARDENING`（`tools/gate_engine.py::_fm_hardening_uncached`，L1316–1354）只查 **block 式**信号：`[indent-smuggle]`（标量值后缩进键行，L1323）、`[dup-key]`（L1333）、`[invalid]`（L1337）、`[parse-diverge]`（L1344–1353，且**只比 `id/verdict/status/artifact_sha256` 四个键，不含 `negative_controls`**）。**flow 式写法不触发上述任一条** ⇒ 门禁层既不 block 也不 warn，给出虚假"干净"信号。
  - 对照：真正吃到这条卡的 replay 路径 `check_negative_controls`（`atom_evidence_replay.py:1192,1207`）其实要求 block 列表/block map，会 `refute:negative_control_bad_schema`——但**仅 M1/M7** 走 replay；非 replay 变体（M2–M6）和**门禁硬化层本身**对 flow 式 nc 完全静默接受。
  - 这正是 539 硬化要堵的"走私/重复键/语法/一致性"族在 `negative_controls` 新字段上的复活：硬化层与 replay 路径对 `negative_controls` 的 block/flow 约束**不一致**，且 `[parse-diverge]` 不查该键，flow 式可夹带被自定义解析器独吞的内容。
- **后果**：一张用 flow 式 `negative_controls` 的卡在门禁层被当合法，硬化给假阴性；若后续真跑 replay 才失败，等于把"格式不合规"延迟到最贵的路径才暴露，且静态审计扫不到。
- **建议修**：① 在 `EV-FM-YAML-HARDENING` 加"flow 式 `negative_controls` 拒绝"信号（要求 block 式），或 ② 把 `negative_controls` 加入 `[parse-diverge]` 比对键、并在 `parse_frontmatter` 对 flow 式 nc 直接抛 `ValueError`（与 replay 路径一致）。

## 各假设逐条裁决（ESCAPE / BLOCKED / INCONCLUSIVE）

### B · V-iso 阴阳同构
| 假设 | 结果 | 证据 / 说明 |
|---|---|---|
| B1 iso_judge 绕过（删 1 行实则改语义） | **INCONCLUSIVE** | 需真实编译比对阴面是否"删 1 行改语义"，纯函数探针无法判定；本轮未做（见未覆盖清单） |
| B2 翻转造假（阳面恒真） | **BLOCKED** | `_nc_flip_ok("becomes_present",5,5)→(False,False)`；`("becomes_absent",3,0)→(True,_)`；恒真 text 不被当翻转 |
| B3 阴面不锚 sha | **ESCAPE** | 见上，fixture 可借别卡产物，schema 仅 naming warn |
| B4 阴面编译失败归类 | **BLOCKED** | `classify_command_failure`：compiler_missing→infra_error / compile_error→refute / timeout→infra_error / rc0→confirm，阳面 rc≠0 不被豁免 |
| B5 YAML flow 走私 | **ESCAPE** | 见上，硬化层静默收下 flow 式 nc |
| B6 nc1 诚实性（换优化级/符号名） | **INCONCLUSIVE** | 需真编译 `ATOM-CONC-001` 在 -O0/-O2/-Os 三侧比对读数，超纯函数范围 |

### C · 新旧接缝
| 假设 | 结果 | 证据 / 说明 |
|---|---|---|
| C1 548 新规则真仓库零误伤 | **BLOCKED** | `check_card_path_canonical()` 真仓库 0 命中（61 规则，存量 0 误伤） |
| C2 549 fast 分支接缝（skip replay 后 warn 是否计入） | **INCONCLUSIVE** | 549 未实现；当前 M2 非 replay 算子 ⇒ `CARD-PATH-NOT-CANONICAL` 走门禁恒定可见，留待 549 自测 |
| C3 沙箱读副本、M2 三异体都见 | **BLOCKED** | 沙箱里 M2 大写 / `./` / 反斜杠 三种表单均被 `check_card_path_canonical` 命中（规则读副本，不漏判） |

### D · mutation_fuzz 判决诚实性（本轮最高优先，全绿）
| 假设 | 结果 | 证据 / 说明 |
|---|---|---|
| D1 双解析器不一致 / 用桩 | **BLOCKED** | spy `_snapshot` 在 `classify` 内被真实调用（t_d1），非桩非缓存 |
| D2 跨卡规则按卡裁剪 | **BLOCKED** | 改本卡 id 撞别卡 ⇒ `EV-ID-UNIQUE` 仍进 `new_block`（t_d2） |
| D3 n_a 藏身（逃逸冒充 blocked） | **BLOCKED** | 不可解析 / 空 text assert 均 → `n_a`+`malformed`，不冒充 blocked（t_d3） |
| D4 baseline 不重置 | **BLOCKED** | 同卡两次 `run_fuzz` 排除 n_a 后 verdict 集合一致（t_d4） |
| D5 只报新 blocked 不报回归 | **BLOCKED** | 注入 dup `serves` 新 block 如实报出，verdict∈{blocked,escaped,n_a} 不谎报（t_d5） |
| D6 隐藏 replay infra_error | **BLOCKED** | 注入 `infra_error:compiler_missing` ⇒ `n_a`+`why` 含 infra_error，不当 escaped/不静默丢（t_d6） |
| D7 selection bias（--cards all 漏卡） | **BLOCKED** | `by_card` 数 == 选中数（t_d7），无漏卡 |

## 对 533 / 534 / 543 设计论断的裁决

| 论断 | 裁决 |
|---|---|
| 533 §2.1「`negative_controls` 阴阳同构：阴面翻转须真由删机制引起，schema 严判」 | **部分成立**：结构判据在（B2 翻转造假、B4 编译失败均被挡）；但有 **2 个准入缺口**（B3 阴面 fixture 未锚阳夹具、B5 flow 式被硬化层沉默接受） |
| 534 §6.5 / §4.3 / §6.1（L2 预算/自证/心跳） | **本轮未重测**（属 A 面，已由 545 裁决：预算闸门仅第一级成立、自证同人不成立、心跳依赖时钟一致）；547 不重复 |
| 543「mutation_fuzz = 系统自检第一闸，判决诚实」 | **成立**：D1–D7 全 BLOCKED，无桩/缓存/裁剪/藏 n_a/藏 infra_error/漏卡；本轮探针范围内该闸可信 |

## 饱和声明 + 未覆盖清单（不许假装打完）

**已饱和并实锤**：D 面 7/7、C 面 2/3（C1/C3）已饱和；B 面 B2/B3/B4/B5 已判定（B3/B5=ESCAPE 已实锤）。

**未覆盖（诚实列出，不硬凑）**：
- **B1**（iso_judge / `judge_min_diff` 绕过：阴面伪装 delete-only 实则改语义）→ 需真实编译构造夹具（宏/内联把机制藏进一行删除），纯函数探针无法判定；**留待带 g++ 的真编译轮次**。相关实现：`tools/viso_diff.py::judge_min_diff`（L208）、`tools/atom_evidence_replay.py::check_negative_controls`（L1183）。
- **B6**（nc1 诚实性：换 -O2/换符号名/删无关行，翻转是否仍只对 fence 敏感）→ 需真实编译 `ATOM-CONC-001` 在 -O0/-O2/-Os 三侧比对，排除"删啥都翻转"伪因果；**留待真编译轮次**。
- **C2**（549 fast 分支接缝：skip replay 后纯门禁 warn 是否仍计入 `new_warn`）→ 549 尚未实现，M2 当前非 replay 算子，门禁恒定可见；**属 549 自测范围，本轮不伪造结论**。

## 复跑

```
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe _adv_v95b/probes/run_all.py
# 红(有 ESCAPE)  —— 当前 2 个 ESCAPE（B3、B5）
```
