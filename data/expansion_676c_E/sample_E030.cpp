// sample_E030
// defect_type: memory_order
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E030.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> in_flight{0};
static std::atomic<long> total{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void task(){
  wait_go();
  /*DEFECT: 准入判断与计数增减全用 relaxed：relaxed 不建立顺序，限流逻辑在弱内存序下可超限*/
  while (in_flight.fetch_add(1, std::memory_order_relaxed) > 4) {}
  total.fetch_add(1, std::memory_order_relaxed);
  in_flight.fetch_sub(1, std::memory_order_relaxed);
}
int main(){
  std::thread a(task), b(task), c(task), d(task), e(task);
  go.store(true, std::memory_order_release);
  a.join(); b.join(); c.join(); d.join(); e.join();
  std::printf("E030 total=%ld\n", total.load(std::memory_order_relaxed));
  return 0;
}
