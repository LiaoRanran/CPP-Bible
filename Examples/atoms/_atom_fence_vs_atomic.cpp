// ATOM-CONC-001 夹具：__atomic_signal_fence ≠ __atomic_thread_fence（"屏障"不是一种东西）
//
// ── 为什么零 #include ────────────────────────────────────────────────────
// riscv64-unknown-elf-g++ 是裸机工具链：**连 <cstdio> 都没有**（实测
// `fatal error: cstdio: No such file or directory`）。为了让同一份源码能同时喂给
// MinGW / Linux g++-14 / riscv64 三侧（312 §4.4 风险表只预警了 <atomic>，实际更窄），
// 这里只用编译器内建（__atomic_*、__ATOMIC_SEQ_CST）与手写 printf 声明。
//
// ── 为什么每个函数独占全局变量 ──────────────────────────────────────────
// ATOM-CONC-001 要说清的是"**某个函数体内**有没有 load / 有没有屏障指令"。
// 2026-09-12 起 artifact_assert 已支持**符号区间语义**（contains_in / absent_in：
// `<symbol>:` → 下一个列 0 标签或 .cfi_endproc/.seh_endproc），本卡即以区间断言为准。
// 独占命名仍然保留，作为**第二层保险**：区间切分一旦退化（例如又只认列 0 的收尾伪指令），
// 全局形态下的短读（`s_p_b` / `s_sf_b` …）还能兜住最关键的几条断言。
// 与之配套：main **不直接 load** 这些标志（置位走 noinline setter 的 store），于是
//     "区间内 absent(s_xx_b)"  ≡  "该函数体内没有 load"。
//
// ── 本轮实测（GCC 15.3 -O2，MinGW x86-64）确立的方向 ─────────────────────
//   ① spin_plain        ：循环**连同标志读取一起被整段删除**
//                          （函数体只剩 `mov eax, s_p_a[rip]; ret`，区间内无 s_p_b）
//   ② spin_signal_fence ：**循环被保留**——而 signal_fence 是**零指令**的：
//                          区间内有 `.L8: mov eax, s_sf_b[rip]; test; je .L8`,
//                          但一条屏障指令都没有。
//   ③ spin_with_fence   ：**循环被保留**——seq_cst thread_fence 在 x86-64 编译成
//                          `lock or QWORD PTR [rsp], 0`（**一次真实内存写**）。
//   ④ spin_volatile     ：volatile 访问保留（活性对照：证明"消除"不是观测通路坏了）
//   ⑤ spin_fence_outside：屏障挪到**循环之外**（同全局形态、同函数）⇒
//                          **循环又被整段删除**（区间内只有 `mov eax, s_o_a[rip]; ret`）。
// ② 与"零成本的屏障拦不住优化"的直觉相反，是本原子的落点：**只要循环体里有屏障
// （哪怕它零指令），"无副作用的（可能不终止的）循环"这一前提就不再成立**——C++
// [intro.progress] 只允许把无副作用的死循环当成 UB 删掉；屏障是同步操作，循环不再
// 满足该前提，于是必须保留。也就是说"能不能阻止消除"与"屏障强不强"无关，
// 差别只在指令层。这正是"**屏障 ≠ 原子类型**"：屏障约束的是**顺序**，不给普通变量
// 提供原子性（signal_fence 甚至对 CPU 零约束）。
//
// ⑤ 是②的机制隔离对照：把同一个屏障从循环体里挪到循环之前，若循环**又**被删掉，
// 就证明起作用的不是"函数里存在屏障"，而是"**循环体里有屏障**"（否决"编译器只是
// 看到函数里有 barrier 就不敢动手"这一竞争解释）。

extern "C" int printf(const char *, ...);

// ── writer 对照：普通写 / 普通写，中间分别放 signal_fence 与 thread_fence
int w_sf_a = 0;   // 仅 writer_signal_fence 引用
int w_sf_b = 0;   // 仅 writer_signal_fence 引用
int w_tf_a = 0;   // 仅 writer_thread_fence 引用
int w_tf_b = 0;   // 仅 writer_thread_fence 引用

