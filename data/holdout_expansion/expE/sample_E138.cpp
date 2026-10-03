// sample_E138
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E138.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static std::atomic<Node*> top{nullptr};
static std::atomic<int> step{0}, retries{0};
static Node arena[2];
int main(){
  arena[0].v = 1; arena[0].next = nullptr;
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Node* expected = top.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    int guard = 0;
    /*DEFECT: 重试循环没有次数/状态校验，且 expected 会被 CAS 失败自动改写；
       ABA 期间一次「伪变化」会让循环把别人的后继当成自己的后继继续推进 */
    while (guard++ < 3){
      Node* nxt = expected->next;
      if (top.compare_exchange_weak(expected, nxt, std::memory_order_acq_rel, std::memory_order_acquire)) break;
      retries.fetch_add(1, std::memory_order_relaxed);
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  top.store(&arena[0], std::memory_order_release);
  arena[1].v = 2; arena[1].next = &arena[0];
  top.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E138 retries=%d top_v=%d\n", retries.load(), top.load()->v);
  return 0;
}
