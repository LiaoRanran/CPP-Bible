// Examples/_atom_shared_deleter_erase.cpp
// 服务 ATOM-MEM-UNIQUE-002（第二卡）：shared_ptr 的删除器被**类型擦除**进控制块——
// 与 unique_ptr 相反：语言层面不存在 shared_ptr<T, D>；删除器经构造函数按值注入、拷贝进控制块，
// 被同一控制块的所有持有者共享；对象大小恒为两个指针（与删除器无关）。
#include <cstddef>
#include <cstdio>
#include <memory>
#include <utility>

// ---- 观测点（volatile：-O2 不可折叠，观测通路必须活着）----
static volatile int g_deleter_copies = 0;    // 删除器被**拷贝**的次数
static volatile int g_deleter_calls = 0;     // 删除器被**调用**的次数
static volatile int g_tag_seen = -1;         // 被调用实例的 tag（证明调用的是哪一份删除器）
static volatile long g_obj_new = 0;          // 堆分配次数（擦除的运行期代价：控制块）

// 计数全部堆分配（对象与控制块都经这里），供③的差分对照使用
void* operator new(std::size_t n) { g_obj_new = g_obj_new + 1; return std::malloc(n); }
void  operator delete(void* p) noexcept { std::free(p); }
void  operator delete(void* p, std::size_t) noexcept { operator delete(p); }

struct TagDel {
    int tag = 0;
    TagDel() = default;
    explicit TagDel(int t) : tag(t) {}
    TagDel(const TagDel& o) : tag(o.tag) { g_deleter_copies = g_deleter_copies + 1; }
    TagDel(TagDel&& o) noexcept : tag(o.tag) {}          // 移动不算拷贝
    void operator()(int* p) const noexcept {
        g_deleter_calls = g_deleter_calls + 1;
        g_tag_seen = tag;
        delete p;
    }
};

int main() {
    // ① 类型层面：删除器不进 shared_ptr 的类型参数（对象大小与删除器无关）
    {
        std::shared_ptr<int> sp_default(new int(1));
        std::shared_ptr<int> sp_tagdel(new int(2), TagDel(5));
        std::printf("sizeof shared_ptr default=%d\n", (int)sizeof(sp_default));
        std::printf("sizeof shared_ptr with stateful deleter=%d\n", (int)sizeof(sp_tagdel));
        int equal = (sizeof(sp_default) == sizeof(sp_tagdel)) ? 1 : 0;
        std::printf("shared_ptr sizes equal=%d\n", equal);
    }

    // ② 删除器被拷贝进控制块（一次），此后被所有持有者共享（拷贝不再发生）
    {
        TagDel d(99);
        int copies0 = g_deleter_copies;
        int calls0 = g_deleter_calls;
        std::shared_ptr<int> sp(new int(3), d);
        int copies1 = g_deleter_copies;
        auto sp2 = sp;
        auto sp3 = sp;
        int copies2 = g_deleter_copies;
        std::printf("deleter copies on ctor=%d\n", copies1 - copies0);
        std::printf("deleter copies on share=%d\n", copies2 - copies1);
        sp.reset();
        sp2.reset();
        sp3.reset();                                  // 最后一个引用释放才调用删除器
        std::printf("deleter calls after all reset=%d\n", (int)g_deleter_calls - calls0);
        std::printf("deleter tag seen=%d\n", (int)g_tag_seen);
    }

    // ③ 擦除的运行期代价：shared_ptr 需要**控制块**（额外堆分配），unique_ptr 不需要；
    //    make_shared 把对象与控制块合并成一次分配。
    //    红队 S2 拦截记录：原版拿"unique_ptr 传右值(0 拷贝) vs shared_ptr 传左值(1 拷贝)"当对照，
    //    差异只来自实参**值类别**，与"类型参数 vs 擦除"无关 ⇒ 已换成与值类别无关的分配计数。
    {
        long a0 = g_obj_new;
        {
            std::shared_ptr<int> sp(new int(4));
            auto sp2 = sp;
            (void)sp2;
        }
        long a1 = g_obj_new;
        {
            std::shared_ptr<int> sp = std::make_shared<int>(5);
            auto sp2 = sp;
            (void)sp2;
        }
        long a2 = g_obj_new;
        {
            std::unique_ptr<int, TagDel> up(new int(6), TagDel(7));
            auto up2 = std::move(up);
            (void)up2;
        }
        long a3 = g_obj_new;
        std::printf("shared_ptr from raw ptr allocs=%d\n", (int)(a1 - a0));
        std::printf("make_shared allocs=%d\n", (int)(a2 - a1));
        std::printf("unique_ptr allocs=%d\n", (int)(a3 - a2));
    }

    // ④ 擦除的语义后果：同一个静态类型 shared_ptr<int> 的变量可先后持有不同删除器
    {
        std::shared_ptr<int> sp;
        sp = std::shared_ptr<int>(new int(8), TagDel(11));
        sp.reset();
        std::printf("tag seen after reset #1=%d\n", (int)g_tag_seen);
        sp = std::shared_ptr<int>(new int(9), TagDel(22));
        sp.reset();
        std::printf("tag seen after reset #2=%d\n", (int)g_tag_seen);
    }
    return 0;
}
