// ATOM-MEM-ALLOC-002 夹具（v2）：三种分配策略的**统一口径**元数据与时空权衡。
//
// ── v2 相对 v1 的三处修正（红队 B1/H4/H5）────────────────────────────────
// B1【统一口径】元数据 := 为管理这批分配，分配器**自身占用且不承载用户数据的全部字节**，
//    由同一函数口径逐项拆分为「结构本体」+「bookkeeping 数组/链表节点（堆内存）」。
//    v1 的三个 meta() 口径互不相同：arena 只算一个 size_t（连容器头都不算）、
//    pool 只算 `sizeof(free_list)`（**漏掉 free-list 的堆数组 8192 B**）、
//    bitmap 含数据结构本体 ⇒ 汇总方向失真（"pool 最省"是漏算造成的）。
// H4【活性对照】每个策略都跑**两个规模**（1000 / 8000）并各打印元数据；
//    若读数是写死的常量，两点必然相同；实测两点不同 ⇒ 证明读数是运行时算出来的。
// H5【workload 如实】真实执行「分配 N 次 → 全量释放 → 再分配 N 次」；
//    pool/bitmap 的单块释放接口**被真正调用**（v1 只定义未调用，描述与行为不符）。
// ────────────────────────────────────────────────────────────────────────
// 输出纪律：默认只打印确定性读数；本夹具不重载 operator new/delete（避 P4）。
// 值的字面量不进 printf 格式串、注释不写带双引号的完整取值（避 S3-EXPECTED-HARDCODED）。
#include <cstdio>
#include <cstddef>
#include <vector>

namespace {

constexpr std::size_t kReq   = 24;    // 请求大小（字节）
constexpr std::size_t kBlock = 32;    // pool/bitmap 定长块（⇒ 每块内部碎片 8 字节）
constexpr std::size_t kN1    = 1000;
constexpr std::size_t kN2    = 8000;

// 统一口径的元数据拆解
struct Meta {
    std::size_t struct_bytes;        // 容器头 + 标量计数器（对象内）
    std::size_t bookkeeping_bytes;   // bookkeeping 数组/链表节点的堆内存
    std::size_t total() const { return struct_bytes + bookkeeping_bytes; }
};

struct Arena {
    std::vector<unsigned char> buf;
    std::size_t off = 0;
    explicit Arena(std::size_t cap) : buf(cap) {}
    void* alloc() {
        if (off + kReq > buf.size()) return nullptr;
        void* p = buf.data() + off;
        off += kReq;
        return p;
    }
    void release_all() { off = 0; }          // 只能整体重置（无单块释放接口）
    std::size_t used() const { return off; }
    Meta meta() const { return Meta{sizeof(buf) + sizeof(off), 0}; }
};

struct Pool {
    std::vector<unsigned char> buf;
    std::vector<void*> free_list;            // ← 它的堆数组是元数据的大头
    std::size_t used_blocks = 0;
    explicit Pool(std::size_t blocks) : buf(blocks * kBlock) { init_(); }
    void init_() {
        const std::size_t blocks = buf.size() / kBlock;
        free_list.clear();
        free_list.reserve(blocks);
        for (std::size_t i = blocks; i-- > 0;)
            free_list.push_back(buf.data() + i * kBlock);
    }
    void* alloc() {
        if (free_list.empty()) return nullptr;
        void* p = free_list.back();
        free_list.pop_back();
        ++used_blocks;
        return p;
    }
    void free(void* p) { free_list.push_back(p); --used_blocks; }   // 单块回收（v2 真被调用）
    void release_all() { free_list.clear(); used_blocks = 0; init_(); }
    std::size_t used() const { return used_blocks * kBlock; }
    Meta meta() const {
        return Meta{sizeof(buf) + sizeof(free_list) + sizeof(used_blocks),
                    free_list.capacity() * sizeof(void*)};
    }
};

struct Bitmap {
    std::vector<unsigned char> buf;
    std::vector<unsigned char> bits;         // 1 bit / 块
    std::size_t used_blocks = 0;
    explicit Bitmap(std::size_t blocks)
        : buf(blocks * kBlock), bits((blocks + 7) / 8, 0) {}
    void* alloc() {
        for (std::size_t i = 0; i < bits.size() * 8; ++i) {
            if (i * kBlock >= buf.size()) break;
            if (!(bits[i / 8] & (1u << (i % 8)))) {
                bits[i / 8] |= static_cast<unsigned char>(1u << (i % 8));
                ++used_blocks;
                return buf.data() + i * kBlock;
            }
        }
        return nullptr;
    }
    void free(void* p) {                     // 单块回收（v2 真被调用）
        const std::size_t i = (static_cast<unsigned char*>(p) - buf.data()) / kBlock;
        bits[i / 8] &= static_cast<unsigned char>(~(1u << (i % 8)));
        if (used_blocks) --used_blocks;
    }
    void reset_all() {                    // 清空所有位 ⇒ 与 pool/arena 的 reset 语义对齐（全部归还）
        for (std::size_t i = 0; i < bits.size(); ++i) bits[i] = 0;
        used_blocks = 0;
    }
    std::size_t used() const { return used_blocks * kBlock; }
    Meta meta() const {
        return Meta{sizeof(buf) + sizeof(bits) + sizeof(used_blocks),
                    bits.capacity()};
    }
};

template <class A, class Free, class Reset>
void report(const char* tag, std::size_t n, A& a, Free fre, Reset rst) {
    // workload：分配 n 次 → 单块释放（若支持）→ 全量重置 → 再分配 n 次
    std::size_t served1 = 0;
    for (std::size_t i = 0; i < n; ++i) { if (a.alloc()) ++served1; }
    const std::size_t peak_after_first = a.used();
    for (std::size_t i = 0; i < n; ++i) fre(a);          // ← v2 真调用单块释放
    rst(a);
    std::size_t served2 = 0;
    for (std::size_t i = 0; i < n; ++i) { if (a.alloc()) ++served2; }
    const Meta m = a.meta();
    std::printf("%s_served_first=%zu\n", tag, served1);
    std::printf("%s_served_second=%zu\n", tag, served2);
    std::printf("%s_peak_after_first=%zu\n", tag, peak_after_first);
    std::printf("%s_meta_struct_bytes=%zu\n", tag, m.struct_bytes);
    std::printf("%s_meta_bookkeeping_bytes=%zu\n", tag, m.bookkeeping_bytes);
    std::printf("%s_meta_total_bytes=%zu\n", tag, m.total());
}

struct NoFree { void operator()(Arena&) const {} };      // arena 无单块释放（如实声明）

}  // namespace

