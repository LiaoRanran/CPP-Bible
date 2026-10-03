// sample_E001
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E001.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> data{0};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  data.store(42, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
}
static void consumer(){
  wait_go();
  /*DEFECT: relaxed 轮询 ready：与 release 存储之间没有 synchronizes-with，读到 true 也可能读到 data==0*/
  while(!ready.load(std::memory_order_relaxed)){}
  std::printf("E001 data=%d\n", data.load(std::memory_order_relaxed));
}
int main(){
  std::thread p(producer), c(consumer);
  go.store(true, std::memory_order_release);
  p.join(); c.join();
  return 0;
}
