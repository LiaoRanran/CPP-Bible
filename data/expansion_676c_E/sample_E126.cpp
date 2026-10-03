// sample_E126
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E126.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0}, reclaimed{0};
static void reclaim(Node* n){
  /*DEFECT: 回收路径完全无视已发布的 hazard：只要自己摘下 head 就 delete，
     不检查是否有人在读它 ⇒ 读侧必然出现 ABA / UAF */
  Node* exp = head.load(std::memory_order_acquire);
  if (head.compare_exchange_strong(exp, n->next, std::memory_order_acq_rel, std::memory_order_acquire)){
    delete n;
    reclaimed.fetch_add(1, std::memory_order_relaxed);
  }
}
int main(){
  Node* n1 = new Node{1, nullptr};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    /*DEFECT: 读侧只发布 hazard、从不再校验 head：一旦删除线程在两步之间回收并复用，
       这里就会消费到「同地址不同对象」 */
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    std::printf("E126 v=%d\n", p->v);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  reclaim(head.load(std::memory_order_acquire));
  head.store(new Node{2, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E126 reclaimed=%d\n", reclaimed.load());
  return 0;
}
