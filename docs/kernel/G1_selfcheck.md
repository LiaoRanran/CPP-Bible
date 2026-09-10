# G1 验收自检（Self-Check for Gate G1）

> 提交基线：`f50b829`（G1 四件套 + ADR×3 + L0/L1/L2 骨架 + 覆盖工具）+ 本轮缺陷修复与补充调研。
> 本文件是 G1 阶段门的验收材料，按总规程 0.1/0.3/0.4 编写。

## 1. 交付物清单与验收门逐条核对

| 验收门要求 | 交付物 | 核对结果 |
|---|---|---|
| 地图可覆盖全部章主题（逐章映射，列覆盖率） | `docs/kernel/G1_knowledge_map.md` + `tools/atom_coverage_map.py --check` | ✅ 147/147 = 100%，`--check` 实跑通过（未映射 0，exit 0），**任何人可复算** |
| 任取 3 个知识点能据本体判断类型与关系且无歧义 | 本文件第 2 节现场演示 | ✅ 3 个真实书内知识点走完整判定链（含排除法） |
| 术语表能消解 ≥5 组真实易混词 | `docs/kernel/G1_terminology.md` | ✅ 6 组（超额），每组含统一写法/禁用/判定规则/实测计数；组 6 本轮补齐实测 |
| 落得到字段/文件/ID（0.3 反"只有原则"） | `docs/kernel/G1_layout.md`（frontmatter 14 字段 + 硬约束）、`atoms/id_migrations.json`（已初始化） | ✅ 字段名、目录路径、ID 格式、JSON schema 全部落盘 |
| 留痕 ADR（0.5） | `docs/adr/ADR-0001~0003`（随 f50b829）+ `ADR-0004/0005`（本轮附加调研） | ✅ 5 份，每份含背景/候选/否决理由/后果 |

**本轮修复的 G1 缺陷**（升级到 5 分的依据，0.4 要求写明）：

| 缺陷 | 修复 | 升分 |
|---|---|---|
| `G1_layout.md` frontmatter 示例用了非法 YAML 键 `misconception[]`（行家一眼挑出的硬伤） | 改为合法 YAML 序列 | layout 4→5 |
| cpp 块 7572 vs 7515 口径差标"待确认"未定死 | 实测定性：`parse`/CI 编译口径认**缩进围栏**（10 文件 51 个 + 连锁 6），`metrics_snapshot` 只认顶格；**定死 D 的分母 = 7572 口径**（原子验证对象 = CI 会编译的块）；缩进盲区移交工具修复波 | map 4→5 |
| P0 阈值 `D ≥ 9%` 无依据（拍脑袋嫌疑） | 锚定为 **2× 全书均值（3.94%）≈ 8%**，并验证定级结果与 9% 完全一致（结论对阈值不敏感） | map（合并上条） |
| `M1_ontology.md` 的 `equivalent` 例子不干净（表达式级、不可验证） | 换成标准明文等价 `std::move(x) ≡ static_cast<remove_reference_t<decltype(x)>&&>(x)`（[xvalue.cast]，可编译互证） | ontology 4→5 |
| `G1_terminology.md` 组 6（const 家族）无计数证据 | 词界实测：const 6632 / constexpr 2975 / consteval 384 / constinit 240 | terminology 4→5 |

## 2. 验收门第 2 条演示：3 个知识点完整判定

三个知识点全部取自现存 147 章真实内容，覆盖三个不同域与三种不同类型。

### 2.1 "vector 扩容会使全部迭代器失效"（ch77_vector，STL 域）

- **类型判定**：`mechanism`（判据"回答内部怎么运作"——扩容→新分配→元素搬运→旧存储释放→旧迭代器指向已释放存储）。排除法：不是 `rule`（标准未给迭代器失效统一条款，是实现行为的汇总）；不是 `pitfall`（它本身是中性机制陈述，"扩容后继续使用旧迭代器是 UB"才是另一条 pitfall 断言）。
- **粒度 4 问**：①可证伪（取旧迭代器解引用，sanitizer 必报 heap-use-after-free）✓；②边界闭合（libstdc++ / C++17 / -O2 下 `push_back` 触发扩容）✓；③单断言（"失效"是一个因果，"继续用是 UB"须拆出）✓；④独立（不依赖未验证断言）✓。
- **关系边**：`realizes` → libstdc++ vector 扩容实现；`causes` → ATOM-UB-ITER-001（使用失效迭代器 = UB）；`prerequisite` → ATOM-MEM-STACKHEAP-*（堆分配语义）。
- **ID**：`ATOM-STL-VECIT-001`。判定无歧义。

### 2.2 "constexpr 函数可以在运行期调用"（ch69_constexpr，TMPL 域）

