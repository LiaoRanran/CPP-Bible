# 343_第六批CONC域收口与CONC-003生产_执行提示词

> 2026-09-12 · 投喂Agent执行 · 线B收口 + 线B新生产

---

## 一、任务总览

两条线并行推进，按依赖顺序执行：

1. **线B-1：CONC-002 原子化收口**（卡生产层已完成，红队0阻断，A4修复已闭环）
2. **线B-2：CONC-003 全新生产**（数据竞争UB + TSan检测）

线C（ccache）仍卡在授权点，本提示词不涉及。线D/E已完成。

---

## 二、线B-1：CONC-002 原子化收口

### 2.1 已完成状态（接手起点）

| 项 | 状态 |
|---|---|
| 夹具 `Examples/atoms/_atom_lock_cost.cpp` | ✅ 双构建 -DBENCH_FULL 宏门控 |
| 工件 `.asm` (sha d84c7516) | ✅ 双平台实测 |
| 证据卡 `evidence/conc/EV-CONC-003.md`（判据） | ✅ gate block=0 |
| 证据卡 `evidence/conc/EV-CONC-004.md`（性能） | ✅ gate block=0 |
| 红队独立子agent盲读 | ✅ 阻断0/高级2/建议3，A4修复已闭环 |
| 原子草稿 `goldens/conc/ATOM-CONC-LOCK-001_draft.md` | ❌ 未写 |
| 原子化（move+签署+gate+golden_lock） | ❌ 未做 |
| 分离提交 | ❌ 未做 |

### 2.2 执行步骤

**Step 1：写原子草稿**

路径：`goldens/conc/ATOM-CONC-LOCK-001_draft.md`

参考样板：`atoms/conc/ATOM-CONC-FENCE-001.md`（已verified，CONC域首颗，格式完全对齐）

frontmatter必填字段（gate_engine ATOM_REQUIRED，缺一即block）：
```yaml
---
id: ATOM-CONC-LOCK-001
domain: conc
topic: lock
type: contrast          # 10类之一：mechanism/pitfall/contrast/...
title: "锁的代价与无锁的代价"
claim: "≤50字，本地产物可证，单句可证伪"
status: draft
dal: C                  # 并发/内存模型错用即UB且难复现 → DAL C
human_review: optional   # DAL C = optional，但豁免须人签 dal_reviewed_by
rubric_self: 4/5
verified: false
relations:
  prereq: [ATOM-CONC-FENCE-001]   # 屏障是锁的基础
  contrasts: []
  serves: [EV-CONC-003, EV-CONC-004]
pedagogy:
  misconception: [MIS-CONC-002]    # 扁平命名，不新建子目录
  level: intermediate
status_history:
  - {level: draft, at: "2026-09-12", by: writer:agent}
---
```

claim写法（参考CONC-001的收窄风格）：
- 锚方向不锚倍数（同机跨运行可波动2x+，PERF-003/004教训）
- 必须声明变量域（核数/竞争度/迭代数）
- 必须写证伪条件（低核环境CAS可能不退化）
- 示例："高竞争下CAS的原子RMW代价可能超过mutex；但该结论依赖核数与竞争度，≤2核环境可能反向——锁与无锁各有适用域，无绝对最优"

正文结构（对齐ATOM-CONC-FENCE-001）：
1. claim（单句）
2. 直觉节（beginner类比）
3. 证据节（引EV-CONC-003/004，含双平台数据）
4. 误解节（引MIS-CONC-002）
5. 边界与前提（核数/竞争度/迭代数）
6. relations说明
7. 修订记录（如有）

**Step 2：门禁预检**

```bash
python tools/gate_engine.py --check          # block必须=0
python tools/atom_evidence_replay.py --check  # confirm=52（50+2新卡）
python tools/poison_drill.py                  # 8/8
python -m pytest tests/                       # 全过
```

**Step 3：原子化**

```bash
# 草稿是untracked，git mv不适用，用文件系统移动
move goldens\conc\ATOM-CONC-LOCK-001_draft.md atoms\conc\ATOM-CONC-LOCK-001.md
```

