// sample_E134
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E134.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n1 = new Node{1, nullptr};
  Node* n2 = new Node{2, n1};
  top.store(n2, std::memory_order_release);
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: ABA 后 old 已被 delete：往 old->next 写字段是 use-after-free **写** */
    old->next = nullptr;
    /*DEFECT: 再把陈旧指针挂回链表头，链表从此指向已释放内存 */
    Node* exp = top.load(std::memory_order_acquire);
    do { old->next = exp; }
    while (!top.compare_exchange_weak(exp, old, std::memory_order_release, std::memory_order_relaxed));
    std::printf("E134 relinked stale\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = top.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  top.store(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  return 0;
}
