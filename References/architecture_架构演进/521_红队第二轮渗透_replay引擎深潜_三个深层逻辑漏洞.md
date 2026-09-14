# 521 红队第二轮渗透 · replay引擎深潜 · 三个深层逻辑漏洞

> 日期：2026-09-14
> 上一轮520找了4个表层漏洞（S1自证/warn基线/静态分析/工具债）。
> 这一轮钻到replay引擎源码里，找更深的逻辑漏洞。

---

## 一、Replay四层验证链的完整拆解

Replay跑一张卡的完整流程：

```
① 解析frontmatter → 检查必填字段（command/artifact/sha/run_*）
② 跑command → 拿stdout
③ run_match → 程序输出 == .out文件里的key=value？
④ artifact_sha → 重生成的工件sha == 卡上的sha？
   4a. 同编译器 → sha强制校验
   4b. 跨编译器 → 降级走artifact_assert结构断言
   4c. P0-A重编译不变量 → 独立重编译再比对sha
```

---

## 二、三个深层漏洞

### 漏洞5：整个replay假设"command是可信的"，但从未验证command和claim的关系 🔴

**位置**：整个replay流程

**问题**：
Replay验证了：
- 程序输出和.out一致
- 工件sha和卡上一致
- 重编译不变量

但**没有验证command本身做的事和原子的claim有关**。

**攻击路径**：
1. 想写一个关于"内存泄漏"的原子
2. 写一个完全不相关的command：`echo "leak_detected=1"`
3. .out文件也写`leak_detected=1`
4. artifact随便生成一个空的.asm
5. artifact_assert写`contains_in: ["leak"]`——但asm是空的...

等等，artifact_assert会拦。让我想一个更实际的攻击：

**实际攻击路径**：
1. 夹具是一个C++程序，输出"a=1 b=2"
2. claim写"这个程序演示了X"
3. 但实际上这个程序和X完全无关
4. replay全绿，因为它只验证"程序输出和.out一致"

**谁来拦？**
- gate_engine的55条规则全是格式检查
- 只有红队盲读能发现"claim和代码不匹配"

**这就是为什么7轮对抗后，系统依然靠人审**——机器验证不了语义。

**修补方向**（但不是现在）：
- 未来加"claim-code一致性检查"——这需要LLM，不是纯规则
- 现在能做的：在replay里加一个warning"你确认command和claim有关吗？"——但这只是提醒，不是阻断

---

### 漏洞6：P0-A重编译不变量对构建脚本卡直接跳过，且是fail-open不是fail-closed 🟡

**位置**：`_recompile_invariant()`（line 1104）

**实现**：
```python
lines = _artifact_compile_lines(cmd, art_rel)
if not lines:
    return "unavailable", "..."
    # → infra_error:recompile_unavailable
```

**问题**：
`_artifact_compile_lines()`只找command里直接的`g++ -o xxx.asm`行。

如果command是：
```
make -f Makefile.atom && ./postprocess.sh
```

那找不到直接编译行 → 返回`unavailable` → `infra_error:recompile_unavailable`。

**但这不是逃逸**——infra_error是fail-closed（exit 1）。

等等，让我再读一下...它确实返回infra_error，exit 1。所以构建脚本卡**根本跑不过replay**。

**这才是真正的问题**：
- 想写一个用make的多TU原子？
- replay直接infra_error:recompile_unavailable
- 你必须改成直接`g++ -o a.asm && g++ -o b.asm`的形式

**这限制了夹具的表达能力**——不能用构建系统。

**修补方向**：
- P1：`_artifact_compile_lines()`支持`make`/`cmake`的解析（从Makefile里找编译行）
- 或者：P0-A重编译不变量对构建脚本卡降级为warn（只提醒，不阻断）

---

### 漏洞7：跨编译器路径的artifact_assert可以用"恒真符号"逃逸，且判别力检查只覆盖contains_in不覆盖contains_any 🔴

**位置**：`check_artifact_assert()`（line 623）

**实现**：
跨编译器路径不检查sha，改走artifact_assert：
- `contains_in: {symbol, region}` — 检查符号在某个函数区间内
- `absent_in: {symbol, region}` — 检查符号不在某个区间内
- `contains_any: [symbols]` — 检查任一符号存在

