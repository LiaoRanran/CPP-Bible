# 527 批次F 交接 · 解锁 push + 概念归一 + 红队卡处置

> 仓库 `C:\CodeLearnling\note\note\C++\CPP-Bible`　本批目标：先把 push 解锁（ahead 187 堵着），
> 再修概念图谱根基污染。铁律：不 push、不 `--accept`（人审权）；一任务一 commit；
> 存量零误伤；不编造；并发时先等其退出。

---

## 〇、开工实测（fresh，无并发 python 进程）

| 命令 | 实测 |
|---|---|
| `golden_lock.py check` | **WORSE warn_findings: 32 → 57**（exit 1，等待人审 accept）✓ 与提示词预期一致 |
| `poison_drill.py`（单跑，.venv） | **83/83** · RULE-COVERAGE 33/58 · **exit 0** |
| `cppbible.py check --stage quality` | **25 passed / 2 failed** —— ❌ Golden Lock、❌ **Poison Drill** |

**矛盾复现** ✓：同一脚本单跑 83/83 绿、在 quality 里 82/83 红。

---

## 任务A：quality 里 Poison FAIL 的根因（P0）

### A.1 结论（**确定性 bug**，不是并发污染）

**`cppbible.py` 用"拉起它的解释器"（`PYTHON_EXE`）跑所有步骤**；本机
`workbuddy` python **没装 PyYAML**，而 `.venv` 装了 **PyYAML 6.0.3**。
而 `gate_engine.check_frontmatter_hardening()` 的开头是：

```python
try:
    import yaml
except ImportError:          # pragma: no cover
    return []                # ← 静默跳过**整个**检查
```

⇒ 在无 pyyaml 的解释器下，**连不需要 pyyaml 的信号①（缩进走私，纯正则）也一起丢掉** ⇒
poison 的 P43（缩进走私）没有拦截者 ⇒ 82/83 ⇒ Poison Drill FAIL ⇒ quality 红。
单跑用 `.venv`（有 pyyaml）⇒ 83/83 绿。**这就是"单跑绿、quality 红"的全部原因。**

### A.2 证据链（按提示词给的排查方向逐条落）

| 方向 | 排查结果 |
|---|---|
| ① Golden Lock FAIL 会不会改 `golden_state.json`，而 poison 读它导致分母变化 | **排除**：`poison_drill` 源码里**没有任何** `golden` 引用（`Select-String` 零命中）；`golden_lock` 的 `_save()` 只在 `sync`/`accept` 路径调用，`check` 的 FAIL 路径**不写** |
| ② 并发污染（探针写在真实仓） | **排除**：开工前 `Get-CimInstance Win32_Process` 无其他 python；poison 的样例全部在 `sandbox()`（patch `ge.ATOMS/EVIDENCE`）里写卡 |
| ③ cppbible 的失败聚合 | **排除**：`run(cmd, check=True)` 逐条捕获，`failed` 计数与 `return 1 if failed else 0` 正确；只是 FAIL 时只打印 `e.stdout[-800:]`（本批顺手改掉，见 A.4） |
| ④ 按 quality **同序**复现 | 用 `_repro527.py` 依次跑 replay(248.5s)→gate(4.2s)→golden(175.3s，exit 1)→debt(0.2s)→poison ⇒ **poison 83/83 exit 0**，**不复现** ⇒ 排除"前序步骤留下脏状态" |
| ⑤ 换解释器 | 用 **workbuddy python** 跑 poison ⇒ **82/83**，失败行 `P43 缩进走私（E07 缩进 verdict 提升顶层键）: 拦截者（漏网！）❌` ⇒ **复现** ✓ |
| ⑥ 依赖对比 | `.venv`：`PyYAML 6.0.3` ✓；workbuddy：`ImportError` ✗ |
| ⑦ 锁探活是否因解释器不同 | **排除**：`_pid_alive(999999)=False`、`_pid_alive(99999999)=False`、`_pid_alive(self)=True` —— 两解释器**完全一致** |

### A.3 修复（确定性 bug ⇒ 修它 + 配 pytest）

1. **信号①提前**：把缩进走私检测（纯 Python，不需 pyyaml）**移到 `import yaml` 之前**恒跑；
2. **缺依赖不许静默**：`except ImportError: return []` 改为留一条 **warn**
   `跳过 YAML 硬化的 ②/③/④ 信号：当前解释器缺 pyyaml（<可执行文件路径>）`——
   "跳过＝永久免检"是 368 P1-2 已确立的反模式（508"台账不存在＝永久免检"同源）。
   为何是 warn 不是 block：pyyaml 是**可选依赖**，把它当内容问题拦红会让"环境故障"伪装成
   "内容缺陷"；但静默跳过会让"检查没跑"伪装成"检查通过"。
