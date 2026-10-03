// sample_E114
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E114.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node arena[3];
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> head_count{0};
static void push(Node* n){
  Node* old = top.load(std::memory_order_relaxed);
  do { n->next = old; }
  while (!top.compare_exchange_weak(old, n, std::memory_order_release, std::memory_order_relaxed));
  head_count.fetch_add(1, std::memory_order_relaxed);
}
int main(){
  Node* n1 = &arena[0]; n1->v = 1;
  Node* n2 = &arena[1]; n2->v = 2;
  push(n1); push(n2);
  std::thread a([&]{
    Node* expected = top.load(std::memory_order_acquire);
    Node* nxt = expected->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 两阶段 push 的「预留」阶段持有陈旧 expected：ABA 后 CAS 仍成功，nxt 已是过期的后继 */
    if (top.compare_exchange_strong(expected, nxt, std::memory_order_acq_rel, std::memory_order_acquire))
      head_count.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);   // top 变
  top.store(&arena[1], std::memory_order_release);   // top 又变回同一地址（A->B->A）
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E114 head_count=%d top_v=%d\n", head_count.load(), top.load()->v);
  return 0;
}
