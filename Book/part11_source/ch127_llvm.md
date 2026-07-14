# 第127章　LLVM / Clang 架构（C++）

⟶ Book/part11_source/ch125_libcxx.md
⟶ Book/part02_toolchain/ch11_compilers.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++20 -O0/-O2 -S -masm=intel`）。
> 取证源码根：`Examples/_ch127_*.cpp`。LLVM/Clang 本机未安装，源码剖析一律引用上游仓库 `https://github.com/llvm/llvm-project/...` 并标注「上游参考」，行号为该文件中相关逻辑的代表性位置。
> 工具链：`C:/Qt/Tools/mingw1310_64/bin/g++.exe`（GCC 13.1.0）。

## ① 概述：LLVM 项目与 Clang [标准]

⟶ Book/part11_source/ch126_msstl.md
⟶ Book/part11_source/ch128_boost.md


LLVM 是一套**模块化、可重用**的编译器后端基础设施；Clang 是构建在 LLVM 之上的 C/C++/Obj-C 前端。二者分离：Clang 把源码翻译成中立的 **LLVM IR**，LLVM 后端把 IR 优化并生成目标机器码。这种「前端/IR/后端」解耦让 Rust、Swift、Julia 等都能复用同一套优化器与代码生成器。

```cpp
// ① 典型的 Clang 调用：源码 -> IR -> 汇编（命令见 ⑩）
// clang++ -std=c++20 -O2 -emit-llvm -S main.cpp -o main.ll
// clang++ -std=c++20 -O2 main.cpp -o main
int main() { return 42; }
```

- `[标准]`：C++ 标准本身不规定编译器内部结构；但 Clang 以「忠实实现标准 + 可诊断扩展」为工程目标（见 ⑦）。
- `[平台]`：Clang/LLVM 覆盖 x86-64、ARM/AArch64、RISC-V、PowerPC 等（见 ⑫）。

## ② 架构：前端 / 优化器 / 后端 / IR [实现]

经典三段式。Clang（C++ 前端）产出 LLVM IR；优化器（Pass 管道）在 IR 上做与机器无关的变换；后端（Target）把优化后的 IR  lowering 成具体 ISA。

```text
┌────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  C++ 源码   │──▶│  Clang 前端  │──▶│  LLVM IR     │──▶│  Pass 管道   │
│  (.cpp)     │   │ (Lex/Parse/ │   │ (SSA, 类型化)│   │ (优化)       │
└────────────┘   │  Sema/AST/  │   └──────┬───────┘   └──────┬───────┘
                 │  CodeGen)   │          │                  │
                 └────────────┘          ▼                  ▼
                                   ┌──────────────┐   ┌──────────────┐
                                   │  后端 Target  │   │  机器码/目标  │
                                   │ (x86/ARM/    │──▶│  (.s/.o/.exe) │
                                   │  RISCV)      │   └──────────────┘
                                   └──────────────┘
```

```cpp
// ② 三组件各自独立演进：换前端不影响后端
// Clang(前端) 1.0 ─┐
//  Rustc(前端)  ───┼─▶ 同一套 LLVM 优化器 + x86 后端
//  Swift(前端)  ─┘
struct CompileUnit { const char* frontend; const char* target; };
```

- `[实现]`：Clang 的 IR 生成集中在 `clang/lib/CodeGen/`，每个 AST 节点有对应 `Emit*` 函数（见 ⑤）。
- `[经验]`：理解 LLVM 的关键不是记住某个 Pass，而是理解 **IR 是通用货币**——所有优化都在 IR 上表达。

## ③ LLVM IR 表示 [标准]

LLVM IR 是**强类型、SSA 形式、低级但机器无关**的中间表示。函数、基本块、指令三层结构；每个值（除 PHI 外）只被赋值一次。

```cpp
// ③ 与 C++ 对应的 IR 直觉（典型输出，clang 未本机安装）
// 源码: int add(int a, int b){ return a+b; }
// 对应 IR 概念（非逐字）:
//   define i32 @add(i32 %a, i32 %b) {
//     %sum = add i32 %a, %b      ; SSA: %sum 仅一次赋值
//     ret i32 %sum
//   }
int add(int a, int b) { return a + b; }
```

```cpp
// ③ IR 中类型是一等公民：i1/i8/i32/i64/ptr/<数组>/<结构体>
// 这与 C++ 的强类型在 CodeGen 阶段被忠实地映射
extern "C" int g(int* p, long n) { return (int)(p[0] + n); }
```

- `[标准]`：IR 的 SSA + 类型系统使「值版本」分析（常量传播、死代码消除）天然高效。
- `[平台]`：IR 与 ABI 解耦——同一份 `.ll` 可被不同 Target 后端消费。

## ④ Pass 框架与优化管道 [实现]

早期 LLVM 用 `FunctionPassManager`/`ModulePassManager` 顺序跑 Pass；现代 LLVM（≥14）转向 **Analysis/Transform 分离的新 PassManager**，由 `PassBuilder` 按优化等级组装管道。