// ── spin 对照：四种"等标志"，各自独占一组全局
int s_p_a = 0;    // 仅 spin_plain 引用
int s_p_b = 0;    // 仅 spin_plain 读取（main 只做 store）
int s_sf_a = 0;   // 仅 spin_signal_fence 引用
int s_sf_b = 0;   // 仅 spin_signal_fence 读取
int s_f_a = 0;    // 仅 spin_with_fence 引用
int s_f_b = 0;    // 仅 spin_with_fence 读取
volatile int s_v_a = 0;   // 仅 spin_volatile 引用（全局自身 volatile）
volatile int s_v_b = 0;   // 仅 spin_volatile 读取
int s_o_a = 0;    // 仅 spin_fence_outside 引用
int s_o_b = 0;    // 仅 spin_fence_outside 读取

// 置位器：**唯一**写这些标志的地方。返回值不用来观测（避免把 load 引进 main）。
__attribute__((noinline)) void set_all_flags(int v)
{
    s_p_b = v;
    s_sf_b = v;
    s_f_b = v;
    s_v_b = v;
    s_o_b = v;
    // 给"被读的数据"以互不相同的非零值：运行期打印 7/8/9/10/11 即证明观测通路活着
    s_p_a = 7;
    s_sf_a = 8;
    s_f_a = 9;
    s_v_a = 10;
    s_o_a = 11;
    w_sf_a = 1;
    w_tf_a = 1;
}

// 普通写 + 普通写，中间是**编译期**屏障：期望产出的机器码里没有任何屏障指令
__attribute__((noinline)) int writer_signal_fence()
{
    w_sf_a = 1;
    __atomic_signal_fence(__ATOMIC_SEQ_CST);
    w_sf_b = 2;
    return w_sf_a + w_sf_b;
}

// 普通写 + 普通写，中间是**硬件**屏障（x86-64 上编译为 lock 前缀空操作）
__attribute__((noinline)) int writer_thread_fence()
{
    w_tf_a = 1;
    __atomic_thread_fence(__ATOMIC_SEQ_CST);
    w_tf_b = 2;
    return w_tf_a + w_tf_b;
}

// 无屏障、无 volatile：-O2 判定循环不变 ⇒ 整循环被消除
__attribute__((noinline)) int spin_plain()
{
    while (!s_p_b) {
    }
    return s_p_a;
}

// 循环体里放**编译期**屏障：零指令，但仍足以保住整个循环（实测②）
__attribute__((noinline)) int spin_signal_fence()
{
    while (!s_sf_b) {
        __atomic_signal_fence(__ATOMIC_SEQ_CST);
    }
    return s_sf_a;
}

// 循环体里放**硬件**屏障：在 x86-64 上产生真实内存写 ⇒ 循环被保留（实测）
__attribute__((noinline)) int spin_with_fence()
{
    while (!s_f_b) {
        __atomic_thread_fence(__ATOMIC_SEQ_CST);
    }
    return s_f_a;
}

// volatile 读取：强制每次迭代真实访存（活性对照 + 有界兜底，保证不挂死）
__attribute__((noinline)) int spin_volatile()
{
    unsigned bound = 1000000;
    while (!s_v_b && --bound > 0) {
    }
    return s_v_a;
}

// 机制隔离对照：**同一个屏障，挪到循环之外**（全局形态与 ② 完全同构）
__attribute__((noinline)) int spin_fence_outside()
{
    __atomic_signal_fence(__ATOMIC_SEQ_CST);   // 屏障在循环之外
    while (!s_o_b) {
    }
    return s_o_a;
}

int main()
{
    set_all_flags(1);                  // 先置位再调用：即使某侧不消除也不会挂死
    int r_p = spin_plain();
    int r_sf = spin_signal_fence();
    int r_f = spin_with_fence();
    int r_v = spin_volatile();
    int r_o = spin_fence_outside();
    int r_wsf = writer_signal_fence();
    int r_wtf = writer_thread_fence();

    printf("spin_plain_ret=%d|spin_signal_fence_ret=%d|spin_with_fence_ret=%d|spin_volatile_ret=%d\n",
           r_p, r_sf, r_f, r_v);
    printf("spin_fence_outside_ret=%d|writer_signal_fence_ret=%d|writer_thread_fence_ret=%d\n",
           r_o, r_wsf, r_wtf);
    printf("functions_present=7|spin_volatile_engaged=%d\n", (r_v != 0) ? 1 : 0);
    return 0;
}
