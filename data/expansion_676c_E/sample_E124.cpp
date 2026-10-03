// sample_E124
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E124.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* a1 = new Node{1, nullptr};
  Node* a2 = new Node{2, a1};
  head.store(a2, std::memory_order_release);
  std::thread t([&]{
    Node* cur = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 无 hazard pointer / 无 epoch：读到的 cur 在下一步之前可能已被删除并复用，
       下面两行对已释放内存的读写是 use-after-free */
    std::printf("E124 v=%d\n", cur->v);
    Node* nxt = cur->next;
    std::printf("E124 next_v=%d\n", nxt ? nxt->v : -1);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;                                  // 释放正在被遍历的节点
  head.store(new Node{7, nullptr});             // 地址复用
  step.store(2, std::memory_order_release);
  t.join();
  return 0;
}
