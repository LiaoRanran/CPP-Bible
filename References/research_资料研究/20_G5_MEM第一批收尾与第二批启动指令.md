# G5 下一轮指令：MEM 第一批收尾 + 第二批启动

> 2026-09-11 · 给执行 Agent（Writer/Gatekeeper 角色）· 监工质检已完成，有条件通过。

---

## 一、当前状态（接地，不要假设）

- 第一批 8 颗 MEM 原子草稿在 `goldens/mem/`（VALUE/PERF/RAII/UNIQUE/SHARED/WEAK/NEW/ALIGN），全部 draft，Writer 自评 4/5
- 20 张证据卡 `evidence/mem/EV-MEM-001..020`，replay confirm=23/0（含 3 张 UB 存量卡）
- 监工质检报告：`docs/G5_MEM_batch_quality_inspection.md`——有条件通过，1 条一般缺陷 + 3 条建议
- 机器门禁：gate block=0 · golden 恶化 0 · poison 4/4
- 本地 ahead 9（origin/master 还在 c2ac07b），References/11-19 共 9 份调研文档未 commit

---

## 二、第一步：修复质检缺陷（必须先做）

### 缺陷 1（一般）：RAII-001 引用不存在的 MIS-MEM-010

- 定位：`goldens/mem/ATOM-MEM-RAII-001_draft.md:43` — `misconceptions: [MIS-MEM-009, MIS-MEM-010]`
- 问题：`misconceptions/` 只有 MIS-MEM-001 到 009，MIS-MEM-010 不存在
- 修复方案（二选一，你判断哪个更合理）：
  - **A**：新建 `misconceptions/MIS-MEM-010.md`，主题为"析构函数只在正常返回路径调用，异常路径跳过"（RAII 核心误解），按现有 MIS-MEM-*.md 的格式写
  - **B**：把 RAII-001 的引用改为已存在的匹配 ID（先读 `misconceptions/MIS-MEM-003/004/006/007/008.md` 看哪个覆盖"异常路径资源泄漏"主题，选最匹配的）
- 选 A 还是 B：如果现有 003-008 中有精确匹配"异常路径跳过析构/泄漏"的就选 B，否则选 A 新建
- 修复后重跑 `gate_engine.py --check` 确认无新增 block

### 建议项（顺手做，不强制）

- ALIGN-001 的 `misconceptions: [MIS-MEM-002]` 注释写"如有专门条目"——读 MIS-MEM-002 确认是否覆盖对齐/padding 主题；若不匹配，新建对齐专用误解条目或改引用
- 8 颗原子的 `claim_boundary.compilers` 只有 GCC 15.3.0——在证据卡侧补一行注释"Clang 列待 CI 回填"（与 B/C 样板做法一致），不需要真跑 Clang

---

## 三、第二步：等待人审（你不能代审）

- 8 颗原子的 `status: draft` → `verified` **唯 human:liaoranran 可签署**，你不得自置
- 人审通过后，用户会告诉你"签了"或给出具体签署指令
- 在人审结果出来之前，**不要原子化、不要改 status**
- 人审可能要求修改某些原子——如果有修改意见，按意见修改后重新跑门禁，再等人审

---

## 四、第三步：人审通过后原子化（按依赖顺序）

### 依赖链（必须遵守）

```
RAII-001（无前置，beginner 入口）
  ├── NEW-001（prerequisite → RAII-001）
  └── UNIQUE-001（prerequisite → RAII-001）
        └── SHARED-001（prerequisite → UNIQUE-001）
              └── WEAK-001（prerequisite → SHARED-001）

VALUE-001（contrasts → MOVE-002，已原子化，可并行）
PERF-001（prerequisite → MOVE-002，已原子化，可并行）
ALIGN-001（无前置，可并行）
```

### 原子化操作（每颗）

1. `git mv goldens/mem/ATOM-MEM-XXX-001_draft.md atoms/mem/ATOM-MEM-XXX-001.md`（保留历史）
2. frontmatter：`status: draft` → `verified` + `verified_by: human:liaoranran` + `verified_at: 2026-09-11`（日期以实际人审日为准）
3. 如果人审授 5 分，rubric 自评改为 `5/5（人审授予）` 并补锚定依据
4. 每原子化一颗后跑 `gate_engine.py --check`，确认 ATOM-REL-TARGET 不新增（因为按依赖顺序，目标应该已存在）
5. 全部原子化后跑 `golden_lock.py sync`——EV-SERVES-EXIST 债（12 条）应自动清零
6. 顺带：VALUE-001/PERF-001 原子化后，MOVE-002 的 ATOM-REL-TARGET 存量债（指向 VALUE/PERF）自动清零

