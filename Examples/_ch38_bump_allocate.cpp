// ch38 allocator —— 真实反汇编证据源：monotonic_buffer_resource 的「指针碰撞」内核
// 极简 bump allocator：只增不减，分配 = 推进指针；这正是 §⑩ 的核心，无链表/无 free。
#include <cstddef>
void* bump_allocate(char*& cur, char* end, size_t n) __attribute__((used));
void* bump_allocate(char*& cur, char* end, size_t n) {
    char* p = cur;
    if (p + n > end) return nullptr;   // 缓冲耗尽 → 返回空（真实实现会向上游要新缓冲）
    cur = p + n;                        // bump：仅推进指针
    return p;
}
