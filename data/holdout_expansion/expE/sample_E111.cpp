// sample_E111
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E111.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> live{0};            // 存活节点数（业务不变量）
static Node* alloc_slot(int v){
  for (int i = 0; i < 3; ++i)
    if (arena[i].v == 0){ arena[i].v = v; arena[i].next = nullptr; live.fetch_add(1); return &arena[i]; }
  return nullptr;
}
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  return old;
}
int main(){
  push(alloc_slot(1));
  push(alloc_slot(2));
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用陈旧的 old 做 CAS。期间 top 经历了 A->B->A（同一槽位被回收再复用），
       CAS 只比较指针值，误判为「没变」而成功 ⇒ 新节点被从链表里抹掉 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      std::printf("E111 CAS succeeded on stale pointer\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* p = pop(); live.fetch_sub(1); p->v = 0;     // 回收槽位
  push(alloc_slot(3));                              // 复用同一槽位 ⇒ top 回到同一地址
  step.store(2, std::memory_order_release);
  a.join();
  int count = 0; Node* it = top.load();
  while (it != nullptr && count < 8){ ++count; it = it->next; }
  std::printf("E111 reachable=%d live=%d\n", count, live.load());
  return 0;
}
