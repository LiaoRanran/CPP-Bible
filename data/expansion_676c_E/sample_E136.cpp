// sample_E136
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E136.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, removed{0}, added{0};
int main(){
  for (int i = 0; i < 3; ++i){ arena[i].v = 0; arena[i].next = nullptr; }
  arena[0].v = 1;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    /*DEFECT: 先摘链（CAS）再改链，中间非原子 ⇒ 摘下的节点在窗口内可被复用并再次挂链 */
    Node* old = top.load(std::memory_order_acquire);
    Node* nxt = old->next;
    if (top.compare_exchange_strong(old, nxt, std::memory_order_acq_rel, std::memory_order_acquire))
      removed.fetch_add(1, std::memory_order_relaxed);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 窗口内 old 已被别人 push 回同一个槽位（值又变回同一个地址），
       这里再 CAS 摘一次 ⇒ 同一个节点被摘两次 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      removed.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[2], std::memory_order_release);
  added.fetch_add(1, std::memory_order_relaxed);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);   // 同址重新挂链
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E136 removed=%d added=%d\n", removed.load(), added.load());
  return 0;
}