### 原子化顺序建议

```
批次 1（可并行）：RAII-001、VALUE-001、PERF-001、ALIGN-001
批次 2（依赖批次 1）：NEW-001、UNIQUE-001
批次 3（依赖批次 2）：SHARED-001
批次 4（依赖批次 3）：WEAK-001
```

---

## 五、第四步：commit + push（原子化完成后）

- 提交信息走 `git commit -F <UTF-8 文件>`（不用 -m "中文"，避免 GBK 乱码）
- 提交内容：8 颗原子化 + MIS-MEM-010 修复 + References/11-19 调研文档入库
- References/11-19 共 9 份文档（11 内存模型/12 RCU/13 无锁/14 并发bug/15 本指令/16 形式化验证/17 C++26/18 ARM/19 seqlock）——这些是监工产出的调研文档，无内容风险，一并入库
- push 前跑 WSL 预检（`tools/ci_local_precheck.py`），全绿再推
- 推送后观察 CI，不带红进下一步

---

## 六、第五步：MEM 域第二批（可选，视用户指示）

如果用户要求继续生产 MEM 域第二批，候选原子（从 G1 知识地图选，与第一批不重复）：

| 候选 ID | 主题 | 类型 | 证据卡需求 |
|---|---|---|---|
| ATOM-MEM-VALUE-002 | 引用折叠与完美转发（T&& + std::forward） | mechanism | 引用折叠编译期证明 + forward 保持值类别 |
| ATOM-MEM-RAII-002 | 拷贝控制五件套（构造/析构/拷贝/移动/赋值）与 Rule of 0/3/5 | mechanism | 编译器自动生成条件 + =default/=delete |
| ATOM-MEM-UNIQUE-002 | 自定义 deleter 与数组形式 unique_ptr<T[]> | mechanism | deleter 调用 + 数组析构 |
| ATOM-MEM-SHARED-002 | make_shared 优势（单次分配 + 异常安全）与控制块布局 | pitfall | make_shared vs shared_ptr(new T) 分配次数对比 |
| ATOM-MEM-ALLOC-001 | allocator 接口与 std::allocator 实现 | mechanism | allocate/deallocate + construct/destroy 分离 |
| ATOM-MEM-LEAK-001 | 内存泄漏检测工具（ASan / valgrind） | tool | ASan 报告解读 + 漏报场景 |
| ATOM-MEM-PERF-002 | 小对象优化（SSO / 小对象缓冲） | mechanism | std::string SSO 阈值实测 + 汇编 |
| ATOM-MEM-PERF-003 | 内存池与 arena 分配 | mechanism | 分配器对比 + 碎片量化 |

第二批启动前先等用户确认选哪几个，不要自行开工。

---

## 七、铁律（重申，违反即拦截）

1. **verified 唯 human:liaoranran 可签**——你不得自置 status: verified
2. **5 分唯人审授予**——你最高自评 4，不得自封 5
3. **工件与断言同代**——改 .cpp 或改卡里计数必须重生成工件换 sha256
4. **产物写 build/**——路径正斜杠，不在仓库根留 .exe
5. **中文提交走 -F UTF-8 文件**——不用 -m "中文"
6. **查同名必须 rglob**——新建文件前递归查
7. **验证不带 PATH 前置**——用 `toolchain.resolve_gpp()` 钉编译器，不用裸 g++
8. **硬编码期望会被 S3 拦**——expected.run 是描述，actual.run 是机器输出
9. **计数/计时 -O0/-O2 双跑**——计数器 volatile
10. **UB 类证据卡必须 Linux/WSL 过 sanitizer**——Windows 会 skip

---

## 八、交付物清单

- [ ] MIS-MEM-010 缺陷修复（新建或改引用）
- [ ] ALIGN-001 误解 ID 确认（建议项）
- [ ] 等待人审（不代审）
- [ ] 人审通过后按依赖顺序原子化 8 颗
- [ ] golden_lock sync（EV-SERVES-EXIST 清零确认）
- [ ] References/11-19 入库
- [ ] commit + push（WSL 预检全绿后）
- [ ] CI 观察（不带红进下一步）
- [ ] 第二批候选清单交用户确认（不自行开工）

**完成后报告：每颗原子的原子化提交号、golden_lock 前后对比、CI 结果。**
