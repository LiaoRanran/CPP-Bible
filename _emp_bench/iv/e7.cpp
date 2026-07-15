#include <cstddef>
#include <array>
#include <new>
template <std::size_t BlockSize, std::size_t BlockCount>
class FixedPool {
    union Slot { unsigned char data[BlockSize]; Slot* next; };
    alignas(std::max_align_t) std::array<Slot, BlockCount> pool_;
    Slot* free_ = nullptr;
public:
    FixedPool(){ for(std::size_t i=0;i<BlockCount;++i){ pool_[i].next=free_; free_=&pool_[i]; } }
    void* allocate() noexcept { if(!free_) return nullptr; Slot* s=free_; free_=s->next; return s; }
    void deallocate(void* p) noexcept { Slot* s=static_cast<Slot*>(p); s->next=free_; free_=s; }
};
int main(){ FixedPool<32,8> p; void* a=p.allocate(); p.deallocate(a); return a?0:1; }
