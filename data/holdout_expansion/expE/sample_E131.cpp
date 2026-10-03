// sample_E131
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E131.json)

#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
struct Node { int v; int payload[4]; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n = new Node{1, {1, 2, 3, 4}};
  head.store(n, std::memory_order_release);
  std::thread r([&]{
    /*DEFECT: 读侧不做任何保护就长期持有指针 */
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: reclaim 已经 delete 了 p：下面读 payload 是 use-after-free */
    int s = 0;
    for (int i = 0; i < 4; ++i) s += p->payload[i];
    std::printf("E131 sum=%d\n", s);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;                                  /* 立即回收：不给读侧任何窗口 */
  head.store(new Node{1, {1, 2, 3, 4}});
  step.store(2, std::memory_order_release);
  r.join();
  return 0;
}
