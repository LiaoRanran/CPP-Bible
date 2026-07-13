// 自包含分区式分配器等价：bump-pointer arena
// 展示 Chromium PartitionAlloc 单分区的 O(1) 分配思想：仅移动指针，无系统调用。
#include <cstddef>
#include <cstdint>

struct Arena {
    char* begin;
    char* cur;
    char* end;
    void init(void* buf, size_t sz) {
        begin = cur = (char*)buf;
        end = begin + sz;
    }
    // O(1) 分配：bump 指针即可（PartitionAlloc 的真实路径也类似走 fast 分支）
    void* alloc(size_t sz) {
        char* p = cur;
        cur += sz;
        if (cur > end) return nullptr;   // 简化：忽略对齐与越界细分
        return p;
    }
};

// 热点：连续分配三个对象，用于观察 alloc 是否被内联为纯指针加法
void* make_three(Arena& a) {
    void* p1 = a.alloc(16);
    void* p2 = a.alloc(16);
    void* p3 = a.alloc(32);
    (void)p2; (void)p3;
    return p1;
}

int main() {
    static char buffer[4096];
    Arena a;
    a.init(buffer, sizeof(buffer));
    void* p = make_three(a);
    // 校验分配确实落在 buffer 区间内（返回是否成功，确定性退出码）
    return (p >= buffer && p < buffer + sizeof(buffer)) ? 0 : 1;
}
