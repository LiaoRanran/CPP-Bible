// sample_E117
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E117.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static Cell ring[4];
static std::atomic<Cell*> head{nullptr};
static std::atomic<Cell*> tail{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> drained{0};
static void reset_ring(){
  for (int i = 0; i < 4; ++i){ ring[i].v = 0; ring[i].next = nullptr; }
  head.store(&ring[0], std::memory_order_release);
  tail.store(&ring[3], std::memory_order_release);
  ring[3].next = &ring[0];
}
int main(){
  reset_ring();
  for (int i = 0; i < 4; ++i) ring[i].v = i + 1;
  std::thread a([&]{
    Cell* t = tail.load(std::memory_order_acquire);
    Cell* h = head.load(std::memory_order_acquire);
    (void)h;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: tail 的 CAS 没有版本号：槽位被回收再复用后 tail 回到同一地址，CAS 误判「未变」 */
    Cell* exp = t;
    if (tail.compare_exchange_strong(exp, exp->next, std::memory_order_acq_rel, std::memory_order_acquire))
      drained.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  tail.store(&ring[0], std::memory_order_release);
  tail.store(&ring[3], std::memory_order_release);   // 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E117 drained=%d head_v=%d\n", drained.load(), head.load()->v);
  return 0;
}
