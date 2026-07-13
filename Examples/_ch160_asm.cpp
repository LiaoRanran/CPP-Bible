// 文件：Examples/_ch160_asm.cpp
// 行号：1
// 汇编取证源：allocate() 热路径，用于 g++ -O2 -S -masm=intel 提取
#include <cstddef>
#include <vector>
#include <new>

class Pool {
    struct FN { FN* next; };
    FN* head_ = nullptr;
    std::vector<void*> chunks_;
    size_t bs_;
    void grow() {
        void* m = ::operator new(bs_ * 4096);
        chunks_.push_back(m);
        auto* b = static_cast<std::byte*>(m);
        for (size_t i = 0; i < 4096; ++i) {
            auto* n = reinterpret_cast<FN*>(b + i * bs_);
            n->next = head_; head_ = n;
        }
    }
public:
    explicit Pool(size_t bs) : bs_(bs) {}
    ~Pool() { for (void* c : chunks_) ::operator delete(c); }
    void* allocate() {                 // __attribute__((noinline)) 便于定位
        if (!head_) grow();
        FN* n = head_; head_ = n->next; return n;
    }
};

void* hot_allocate(Pool& p) { return p.allocate(); }

int main() {
    Pool p(64);
    void* x = hot_allocate(p);
    (void)x;
    return 0;
}
