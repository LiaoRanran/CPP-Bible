// sample_E127
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E127.json)

#include <atomic>
#include <thread>
#include <cstdio>
#include <vector>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n2 = new Node{2, nullptr};
  Node* n1 = new Node{1, n2};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    /*DEFECT: 读侧把 hazard 登记在自己线程的栈变量上，但 reclaimer 从不扫描 hazard 集合：
       「保护」是单向宣告，不构成任何互斥 */
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 此时 p 已被释放并可能被复用，下面读 p->next 是 use-after-free + ABA */
    std::printf("E127 v=%d next=%d\n", p->v, p->next ? p->next->v : -1);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  delete n2;                              /*DEFECT: 直接 delete 链上的第二个节点，完全不做退休扫描 */
  head.store(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
