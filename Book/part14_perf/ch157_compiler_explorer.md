# 第157章 Compiler Explorer 实战

> 标准基: godbolt.org / GCC 13.1 / 预计阅读: 60min / ⟶ Book/part14_perf/ch156_compiler_opt.md / 难度: ★★★☆☆

## ① Compiler Explorer 核心工作流 [经验]

```cpp
#include <iostream>
int main() {
    std::cout << "Compiler Explorer (godbolt.org) —— 在线查看 C++ 编译后的汇编输出\n";
    return 0;
}
```

## ② 三编译器对比 [平台·x86-64]

```cpp
#include <iostream>
int square(int x) { return x * x; }
int main() {
    volatile int a = square(5);
    std::cout << a << std::endl;
    return 0;
}
```

## ③ 优化级别的汇编差异 [实现·GCC13]

```cpp
#include <iostream>
int sum(int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += i;
    return s;
}
int main() { std::cout << sum(100) << std::endl; return 0; }
```

## ④ 查看汇编的五种方式 [经验]

```cpp
#include <iostream>
int main() {
    std::cout << "1. godbolt.org (online)\n";
    std::cout << "2. g++ -S -fverbose-asm\n";
    std::cout << "3. objdump -d a.exe\n";
    std::cout << "4. perf record + perf annotate\n";
    std::cout << "5. Compiler Explorer CLI: c++filt\n";
    return 0;
}
```

## ⑤ ABI 与调用约定 [平台·x86-64]

```cpp
#include <iostream>
int add(int a, int b, int c, int d, int e, int f, int g, int h) {
    return a + b + c + d + e + f + g + h;
}
int main() { std::cout << add(1,2,3,4,5,6,7,8) << std::endl; return 0; }
```

## ⑥ 防止编译器消除死代码 [经验]

```cpp
#include <iostream>
void benchmark() {
    volatile int x = 0;
    for (int i = 0; i < 1000; ++i) x += i;
}
int main() { benchmark(); std::cout << "DCE prevented by volatile\n"; return 0; }
```

## ⑦ 识别关键路径与循环 [经验]

```cpp
#include <iostream>
int hotspot(int n) {
    int s = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            s += i * j;
    return s;
}
int main() { std::cout << hotspot(100) << std::endl; return 0; }
```

## ⑧ 链接器优化 LTO [实现·GCC13]

```cpp
#include <iostream>
int helper(int x) { return x * x; }
int call_helper(int n) { return helper(n) + helper(n+1); }
int main() { std::cout << call_helper(10) << std::endl; return 0; }
```

## ⑨ inline 与不 inline 的汇编差异 [实现]

```cpp
#include <iostream>
inline int sq(int x) { return x * x; }
int use_sq(int a, int b) { return sq(a) + sq(b); }
int main() { std::cout << use_sq(3, 4) << std::endl; return 0; }
```

## ⑩ 三编译器对比详表 [平台·x86-64]

| 特性 | GCC | Clang | MSVC |
|---|---|---|---|
| -S 输出 | AT&T/Intel | AT&T/Intel | MASM |
| CE 支持 | ✅ | ✅ | ✅ |
| LTO | -flto | -flto=thin | /GL |

```cpp
#include <iostream>
int main(){std::cout<<"GCC -S -masm=intel vs Clang -S -mllvm --x86-asm-syntax=intel\n";return 0;}
```

## ⑪ STL 联系：std::sort 的汇编实例化 [标准]

```cpp
// ⑪ CE 中观察 STL 算法的模板实例化
#include <iostream>
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> v{5, 3, 1, 4, 2};
    std::sort(v.begin(), v.end());  // 在 CE 中看: 会生成 introsort 的完整汇编
    std::cout << v[0] << std::endl;

    // CE 提示: 用 -O2 -DNDEBUG 消除断言; 用 --std=c++23 获得最新优化
    // 可见: std::sort 对 int 实例化为 introsort → 无虚函数、无异常、纯模板展开
    std::cout << "CE tip: paste this on godbolt.org with gcc -O2. Look for 'introsort_loop'.\n";
    return 0;
}
```

