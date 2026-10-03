// sample_E130
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E130.json)

#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<int> step{0}, grace{0};
int main(){
  head.store(new Node{1, nullptr}, std::memory_order_release);
  std::thread r([&]{
    /*DEFECT: 「RCU 读侧」什么保护都没做（没有 read_lock / 没有 hazard / 没有 epoch）：
         读侧随时可能被 reclaim 线程搬走并复用同一地址 ⇒ ABA / UAF 语义上完全敞开 */
    Node* p = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    std::printf("E130 v=%d\n", p->v);
    grace.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  /*DEFECT: reclaim 不等读侧 grace period（无条件 sleep 代替），随后复用地址 */
  std::this_thread::sleep_for(std::chrono::milliseconds(1));
  head.store(new Node{1, nullptr});
  step.store(2, std::memory_order_release);
  r.join();
  delete dead;
  std::printf("E130 grace=%d\n", grace.load());
  return 0;
}