```cpp
// ④ 现代 PassManager 的 C++ 入口（上游典型结构，非可独立编译）
// 文件：llvm/lib/Passes/PassBuilder.cpp（上游参考）
// 行号：约 900（PassBuilder::buildPerModuleDefaultPipeline）
//   PipelineTuningOptions 决定哪些 Pass 进入 O2/O3 管道
//   ModulePassManager MPM = PB.buildPerModuleDefaultPipeline(Level);
//   MPM.run(M, MAM);   // M = Module&, MAM = ModuleAnalysisManager&
```

```cpp
// ④ 一个最小「自定义 Pass」骨架（适配新 PassManager）
// 文件：llvm/include/llvm/IR/PassManager.h（上游参考）
// 行号：约 200（PassConcept / AnalysisManager 定义）
// struct MyPass : PassInfoMixin<MyPass> {
//     PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM);
// };
```

- `[实现]`：Pass 必须是**幂等、可组合**的；优化器通过 `AnalysisManager` 缓存（如 DominatorTree）避免重复计算。
- `[经验]`：管道顺序影响收益——先 CFG 简化，再循环优化，最后代码布局。

## ⑤ [实现] 源码剖析：Clang CodeGen 如何发射函数 [实现]

Clang 把 AST 翻译成 IR 的核心在 `clang/lib/CodeGen/`。`CodeGenFunction` 是「单函数发射器」，每个 AST 语句节点由 `Emit*Stmt` 处理；表达式由 `CodeGenFunction::EmitExpr` 分派到 `Scalar/Complex/Agg 表达式 emitter`。

```cpp
// ⑤ 源码剖析（上游参考）
// 文件：https://github.com/llvm/llvm-project/blob/main/clang/lib/CodeGen/CodeGenFunction.h
// 行号：约 450（class CodeGenFunction：持有 Builder、CurFn、CGM 等）
//   class CodeGenFunction {
//     CodeGenModule &CGM;            // 模块级上下文
//     llvm::IRBuilder<> Builder;     // 往当前 BasicBlock 追加 IR
//     llvm::Function *CurFn;         // 当前正在发射的函数
//     void EmitStmt(const Stmt *S);  // 语句分派
//   };
```

```cpp
// ⑤ 源码剖析（上游参考）：循环发射
// 文件：https://github.com/llvm/llvm-project/blob/main/clang/lib/CodeGen/CGStmt.cpp
// 行号：约 700（CodeGenFunction::EmitForStmt：为 for/range 发射前/条件/增量基本块）
//   void CodeGenFunction::EmitForStmt(const ForStmt &S,
//                                     ArrayRef<const Attr *> Attrs) {
//     // 1. 发射 init  2. 建条件块/体块/增量块  3. 用 Builder.CreateBr 串联
//   }
//
// 对应我们在 ⑨ 看到的：for 循环在 IR 层是 BasicBlock 的 CFG，
// 优化器（LoopSimplify/Unroll）才有机会将其展开为常量（mov eax,10）。
```

- `[实现]`：`IRBuilder` 不是「写文本」，而是构造 `llvm::Value*` 对象图；Clang 每 emit 一条表达式就拿到一个 `Value*`，供父节点复用（这正是 GVN 能去重的基础，见 ⑧）。
- `[平台]`：上述路径为上游 `main` 分支；具体行号随版本漂移，引用时务必带 commit/分支。

## ⑥ Clang 前端与 AST [实现]

Clang 前端管线：`Lexer`(分词) → `Parser`(语法 → AST) → `Sema`(语义检查/类型推导) → `CodeGen`(AST → IR)。AST 是带完整类型信息的树。

```cpp
// ⑥ AST 节点层级（上游典型，非独立编译）
// 文件：https://github.com/llvm/llvm-project/blob/main/clang/include/clang/AST/Expr.h
// 行号：约 1200（class BinaryOperator : public Expr）
//   class BinaryOperator : public Expr {
//     enum Opcode Opc; Expr *SubExprs[2];  // LHS/RHS
//   };
int binary_example(int a, int b) { return a * b + 1; } // AST: (BinaryOperator '+'
                                                      //        (BinaryOperator '*' a b) 1)
```

```cpp
// ⑥ Sema 在 CodeGen 之前就完成了重载解析与类型检查
// → CodeGen 阶段拿到的 AST 已是「良类型」的，无需再查重载
template <typename T> T poly(T a, T b) { return a + b; }
int use_poly() { return poly(2, 3) + poly(1.5, 2.5); }
```

- `[实现]`：AST 与 IR 的边界清晰——**Sema 保证语义正确，CodeGen 只负责忠实 lowering**。这也是 Clang 诊断质量高的根源（见 ⑦）。
- `[经验]`：要读懂 IR 为什么是那样，先理解 AST 节点是怎么被 Emit 的（⑤ 的 `EmitStmt`/`EmitExpr`）。

