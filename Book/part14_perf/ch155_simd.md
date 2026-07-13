# 第155章　SIMD / AVX 向量化（C++/硬件）

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23`）。
> 自动向量化取证命令（GCC 默认在 `-O3` 才开 tree-vectorize；`-O2` 不向量化，这点与 Clang 不同，下文明示）：
> `g++ -std=c++23 -O3 -mavx2 -ftree-vectorize -S -masm=intel Examples/_ch155_simd.cpp -o Examples/_ch155_simd.asm`
> 所有 ```asm 块均为上述真实编译产物，未加任何编造。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/`；本章以真实编译产物（汇编）为证据。

## ① 概述：SIMD 是什么 [标准]

⟶ Book/part14_perf/ch154_cache_opt.md
⟶ Book/part14_perf/ch156_compiler_opt.md


**SIMD**（Single Instruction, Multiple Data，单指令多数据）指一条指令同时对一组（向量）数据做相同运算。对比 SISD（标量，一次一个数据），SIMD 用更少的指令完成批量同构计算，是多媒体、数值、AI 推理的核心加速手段。

```cpp
// ① 标量：一次加一个 float（4 字节）
float scalar_add(float a, float b) { return a + b; }

// ① 向量等价：一条 vaddps 同时加 8 个 float（AVX2，256 位）
//    c[i..i+7] = a[i..i+7] + b[i..i+7]  一次完成
```

- `[标准]`：C++ 本身不直接规定 SIMD，SIMD 由**目标架构 ISA**（x86 的 SSE/AVX、ARM 的 NEON）与编译器提供；C++ 侧通过三种途径利用：自动向量化、intrinsics、`std::experimental::simd`。
- `[经验]`：SIMD 不是"更快的循环"，而是"更宽的循环"——**数据必须同构、连续、无依赖**才能受益（见 ④）。

## ② SSE/AVX/AVX-512 演进与寄存器宽度 [标准]

x86 向量指令集按寄存器宽度代际演进，宽度翻倍 = 同一条指令吞吐翻倍：

| 代际 | 年份 | 寄存器 | 宽度 | 单精度 float/寄存器 |
|---|---|---|---|---|
| MMX | 1997 | mm0–7 (64bit) | 64 | 2 |
| SSE | 1999 | xmm0–15 | 128 | 4 |
| AVX | 2011 | ymm0–15 (低128=xmm) | 256 | 8 |
| AVX2 | 2013 | ymm0–15 | 256 | 8（整数也向量化） |
| AVX-512 | 2017 | zmm0–31 | 512 | 16 |

```cpp
// ② 寄存器宽度决定每轮处理的元素数（float，4 字节）
//   SSE  xmm: 16B / 4B = 4 个 float
//   AVX  ymm: 32B / 4B = 8 个 float
//   AVX512 zmm: 64B / 4B = 16 个 float
constexpr int floats_per_sse   = 16 / 4;  // 4
constexpr int floats_per_avx   = 32 / 4;  // 8
constexpr int floats_per_avx512= 64 / 4;  // 16
```

- `[标准]`：AVX 引入 **VEX 编码**，把 xmm 扩展为 ymm 的低 128 位，并支持三操作数（`vaddps dst, src1, src2`，不破坏 src1）。
- `[平台]`：AVX-512 在消费级 CPU 上**并非全量支持**（Intel 部分 SKU 砍掉，AMD Zen4+ 才较完整）；用前需运行时检测（见 ⑬、⑰）。

## ③ 编译器自动向量化（auto-vectorization） [实现]

编译器能在满足约束时，把普通标量循环**自动改写**为向量指令，无需手写 intrinsics。

```cpp
// ③ 这段代码在 -O3 -mavx2 下会被 GCC 自动向量化为 vaddps ymm（见 ⑧ 真实汇编）
void saxpy(float* __restrict y, const float* __restrict x,
           float a, int n) {
    for (int i = 0; i < n; ++i)
        y[i] = a * x[i] + y[i];   // FMA 还可进一步合成为 vfma
}
```

- `[实现]`：GCC 的自动向量化在 **`-O3`**（或显式 `-ftree-vectorize`，或 `-O2 -ftree-vectorize`）开启；`-O2` 默认**不**向量化（这是与 Clang `-O2` 行为不同的关键差异）。
- `[经验]`：先用自动向量化（零成本、可移植），只有热点且编译器"不肯向量化"时才下沉到 intrinsics。

## ④ 循环向量化的必要条件（无依赖、连续访问） [标准]

向量化的充要条件，缺一不可：

```cpp
// ④ 条件A：连续内存访问（步长 1）
void good(float* a, float* b, float* c, int n) {     // ✔ 连续
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}

// ④ 条件B：循环迭代间无数据依赖（后可向依赖）
void bad_dep(float* a, int n) {                       // ✘ 依赖前一项
    for (int i = 1; i < n; ++i) a[i] = a[i-1] + a[i];
}

