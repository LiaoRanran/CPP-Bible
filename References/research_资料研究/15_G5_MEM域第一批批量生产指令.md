# G5 MEM 域第一批批量生产指令（Writer Agent 专用）

> 自包含文档，可直接投喂执行 Agent。G5 首原子 RVREF-001 已 verified（5 分），本指令启动 MEM 域第一批剩余原子的完整流水线。
> 监工产出，2026-09-11。

---

## 一、你的角色

你是 **Writer Agent**，只负责写，不评判质量、不打 rubric 分（最高自评 4）。
写完后交 RedTeamer 攻击，你按缺陷修改，循环到 RedTeamer 无严重缺陷 → Gatekeeper 全绿 → 人审。

**禁止**：改 Book/ 原文、改已有 verified 原子、自置 verified 状态、自签 verified_by。

---

## 二、目标

产出 MEM 域第一批 **8 个原子**（已有 MOVE-002、RVREF-001 两颗 verified，本批补齐后 MEM 域共 10 颗）。
每个原子必须包含五件套：
1. 原子文档 `goldens/mem/{ATOM-ID}_draft.md`
2. 证据卡 `evidence/mem/EV-MEM-{NNN}.md`（至少 1 张，机制类必须 2 张：主论断 + 证伪对照/版本边界）
3. 实证夹具 `Examples/_atom_{name}.cpp`
4. 汇编工件 `Examples/_atom_{name}.asm`（如断言涉及汇编）
5. 运行输出（回填证据卡 actual 字段）

---

## 三、候选原子清单（按优先级排序）

### 必做（还债：已有原子的 relations 指向了它们，当前背 ATOM-REL-TARGET warn）

#### 1. ATOM-MEM-VALUE-001（值类别体系）
- **title**：C++ 的值不是"左/右"二分：lvalue / xvalue / prvalue / glvalue / rvalue 五分类
- **type**：mechanism
- **audience**：intermediate
- **claim**：C++11 起每个表达式属于两个正交维度的交叉：glvalue（有身份）vs rvalue（可移动）；lvalue = glvalue ∧ ¬rvalue，xvalue = glvalue ∧ rvalue，prvalue = ¬glvalue ∧ rvalue。`std::move(x)` 把 lvalue 转为 xvalue（不是 prvalue），临时对象是 prvalue。
- **relations**：prerequisite → 无（这是基础）；contrasts → ATOM-MEM-MOVE-002
- **证据卡需求**：用 `decltype` 推导不同表达式的值类别（`decltype(x)` 对 lvalue 返 T&、对 xvalue 返 T&&、对 prvalue 返 T），static_assert 编译期证明
- **参考**：ISO [basic.lval]、MOVE-002 原子

#### 2. ATOM-MEM-PERF-001（移动语义性能量化）
- **title**：移动比拷贝快多少？用字节搬运量和分配次数量化
- **type**：pitfall
- **audience**：intermediate
- **claim**：移动构造的收益来自"掏空源对象"——只搬指针（8 字节）并置空源，vs 纯值类型必须搬全部数据（如 32 字节 SIMD）。对无动态资源的类型，移动 = 拷贝，std::move 无收益。
- **relations**：prerequisite → ATOM-MEM-MOVE-002；contrasts → ATOM-MEM-MOVE-002
- **证据卡需求**：汇编层量化——移动构造的指令数/字节搬运量 vs 拷贝构造；运行时分配次数对比（EV-MEM-001 已有基础，可扩展）
- **参考**：EV-MEM-001（移动不分配堆内存）、MOVE-002 原子

### 高优先级（MEM 域核心知识点）

#### 3. ATOM-MEM-RAII-001（RAII 与异常安全）
- **title**：RAII 不是"智能指针"：构造获取资源、析构释放，异常路径也不泄漏
- **type**：mechanism
- **audience**：beginner
- **claim**：RAII 的核心是把资源生命周期绑定到对象生命周期——构造函数获取资源、析构函数释放，栈展开时析构自动调用，即使异常也不泄漏。lock_guard、unique_ptr、vector 都是 RAII。
- **relations**：prerequisite → 无（beginner 级）
- **证据卡需求**：异常抛出后，栈上 RAII 对象的析构被调用（打印日志证明），而裸 new/delete 在异常路径泄漏
- **参考**：ISO [except.ctor]、Book 异常安全章节