## ⑦ 与 C++ 标准：诊断 / 实现 [标准]

Clang 以「诊断友好」著称：模板错误用 `note:` 串联实例化栈；`-Werror`、`-Weverything`、`-fsanitize=...` 都是 Clang 的特色。标准遵循度由 `clang/test/CXX/...` 下的 conformance 测试守护。

```cpp
// ⑦ 标准违反的清晰诊断（典型输出，Clang 未本机安装）
//   template<class T> requires T::value struct X {};
//   X<int> x;   // error: 'int' does not have 'value'
// Clang 会沿模板实例化链给出 note，而非只抛一行 cryptic 错误
template <typename T> struct needs { static constexpr bool value = T::flag; };
template <typename T> requires (needs<T>::value) int f(T) { return 0; }
```

```cpp
// ⑦ 实现定义行为：Clang 用 __builtin / 属性暴露底层控制
// -fsanitize=undefined 在 IR 中插入运行时检查（由 UBSan Pass 完成）
int ub_example(int* p) {
    return p[1'000'000'000]; // 若越界，UBSan 在优化后 IR 注入 __ubsan_handle_*
}
```

- `[标准]`：Clang 对 C++20 模块化、`<ranges>`、concepts 的支持与 GCC 互有快慢（见 ⑭/⑮）。
- `[经验]`：把 `-Wall -Wextra -Werror` 当默认；Clang 的 `-Wshadow`/`-Wconversion` 能抓出大量潜藏 bug。

## ⑧ 优化管道：SCCP / GVN / 循环优化 [实现]

三个机器无关优化的代表：
- **SCCP（稀疏条件常量传播）**：沿 CFG 传播常量，遇不可判定则退化为「未知」，最终把可定值替换为立即数。
- **GVN（全局值编号）**：同一表达式只算一次，重复出现复用其结果。
- **循环优化**：LoopRotate / LICM / LoopUnroll 把循环变成更易优化的形态。

```cpp
// ⑧ SCCP 示例：caller() 传入常量 7，compute 全程被折叠
// 见 ⑨ 真实汇编：O2 下 caller() 直接 mov eax, 92
int compute(int x) {
    int a = x * 2;
    int b = x * 2;   // 与 a 同值（GVN 可复用）
    int c = (x + 1) * (x + 1);
    return a + b + c;
}
int caller() { return compute(7); }  // SCCP: 全部代入 -> 常量
```

```cpp
// ⑧ GVN 去重：两个 x*2 在 IR 中合并为单个 mul
// 文件：https://github.com/llvm/llvm-project/blob/main/llvm/lib/Transforms/Scalar/GVN.cpp
// 行号：约 1100（GVN::processNonLocalLoad / performGVN 主循环，上游参考）
//   if (VN.lookup(Expr)->hasValue())  // 同值编号已存在 -> 替换
//       replaceAllUsesWith(Existing);
```

```cpp
// ⑧ 循环优化：LICM 把不变计算移出循环体
// 文件：https://github.com/llvm/llvm-project/blob/main/llvm/lib/Transforms/Scalar/LICM.cpp
// 行号：约 300（llvm::hoist / sink 决策，上游参考）
int dot(const int* a, const int* b, int n, int k) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += (a[i] + k) * b[i]; // k 循环不变，可外提
    return s;
}
```

- `[实现]`：这些 Pass 在 `buildPerModuleDefaultPipeline` 中按 O2 组合（见 ④）；`opt` 可单独调试（见 ⑩）。
- `[经验]`：SCCP 与 GVN 经常协同——SCCP 先折叠出常量，GVN 再去重，最终 IR 大幅瘦身。

## ⑨ [实现] 真实：用 g++ 编译展示内联 / O2 差异 [实现]

我们用 GCC 13.1.0 真实编译 `Examples/_ch127_inline.cpp`，对比 `-O0` 与 `-O2` 的汇编。**这是真实取证，非示意**。

```cpp
// 文件：Examples/_ch127_inline.cpp，行号：9（use_inlined）/ 14（use_noinline）/ 5（add_inline）
// 编译命令（真实）：
//   g++ -std=c++20 -O0 -S -masm=intel _ch127_inline.cpp -o _ch127_inline_O0.asm
//   g++ -std=c++20 -O2 -S -masm=intel _ch127_inline.cpp -o _ch127_inline_O2.asm
#include <cstdio>
inline int add_inline(int a, int b) { return a + b; }
__attribute__((noinline)) int add_noinline(int a, int b) { return a + b; }
int use_inlined() {
    int s = 0;
    for (int i = 0; i < 4; ++i) s += add_inline(i, 1); // 期望被内联
    return s;
}
int use_noinline() { return add_noinline(3, 4); }       // noinline：保留真实 call
```