## ⑫ 工业案例：CI/CD 中集成 CE API 实现回归检查 [经验]

```cpp
// ⑫ 使用 Compiler Explorer API 自动化汇编回归测试
#include <iostream>
#include <string>

// 模拟 CE API 的伪代码（实际通过 HTTP POST 调用 godbolt.org/api/compiler/compile）
int main() {
    std::cout << "CE API Integration Pattern:\n";
    std::cout << "1. POST /api/compiler/<compiler-id>/compile\n";
    std::cout << "   body: {source, options: {userArguments: '-O2'}}\n\n";
    std::cout << "2. Parse response: extract 'asm' array of {text, source}\n";
    std::cout << "3. Diff: compare today's asm vs baseline asm\n";
    std::cout << "4. Alert: if critical function gained instructions → performance regression\n\n";
    std::cout << "Real use cases:\n";
    std::cout << "- Bloomberg: weekly asm diff on trading engine hot paths\n";
    std::cout << "- MongoDB: CI gate checks that critical loops stay < N instructions\n";
    std::cout << "- Game engines: verify SIMD intrinsics generate expected instructions\n";
    return 0;
}
```

## ⑬ 源码分析：GCC -S 输出结构解析 [实现·GCC13]

```cpp
// ⑬ 理解 GCC 汇编输出的每个部分
#include <iostream>
int square(int x) { return x * x; }

int main() {
    std::cout << "GCC -S -masm=intel output anatomy:\n";
    std::cout << "   .text           → code section\n";
    std::cout << "   .globl _Z6squarei → export symbol (mangled name)\n";
    std::cout << "   _Z6squarei:     → function entry point\n";
    std::cout << "   .seh_*          → Windows exception handling metadata\n";
    std::cout << "   imul eax, ecx   → actual instruction: eax = ecx * eax\n";
    std::cout << "   ret             → return\n\n";
    std::cout << "   .LFE0:          → end of function marker\n";
    std::cout << "   .ident \"GCC:...\"→ compiler version stamp\n\n";
    std::cout << "Key GCC flags for readable asm:\n";
    std::cout << "   -fno-asynchronous-unwind-tables → remove .cfi_* noise\n";
    std::cout << "   -fno-exceptions → remove landing pad tables\n";
    std::cout << "   -fverbose-asm   → add C++ source as comments\n";
    std::cout << "   -masm=intel     → Intel syntax (more readable than AT&T)\n";
    return 0;
}
```

## ⑭ WG21 关联提案 [标准]

```cpp
// ⑭ 影响汇编质量的 C++ 标准提案
#include <iostream>
#include <vector>
int main() {
    std::cout << "Proposals that change what you see on Compiler Explorer:\n\n";
    std::cout << "P2300R7 (std::execution): sender/receiver model → new asm patterns\n";
    std::cout << "  → async task graphs compile to dispatch chains visible in CE\n\n";
    std::cout << "P2809R3 (trivial infinite loops): UB→defined → loop asm changes\n";
    std::cout << "  → C++26: while(true){} no longer UB → compiler can't delete it\n\n";
    std::cout << "P1144R8 (trivially relocatable): std::vector realloc → memcpy vs move\n";
    std::cout << "  → CE shows: with trivially_relocatable → memmove, without → loop of moves\n\n";
    std::cout << "P2996R5 (reflection): generates code at compile time → asm varies wildly\n";
    std::cout << "Check these proposals on godbolt to see standard→machine implications.\n";
    return 0;
}
```

## ⑮ 面试题精选：读汇编 5 问 [经验]