- **类型判定**：`rule`（标准明文规定，`standard_ref: [dcl.constexpr]`——constexpr 函数是"可用于常量表达式的函数"，调用点决定求值期，声明本身不强制编译期）。排除法：不是 `concept`（不是回答"这是什么"的定义性条目）；不是 `evolution`（"C++11 语义收紧→C++14 放宽"是**另一条**演化断言，本断言在 C++11 起就成立）。
- **粒度 4 问**：①可证伪（`constexpr int f(){return 1;} int main(){int x; std::cin>>x; return f()+x;}` 若强制编译期求值则编译失败，实测通过）✓；②边界（C++11 起、任意 -O）✓；③单断言 ✓；④独立 ✓。
- **关系边**：`contrasts` → ATOM-TMPL-CEVAL-001（consteval：必须编译期——与术语表组 6 判定规则一致）；`misconceived_as` → "constexpr = 编译期 const"（书中高频误解，术语表组 6 禁用清单直接引用）；`evolved_from` → C++11 严格版语义（另一原子）。
- **ID**：`ATOM-TMPL-CEXPF-001`。

### 2.3 "std::atomic<int>::load 默认内存序是 seq_cst"（ch107_atomic，CONC 域）

- **类型判定**：`rule`（标准规定默认实参，`standard_ref: [atomics.types.operations]`——`load(memory_order = memory_order_seq_cst)`）。排除法：不是 `mechanism`（不回答"怎么运作"）；不是 `contrast`（"relaxed 读与 seq_cst 读的代价差异"是另一条对比原子）。
- **粒度 4 问**：①可证伪（读标准条文 + `static_assert` 默认实参存在性可编译验证）✓；②边界（标准层面，实现无关）✓；③单断言 ✓；④独立 ✓。
- **关系边**：`specializes` → ATOM-CONC-ATOMICOP-001（原子操作集）；`prerequisite` → ATOM-CONC-MEMORD-001（内存序语义——不懂 memory_order 无法理解默认值含义）；`contrasts` → ATOM-CONC-ATLOAD-002（relaxed 显式读）。
- **ID**：`ATOM-CONC-ATLOAD-001`。

**演示结论**：三个知识点均能唯一落型、边语义无二义、粒度 4 问全过——验收门第 2 条达成。

## 3. 反例自检汇总（0.3：什么情况算没做到）

- 覆盖率若非 100% 或无法用 `atom_coverage_map.py --check` 复算 → 地图失效（已实跑 100%，exit 0）。
- 若 3 个演示中任何一个出现"既可归 A 也可归 B 而判据不能裁决" → 类型学失效（上节均用排除法闭环）。
- 若某组易混词只有统一写法没有判定规则、或证据计数为 0 却称高频 → 词表失效（6 组全有判定规则与实测计数，组 6 本轮补齐）。
- 若原子模板落不到字段/硬约束 → 布局失效（14 字段表 + `verified ⟹ evidence ∧ first_hand ∧ superiority` 硬约束）。
- 若 ADR 缺候选/否决 → 留痕失效（5 份 ADR 全含候选与否决理由）。

## 4. rubric 总评

- 四份 G1 文档本轮修复后自评 **5 分**（行家视角硬伤已清零：YAML 合法性、口径可复算、阈值有锚、例子可验证、证据全实测）。
- 升分轨迹：4 分（初版，f50b829）→ 5 分（本轮补齐 5 项，见第 1 节表）。
- 仍诚实标注的两点：①`metrics_snapshot` 缩进围栏盲区（57 块）只是**定死与移交**，未修（修则联动 7515 真值，非 G1 范围）；②PERF 域 P0 定级是架构师按"最薄弱优先"追加（样板未点名），ADR-0003 已标"待确认"。

## 5. 移交与需你决策的事项（DRQ）

**DRQ-G1-1｜越阶段产出的 G2 草稿处置**（工作区未提交内容）：
上一轮会话在 G1 提交后**未停下等验收**，已开动 G2 并留下一批未提交草稿：`docs/kernel/M2_empirical.md`（G2.1 实证方法，含防折叠血泪规则）、`docs/kernel/M3_sources.md`（G2.2 置信公式，可手算）、`tools/gray_zone_scan.py`（灰色地带初筛）、`Examples/_atom_move_alloc.cpp`（+asm，样板 A 实验）、`Examples/_atom_eval_order.cpp`（样板 B）、`evidence/mem/EV-MEM-001.md`（首张证据卡）。
- **A：封存**——保持未提交不动，G1 验收通过后以 G2 起点草稿身份进入正式评审（我的倾向：质量不低且含真实实验产物，删了可惜；但它们没走过 G2 的完整工序与验收）。
- **B：本次一并提交入库**——打破阶段门先例。
- **C：删除重来**——最干净但浪费已跑出的真实实验。
- 代价：A 无；B 破坏门制纪律；C 损失约半天实验工作。

**DRQ-G1-2｜PERF 域 P0**：架构师追加（VERIFIED=0/UNVERIFIED=31 的零验证核心域），样板未点名。确认接受或降级 P1？

**DRQ-G1-3｜`metrics_snapshot` 缩进围栏盲区**（57 块 ≈0.75% 不进 README 真值）：G1 已定死口径与移交，修复动作放 G2 前、G3 门禁期、还是单独工具修复波？
