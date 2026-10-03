// sample_E113
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E113.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[4];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> pushes{0}, pops{0};
static Node* alloc_slot(int v){
  for (int i = 0; i < 4; ++i)
    if (arena[i].v == 0){ arena[i].v = v; arena[i].next = nullptr; return &arena[i]; }
  return nullptr;
}
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
  pushes.fetch_add(1, std::memory_order_relaxed);
}
static Node* pop(){
  Node* old = top.load(std::memory_order_acquire);
  while (old && !top.compare_exchange_weak(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  if (old) pops.fetch_add(1, std::memory_order_relaxed);
  return old;
}
int main(){
  push(alloc_slot(10));
  push(alloc_slot(20));
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: pop 的 CAS 只比较指针值，缺少版本号/tag：top 经历 A->B->A 后这次 CAS 会误成功 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire)){}
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* p = pop(); if (p) p->v = 0;          // 回收
  push(alloc_slot(30));                       // 复用
  step.store(2, std::memory_order_release);
  a.join();
  int count = 0; Node* it = top.load();
  while (it != nullptr && count < 8){ ++count; it = it->next; }
  std::printf("E113 reachable=%d pushes=%d pops=%d\n", count, pushes.load(), pops.load());
  return 0;
}
