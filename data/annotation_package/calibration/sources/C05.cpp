// sample_E007
// [redacted]
// severity: high
// [redacted]
// expected_verdict: miss
// [redacted]
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E007.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> payload{0};
static std::atomic<bool> stage1{false}, stage2{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  payload.store(11, std::memory_order_relaxed);
  stage1.store(true, std::memory_order_release);
  payload.store(22, std::memory_order_relaxed);
  /* [redacted]*/
  stage2.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!stage2.load(std::memory_order_acquire)){}
  std::printf("E007 payload=%d\n", payload.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
