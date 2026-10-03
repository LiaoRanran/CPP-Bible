// sample_E014
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E014.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> body{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  body.store(31, std::memory_order_relaxed);
  /*DEFECT: relaxed fence 不提供 release 语义，且其后的 flag.store 也是 relaxed：无任何同步*/
  std::atomic_thread_fence(std::memory_order_relaxed);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_acquire)){}
  std::printf("E014 body=%d\n", body.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