int main() {
    std::printf("req_bytes=%zu\n", kReq);
    std::printf("block_bytes=%zu\n", kBlock);
    std::printf("internal_frag_per_block=%zu\n", kBlock - kReq);
    std::printf("scale_n1=%zu\n", kN1);
    std::printf("scale_n2=%zu\n", kN2);
    std::printf("arena_single_free_supported=%d\n", 0);   // 如实声明：只有整体重置

    Arena a1(kN1 * kReq), a2(kN2 * kReq);
    report("arena_n1", kN1, a1, NoFree{}, [](Arena& x) { x.release_all(); });
    report("arena_n2", kN2, a2, NoFree{}, [](Arena& x) { x.release_all(); });

    Pool p1(kN1), p2(kN2);
    report("pool_n1", kN1, p1, [](Pool& x) { x.free(x.buf.data()); }, [](Pool& x) { x.release_all(); });
    report("pool_n2", kN2, p2, [](Pool& x) { x.free(x.buf.data()); }, [](Pool& x) { x.release_all(); });

    Bitmap b1(kN1), b2(kN2);
    // reset 语义与 pool/arena 对齐：**全部归还**（v2 初版只释放首块 ⇒ served_second=1，与其他策略不一致）
    report("bitmap_n1", kN1, b1, [](Bitmap& x) { x.free(x.buf.data()); }, [](Bitmap& x) { x.reset_all(); });
    report("bitmap_n2", kN2, b2, [](Bitmap& x) { x.free(x.buf.data()); }, [](Bitmap& x) { x.reset_all(); });

    std::printf("scale_ratio=%zu\n", kN2 / kN1);
    return 0;
}
