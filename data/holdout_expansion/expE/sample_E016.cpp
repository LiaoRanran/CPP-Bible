// sample_E016
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E016.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> body{0};
static std::atomic<bool> flag{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  body.store(64, std::memory_order_relaxed);
  /*DEFECT: seq_cst fence 被夹在 relaxed 载荷写与 relaxed 标志写之间，fence 两侧都不是 release 操作，fence 形同虚设*/
  std::atomic_thread_fence(std::memory_order_seq_cst);
  flag.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  while(!flag.load(std::memory_order_acquire)){}
  std::printf("E016 body=%d\n", body.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
