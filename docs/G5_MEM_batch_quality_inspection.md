# 质量质检报告 · G5 MEM 域第一批批量生产（8 原子）

> 监工独立复跑 · 2026-09-11 · 范围：goldens/mem/ATOM-MEM-*_draft.md × 8 + evidence/mem/EV-MEM-006..020 × 15（新卡）
> 机器门禁全部独立复跑，不采信执行 Agent 自报。

---

## 一、机器门禁（监工独立复跑）

| 门禁 | 执行 Agent 自报 | 监工独立复跑 | 结论 |
|---|---|---|---|
| `atom_evidence_replay.py --check` | confirm=20/refute=0 | **confirm=23/refute=0**（含 3 张 UB 存量卡） | ✅ 一致且更全 |
| `gate_engine.py --check`（29 规则） | block=0, warn=22 | **block=0, warn=22**（全 EV-SERVES-EXIST 预期债务） | ✅ 一致 |
| `golden_lock.py check` | 恶化 0 | **恶化 0 · 改善 0** | ✅ 一致 |
| `poison_drill.py` | 4/4 | **4/4**（P1/P2/P3 拦截 + 阴性放行） | ✅ 一致 |

**门禁结论：全部通过，无假阳性。**

---

## 二、五重剖面完整性（8/8 逐颗核查 frontmatter）

| 原子 | 多源精炼 | 一手实证 | superiority | depth 纵深 | 教学封装 |
|---|---|---|---|---|---|
| VALUE-001 | ✅ 2iso+cppref | ✅ EV-006/007 | ✅ 具体增量 | ✅ compiler层 | ✅ 动机+误解+3问+预测 |
| PERF-001 | ✅ 1iso+cppref | ✅ EV-008/001/002 | ✅ 量化+三判据 | ✅ asm层 | ✅ 完整 |
| RAII-001 | ✅ 2iso+cppref | ✅ EV-009/010 | ✅ 观测事实 | ✅ runtime层 | ✅ 完整 |
| UNIQUE-001 | ✅ 2iso+cppref | ✅ EV-011/012 | ✅ 零开销实证 | ✅ compiler层 | ✅ 完整 |
| SHARED-001 | ✅ 2iso+cppref | ✅ EV-013/014 | ✅ 证伪自带修复 | ✅ runtime层 | ✅ 完整 |
| WEAK-001 | ✅ 2iso+cppref | ✅ EV-015/016 | ✅ 对照卡 | ✅ runtime层 | ✅ 完整 |
| NEW-001 | ✅ 2iso+cppref | ✅ EV-017/018 | ✅ 两层可观测 | ✅ runtime层 | ✅ 完整 |
| ALIGN-001 | ✅ 2iso+cppref | ✅ EV-019/020 | ✅ padding量化 | ✅ compiler层 | ✅ 完整 |

**五重剖面 8/8 全部齐全，无缺项。**

---

## 三、证据卡抽样质检（2/20 深度读）

### EV-MEM-009（RAII 异常路径）—— 红队曾抓硬编码
- ✅ 硬编码问题已修复：`expected.run` 是描述性文字，`actual.run` 是机器输出 `after safe_path g_live=0|after leak_path g_live=1`
- ✅ `g_live` 是 volatile 计数（不是字符串字面量），S3-EXPECTED-HARDCODED 不再触发
- ✅ 双向证伪条件齐全（RAII 不归 0 / 裸路径归 0 均 refute）
- ✅ 负观测诚实（泄漏 = g_live 留 1，不是"没看到就当没事"）

### EV-MEM-014（shared_ptr 循环引用泄漏）
- ✅ 证伪对照自带：`nodes destroyed count=0` 直接推翻"shared 总是安全"
- ✅ 指向修复路径：明确给出 weak_ptr（ATOM-MEM-WEAK-001）
- ✅ 反向证伪条件：去掉循环则 destroyed=2

**抽样结论：证据卡质量高，红队打磨痕迹真实可见。**

---

## 四、缺陷清单

### ❌ 一般缺陷（1 条）

1. **[一般] RAII-001 引用不存在的误解 ID**
   - 定位：`goldens/mem/ATOM-MEM-RAII-001_draft.md:43` — `misconceptions: [MIS-MEM-009, MIS-MEM-010]`
   - 问题：`misconceptions/` 目录只有 `MIS-MEM-001` 到 `MIS-MEM-009`，**MIS-MEM-010 不存在**
   - 影响：教学封装字段引用悬空，读者点击 MIS-MEM-010 无对应文件
   - 修复方案：① 新建 `MIS-MEM-010.md`（RAII 相关误解，如"析构只在正常路径调用"）；或 ② 改为已存在的 ID（如 MIS-MEM-003/004/006/007/008 中匹配的）
   - 不阻断：不影响机器门禁（gate_engine 不校验误解 ID 存在性），但影响教学封装完整性

