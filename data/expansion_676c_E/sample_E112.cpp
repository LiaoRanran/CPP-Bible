// sample_E112
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E112.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0};
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
  push(new Node{1, nullptr});
  push(new Node{2, nullptr});
  std::thread a([&]{
    Node* old = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: ABA 后 old 指向已释放节点，读取 old->next 参与 CAS 就是在读悬垂内存 */
    Node* nxt = old->next;
    /*DEFECT: 继续解引用已 delete 的对象 */
    std::printf("E112 stale v=%d\n", old->v);
    top.compare_exchange_strong(old, nxt, std::memory_order_acq_rel, std::memory_order_acquire);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = pop();
  delete dead;                                    // 制造 A->B->A 的同时释放内存
  push(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  return 0;
}