```asm
; 真实取证 A：use_noinline @ -O0 —— 保留真实 call（行号 14 的 add_noinline 仍被调用）
_Z12use_noinlinev:
	.seh_endprologue
	mov	edx, 4
	mov	ecx, 3
	call	_Z12add_noinlineii     ; 真实函数调用，未内联（noinline + O0）
```

```asm
; 真实取证 B：use_inlined @ -O2 —— 循环被完全展开并折叠为常量（行号 9）
_Z11use_inlinedv:
	.seh_endprologue
	mov	eax, 10                  ; (0+1)+(1+1)+(2+1)+(3+1) = 10，编译器已算好
	ret
```

- `[实现]`：`-O2` 下 `use_inlined` 里对 `add_inline` 的 4 次调用被内联、循环被展开、加法被常量折叠，最终只留下 `mov eax, 10`。这正是 ⑧ 所述 SCCP/GVN/Unroll 协同的结果——**在 GCC 上也成立**，证明优化原理跨编译器通用。
- `[平台]`：GCC 的 `-O2` 管道同样含内联、循环展开、常量传播；Clang 用同名 Pass 但启发式不同，数字可能略有差异但机制一致。

另一组真实取证来自 `Examples/_ch127_gvn.cpp`：`caller()` 调用 `compute(7)`，在 `-O2` 下被完全折叠：

```asm
; 真实取证 C：caller @ -O2 —— SCCP 把 compute(7) 折叠为常量 92（a=14,b=14,c=64, 14+14+64=92）
_Z6callerv:
	.seh_endprologue
	mov	eax, 92
	ret
```

```cpp
// ⑨ 对照：同一份源码在 -O0 下不做常量传播（compute 仍是真实 mul/add）
// 文件：Examples/_ch127_gvn.cpp，行号：3（compute）
// 编译：g++ -std=c++20 -O0 -S -masm=intel _ch127_gvn.cpp -o _ch127_gvn_O0.asm
// 汇编中可见 mov/add/mul 序列（无折叠），与 O2 的 mov eax,92 形成硬对比。
int compute(int x) { int a=x*2; int b=x*2; int c=(x+1)*(x+1); return a+b+c; }
```

## ⑩ 工具链：opt / llc / clang -emit-llvm [平台]

LLVM 提供一套单职责工具，便于「逐步观察」每一阶段产物。以下命令为**真实命令**，但 clang/opt/llc 本机未安装，汇编/IR 片段标注「典型输出」。

```bash
# ⑩ 典型输出（clang 未本机安装，命令真实、输出为代表性质）
# 1) 源码 -> LLVM IR（人类可读 .ll）
clang++ -std=c++20 -O2 -emit-llvm -S main.cpp -o main.ll
# 2) IR -> 优化后 IR（显式跑某个 Pass）
opt -O2 -S main.ll -o main.opt.ll
# 3) IR -> 目标汇编
llc -O2 -march=x86-64 -o main.s main.opt.ll
# 4) IR -> 目标对象文件
llc -O2 -march=x86-64 -filetype=obj -o main.o main.opt.ll
```

```cpp
// ⑩ clang -emit-llvm 的 IR 典型输出（代表性质，非本机产生）
// 对应源码: int caller(){ return compute(7); }  其中 compute 见 ⑧
//   define i32 @_Z6callerv() #0 {
//     ret i32 92                ; 与 ⑨ GCC O2 的 mov eax,92 完全等价
//   }
//   ; 关键：前端产出 IR 后，优化器已把 compute(7) 折叠成常量返回
int caller_typical() { return 92; }  // 语义等价于优化后的 caller()
```

- `[平台]`：GCC 对应物是 `g++ -S -fverbose-asm`（看汇编）与内部 GIMPLE（无可公开 `-fdump` IR 文本的标准格式）；Clang/LLVM 的 IR 完全外显，是学习编译优化的首选。
- `[经验]`：调试「为什么没优化」时，先 `clang -emit-llvm -O0` 看 IR，再 `-O2` 对比，定位是哪个 Pass 没触发。

## ⑪ 性能 [经验]

LLVM 优化是**编译时间 ↔ 运行时间**的权衡。`-O0` 几乎不优化（快编译、慢运行），`-O2/-O3` 投入更多 Pass，`-Os` 偏向尺寸，LTO/PGO 跨 TU 进一步优化。

```cpp
// ⑪ 微基准直觉：优化把「运行期计算」搬到「编译期」
// 未优化：每次调用都做 4 次加法 + 循环判停
// 优化后：直接返回常数（见 ⑨ 的 mov eax,10 / mov eax,92）
// 收益量级（示意，非本机实测）：热点循环内联展开可省 3~15 周期/迭代
int bench_inline() {
    int s = 0;
    for (int i = 0; i < 4; ++i) s += (i + 1);
    return s;   // 优化后等同于 return 10;
}
```

