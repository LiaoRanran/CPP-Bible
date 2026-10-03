// sample_E128
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E128.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<long> ver{0};
static std::atomic<int> step{0}, ops{0};
int main(){
  for (int i = 0; i < 3; ++i){ arena[i].v = 0; arena[i].next = nullptr; }
  Node* n1 = &arena[0]; n1->v = 1;
  Node* n2 = &arena[1]; n2->v = 2; n2->next = n1;
  top.store(n2, std::memory_order_release);
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 明明有 ver 计数器却没把它和指针打包进同一个原子字（缺 tagged pointer）：
       CAS 只比较指针，ver 的存在不提供任何保护 ⇒ A->B->A 后误成功 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){
      ops.fetch_add(1, std::memory_order_relaxed);
      ver.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  arena[1].v = 0;
  top.store(n1, std::memory_order_release);
  arena[1].v = 2; arena[1].next = n1;
  top.store(n2, std::memory_order_release);      // top 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E128 ops=%d ver=%ld top_v=%d\n", ops.load(), ver.load(), top.load()->v);
  return 0;
}