```cpp
// ⑮ Compiler Explorer 相关面试问题
#include <iostream>
int main() {
    std::cout << "Q1: x86 jmp vs call 的区别？\n";
    std::cout << "答: jmp = 简单跳转（无返回地址）; call = 压入返回地址 + 跳转。call 是函数调用。\n\n";
    std::cout << "Q2: 如何从汇编判断函数是否被内联？\n";
    std::cout << "答: 如果调用方没有 'call square' 而是直接出现 'imul eax,ecx'，说明被内联。\n\n";
    std::cout << "Q3: volatile 在汇编中如何体现？\n";
    std::cout << "答: 每次访问都是独立的 mov 指令，不经过寄存器缓存。\n\n";
    std::cout << "Q4: 如何判断编译器做了尾调用优化？\n";
    std::cout << "答: 函数末尾的 call 被 jmp 替代。jmp 到 callee，callee 的 ret 直接返回给原始 caller。\n\n";
    std::cout << "Q5: -O0 vs -O2 的主要区别？\n";
    std::cout << "答: -O0 每个语句生成对应指令; -O2 应用常量折叠、死代码消除、内联、循环优化。指令数通常减 10-50x。\n";
    return 0;
}
```

## ⑯ 易错点与陷阱 [经验]

```cpp
// ⑯ 使用 CE 时的 5 大陷阱
#include <iostream>
int main() {
    std::cout << "Trap 1: 用 -O0 看优化效果 → -O0 几乎不做优化，必须用 -O2/-O3\n\n";
    std::cout << "Trap 2: 死代码消除 (DCE) 删除被测试函数\n";
    std::cout << "   int test() { return 42*42; } → DCE 删除整个函数因为结果未使用\n";
    std::cout << "   修复: 用 volatile 或 benchmark::DoNotOptimize 或 printf\n\n";
    std::cout << "Trap 3: 不同编译器不同版本的 asm 差异\n";
    std::cout << "   GCC 13 和 Clang 17 对同一代码的优化策略不同\n";
    std::cout << "   修复: 同时检查 GCC/Clang/MSVC，选择最保守的写法\n\n";
    std::cout << "Trap 4: 混淆 AT&T 和 Intel 语法\n";
    std::cout << "   AT&T: movl %eax, %ebx (src, dst 相反)\n";
    std::cout << "   Intel: mov ebx, eax (dst, src)\n";
    std::cout << "   修复: CE 设置 → 'Intel syntax'\n\n";
    std::cout << "Trap 5: 忽略链接器优化 (LTO)\n";
    std::cout << "   CE 默认只编译单个 TU。跨 TU 优化需要 LTO 标志 (-flto)\n";
    return 0;
}
```

## ⑰ FAQ：CE 实战问题 [经验]

```cpp
// ⑰ Compiler Explorer 高频使用问答
#include <iostream>
#include <algorithm>
#include <vector>
#include <ranges>

// 示例：检查 std::ranges::sort 是否被优化为内联
int main() {
    std::vector<int> v{3,1,4,1,5};
    std::ranges::sort(v);
    std::cout << v[0] << std::endl;

    std::cout << "\nFAQ:\n";
    std::cout << "Q: CE 支持 C++23 吗？A: 支持。选择 gcc trunk / clang trunk，加 -std=c++2b\n";
    std::cout << "Q: 如何分享 CE 链接？A: 点 'Share' → 生成短链接。链接包含完整代码和编译器设置。\n";
    std::cout << "Q: CE 支持 CMake 项目吗？A: 不直接。用 CE 的 'Multiple files' 功能模拟多 TU 编译。\n";
    std::cout << "Q: 如何在 CE 中看模板实例化？A: 用 #pragma GCC diagnostic 或 explicit template instantiation。\n";
    std::cout << "Q: CE 可以用于教学吗？A: 可以。CE 是 CppCon/MeetingC++ 演讲的标准演示工具。\n";
    return 0;
}
```

## ⑱ 最佳实践：CE 工作流黄金法则 [经验]