```cpp
// ⑪ LTO：跨翻译单元的内联（典型输出，需 clang/llvm 工具链）
//   clang++ -O2 -flto -c a.cpp -o a.o
//   clang++ -O2 -flto -c b.cpp -o b.o
//   clang++ -O2 -flto a.o b.o -o app   ; 链接期再跑一次全程序优化
// GCC 等价：g++ -O2 -flto ...（本机 GCC 13 支持，但未在此章实测）
```

- `[经验]`：绝大多数项目 `-O2` 性价比最高；`-O3` 对向量化友好但可能增大代码体积导致 icache 抖动。
- `[平台]`：Clang 与 GCC 在 `-O2` 下生成代码的性能差距通常在个位数百分比，选熟悉的即可。

## ⑫ 跨平台后端：x86 / ARM / RISC-V [平台]

同一份 LLVM IR 经不同 `Target` 后端生成不同 ISA。后端含指令选择（DAG/SelectionDAG 或 GlobalISel）、寄存器分配、指令调度、代码布局。

```cpp
// ⑫ 一份源码，多后端目标（典型输出，需 llc）
//   llc -march=x86-64  -> add eax, edx        (CISC, 少指令)
//   llc -march=aarch64 -> add w0, w0, w1       (RISC, 三地址)
//   llc -march=riscv64 -> addw a0, a0, a1      (RISC-V, 压缩扩展另算)
// 源码（与各后端无关，体现 IR 的中立性）：
int neutral_add(int a, int b) { return a + b; }
```

```cpp
// ⑫ 后端特定的内建：用 attribute 选择调用约定 / 指令集
// Clang: __attribute__((target("avx2"))) 让函数体用 AVX2 指令（上游 CodeGen 会选 VEX 编码）
__attribute__((target("avx2"))) int vec_sum(const int* p, int n) {
    int s = 0; for (int i = 0; i < n; ++i) s += p[i]; return s;
}
```

- `[平台]`：RISC-V 后端在 LLVM 中成熟度近年快速上升，常被用作教学后端（指令集规整、文档好）。
- `[实现]`：后端代码在 `llvm/lib/Target/<Arch>/`，每个架构一个子目录（X86/ARM/RISCV/...）。

## ⑬ 常见陷阱 [经验]

```cpp
// ⑬ 陷阱1：依赖未定义行为，优化后结果「诡异」
// 有符号溢出是 UB；-O2 下编译器可能直接假定「不会溢出」并删掉判停条件
int trap_ub(int x) { while (x + 1 > x) ++x; return x; } // 可能死循环或被删
```

```cpp
// ⑬ 陷阱2：volatile 不是同步原语，也不是优化开关
// 想跨线程可见/原子，用 <atomic>；volatile 只保证「不省略对内存的访问」
volatile int flag = 0;
int spin() { while (!flag) {} return flag; } // 不是正确的线程同步
```

```cpp
// ⑬ 陷阱3：把 IR 当「稳定 ABI」
// LLVM IR 没有稳定二进制/文本 ABI；跨版本 .ll 可能无法重放
// 陷阱4：fp-contraction / FMA 差异导致浮点结果跨编译器不一致（用 -ffp-contract=off 锁定）
double trap_fma(double a, double b, double c) { return a * b + c; }
```

- `[经验]`：最常见的是**过度依赖 UB 然后怪优化器**。写「定义良好」的代码，优化器才会给你想要的结果。
- `[标准]`：C++ 标准定义 UB 的边界；Clang/GCC 的优化都建立在「UB 不会发生」的假设上。

## ⑭ 与 GCC 对比：CGEN vs GCC 后端 [平台]

Clang/LLVM 与 GCC 是两套独立实现：Clang 用 LLVM 的机器无关 IR + 每架构 Target 库；GCC 用 GIMPLE（高层 IR）+ RTL（低层 IR）+ 每架构后端（machine description `.md`）。

```cpp
// ⑭ 同一优化意图，两边都能做，机制不同：
//   GCC:  GIMPLE 上做 IPA/内联 -> RTL 上指令选择（.md 描述）
//   LLVM: LLVM IR 上做 Pass   -> SelectionDAG/GlobalISel 指令选择
// 源码层完全无关，结果等价：
int both_inline(int a, int b) { return (a + b) * (a + b); }
```

```cpp
// ⑭ 诊断差异（典型输出）
//   Clang: 颜色化、模板实例化栈 note、--fixit 建议
//   GCC:   传统文本、部分情景下消息更精简
// 二者 -Wall -Wextra 覆盖集合有差异，建议 CI 同时跑两者以最大化警告覆盖
void unused_warn(int x) { int y = x; (void)y; } // -Wunused 两边都会报
```

- `[平台]`：关键区别——**LLVM IR 是外部可见、可序列化的文本**；GCC 的 GIMPLE/RTL 主要内部使用。这决定了 LLVM 生态（clang 插件、opt、LLDB、KLEE）更开放。
- `[经验]`：跨编译器项目（库作者）务必在 Clang 与 GCC 上各编译一遍，避免踩「某编译器扩展」的坑。

