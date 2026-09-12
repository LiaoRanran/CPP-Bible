// 受控实验 ATOM-UB-ALIAS（UB 类）：严格别名——通过不兼容类型指针访问对象是**未定义行为**
//
// 标准态度（对比另一类"灰色地带"）：
//   * 求值顺序 unspecified  → 标准给了**合法结果集合**，两种顺序都合法，程序不会崩，只是不可依赖；
//   * 严格别名 strict aliasing → 标准**完全不再要求**任何行为（[basic.lval]），优化器可以假定
//     "不同类型的指针不指向同一对象"，并据此删除/重排访问。
// 本夹具把两者放在同一份文件里对照，正是为了教"unspecified ≠ UB"。
//
// 观测设计（为什么不直接断言某个数值）：
//   UB 的**结果**按定义不可预测，所以**不能**把"返回值"写成 expected（那会变成"我有幸跑出来的值"）。
//   本夹具改为观测**同一对象的两种读法是否自洽**：
//     r_func  = 函数返回值（严格别名下优化器可把它算成常量）
//     r_mem   = 从内存 memcpy 读回的实际内容
//   二者**不一致**即证明优化器利用了"不别名"假设 → UB 被实证触发。
//
// 证伪对照：`-fno-strict-aliasing` 关闭该假设后，两种读法应恢复一致。
//   （与"假移动对照"同理：没有它，就无法区分"UB 真被利用"与"我算错了"。）
//
// 复现：
//   g++ -std=c++23 -O2 Examples/_atom_strict_alias.cpp -o build/_replay_alias.exe && build/_replay_alias.exe
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_strict_alias.cpp -o Examples/_atom_strict_alias.asm

#include <cstdio>
#include <cstring>

// 防折叠汇点：让结果必须被真实计算。
// ⚠️ 必须是 64 位的 `long long`，两次踩坑都留痕：
//   ① 首版用 `volatile int`：累加 1073741824×2 时**自身整数溢出**，UBSan 报
//      "signed integer overflow" → 证据卡判 refute:sanitizer_reported（由卡的 sanitizer 校验抓到）；
//   ② 第二版改用 `long` **仍然溢出**——因为 **Windows 是 LLP64（`long` = 32 位）**，
//      只有 Linux/macOS（LP64）才是 64 位；asm 实测此处仍是 `mov DWORD PTR`，一眼看穿。
// 结论：跨平台要 64 位就用 `long long`。教训——**研究 UB 的夹具自己最容易踩 UB**，
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
    *fp = 2.0f;                       // UB：[basic/lval] 不允许通过 float 访问 int 对象
    int r = 0;
    std::memcpy(&r, &x, sizeof r);    // 用 memcpy 读回，避免再引入第二处 UB
    return r;
}

// ── 合规路径（对照）：全程 memcpy，不违反别名规则 ─────────────────────────
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
    // 第三次踩坑（经典 C 陷阱）：`int + int` 会在 **int 域内**先溢出，即使目标是 long long。
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
