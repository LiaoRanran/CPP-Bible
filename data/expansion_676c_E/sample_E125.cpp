// sample_E125
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E125.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> head{nullptr};
static std::atomic<void*> hazard{nullptr};
static std::atomic<int> step{0};
int main(){
  Node* n1 = new Node{1, nullptr};
  head.store(n1, std::memory_order_release);
  std::thread t([&]{
    /*DEFECT: hazard pointer 的协议要求「读指针 → 发布 hazard → **重新校验指针**」；
       这里读指针之后立刻解引用，登记与校验都没有做 ⇒ reclaimer 完全可以在
       读指针与解引用之间把节点回收并复用同一地址 */
    Node* p = head.load(std::memory_order_acquire);
    hazard.store(p, std::memory_order_release);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: p 此刻已被 reclaimer 释放（它无视了已发布的 hazard），解引用即 UAF */
    std::printf("E125 v=%d\n", p->v);
    /*DEFECT: 事后才校验 head 是否仍等于 p —— 校验早已晚于使用（check-after-use）*/
    if (head.load(std::memory_order_acquire) == p) std::printf("E125 still valid\n");
  });
  while (step.load(std::memory_order_acquire) != 1){}
  /*DEFECT: reclaimer 侧完全不扫描 hazard 集合：只要摘下 head 就 delete */
  Node* dead = head.exchange(nullptr, std::memory_order_acq_rel);
  delete dead;
  head.store(new Node{8, nullptr});
  step.store(2, std::memory_order_release);
  t.join();
  std::printf("E125 hazard=%d\n", hazard.load() != nullptr);
  return 0;
}
