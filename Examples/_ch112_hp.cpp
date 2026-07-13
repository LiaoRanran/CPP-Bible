// Hazard Pointer 取证源：读者登记 + 回收者扫描
#include <atomic>
#include <cstddef>

struct Node { int val; Node* next; };

constexpr int MAX_HP = 64;
alignas(64) std::atomic<void*> g_hp[MAX_HP];   // 全局 Hazard Pointer 数组

struct Retired { void* ptr; Retired* next; };
std::atomic<Retired*> g_retired{nullptr};

// 读者：把 src 当前值登记进 slot 号 HP，返回受保护的指针
extern "C" void* hp_protect(std::atomic<void*>* src, int slot) {
    void* p;
    do {
        p = src->load(std::memory_order_acquire);
        g_hp[slot].store(p, std::memory_order_seq_cst);
    } while (p != src->load(std::memory_order_acquire));
    return p;
}

// 读者：离开临界区，清除登记
extern "C" void hp_clear(int slot) {
    g_hp[slot].store(nullptr, std::memory_order_release);
}

// 回收者：扫描全局 HP 表，未被保护的 retired 才真正 delete
extern "C" void hp_scan_and_reclaim() {
    Retired* head = g_retired.exchange(nullptr, std::memory_order_acquire);
    Retired* keep = nullptr;
    while (head) {
        Retired* nxt = head->next;
        bool hazard = false;
        for (int i = 0; i < MAX_HP; ++i) {
            if (g_hp[i].load(std::memory_order_acquire) == head->ptr) {
                hazard = true;
                break;
            }
        }
        if (hazard) {
            head->next = keep;
            keep = head;
        } else {
            delete static_cast<Node*>(head->ptr);
            delete head;
        }
        head = nxt;
    }
    if (keep) {
        Retired* tail = keep;
        while (tail->next) tail = tail->next;
        tail->next = g_retired.load(std::memory_order_relaxed);
        g_retired.store(keep, std::memory_order_release);
    }
}