3. **连带修 cppbible 的可诊断性**：新增 `_fail_digest()`——FAIL 时先打印含
   ❌/FAIL/Traceback 的信号行再打尾部 800 字符。本批定位根因时，poison 的 80+ 行输出被
   尾部 800 字符截掉、失败行落在中段，只能另写复现脚本才拿到证据。

**验证**：

| 环境 | gate | poison |
|---|---|---|
| `.venv`（有 pyyaml） | EXIT=0 **BLOCK=0 / WARN=57**（不变） | **83/83** |
| workbuddy（无 pyyaml） | EXIT=0 BLOCK=0 / WARN=**58**（多出的正是那条可见 warn） | **83/83**（P43 恢复拦截 ✓） |

`tests/test_gate_engine.py` **113 全过**，含新增回归锁
`test_yaml_hardening_indent_signal_survives_without_pyyaml`（用 `sys.modules["yaml"]=None`
模拟无 pyyaml：断言①仍 block + 降级 warn 可见 + 恢复后不再出现该 warn）。

### A.4 给运维的一句话

**跑门禁用装了 dev 依赖的解释器**（本仓是 `.venv`，`pyproject` 的 dev 组含 `pyyaml`）。
用裸环境解释器跑时，YAML 硬化的 ②/③/④ 会降级——现在**至少是可见的 warn**，不再静默。

---

## 任务B：解锁 push

### B1 warn 32→57 的构成（复现确认）

提示词：确认 57 = 31 基线 + 26 张存量卡的 STAGING warn。**复现结果一致** ✓
（下表的 20/54 是**本批 D/E 完成后**的终值，见 §B2 说明）

| 规则 | 数量 | 来源 |
|---|---|---|
| `ATOM-CLAIM-STRUCTURED` | **20** | 526 规则1 的存量 STAGING（27 张 − 已回填 7 张：样板 1 + 任务D 3 + 任务E 3） |
| `EV-MATRIX-UNBACKED` | 16 | 499 已审计（A3① 刻意设计，排除 `actual:` 段） |
| `EV-OUT-UNDECLARED-KEY` | 6 | 373-B3 窄化后遗留 |
| `EV-FALSIFICATION-QUANT` | 4 | S6 P5 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | **3** | 527 任务D 的三张红队卡（基准已登记 ⇒ 降级 warn） |
| `ATOM-REL-TARGET` | 2 | 规划前向引用（499 已记） |
| `EV-ASSERT-SYMBOL-MAPPED` | 2 | 499 已记（含 EV-MEM-017 `_Znwm`） |
| `EV-SERVES-EXIST` | 1 | 499 已记 |
| **合计 warn** | **54** | = 31（非 526 规则）+ 20（STAGING）+ 3（规则3） |
| **block** | **0** | ✓ 存量零误伤 |

> **⚠️ 数字与提示词不同步（须监工注意）**：提示词 B2 给的 accept 理由写"基线 32→57"，
> 那是**开工时**的数字。本批 D/E 又改了 warn 构成：E 让 3 张卡退出 STAGING（−3）、
> D 给 3 张红队卡加了 inference 命题（+3），**净变化 −3 ⇒ 终值 54**。
> 若监工要 accept，理由里的数字请用**收工实测值**（见 §收工验收）。

### B2 人审 accept 命令（**本苦力未执行**，原文照办）

```
python tools/golden_lock.py check --accept "批次E claim_structured STAGING 对存量26卡warn，基线32→57"
```

**上面的命令是提示词原文**。按本批终值（54）建议改用：

```
python tools/golden_lock.py check --accept "526/527 claim_structured 落地：规则 55→58，存量 STAGING warn + 527 规则3 warn；warn_findings 32→54（20 STAGING + 3 规则3），0 block"
```

### B3 `prepush_check.py` 结果（9 项）

第一次实跑（在任务D 的三张卡**尚未提交**时）：

```
  [✗] quality
  [✅] consistency   [✅] metrics   [✅] compile_gate   [✅] exempt_audit
  [✅] expected(changed)   [✅] star_h2   [✅] hygiene
  [✗] worktree —— 受控目录有未提交改动：M atoms/mem/ATOM-MEM-ALLOC-002.md;
                  M atoms/mem/ATOM-MEM-LEAK-002.md; M atoms/mem/ATOM-MEM-PERF-004.md

  [prepush] FAIL: 2 项未过，勿 push
```

