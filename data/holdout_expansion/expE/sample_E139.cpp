// sample_E139
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E139.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Block { int tag; int data; Block* next; };
static std::atomic<Block*> freelist{nullptr};
static std::atomic<Block*> published{nullptr};
static std::atomic<int> step{0};
int main(){
  Block* b1 = new Block{1, 111, nullptr};
  freelist.store(b1, std::memory_order_release);
  published.store(b1, std::memory_order_release);
  std::thread t([&]{
    Block* b = published.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 读侧仍在使用 b；reclaim 已把它 delete 并让新对象复用同一地址，
       这里读到的 tag/data 属于另一个对象（ABA 的典型表现） */
    std::printf("E139 tag=%d data=%d\n", b->tag, b->data);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Block* old = freelist.exchange(nullptr, std::memory_order_acq_rel);
  delete old;                                     /*DEFECT: 立即回收，无 grace period */
  freelist.store(new Block{2, 222, nullptr});     /* 很可能复用同一地址 */
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