#### 4. ATOM-MEM-UNIQUE-001（unique_ptr 所有权转移）
- **title**：unique_ptr 是"移动-only 的 RAII 包装"：拷贝被删除、转移靠 move
- **type**：mechanism
- **audience**：intermediate
- **claim**：unique_ptr 独占所有权，拷贝构造/拷贝赋值被 = delete；所有权转移只能通过 move（std::move 或 return）。自定义 deleter 影响大小和语义（无状态 deleter 空基类优化 → 零开销；有状态 deleter 增加存储）。
- **relations**：prerequisite → ATOM-MEM-RAII-001、ATOM-MEM-MOVE-002
- **证据卡需求**：static_assert 证明 is_copy_constructible<unique_ptr<T>> = false；汇编证明无状态 deleter 的 unique_ptr 大小 = 裸指针（8 字节）
- **参考**：ISO [unique.ptr]、MOVE-002

#### 5. ATOM-MEM-SHARED-001（shared_ptr 引用计数与控制块）
- **title**：shared_ptr 是"两个指针"：对象指针 + 控制块指针，引用计数在控制块里
- **type**：mechanism
- **audience**：intermediate
- **claim**：shared_ptr<T> 大小 = 2 个指针（16 字节），一个指向对象、一个指向控制块（含引用计数、弱计数、deleter、分配器）。拷贝 shared_ptr 是原子递增引用计数（RMW，有 cache 开销）；最后一个 shared_ptr 析构时销毁对象，最后一个 weak_ptr 析构时释放控制块。
- **relations**：prerequisite → ATOM-MEM-UNIQUE-001
- **证据卡需求**：sizeof(shared_ptr<int>) = 16 静态断言；汇编证明拷贝 shared_ptr 生成 lock inc 或 atomic fetch_add；运行时证明引用计数变化
- **参考**：ISO [util.smartptr.shared]、folly Hazptr（对比：HP 是无锁回收，shared_ptr 是引用计数回收）

#### 6. ATOM-MEM-WEAK-001（weak_ptr 打破循环引用）
- **title**：weak_ptr 是"不延长寿命的观察者"：专门打破 shared_ptr 循环引用
- **type**：pitfall
- **audience**：intermediate
- **claim**：weak_ptr 不增加引用计数，只增加弱计数；通过 lock() 临时获得 shared_ptr（如果对象还活着）。parent→child 用 shared_ptr、child→parent 必须用 weak_ptr，否则循环引用导致内存泄漏。
- **relations**：prerequisite → ATOM-MEM-SHARED-001
- **证据卡需求**：循环引用场景（A→B shared、B→A shared）的内存泄漏演示（析构不被调用）；改用 weak_ptr 后析构正常调用
- **参考**：ISO [util.smartptr.weak]

#### 7. ATOM-MEM-NEW-001（new/delete 分层）
- **title**：new 表达式做两件事：operator new 分配内存 + 构造函数初始化；delete 反过来
- **type**：mechanism
- **audience**：intermediate
- **claim**：`T* p = new T()` = ①调用 operator new(sizeof(T)) 分配原始内存 ②在该内存上调用 T 的构造函数。`delete p` = ①调用析构函数 ②调用 operator delete 释放内存。operator new/delete 可被替换/重载，这是 allocator 和内存池的基础。placement new 在已分配内存上构造对象。
- **relations**：prerequisite → ATOM-MEM-RAII-001
- **证据卡需求**：重载 operator new/delete 打印分配/释放日志，证明 new 表达式的两步；汇编证明 new 生成 call _Znwm + 构造调用
- **参考**：ISO [expr.new]、[expr.delete]、[support.dynamic]

#### 8. ATOM-MEM-ALIGN-001（对齐与 padding）
- **title**：struct 大小不是字段之和：对齐填充、空基类优化、[[no_unique_address]]
- **type**：pitfall
- **audience**：beginner
- **claim**：结构体大小受对齐约束——每个字段偏移必须是其对齐的整数倍，末尾填充到最大对齐的整数倍。空基类在继承时大小为 0（空基类优化 EBO），但作为成员时占 1 字节；C++20 [[no_unique_address]] 让空成员也不占空间。
- **relations**：prerequisite → 无（beginner 级）
- **证据卡需求**：static_assert 证明不同字段顺序的 struct 大小不同；offsetof 证明 padding 位置；汇编证明 EBO 后的派生类大小 = 数据成员大小
- **参考**：ISO [basic.align]、[class.derived]、CPP-Bible ch21（const 族深耕章，已 verified）

