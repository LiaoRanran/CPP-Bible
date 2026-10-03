// sample_E129
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E129.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Block { int idx; Block* next; };
static Block pool[3];
static std::atomic<Block*> freelist{nullptr};
static std::atomic<int> step{0}, allocs{0}, frees{0};
int main(){
  for (int i = 0; i < 3; ++i){ pool[i].idx = i; pool[i].next = (i + 1 < 3) ? &pool[i+1] : nullptr; }
  freelist.store(&pool[0], std::memory_order_release);
  std::thread a([&]{
    Block* head = freelist.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: freelist 分配没有版本号：head 槽位被 free 再 alloc 走一圈后回到同一地址，
       CAS 误成功 ⇒ 同一 block 被两个持有者同时分配（double ownership） */
    if (freelist.compare_exchange_strong(head, head->next, std::memory_order_acq_rel, std::memory_order_acquire))
      allocs.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  freelist.store(&pool[1], std::memory_order_release);   // 分配掉 pool[0]
  frees.fetch_add(1, std::memory_order_relaxed);
  freelist.store(&pool[0], std::memory_order_release);   // 释放回同一地址 ⇒ ABA
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E129 allocs=%d frees=%d\n", allocs.load(), frees.load());
  return 0;
}