修改frontmatter：
- `status: draft` → `status: verified`
- 新增 `verified_by: human:liaoranran`
- 新增 `verified_at: "2026-09-12"`
- 删除 `rubric_self: 4/5`，改写为正文「5分锚定依据（人审授予）」三条
- status_history追加：`{level: verified, at: "2026-09-12", by: human:liaoranran}`

**Step 4：原子化后立即复跑门禁（铁律1）**

```bash
python tools/gate_engine.py --check
# 预期block=0，warn可能增加（EV-SERVES-EXIST随原子化自动清零）
```

**Step 5：golden_lock sync**

```bash
python tools/golden_lock.py sync
python tools/golden_lock.py check
# 预期：verified_atoms 21→22，evidence 50→52，replay_confirm 50→52，恶化0
```

注意：Windows侧golden_lock可能被safe-delete shim拦截，改用WSL python3跑。

**Step 6：全量复算**

```bash
python tools/atom_evidence_replay.py --check   # 52/52 confirm
python tools/poison_drill.py                   # 8/8
python -m pytest tests/                        # 全过
```

**Step 7：WSL预检**

```bash
wsl.exe -e bash -lc "cd '/mnt/c/CodeLearnling/note/note/C++/CPP-Bible' && python3 tools/ci_local_precheck.py 2>&1 | tail -20"
# 预期31步全过（Evidence Replay已修跨编译器断言）
```

