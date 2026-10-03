// sample_E115
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E115.json)

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
    /*DEFECT: ABA 后 CAS 误成功，old 实际已被别人 pop 并 delete；此处 delete 同一块内存 */
    if (top.compare_exchange_strong(old, old->next, std::memory_order_acq_rel, std::memory_order_acquire))
      delete old;                       // 二次释放
    std::printf("E115 popped stale\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = pop();
  delete dead;                          /*DEFECT: 先释放，再让新节点复用同一地址，
     于是 top 的指针值又回到 old —— 这正是 ABA 的「B」那一半 */
  push(new Node{3, nullptr});
  step.store(2, std::memory_order_release);
  a.join();
  delete dead;
  return 0;
}
