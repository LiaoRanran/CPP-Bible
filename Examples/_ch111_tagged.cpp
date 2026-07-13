#include <atomic>
#include <cstdint>
#include <cstring>

// tagged pointer: 64 位地址 + 64 位版本号，打包成 __int128
struct TaggedPtr {
    void*        ptr;
    std::uint64_t tag;
};

static_assert(sizeof(__int128) == 16);
static_assert(sizeof(TaggedPtr) == 16);

using AtomicTagged = std::atomic<__int128>;

// 尝试把 (old.ptr, old.tag) 换成 (new_ptr, old.tag+1)
bool push_tagged(AtomicTagged& a, void* old_ptr, void* new_ptr) {
    TaggedPtr oldp{old_ptr, 0};
    __int128 old_v;
    std::memcpy(&old_v, &oldp, sizeof(old_v));
    TaggedPtr newp{new_ptr, 1};
    __int128 new_v;
    std::memcpy(&new_v, &newp, sizeof(new_v));
    return a.compare_exchange_strong(old_v, new_v,
                                      std::memory_order_acq_rel,
                                      std::memory_order_acquire);
}
