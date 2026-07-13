// 文件：Examples/_ch128_shared_ptr.cpp
// 说明：不依赖 Boost/std::shared_ptr 的自包含引用计数指针，
//       演示 Boost.SmartPtr 与 std::shared_ptr 解决的核心机制（原子引用计数 + 析构）。
#include <atomic>
#include <cstdio>

struct ControlBlock {
    std::atomic<int> strong;
    int weak;
};

template <typename T>
class my_shared_ptr {
    T*           ptr_;
    ControlBlock* cb_;
public:
    explicit my_shared_ptr(T* p = nullptr)
        : ptr_(p), cb_(p ? new ControlBlock{1, 0} : nullptr) {}

    my_shared_ptr(const my_shared_ptr& o) noexcept
        : ptr_(o.ptr_), cb_(o.cb_) {
        if (cb_) cb_->strong.fetch_add(1, std::memory_order_relaxed);
    }

    ~my_shared_ptr() {
        if (cb_ && cb_->strong.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            delete ptr_;          // 最后一个持有者负责销毁对象
            delete cb_;           // 以及控制块
        }
    }

    int use_count() const noexcept {
        return cb_ ? cb_->strong.load(std::memory_order_acquire) : 0;
    }
    T* operator->() const noexcept { return ptr_; }
};

struct Widget { int id; };

int main() {
    my_shared_ptr<Widget> a(new Widget{42});
    my_shared_ptr<Widget> b = a;          // 拷贝：引用计数 +1
    int n = a.use_count() + b->id;        // 使用：n = 2 + 42 = 44
    return n;
}
