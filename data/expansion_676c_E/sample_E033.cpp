// sample_E033
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E033.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> seq{0};
static std::atomic<int> payload{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  payload.store(88, std::memory_order_relaxed);
  seq.store(1, std::memory_order_relaxed);
}
static void waiter(){
  wait_go();
  /*DEFECT: relaxed 轮询 seq：即使读到 1，payload 的写入也没有任何 synchronizes-with 保证*/
  while (seq.load(std::memory_order_relaxed) == 0){}
  std::printf("E033 payload=%d\n", payload.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), w(waiter);
  go.store(true, std::memory_order_release);
  p.join(); w.join();
  return 0;
}