---

## 四、生产流程（每个原子严格按此走）

### Step 1：Writer 写初稿
- 从 Book 对应章节提取内容（不要凭空写，先 `grep` 关键词定位章节）
- 写原子 frontmatter（严格按 G1_layout.md 字段：id/title/domain/type/audience/cognitive_load/prerequisites_readable/status/claim/claim_boundary/relations/evidence/sources/misconceptions/superiority/depth）
- 写正文四段式：主张 → 为什么（直觉/类比）→ 怎么做（代码示例）→ 例外/边界
- 写证据卡 + 夹具
- Writer 自评 rubric（最高 4，不给 5）

### Step 2：RedTeamer 攻击（你自己扮演，但必须独立、不留情）
按 8 条语义红队清单逐条检查：
1. 标准版本边界：C++11/14/17/20/23 下是否一致？
2. 断言-证据同代：改了 .cpp 或卡里计数，工件重生成了吗？sha256 换了吗？
3. 零观测伪证据：输出符合预期，但汇编里能找到观测通路吗？
4. 自身 UB：夹具自己有没有踩 UB？sanitizer 过了吗？
5. 证伪对照：实验有区分力吗？
6. 跨编译器：GCC 成立的，Clang 成立吗？
7. 术语精确：unspecified / undefined / implementation-defined 用对了吗？
8. 过度简化："不该用"有没有漏掉重要例外？

输出缺陷报告（严重/一般/建议），然后**自己修改**（G5 初期 Writer/RedTeamer 同一 Agent，但必须分两轮、留痕）。

### Step 3：Gatekeeper 机器验证
```powershell
.venv\Scripts\python.exe tools\atom_evidence_replay.py --check
.venv\Scripts\python.exe tools\gate_engine.py --check
.venv\Scripts\python.exe tools\golden_lock.py check
.venv\Scripts\python.exe tools\poison_drill.py
.venv\Scripts\python.exe -m pytest tests\ -q
```
全绿才进下一步。warn 如果是预期债务（如 relations 指向尚未锻造的原子），用 `golden_lock.py --accept "理由"` 留痕后 sync。

### Step 4：提交
- 中文 commit message 走 `-F` UTF-8 文件
- 推送前跑 WSL 预检（`tools/ci_local_precheck.py`）
- 每个原子一个提交，不要混在一起

---

## 五、证据卡硬性要求（M2 规范）

