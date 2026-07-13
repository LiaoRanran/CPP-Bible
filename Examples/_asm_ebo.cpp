// ch52 EBO 真实布局/汇编提取源
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_ebo.cpp -o _asm_ebo.asm
#include <cstddef>

struct Empty {};                       // 空类，sizeof = 1（Itanium ABI 占位）
struct Derived : Empty { int x; };    // EBO：Empty 占 0 字节，x 在偏移 0
struct AsMember { Empty e; int x; };  // 作为成员：Empty 占 1 字节，x 在偏移 4（含 3 填充）

static_assert(sizeof(Derived) == sizeof(int));
static_assert(sizeof(AsMember) == 2 * sizeof(int));   // 含 Empty 占位 + 对齐填充

// 读取 Derived::x —— 应在偏移 0，证明空基类未占空间
int read_derived(Derived* p) { return p->x; }

// 读取 AsMember::x —— 应在偏移 4（Empty 占位 1 + 3 填充）
int read_member(AsMember* p) { return p->x; }

// offsetof 证据
constexpr std::size_t off_d = offsetof(Derived, x);   // 期望 0
constexpr std::size_t off_m = offsetof(AsMember, x);  // 期望 4