* **`worktree ✗` 是我的疏漏**：任务D 改了三张卡却没提交（写完就去追 YAML 报错了），
  已被 prepush 抓到 ✓ —— 正是这道"受控目录必须干净"的闸门该干的事。
  补提交（`e60ed82`）后受控目录 **0 改动** ✓。
* **`quality ✗`**：见 §收工验收（复跑后回填）。

> 提示词说"任务A修完、任务B2人审后 push 应能过"——**B2 的 `--accept` 属人审权，本苦力未执行**，
> 故 Golden Lock 项在收工时**预期仍 FAIL**，这是设计使然，不是缺陷。

---

## 任务C：概念名归一（P1）

### C.1 新 `tools/concept_aliases.txt`（11 条别名，每条附词频证据）

```
内存屏障(fence) <- 栅栏, 内存栅栏, 屏障, memory fence, memory barrier, fence
互斥量(mutex) <- 互斥锁, mutex
内存序 <- 内存顺序, memory_order
happens-before <- happens before
```

**刻意未收**（逐条写明理由，防以后有人"看着像就加"）：

| 未收项 | 词频 Book//atoms | 理由 |
|---|---|---|
| `编译器屏障` / `硬件屏障` | 46/1、13/1 | **不是别名而是子类**——EV-CONC-002 明确区分 signal_fence=纯编译器屏障 / thread_fence=硬件屏障；归一会抹掉子类区别，正确表达是命题里的 `specializes` 关系 |
| `seq_cst` / `顺序一致性` | 461/0、4/0 | 是 `memory_order` 的**枚举值**（概念的取值），不是概念本身的另一种写法 |
| `原子性` / `原子操作` / `可见性` | 100/12、117/4、162/1 | **尚无规范概念**——概念层要有规范名才谈得上别名，留待回填时由人定 |
| `先行发生` / `内存隔离` | 0/0、1/0 | 零/极低频，无证据不动 |
| 提示词示例的裸 `锁` | 1845 | 绝大多数是"自旋锁/死锁/加锁"的一部分；收进来等于替作者把"锁"窄化成"互斥量"，属过度声称（铁律4） |

### C.2 归一机制（build + query 两条链路）

* `load_concept_aliases()` / `_alias_key()` / `_canon_concept()`：**整串精确匹配**
  （strip + ASCII casefold），**不做子串替换**——`锁` 是 `自旋锁` 的子串、`fence` 嵌在
  `atomic_signal_fence` 里，子串改写会制造胡说；概念名是命题级短语，只该整串认。
* `build()` 把 subject/object 归一后再入 `concept_edges`，并把 `aliases`/`alias_hits`
  写进 build 输出（**0 处也如实报**）。
* `concepts <名>` 查询侧同样走别名，命中时打印 `[别名解析：栅栏 → 内存屏障(fence)]`。

### C.3 归一前后（如实报告，含**预期偏差**）

| 项 | 值 |
|---|---|
| 概念节点数（**任务C 单测时**） | **3 → 3**（无变化，此时只有样板卡有命题） |
| 概念节点数（**任务 D/E 回填后**） | **3 → 41**，命题边 **2 → 21** ✓ |
| 别名归一命中 | **0 处**（表 11 条） |
| `concepts 栅栏` | 526 时"**查不到**" → 现在**命中** `内存屏障(fence)` 的 2 条命题（observation 1 / inference 1）✓ |
| tests | `tests/test_knowledge_graph.py` 6→**8 全过**（新增：命题用别名 → 入图归一为规范名；整串匹配边界 `自旋锁`≠`锁`、`atomic_signal_fence`≠`fence`、ASCII 大小写不敏感） |

**概念数增长的真实因果**（比提示词的预期更具体）：41 个概念来自**任务D/E 新增的 21 条命题**
（6 张卡 × 2-4 条），**不是**归一从 Book/ 吸收来的。也就是说 526 §八 说的
"从文件图长出概念图"这件事，**驱动力是"命题变多"**——归一只是保证增长时不分裂。
这条因果关系值得记住：想扩概念层，要去做**回填**（把 claim 拆成命题），而不是去改别名表。

