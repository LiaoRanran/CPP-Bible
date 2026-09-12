# G5 首个原子打磨指令：ATOM-MEM-RVREF-001 从 4 到 5

> 自包含投喂文档。执行 Agent 读完即开工，无需额外上下文。
> 监工已独立质检（五重剖面 5/5、双卡 confirm、标准条款 eel.is 逐字核验），复评 4/5 达 Agent 上限；人审裁决**不授 5 分，继续打磨**。本指令是从 4 到 5 的具体差距清单。

## 一、任务

打磨 `goldens/mem/ATOM-MEM-RVREF-001_draft.md`（具名右值引用是左值），使其达到 5 分标准：**行家无硬伤 + 独有洞见**。4 分的"完整有据"已满足，缺的是实证完整性和洞见深度。

## 二、P0 必须完成（缺一项不到 5 分）

### P0-1 补 C++11/14 实测，消除 claim_boundary 的"待补"
- 当前 `claim_boundary.standard` 只写 `[C++17, C++20, C++23]`，C++11/14 明标"待补"。5 分样板不允许核心覆盖档留空。
- 至少补 C++14 一档（`-std=c++14`），验证主体论断"具名右值引用是左值"在 C++14 下同样成立；`return x;` 路径在 C++14 下是拷贝（P0527R1 是 C++20 才进的）。
- 新建或更新证据卡，`claim_boundary` 同步扩展，删除"待补"措辞。

### P0-2 补 Clang 列实测，满足 M2 双编译器边界
- 当前只有 GCC 15.3.0 / 13.1.0。M2 永久边界要求 GCC + Clang 双编译器实测。
- 走 CI 的 Clang-19 矩阵（本机无 Clang），在 Gray-zone / Cross-check 步补 `::notice::` 输出，留痕即可。
- 主体论断（具名右值引用是左值）在 Clang 下必然一致；`return x;` 版本边界也应一致（标准行为）。把 Clang 输出写进证据卡 `actual`。

### P0-3 补第三组对照：无移动构造的类型，`std::move` 静默退化拷贝
- 红队第 1 轮说"留待 G5 批量生产时按需补"——5 分样板必须现在补。
- 设计一个没有移动构造的类型（或 `=delete` 移动构造），验证 `std::move(x)` 仍选中拷贝构造（退化），与前两组（as_is 拷贝 / moved 移动）形成三角验证。
- 这组同时证伪"写了 std::move 就一定移动"的常见误解。

## 三、P1 深化洞见（从"是什么"到"为什么"）

### P1-1 版本边界的"为什么"
- 现在只说了 `return x;` C++17 拷贝 / C++20+ 隐式移动，没说**为什么改**。
- 补 P0527R1 / P1825R0 的动机：右值引用形参与局部对象在 return 时的不对称、用户被迫写 `std::move(x)` 的冗余、以及隐式移动后对 NRVO 的交互。
- 引用标准提案编号和一句话动机，不展开论文式综述。

### P1-2 决策树：什么时候写 std::move、什么时候不能写
- 把"怎么做"表格升级为一张可操作的决策树（文字版即可，不强制 mermaid）：
  - 函数体内不再用 x → 写 `std::move`
  - 还要读 x → 拷贝
  - 传给 `T&&` 形参 → `std::move`
  - 传给转发引用 `T&&`（模板）→ `std::forward`
  - return 局部对象 → **不写**（写了阻断 NRVO）
  - return T&& 形参 → C++20+ 不写（隐式移动），C++17 及以前写
  - mem-initializer-list → 写
  - lambda 非 mutable 捕获 → init-capture
- 每个分支标注"为什么"，不是只给结论。

### P1-3 与 ATOM-MEM-MOVE-002 的串联示例
- 两个原子讲同一族问题的两面（MOVE-002：move 只是 static_cast；RVREF-001：cast 的值类别后果）。
- 补一个串联代码块：先演示 `std::move(x)` 不做移动（MOVE-002 点），再演示即使 cast 成 xvalue，具名后仍是左值（RVREF-001 点）——让读者看到知识怎么连起来。
- 在 `relations` 或正文首段明确学习路径：先 MOVE-002 再 RVREF-001。

## 四、P2 超额项（做了加分，不做不阻断）