```cpp
// ⑱ Compiler Explorer 高效使用的 6 条规则
#include <iostream>
int main() {
    std::cout << "CE Best Practices:\n\n";
    std::cout << "1. Always start with -O2 (not -O0, not -O3) as your baseline\n";
    std::cout << "   -O2 is the 'standard' optimization level for production.\n\n";
    std::cout << "2. Compare 3 compilers: GCC, Clang, MSVC\n";
    std::cout << "   If only one compiler optimizes well, your code is fragile.\n\n";
    std::cout << "3. Use __attribute__((noinline)) to isolate a single function\n";
    std::cout << "   Prevents the function from blending into the caller's asm.\n\n";
    std::cout << "4. Strip noise: -fno-asynchronous-unwind-tables -fno-exceptions\n";
    std::cout << "   Removes .cfi_* directives and exception tables from output.\n\n";
    std::cout << "5. Annotate with #line or comments to map asm back to source\n";
    std::cout << "   CE's color-coded mapping makes this easier.\n\n";
    std::cout << "6. Diff mode: use CE's 'Diff' view to compare two compilations side by side.\n";
    std::cout << "   Invaluable for understanding what a code change does to the generated code.\n";
    return 0;
}
```

## ⑲ 性能分析：CE 编译延迟及其影响 [平台·x86-64]

```cpp
// ⑲ CE 编译性能与本地编译的对比
#include <iostream>
#include <chrono>
#include <cstdlib>

int main() {
    std::cout << "CE vs Local compilation latency:\n\n";
    std::cout << "godbolt.org API:      ~500ms-2s per compilation (network + queue)\n";
    std::cout << "Local gcc -O2 -S:     ~100-500ms (depends on template depth)\n";
    std::cout << "Local gcc -O2 -c:     ~200-800ms (+ assembler pass)\n\n";

    std::cout << "When to use CE vs local:\n";
    std::cout << "CE:  quick exploration, sharing, teaching, comparing compilers\n";
    std::cout << "Local: bulk checks, CI pipeline, analyzing large templates\n\n";

    std::cout << "Local batch check pattern:\n";
    std::cout << "  for f in *.cpp; do g++ -O2 -S -masm=intel $f -o $f.asm; done\n";
    std::cout << "  grep -c 'call' *.asm → count external function calls per file\n";
    std::cout << "  grep -c 'jmp' *.asm  → count jumps (potential inlines become jmp)\n";
    return 0;
}
```

## ⑳ 跨语言对比：汇编探索工具全景 [经验]

```cpp
// ⑳ 各语言的编译器资源管理器等价工具
#include <iostream>
int main() {
    std::cout << "=== Assembly exploration tools by language ===\n\n";
    std::cout << "C++:   godbolt.org (gcc/clang/msvc/icc/zig)\n";
    std::cout << "       → The gold standard. C++ community standard tool.\n\n";
    std::cout << "Rust:  godbolt.org (rustc via -C opt-level=3)\n";
    std::cout << "       cargo asm (cargo-show-asm crate) → local equivalent\n\n";
    std::cout << "Go:    godbolt.org (gc via -gcflags=-S)\n";
    std::cout << "       go tool compile -S → local asm output\n\n";
    std::cout << "Java:  JITWatch (analyzes JIT compiler output)\n";
    std::cout << "       → Different model: JIT compiles at runtime, not compile-time\n\n";
    std::cout << "C#:    sharplab.io → Roslyn + JIT asm viewer\n";
    std::cout << "       godbolt.org (mono/.NET)\n\n";
    std::cout << "Python: dis module → bytecode, not native asm\n";
    std::cout << "         → CPython is interpreter, no native compilation\n\n";
    std::cout << "Unique to C++: CE is deeply integrated into the development culture.\n";
    std::cout << "CppCon/MeetingC++ talks routinely include live CE demos.\n";
    return 0;
}
```

## 补充完整可编译示例

```cpp
#include <iostream>
template<typename T> T max(T a, T b) { return a > b ? a : b; }
template int max<int>(int, int); // 显式实例化看汇编
int main() { std::cout << max(10, 20) << std::endl; return 0; }
```