注意：Windows replay与WSL预检禁止并行（同写Examples/*.asm出假refute），必须串行。

**Step 8：分离提交**

```bash
git add atoms/conc/ATOM-CONC-LOCK-001.md evidence/conc/EV-CONC-003.md evidence/conc/EV-CONC-004.md Examples/atoms/_atom_lock_cost.* misconceptions/MIS-CONC-002.md
git commit -F commit_msg_lock.txt   # UTF-8文件
```

提交范围只挑CONC-002产物，不混References/（铁律3）。

---

## 三、线B-2：CONC-003 全新生产（数据竞争UB + TSan）

### 3.1 主题与claim方向

**主题**：数据竞争是UB，TSan可检测但有边界

**claim方向**（需收窄到≤50字，本地产物可证）：
- 数据竞争是C++未定义行为（标准条文）
- TSan可检测数据竞争，但有性能开销与漏报场景
- "没被TSan报"≠"没有数据竞争"（与LEAK-001/002同族）

### 3.2 关键环境约束（必须遵守）

1. **TSan仅WSL/Linux可用**，MinGW链接失败（cannot find -ltsan）
2. **TSan命令必须前缀 `setarch -R`**，否则WSL裸跑报"unexpected memory mapping"
3. **Windows侧只出.asm**，不跑TSan
4. **sanitizer判定按类型归并**（[thread]），不按子串（LeakSanitizer复用SUMMARY: AddressSanitizer的坑已在案）
5. **夹具必须有界循环**，无限循环→replay超时600s→rc=124→refute
6. **双构建同源宏门控**（-DBENCH_FULL只给.out生成用，actual.run_*只放方向量与常量）

### 3.3 生产步骤（五件套）

**Step 1：夹具设计**

路径：`Examples/atoms/_atom_data_race.cpp`

设计要求：
- 唯一变量=是否有数据竞争（有竞争vs无竞争对照）
- 活性对照=单线程基线
- 有竞争版本：两个线程并发读写同一非原子变量
- 无竞争版本：用std::atomic或mutex保护
- 打印确定性计数（*_result），不打印时序数据
- -DBENCH_FULL宏门控：默认构建只出方向量，BENCH_FULL构建出完整TSan输出
- 有界循环（迭代次数固定，不无限等待）

**Step 2：双平台工件**

- Windows/MinGW 15.3：编译出.asm（sha256锚定），不跑TSan
- WSL g++-13.3/14.2：
  - 正常编译出.asm
  - `setarch -R g++ -fsanitize=thread -g -O1` 跑TSan，stderr落.out
  - 有竞争版本应报"WARNING: ThreadSanitizer: data race"
  - 无竞争版本应零报告

**Step 3：两张证据卡**

- `evidence/conc/EV-CONC-005.md`（判据卡）：数据竞争的UB性质 + 符号级证据
- `evidence/conc/EV-CONC-006.md`（检测卡）：TSan检测结果 + 边界（漏报场景）

必填字段（EV_REQUIRED，缺一即block）：
fixture/command/artifact/artifact_sha256/artifact_compiler/actual/expected/falsification/matrix/controlled_vars

断言锚：
- 只锚常量+活性对照（不锚时序数据）
- 断言候选必须在Linux工件中grep验证（Windows sha路径覆盖不到artifact_assert，第五批教训）
- TSan输出用contains_any（吸收版本差异）
- expected_sanitizer: [thread]（有竞争版本会报，同EV-MEM-014/024口径）

**Step 4：误解**

`misconceptions/MIS-CONC-003.md`（扁平命名，不新建子目录）
- 触发词：数据竞争/race/TSan/没报就是安全
- 3条反例

**Step 5：红队（独立子agent，两段式盲读）**

P1-1纪律：先只读夹具源码+工件（不读卡），再对照卡。
can't-miss清单（13条，含本批新增）：
1. 口径不统一（ALLOC-002教训）
2. 消除与失败不可区分（LEAK-001教训）
3. 自证断言（UNIQUE-002教训）
4. 恒真观测（SHARED-002教训）
5. 派生重复读数（LEAK-002教训）
6. 编译期折叠常量冒充活性观测（ALLOC-002教训）
7. 载体口径不同变（PERF-004教训）
8. 断言字面量未在Linux工件实测（第五批教训）
9. 无限循环导致replay超时（CONC-001教训）
10. 性能数据锚倍数（PERF-003/004教训）
11. 夹具重载operator new/delete（P4规则）
12. 三变量同变（PERF-003教训）
13. TSan命令缺setarch -R前缀（CONC-003环境约束）

每条阻断必须配：替代解释≥1 + 验证动作 + 错误预测≥3

修复循环≤2轮，超出部分升级写入人审问题。

**Step 6：原子草稿+原子化**

同CONC-002的Step 1-8流程，ID为`ATOM-CONC-RACE-001`（gate要求ATOM-{DOMAIN}-{TOPIC}-{NNN}格式）。

---

## 四、铁律（不可违反）

1. 原子化后立即跑gate（草稿在goldens/不被扫描，问题只在mv那一刻引爆）
2. 红队两段式盲读，修复循环≤2轮
3. 提交只挑本批产物，不混References/
4. claim/actual不编造，断言锚只锚常量+活性对照
5. 夹具不重载operator new/delete
6. 未原子化、未commit、未push前，不报"完成"
7. push交给用户/监工，Agent不负责push
8. Windows replay与WSL预检串行，不并行
9. misconceptions/MIS-CONC-*扁平命名，不新建子目录
10. G6 status_history用{level, at, by}，by必须带前缀machine:/redteam:/human:

---

## 五、交付物清单

### CONC-002收口
- [ ] `atoms/conc/ATOM-CONC-LOCK-001.md`（verified）
- [ ] 分离提交（含原子+2卡+夹具+误解）

### CONC-003生产
- [ ] `Examples/atoms/_atom_data_race.cpp` + `.asm` + `.out`
- [ ] `evidence/conc/EV-CONC-005.md` + `EV-CONC-006.md`
- [ ] `misconceptions/MIS-CONC-003.md`
- [ ] `goldens/conc/ATOM-CONC-RACE-001_draft.md`
- [ ] 红队报告
- [ ] 原子化+分离提交

### 门禁自证（每颗原子化后）
- [ ] replay confirm（Windows+WSL双平台）
- [ ] gate block=0
- [ ] poison 8/8
- [ ] pytest全过
- [ ] golden_lock sync无恶化
- [ ] WSL ci_local_precheck 31步全过