### ⚠️ 建议项（3 条）

2. **[建议] 原子化必须按依赖顺序**
   - 依赖链：RAII-001 → NEW-001 / UNIQUE-001 → SHARED-001 → WEAK-001
   - SHARED-001 的 prerequisite 指向 UNIQUE-001，WEAK-001 指向 SHARED-001——两者都在同批 goldens/
   - gate_engine 只扫 atoms/ 不扫 goldens/，所以现在不报 ATOM-REL-TARGET；原子化时若顺序错误会触发
   - 建议原子化顺序：RAII → NEW/UNIQUE（可并行）→ SHARED → WEAK；VALUE/PERF/ALIGN 可随时并行

3. **[建议] ALIGN-001 误解 ID 匹配度存疑**
   - 定位：`ATOM-MEM-ALIGN-001_draft.md:42` — `misconceptions: [MIS-MEM-002]`，注释写"对象布局/对齐相关误读（如有专门条目）"
   - "如有专门条目"暗示 Writer 不确定 MIS-MEM-002 是否真的覆盖对齐主题
   - 建议：人审时确认 MIS-MEM-002 内容，若不匹配则新建对齐专用误解条目

4. **[建议] claim_boundary 缺 Clang 列**
   - 8 颗原子的 `claim_boundary.compilers` 均只有 `[GCC 15.3.0]`
   - M2 §2 永久边界要求"GCC + Clang 双编译器实测"主要针对 UB/灰区类；mechanism 类可接受单编译器
   - 但建议在卡侧标注"Clang 列待 CI 回填"，与 B/C 样板的做法一致

---

## 五、术语冲突检查

对照 `docs/kernel/G1_terminology.md`：
- 值类别（组 3）：`std::move = 无条件转 xvalue` — 与 VALUE-001 / MOVE-002 一致 ✅
- RAII / unique_ptr / shared_ptr / weak_ptr / 对齐 / new-delete：术语表未收录这些具体术语（属扩展术语，无冲突）✅
- **无术语冲突。**

---

## 六、Rubric 复评

| 原子 | Writer 自评 | 监工复评 | 依据 |
|---|---|---|---|
| VALUE-001 | 4/5 | **4/5** | 五分类 decltype 硬证明 + xvalue 证伪卡，结构清晰 |
| PERF-001 | 4/5 | **4/5** | 移动性能量化 + 三判据 + asm 层互证，type=pitfall 合理 |
| RAII-001 | 4/5 | **4/5** | 异常路径 g_live 观测 + 逆序析构，beginner 入口定位准 |
| UNIQUE-001 | 4/5 | **4/5** | sizeof 零开销 + 拷贝删除编译错误文本坐实 |
| SHARED-001 | 4/5 | **4/5** | 引用计数可观测 + 循环泄漏证伪自带修复路径 |
| WEAK-001 | 4/5 | **4/5** | 与 EV-014 同结构对照卡，weak 打破循环可证 |
| NEW-001 | 4/5 | **4/5** | 两层分离可观测 + sized-delete 坑诚实留痕 |
| ALIGN-001 | 4/5 | **4/5** | padding 三数量化 + memcpy 安全 vs 强转 UB |

**监工复评 8/8 均为 4/5（Agent 最高自评上限），达到"完整有据"标准。**
**是否授 5 分：唯人审决定。** 监工不自主打 5 分。

---

## 七、存量债务区分

| 债务 | 数量 | 性质 | 清零时机 |
|---|---|---|---|
| EV-SERVES-EXIST | 12 | **本批新建**（草稿在 goldens/，证据卡服务的原子未进 atoms/） | 原子化时自动清零 |
| ATOM-REL-TARGET | 4 | **历史遗留**（MOVE-002→VALUE/PERF、UB-GRAY→ALIAS/DEF） | 锻造目标原子时清零 |
| MIS-MEM-010 悬空 | 1 | **本批新建缺陷** | 修复 RAII-001 引用或新建误解条目 |

---

## 八、放行结论

**有条件通过。**

- ✅ 机器门禁全绿（replay 23/0 · gate block=0 · golden 恶化 0 · poison 4/4）
- ✅ 五重剖面 8/8 齐全
- ✅ 证据卡抽样质量高，红队打磨痕迹真实
- ✅ 无术语冲突
- ❌ 1 条一般缺陷：RAII-001 引用不存在的 MIS-MEM-010
- ⚠️ 3 条建议：原子化依赖顺序、ALIGN 误解匹配、Clang 列标注

**放行条件**：修复 MIS-MEM-010 缺陷（新建条目或改引用）后，8 颗原子可进入人审流程。人审通过后按依赖顺序原子化进 `atoms/mem/`。

**监工不自主授 5 分、不自主置 verified。** 8 颗均为 draft 状态，verified 唯 human:liaoranran 可签署。