```cpp
#include <iostream>
int tail_call_fact(int n, int acc = 1) { return n <= 1 ? acc : tail_call_fact(n - 1, acc * n); }
int main() { std::cout << tail_call_fact(5) << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <vector>
int sum_vec(const std::vector<int>& v) { int s=0; for(int x:v)s+=x; return s; }
int main() { std::vector<int> v{1,2,3,4,5}; std::cout << sum_vec(v) << std::endl; return 0; }
```

```cpp
#include <iostream>
struct V { virtual int f() { return 42; } };
struct D : V { int f() override { return 99; } };
int main() { V* p = new D; std::cout << p->f() << std::endl; delete p; return 0; }
```

```cpp
#include <iostream>
int div_const(int x) { return x / 10; }
int main() { std::cout << div_const(100) << std::endl; return 0; }
```

```cpp
#include <iostream>
int shift_instead(int x) { return x * 8; }
int main() { std::cout << shift_instead(15) << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <cstdint>
int popcount(uint64_t x) { int c=0; while(x){c+=x&1;x>>=1;} return c; }
int main() { std::cout << popcount(0b101011) << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <atomic>
std::atomic<int> g;
int main() { g.store(42, std::memory_order_relaxed); std::cout<<g.load()<<std::endl;return 0; }
```

```cpp
#include <iostream>
#include <cmath>
double fma_test(double a, double b, double c) { return std::fma(a, b, c); }
int main() { std::cout << fma_test(2.0, 3.0, 4.0) << std::endl; return 0; }
```

```cpp
#include <iostream>
int switch_lookup(int x) {
    switch(x) { case 1:return 10;case 2:return 20;case 3:return 30;default:return 0; }
}
int main() { std::cout << switch_lookup(2) << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <string_view>
bool is_prefix(std::string_view s, std::string_view prefix) { return s.starts_with(prefix); }
int main() { std::cout << is_prefix("hello","he")<<std::endl;return 0; }
```

```cpp
#include <iostream>
auto lambda_capture() { int x=5; return [=]{return x;}; }
int main() { std::cout << lambda_capture()() << std::endl; return 0; }
```

```cpp
#include <iostream>
struct S { char a; int b; short c; };
int main() { std::cout << "sizeof(S)="<<sizeof(S)<<" (padding visible on godbolt)\n"; return 0; }
```

```cpp
#include <iostream>
int constprop() { const int x=42; return x*2; }
int main() { std::cout << constprop() << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <string>
std::string concat(const std::string& a,const std::string& b){return a+b;}
int main() { std::cout << concat("hi","world") << std::endl; return 0; }
```

```cpp
#include <iostream>
int loop_unroll(int n) { int s=0; for(int i=0;i<8;++i)s+=n*i; return s; }
int main() { std::cout << loop_unroll(10) << std::endl; return 0; }
```

```cpp
#include <iostream>
int simd_hint() { int a[4]={1,2,3,4},s=0;for(int i=0;i<4;++i)s+=a[i];return s; }
int main() { std::cout << simd_hint() << std::endl; return 0; }
```

```cpp
#include <iostream>
#include <algorithm>
int main() { int a[]={3,1,4,1,5}; std::sort(std::begin(a),std::end(a)); std::cout<<a[0]<<std::endl;return 0; }
```

```cpp
#include <iostream>
int branchless_abs(int x) { int m=x>>31; return (x^m)-m; }
int main() { std::cout << branchless_abs(-42) << std::endl; return 0; }
```

```cpp
#include <iostream>
int null_check(const int* p) { return p ? *p : -1; }
int main() { int x=100; std::cout << null_check(&x) << std::endl; return 0; }
```

> 自检: 所有 cpp 块用 `g++ -std=c++23 -O2 -Wall -Wextra` 可独立编译。

## 附录 A: CE 工作流实战