> **与提示词的预期偏差（重要）**：提示词预期"归一后概念数会**从 Book 层吸收更多概念**"。
> 实际**不会**——概念层的数据源**只有带 `claim_structured` 的原子命题**（526 Step 4 的设计），
> Book/ 层没有任何命题，自然不进概念层。所以：
> * 本任务的价值在 **build/query 两条链路的归一机制 + 护栏**（回填者按 Book/ 口语写也不会分叉），
>   以及**修真了 526 报的那个具体痛点**（`concepts 栅栏` 查得到）；
> * "概念数增长"要等**回填铺开**（命题本身变多）才会发生，不是归一带来的。
> 若监工要的是"让 Book/ 的概念进图谱"，那是**另一个设计**（需要从教材正文抽概念，
> 属 526 §七"不做模型自动抽取"的范畴）——本批不擅自扩。

---

## 任务D：3 张 red-team 卡命题拆分（P1）

| 卡 | 命题数 | observation | inference（挂已登记独立基准） |
|---|---|---|---|
| `ATOM-MEM-ALLOC-002` | 3 | 2（统一口径读数 arena 32B/bitmap 181B/pool 8056B；随块数线性增长 8056→64056B） | 1（元数据开销与"是否支持单块释放"绑定 — ISO `[mem.res.monotonic.buffer]`/`[mem.res.pool]`） |
| `ATOM-MEM-LEAK-002` | 3 | 2（零依赖观测定性 cycle_live_objects=2 / LSan 报告随无关计数器从零报告变为 64 B leaked） | 1（判定应先于工具报告用零依赖观测 — LSan/ASan 文档可达性判据） |
| `ATOM-MEM-PERF-004` | 3 | 2（地址确定性判定 tight_same_line=1/padded_same_line=0；方向 sharing_is_slower=1 + 活性对照） | 1（"padding 一定值得"是过度概括 — ISO `[hardware.interference]` 提示值 + cppreference） |

* **inference 全部挂"卡上已登记的 `independent: true` 来源"** ⇒ 规则3 走**降级 warn** 而非 block
  （这就是 526 设计的降级通道在本批第一次被真实使用）。
* **未硬填**：三卡的 inference 都有 ISO/cppreference/impl_doc 级基准，**没有出现"纯作者推断无标准源"**
  的情形，故本批**没有**需要 `needs_human_review: true` 挂起的命题。
  （若将来遇到：**不要**把无基准的推断写成 `claim_type: inference`——那会撞规则3 block；
  也不要不写 `claim_type`——那会撞规则1。正确做法是留在 worklog 等人签，本批已验证这两条边界。）
* 实测：规则1/2 对三卡**0 命中**；规则3 **3 warn / 0 block**；gate **BLOCK=0**。

### D.4 自查抓到的一个真错误（值得记住）

给 `ATOM-MEM-LEAK-002` 写 prop-2 时，`statement` 里带了 LSan 原始报告的
`SUMMARY: AddressSanitizer: …`（**ASCII 冒号+空格**）⇒ `EV-FM-YAML-HARDENING` 立刻报
`[invalid] YAML 语法非法：mapping values are not allowed here`（YAML 纯标量不许含 `": "`）。
修法：该标量改用**双引号**（两个解析器都认）。**gate 抓到了我的错**——这条规则是有用的。

---

## 任务E：存量回填 3 张（P2）

选卡标准：STAGING 名单内 + 证据最多（各 3 张且全部带工件断言）+ claim 最长 + **已人签**
（这样加 inference 命题也不会产生规则3 warn）。

| 卡 | 命题数 | observation | inference |
|---|---|---|---|
| `ATOM-MEM-RAII-002`（Rule of 0/3/5） | 4 | 3（Zero 隐式语义按成员形状 / 只写析构致同缓冲两次析构 / noexcept 决定扩容搬迁路径） | 1（判据是"成员形状"而非口诀） |
| `ATOM-MEM-ALLOC-001`（allocator 策略抽象） | 4 | 3（allocate 不构造 / arena 接入 vector 零堆 / monotonic 零上游分配） | 1（allocator=内存策略抽象） |
| `ATOM-MEM-PERF-002`（SSO 阈值） | 3 | 1（max_zero_alloc_len=15 / first_heap_len=16）… 见下 | 1（SSO 是实现内建、阈值不可移植） |

* 所有 observation 读数**逐字取自证据卡的 `actual`/`artifact_assert`**（不引卡面散文里未落痕的数字）。
* 实测：三规则对三卡**全部 0 命中**；gate **WARN 57→54**（3 张退出 STAGING，且人签使规则3 不触发）。

### E.3 余下 20 张 backlog（下批继续，本批不做完）

