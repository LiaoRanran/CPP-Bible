// [redacted]
//
// 标准态度（对比另一类"灰色地带"）：
//   * 求值顺序 unspecified  → 标准给了**合法结果集合**，两种顺序都合法，程序不会崩，只是不可依赖；
// [redacted]
//     "不同类型的指针不指向同一对象"，并据此删除/重排访问。
// [redacted]
//
// 观测设计（为什么不直接断言某个数值）：
// [redacted]
//   本夹具改为观测**同一对象的两种读法是否自洽**：
//     r_func  = 函数返回值（严格别名下优化器可把它算成常量）
//     r_mem   = 从内存 memcpy 读回的实际内容
// [redacted]
//
// 证伪对照：`-fno-strict-aliasing` 关闭该假设后，两种读法应恢复一致。
// [redacted]
//
// 复现：
// [redacted]
// [redacted]

#include <cstdio>
#include <cstring>

// 防折叠汇点：让结果必须被真实计算。
// ⚠️ 必须是 64 位的 `long long`，两次踩坑都留痕：
// [redacted]
// [redacted]
//   ② 第二版改用 `long` **仍然溢出**——因为 **Windows 是 LLP64（`long` = 32 位）**，
//      只有 Linux/macOS（LP64）才是 64 位；asm 实测此处仍是 `mov DWORD PTR`，一眼看穿。
// [redacted]
// 而且"换个更宽的类型"这件事还必须顺带过一遍数据模型差异（本项目的老坑）。
static volatile long long g_sink = 0;

// ── 形态 A：写不同、读同一 ──────────────────────────────────────────────
// 严格别名下，编译器可假定 *ip 与 *fp 不指向同一对象 → `return *ip` 可被替换为常量 1。
__attribute__((noinline)) int alias_kill(int* ip, float* fp) {
    *ip = 1;
    *fp = 2.0f;
    return *ip;
}

// ── 形态 B：直接以 float* 写 int 对象，再以 int 读回 ─────────────────────
__attribute__((noinline)) int write_via_float_ptr() {
    alignas(float) int x = 0;
    float* fp = reinterpret_cast<float*>(&x);
    *fp = 2.0f;                       // [redacted]
    int r = 0;
    std::memcpy(&r, &x, sizeof r);    // [redacted]
    return r;
}

// [redacted]
__attribute__((noinline)) int write_via_memcpy() {
    int x = 0;
    const float v = 2.0f;
    std::memcpy(&x, &v, sizeof x);
    int r = 0;
    std::memcpy(&r, &x, sizeof r);
    return r;
}

int main() {
    // 形态 A
    alignas(float) int a = 0;
    const int a_func = alias_kill(&a, reinterpret_cast<float*>(&a));
    int a_mem = 0;
    std::memcpy(&a_mem, &a, sizeof a_mem);
    // [redacted]
    // 必须**先提升再相加**。三次坑都留痕：int 宽度 → long 在 LLP64 下仍是 32 位 → 提升时机。
    g_sink = static_cast<long long>(a_func) + static_cast<long long>(a_mem);

    // 形态 B（与合规路径同一意图）
    const int b_ub = write_via_float_ptr();
    const int b_ok = write_via_memcpy();
    g_sink = g_sink + b_ub + b_ok;

    std::printf("A 函数返回=%d 内存实际=%d 自洽=%s\n",
                a_func, a_mem, (a_func == a_mem) ? "是" : "否");
    std::printf("B UB路径=%d 合规路径=%d 一致=%s\n",
                b_ub, b_ok, (b_ub == b_ok) ? "是" : "否");
    //@ A 函数返回=?? 内存实际=?? 自洽=??
    //@ B UB路径=?? 合规路径=?? 一致=??
    return 0;
}