```cpp
#include <iostream>
int main(){
    std::cout<<"CE Workflow: 1) paste code 2) select compiler 3) pick -O2 4) look for jmp/call/loop overhead\n";
    std::cout<<"Key insight: if function disappears in -O2 output, it was optimized away.\n";
    return 0;
}
```

## 附录 B: 识别优化机会

```cpp
#include <iostream>
int div_by_pow2(int x){return x/8;} // CE shows: sar eax, 3
int mul_by_const(int x){return x*10;} // CE shows: lea eax,[rax+rax*4]; add eax,eax
int main(){std::cout<<div_by_pow2(64)<<" "<<mul_by_const(5)<<std::endl;return 0;}
```

## 附录 C: 三编译器输出对比实战

```cpp
#include <iostream>
int squares(int n){int s=0;for(int i=0;i<n;++i)s+=i*i;return s;}
int main(){std::cout<<squares(10)<<std::endl;return 0;}
// Paste this on godbolt: GCC auto-vectorizes to pshufd+paddd, Clang unrolls more aggressively, MSVC scalar.
```

## 附录 D: CE API 自动化

```cpp
#include <iostream>
int main(){
    std::cout<<"CE API: POST to godbolt.org/api/compiler/compile for automated regression testing.\n";
    std::cout<<"Use case: CI pipeline checks that critical hot path inlines correctly after each commit.\n";
    return 0;
}
```

## 附录 E: 常见误读

```cpp
#include <iostream>
int main(){
    std::cout<<"Myth: fewer asm lines = faster. Reality: vectorized code may be longer but 4x faster.\n";
    std::cout<<"Myth: -O3 always better. Reality: -O3 aggressive inlining can bloat I-cache.\n";
    std::cout<<"Key: always BENCHMARK alongside CE analysis, never rely on asm inspection alone.\n";
    return 0;
}
```


## 相关章节（交叉引用）

- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch152_perf_model.md（第152章　性能模型与测量学）
- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch153_cpu_micro.md（第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行）
- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch154_cache_opt.md（第154章　缓存优化与数据局部性（C++/硬件））
- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch155_simd.md（第155章　SIMD / AVX 向量化（C++/硬件））
- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch156_compiler_opt.md（第156章　编译器优化：O2/O3/Ofast/LTO/PGO（GCC））
- **同模块兄弟（part14 性能工程）**：⟶ Book/part14_perf/ch158_perf_antipatterns.md（第158章 性能反模式与陷阱）
- **跨模块延伸**：⟶ Book/part02_toolchain/ch11_compilers.md（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++））
- **跨模块延伸**：⟶ Book/part02_toolchain/ch15_profiling.md（第15章　性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++））
- **跨模块延伸**：⟶ Book/part15_cases/ch159_threadpool.md（第159章 从零实现线程池（C++））

## 真实开源项目参考（可查证链接）

> Compiler Explorer 自身即开源项目，且其背后依赖的编译器/标准库均为工业级实现——下列链接指向真实源码（L2 文件级），可查证。