```
 1. ATOM-CONC-LOCK-001     2. ATOM-CONC-RACE-001     3. ATOM-HIST-AUTOPTR-001
 4. ATOM-LANG-INLINE-001   5. ATOM-MEM-ALIGN-001     6. ATOM-MEM-LEAK-001
 7. ATOM-MEM-MOVE-002      8. ATOM-MEM-NEW-001       9. ATOM-MEM-PERF-001
10. ATOM-MEM-PERF-003     11. ATOM-MEM-RAII-001     12. ATOM-MEM-RVREF-001
13. ATOM-MEM-SHARED-001   14. ATOM-MEM-SHARED-002   15. ATOM-MEM-UNIQUE-001
16. ATOM-MEM-UNIQUE-002   17. ATOM-MEM-VALUE-001    18. ATOM-MEM-VALUE-002
19. ATOM-MEM-WEAK-001     20. ATOM-UB-GRAY-001
```
（数量校正：提示词说"剩下 23 张"，实为 **20 张**——全库 27 张 − 526 样板 1 − 任务D 3 − 任务E 3 = 20；
STAGING 名单 27 条里已回填 7 条。）

**优先建议**：`ATOM-MEM-PERF-001`（3 张证据、claim 短好拆）、`ATOM-LANG-INLINE-001`
（唯一 draft，尚无人工签——**它是最该先补人签再命题的**）、`ATOM-UB-GRAY-001`（UB 域唯一）。

---

## 收工验收（fresh run，全部实跑）

| 命令 | 实测 | 说明 |
|---|---|---|
| `golden_lock.py check` | **WORSE warn_findings: 32 → 54**（exit 1） | ✅ 预期如此——`--accept` 属人审权，本苦力未执行 |
| `poison_drill.py`（.venv） | **83/83** · RULE-COVERAGE 33/58 · exit 0 | 无 pyyaml 的 workbuddy 解释器下**同样 83/83**（任务A 修复前是 82/83） |
| `cppbible.py check --stage quality` | **26 passed / 1 failed**（唯一失败：**Golden Lock**） | 任务A 修复前是 **25/2**（Golden Lock + Poison Drill）✓ 修好了 |
| `knowledge_graph.py build && stats` | **323 节点 / 291 边 · 概念 41 / 命题边 21** | 概念 3→41 由任务D/E 的 21 条新命题带来 |
| `pytest -m fast` | **152 全绿**，exit 0 | — |
| 受控目录改动 | **0** | prepush 的 `worktree` 项已由补提交任务D 修复 |

**push 解锁判定**：除 Golden Lock（等人审 `--accept`）外**无其它阻塞**。
人审后按 §B2 的命令 accept（理由用** 32→54**），再跑 `prepush_check.py` 即得 9/9。

### 本批提交（6 个）

| commit | 内容 |
|---|---|
| `713d0c9` | 任务A：YAML 硬化不许静默跳过（根因修复 + 回归锁 + cppbible 失败摘要） |
| `d637fc1` | 任务C：概念别名归一（表 + build/query 两条链路 + 2 测试） |
| `e60ed82` | 任务D：3 张 red-team 卡命题化（+ 自查修掉的 YAML 冒号错误） |
| `a0582f2` | 任务E：3 张 mem 存量卡回填（+20 张 backlog） |
| `1cd675a` | 任务A 的连带修复：`ConstructorError` 改名遗漏导致的 NameError |

### 我的两个疏漏（如实记录）

1. **任务D 的三张卡漏提交**——写完就去追 YAML 报错了，被 `prepush_check` 的 `worktree` 项抓到 ✓
   （已补提交 `e60ed82`）。
2. **`ConstructorError` 改名遗漏**：任务A 把 `import ConstructorError` 改成 `_ctor_error`，
   但 `_UniqueKeyLoader` 内部仍用旧名 ⇒ dup-key 路径 `NameError`。
   我此前只跑了 `tests/test_gate_engine.py`，**没覆盖** `tests/test_p0d_hardening.py` ⇒
   是收工的 `pytest -m fast`（全量）才抓到的。**教训：改核心工具后要跑全量，不是只跑单个文件。**

### 明确未做（按提示词 §七）

* 未执行 `--accept`（人审权）/ 未 push
* 未一次回填 26 张（本批做 3 张，余 20 张进 backlog）
* 未改 Book/ 教学原文（只做图谱层归一）
* 未新增工具目录（都在 `gate_engine.py` / `knowledge_graph.py` / `cppbible.py` 现有文件里改）
