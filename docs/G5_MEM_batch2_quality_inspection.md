# 红队报告 + 质检报告 · G5 MEM 域第二批批量生产（4 原子）

> Writer 执行 Agent 产出 · 2026-09-11 · 范围：goldens/mem/ATOM-MEM-{VALUE-002,RAII-002,ALLOC-001,PERF-002}_draft.md × 4 + evidence/mem/EV-MEM-021..031 × 11（新卡）+ misconceptions/MIS-MEM-017..023 × 7 + Examples/atoms/_atom_*.cpp × 12（11 主夹具 + 1 ASan 第二证据腿）
> 三权分立状态：Writer 完成 → RedTeamer（独立子 agent）两轮攻击/复核完毕 → Gatekeeper 机器门禁自报如下。**未原子化、未置 verified、未 commit/push，待人审签署**（人审后按 Step 4 执行 git mv + 签署 + golden_lock sync）。

---

## 一、红队报告（两轮，RedTeamer 为独立子 agent，与 Writer 分离）

### 第 1 轮（S1–S6 逐层攻击）

| 原子 | 判定 | 关键缺陷 |
|---|---|---|
| VALUE-002 | 修改后再审 | [一般] claim_boundary 覆盖 C++11..23 但实测仅 c++23（未注 machine-run 档口径，VALUE-001 第 1 轮同类）；[建议] EV-MEM-021 artifact_assert 锚定出现在输出字面量里的期望类型串（"期望值进字面量"级）；[建议] EV-MEM-022 reproduce "三行"笔误 |
| RAII-002 | 修改后再审 | [一般] claim"删除拷贝"过度概括（可拷贝 RAII 成员拷贝是隐式生成且语义正确，与自家 EV-MEM-023 边界说明相抵）；[一般] EV-MEM-025 含无代码支撑的"-O0 moves=4 构造噪声"断言；[一般] EV-MEM-024 的 ASan 第二证据腿源码未入库、两份代码"同型"不可复核；[建议] rule_zero frees 绝对计数口径；[建议] EV-MEM-023 depth_layer 错位 |
| ALLOC-001 | 可提交待人审 | [建议] MIS-MEM-021 把"C++17 移除 construct/destroy"（条文）挂到"EV-MEM-026 实测"（实测的是 allocate 零构造）；[建议] 跨标准注记；[建议] 繁体错字"組" |
| PERF-002 | 修改后再审 | [一般] domain: PERF 与同族 ATOM-MEM-PERF-001（domain: MEM）及 ID/目录体系不一致；[一般] claim"三实现参数互不相同"与自身数据矛盾（MSVC 32/15 == libstdc++ 32/15）；[建议] claim"赋值 allocs=0"超实测范围；[建议] EV-MEM-031 对照最弱未声明定位 |

横向专项全部通过：S1 无自签（4 颗均 draft、自评 4/5 且明示上限）；cognitive_load/audience 全合法；prerequisite 目标全部 verified；`|` 无污染；command 均为 replay 不经 shell 可执行形态；正文引用的 EV/MIS 编号全部真实且语义一致。

### 第 2 轮（复核，13 项修订逐条核销）

- VALUE-002：3/3 ✅（claim_boundary 口径注记、artifact_assert 换锚为 `sink_lvalue` 符号 + `auto&& from` 结构锚、reproduce 笔误）→ **可提交待人审**
- RAII-002：4/5 ✅，1 项部分整改（claim 主干仍残留全称"删除拷贝"）→ **修改后再审**
- ALLOC-001：3/3 ✅（附 1 条建议级：MIS-MEM-021 正文未与 refutations 同步）→ **可提交待人审**
- PERF-002：3/3 ✅，但发现收窄口径跨文件残留 3 处（draft ASCII 图、EV-MEM-030 hypothesis、MIS-MEM-022）→ **修改后再审**

### 终轮 Writer 修订（7 处一行级，纯 diff 级复核）