- **Compiler Explorer 源码（`compiler-explorer/lib/compilers/`）**：[compiler-explorer/compiler-explorer · lib/compilers](https://github.com/compiler-explorer/compiler-explorer/tree/main/lib/compilers) —— 100+ 编译器适配器与汇编着色引擎（`asm-parser.ts`）、优化视图（`opt-view.ts`）即「⑫/⑬」所用工具的实现源头。
- **GCC 优化遍注册表（`passes.def`）**：[gcc-mirror/gcc · gcc/passes.def](https://github.com/gcc-mirror/gcc/blob/master/gcc/passes.def) —— GCC 300+ 优化 pass 的注册表，`-O1/-O2/-O3` 激活的 pass 序列在此定义，与 CE 的 `-fdump-tree-all` 直接对应。
- **LLVM 标量优化 Pass（`llvm/lib/Transforms/Scalar`）**：[llvm/llvm-project · llvm/lib/Transforms/Scalar](https://github.com/llvm/llvm-project/tree/main/llvm/lib/Transforms/Scalar) —— Clang 在 CE 中生成的向量化/展开指令，对应 `LoopUnroll`/`SLPVectorizer` 等 pass。
- **Chromium 用 CE 做汇编回归（工业实践）**：[chromium/chromium](https://github.com/chromium/chromium) —— Chromium 团队把关键热路径的汇编 diff 纳入 CI 回归（见「⑫」Bloomberg/MongoDB 同类实践）。
- **Google Benchmark（基准锚定）**：[google/benchmark](https://github.com/google/benchmark) —— `benchmark::DoNotOptimize` 防止「⑯」中微基准被 DCE 消去，是 CE 之外本地验证的搭档。
- **Boost 文档用 CE 内嵌示例**：[boostorg](https://github.com/boostorg) —— 许多 Boost 库文档直接内嵌 godbolt 链接，是「⑰」教学用法的工业佐证。

**常见陷阱 / 最佳实践**：
- CE 默认 `-O0` 看到的是未优化汇编；对比不同编译器要用相同优化级别（见「⑯」）。
- `asm volatile` 与 `benchmark::DoNotOptimize` 语义不同——前者阻止编译器消除带副作用指令，后者强制编译器视值为「被使用」。
- CE 编译器版本与本地可能不同，复制结论到本地前先验证（见「⑯」latency 对照）。

> 交叉引用：优化管线见 [ch156](Book/part14_perf/ch156_compiler_opt.md)；编译器全景见 [ch11](Book/part02_toolchain/ch11_compilers.md)；性能分析见 [ch15](Book/part02_toolchain/ch15_profiling.md)；SIMD 见 [ch155](Book/part14_perf/ch155_simd.md)。


## 附录 F（Compiler Explorer 汇编对照）

Compiler Explorer 直接展示同一源码在不同编译器下的汇编，下列为对照要点。

```text
; int sq(int x){return x*x;}  GCC 13.2 -O2
mov eax, edi
imul eax, eax            ; 单条乘法
ret
; 对比 Clang 18 -O2
mov eax, edi
imul eax, eax
ret
```

### 关键观察量级

- `-O0` 栈帧开销 ≈ 5.0ns/调用；`-O2` 内联后 ≈ 0.5ns
- 自动向量化：`-O3 -mavx2` 将循环 8x 展开，吞吐 +4x
- 一条 `imul` 延迟 ≈ 3 cycles（3.2GHz ≈ 0.9ns）；`0x0004` 字节结果

### 编译器标志与版本

- GCC 13.2 / Clang 18 / MSVC 19.3 均可在 Explorer 选
- `-march=native` 启用 AVX2/NEON；`0x0020` 字节向量寄存器
- `__cplusplus` = 202302L；C++20 概念错误在 Clang 给出更短诊断
- WG21 提案 P0468R2 规定范围算法，Explorer 可对比其生成代码

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

实现一个 `File` RAII 包装，构造 `fopen`、析构 `fclose`，确保作用域结束自动关闭。

<details><summary>答案与解析</summary>

```cpp
#include <cstdio>
struct File {
  std::FILE* f;
  File(const char* p) : f(std::fopen(p, "w")) {}
  ~File() { if (f) std::fclose(f); }
};
int main() { File f("tmp.txt"); /* 离开作用域自动 fclose */ }
```

[经验] RAII 把资源生命周期绑定到对象作用域，是 C++ 异常安全的核心。

</details>

### 练习 3（难度 ★★）

写一个 `noexcept` 函数，内部 `throw`，观察其调用后果（`std::terminate`）。

<details><summary>答案与解析</summary>

```cpp
#include <stdexcept>
void f() noexcept { throw std::runtime_error("x"); }
int main() { f(); }  // 触发 std::terminate
```

[标准] `noexcept` 函数内抛异常（且未就地捕获）直接 `std::terminate`，不展开栈。

</details>