- **P2-1** 误解反例从 2 条扩到 3-4 条，覆盖函数体 / mem-init-list / lambda / return 四个场景（MIS-MEM-005 是 deep，当前刚好达标 ≥2，5 分应超额）。
- **P2-2** WSL 补一次 ASan/UBSan 运行（MEM 计数类非强制，但能让"无 UB"更有底气，尤其涉及移动后源对象状态）。

## 五、存量联动（顺手做，不影响本原子评分）

- 整库修正 `[xvalue.cast]` → `[expr.static.cast]`（eel.is 已确认前者不存在）。受影响文件：
  - `atoms/mem/ATOM-MEM-MOVE-002.md`（3 处，已 verified 原子）
  - `goldens/A_move.md`（4 处，G4 样板）
  - `docs/kernel/G1_selfcheck.md`（1 处）
  - `docs/kernel/M1_ontology.md`（1 处）
- 本原子正文未引用此错误条款（仅红队记录提及），无需改。
- 修正后跑 `gate_engine --check` 确认无回归。

## 六、硬性约束（违反即被监工拦截）

1. **所有新实证必须真机复跑**：GCC 15.3.0 `-std=c++23 -O2 -Wall -Wextra`，输出逐字匹配证据卡 `actual`；计数器必须 `volatile`，汇编层找不到调用点却"证实"=伪证据（M2 §5）。
2. **工件与断言同代**：改夹具或改卡里计数必须重生成 .asm 并换 sha256，禁止"旧工件配新断言"。
3. **版本边界必须实测**，不准凭记忆写"C++14 也是拷贝"——跑了再写。
4. **Clang 列走 CI**，本机不装 Clang；MSVC 仍按永久边界以标准条文代替，禁写"三编译器全实测"。
5. **红队独立攻击**：Writer 写完后必须由独立 RedTeamer 子 agent 按 S1-S6 逐条攻击，重点查：零观测伪证据、版本边界误判、硬编码期望、工件不同代。Writer 不得自审。
6. **不改其他原子/章节内容**，除存量 `[xvalue.cast]` 修正外，不越界。
7. **status 保持 draft**，verified 唯人可置（S1），不得自签。
8. **中文提交走 `git commit -F` UTF-8 文件**，不用 `-m "中文"`。

## 七、交付物

1. 更新后的 `goldens/mem/ATOM-MEM-RVREF-001_draft.md`（P0+P1 全部落地，P2 按需）
2. 新建/更新证据卡：EV-MEM-004（补 C++14 档 + Clang 列）、EV-MEM-005（补 C++14 档）、新增第三组对照卡或并入现有卡
3. 打磨记录：Writer 做了什么、红队抓了什么、每条 P0/P1 如何落地
4. 存量 `[xvalue.cast]` 修正（单独 commit 或同 commit 注明）
5. 门禁自证：`atom_evidence_replay.py --check`（新卡 confirm）、`compile_all --main-only`、`compile_gate`、`gate_engine --check`、`pytest`

## 八、验收门（监工独立复跑，不采信自报）

打磨完成后提交，监工会做：
1. 证据卡 replay：新卡/更新卡全部 confirm，artifact_sha 匹配
2. C++14 档真机独立编译运行，输出与卡一致
3. Clang 列 CI notice 留痕核实
4. 第三组对照真机验证（无移动构造类型确实退化拷贝）
5. 标准条款复核（P0527R1/P1825R0 引用准确）
6. 决策树/串联示例技术正确性
7. `[xvalue.cast]` 存量修正完整性（5 处文件全改，无遗漏）
8. 门禁全绿

**全部通过后，再次提交人审，由用户决定是否授 5 分并原子化。**

## 九、血泪注意事项（继承项目铁律）

- 验证不带 PATH 前缀（系统 g++ 是 13.1.0 缺 cc1plus），用完整路径 `C:\Qt\Tools\mingw1530_64\bin\g++.exe`
- 产物写 `build/`，正斜杠，禁止在仓库根留 a.exe
- 查同名必须 `rglob`（quality_dashboard 撞名教训）
- 计数/计时类实验 -O0/-O2 双跑，计数器 volatile
- 注释里的机制断言必须有代码实证（mutable 死代码事件已写进 goldens/README checklist）
- `--only` 接完整文件路径，不接缩写（缩写会 0 checked 假全绿）
- 本原子是 G5 首个原子，打磨质量直接决定后续批量生产的上限——宁可慢，不要放水