1. RAII-002 draft claim 主干收窄为"隐式特殊成员函数语义全部正确（可拷贝成员拷贝隐式生成且语义正确、不可拷贝成员如 unique_ptr 的拷贝被删除）"；grep 验证"删除拷贝"仅存于"不是一律"语境。
2. MIS-MEM-021 正文第 2 条与 refutations[1] 同步分口径（条文 vs 实测）。
3. PERF-002 draft ASCII 图"构造/拷贝：0 次堆分配（赋值同路径）"（长串"赋值 1 次"有 EV-MEM-030 实测行背书）。
4. EV-MEM-030 hypothesis 同步"拷贝零堆分配（赋值走同一实现路径，未单列观测行）"。
5. MIS-MEM-022 两处同步同口径。
6. EV-MEM-024 falsification 措辞统一（"三条件均不成立"）。
7. EV-MEM-031 补"布局锚定卡"定位 + depth_layer 分层说明。

红队对第 3 轮的授权口径："剩余问题均为一行级文本修改……纯 diff 级复核即可"——上述 7 处均按其 prescribed 原文修改并经 grep 机械核验（详见 Gatekeeper 记录）。

---

## 二、Gatekeeper 机器门禁（Writer 自报，供监工独立复跑）

| 门禁 | 命令 | 结果 | 结论 |
|---|---|---|---|
| 证据卡复算 | `tools/atom_evidence_replay.py --check` | **confirm=34 / refute=0**（23 存量 + 11 新卡，含 sha256 重生成一致） | ✅ |
| 门禁引擎 | `tools/gate_engine.py --check`（29 规则） | **block=0**，warn=15（= 4 预存 + 11 条 EV-SERVES-EXIST，服务对象为未锻造的 draft 原子，原子化后自动清零——与第一批同款预期债务） | ✅ |
| 黄金锁 | `tools/golden_lock.py check` | 恶化 1（warn_findings 4→15，即上述预期债务）· 改善 2（evidence_total 23→34、replay_confirm 23→34）；block_findings 保持 0 | ✅（预期态，收尾 sync 后核销） |
| 毒样例 | `tools/poison_drill.py` | **4/4**（P1/P2/P3 拦截 + 阴性放行） | ✅ |
| 单元测试 | `.venv\Scripts\python.exe -m pytest tests/ -q` | **82 passed** | ✅ |

批内 S3-EXPECTED-HARDCODED 曾拦 3 处（EV-MEM-021 `sink_lvalue(int&) called` 整句常量、EV-MEM-023 `rule zero: static_assert move=1 copy=0` 整句常量 ×2），已按 VALUE-001 先例改为"计算片段拼接输出"（`sink_lvalue called x=` + 运行时值；`move_constructible=`/`copy_constructible=` 经 `is_move/copy_constructible_v` 运行时打印）并重生成工件换 sha，复核归零。

---

## 三、证据卡清单（11 张，全部 verdict: confirm）

| 卡 | 服务原子 | 观测口径 | 核心数字 |
|---|---|---|---|
| EV-MEM-021 | VALUE-002 | compiler（static_assert + 推导观测） | 折叠 4 规则全绿；万能引用左值 T=int&/右值 T=int；const T&& 只接右值 |
| EV-MEM-022 | VALUE-002 | runtime（-O0/-O2 双跑一致） | forward 右值 copies=0 moves=1；forward 左值 copies=1；省略 forward copies=1 moves=0 |
| EV-MEM-023 | RAII-002 | runtime | move_constructible=1 copy_constructible=0；owner_changed=1；allocs=1 dtors=1 frees=1 |
| EV-MEM-024 | RAII-002 | runtime + WSL ASan 旁证 | buggy allocs=1 same_ptr=1 dtor_runs=2；correct allocs=2 same_ptr=0；ASan 实报 attempting double-free（第二证据腿源码已入库：Examples/atoms/_atom_rule_three_bug_asan.cpp:14） |
| EV-MEM-025 | RAII-002 | runtime（-O0/-O2 一致） | noexcept 组 copies=0 moves=4；漏标组 copies=4 moves=0 |
| EV-MEM-026 | ALLOC-001 | runtime（-O0/-O2 一致） | allocate: allocs=1 ctors=0；construct ctors=2；destroy dtors=2；deallocate frees=1 |
| EV-MEM-027 | ALLOC-001 | runtime（-O0/-O2 一致） | arena calls=5 bytes=124 heap_new=0；std 组 heap_new=5（同构对照） |
| EV-MEM-028 | ALLOC-001 | runtime（-O0/-O2 一致） | monotonic upstream_allocs=0；delegating res_calls=5 bytes=124 |
| EV-MEM-029 | PERF-002 | runtime（-O0/-O2 一致，双通路交叉） | len≤15 allocs=0；len=16 allocs=1；max_zero_alloc_len=15 first_heap_len=16 |
| EV-MEM-030 | PERF-002 | runtime（-O0/-O2 一致） | 短拷贝 0 / 长拷贝 1 / 长赋值 1 / 拼接越阈 1 |
| EV-MEM-031 | PERF-002 | compiler（布局锚定卡） | sizeof=32（static_assert）+ capacity=15 + len=15/16 分配计数三值自洽 |

