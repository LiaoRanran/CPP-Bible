# G5 MEM 域批量生产 · 验收报告（第一批 8 颗 mechanism 原子 draft）

> 日期：2026-09-11 · 流水线：Writer(主 agent) → 独立 RedTeamer 子 agent → Gatekeeper → 人审
> 状态：**8 颗原子草稿全部达成 S1–S6 机器门禁，待监工终检 + 人审 `verified`**

## 一、产物清单

| # | 原子 ID | 主题 | 类型/受众 | 提交 | 证据卡 |
|---|---|---|---|---|---|
| 1 | ATOM-MEM-VALUE-001 | 值类别五分类 | mechanism / intermediate | `187b199` | EV-MEM-006/007 |
| 2 | ATOM-MEM-PERF-001 | 移动性能量化 | mechanism / intermediate | `94495c5` | EV-MEM-001/002/008 |
| 3 | ATOM-MEM-RAII-001 | RAII 与异常安全 | mechanism / beginner | `43ba696` | EV-MEM-009/010 |
| 4 | ATOM-MEM-UNIQUE-001 | unique_ptr 所有权转移 | mechanism / intermediate | `db16c0f` | EV-MEM-011/012 |
| 5 | ATOM-MEM-SHARED-001 | shared_ptr 引用计数 | mechanism / intermediate | `2746ebd` | EV-MEM-013/014 |
| 6 | ATOM-MEM-WEAK-001 | weak_ptr 打破循环 | mechanism / intermediate | `43c0302` | EV-MEM-015/016 |
| 7 | ATOM-MEM-NEW-001 | new/delete 分层 | mechanism / beginner | `463d7ea` | EV-MEM-017/018 |
| 8 | ATOM-MEM-ALIGN-001 | 对齐与 padding | mechanism / intermediate | `58e6074` | EV-MEM-019/020 |

- 共 **8 颗原子草稿**（`goldens/mem/`） + **20 张证据卡**（`evidence/mem/EV-MEM-001..020`）。
- 每颗原子自评 **4/5**（Rubric 满分 5，Writer 最高自评 4，未自称达标，符合三权分立纪律）。

## 二、机器门禁（每颗独立跑，全批 8/8 通过）

| 门禁 | 结果 |
|---|---|
| `atom_evidence_replay.py` | confirm=20 / refute=0（每卡：编译 rc=0 · 运行逐字 · 工件 sha 同代 · sanitizer 工具链不支持已标注） |
| `gate_engine.py` (29 规则) | **block=0**；warn=22 全为预期债务（见第四节） |
| `poison_drill.py` | **4/4**（P1 假论断 / P2 过期工件 / P3 缺反例 / 阴性对照 全部拦截+放行） |
| `pytest tests/` | **全过**（100%） |
| `golden_lock.py` | 整体**无恶化**（13 条审计记录留痕，EV-SERVES-EXIST 预期债务已 `--accept`） |

## 三、红队打磨记录（Writer ≠ RedTeamer，三权分立）

- **VALUE-001**：初版 `&std::move(x)` 误判 xvalue 可取地址 → **编译器直接报错**（正是红队要抓的"注释无实证"）。
  重设计为"xvalue 有身份（移动后源对象被改动）"对照，真实可运行。
- **RAII-001**：硬性拦截 **S3-EXPECTED-HARDCODED**——初版打印 `"RAII dtor ran"`/`"unwound"` 硬编码结论字面量。
  改为 `g_live` 状态观测（归 0 即证明析构在异常路径执行），重生成工件并换 sha。
- **NEW-001**：修复 **-O2 优化坑**——编译器优先调带尺寸 `operator delete(void*, size_t)`，初版只重载无尺寸版导致
  `dealloc` 计数不增（误以为 delete 不释放）。补尺寸重载后 `dealloc=1`，并在卡内/正文留痕。
- **注释断言配实证**：UNIQUE-001 拷贝删除用**真实编译错误文本**坐实；ALIGN-001 指针强转 UB 用
  `[basic.align]`/`[strict.aliasing]` 标准条款标注（UB 不可运行，仅留证伪条件文本）。

## 四、预期债务（进入"原子化"阶段后自动清零）

| 债务 | 数量 | 来源 | 清零时机 |
|---|---|---|---|
| `EV-SERVES-EXIST` | 12 | 8 颗草稿各 2 卡指向 `goldens/` 草稿 | 草稿移 `atoms/mem/` 时自动清零 |
| `ATOM-REL-TARGET` | 4 | MOVE-002→VALUE/PERF、UB-GRAY→ALIAS/DEF | 存量历史（G4 样板引用的未锻造原子），非本批引入 |

- 整体 golden_lock **恶化 0**；每颗原子的预期债务均经 `--accept` 留痕，符合 RVREF-001 既定流程。

## 五、放行结论

✅ **8 颗 MEM 域 mechanism 原子草稿**全部满足：五重剖面齐全（多源精炼 / 一手实证 / superiority / 纵深 / 教学封装）、
S1–S6 制衡层全绿、真机复算 confirm=20/0、门禁零阻断。

**下一步（待你拍板）**：
1. 监工 RedTeamer 终检 / 人审，将 `status: draft` → `verified`（唯人可置，Writer 不自封）。
2. 原子化：草稿移 `atoms/mem/` → `EV-SERVES-EXIST` 债自动清零。
3. 顺带可清 `ATOM-REL-TARGET` 存量债（锻造 VALUE/PERF/ALIAS/DEF 等目标原子）。