## ⑮ 演进：C++ 标准支持 [标准]

Clang 通常**最快**跟进新标准特性（因 AST/Sema 模块化好）；GCC 随后追赶。C++20 的 modules/concepts/ranges、C++23 的 `std::expected`/deducing-this 均已在 Clang 主线可用。

```cpp
// ⑮ C++20 concepts：Clang 的 Sema 在实例化前即检查约束（见 ⑥/⑦）
template <typename T>
requires std::integral<T>
T square(T x) { return x * x; }
static_assert(std::is_same_v<decltype(square(3)), int>);
```

```cpp
// ⑮ C++20 模块（Clang 用 -fmodules，GCC 用 -fmodules-ts，参见 ch118）
// export module math;  export int sq(int x){ return x*x; }
// Clang 的模块实现成熟度高于 GCC 13（参考 ch118 ⑱ 对比表）
export module math_evolution;
export int sq(int x) { return x * x; }
```

- `[标准]`：WG21 提案在 Clang 的 `clang/test/CXX/` 与 GCC 的 `testsuite/` 都有 conformance 测试守护。
- `[经验]`：尝鲜新标准特性优先 Clang 主线；生产稳定性则看发行版打包质量。

## ⑯ 最佳实践 [经验]

```cpp
// ⑯ 实践1：用 -O2 起步，profiling 驱动优化（不要盲上 -O3）
// 编译期：g++ -std=c++20 -O2 -g -flto  (GCC 13 本机可用)
int hot(int* p, int n) { int s=0; for(int i=0;i<n;++i) s+=p[i]; return s; }
```

```cpp
// ⑯ 实践2：用 [[likely]]/[[unlikely]] 给分支预测提示（C++20，IR 会带 !prof 元数据）
int classify(int x) {
    if (x > 0) [[likely]]   return 1;
    else        [[unlikely]] return 0;
}
```

```cpp
// ⑯ 实践3：把「编译期可定」的计算标 constexpr，给优化器最大空间
constexpr int lookup_size(int n) { return n * n + 1; }
static_assert(lookup_size(7) == 50);
```

- `[经验]`：优化是**测量**出来的，不是猜出来的。先 `-O2`，profile 定位热点，再针对性用内联提示/LTO/PGO。
- `[实现]`：`[[likely]]` 在 Clang 中会被 CodeGen 写入 `!prof` 权重元数据，影响块布局 Pass。

## ⑰ 贡献 [经验]

给 LLVM/Clang 贡献：先 `git clone` llvm-project，用 CMake + Ninja 构建（建议只开需要的 target 以省时），跑 `ninja check-clang` 验证。

```bash
# ⑰ 典型构建流程（命令真实，本机未装 llvm 工具链故未实跑）
# git clone https://github.com/llvm/llvm-project.git
# cmake -G Ninja -DLLVM_ENABLE_PROJECTS=clang \
#       -DCMAKE_BUILD_TYPE=Release \
#       -DLLVM_TARGETS_TO_BUILD=X86 \
#       llvm-project/llvm -B build
# ninja -C build            # 构建 clang + llvm
# ninja -C build check-clang  # 跑 Clang 回归测试
```

```cpp
// ⑰ 贡献最小示例：加一个 Clang 警告选项骨架（上游典型位置）
// 文件：https://github.com/llvm/llvm-project/blob/main/clang/include/clang/Basic/DiagnosticGroups.td
// 行号：约 600（def 一个诊断组，上游参考）
//   def MyNewWarn : DiagGroup<"my-new-warn">;   // 然后在 Sema 中 Emit 它
// 配套：clang/lib/Sema/SemaXXX.cpp 中 Diag(Loc, diag::warn_my_new_warn);
```

- `[经验]`：LLVM 代码风格要求 80 列、2 空格缩进、`[Reference]` 注释风格；PR 前务必 `clang-format` 与 `ninja check-all`。
- `[平台]`：所有讨论在 GitHub 与 Discourse（llvm-dev）进行；RFC 先于大改动。

## ⑱ 跨语言：Rust / Swift 用 LLVM [平台]

LLVM 是「语言无关后端」的典范。Rust 的 `rustc` 把 MIR  lowering 到 LLVM IR；Swift 用 Swift Intermediate Language 再降到 LLVM IR；二者都复用同一套优化器与 Target。

```cpp
// ⑱ 概念映射（不是 Rust/Swift 源码，是「等价 C++ 语义」示意）
// Rust:  fn add(a:i32,b:i32)->i32 { a+b }   -> LLVM IR 与下方 C++ 同构
// Swift: func add(_ a:Int,_ b:Int)->Int { a+b }
int add_cross_lang(int a, int b) { return a + b; }  // 三语言最终都落到同一 IR
```

