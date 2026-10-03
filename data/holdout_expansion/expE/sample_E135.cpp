// sample_E135
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E135.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[2];
static std::atomic<Node*> top{nullptr};
static std::atomic<unsigned> ver{0};
static std::atomic<int> step{0}, stale_succ{0};
int main(){
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Node* p = top.load(std::memory_order_acquire);
    Node* nxt = p->next;
    unsigned v0 = ver.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 指针与版本号分处两个原子对象，校验与更新无法原子完成：
       在「读 p」「读 ver」「写 top」之间 ver 可能已被别人推进，校验形同虚设 ⇒ ABA 仍会发生 */
    if (ver.load(std::memory_order_acquire) == v0){
      stale_succ.fetch_add(1, std::memory_order_relaxed);
      Node* exp = p;
      top.compare_exchange_strong(exp, nxt, std::memory_order_acq_rel, std::memory_order_acquire);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E135 stale_succ=%d ver=%u\n", stale_succ.load(), ver.load());
  return 0;
}