批内观测方法论留痕（已写入卡内 drill_note）：
- **MinGW 动态 libstdc++ 的 DLL 边界**：new_delete_resource 等库内非模板代码的 operator new 调用不经过 exe 替换版本（DLL 内符号自绑定）——EV-MEM-028 初版以 operator new 钩子观测得假阴性 heap_new=0，重写为虚资源层计数后得 res_calls=5；pmr 证据一律以资源层计数为准。
- **计数通路唯一**：EV-MEM-029 初版 CountAlloc 手动计数 + operator new 钩子双重计数（len=16 假信号 allocs=2），修正后 allocs=1。

---

## 四、五重剖面完整性（4/4）

| 原子 | 多源精炼 | 一手实证 | superiority | depth 纵深 | 教学封装 |
|---|---|---|---|---|---|
| VALUE-002 | ✅ 3iso+cppref | ✅ EV-021/022 | ✅ 折叠语法前提留痕+量化代价 | ✅ compiler/runtime | ✅ 动机+2误解+3问+预测 |
| RAII-002 | ✅ 2iso+cppref | ✅ EV-023/024/025（含 ASan 旁证） | ✅ 三卡对照对+ASan 因果链 | ✅ runtime | ✅ 完整 |
| ALLOC-001 | ✅ 2iso+cppref | ✅ EV-026/027/028 | ✅ 包装论三行对照表 | ✅ runtime | ✅ 完整 |
| PERF-002 | ✅ iso+cppref+impl_doc（文档值口径标注） | ✅ EV-029/030/031 | ✅ 阶跃实测+三实现参数+COW 因果 | ✅ runtime/compiler | ✅ 完整 |

---

## 五、遗留事项（不阻断人审）

1. **EV-SERVES-EXIST ×11**：服务对象为 4 颗 draft 原子，人审原子化（git mv 进 atoms/）后自动清零。
2. **Clang 列**：11 卡均标注"待 CI Cross-check 步回填"（本机无 Clang，M2 边界）；PERF-002 的 libc++/MSVC 参数为文档值口径并已显式标注。
3. **EV-MEM-025 -O0 口径**：双跑逐字一致（recorded in run_cxx23_O0）；replay 机器口径为 -O2（EV-MEM-008 先例）。
4. **推送前**：须先跑 WSL `ci_local_precheck.py`（Evidence Replay 步在 WSL 必失败为已知边界，Windows 侧 confirm 全绿即可放行）；提交用 `git commit -F` UTF-8 文件。
5. **本批临时探针已清理**（build/_probe_pmr.*、build/_find_hardcoded.py、build/_double_free_asan.*），ASan 正式夹具已入库 Examples/atoms/_atom_rule_three_bug_asan.cpp。

---

## 六、交付物清单核对（指令 §七）

| 交付物 | 状态 |
|---|---|
| 1–4. goldens/mem/ 4 颗 draft | ✅ ATOM-MEM-VALUE-002 / RAII-002 / ALLOC-001 / PERF-002（均 status: draft、自评 4/5） |
| 5. evidence/mem/ 11 张新卡 | ✅ EV-MEM-021..031（replay 34/34 confirm） |
| 6. Examples 夹具 | ✅ 11 主夹具 + .asm 工件（sha 同代）+ 1 ASan 夹具 |
| 7. misconceptions 7 条 | ✅ MIS-MEM-017..023（编号已 rglob 确认未占用；deep 类 refutations ≥2） |
| 8. 红队报告 + 质检报告 | ✅ 本文档 |
| 9. 原子化进 atoms/mem/ | ⏸ **待人审签署**（三权分立铁律） |