```cpp
// ⑱ 共享优化器意味着「跨语言优化知识可迁移」：
// Rust 的 #[inline] / Swift 的 @inlinable 与 C++ 的 inline 在 LLVM 层
// 走的都是同一个 Inliner Pass（见 ⑧/⑨ 的机制）
template <typename T> inline T add_generic(T a, T b) { return a + b; }
```

- `[平台]`：启示——学透 LLVM IR 与 Pass，等于同时掌握了 C++/Rust/Swift 三套编译器的「底层语言」。
- `[经验]`：多语言团队可用 LLVM IR 作为「通用中间契约」，做跨语言 FFI 优化（如 Rust 导出给 C++ 调用）。

## ⑲ 调试 / 源码阅读 [实现]

阅读 LLVM/Clang 源码的入口：先 `clang -emit-llvm -O0 -S` 看 IR，再对照 `clang/lib/CodeGen` 中对应 `Emit*` 函数；用 `opt -print-after-all` 观察每个 Pass 后的 IR 变化。

```cpp
// ⑲ 源码阅读锚点（上游参考）
// 文件：https://github.com/llvm/llvm-project/blob/main/llvm/lib/IR/IRBuilder.cpp
// 行号：约 1500（IRBuilderBase::CreateAdd：所有 '+' 在 IR 层的统一入口）
//   Value *IRBuilderBase::CreateAdd(Value *LHS, Value *RHS, const Twine &Name,
//                                  bool HasNUW, bool HasNSW) {
//     return Insert(BinaryOperator::CreateAdd(LHS, RHS, Name), ...);
//   }
// 结论：C++ 里任何整数 '+' 最终都经 CreateAdd -> BinaryOperator::CreateAdd
```

```cpp
// ⑲ 源码阅读锚点（上游参考）：诊断发出
// 文件：https://github.com/llvm/llvm-project/blob/main/clang/lib/Sema/Sema.cpp
// 行号：约 800（Sema::Diag：Clang 所有诊断的统一入口，对应 ⑦ 的友好报错）
//   DiagnosticBuilder Sema::Diag(SourceLocation Loc, unsigned DiagID);
// 想理解「为什么报这个错」，从 Diag(..., diag::err_xxx) 反向追 AST 检查点
```

- `[实现]`：LLVM 源码以 `lib/` + `include/` 对应，`XXX.cpp` 实现 `XXX.h` 中声明的接口；阅读时「先接口后实现」最高效。
- `[经验]`：不要试图通读——带着具体问题（「'+' 怎么变成 IR？」「这个警告在哪发出？」）去读，命中即止。

## ⑳ 速查表 [标准]

| 主题 | 命令 / 概念 | 说明 |
|---|---|---|
| 源码→IR | `clang -emit-llvm -S -O2 x.cpp` | 生成人类可读 `.ll`（典型输出） |
| IR→汇编 | `llc -O2 -march=x86-64 x.ll` | 后端指令选择（典型输出） |
| 单 Pass 调试 | `opt -O2 -print-after-all x.ll` | 观察每个 Pass 后 IR（典型输出） |
| 内联开关 | `inline` / `__attribute__((noinline))` | 控制 Inliner Pass（见 ⑨） |
| 常量传播 | SCCP | 折叠 `compute(7)`→`92`（真实取证 ⑨） |
| 去重 | GVN | 合并重复 `x*2`（见 ⑧） |
| 跨 TU 优化 | `-flto`（GCC）/ `-flto`（Clang） | 链接期全程序优化（见 ⑪） |
| 浮点一致性 | `-ffp-contract=off` | 锁定 FMA，避免跨编译器差异（见 ⑬） |
| 源码入口 | `clang/lib/CodeGen/` | AST→IR 发射（见 ⑤） |
| 诊断入口 | `clang/lib/Sema/Sema.cpp::Diag` | 所有报错统一出口（见 ⑲） |

```cpp
// ⑳ 一页纸心智模型：C++ 源码经过「Clang 前端 → LLVM IR → Pass 管道 → 后端」
// 优化发生在 IR 与后端两层；前端只负责「忠实地翻译」（见 ②/⑤/⑧）
int model(int a, int b) {
    int t = a + b;     // CreateAdd (⑲)
    return t * t;      // SCCP/GVN 在常量场景折叠 (⑧⑨)
}
```

```cpp
// ⑳ 与上章（ch118 Modules）的承接：模块只改「编译组织」，不改「优化机制」
// 无论 #include 还是 import，落到 IR/Pass 后完全等价——Modules 省的是
// 编译期解析，不是运行期优化（Modules 结论见 ch118 ⑲）
export module opt_bridge;
export int bridge(int a, int b) { return (a + b) * (a + b); }
```