**漏洞**：
判别力证明（N≥2次出现的检查）只覆盖`contains_in`和`absent_in`。

**`contains_any`完全没有判别力检查**。

**攻击路径**：
1. 写一个`contains_any: [".file", ".section"]`的断言
2. 任何gcc -S产出的asm都有.file和.section
3. 跨编译器路径 → artifact_assert通过 → confirm

**这就是E03的变种**——但E03当时只修了contains_in，漏了contains_any。

**修补**：
- P0：把判别力检查扩展到`contains_any`
- P1：`contains_any`里的每个符号都要检查"是否在双平台都恒真"

---

## 三、Rerun一遍520的4个漏洞

| 漏洞 | 520说的 | 本轮深潜后的修正 |
|---|---|---|
| 1. S1字符串自证 | 谁都能写human:xxx | 正确，且git author binding是宽松匹配 |
| 2. warn基线膨胀 | 32条warn永久基线 | 正确，且没有过期机制 |
| 3. 全是静态分析 | 不验证程序行为 | **部分修正**：replay其实验证了运行时输出（run_match）和工件sha（重编译不变量）。但不验证"行为和claim有关" |
| 4. 工具债无管理 | 100个工具不知道谁在用谁 | 正确，且tools/legacy/已经有4个死代码 |

---

## 四、漏洞优先级重排

| # | 漏洞 | 严重度 | 修补工作量 |
|---|---|---|---|
| 7 | contains_any无判别力检查 | 🔴 P0 | 1h（加检查逻辑） |
| 1 | S1字符串自证 | 🔴 P0 | 3h（verified_by改git提取） |
| 6 | 构建脚本卡replay失败 | 🟡 P1 | 2h（make解析或降级warn） |
| 5 | claim-code语义不匹配 | 🔴 P0 | 不能机器修，靠红队 |
| 2 | warn基线膨胀 | 🟡 P1 | 2h（加过期机制） |
| 4 | 工具债无管理 | 🟡 P1 | 4h（调用关系图） |

---

## 五、架构完善建议

### 5.1 立刻修（P0，1个苦力批次）

1. **contains_any判别力检查**：把contains_in的N≥2次检查逻辑复制到contains_any
2. **S1 verified_by改git提取**：不再接受手写，自动从git commit提取
3. **加一个"语义一致性warning"**：replay跑完后，打印"你确认command和claim有关吗？"——不阻断，但提醒

### 5.2 下一批修（P1，1个苦力批次）

4. **构建脚本卡降级**：P0-A重编译不变量对make/cmake卡降级为warn（不是infra_error）
5. **warn基线过期机制**：warn超过3个月自动升为block
6. **工具调用关系图**：tool_integrity扩展，自动生成依赖图

### 5.3 长期方向（好模型）

7. **claim-code一致性检查**：用LLM判断"这个claim和这段代码是否相关"——这是真正的"智能"层，纯规则做不到

---

## 六、红队元结论（第二轮）

**第一轮520的结论**：格式门禁强，逻辑门禁弱。
**第二轮修正**：
- 逻辑门禁其实比想象的强——replay做了4层验证（输出/sha/重编译/sanitizer）
- 真正的缺口是**语义层**——机器验证不了"这个实验证明了什么claim"
- 这不是漏洞，是边界。纯规则系统能做到这步已经不错了

**真正该怕的**：
- 不是"聪明的攻击者绕过规则"（7轮对抗已经抓得差不多了）
- 而是"系统越来越复杂，但没人真正理解它在做什么"

**这就是为什么247份架构文档本身就是问题**——写文档的速度超过了执行的速度，系统复杂度超过了人脑能理解的范围。

**下一步不是再加规则，是让现有的规则更鲁棒**：
- 修contains_any逃逸
- 修S1自证
- 让构建脚本卡能跑
- 然后停下来，跑一周，看看系统会不会自己出问题

---

*文档编号 521。这是第二轮红队，钻到replay引擎源码。共7个漏洞，P0有3个。*