1. **必须有证伪对照**：恒真测试会"证实"一切。例如证明"移动不分配"，必须有一个"假移动"对照（如 CopyOnly 类型）输出分配=1。
2. **计数/计时类实验双跑**：-O0 与 -O2，计数器 volatile。汇编层找不到调用点却"证实"了 = 伪证据。
3. **汇编断言只锚定跨平台稳定特征**：符号存在性（如 `_ZNSt8auto_ptr`），不写死调用次数（GCC 15.3=3 次、13.1=4 次）。
4. **command 产物写 build/**：路径正斜杠，不要在仓库根留 a.exe。
5. **UB 类证据卡必须在 WSL/Linux 侧过 sanitizer**：Windows MinGW 无 libasan。
6. **工件与断言同代**：改 .cpp → 重生成 .asm → 换 sha256。旧工件 hash vs 旧记录 hash 一致 ≠ 复现性。
7. **双编译器边界**：GCC + Clang 双编译器实测（Clang 列走 CI Gray-zone Matrix 的 notice 注解回填）；MSVC 以标准条文代替。
8. **版本边界**：论断涉及版本差异的（如 return x; 的隐式移动 C++17 vs C++20），必须补版本卡。

---

## 六、frontmatter 字段速查（G1_layout.md）

```yaml
---
id: ATOM-MEM-{NAME}-{NNN}
title: （一句话主张，不是名词短语）
domain: MEM
type: mechanism | pitfall | contrast | evolution | rule
audience: beginner | intermediate | expert
cognitive_load: low | medium | high
prerequisites_readable: true | false
status: draft              # 你只写 draft，verified 由人审签署
claim: >-
 （核心论断，可证伪，含版本边界声明）
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0, GCC 13.1.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-XXXX}
  - {type: contrasts, target: ATOM-MEM-XXXX}
evidence:
  - EV-MEM-{NNN}
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [条款]", independent: true}
misconceptions: [MIS-MEM-{NNN}]   # 引用全局误解库 ID（如尚未建库，先写文本，标注 TODO）
superiority: >-
 （与现有资料的差异，禁词：更详细/更全面/帮助理解）
depth:
  layer: 2 | 3 | 4
  anchors: [ISO 条款, 证据卡 ID, 汇编行号]
---
```

---

## 七、血泪铁律（G1-G4 全部踩坑积累，违反即打回）

1. **工件必须与断言同代**——改 .cpp 或卡里计数 → 重生成 .asm → 换 sha256
2. **验证不带 PATH 前置**——手动跑命令不要前置编译器路径，那会掩盖缺陷
3. **硬编码期望会被 S3 拦**——期望片段出现在夹具字符串字面量里 = 作弊级
4. **查同名必须 rglob**——新建文件前 `Get-ChildItem -Recurse -Filter "*.py"` 查全仓库
5. **中文提交走 -F**——commit message 写进 UTF-8 文件，`git commit -F msg.txt`
6. **不要预设汇编里有什么**——先看工件再写断言，-O2 可能内联一切
7. **标准版本边界**——用旧规则套新标准是最严重的语义错误
8. **relations 先确认目标存在**——指向尚未锻造的原子会背 ATOM-REL-TARGET 债
9. **异构环境不污染工件**——WSL 跑 replay 会换 MinGW 的 .asm，replay 已有快照还原
10. **gray_zone 术语精确**——unspecified / undefined / implementation-defined 不是措辞差异

---

## 八、可用资产

| 资产 | 路径 | 用途 |
|---|---|---|
| 黄金模板 A（mechanism） | goldens/A_move.md | mechanism 型参照 |
| 黄金模板 B（contrast） | goldens/B_eval_order.md | contrast 型参照 |
| 黄金模板 C（evolution） | goldens/C_auto_ptr.md | evolution 型参照 |
| MEM 已验证原子 | atoms/mem/ATOM-MEM-MOVE-002.md | 移动语义，5 分 |
| MEM 已验证原子 | atoms/mem/ATOM-MEM-RVREF-001.md | 右值引用形参，5 分 |
| 原子规范 | docs/kernel/G1_layout.md | frontmatter + 正文结构 |
| 实证方法 | docs/kernel/M2_empirical.md | 证据卡格式 |
| 门禁规则 | docs/kernel/M4_gate_engine.md | 29 条规则 |
| 制衡层 | docs/kernel/S1_S6_controls.md | S1-S6 |
| 工具 | tools/ | replay/gate/golden/poison/m5 |
| 来源库 | 桌面 cppb参考资料/ | 22 本书 + WG21 + eel.is |
| 调研成果 | References/11, 12, 13 | 内存模型/RCU/无锁数据结构 |

---

## 九、完成标准

本批 8 个原子全部满足：
- [ ] 每个原子五件套齐全（原子文档 + ≥1 证据卡 + 夹具 + 工件 + 运行输出）
- [ ] evidence replay 全 confirm（新增卡全部通过）
- [ ] gate_engine block=0（warn 是预期债务且已 --accept 留痕）
- [ ] golden_lock 无恶化
- [ ] poison_drill 4/4
- [ ] pytest 全过
- [ ] 每个原子一个提交，WSL 预检通过后推送
- [ ] 向监工报批次验收报告（每原子 rubric 自评 + RedTeamer 缺陷数 + 门禁结果）

**完成后停在人审门口，不要自置 verified。**

---

*本指令由监工基于 G1-G4 全部经验 + G5 开工指令 + 三轮并发调研整理。执行中遇到未覆盖情况，按"能机器判定的不靠人记、能复现的不口头声称、语义终审权在人"三条原则处理。*
