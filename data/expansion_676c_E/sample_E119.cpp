// sample_E119
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E119.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; };
static Cell ring[3];
static std::atomic<Cell*> head{nullptr};
static std::atomic<int> step{0}, empties{0}, nonempties{0};
int main(){
  head.store(&ring[0], std::memory_order_release);
  ring[0].v = 5;
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 用陈旧 h 判断「队列是否为空」：head 经历 A->B->A 后两次观测无法区分，
       于是把「刚被放回的元素」当成新元素消费，或把空队列当成非空 */
    if (h != nullptr) nonempties.fetch_add(1, std::memory_order_relaxed);
    else empties.fetch_add(1, std::memory_order_relaxed);
    std::printf("E119 h_v=%d\n", h->v);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&ring[1], std::memory_order_release);
  head.store(&ring[0], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E119 empty=%d nonempty=%d\n", empties.load(), nonempties.load());
  return 0;
}