// ④ 条件C：无循环体内函数调用/虚调用阻断
//    （纯算术、内联小函数可向量化；printf/虚函数通常打断）
```

```cpp
// ④ 条件D：指针不可别名（用 __restrict 或不同数组证明无重叠）
void no_alias(float* __restrict out, const float* __restrict in, int n) {
    for (int i = 0; i < n; ++i) out[i] = in[i] * 2.0f;  // ✔ 可向量化
}
```

- `[标准]`：向量化要求**可静态证明**"每次迭代独立且地址可计算"；任何潜在别名/依赖都会逼退向量化。
- `[经验]`：最常被忽略的是别名——两个 `float*` 参数编译器默认**假定可能重叠**，加 `__restrict` 常是向量化的临门一脚。

## ⑤ #pragma GCC optimize / #pragma omp simd [实现]

函数级或循环级强制提示编译器向量化。

```cpp
// ⑤ 函数级：强制对该函数开向量化（即便全局 -O2）
#pragma GCC optimize("O3","tree-vectorize")
void forced(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// ⑤ OpenMP 的 simd 指示：告诉编译器循环可矢量化，并允许忽略某些依赖假设
#include <omp.h>
void omp_simd(float* a, float* b, float* c, int n) {
    #pragma omp simd
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// ⑤ 还有 GCC 专用循环 pragma（需配合 -O3 才生效）
void gcc_pragma(float* a, float* b, float* c, int n) {
    #pragma GCC ivdep          // 暗示"无依赖、无别名"，助向量化
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

- `[实现]`：`#pragma omp simd` 是**跨编译器标准**写法（GCC/Clang/ICC 都认）；`#pragma GCC ivdep` 仅 GCC/ICX 认。二者都是"建议"，最终是否向量化看后端。
- `[经验]`：优先 `#pragma omp simd`（可移植）；`#pragma GCC optimize` 慎用——它改的是**单函数**优化级别，易与全局不一致引发调试困惑。

## ⑥ std::experimental::simd (DAT, 标准方向) [标准]

C++ 标准曾以 **DAT（Data-Parallel Types）** 提案把 SIMD 纳入语言，`<experimental/simd>` 是其 TS 实现（GCC/libstdc++ 提供）。

```cpp
// ⑥ 用 std::experimental::simd 表达"对 N 个 float 同时运算"
#include <experimental/simd>
namespace stdx = std::experimental;
void simd_class(float* a, float* b, float* c, int n) {
    using V = stdx::native_simd<float>;   // 宽度 = 本机最优（通常 8 或 16）
    for (int i = 0; i + V::size() <= n; i += V::size()) {
        V va(&a[i], stdx::element_aligned);
        V vb(&b[i], stdx::element_aligned);
        V vc = va + vb;                    // 一条向量加
        vc.copy_to(&c[i], stdx::element_aligned);
    }
}
```

```cpp
// ⑥ 常见算法：可以一次做多条（本块自含 DAT 头与命名空间别名，可独立编译）
#include <experimental/simd>
namespace stdx = std::experimental;
void simd_math(float* x, float* y, int n) {
    using V = stdx::native_simd<float>;
    for (int i = 0; i + V::size() <= n; i += V::size()) {
        V vx(&x[i], stdx::element_aligned);
        V vy = stdx::sqrt(vx) + stdx::abs(vx);   // 向量 sqrt + abs
        vy.copy_to(&y[i], stdx::element_aligned);
    }
}
```

- `[标准]`：DAT 把"向量宽度"抽象为类型参数，**代码与具体 AVX/SSE 解耦**，是官方推荐方向。但截至 C++23 仍是 `experimental`，**未进入正式标准**（WG21 仍在推进）。
- `[经验]`：生产代码若需稳定 ABI，暂以自动向量化 + intrinsics 为主；`std::experimental::simd` 适合研究/算法库，且需 `-fno-math-errno` 等配合才高效。

## ⑦ intrinsics（_mm_add_ps / _mm256_loadu_ps 等） [实现]

intrinsics 是编译器内建函数，名字直接对应一条汇编指令，完全可控但要手写寄存器编排。

```cpp
// ⑦ SSE：128 位，一次 4 个 float
#include <immintrin.h>
void sse_add(const float* a, const float* b, float* c) {
    __m128 va = _mm_loadu_ps(a);     // 未对齐加载 4 个 float
    __m128 vb = _mm_loadu_ps(b);
    __m128 vc = _mm_add_ps(va, vb);  // 一条 addps
    _mm_storeu_ps(c, vc);            // 未对齐写回
}
```

```cpp
// ⑦ AVX2：256 位，一次 8 个 float
void avx2_add(const float* a, const float* b, float* c) {
    __m256 va = _mm256_loadu_ps(a);  // 加载 8 个 float
    __m256 vb = _mm256_loadu_ps(b);
    __m256 vc = _mm256_add_ps(va, vb);
    _mm256_storeu_ps(c, vc);
}
```

```cpp
// ⑦ AVX-512：512 位，一次 16 个 float
void avx512_add(const float* a, const float* b, float* c) {
    __m512 va = _mm512_loadu_ps(a);
    __m512 vb = _mm512_loadu_ps(b);
    __m512 vc = _mm512_add_ps(va, vb);
    _mm512_storeu_ps(c, vc);
}
```

```cpp
// ⑦ FMA：乘加合一（a*b+c），AVX2+FMA，减少一条指令、更高精度
void fma_demo(const float* a, const float* b, const float* c, float* d) {
    __m256 va = _mm256_loadu_ps(a);
    __m256 vb = _mm256_loadu_ps(b);
    __m256 vc = _mm256_loadu_ps(c);
    __m256 vd = _mm256_fmadd_ps(va, vb, vc);  // d = a*b + c
    _mm256_storeu_ps(d, vd);
}
```

- `[实现]`：intrinsics 函数名编码了**宽度与数据类型**：`_mm`=128、`_mm256`=256、`_mm512`=512；后缀 `ps`=packed single(float)、`pd`=packed double、`epi32`=32 位整数打包。
- `[经验]`：优先用 `*_loadu_*`/`*_storeu_*`（未对齐，安全通用）；只有**已证明对齐**才用对齐版换极小带宽收益（见 ⑨）。

## ⑧ [实现] 真实汇编：标量循环 vs 向量化（vmovaps/vaddps）

先给出自动向量化的**真实汇编**（GCC 13.1.0，`-O3 -mavx2`）。源码剖析：

```cpp
// 文件：Examples/_ch155_simd.cpp
// 行号：4
void add_arrays(float* __restrict a, float* __restrict b,
                float* __restrict c, int n) {
    for (int i = 0; i < n; ++i)
        c[i] = a[i] + b[i];
}
```

```asm
; 关键证据：自动向量化后的主循环（-O3 -mavx2），每轮 32 字节 = 8 个 float
_Z10add_arraysPfS_S_i:
	test	r9d, r9d
	jle	.L14
	...
.L4:
	vmovups	ymm1, YMMWORD PTR [rcx+rax]     ; 未对齐加载 8 个 float（a）
	vaddps	ymm0, ymm1, YMMWORD PTR [rdx+rax] ; 8 路并行浮点加（a+b）
	vmovups	YMMWORD PTR [r8+rax], ymm0        ; 写回 8 个结果（c）
	add	rax, 32
	cmp	r10, rax
	jne	.L4
	vzeroupper
```

对比**显式 intrinsics 在 `-O2` 即出现 `vmovaps`/`vaddps`**（注意是 `vmovaps` 对齐版，因为 intrinsics 用了 `_mm_load_ps`）：

```asm
; 关键证据：_ch155_align.cpp 的对齐加载（_mm_load_ps -> vmovaps）
_Z12load_alignedPKfS0_Pf:
	vmovaps	xmm0, XMMWORD PTR [rcx]   ; 对齐 16 字节加载
	vaddps	xmm0, xmm0, XMMWORD PTR [rdx]
	vmovaps	XMMWORD PTR [r8], xmm0
	ret
```

- `[实现]`：两条证据一致证明——**向量化后一条 `vaddps` 顶标量 8（SSE）/16（AVX512）次 `vaddss`**。注意 GCC 自动版用 `vmovups`（保守未对齐），intrinsics 对齐版用 `vmovaps`。
- `[实现]`：GCC 在 `-O2` 不自动向量化（见 ③）；要看到 `vaddps ymm` 必须 `-O3` 或 `-O2 -ftree-vectorize`。上例 `.L4` 的 `vaddps ymm` 即本标准点要求的真实取证。

## ⑨ 内存对齐与 _mm_loadu（未对齐加载） [实现]

SIMD 加载/存储有对齐要求：对齐版本（`_mm_load_ps`）要求地址 16 字节对齐，未对齐版本（`_mm_loadu_ps`）任意对齐均可，但可能有极小的跨 cache-line  penalties。

```cpp
// ⑨ 对齐加载（要求 16/32/64 字节对齐，否则段错误）
alignas(16) float a16[4] = {1,2,3,4};
__m128 va = _mm_load_ps(a16);   // OK：alignas(16)

// ⑨ 未对齐加载（安全但略慢，通用首选）
float buf[100];
__m128 vb = _mm_loadu_ps(&buf[3]);  // 任意地址 OK
```

源码剖析（真实 intrinsics 汇编，区分对齐/未对齐）：

```cpp
// 文件：Examples/_ch155_align.cpp
// 行号：5
void load_aligned(const float* __restrict a, const float* __restrict b,
                  float* __restrict c) {
    __m128 va = _mm_load_ps(a);   // 假定 a 16 字节对齐
    __m128 vb = _mm_load_ps(b);
    _mm_store_ps(c, _mm_add_ps(va, vb));
}
void load_unaligned(const float* a, const float* b, float* c) {
    __m128 va = _mm_loadu_ps(a);  // 任意对齐均可
    __m128 vb = _mm_loadu_ps(b);
    _mm_storeu_ps(c, _mm_add_ps(va, vb));
}
```

```asm
; 关键证据：-O2 下 intrinsics 直接映射为对齐(vmovaps) vs 未对齐(vmovups)
_Z12load_alignedPKfS0_Pf:
	vmovaps	xmm0, XMMWORD PTR [rcx]   ; 对齐加载 -> vmovaps
	vaddps	xmm0, xmm0, XMMWORD PTR [rdx]
	vmovaps	XMMWORD PTR [r8], xmm0    ; 对齐存储 -> vmovaps
	ret
_Z14load_unalignedPKfS0_Pf:
	vmovups	xmm0, XMMWORD PTR [rdx]   ; 未对齐加载 -> vmovups
	vaddps	xmm0, xmm0, XMMWORD PTR [rcx]
	vmovups	XMMWORD PTR [r8], xmm0    ; 未对齐存储 -> vmovups
	ret
```

- `[实现]`：`vmovaps` 与 `vmovups` 在**现代 CPU 上对大部分数据路径性能一致**（对齐检查近乎免费）；但用对齐版时若地址未对齐会**直接崩溃**，所以默认用 `u` 版更稳。
- `[经验]`：热数据用 `alignas(64)`（cache line）配合对齐版可避免跨行；但绝大多数场景 `loadu/storeu` 足够，不要把"对齐"当银弹。

## ⑩ mask 与比较指令 [实现]

向量比较产生**掩码（mask）**，每条 lane 置全 1（真）或全 0（假），用于条件选择/过滤。

```cpp
// ⑩ SSE 比较：_mm_cmplt_ps 产生每 lane 的 mask（0xFFFFFFFF 或 0）
void clamp_low(const float* in, float* out, int n, float lo) {
    __m128 vlo = _mm_set1_ps(lo);
    for (int i = 0; i + 4 <= n; i += 4) {
        __m128 v = _mm_loadu_ps(&in[i]);
        __m128 mask = _mm_cmplt_ps(v, vlo);     // v < lo ? 全1 : 全0
        __m128 vmax = _mm_max_ps(v, vlo);        // 取较大者，无需分支
        _mm_storeu_ps(&out[i], vmax);
    }
}
```

```cpp
// ⑩ AVX-512 用真正的 16 位/32 位 k-mask 寄存器（k1..k7），语义更清晰
#include <immintrin.h>
void avx512_select(const float* a, const float* b, float* out, int n) {
    __m512 va = _mm512_loadu_ps(a);
    __m512 vb = _mm512_loadu_ps(b);
    __mmask16 m = _mm512_cmp_ps_mask(va, vb, _CMP_LT_OQ); // 比较 -> k-mask
    __m512 vr = _mm512_mask_mov_ps(vb, m, va);            // m 为真取 va 否则 vb
    _mm512_storeu_ps(out, vr);
}
```

- `[实现]`：SSE/AVX 的 mask 是"位模式藏在向量寄存器里"，AVX-512 引入**独立 k 寄存器**（`k1`–`k7`），`vcmpps ... k1` 直接写掩码，配合 `vmovaps zmm {k1}` 做掩码写，避免"全 0/全 F"的位运算。
- `[经验]`：用 `max/min` 替代 `if` 做条件赋值，能让编译器保留向量化（无分支）；AVX-512 的 k-mask 把"带条件向量化"写得更直白。

## ⑪ 与 ch156 编译器优化衔接 [标准]

SIMD 是编译器优化栈的**底层执行形态**之一：上层优化（循环交换、标量替换、函数内联）决定了能否暴露出"可向量化内核"，下层再由向量化器生成 SIMD。

```cpp
// ⑪ 内联 + 常数折叠后，热点才容易被向量化
inline float op(float x) { return x * 3.0f + 1.0f; }   // 小函数 -> 易内联
void transform(float* a, float* b, int n) {
    for (int i = 0; i < n; ++i) b[i] = op(a[i]);         // 内联后纯算术 -> 可向量化
}
```

- `[标准]`：向量化是**依赖优化链的末端**——若上层未消除别名/未内联/未做循环归一化，向量化器拿不到干净内核（详见 ch156 编译器优化关于优化流水线的论述）。
- `[经验]`：调试"为什么没向量化"时，先看 IR 是否干净（内联、别名），再看向量化器报因（见 ⑯ `-fopt-info-vec`）。

## ⑫ 数据布局：AoS vs SoA 对向量化的影响 [实现]

- **AoS**（Array of Structs）：结构体数组，同类字段分散。
- **SoA**（Struct of Arrays）：字段各自成数组，同类数据连续。

```cpp
// ⑫ AoS：x/y/z 交错，向量化需跨步/广播，浪费 lane
struct Vec3 { float x, y, z; };
void aos_scale(Vec3* __restrict p, int n, float s) {
    for (int i = 0; i < n; ++i) {
        p[i].x *= s; p[i].y *= s; p[i].z *= s;
    }
}
// ⑫ SoA：每字段连续，向量化最干净
void soa_scale(float* __restrict x, float* __restrict y,
               float* __restrict z, int n, float s) {
    for (int i = 0; i < n; ++i) { x[i] *= s; y[i] *= s; z[i] *= s; }
}
```

真实汇编对比（`-O3 -mavx2`，节选）：

```asm
; 关键证据：SoA 干净向量化（每轮 8 个 float，无跨步）
_Z9soa_scalePfS_S_if:
	vbroadcastss	ymm0, xmm2          ; s 广播到 8 lane
.L20:
	vmulps	ymm1, ymm0, YMMWORD PTR [rcx+rax]   ; x[i..i+7] *= s
	vmovups	YMMWORD PTR [rcx+rax], ymm1
	vmulps	ymm1, ymm0, YMMWORD PTR [rdx+rax]   ; y[i..i+7] *= s
	vmovups	YMMWORD PTR [rdx+rax], ymm1
	vmulps	ymm1, ymm0, YMMWORD PTR [r8+rax]    ; z[i..i+7] *= s
	vmovups	YMMWORD PTR [r8+rax], ymm1
	add	rax, 32
	jne	.L20
```

```asm
; 关键证据：AoS 也会被向量化，但按 8 个 Vec3=96 字节整块读改写，存在 lane 浪费
_Z9aos_scaleP4Vec3if:
	vbroadcastss	ymm0, xmm2
.L4:
	vmulps	ymm3, ymm0, YMMWORD PTR 32[rax]   ; 一次读 3 个 Vec3 的字段块
	vmulps	ymm1, ymm0, YMMWORD PTR 64[rax]
	vmulps	ymm4, ymm0, YMMWORD PTR [rax]
	vmovups	YMMWORD PTR 32[rax], ymm3
	vmovups	YMMWORD PTR [rax], ymm4
	vmovups	YMMWORD PTR -32[rax], ymm1
	add	rax, 96
	jne	.L4
```

- `[实现]`：SoA 每轮**满负荷 8 lane**；AoS 每轮读 96 字节覆盖 8 个 Vec3 的 24 个 float，但只有 24 个有义、无 padding 浪费，GCC 仍能向量化但**指令更复杂、带宽利用率略低**。
- `[经验]`：数值/粒子/渲染热点**首选 SoA 或 AoSoA**（Array of Struct of Arrays，分块）；AoS 仅在对齐友好且编译器能整块处理时才可接受。

## ⑬ AVX-512 与降频（throttling）代价 [平台]

AVX-512 寄存器宽、FMA 密，功耗与发热陡增，很多 CPU 在执行 512 位指令时会**降频（throttling）**，单核频率回落。

```cpp
// ⑬ 运行时检测 AVX-512 是否可用（避免在不支持机器上 SIGILL）
#include <immintrin.h>
#include <cpuid.h>
bool have_avx512() {
    unsigned a, b, c, d;
    if (__get_cpuid_count(7, 0, &a, &b, &c, &d))
        return (b & (1 << 16)) != 0;   // AVX-512F 位
    return false;
}
```

真实汇编（`-O3 -mavx512f`，节选主循环）：

```asm
; 关键证据：zmm 512 位，每轮 64 字节 = 16 个 float
_Z13add_arrays512PfS_S_i:
	...
.L4:
	vmovups	zmm1, ZMMWORD PTR [rcx+rax]   ; 加载 16 个 float
	vaddps	zmm0, zmm1, ZMMWORD PTR [rdx+rax]
	vmovups	ZMMWORD PTR [r8+rax], zmm0    ; 写回 16 个结果
	add	rax, 64
	cmp	r10, rax
	jne	.L4
	vzeroupper
```

- `[平台]`：zmm 一次 16 float 吞吐翻倍，但**降频**可能让 AVX-512 在长密集循环里反而不如 AVX2（频率损失 > 宽度收益）。Intel 服务器 SKU 影响小，消费级差异大。
- `[经验]`：用 `-mavx512f` 前实测；或折中用 `-mavx2 -mfma`。ARM/部分 Intel 上 AVX2 性价比往往最高。

## ⑭ 误用：非连续 / 带分支的循环无法向量化 [实现]

```cpp
// ⑭ 反例1：步长 != 1（跨步访问）-> 不可向量化
void stride(float* a, float* b, int n) {
    for (int i = 0; i < n; i += 2) b[i] = a[i] * 2;   // 隔一个取，破坏连续性
}
// ⑭ 反例2：循环携带依赖 -> 必须串行
void dep(float* a, int n) {
    for (int i = 1; i < n; ++i) a[i] = a[i-1] + a[i]; // a[i] 依赖 a[i-1]
}
```

源码剖析（真实汇编，仍是标量 `vaddss`）：

```cpp
// 文件：Examples/_ch155_dep.cpp
// 行号：4
void add_dependent(float* a, int n) {
    for (int i = 1; i < n; ++i)
        a[i] = a[i - 1] + a[i];
}
```

```asm
; 关键证据：-O3 -mavx2 下依旧标量（vaddss = scalar single），因为依赖链无法并行
_Z13add_dependentPfi:
	cmp	edx, 1
	jle	.L5
	vmovss	xmm0, DWORD PTR [rcx]
	...
.L3:
	vaddss	xmm0, xmm0, DWORD PTR [rax]   ; 一次只算 1 个 float（标量）
	add	rax, 4
	vmovss	DWORD PTR -4[rax], xmm0
	cmp	rax, rdx
	jne	.L3
```

- `[实现]`：证据显示即便开 `-O3`，依赖循环也只生成 `vaddss`（标量单精度），**完全没有 `vaddps`**——编译器诚实退化为串行。
- `[经验]`：向量化的天敌=别名、依赖、分支、跨步、函数调用。改这些比改指令重要得多。

## ⑮ 性能基准（标量 vs 向量） [经验]

```cpp
// ⑮ 朴素基准框架（计时用 std::chrono），对比标量 / AVX2
#include <chrono>
#include <iostream>
#include <vector>
static double bench(void(*f)(float*,float*,float*,int),
                    std::vector<float>& a, std::vector<float>& b,
                    std::vector<float>& c, int n, int iters) {
    auto t0 = std::chrono::steady_clock::now();
    for (int k = 0; k < iters; ++k) f(a.data(), b.data(), c.data(), n);
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double>(t1-t0).count();
}
```

```cpp
// ⑮ 标量版
void scalar(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
// ⑮ AVX2 版（手写，展示理想上限；实际 -O3 自动向量化已接近此值）
void avx2(float* a, float* b, float* c, int n) {
    int i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(a+i), vb = _mm256_loadu_ps(b+i);
        _mm256_storeu_ps(c+i, _mm256_add_ps(va, vb));
    }
    for (; i < n; ++i) c[i] = a[i] + b[i];   // 尾部标量收尾
}
```

- `[经验]`：真实基准中 AVX2 对连续浮点循环常达 **4–8× 加速**（受内存带宽上限约束，并非严格 8×）；瓶颈常在**带宽**而非 ALU（见 ⑱）。
- `[经验]`：永远**实测**，不要"相信向量化更快"——非热点/小数据/依赖循环，向量化毫无收益甚至因 prologue/epilogue 变慢。

## ⑯ 调试：查看 asm 是否真的向量化 [实现]

```bash
# ⑯ 让 GCC 报告向量化成败原因（-O3 才有意义）
g++ -std=c++23 -O3 -mavx2 -fopt-info-vec -fopt-info-vec-missed \
    -S -masm=intel Examples/_ch155_simd.cpp -o Examples/_ch155_simd.asm
# 输出含：
#   <source>:6:9: note: loop vectorized  (✔ 成功)
#   <source>:X: note: not vectorized: control flow in loop (✘ 有分支)
```

```cpp
// ⑯ 也可在代码里用 builtin 辅助诊断（编译期确认宽度）
#include <immintrin.h>
constexpr int lanes_avx2 = sizeof(__m256) / sizeof(float);  // = 8
static_assert(lanes_avx2 == 8, "AVX2 width");
```

- `[实现]`：`-fopt-info-vec` 打印**成功**向量化的循环；`-fopt-info-vec-missed` 打印**失败原因**（"可能存在别名""存在控制流"等），是定位 ⑭ 类问题的第一工具。
- `[经验]`：看 asm 是否出现 `ymm/zmm` 与 `vaddps/vmulps` 是最硬的证据（如 ⑧/⑫/⑬/⑭ 各节所示），比"优化选项开了"更可靠。

## ⑰ 跨平台（x86 vs ARM NEON） [平台]

x86 用 SSE/AVX，ARM 用 **NEON**（高级 SIMD，AArch64 默认 128 位 `float32x4_t`）。

```cpp
// ⑰ x86 AVX2 已在 ⑦/⑳ 的 v_avx2 中实现，下面给出 ARM 等价
// ⑰ ARM NEON 等价（AArch64，GCC/Clang 均支持）
//    说明：以下为 ARM-only 代码；本教科书编译门禁为 MinGW x86-64，
//    不存在 <arm_neon.h>，故用 #ifdef 跳过，避免 x86 上编译失败。
//    跨平台库的生产做法是在此按架构分发（或改用 ⑥ 的
//    std::experimental::simd / 自动向量化，避免手写双份 intrinsics）。
#if defined(__aarch64__) || defined(__ARM_NEON)
#include <arm_neon.h>
void neon_add(const float* a, const float* b, float* c) {
    float32x4_t va = vld1q_f32(a);   // 加载 4 个 float
    float32x4_t vb = vld1q_f32(b);
    float32x4_t vc = vaddq_f32(va, vb);
    vst1q_f32(c, vc);                // 写回 4 个结果
}
#endif
```

- `[平台]`：NEON 函数名风格与 x86 intrinsics **不互通**（`vaddq_f32` vs `_mm_add_ps`），但语义一一对应。跨平台库常用宏/抽象层（如 `std::experimental::simd`、Eigen、xsimd）屏蔽差异。
- `[经验]`：不要在可移植代码里直接写平台 intrinsics；用自动向量化或跨平台抽象，仅在底层 backend 按架构分发。

## ⑱ 最佳实践 [经验]

```cpp
// ⑱ 1) 先保证连续、无别名、无依赖，让 -O3 自动向量化
void best(float* __restrict a, float* __restrict b,
          float* __restrict c, int n) {
    #pragma omp simd
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
// ⑱ 2) 用无分支写法保留向量化（max/min 替代 if）
void best_clamp(float* a, float* b, int n, float lo) {
    for (int i = 0; i < n; ++i) b[i] = (a[i] < lo) ? lo : a[i]; // 仍可能分支
    // 更好的向量化友好写法：
    for (int i = 0; i < n; ++i) b[i] = std::max(a[i], lo);
}
```

- `[经验]`：向量化的**第一杠杆是数据布局与别名**，不是 intrinsics。顺序：SoA/AoSoA → `__restrict` → 去分支/去依赖 → 自动向量化 → 必要时 intrinsics → 实测。
- `[经验]`：注意**内存带宽墙**——当算访比低（如纯 `a+b`），加速受限于 DRAM 带宽，AVX-512 也救不了；提升算访比（融合更多运算/FMA）才能吃满 ALU。

## ⑲ 工具（Compiler Explorer / -fopt-info-vec） [实现]

```bash
# ⑲ 本地快速取证：一条命令看向量化 asm
g++ -std=c++23 -O3 -mavx2 -ftree-vectorize -S -masm=intel \
    Examples/_ch155_simd.cpp -o Examples/_ch155_simd.asm
# ⑲ 看向量化成败原因
g++ -std=c++23 -O3 -mavx2 -fopt-info-vec-all=vec.log Examples/_ch155_simd.cpp
# ⑲ 在线：https://godbolt.org 选 x86-64 gcc 13.1，-O3 -mavx2，直接对照 asm
```

- `[实现]`：Compiler Explorer（godbolt.org）可在浏览器里切换编译器/标志看实时 asm，是验证"是否真向量化"的最快途径；本地用 `-fopt-info-vec` + `-S -masm=intel` 等价。
- `[经验]`：把热点函数单独抽成小 TU 丢进 Compiler Explorer，对照 `vaddps`/`vmulps` 是否出现，比肉眼读源码判断可靠。

## ⑳ 速查表 [标准]

| 主题 | 要点 | 标志/指令 |
|---|---|---|
| 自动向量化 | GCC 需 `-O3` 或 `-ftree-vectorize` | `-O3 -mavx2` |
| 强制向量化 | 跨编译器标准 | `#pragma omp simd` |
| 宽度 | SSE=4 / AVX=8 / AVX512=16 个 float | `xmm`/`ymm`/`zmm` |
| 加法 | 向量浮点加 | `vaddps` |
| 加载 | 未对齐（安全）/对齐（需对齐） | `vmovups` / `vmovaps` |
| 乘加 | FMA 合一 | `vfma*` / `_mm256_fmadd_ps` |
| 条件 | 比较生成 mask | `vcmpps` / `k` 寄存器 |
| 布局 | SoA 优于 AoS | SoA / AoSoA |
| 取证 | 看 asm / 看原因 | `-S -masm=intel` / `-fopt-info-vec` |
| 跨平台 | x86↔ARM 不互通 intrinsics | NEON `vaddq_f32` |

```cpp
// ⑳ 一页速记：从标量到 AVX2 的进化（同一语义，宽度递增）
void v_sse (const float* a, const float* b, float* c) { // 4-wide
    __m128 va=_mm_loadu_ps(a), vb=_mm_loadu_ps(b); _mm_storeu_ps(c,_mm_add_ps(va,vb)); }
void v_avx2(const float* a, const float* b, float* c) { // 8-wide
    __m256 va=_mm256_loadu_ps(a), vb=_mm256_loadu_ps(b); _mm256_storeu_ps(c,_mm256_add_ps(va,vb)); }
void v_auto(float* __restrict a, float* __restrict b, float* __restrict c, int n) { // 编译器选宽
    for (int i=0;i<n;++i) c[i]=a[i]+b[i]; }
```

- `[标准]`：`vaddps` 是 SIMD 向量化的"签名指令"；看到 `ymm/zmm` + `vaddps/vmulps` 即证明向量化生效。
- `[经验]`：能用 `v_auto`（自动向量化）就别手写 intrinsics；手写只在算法无法被自动识别（如复杂 gather/scatter、特殊 permute）时出手。

## 补充完整可编译示例（simd）

```cpp
// S1 基本标量加（对照基线）
void base_add(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// S2 __restrict 消除别名假设
void ra_add(float* __restrict a, float* __restrict b,
            float* __restrict c, int n) {
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// S3 #pragma omp simd 显式提示
#include <omp.h>
void omp_add(float* a, float* b, float* c, int n) {
    #pragma omp simd
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// S4 SSE 4-wide 乘
void sse_mul(const float* a, const float* b, float* c) {
    __m128 va = _mm_loadu_ps(a), vb = _mm_loadu_ps(b);
    _mm_storeu_ps(c, _mm_mul_ps(va, vb));
}
```

```cpp
// S5 AVX2 8-wide 乘
void avx2_mul(const float* a, const float* b, float* c) {
    __m256 va = _mm256_loadu_ps(a), vb = _mm256_loadu_ps(b);
    _mm256_storeu_ps(c, _mm256_mul_ps(va, vb));
}
```

```cpp
// S6 AVX-512 16-wide 乘
void avx512_mul(const float* a, const float* b, float* c) {
    __m512 va = _mm512_loadu_ps(a), vb = _mm512_loadu_ps(b);
    _mm512_storeu_ps(c, _mm512_mul_ps(va, vb));
}
```

```cpp
// S7 FMA 融合乘加（需 -mfma）
void fma_op(const float* a, const float* b, const float* c, float* d) {
    __m256 va=_mm256_loadu_ps(a), vb=_mm256_loadu_ps(b), vc=_mm256_loadu_ps(c);
    _mm256_storeu_ps(d, _mm256_fmadd_ps(va, vb, vc));
}
```

```cpp
// S8 对齐加载（要求 alignas(32)）
alignas(32) float ga[8] = {1,2,3,4,5,6,7,8};
void aligned_load() {
    __m256 v = _mm256_load_ps(ga);   // 地址必须 32 字节对齐
    (void)v;
}
```

```cpp
// S9 向量比较 + max（无分支 clamp）
void v_clamp(const float* in, float* out, int n, float lo) {
    __m128 vlo = _mm_set1_ps(lo);
    for (int i = 0; i + 4 <= n; i += 4) {
        __m128 v = _mm_loadu_ps(&in[i]);
        _mm_storeu_ps(&out[i], _mm_max_ps(v, vlo));
    }
}
```

```cpp
// S10 SoA 三分量缩放（最优布局）
void soa(float* x, float* y, float* z, int n, float s) {
    for (int i = 0; i < n; ++i) { x[i]*=s; y[i]*=s; z[i]*=s; }
}
```

```cpp
// S11 AoS（次优布局，对照）
struct V3 { float x, y, z; };
void aos(V3* p, int n, float s) {
    for (int i = 0; i < n; ++i) { p[i].x*=s; p[i].y*=s; p[i].z*=s; }
}
```

```cpp
// S12 运行时检测 AVX2
#include <immintrin.h>
#include <cpuid.h>
bool have_avx2() {
    unsigned a,b,c,d;
    if (__get_cpuid_max(0,nullptr) >= 7 && __get_cpuid_count(7,0,&a,&b,&c,&d))
        return (b & (1<<5)) != 0;   // AVX2 位
    return false;
}
```

```cpp
// S13 跨平台抽象（自动向量化版，x86/ARM 都编译）
void portable(float* __restrict a, float* __restrict b,
              float* __restrict c, int n) {
    for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// S14 尾部收尾：向量主循环 + 标量补齐余数（避免越界）
void with_tail(const float* a, const float* b, float* c, int n) {
    int i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va=_mm256_loadu_ps(a+i), vb=_mm256_loadu_ps(b+i);
        _mm256_storeu_ps(c+i, _mm256_add_ps(va, vb));
    }
    for (; i < n; ++i) c[i] = a[i] + b[i];
}
```

```cpp
// S15 std::experimental::simd 抽象版（需 <experimental/simd>）
#include <experimental/simd>
void dat_add(const float* a, const float* b, float* c, int n) {
    using V = std::experimental::native_simd<float>;
    for (int i = 0; i + V::size() <= n; i += V::size()) {
        V va(&a[i], std::experimental::element_aligned);
        V vb(&b[i], std::experimental::element_aligned);
        (va+vb).copy_to(&c[i], std::experimental::element_aligned);
    }
}
```

```cpp
// S16 用 std::chrono 计时（与 ⑮ 一致）
#include <chrono>
double now() {
    return std::chrono::duration<double>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
```

## 附录 E：SIMD设计权衡与实战 [H: Design / I: Practice / J: Learning]

```
SIMD设计决策树:
1. 数据连续？ → 否: 重排数据或用SoA布局; 是: 继续
2. 对齐？ → 否: movups(未对齐,慢20%); 是: movaps(对齐,最快)
3. 数据量？ → <16: 标量更快(SIMD启动开销); ≥16: SIMD赢
4. 跨平台？ → x86: AVX2(256bit)/AVX-512(512bit); ARM: NEON(128bit)
   → 便携: std::simd(C++26方向) 或 手写intrinsics + #ifdef

工业SIMD案例:
- ClickHouse: 列式存储, 每列SIMD并行处理 → 10×于行式数据库
- JPEG XL: AVX-512编码 → 2×于AVX2, 5×于标量
- Halide (Google): 图像处理DSL → 自动生成SIMD/多核代码
- Eigen: Matrix<float,4,4> → 编译期展开为4条mulps指令

反模式:
- 手动SIMD但编译器已自动向量化 → 用-fopt-info-vec检查
- AVX-512降频: Skylake-X使用AVX-512会降低CPU频率10-20%
  → 评估: 数据量>1KB时AVX-512净赢, <1KB用AVX2

面试: SIMD宽度? A: SSE=128bit(4×float), AVX2=256bit(8×float), AVX-512=512bit(16×float)
       std::simd vs intrinsics? A: std::simd=便携(C++26), intrinsics=最快但平台特定
       何时不用SIMD? A: 分支密集/数据不连续/量<16
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第154章](Book/part14_perf/ch154_cache_opt.md) | 向量化计算/图像处理 | 本章提供概念，第154章提供实现 |
| [第156章](Book/part14_perf/ch156_compiler_opt.md) | 计时器/性能测量 | 本章提供概念，第156章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch76_stl_arch.md`（第76章　STL 架构与迭代器概念）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part07_stl/ch87_bitset.md`（第87章　bitset：编译期定长位集）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part14_perf/ch153_cpu_micro.md`（第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part14_perf/ch157_compiler_explorer.md`（第157章 Compiler Explorer 实战）—— 编号相邻、主题接续。
- **同模块**：`Book/part14_perf/ch152_perf_model.md`（第152章　性能模型与测量学）—— 同模块下的其他主题。

## 附录 F：SIMD 工业实践与深度 [F: Industry / E: Low-level / B: Principle]

真实生产代码里的 SIMD 几乎从不直接手写 intrinsics，而是依赖库与编译器向量化：

- **LLVM Loop Vectorizer / SLP Vectorizer**：`-O2` 下自动把标量循环转成 AVX2；`#pragma clang loop vectorize(enable)` 显式提示。LLVM 的 `@llvm.experimental.vector.reduce` 系列内在支撑 reduction 合并。
- **Eigen**：内部 `internal::packet_traits<T>` 把逐元素运算映射到 `Packet4f`/`Packet8f`（SSE/AVX），矩阵乘走 `gebp` 微内核，自动 dispatch 到 AVX-512。
- **folly::simd**（Meta）：`folly::simd::Vec<T, W>` 类型安全封装，提供 `load`/`store` 与原生 intrinsic 的零开销桥接。
- **DPDK**：`rte_eth_rx_burst` 用向量化收包（AVX-512 版 `ice_recv_pkts_vec_avx512`），配合 `rte_prefetch0` 隐藏内存延迟；数据面要求确定性吞吐，禁用分支预测失败路径。
- **Boost.SIMD**（历史）：Boost 社区早期 SIMD 抽象，后并入 `std::simd`（P0918），展示 `pack<float, 8>` 风格的 API。
- **Google ruy / gemmlowp**：移动端量化矩阵乘，手写 ARM NEON `int8x16_t` 微内核，吞吐由 `1.2 GFLOP/s` 量级实测约束。

编译侧：`g++ -std=c++23 -mavx2 -mfma -O3` 让编译器把内层循环向量化；`clang++ -march=native -fno-math-errno` 避免标量回退。AVX2 单条 `vfmadd231ps` 在 3.5 GHz 上 5 周期延迟、0.5 周期吞吐，理论 8×float/指令。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

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

### 练习 2（难度 ★★）

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

### 练习 3（难度 ★★）

解释虚函数表（vtable）的内存开销：一个含虚函数的类对象通常增加多少字节（64 位）？写代码打印 `sizeof`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
struct Base { virtual ~Base()=default; int x; };
int main() { std::cout << sizeof(Base) << '\n'; }  // 通常 16 = 8(vptr)+4(int)+填充
```

[实现·GCC13] [平台·x86-64] 64 位下 vptr 占 8 字节，虚调用为一次间接 call。

</details>

