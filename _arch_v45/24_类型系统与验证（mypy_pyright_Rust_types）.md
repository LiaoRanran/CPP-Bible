# 方向 24：类型系统与验证（mypy / pyright / Rust types）

## 核心结论
1. 类型系统是"编译期最便宜的验证"：Rust 的借用检查器在编译期消灭整类 UB（UAF/数据竞争），mypy/pyright 给 Python 做渐进类型。这构成了 QueYi 的**参照系**——类型系统验证了"结构"，QueYi 验证"知识/语义"。
2. 关键洞察：Rust 之所以安全，是因为把"内存 UB"上移到类型系统；但**逻辑/语义错误（算法错、领域知识错）类型系统管不了**——这正是 QueYi 的生存空间（验证 LLM 生成的 C++ 的"知识正确性"，而非内存安全）。
3. 对审稿人：把 QueYi 定位为"类型系统之外的语义验证层"，并用 Rust 的借用检查作 motivation（"即使 Rust 也只管内存，不管知识"），立论更稳。

## 精确数字与案例
- **Rust types**：所有权 + 借用 + 生命周期，编译期防 UAF/竞争；`unsafe` 块显式标出逃逸区。实证：被大量研究引用为"消除整类 CVE"。
- **mypy**：Python 静态类型检查器，渐进类型（`Optional`/`Any`）；误报可控；与 pytest 集成。
- **pyright**：Microsoft 的 Python 类型检查器，更快、VS Code 默认；支持更全的类型语法。
- **类型与验证的关系谱**：运行时测试（最弱/最贵）< 静态分析（方向 23）< 类型系统（编译期）< 形式化验证（最强/最贵）。QueYi 落在"静态分析 + 语义性质"之间，定位清晰。
- **案例**：用 Rust 重写可消除方向 16 的 ①⑨ 类 UB，但 ⑦未排序修改、⑫宏 仍可能；说明类型系统非万能——QueYi 补剩余。

## 对阙疑的 3 条具体行动
1. **related work 放类型系统段**：列 Rust 借用检查 + mypy/pyright，明确"类型系统验证结构、QueYi 验证知识"，划清谱系。
2. **用 Rust 作 motivation 锚**：在 intro 写"即便 Rust 消除了内存 UB，LLM 生成的 C++ 仍有知识性错误（错误算法/误用 API），QueYi 专门抓这类"。
3. **考虑类型化前端（远期）**：讨论 QueYi 未来是否支持"先 clang-tidy 类型检查、再语义验证"的分层 pipeline，展示 roadmap（方向 51 护城河）。

## 盲区（诚实标注）
- "Rust 消除整类 CVE"是社区共识，无 QueYi 专属量化；若稿中引用需找具体研究数据。
- mypy/pyright 与 QueYi（C++）直接关联弱，仅作"类型验证"参照，勿强行对比。
- 形式化验证（Coq/Dafny）未展开，若强调"最严验证"应补（可作为 future work）。

## 来源
- [1] Rust ownership — https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- [2] mypy — https://mypy-lang.org/
- [3] pyright — https://github.com/microsoft/pyright
- [4] 类型与验证谱 — 方向 23/方向 16