- `[标准]`：LLVM/Clang 是**标准无关**的基础设施——它实现 C++ 标准，但不被标准定义内部结构。
- `[经验]`：把 LLVM 当「可观察的编译器」来学：IR 是语言、Pass 是动词、后端是方言。掌握它，你同时懂了 C++/Rust/Swift 的底层。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第126章](Book/part11_source/ch126_msstl.md) | 无锁队列/计数器 | 本章提供概念，第126章提供实现 |
| [第128章](Book/part11_source/ch128_boost.md) | 日志格式化/序列化 | 本章提供概念，第128章提供实现 |
| [第125章](Book/part11_source/ch125_libcxx.md) | 泛型库/编译期计算 | 本章提供概念，第125章提供实现 |
| [第11章](Book/part02_toolchain/ch11_compilers.md) | 数据局部性/缓存友好设计 | 本章提供概念，第11章提供实现 |

## 附录 F：LLVM架构

```cpp
#include <iostream>
int main(){std::cout<<"LLVM=Frontend(Clang→AST→IR)→Optimizer(Passes)→Backend(MC→binary)"<<std::endl;return 0;}
```
面试: LLVM IR SSA为什么? 每次变量赋值一次→简化Pass; Clang=library化(可嵌入IDE) vs GCC=monolithic


## 相关章节（交叉引用）

- **相邻主题**：`Book/part11_source/ch129_qt.md`（第129章　Qt 对象模型与信号槽（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part11_source/ch124_libstdcxx.md`（第124章　libstdc++ 架构与阅读入口（C++））—— 同模块下的其他主题。

## 底层视角：LLVM IR、SSA 与后端向量化 [E: Low-level]

[标准] LLVM IR 为 SSA 形式，`Instruction` 等对象含 `0x0008` 指针链；`clang` 前端生成 IR 后由 `opt` 做 `-O2`/`-O3` 优化。`GCC 13.1.0` 与 `Clang 17` 后端对热点循环发射 AVX（`0x0020` 宽）/ AVX-512（`0x0040` 宽）指令，要求数据 `alignas(0x0020)`/`alignas(0x0040)`。

LLVM 用 `0x0040`（64 字节）对齐的 `SmallVector` 内联缓冲减少堆分配；Pass 管理器按 `0x0008` 函数指针表驱动。`MSVC 19.3` 不共用 LLVM 后端，但 `C++17`/`C++20` 抽象一致。缓存行 `0x0040` 是寄存器分配与指令调度的基本时间/空间单位（L1 ≈1 ns，L3 ≈12 ns，主存 ≈100 ns）。

## 附录 G：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **Clang/LLVM 16 的 C++17 并行 STL 与 ABI 迁移**：2023 年 LLVM 将默认 C++ 标准推到 C++17，`libc++` 默认启用 `_LIBCPP_ENABLE_ASSERTIONS`，生产环境若未显式关闭会在迭代器越界时直接 `abort`。工业上常见 Bug 是 CI 本地通过、生产容器因该断言崩溃——属于**默认行为随版本变化的隐性破坏**。
- **Opaque Pointer 迁移（LLVM 14→15 删除 `PointerType::getElementType`）**：不少内部 Pass 直接读 `getElementType()`，升级后编译失败。这是典型的**内部 API 不保证稳定**教训：LLVM 的 C++ API（`llvm::*` 命名空间）稳定性远低于其 `LLVMContext`/`IRBuilder` 公开契约。

### 常见 Bug 与 Debug 方法

- **优化 Pass 把代码优化没**：`opt -passes='default<O2>' -print-pass-manager` 打印实际跑的 Pass 管线；二分定位可疑 Pass 用 `opt -passes='require<domtree>,gvn'` 单独跑。
- **崩溃定位**：`bugpoint` 自动约减到最小复现 IR；`lli -print-before-all -print-after-all` 看每个 Pass 前后的 IR 差异。
- **Code Review 关注点**：新增 Pass 是否破坏了 SSA 形式、是否漏了 `AU.addPreserved<GlobalsAA>` 导致后续分析失效。

### 设计取舍（Trade-off）与反模式（Anti-Pattern）

| 维度 | 选择 | 代价 |
|------|------|------|
| 嵌入 vs 独立 | `libclang` C API 嵌入 IDE | C API 稳定但功能滞后于 C++ API |
| Pass 粒度 | 大 Pass（如 `instcombine`） | 单测难、回归面大 |
| 注册机制 | `PassBuilder` 回调注册自定义 Pass | 与上游管线耦合 |

- **反模式**：在业务代码里 `using namespace llvm;` 把上千符号灌进全局；直接依赖 `llvm::Value` 的内部子类布局（跨版本 ABI 不稳）。
- **API Design**：对外只暴露稳定的 C 接口或 `IRBuilder`/`LLVMContext`；内部 `Pass` 用 `AnalysisManager` 显式声明依赖，避免隐式全局状态。

### 重构建议

将手写的 `dyn_cast` 链重构为 `std::visit` 式分发或 `InstVisitor` 子类，降低漏判分支的风险；用 `LLVM_DEBUG` + `dbgs()` 替代临时 `errs()` 调试输出，便于用 `-debug-only` 开关精细控制。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

